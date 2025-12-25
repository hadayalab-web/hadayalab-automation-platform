#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本番Webhook URLでワークフローをテスト
"""

import json
import urllib.request
import urllib.error

# 本番Webhook URL（ワークフローがActiveである必要があります）
WEBHOOK_URL = "https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-deploy"

def test_production_webhook():
    """本番Webhook URLでテスト実行"""
    print("=== Testing Production Webhook ===\n")
    print(f"[INFO] Using production webhook URL")
    print(f"  URL: {WEBHOOK_URL}\n")

    # テストデータを準備
    test_data = {
        "ref": "refs/heads/main",
        "repository": {
            "name": "hadayalab-automation-platform",
            "full_name": "hadayalab-web/hadayalab-automation-platform"
        },
        "head_commit": {
            "id": "abc123def456",
            "message": "Test: Cursor-Vercel workflow test",
            "author": {
                "name": "Test User",
                "email": "test@example.com"
            }
        }
    }

    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "push"
    }

    print("[INFO] Sending webhook request...\n")

    try:
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=json.dumps(test_data).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=120) as response:
            response_body = response.read().decode('utf-8')
            status_code = response.getcode()

            print(f"[OK] Webhook request sent! Status: {status_code}\n")

            if response_body:
                try:
                    result = json.loads(response_body)
                    print("Response:")
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                except json.JSONDecodeError:
                    print("Response (non-JSON):")
                    print(response_body)
            else:
                print("[INFO] Empty response (this is normal for webhook workflows)")

            print("\n[INFO] Next steps:")
            print("1. Check execution history in n8n Dashboard -> Executions")
            print("   URL: https://hadayalab.app.n8n.cloud/executions")
            print("2. Check if deployment started in Vercel Dashboard")
            print("3. Verify deployment status in Vercel")
            print()

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"[ERROR] HTTP Error: {e.code}")
        print(f"Response: {error_body}\n")

        if e.code == 401:
            print("[INFO] Authentication error:")
            print("  - Check if VERCEL_API_TOKEN is set correctly")
            print("  - Verify the token has proper permissions")
        elif e.code == 404:
            print("[INFO] Webhook not found:")
            print("  - Check if workflow is Active")
            print("  - Verify webhook path is correct")
        print()

    except urllib.error.URLError as e:
        print(f"[ERROR] Connection error: {e}\n")

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}\n")

if __name__ == "__main__":
    test_production_webhook()

