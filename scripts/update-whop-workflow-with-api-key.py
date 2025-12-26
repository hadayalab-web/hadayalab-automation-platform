#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Whop APIキーをワークフローに直接設定するスクリプト
"""
import json
import subprocess
import sys
import requests

# Infisical設定
INFISICAL_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
PROJECT_ID = "446f131c-be8d-45e5-a83a-4154e34501a5"

def get_infisical_secret(secret_name):
    """Infisicalからシークレットを取得"""
    try:
        result = subprocess.run(
            ["infisical", "secrets", "get", secret_name, "--token", INFISICAL_TOKEN, "--projectId", PROJECT_ID, "--output", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        secrets = json.loads(output)
        if secrets and len(secrets) > 0:
            return secrets[0]["secretValue"]
        return None
    except Exception as e:
        print(f"[ERROR] Failed to get {secret_name} from Infisical: {e}")
        return None

def update_workflow_with_api_key(workflow_path, api_key):
    """ワークフローJSONを更新してAPIキーを直接設定"""
    print(f"[INFO] Reading workflow file: {workflow_path}")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # APIキーをBearer形式に
    bearer_token = f"Bearer {api_key}"

    # 各HTTP Requestノードを更新
    http_nodes = [
        "http-get-members-1",
        "http-get-member-1",
        "http-cancel-membership-1",
        "http-reactivate-membership-1"
    ]

    updated_count = 0
    for node in workflow["nodes"]:
        if node["id"] in http_nodes:
            # 認証情報の参照を削除
            if "credentials" in node:
                del node["credentials"]

            # 認証タイプを変更
            node["parameters"]["authentication"] = "none"
            if "genericAuthType" in node["parameters"]:
                del node["parameters"]["genericAuthType"]

            # ヘッダーに直接APIキーを設定
            if "options" not in node["parameters"]:
                node["parameters"]["options"] = {}
            if "headers" not in node["parameters"]["options"]:
                node["parameters"]["options"]["headers"] = {}

            node["parameters"]["options"]["headers"]["Authorization"] = bearer_token

            updated_count += 1
            print(f"[OK] Updated node: {node['name']}")

    print(f"\n[INFO] Updated {updated_count} HTTP Request nodes")

    # 更新されたワークフローを保存
    output_path = workflow_path.replace(".json", "-with-api-key.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"[OK] Updated workflow saved to: {output_path}")

    return output_path

def update_workflow_in_n8n(workflow_id, updated_workflow_path, api_key):
    """n8n Cloudのワークフローを更新"""
    base_url = "https://hadayalab.app.n8n.cloud"
    api_endpoint = f"{base_url}/api/v1/workflows/{workflow_id}"

    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    print(f"\n[INFO] Reading updated workflow file: {updated_workflow_path}")
    with open(updated_workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # ペイロードを準備
    payload = {
        "name": workflow["name"],
        "nodes": workflow["nodes"],
        "connections": workflow["connections"],
        "settings": workflow.get("settings", {}),
        "staticData": workflow.get("staticData")
    }

    print(f"[INFO] Updating workflow in n8n Cloud: {workflow_id}")

    try:
        response = requests.put(api_endpoint, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        if "data" in result:
            workflow_data = result["data"]
        else:
            workflow_data = result

        print(f"\n[OK] Workflow updated successfully!")
        print(f"Workflow ID: {workflow_data['id']}")
        print(f"Workflow Name: {workflow_data['name']}")
        print(f"URL: {base_url}/workflow/{workflow_data['id']}")

        return True

    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Failed to update workflow: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return False

def main():
    print("=" * 60)
    print("Whopワークフロー自動設定")
    print("=" * 60)
    print("\n")

    # InfisicalからWhop APIキーを取得
    print("[STEP 1] Getting Whop API Key from Infisical...")
    whop_api_key = get_infisical_secret("WHOP_API_KEY")
    if not whop_api_key or whop_api_key == "*not found*":
        whop_api_key = get_infisical_secret("whop_api_key")
    if not whop_api_key or whop_api_key == "*not found*":
        whop_api_key = get_infisical_secret("WHOP")

    if not whop_api_key or whop_api_key == "*not found*":
        print("[ERROR] Whop API Key not found in Infisical")
        sys.exit(1)

    print(f"[OK] Whop API Key retrieved (preview: {whop_api_key[:20]}...)\n")

    # Infisicalからn8n APIキーを取得
    print("[STEP 2] Getting N8N_API_KEY from Infisical...")
    n8n_api_key = get_infisical_secret("N8N_API_KEY")

    if not n8n_api_key:
        print("[ERROR] Failed to get N8N_API_KEY from Infisical")
        sys.exit(1)

    print(f"[OK] N8N_API_KEY retrieved\n")

    # ワークフローを更新
    workflow_path = "workflows/whop-control.json"
    workflow_id = "3LYMmEXrRpSVhuhE"

    print("[STEP 3] Updating workflow JSON with API key...")
    updated_path = update_workflow_with_api_key(workflow_path, whop_api_key)

    print("\n[STEP 4] Updating workflow in n8n Cloud...")
    if update_workflow_in_n8n(workflow_id, updated_path, n8n_api_key):
        print("\n" + "=" * 60)
        print("設定完了！")
        print("=" * 60)
        print("\n[INFO] ワークフローが更新されました")
        print("[INFO] テスト実行してください:")
        print("  python scripts/test-whop-workflow.py")
    else:
        print("\n[ERROR] ワークフローの更新に失敗しました")
        sys.exit(1)

if __name__ == "__main__":
    main()














