#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
n8nの実行履歴を確認するスクリプト
"""

import json
import subprocess
import sys
import urllib.request
import urllib.error

# Infisical設定
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
PROJECT_ID = "446f131c-be8d-45e5-a83a-4154e34501a5"
N8N_PROJECT_ID = "9D29Es58GIo6IPkZ"
BASE_URL = "https://hadayalab.app.n8n.cloud/rest"
WORKFLOW_ID = "EE7Thl6p9Zsmfns4"

def get_personal_access_token():
    """InfisicalからPersonal Access Tokenを取得"""
    print("[INFO] Getting Personal Access Token...")
    try:
        result = subprocess.run(
            [
                "infisical", "secrets", "get", "N8N_PERSONAL_ACCESS_TOKEN",
                "--token", TOKEN,
                "--projectId", PROJECT_ID,
                "--output", "json"
            ],
            capture_output=True,
            text=True,
            check=True
        )

        output = result.stdout
        json_start = output.find('[')
        json_end = output.rfind(']') + 1
        if json_start >= 0 and json_end > json_start:
            json_str = output[json_start:json_end]
            data = json.loads(json_str)
            token = data[0].get('secretValue')
            if not token or token == '*not found*':
                print("[ERROR] Personal Access Token not found")
                return None
            print("[OK] Personal Access Token retrieved\n")
            return token
        return None
    except Exception as e:
        print(f"[ERROR] Failed to get token: {e}")
        return None

def get_executions(token, workflow_id, limit=5):
    """実行履歴を取得"""
    print(f"=== Getting execution history for workflow {workflow_id} ===\n")
    url = f"{BASE_URL}/executions?workflowId={workflow_id}&limit={limit}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))

        executions = data.get('data', [])
        print(f"[OK] Found {len(executions)} recent executions\n")

        for i, exec_item in enumerate(executions, 1):
            print(f"--- Execution {i} ---")
            print(f"ID: {exec_item.get('id', 'N/A')}")
            print(f"Status: {exec_item.get('finished', False) and 'Finished' or 'Running'}")
            print(f"Mode: {exec_item.get('mode', 'N/A')}")
            print(f"Started: {exec_item.get('startedAt', 'N/A')}")

            # エラー情報を確認
            if exec_item.get('stoppedAt'):
                print(f"Stopped: {exec_item.get('stoppedAt')}")

            # エラーの詳細を確認
            if exec_item.get('data') and exec_item['data'].get('resultData'):
                result_data = exec_item['data']['resultData']
                if result_data.get('error'):
                    print(f"\n[ERROR] Execution error found!")
                    error = result_data['error']
                    print(f"  Error: {error.get('message', 'N/A')}")
                    if error.get('stack'):
                        print(f"  Stack: {error.get('stack')[:200]}...")

                # 各ノードの実行結果を確認
                if result_data.get('runData'):
                    run_data = result_data['runData']
                    print(f"\n  Node execution results:")
                    for node_name, node_runs in run_data.items():
                        if node_runs and len(node_runs) > 0:
                            last_run = node_runs[-1]
                            if last_run.get('error'):
                                print(f"    [ERROR] {node_name}:")
                                error = last_run['error']
                                print(f"      Message: {error.get('message', 'N/A')}")
                                if error.get('stack'):
                                    print(f"      Stack: {error.get('stack')[:200]}...")
                            else:
                                print(f"    [OK] {node_name}: Success")

            print()

        return executions
    except urllib.error.HTTPError as e:
        print(f"[ERROR] Failed to get executions: {e}")
        error_body = e.read().decode('utf-8')
        print(f"Response: {error_body}")
        return []
    except Exception as e:
        print(f"[ERROR] {e}")
        return []

def main():
    print("=== n8n Execution History Check ===\n")

    token = get_personal_access_token()
    if not token:
        print("[ERROR] Cannot proceed without Personal Access Token")
        sys.exit(1)

    executions = get_executions(token, WORKFLOW_ID, limit=10)

    if not executions:
        print("[WARNING] No executions found")
        print("[INFO] This might mean:")
        print("  1. The workflow hasn't been executed yet")
        print("  2. The workflow ID is incorrect")
        print("  3. There's an authentication issue")
    else:
        # 最新の実行を詳しく確認
        latest = executions[0]
        print("=== Latest Execution Details ===")
        print(f"Execution ID: {latest.get('id')}")
        print(f"Status: {'Finished' if latest.get('finished') else 'Running'}")
        print(f"Workflow ID: {latest.get('workflowId')}")
        print()

if __name__ == "__main__":
    main()
















