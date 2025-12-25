#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
n8nからワークフローを削除
"""
import requests
import subprocess
import sys

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
        import json
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

    try:
        response = requests.get(api_endpoint, headers=headers, timeout=10)
        response.raise_for_status()

        result = response.json()

        if "data" in result:
            workflows = result["data"]
        else:
            workflows = result if isinstance(result, list) else []

        for wf in workflows:
            if wf.get("name") == workflow_name:
                return wf

        return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to list workflows: {e}")
        return None

def delete_workflow(api_key, workflow_id):
    """n8nからワークフローを削除"""
    base_url = "https://hadayalab.app.n8n.cloud"
    api_endpoint = f"{base_url}/api/v1/workflows/{workflow_id}"

    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.delete(api_endpoint, headers=headers, timeout=10)
        response.raise_for_status()
        return True

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to delete workflow: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return False

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python delete-workflow-from-n8n.py <workflow_name>")
        sys.exit(1)

    workflow_name = sys.argv[1]

    # InfisicalからAPIキーを取得
    print(f"[INFO] Getting N8N_API_KEY from Infisical...")
    api_key = get_infisical_secret("N8N_API_KEY")

    if not api_key:
        print("[ERROR] Failed to get N8N_API_KEY from Infisical")
        sys.exit(1)

    print(f"[OK] N8N_API_KEY retrieved (preview: {api_key[:20]}...)\n")

    # ワークフローを検索
    print(f"[INFO] Searching for workflow: {workflow_name}")
    workflow_info = get_workflow_by_name(api_key, workflow_name)

    if not workflow_info:
        print(f"[ERROR] Workflow '{workflow_name}' not found in n8n")
        sys.exit(1)

    workflow_id = workflow_info.get("id")
    print(f"[OK] Found workflow: {workflow_name} (ID: {workflow_id})")

    # 削除確認
    print(f"\n[WARNING] This will permanently delete the workflow from n8n!")
    print(f"Workflow: {workflow_name}")
    print(f"ID: {workflow_id}")

    # 削除実行
    print(f"\n[INFO] Deleting workflow...")
    if delete_workflow(api_key, workflow_id):
        print(f"[SUCCESS] Workflow '{workflow_name}' deleted from n8n")
    else:
        print(f"[ERROR] Failed to delete workflow")
        sys.exit(1)



