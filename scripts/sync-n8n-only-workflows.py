#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
n8nのみに存在するワークフローをプロジェクトに取得
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

def get_n8n_workflows(api_key):
    """n8nから全ワークフロー一覧を取得"""
    base_url = "https://hadayalab.app.n8n.cloud"
    api_endpoint = f"{base_url}/api/v1/workflows"

    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(api_endpoint, headers=headers, timeout=10)
        response.raise_for_status()

        result = response.json()

        if "data" in result:
            workflows = result["data"]
        else:
            workflows = result if isinstance(result, list) else []

        return workflows

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to list workflows: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return []

def get_workflow_details(api_key, workflow_id):
    """n8nからワークフローの詳細を取得"""
    base_url = "https://hadayalab.app.n8n.cloud"
    api_endpoint = f"{base_url}/api/v1/workflows/{workflow_id}"

    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

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

def get_local_workflow_names():
    """プロジェクト内のワークフロー名を取得"""
    import glob
    workflows_dir = "workflows"
    workflow_files = glob.glob(os.path.join(workflows_dir, "*.json"))

    local_names = set()
    for filepath in workflow_files:
        filename = os.path.basename(filepath)
        if filename in ["README.md", "workflow-index.md"]:
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                workflow = json.load(f)
                workflow_name = workflow.get("name", filename.replace(".json", ""))
                local_names.add(workflow_name)
        except Exception:
            pass

    return local_names

if __name__ == "__main__":
    print("=" * 60)
    print("n8nのみに存在するワークフローをプロジェクトに取得")
    print("=" * 60)
    print()

    # InfisicalからAPIキーを取得
    print("[INFO] Getting N8N_API_KEY from Infisical...")
    api_key = get_infisical_secret("N8N_API_KEY")

    if not api_key:
        print("[ERROR] Failed to get N8N_API_KEY from Infisical")
        sys.exit(1)

    print(f"[OK] N8N_API_KEY retrieved (preview: {api_key[:20]}...)\n")

    # n8nからワークフロー一覧を取得
    print("[INFO] Fetching workflows from n8n Cloud...")
    n8n_workflows = get_n8n_workflows(api_key)
    print(f"[OK] Found {len(n8n_workflows)} workflows in n8n\n")

    # ローカルのワークフロー名を取得
    local_names = get_local_workflow_names()

    # n8nのみに存在するワークフローを特定
    n8n_only_workflows = []
    for wf in n8n_workflows:
        wf_name = wf.get("name")
        if wf_name not in local_names:
            n8n_only_workflows.append(wf)

    print(f"[INFO] Found {len(n8n_only_workflows)} workflows that exist only in n8n\n")

    # 各ワークフローを取得して保存
    for wf_info in n8n_only_workflows:
        workflow_name = wf_info.get("name")
        workflow_id = wf_info.get("id")

        print(f"[INFO] Fetching workflow: {workflow_name} (ID: {workflow_id})")
        workflow_details = get_workflow_details(api_key, workflow_id)

        if not workflow_details:
            print(f"[WARNING] Failed to get details for {workflow_name}")
            continue

        # ファイル名を生成（ワークフロー名をファイル名に変換）
        safe_filename = workflow_name.lower().replace(" ", "-").replace("/", "-")
        safe_filename = "".join(c for c in safe_filename if c.isalnum() or c in ("-", "_"))
        filepath = f"workflows/{safe_filename}.json"

        save_workflow_to_file(workflow_details, filepath)
        print(f"  ID: {workflow_id}")
        print(f"  Active: {workflow_details.get('active', False)}\n")

    print("=" * 60)
    print(f"[SUCCESS] Synced {len(n8n_only_workflows)} workflows to project!")
    print("=" * 60)












