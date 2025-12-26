#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot API テストスクリプト
InfisicalからTelegram Bot Tokenを取得してTelegram APIをテスト
"""
import requests
import os
import subprocess
import json
import sys

# UTF-8エンコーディング設定
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Infisical設定（既存スクリプトと同じ設定を使用）
INFISICAL_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2luIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
PROJECT_ID = "446f131c-be8d-45e5-a83a-4154e34501a5"

def get_secret_from_infisical(secret_name):
    """Infisicalからシークレットを取得（既存スクリプトと同じ方法）"""
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
        # シークレットが存在しない場合はNoneを返す（正常）
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON for {secret_name}: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Exception getting {secret_name}: {e}")
        return None

def test_telegram_api(bot_token):
    """Telegram Bot APIをテスト"""
    print("=" * 60)
    print("Telegram Bot API テスト")
    print("=" * 60)
    print(f"\n[INFO] Bot Token: {bot_token[:20]}...\n")

    # 1. getMe - Bot情報取得
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    print(f"[TEST] Testing getMe API...")
    print(f"[TEST] URL: {url[:50]}...\n")

    try:
        response = requests.get(url, timeout=10)

        print(f"[INFO] Response status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                print(f"[OK] Bot API connection successful!")
                print(f"[INFO] Bot Information:")
                print(f"  - Bot ID: {bot_info.get('id')}")
                print(f"  - Bot Username: @{bot_info.get('username')}")
                print(f"  - Bot Name: {bot_info.get('first_name')}")
                print(f"  - Can Join Groups: {bot_info.get('can_join_groups')}")
                print(f"  - Can Read All Group Messages: {bot_info.get('can_read_all_group_messages')}")
                return True, bot_info
            else:
                print(f"[ERROR] API returned error: {data.get('description')}")
                return False, None
        else:
            print(f"[ERROR] API request failed with status {response.status_code}")
            print(f"[INFO] Response: {response.text}")
            return False, None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return False, None

def get_updates(bot_token):
    """getUpdates - 最新のメッセージ取得"""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    print(f"\n[TEST] Testing getUpdates API...")

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                updates = data.get('result', [])
                print(f"[OK] Found {len(updates)} updates")
                if updates:
                    print(f"[INFO] Latest update:")
                    print(json.dumps(updates[-1], indent=2, ensure_ascii=False)[:500])
                return True
            else:
                print(f"[ERROR] API returned error: {data.get('description')}")
                return False
    except Exception as e:
        print(f"[ERROR] Failed to get updates: {e}")
        return False

def get_chat_info(bot_token, chat_id):
    """getChat - チャンネル情報取得"""
    url = f"https://api.telegram.org/bot{bot_token}/getChat"
    print(f"\n[TEST] Testing getChat API for chat_id: {chat_id}...")

    try:
        response = requests.get(url, params={'chat_id': chat_id}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                chat_info = data.get('result', {})
                print(f"[OK] Chat information retrieved!")
                print(f"[INFO] Chat Information:")
                print(f"  - Chat ID: {chat_info.get('id')}")
                print(f"  - Chat Type: {chat_info.get('type')}")
                print(f"  - Chat Title: {chat_info.get('title', chat_info.get('username', 'N/A'))}")
                if 'username' in chat_info:
                    print(f"  - Chat Username: @{chat_info.get('username')}")
                if 'description' in chat_info:
                    desc = chat_info.get('description', '')
                    print(f"  - Description: {desc[:100]}{'...' if len(desc) > 100 else ''}")
                if 'member_count' in chat_info:
                    print(f"  - Member Count: {chat_info.get('member_count')}")
                return True, chat_info
            else:
                print(f"[ERROR] API returned error: {data.get('description')}")
                return False, None
        else:
            print(f"[ERROR] API request failed with status {response.status_code}")
            return False, None
    except Exception as e:
        print(f"[ERROR] Failed to get chat info: {e}")
        return False, None

def send_test_message(bot_token, chat_id, message="Test message from n8n automation"):
    """sendMessage - テストメッセージ送信"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    print(f"\n[TEST] Testing sendMessage API to chat_id: {chat_id}...")

    try:
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                message_info = data.get('result', {})
                print(f"[OK] Message sent successfully!")
                print(f"[INFO] Message Information:")
                print(f"  - Message ID: {message_info.get('message_id')}")
                print(f"  - Chat ID: {message_info.get('chat', {}).get('id')}")
                print(f"  - Date: {message_info.get('date')}")
                return True, message_info
            else:
                print(f"[ERROR] API returned error: {data.get('description')}")
                return False, None
        else:
            print(f"[ERROR] API request failed with status {response.status_code}")
            print(f"[INFO] Response: {response.text}")
            return False, None
    except Exception as e:
        print(f"[ERROR] Failed to send message: {e}")
        return False, None

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("InfisicalからTelegram Bot Token取得テスト")
    print("=" * 60 + "\n")

    # InfisicalからTelegram Bot Tokenを取得
    # 複数の可能性のあるキー名を試す
    possible_keys = [
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_BOT_TOKEN_EN',
        'TELEGRAM_BOT_TOKEN_JA',
        'TELEGRAM_BOT_TOKEN_AR',
        'TELEGRAM_BOT_TOKEN_KO',
        'TELEGRAM_BOT_TOKEN_ES',
        'TELEGRAM_BOT_TOKEN_PT_BR',
    ]

    bot_token = None
    token_key = None

    print("[INFO] Searching for Telegram Bot Token in Infisical...\n")
    for key in possible_keys:
        token = get_secret_from_infisical(key)
        if token:
            bot_token = token
            token_key = key
            print(f"[OK] Found Telegram Bot Token in Infisical: {key}")
            break

    if not bot_token:
        print("[ERROR] Telegram Bot Token not found in Infisical")
        print("[INFO] Tried keys:", ", ".join(possible_keys))
        print("[INFO] Please check Infisical dashboard or use environment variable")

        # 環境変数からも試す
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN') or os.getenv('TELEGRAM_BOT_TOKEN_EN')
        if bot_token:
            print(f"[INFO] Using Telegram Bot Token from environment variable")
        else:
            sys.exit(1)
    else:
        print(f"[INFO] Using Telegram Bot Token from Infisical: {token_key}\n")

    # Telegram Bot APIをテスト
    success, bot_info = test_telegram_api(bot_token)

    if success:
        print("\n" + "=" * 60)
        print("追加テスト: getUpdates")
        print("=" * 60)
        get_updates(bot_token)

        # チャンネル情報取得テスト
        print("\n" + "=" * 60)
        print("追加テスト: getChat（チャンネル情報取得）")
        print("=" * 60)

        # 6市場別チャンネルを試す
        test_channels = [
            '@cryptotradeacademy_en',
            '@cryptotradeacademy_ja',
            '@cryptotradeacademy_ar',
            '@cryptotradeacademy_ko',
            '@cryptotradeacademy_es',
            '@cryptotradeacademy_pt_br',
        ]

        print("\n[TEST] Testing channel access...")
        accessible_channels = []
        for channel in test_channels:
            success, chat_info = get_chat_info(bot_token, channel)
            if success:
                accessible_channels.append(channel)
                print(f"[OK] Successfully accessed {channel}")
            else:
                print(f"[WARNING] Could not access {channel}")

        if accessible_channels:
            print(f"\n[OK] Successfully accessed {len(accessible_channels)} channel(s)")
            print(f"[INFO] Accessible channels: {', '.join(accessible_channels)}")

            # テストメッセージ送信（オプション - コメントアウト）
            # print("\n" + "=" * 60)
            # print("追加テスト: sendMessage（テストメッセージ送信）")
            # print("=" * 60)
            # print("[INFO] Uncomment the code below to send a test message")
            # send_test_message(bot_token, accessible_channels[0], "🤖 Test message from n8n automation platform")
        else:
            print("\n[WARNING] No accessible channels found")
    else:
        print("\n[ERROR] Telegram Bot API test failed")
        sys.exit(1)
