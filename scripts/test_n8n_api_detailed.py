#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
n8n API詳細テスト - 認証方法を徹底的に確認
"""
import requests
import json

# 新しいPersonal Access Token
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ZDcxM2YyMS0wZDBiLTRhYmUtYWZjNy1kYjc2MmQ4YWUzMzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY2NTgyODI1LCJleHAiOjE3NjkwOTQwMDB9.Glz7mE73w8H-KlgIpeUgVi17-Y5ost_MnbGHGqwvYdo"

BASE_URL = "https://hadayalab.app.n8n.cloud"

def test_api_endpoints():
    """様々なAPIエンドポイントをテスト"""
    print("=== n8n API認証テスト（徹底調査） ===\n")

    # テストするエンドポイント一覧
    endpoints = [
        # 標準的なREST APIエンドポイント
        f"{BASE_URL}/rest/workflows",
        f"{BASE_URL}/api/v1/workflows",
        f"{BASE_URL}/api/workflows",

        # 認証テスト用エンドポイント
        f"{BASE_URL}/rest/login",
        f"{BASE_URL}/api/v1/login",

        # ユーザー情報取得
        f"{BASE_URL}/rest/me",
        f"{BASE_URL}/api/v1/me",

        # プロジェクト一覧
        f"{BASE_URL}/rest/projects",
        f"{BASE_URL}/api/v1/projects",
    ]

    # 認証ヘッダーのパターン
    auth_patterns = [
        ("Bearer", f"Bearer {API_KEY}"),
        ("X-N8N-API-KEY", API_KEY),
        ("Authorization", API_KEY),  # Bearerなし
        ("n8n-api-key", API_KEY),
    ]

    for endpoint in endpoints:
        print(f"\n{'='*60}")
        print(f"Testing endpoint: {endpoint}")
        print(f"{'='*60}")

        for header_name, header_value in auth_patterns:
            headers = {
                header_name: header_value,
                "Content-Type": "application/json"
            }

            try:
                response = requests.get(endpoint, headers=headers, timeout=10)
                print(f"\n  [{header_name}: {header_value[:30]}...]")
                print(f"  Status: {response.status_code}")

                if response.status_code == 200:
                    print(f"  [OK] SUCCESS!")
                    try:
                        data = response.json()
                        print(f"  Response: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}...")
                    except:
                        print(f"  Response: {response.text[:200]}...")
                    break  # 成功したら次のエンドポイントへ
                elif response.status_code == 401:
                    print(f"  [NG] Unauthorized")
                elif response.status_code == 404:
                    print(f"  ⚠️  Not Found")
                else:
                    print(f"  ⚠️  Status: {response.status_code}")
                    print(f"  Response: {response.text[:200]}...")

            except requests.exceptions.RequestException as e:
                print(f"  ❌ Error: {e}")

        print()

def test_with_project_id():
    """プロジェクトIDを使用したテスト"""
    print("\n\n=== プロジェクトIDを使用したテスト ===\n")

    # 一般的なプロジェクトIDパターン
    project_ids = [
        "9D29Es58GIo6IPkZ",  # 既存スクリプトで使用されているもの
        None,  # プロジェクトIDなし
    ]

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    for project_id in project_ids:
        if project_id:
            endpoint = f"{BASE_URL}/rest/workflows?projectId={project_id}"
        else:
            endpoint = f"{BASE_URL}/rest/workflows"

        print(f"\nTesting: {endpoint}")
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")

            if response.status_code == 200:
                print(f"  [OK] SUCCESS!")
                data = response.json()
                print(f"  Response keys: {list(data.keys())}")
                if "data" in data:
                    print(f"  Workflows count: {len(data['data'])}")
            else:
                print(f"  Response: {response.text[:200]}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    test_api_endpoints()
    test_with_project_id()
    print("\n=== テスト完了 ===")

