#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
n8nからwhop-controlワークフローを取得してプロジェクトに保存
"""
import requests
import json
import subprocess
import sys
import os

# UTF-8エンコーディング設定
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

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

def get_workflow_by_name(api_key, workflow_name):
    """n8nからワークフロー名でワークフローを取得"""
    base_url = "https://hadayalab.app.n8n.cloud"
    api_endpoint = f"{base_url}/api/v1/workflows"

    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    print(f"[INFO] Fetching workflows from n8n Cloud...")

    try:
        response = requests.get(api_endpoint, headers=headers, timeout=10)
        response.raise_for_status()

        result = response.json()

        if "data" in result:
            workflows = result["data"]
        else:
            workflows = result if isinstance(result, list) else []

        # 指定された名前のワークフローを検索
        target_workflow = None
        for wf in workflows:
            if wf.get("name") == workflow_name:
                target_workflow = wf
                break

        if not target_workflow:
            print(f"[ERROR] Workflow '{workflow_name}' not found in n8n")
            print(f"[INFO] Available workflows:")
            for wf in workflows:
                print(f"  - {wf.get('name')} (ID: {wf.get('id')})")
            return None

        print(f"[OK] Found workflow: {target_workflow.get('name')} (ID: {target_workflow.get('id')})")
        return target_workflow

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to list workflows: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return None

def get_workflow_details(api_key, workflow_id):
    """n8nからワークフローの詳細を取得"""
    base_url = "https://hadayalab.app.n8n.cloud"
    api_endpoint = f"{base_url}/api/v1/workflows/{workflow_id}"

    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    print(f"[INFO] Fetching workflow details...")

    try:
        response = requests.get(api_endpoint, headers=headers, timeout=10)
        response.raise_for_status()

        result = response.json()

        if "data" in result:
            workflow = result["data"]
        else:
            workflow = result

        return workflow

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to get workflow details: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return None

def save_workflow_to_file(workflow, filepath):
    """ワークフローをJSONファイルに保存"""
    # ワークフローをクリーンアップ（n8n固有のフィールドを除外）
    clean_workflow = {
        "name": workflow.get("name"),
        "nodes": workflow.get("nodes", []),
        "connections": workflow.get("connections", {}),
        "settings": workflow.get("settings", {}),
        "staticData": workflow.get("staticData", {}),
        "tags": workflow.get("tags", []),
        "triggerCount": workflow.get("triggerCount", 0),
        "versionId": workflow.get("versionId")
    }

    # ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(clean_workflow, f, indent=2, ensure_ascii=False)

    print(f"[OK] Workflow saved to: {filepath}")

if __name__ == "__main__":
    # InfisicalからAPIキーを取得
    print("[INFO] Getting N8N_API_KEY from Infisical...")
    api_key = get_infisical_secret("N8N_API_KEY")

    if not api_key:
        print("[ERROR] Failed to get N8N_API_KEY from Infisical")
        sys.exit(1)

    print(f"[OK] N8N_API_KEY retrieved (preview: {api_key[:20]}...)\n")

    # whop-controlワークフローを取得
    workflow_name = "whop-control"
    workflow_info = get_workflow_by_name(api_key, workflow_name)

    if not workflow_info:
        sys.exit(1)

    # ワークフローの詳細を取得
    workflow_id = workflow_info.get("id")
    workflow_details = get_workflow_details(api_key, workflow_id)

    if not workflow_details:
        sys.exit(1)

    # プロジェクトに保存
    filepath = "workflows/whop-control.json"
    save_workflow_to_file(workflow_details, filepath)

    print(f"\n[SUCCESS] Workflow '{workflow_name}' synced to project successfully!")
    print(f"  File: {filepath}")
    print(f"  ID: {workflow_id}")
    print(f"  Active: {workflow_details.get('active', False)}")












