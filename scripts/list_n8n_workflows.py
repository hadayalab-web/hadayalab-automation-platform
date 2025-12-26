#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
n8n Cloudのワークフロー一覧を取得
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

def list_workflows(api_key):
    """n8n Cloudのワークフロー一覧を取得"""
    base_url = "https://hadayalab.app.n8n.cloud"
    api_endpoint = f"{base_url}/api/v1/workflows"

    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    print("[INFO] Fetching workflows from n8n Cloud...")

    try:
        response = requests.get(api_endpoint, headers=headers, timeout=10)
        response.raise_for_status()

        result = response.json()

        if "data" in result:
            workflows = result["data"]
        else:
            workflows = result if isinstance(result, list) else []

        print(f"\n[OK] Found {len(workflows)} workflows\n")

        # simple-time-checkという名前のワークフローを検索
        simple_time_check_workflows = [wf for wf in workflows if wf.get("name") == "simple-time-check"]

        if simple_time_check_workflows:
            print("=== 'simple-time-check' ワークフロー一覧 ===")
            for wf in simple_time_check_workflows:
                print(f"\nID: {wf.get('id')}")
                print(f"Name: {wf.get('name')}")
                print(f"Active: {wf.get('active', False)}")
                print(f"URL: {base_url}/workflow/{wf.get('id')}")
        else:
            print("'simple-time-check' という名前のワークフローは見つかりませんでした。")

        return workflows

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to list workflows: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        sys.exit(1)

if __name__ == "__main__":
    # InfisicalからPersonal Access Tokenを取得
    print("[INFO] Getting N8N_API_KEY from Infisical...")
    api_key = get_infisical_secret("N8N_API_KEY")

    if not api_key:
        print("[ERROR] Failed to get N8N_API_KEY from Infisical")
        sys.exit(1)

    print(f"[OK] N8N_API_KEY retrieved (preview: {api_key[:20]}...)\n")

    # ワークフロー一覧を取得
    list_workflows(api_key)















