#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram多言語版キー設定確認スクリプト
Infisicalに6市場別Telegram Bot Token/Chat IDが設定されているか確認
"""
import subprocess
import json
import sys

# UTF-8エンコーディング設定
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Infisical設定
INFISICAL_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
PROJECT_ID = "446f131c-be8d-45e5-a83a-4154e34501a5"

MARKETS = {
    'EN': {'name': 'English', 'username': '@cryptotradeacademy_en'},
    'AR': {'name': 'Arabic', 'username': '@cryptotradeacademy_ar'},
    'KO': {'name': 'Korean', 'username': '@cryptotradeacademy_ko'},
    'JA': {'name': 'Japanese', 'username': '@cryptotradeacademy_ja'},
    'ES': {'name': 'Spanish', 'username': '@cryptotradeacademy_es'},
    'PT_BR': {'name': 'Portuguese (BR)', 'username': '@cryptotradeacademy_pt_br'},
}

def get_secret_from_infisical(secret_name):
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
    except subprocess.CalledProcessError:
        return None
    except Exception:
        return None

def check_telegram_keys():
    """6市場別Telegramキーの設定状況を確認"""
    print("=" * 60)
    print("6市場別Telegramキー設定状況確認")
    print("=" * 60)
    print()

    results = {}

    for market_code, market_info in MARKETS.items():
        bot_token_key = f"TELEGRAM_BOT_TOKEN_{market_code}"
        chat_id_key = f"TELEGRAM_CHAT_ID_{market_code}"

        bot_token = get_secret_from_infisical(bot_token_key)
        chat_id = get_secret_from_infisical(chat_id_key)

        status = "✅ 設定済み" if (bot_token and chat_id) else "❌ 未設定"
        results[market_code] = {
            'status': status,
            'bot_token': bot_token is not None,
            'chat_id': chat_id is not None,
            'bot_token_key': bot_token_key,
            'chat_id_key': chat_id_key,
        }

        print(f"{market_code} ({market_info['name']}): {status}")
        print(f"  - {bot_token_key}: {'✅' if bot_token else '❌'}")
        print(f"  - {chat_id_key}: {'✅' if chat_id else '❌'}")
        if bot_token:
            print(f"    Token preview: {bot_token[:20]}...")
        if chat_id:
            print(f"    Chat ID: {chat_id}")
        print()

    # まとめ
    print("=" * 60)
    print("設定状況まとめ")
    print("=" * 60)

    configured = sum(1 for r in results.values() if r['bot_token'] and r['chat_id'])
    total = len(MARKETS)

    print(f"設定済み: {configured}/{total} 市場")
    print(f"未設定: {total - configured}/{total} 市場")

    if configured < total:
        print("\n未設定の市場:")
        for market_code, result in results.items():
            if not (result['bot_token'] and result['chat_id']):
                print(f"  - {market_code}: {MARKETS[market_code]['name']}")
                print(f"    設定が必要なキー:")
                if not result['bot_token']:
                    print(f"      - {result['bot_token_key']}")
                if not result['chat_id']:
                    print(f"      - {result['chat_id_key']}")

    return results

if __name__ == "__main__":
    results = check_telegram_keys()

    # 設定コマンドの例を表示
    print("\n" + "=" * 60)
    print("設定コマンド例（未設定の場合）")
    print("=" * 60)
    print()
    print("# 例: EN市場のBot Tokenを設定")
    print("infisical secrets set TELEGRAM_BOT_TOKEN_EN \"YOUR_BOT_TOKEN\" --token YOUR_TOKEN --projectId " + PROJECT_ID)
    print()
    print("# 例: EN市場のChat IDを設定")
    print("infisical secrets set TELEGRAM_CHAT_ID_EN \"YOUR_CHAT_ID\" --token YOUR_TOKEN --projectId " + PROJECT_ID)

