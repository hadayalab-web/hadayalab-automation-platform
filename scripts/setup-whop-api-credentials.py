#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Whop APIキーをInfisicalから取得して、n8nの認証情報として設定するスクリプト

注意: n8nの認証情報はAPI経由で直接設定できないため、
このスクリプトはInfisicalから取得したAPIキーを表示し、
手動でn8n Dashboardに設定する手順を案内します。
"""
import os
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
        # JSON配列から最初の要素を取得
        secrets = json.loads(output)
        if secrets and len(secrets) > 0:
            return secrets[0]["secretValue"]
        return None
    except Exception as e:
        print(f"[ERROR] Failed to get {secret_name} from Infisical: {e}")
        return None

def main():
    print("=" * 60)
    print("Whop APIキー設定ガイド")
    print("=" * 60)
    print("\n")

    # InfisicalからWhop APIキーを取得
    print("[STEP 1] Getting Whop API Key from Infisical...")

    # 複数の名前を試す
    api_key = get_infisical_secret("WHOP_API_KEY")
    if not api_key or api_key == "*not found*":
        api_key = get_infisical_secret("WHOP_API_KEY")
    if not api_key or api_key == "*not found*":
        api_key = get_infisical_secret("whop_api_key")
    if not api_key or api_key == "*not found*":
        api_key = get_infisical_secret("WHOP")

    if not api_key or api_key == "*not found*":
        print("[ERROR] Whop API Key not found in Infisical")
        print("[INFO] Please check the secret name in Infisical")
        print("[INFO] Common names: WHOP_API_KEY, whop_api_key, WHOP")
        sys.exit(1)

    print(f"[OK] Whop API Key retrieved (preview: {api_key[:20]}...)\n")

    # n8n DashboardのURL
    n8n_url = "https://hadayalab.app.n8n.cloud"

    print("=" * 60)
    print("n8n認証情報設定手順")
    print("=" * 60)
    print("\n")
    print("n8nの認証情報はAPI経由で直接設定できないため、")
    print("以下の手順で手動で設定してください：\n")
    print("1. n8n Dashboardにアクセス:")
    print(f"   {n8n_url}\n")
    print("2. Settings → Credentials に移動\n")
    print("3. 「Add Credential」をクリック\n")
    print("4. 「HTTP Header Auth」を選択\n")
    print("5. 以下の情報を入力:")
    print("   - Name: Whop API Key")
    print("   - Header Name: Authorization")
    print(f"   - Header Value: Bearer {api_key}\n")
    print("6. 「Save」をクリック\n")
    print("7. ワークフロー「whop-control」を開く\n")
    print("8. 各HTTP Requestノード（Get Members, Get Member Details, etc.）を開く\n")
    print("9. 「Credential to connect with」で「Whop API Key」を選択\n")
    print("10. ワークフローを保存\n")
    print("=" * 60)
    print("\n")
    print("[INFO] API Key (full):")
    print(f"Bearer {api_key}\n")
    print("=" * 60)

if __name__ == "__main__":
    main()














