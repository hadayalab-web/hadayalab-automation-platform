#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegramチャンネル制御スクリプト
InfisicalからTelegram Bot Tokenを取得してチャンネルを制御
"""
import requests
import subprocess
import json
import sys

# UTF-8エンコーディング設定
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Infisical設定
INFISICAL_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
PROJECT_ID = "446f131c-be8d-45e5-a83a-4154e34501a5"

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
    except Exception as e:
        print(f"[ERROR] Failed to get {secret_name}: {e}")
        return None

def get_bot_info(bot_token):
    """Bot情報取得"""
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                return data.get('result', {})
        return None
    except Exception as e:
        print(f"[ERROR] Failed to get bot info: {e}")
        return None

def get_chat_info(bot_token, chat_id):
    """チャンネル情報取得"""
    url = f"https://api.telegram.org/bot{bot_token}/getChat"
    try:
        response = requests.get(url, params={'chat_id': chat_id}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                return data.get('result', {})
        return None
    except Exception as e:
        print(f"[ERROR] Failed to get chat info: {e}")
        return None

def send_message(bot_token, chat_id, text, parse_mode='Markdown'):
    """メッセージ送信"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': parse_mode
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                return data.get('result', {})
        return None
    except Exception as e:
        print(f"[ERROR] Failed to send message: {e}")
        return None

def list_accessible_chats(bot_token):
    """Botがアクセス可能なチャット一覧を取得（getUpdatesから）"""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    try:
        response = requests.get(url, params={'limit': 100}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                updates = data.get('result', [])
                chats = {}
                for update in updates:
                    if 'message' in update:
                        chat = update['message'].get('chat', {})
                        chat_id = chat.get('id')
                        if chat_id:
                            chats[chat_id] = {
                                'id': chat_id,
                                'type': chat.get('type'),
                                'title': chat.get('title') or chat.get('username') or chat.get('first_name'),
                                'username': chat.get('username')
                            }
                    elif 'channel_post' in update:
                        chat = update['channel_post'].get('chat', {})
                        chat_id = chat.get('id')
                        if chat_id:
                            chats[chat_id] = {
                                'id': chat_id,
                                'type': chat.get('type'),
                                'title': chat.get('title'),
                                'username': chat.get('username')
                            }
                return list(chats.values())
        return []
    except Exception as e:
        print(f"[ERROR] Failed to get updates: {e}")
        return []

if __name__ == "__main__":
    print("=" * 60)
    print("Telegramチャンネル制御スクリプト")
    print("=" * 60)
    print()

    # InfisicalからTelegram Bot Tokenを取得
    bot_token = get_secret_from_infisical("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("[ERROR] Failed to get TELEGRAM_BOT_TOKEN from Infisical")
        sys.exit(1)

    print(f"[OK] Telegram Bot Token retrieved from Infisical")
    print(f"[INFO] Token preview: {bot_token[:20]}...\n")

    # Bot情報取得
    print("=" * 60)
    print("Bot情報")
    print("=" * 60)
    bot_info = get_bot_info(bot_token)
    if bot_info:
        print(f"  - Bot ID: {bot_info.get('id')}")
        print(f"  - Bot Username: @{bot_info.get('username')}")
        print(f"  - Bot Name: {bot_info.get('first_name')}")
        print(f"  - Can Join Groups: {bot_info.get('can_join_groups')}")
        print(f"  - Can Read All Group Messages: {bot_info.get('can_read_all_group_messages')}")
    else:
        print("[ERROR] Failed to get bot info")
        sys.exit(1)

    # TELEGRAM_CHAT_IDを取得
    chat_id = get_secret_from_infisical("TELEGRAM_CHAT_ID")
    if chat_id:
        print("\n" + "=" * 60)
        print("チャンネル情報（TELEGRAM_CHAT_ID）")
        print("=" * 60)
        chat_info = get_chat_info(bot_token, chat_id)
        if chat_info:
            print(f"  - Chat ID: {chat_info.get('id')}")
            print(f"  - Chat Type: {chat_info.get('type')}")
            print(f"  - Chat Title: {chat_info.get('title', 'N/A')}")
            if 'username' in chat_info:
                print(f"  - Chat Username: @{chat_info.get('username')}")
            if 'description' in chat_info:
                desc = chat_info.get('description', '')
                print(f"  - Description: {desc[:100]}{'...' if len(desc) > 100 else ''}")
            if 'member_count' in chat_info:
                print(f"  - Member Count: {chat_info.get('member_count')}")
        else:
            print(f"[WARNING] Could not get chat info for chat_id: {chat_id}")

    # 6市場別チャンネルをテスト
    print("\n" + "=" * 60)
    print("6市場別チャンネルアクセステスト")
    print("=" * 60)

    test_channels = [
        '@cryptotradeacademy_en',
        '@cryptotradeacademy_ja',
        '@cryptotradeacademy_ar',
        '@cryptotradeacademy_ko',
        '@cryptotradeacademy_es',
        '@cryptotradeacademy_pt_br',
    ]

    accessible_channels = []
    for channel in test_channels:
        chat_info = get_chat_info(bot_token, channel)
        if chat_info:
            accessible_channels.append({
                'username': channel,
                'id': chat_info.get('id'),
                'title': chat_info.get('title'),
                'type': chat_info.get('type')
            })
            print(f"[OK] {channel}: {chat_info.get('title', 'N/A')} (ID: {chat_info.get('id')})")
        else:
            print(f"[WARNING] {channel}: Not accessible")

    if accessible_channels:
        print(f"\n[OK] Successfully accessed {len(accessible_channels)} channel(s)")

        # テストメッセージ送信（オプション - コメントアウト）
        # print("\n" + "=" * 60)
        # print("テストメッセージ送信")
        # print("=" * 60)
        # test_channel = accessible_channels[0]
        # message_result = send_message(
        #     bot_token,
        #     test_channel['id'],
        #     "🤖 Test message from n8n automation platform\n\nThis is a test to verify Telegram API access."
        # )
        # if message_result:
        #     print(f"[OK] Test message sent to {test_channel['username']}")
        #     print(f"[INFO] Message ID: {message_result.get('message_id')}")
    else:
        print("\n[WARNING] No accessible channels found")

