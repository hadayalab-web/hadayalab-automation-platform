#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Whop Entries APIテストスクリプト
アフィリエイター候補をEntryとして作成・管理する機能をテスト
"""
import requests
import json
import subprocess
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# UTF-8エンコーディング設定
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Infisical設定
INFISICAL_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
PROJECT_ID = "446f131c-be8d-45e5-a83a-4154e34501a5"

WHOP_API_BASE_URL = "https://api.whop.com/api/v2"

def get_secret_from_infisical(secret_name: str) -> Optional[str]:
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
        print(f"[ERROR] Failed to get {secret_name}: {e}")
        return None

def get_products(api_key: str) -> list:
    """Whop APIでProduct一覧を取得"""
    url = f"{WHOP_API_BASE_URL}/products"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        print(f"[ERROR] Failed to get products: {e}")
        return []

def create_entry(api_key: str, product_id: str, user_email: str, metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Whop APIでEntryを作成（アフィリエイター候補登録）"""
    url = f"{WHOP_API_BASE_URL}/entries"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "product_id": product_id,
        "user_email": user_email,
        "metadata": metadata,
        "auto_approve": False
    }

    try:
        print(f"[INFO] Creating entry for {user_email}...")
        response = requests.post(url, headers=headers, json=data, timeout=10)

        if response.status_code == 201:
            result = response.json()
            print(f"[OK] Entry created: {result.get('id')}")
            return result
        else:
            print(f"[ERROR] Failed to create entry: {response.status_code}")
            print(f"[DEBUG] Response: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Exception creating entry: {e}")
        return None

def get_entries(api_key: str, product_id: Optional[str] = None, status: Optional[str] = None) -> list:
    """Whop APIでEntry一覧を取得"""
    url = f"{WHOP_API_BASE_URL}/entries"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    params = {}
    if product_id:
        params["product_id"] = product_id
    if status:
        params["status"] = status

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        print(f"[ERROR] Failed to get entries: {e}")
        return []

def update_entry(api_key: str, entry_id: str, metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Whop APIでEntryを更新"""
    url = f"{WHOP_API_BASE_URL}/entries/{entry_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "metadata": metadata
    }

    try:
        print(f"[INFO] Updating entry {entry_id}...")
        response = requests.patch(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        print(f"[OK] Entry updated: {entry_id}")
        return result
    except Exception as e:
        print(f"[ERROR] Failed to update entry: {e}")
        return None

def test_affiliate_candidate_entry(api_key: str, product_id: str):
    """アフィリエイター候補Entry作成のテスト"""
    print("\n" + "=" * 60)
    print("アフィリエイター候補Entry作成テスト")
    print("=" * 60)

    # テストデータ
    test_candidate = {
        "username": "@test_crypto_trader",
        "display_name": "Test Crypto Trader",
        "market": "EN",
        "follower_count": 15000,
        "engagement_rate": 3.5,
        "content_type": "Technical analysis",
        "recent_topics": ["BTC technical analysis", "Chart patterns"],
        "pain_points": ["Limited monetization"],
        "contact_method": "DM",
        "match_score": 8,
        "profile_url": "https://twitter.com/test_crypto_trader",
        "bio": "Crypto trader and educator",
        "language": "en",
        "verified": False,
        "extraction_date": datetime.now().isoformat(),
        "search_query": "crypto technical analysis BTC",
        "status": "New"
    }

    metadata = {
        "affiliate_candidate": test_candidate
    }

    # Entry作成
    entry = create_entry(
        api_key=api_key,
        product_id=product_id,
        user_email=f"test-{test_candidate['username']}@affiliate-candidate.whop",
        metadata=metadata
    )

    if entry:
        print(f"\n[OK] Test entry created successfully!")
        print(f"[INFO] Entry ID: {entry.get('id')}")
        print(f"[INFO] Entry Status: {entry.get('status')}")
        return entry.get('id')
    else:
        print("\n[ERROR] Failed to create test entry")
        return None

def main():
    print("=" * 60)
    print("Whop Entries APIテスト")
    print("=" * 60)
    print()

    # InfisicalからWhop API Keyを取得
    print("[STEP 1] Getting WHOP_API_KEY from Infisical...")
    api_key = get_secret_from_infisical("WHOP_API_KEY")
    if not api_key:
        print("[ERROR] Failed to get WHOP_API_KEY from Infisical")
        sys.exit(1)
    print(f"[OK] WHOP_API_KEY retrieved (preview: {api_key[:20]}...)\n")

    # Product一覧取得
    print("[STEP 2] Getting products...")
    products = get_products(api_key)
    print(f"[OK] Found {len(products)} products\n")

    if products:
        print("Available Products:")
        for product in products[:5]:  # 最初の5つを表示
            print(f"  - {product.get('name')} (ID: {product.get('id')})")
        print()

        # 最初のProduct IDを使用（または専用Productを作成）
        test_product_id = products[0].get('id')
        print(f"[INFO] Using Product ID for test: {test_product_id}\n")

        # Entry一覧取得（現在のEntries確認）
        print("[STEP 3] Getting existing entries...")
        entries = get_entries(api_key, product_id=test_product_id)
        print(f"[OK] Found {len(entries)} entries for product {test_product_id}\n")

        # テストEntry作成
        print("[STEP 4] Creating test affiliate candidate entry...")
        entry_id = test_affiliate_candidate_entry(api_key, test_product_id)

        if entry_id:
            # Entry一覧再取得（確認）
            print("\n[STEP 5] Verifying entry creation...")
            entries_after = get_entries(api_key, product_id=test_product_id)
            print(f"[OK] Total entries: {len(entries_after)}")

            # 作成したEntryを検索
            created_entry = next((e for e in entries_after if e.get('id') == entry_id), None)
            if created_entry:
                print(f"[OK] Created entry found:")
                print(f"  - ID: {created_entry.get('id')}")
                print(f"  - Status: {created_entry.get('status')}")
                print(f"  - Metadata: {json.dumps(created_entry.get('metadata', {}), indent=2, ensure_ascii=False)[:200]}...")
    else:
        print("[WARNING] No products found. Please create a product first.")
        print("[INFO] Whop Dashboard → Products → Create Product")

if __name__ == "__main__":
    main()

