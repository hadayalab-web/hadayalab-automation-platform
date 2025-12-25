#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Copilot Agents/Copilot接続テスト
ユーザー → AI（私） → GitHub Copilot Agents/Copilot の基本接続を検証
"""
import requests
import json
import subprocess
import sys
from datetime import datetime

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

def create_test_issue(api_key, repository="hadayalab-web/hadayalab-automation-platform"):
    """テスト用Issueを作成"""
    base_url = "https://api.github.com"
    endpoint = f"{base_url}/repos/{repository}/issues"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    title = f"[接続テスト] AI -> GitHub Copilot Agents ({timestamp})"
    body = f"""## 接続テスト

このIssueは、**ユーザー → AI（私、司令塔） → GitHub Copilot Agents/Copilot** の基本接続を検証するためのテストです。

### テスト内容

@copilot こんにちは！接続テストです。以下の質問に答えてください：

1. このメッセージを受信できましたか？
2. あなたはGitHub Copilot AgentsまたはGitHub Copilotですか？
3. 現在の日時を教えてください。

### 期待される動作

1. ✅ Issueが作成される
2. ✅ @copilotメンションが認識される
3. ✅ GitHub Copilot Agents/Copilotが応答する
4. ✅ AI（私）が応答を検証する
5. ✅ ユーザーに結果を報告する

**作成時刻**: {datetime.now().isoformat()}
"""

    payload = {
        "title": title,
        "body": body,
        "labels": ["test", "copilot-connection", "automated"]
    }

    print(f"[INFO] Creating test issue in {repository}...")
    print(f"[INFO] Title: {title}")

    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=10)
        response.raise_for_status()

        issue_data = response.json()

        print(f"\n[OK] Issue created successfully!")
        print(f"\nIssue Information:")
        print(f"  Number: #{issue_data['number']}")
        print(f"  Title: {issue_data['title']}")
        print(f"  URL: {issue_data['html_url']}")
        print(f"  State: {issue_data['state']}")

        return issue_data

    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Failed to create issue: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return None

def check_copilot_response(api_key, issue_number, repository="hadayalab-web/hadayalab-automation-platform", max_wait=300):
    """Copilotの応答を確認（最大5分間待機）"""
    base_url = "https://api.github.com"
    endpoint = f"{base_url}/repos/{repository}/issues/{issue_number}/comments"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.github.v3+json"
    }

    print(f"\n[INFO] Waiting for Copilot response (max {max_wait} seconds)...")
    print(f"[INFO] Checking comments every 30 seconds...")

    import time
    start_time = time.time()
    check_interval = 30

    while time.time() - start_time < max_wait:
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            response.raise_for_status()

            comments = response.json()

            # Copilotの応答を検索
            copilot_responses = []
            for comment in comments:
                user_login = comment.get('user', {}).get('login', '').lower()
                body = comment.get('body', '').lower()

                # Copilot関連のユーザーまたはコメントを検出
                if ('copilot' in user_login or
                    'github-actions' in user_login or
                    'bot' in user_login or
                    'copilot' in body or
                    'こんにちは' in body or
                    '受信' in body):
                    copilot_responses.append(comment)

            if copilot_responses:
                print(f"\n[OK] Copilot response found!")
                for resp in copilot_responses:
                    print(f"\nResponse from {resp['user']['login']}:")
                    print(f"  Created: {resp['created_at']}")
                    print(f"  Body: {resp['body'][:200]}...")
                return copilot_responses

            elapsed = int(time.time() - start_time)
            print(f"[INFO] No response yet... (elapsed: {elapsed}s)")

            time.sleep(check_interval)

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to check comments: {e}")
            time.sleep(check_interval)

    print(f"\n[WARNING] No Copilot response received within {max_wait} seconds")
    return None

def main():
    print("=" * 60)
    print("GitHub Copilot Agents/Copilot Connection Test")
    print("=" * 60)
    print("\nFlow: User -> AI (Command Center) -> GitHub Copilot Agents/Copilot")
    print("\n" + "=" * 60 + "\n")

    # GitHub Personal Access Tokenを取得
    print("[STEP 1] Getting GitHub Personal Access Token from Infisical...")
    # 複数の名前を試す（単数形と複数形）
    api_key = get_infisical_secret("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not api_key or api_key == "*not found*":
        print("[INFO] Trying GITHUB_PERSONAL_ACCESS_TOKENS (plural)...")
        api_key = get_infisical_secret("GITHUB_PERSONAL_ACCESS_TOKENS")
    
    if not api_key or api_key == "*not found*":
        print("[ERROR] Failed to get GITHUB_PERSONAL_ACCESS_TOKEN or GITHUB_PERSONAL_ACCESS_TOKENS from Infisical")
        print("[INFO] Please check the secret name in Infisical")
        sys.exit(1)

    print(f"[OK] GitHub API key retrieved (preview: {api_key[:20]}...)\n")

    # テスト用Issueを作成
    print("[STEP 2] Creating test issue...")
    issue = create_test_issue(api_key)

    if not issue:
        print("[ERROR] Failed to create test issue")
        sys.exit(1)

    issue_number = issue['number']
    issue_url = issue['html_url']

    print(f"\n[INFO] Test issue created: {issue_url}")
    print(f"[INFO] Please check the issue and wait for Copilot response...")

    # Copilotの応答を確認
    print("\n[STEP 3] Checking for Copilot response...")
    responses = check_copilot_response(api_key, issue_number)

    # 結果サマリー
    print("\n" + "=" * 60)
    print("Test Result Summary")
    print("=" * 60)
    print(f"\n[OK] Issue Creation: Success")
    print(f"   Issue #: {issue_number}")
    print(f"   URL: {issue_url}")

    if responses:
        print(f"\n[OK] Copilot Response: Success ({len(responses)} response(s))")
        for i, resp in enumerate(responses, 1):
            print(f"   Response {i}: {resp['user']['login']} - {resp['created_at']}")
    else:
        print(f"\n[WARNING] Copilot Response: Not received (please check manually)")
        print(f"   Issue URL: {issue_url}")

    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print(f"1. Check the issue: {issue_url}")
    print("2. Check GitHub Copilot Agents/Copilot response")
    print("3. If response exists, AI (me) will verify and report to user")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

