#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
n8n APIアクセステスト
"""
import requests
import json

# 新しいPersonal Access Token
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ZDcxM2YyMS0wZDBiLTRhYmUtYWZjNy1kYjc2MmQ4YWUzMzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY2NTgyODI1LCJleHAiOjE3NjkwOTQwMDB9.Glz7mE73w8H-KlgIpeUgVi17-Y5ost_MnbGHGqwvYdo"

BASE_URL = "https://hadayalab.app.n8n.cloud"

def test_api_access():
    """n8n APIへのアクセスをテスト"""
    print("=== n8nダッシュボードアクセステスト ===\n")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 1. ワークフロー一覧を取得
    print("1. ワークフロー一覧を取得中...")
    try:
        response = requests.get(f"{BASE_URL}/rest/workflows", headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        print(f"  [OK] ワークフロー一覧取得成功")

        if "data" in data:
            workflows = data["data"]
            print(f"  ワークフロー数: {len(workflows)}")

            if len(workflows) > 0:
                print("\n  既存のワークフロー:")
                for wf in workflows[:5]:  # 最初の5つだけ表示
                    print(f"    - {wf.get('name', 'N/A')} (ID: {wf.get('id', 'N/A')})")
        else:
            print(f"  レスポンス形式: {json.dumps(data, indent=2, ensure_ascii=False)}")

    except requests.exceptions.HTTPError as e:
        print(f"  [NG] HTTPエラー: {e}")
        print(f"  ステータスコード: {e.response.status_code}")
        print(f"  レスポンス: {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"  [NG] リクエストエラー: {e}")

    # 2. ユーザー情報を取得（別のエンドポイントでテスト）
    print("\n2. ユーザー情報を取得中...")
    try:
        response = requests.get(f"{BASE_URL}/rest/login", headers=headers, timeout=10)
        # ログインエンドポイントは認証が必要ない可能性があるので、エラーは無視
        print(f"  ステータスコード: {response.status_code}")
    except Exception as e:
        print(f"  エラー: {e}")

    print("\n=== テスト完了 ===")

if __name__ == "__main__":
    test_api_access()















