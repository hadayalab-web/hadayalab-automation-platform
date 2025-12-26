#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Whop APIを直接テスト
"""
import requests
import json

def test_whop_api(api_key):
    """Whop APIを直接テスト"""
    print("=" * 60)
    print("Whop API直接テスト")
    print("=" * 60)
    print(f"\n[INFO] API Key: {api_key[:20]}...\n")

    url = "https://api.whop.com/api/v2/memberships"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    params = {
        "page": 1,
        "per_page": 5
    }

    print(f"[TEST] Request URL: {url}")
    print(f"[TEST] Request params: {json.dumps(params, indent=2, ensure_ascii=False)}")
    print(f"[TEST] Request headers: Authorization: Bearer {api_key[:20]}...\n")

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)

        print(f"[INFO] Response status: {response.status_code}")
        print(f"[INFO] Response headers: {dict(response.headers)}\n")

        if response.status_code == 200:
            try:
                data = response.json()
                print(f"[OK] API request successful!")
                print(f"[INFO] Response data:")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
                if len(json.dumps(data, indent=2, ensure_ascii=False)) > 1000:
                    print("... (truncated)")
                return True
            except json.JSONDecodeError:
                print(f"[WARNING] Response is not JSON")
                print(f"[INFO] Response text: {response.text[:500]}")
                return False
        else:
            print(f"[ERROR] API request failed with status {response.status_code}")
            print(f"[INFO] Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return False

if __name__ == "__main__":
    # ユーザーが提供したAPIキー
    api_key = "apik_KbyD0T3ENibNW_C3791174_58437b1dc69efe1fa96a635be9c1b8edc77bbc3cfe4bc04bbb7148b140e9ca58"

    test_whop_api(api_key)














