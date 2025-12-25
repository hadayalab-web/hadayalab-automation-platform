#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ワークフローWebhookテスト
"""
import requests
import json

WEBHOOK_URL = "https://hadayalab.app.n8n.cloud/webhook/simple-time-check"

print("=== ワークフローテスト ===")
print(f"\nWebhook URL: {WEBHOOK_URL}")
print("\nWebhookを実行中...")

try:
    response = requests.get(WEBHOOK_URL, timeout=30)
    response.raise_for_status()

    print("[OK] ワークフロー実行成功！")
    print(f"\nステータスコード: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    print(f"\nレスポンス（生）:")
    print(response.text[:500])

    # JSONとして解析を試みる
    try:
        print(f"\nレスポンス（JSON）:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print("（JSON形式ではありません）")

except requests.exceptions.RequestException as e:
    print(f"[NG] エラー: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"ステータスコード: {e.response.status_code}")
        print(f"レスポンス: {e.response.text}")

