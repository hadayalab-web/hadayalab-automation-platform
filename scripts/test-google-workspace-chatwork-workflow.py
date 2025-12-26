#!/usr/bin/env python3
"""
Google Workspace / Chatwork Control ワークフローのテストスクリプト
"""

import json
import sys
import requests
from pathlib import Path

# .envファイルを読み込む
def load_env_file(env_path: Path):
    """.envファイルを読み込んで環境変数に設定"""
    if not env_path.exists():
        return
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                os.environ[key] = value

import os

# .envファイルを読み込む（.env.envも確認）
env_path = Path(__file__).parent.parent / ".env"
if not env_path.exists():
    env_path = Path(__file__).parent.parent / ".env.env"
load_env_file(env_path)

# ワークフローのWebhook URL
WEBHOOK_URL = "https://hadayalab.app.n8n.cloud/webhook/google-workspace-chatwork-control"

def test_webhook_basic():
    """Webhookの基本動作をテスト（無効なアクション）"""
    print("=" * 80)
    print("テスト: Webhook基本動作確認")
    print("=" * 80)
    
    payload = {
        "action": "invalid_action_test"
    }
    
    print(f"リクエスト: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    print(f"URL: {WEBHOOK_URL}")
    print()
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=30)
        print(f"ステータスコード: {response.status_code}")
        
        # レスポンステキストを確認
        response_text = response.text
        print(f"レスポンス（テキスト）: {response_text[:500]}")
        
        # JSONレスポンスを試行
        try:
            response_json = response.json()
            print(f"レスポンス（JSON）: {json.dumps(response_json, indent=2, ensure_ascii=False)}")
        except:
            print("レスポンスはJSON形式ではありません")
        
        if response.status_code == 200:
            print("\n[OK] Webhookは応答しています（ステータスコード200）")
            return True
        else:
            print(f"\n[WARN] 予期しないステータスコード: {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print("\n[ERROR] タイムアウト: ワークフローが応答しませんでした")
        return False
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] 接続エラー: Webhook URLに接続できませんでした")
        return False
    except Exception as e:
        print(f"\n[ERROR] 例外が発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_chatwork_send_message():
    """Chatworkメッセージ送信をテスト"""
    print("=" * 80)
    print("テスト: Chatworkメッセージ送信")
    print("=" * 80)
    
    # テストデータ（実際のroomIdはユーザーが設定する必要がある）
    payload = {
        "action": "chatwork_send_message",
        "roomId": "123456789",  # 実際のルームIDに置き換える必要があります
        "message": "テストメッセージ from n8n workflow"
    }
    
    print(f"リクエスト: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    print(f"URL: {WEBHOOK_URL}")
    print()
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=30)
        print(f"ステータスコード: {response.status_code}")
        
        try:
            response_json = response.json()
            print(f"レスポンス: {json.dumps(response_json, indent=2, ensure_ascii=False)}")
            
            if response.status_code == 200:
                if isinstance(response_json, dict) and response_json.get('success'):
                    print("\n[OK] テスト成功")
                    return True
                else:
                    error_msg = response_json.get('error', 'Unknown error')
                    print(f"\n[ERROR] テスト失敗: {error_msg}")
                    return False
            else:
                print(f"\n[ERROR] HTTPエラー: {response.status_code}")
                return False
        except:
            print(f"レスポンス（テキスト）: {response.text[:500]}")
            return False
    except Exception as e:
        print(f"\n[ERROR] 例外が発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_workflow_info():
    """ワークフロー情報を表示"""
    print("=" * 80)
    print("ワークフロー情報")
    print("=" * 80)
    print(f"Webhook URL: {WEBHOOK_URL}")
    print(f"ワークフローID: bELMAoceJ0vFNMaa")
    print(f"ワークフローURL: https://hadayalab.app.n8n.cloud/workflow/bELMAoceJ0vFNMaa")
    print()
    print("サポートするアクション:")
    print("  - gmail_send")
    print("  - sheets_read")
    print("  - chatwork_send_message")
    print("  - chatwork_create_task")
    print()

def main():
    test_workflow_info()
    
    print("=" * 80)
    print("注意事項")
    print("=" * 80)
    print("1. このテストスクリプトは、実際のroomIdが必要です")
    print("2. Google Workspaceアクション（gmail_send, sheets_read）のテストは、")
    print("   認証情報が設定されている必要があります")
    print("3. Chatworkアクションのテストは、有効なroomIdが必要です")
    print()
    
    # 基本テストを実行
    print("=" * 80)
    print("基本動作テストを実行します...")
    print("=" * 80)
    test_webhook_basic()
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        if len(sys.argv) > 2 and sys.argv[2] == "chatwork":
            print()
            test_chatwork_send_message()
        else:
            print("使用方法: python test-google-workspace-chatwork-workflow.py --test chatwork")
    else:
        print("Chatworkアクションのテストを実行する場合は：")
        print("  python scripts/test-google-workspace-chatwork-workflow.py --test chatwork")

if __name__ == "__main__":
    main()

