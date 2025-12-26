#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cursor-Vercelワークフローのテストスクリプト
"""

import json
import urllib.request
import urllib.error

WEBHOOK_URL = "https://hadayalab.app.n8n.cloud/webhook-test/cursor-vercel-deploy"

def test_workflow():
    """ワークフローをテスト実行"""
    print("=== Cursor-Vercel Workflow Test ===\n")

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

    print("[INFO] Sending test webhook...")
    print(f"  URL: {WEBHOOK_URL}\n")

    try:
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=json.dumps(test_data).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))

            print("[OK] Workflow executed successfully!\n")
            print("Response:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print("\n[INFO] Next steps:")
            print("1. Check execution history in n8n Dashboard -> Executions")
            print("2. Check if deployment started in Vercel Dashboard")
            print()

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"[ERROR] Test execution failed")
        print(f"Status: {e.code}")
        print(f"Response: {error_body}\n")
        print("[INFO] Troubleshooting:")
        print("1. Check if workflow is Active")
        print("2. Check if VERCEL_API_TOKEN environment variable is set correctly")
        print("3. Check error logs in n8n Dashboard -> Executions")
        print()

    except urllib.error.URLError as e:
        print(f"[ERROR] Connection error: {e}\n")

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}\n")

if __name__ == "__main__":
    test_workflow()















