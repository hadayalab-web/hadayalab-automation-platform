#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Whop制御ワークフローのテストスクリプト
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

def test_whop_api_key(api_key):
    """Whop APIキーをテスト"""
    print("[STEP 1] Testing Whop API Key...")

    url = "https://api.whop.com/api/v2/memberships"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, params={"per_page": 1})
        response.raise_for_status()
        print(f"[OK] Whop API Key is valid!")
        print(f"[INFO] Response status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Whop API Key test failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"[INFO] Status Code: {e.response.status_code}")
            print(f"[INFO] Response: {e.response.text}")
        return False

def test_workflow_webhook(action="get_members", **kwargs):
    """ワークフローのWebhookをテスト"""
    print(f"\n[STEP 2] Testing workflow webhook with action: {action}...")

    webhook_url = "https://hadayalab.app.n8n.cloud/webhook/whop-control"

    payload = {
        "action": action,
        **kwargs
    }

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        print(f"[INFO] Response status: {response.status_code}")
        print(f"[INFO] Response headers: {dict(response.headers)}")

        try:
            response_json = response.json()
            print(f"[INFO] Response body: {json.dumps(response_json, indent=2, ensure_ascii=False)}")
        except:
            print(f"[INFO] Response text: {response.text}")

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
    print("Whop制御ワークフローテスト")
    print("=" * 60)
    print("\n")

    # InfisicalからWhop APIキーを取得
    api_key = get_infisical_secret("WHOP_API_KEY")
    if not api_key or api_key == "*not found*":
        api_key = get_infisical_secret("whop_api_key")
    if not api_key or api_key == "*not found*":
        api_key = get_infisical_secret("WHOP")

    if not api_key or api_key == "*not found*":
        print("[ERROR] Whop API Key not found in Infisical")
        sys.exit(1)

    # Whop APIキーをテスト
    if not test_whop_api_key(api_key):
        print("\n[WARNING] Whop API Key test failed. Please check:")
        print("1. API Key is correct in Infisical")
        print("2. API Key has necessary permissions")
        print("3. API Key is not expired")
        sys.exit(1)

    # ワークフローのWebhookをテスト
    print("\n" + "=" * 60)
    print("ワークフローWebhookテスト")
    print("=" * 60)

    # テスト1: メンバー一覧取得
    test_workflow_webhook("get_members", page=1, per_page=5)

    print("\n" + "=" * 60)
    print("テスト完了")
    print("=" * 60)
    print("\n[INFO] 次のステップ:")
    print("1. n8n Dashboardで認証情報「Whop API Key」が設定されているか確認")
    print("2. ワークフロー「whop-control」の各HTTP Requestノードで認証情報が選択されているか確認")
    print("3. n8n Dashboard → Executions で実行結果を確認")

if __name__ == "__main__":
    main()













