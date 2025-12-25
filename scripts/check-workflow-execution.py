#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
n8nワークフローの実行結果を確認するスクリプト
"""
import requests
import json
import subprocess
import sys
from datetime import datetime, timedelta

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

def get_workflow_executions(workflow_id, api_key, limit=5):
    """ワークフローの実行履歴を取得"""
    base_url = "https://hadayalab.app.n8n.cloud"
    api_endpoint = f"{base_url}/api/v1/executions"

    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    params = {
        "workflowId": workflow_id,
        "limit": limit
    }

    try:
        response = requests.get(api_endpoint, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to get executions: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return None

def main():
    print("=" * 60)
    print("n8nワークフロー実行結果確認")
    print("=" * 60)
    print("\n")

    workflow_id = "3LYMmEXrRpSVhuhE"

    # InfisicalからAPIキーを取得
    print("[INFO] Getting N8N_API_KEY from Infisical...")
    api_key = get_infisical_secret("N8N_API_KEY")

    if not api_key:
        print("[ERROR] Failed to get N8N_API_KEY from Infisical")
        sys.exit(1)

    print(f"[OK] N8N_API_KEY retrieved\n")

    # 実行履歴を取得
    print(f"[INFO] Getting execution history for workflow: {workflow_id}...")
    executions = get_workflow_executions(workflow_id, api_key)

    if not executions:
        print("[ERROR] Failed to get executions")
        sys.exit(1)

    # 実行結果を表示
    print("\n" + "=" * 60)
    print("最新の実行結果")
    print("=" * 60)

    if "data" in executions:
        exec_list = executions["data"]
    else:
        exec_list = executions.get("results", [])

    if not exec_list:
        print("[INFO] 実行履歴が見つかりませんでした")
        print("[INFO] ワークフローを実行してから再度確認してください")
        return

    for i, exec_data in enumerate(exec_list[:5], 1):
        print(f"\n--- 実行 #{i} ---")
        print(f"ID: {exec_data.get('id', 'N/A')}")
        print(f"ステータス: {exec_data.get('finished', False) and '完了' or '実行中'}")
        success = exec_data.get('finished', False) and (exec_data.get('stoppedAt') is not None)
        print(f"成功: {'OK' if success else 'NG'}")

        if exec_data.get('startedAt'):
            started = datetime.fromisoformat(exec_data['startedAt'].replace('Z', '+00:00'))
            print(f"開始時刻: {started.strftime('%Y-%m-%d %H:%M:%S')}")

        if exec_data.get('stoppedAt'):
            stopped = datetime.fromisoformat(exec_data['stoppedAt'].replace('Z', '+00:00'))
            print(f"終了時刻: {stopped.strftime('%Y-%m-%d %H:%M:%S')}")
            if exec_data.get('startedAt'):
                duration = stopped - started
                print(f"実行時間: {duration.total_seconds():.2f}秒")

        # エラー情報
        if exec_data.get('data', {}).get('resultData', {}).get('error'):
            error = exec_data['data']['resultData']['error']
            print(f"エラー: {error.get('message', 'Unknown error')}")

    print("\n" + "=" * 60)
    print("詳細確認")
    print("=" * 60)
    print(f"\n[INFO] n8n Dashboardで詳細を確認:")
    print(f"https://hadayalab.app.n8n.cloud/executions")
    print(f"\n[INFO] ワークフローを直接確認:")
    print(f"https://hadayalab.app.n8n.cloud/workflow/{workflow_id}")

if __name__ == "__main__":
    main()

