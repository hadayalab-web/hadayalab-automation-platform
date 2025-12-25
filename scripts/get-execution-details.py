#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
n8nワークフローの実行詳細を取得
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

def get_execution_details(execution_id, api_key):
    """実行詳細を取得"""
    base_url = "https://hadayalab.app.n8n.cloud"
    api_endpoint = f"{base_url}/api/v1/executions/{execution_id}"

    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to get execution details: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return None

def main():
    if len(sys.argv) > 1:
        execution_id = sys.argv[1]
    else:
        execution_id = "32"  # デフォルトの実行ID

    print("=" * 60)
    print("n8nワークフロー実行詳細")
    print("=" * 60)
    print(f"\n[INFO] Getting execution details for ID: {execution_id}\n")

    # InfisicalからAPIキーを取得
    api_key = get_infisical_secret("N8N_API_KEY")

    if not api_key:
        print("[ERROR] Failed to get N8N_API_KEY from Infisical")
        sys.exit(1)

    # 実行詳細を取得
    details = get_execution_details(execution_id, api_key)

    if not details:
        print("[ERROR] Failed to get execution details")
        sys.exit(1)

    # 実行結果を表示
    if "data" in details:
        exec_data = details["data"]
    else:
        exec_data = details

    print("=" * 60)
    print("実行情報")
    print("=" * 60)
    print(f"ID: {exec_data.get('id', 'N/A')}")
    print(f"Finished: {exec_data.get('finished', False)}")
    print(f"Mode: {exec_data.get('mode', 'N/A')}")
    print(f"Started At: {exec_data.get('startedAt', 'N/A')}")
    print(f"Stopped At: {exec_data.get('stoppedAt', 'N/A')}")

    # エラー情報
    if exec_data.get('data', {}).get('resultData', {}).get('error'):
        print("\n" + "=" * 60)
        print("エラー情報")
        print("=" * 60)
        error = exec_data['data']['resultData']['error']
        print(f"Error: {json.dumps(error, indent=2, ensure_ascii=False)}")

    # ノード実行結果
    if exec_data.get('data', {}).get('resultData', {}).get('runData'):
        print("\n" + "=" * 60)
        print("ノード実行結果")
        print("=" * 60)
        run_data = exec_data['data']['resultData']['runData']
        for node_name, node_data in run_data.items():
            print(f"\nNode: {node_name}")
            if 'error' in node_data:
                print(f"  Error: {json.dumps(node_data['error'], indent=2, ensure_ascii=False)}")
            if 'data' in node_data:
                main_data = node_data.get('main', [])
                if main_data and len(main_data) > 0:
                    print(f"  Data available: {len(main_data[0])} items")
                    if len(main_data[0]) > 0:
                        print(f"  First item: {json.dumps(main_data[0][0], indent=2, ensure_ascii=False)[:500]}")
                else:
                    print(f"  No data")
    else:
        print("\n[INFO] No run data available")

if __name__ == "__main__":
    main()

