#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
6市場別Telegramキーの実値確認スクリプト
"""
import subprocess
import json
import sys
import requests

# UTF-8エンコーディング設定
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Infisical設定
INFISICAL_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
PROJECT_ID = "446f131c-be8d-45e5-a83a-4154e34501a5"

MARKETS = {
    'EN': {'name': 'English', 'username': '@cryptotradeacademy_en', 'key_suffix': 'EN'},
    'AR': {'name': 'Arabic', 'username': '@cryptotradeacademy_ar', 'key_suffix': 'AR'},
    'KO': {'name': 'Korean', 'username': '@cryptotradeacademy_ko', 'key_suffix': 'KO'},
    'JA': {'name': 'Japanese', 'username': '@cryptotradeacademy_ja', 'key_suffix': 'JA'},
    'ES': {'name': 'Spanish', 'username': '@cryptotradeacademy_es', 'key_suffix': 'ES'},
    'PT_BR': {'name': 'Portuguese (BR)', 'username': '@cryptotradeacademy_pt_br', 'key_suffix': ['PT-BR', 'PT_BR']},  # PT-BRを優先
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
    except Exception:
        return None

def test_bot_token(bot_token):
    """Bot Tokenの有効性をテスト"""
    if not bot_token:
        return False, None
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                return True, data.get('result', {})
        return False, None
    except Exception:
        return False, None

def test_chat_access(bot_token, chat_id):
    """チャンネルアクセスの有効性をテスト"""
    if not bot_token or not chat_id:
        return False, None
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getChat"
        response = requests.get(url, params={'chat_id': chat_id}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                return True, data.get('result', {})
        return False, None
    except Exception:
        return False, None

if __name__ == "__main__":
    print("=" * 60)
    print("6市場別Telegramキー実値確認")
    print("=" * 60)
    print()

    results = {}

    for market_code, market_info in MARKETS.items():
        # キーサフィックスを取得（PT_BRの場合は複数試行）
        key_suffixes = market_info.get('key_suffix', market_code)
        if isinstance(key_suffixes, str):
            key_suffixes = [key_suffixes]

        bot_token = None
        chat_id = None
        bot_token_key = None
        chat_id_key = None

        # 複数のキー名を試行
        for suffix in key_suffixes:
            temp_bot_token_key = f"TELEGRAM_BOT_TOKEN_{suffix}"
            temp_chat_id_key = f"TELEGRAM_CHAT_ID_{suffix}"

            temp_bot_token = get_secret_from_infisical(temp_bot_token_key)
            temp_chat_id = get_secret_from_infisical(temp_chat_id_key)

            # 最初に見つかった値を使用
            if temp_bot_token and not bot_token:
                bot_token = temp_bot_token
                bot_token_key = temp_bot_token_key
            if temp_chat_id and not chat_id:
                chat_id = temp_chat_id
                chat_id_key = temp_chat_id_key

            # 両方見つかった場合は終了
            if bot_token and chat_id:
                break

        # 見つからない場合は最初のキー名を使用（表示用）
        if not bot_token_key:
            bot_token_key = f"TELEGRAM_BOT_TOKEN_{key_suffixes[0]}"
        if not chat_id_key:
            chat_id_key = f"TELEGRAM_CHAT_ID_{key_suffixes[0]}"

        print(f"{market_code} ({market_info['name']}):")
        print(f"  - {bot_token_key}: ", end="")
        if bot_token:
            print(f"✅ {bot_token[:20]}...")
            # Bot Tokenテスト
            is_valid, bot_info = test_bot_token(bot_token)
            if is_valid:
                print(f"    Bot Username: @{bot_info.get('username', 'N/A')}")
                print(f"    Bot Name: {bot_info.get('first_name', 'N/A')}")
            else:
                print(f"    ⚠️ Bot Token無効")
        else:
            print("❌ 未設定")

        print(f"  - {chat_id_key}: ", end="")
        if chat_id:
            print(f"✅ {chat_id}")
            # Chat IDテスト
            if bot_token:
                has_access, chat_info = test_chat_access(bot_token, chat_id)
                if has_access:
                    print(f"    Chat Title: {chat_info.get('title', 'N/A')}")
                    print(f"    Chat Type: {chat_info.get('type', 'N/A')}")
                else:
                    print(f"    ⚠️ Chat ID無効またはアクセス不可")
        else:
            print("❌ 未設定")

        print()

        results[market_code] = {
            'bot_token': bot_token,
            'chat_id': chat_id,
            'bot_token_valid': test_bot_token(bot_token)[0] if bot_token else False,
            'chat_access_valid': test_chat_access(bot_token, chat_id)[0] if (bot_token and chat_id) else False,
        }

    # まとめ
    print("=" * 60)
    print("確認結果まとめ")
    print("=" * 60)

    configured_count = sum(1 for r in results.values() if r['bot_token'] and r['chat_id'])
    valid_bot_count = sum(1 for r in results.values() if r['bot_token_valid'])
    valid_chat_count = sum(1 for r in results.values() if r['chat_access_valid'])

    print(f"設定済み: {configured_count}/{len(MARKETS)} 市場")
    print(f"Bot Token有効: {valid_bot_count}/{len(MARKETS)} 市場")
    print(f"Chat ID有効: {valid_chat_count}/{len(MARKETS)} 市場")

    if configured_count < len(MARKETS):
        print("\n未設定の市場:")
        for market_code, result in results.items():
            if not (result['bot_token'] and result['chat_id']):
                print(f"  - {market_code}: {MARKETS[market_code]['name']}")

