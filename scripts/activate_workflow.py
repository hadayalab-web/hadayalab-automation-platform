#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ワークフローをアクティブ化
"""
import requests
import json
import subprocess
import sys

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

def activate_workflow(workflow_id, api_key):
    """ワークフローをアクティブ化"""
    base_url = "https://hadayalab.app.n8n.cloud"
    api_endpoint = f"{base_url}/api/v1/workflows/{workflow_id}/activate"

    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    print(f"[INFO] Activating workflow: {workflow_id}")

    try:
        response = requests.post(api_endpoint, headers=headers, json={})
        response.raise_for_status()

        print(f"[OK] Workflow activated successfully!")
        return True

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to activate workflow: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return False

if __name__ == "__main__":
    # ワークフローIDを読み込む
    try:
        with open("workflow-id.txt", "r", encoding="utf-8") as f:
            workflow_id = f.read().strip()
    except FileNotFoundError:
        workflow_id = "iOSBFERBGZkvY25c"  # デフォルト値
        print(f"[INFO] workflow-id.txt not found, using default: {workflow_id}")

    # InfisicalからPersonal Access Tokenを取得
    print("[INFO] Getting N8N_API_KEY from Infisical...")
    api_key = get_infisical_secret("N8N_API_KEY")

    if not api_key:
        print("[ERROR] Failed to get N8N_API_KEY from Infisical")
        sys.exit(1)

    # ワークフローをアクティブ化
    activate_workflow(workflow_id, api_key)





