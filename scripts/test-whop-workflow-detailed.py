#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Whopワークフローの詳細テスト
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

def test_workflow_with_detailed_response(action="get_members", **kwargs):
    """ワークフローのWebhookを詳細にテスト"""
    print(f"\n[TEST] Testing workflow webhook with action: {action}...")

    webhook_url = "https://hadayalab.app.n8n.cloud/webhook/whop-control"

    payload = {
        "action": action,
        **kwargs
    }

    print(f"[INFO] Request URL: {webhook_url}")
    print(f"[INFO] Request payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        print(f"\n[INFO] Response status: {response.status_code}")
        print(f"[INFO] Response headers: {dict(response.headers)}")

        # レスポンスボディを確認
        if response.headers.get('Content-Length') == '0' or len(response.text) == 0:
            print("[WARNING] Response body is empty")
        else:
            try:
                response_json = response.json()
                print(f"[INFO] Response body (JSON):")
                print(json.dumps(response_json, indent=2, ensure_ascii=False))
            except:
                print(f"[INFO] Response body (text): {response.text}")

        if response.status_code == 200:
            print(f"[OK] Workflow webhook test successful!")
            return True
        else:
            print(f"[WARNING] Workflow webhook returned status {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Workflow webhook test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Whopワークフロー詳細テスト")
    print("=" * 60)

    # テスト1: メンバー一覧取得
    test_workflow_with_detailed_response("get_members", page=1, per_page=5)

    print("\n" + "=" * 60)
    print("テスト完了")
    print("=" * 60)
    print("\n[INFO] n8n Dashboardで実行結果を確認:")
    print("https://hadayalab.app.n8n.cloud/executions")

if __name__ == "__main__":
    main()




