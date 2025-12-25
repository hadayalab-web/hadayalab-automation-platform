#!/usr/bin/env python3
"""
ワークフロー1のデプロイ・テスト・デバッグスクリプト
使用方法: python scripts/deploy_workflow_1.py
"""

import json
import subprocess
import sys
import urllib.request
import urllib.parse
from pathlib import Path

# Infisical設定
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
PROJECT_ID = "446f131c-be8d-45e5-a83a-4154e34501a5"
N8N_PROJECT_ID = "9D29Es58GIo6IPkZ"
BASE_URL = "https://hadayalab.app.n8n.cloud/rest"

def get_personal_access_token():
    """InfisicalからPersonal Access Tokenを取得"""
    print("Personal Access Tokenを取得中...")
    try:
        result = subprocess.run(
            [
                "infisical", "secrets", "get", "N8N_PERSONAL_ACCESS_TOKEN",
                "--token", TOKEN,
                "--projectId", PROJECT_ID,
                "--output", "json"
            ],
            capture_output=True,
            text=True,
            check=True
        )

        # JSONを抽出
        output = result.stdout
        json_start = output.find('[')
        json_end = output.rfind(']') + 1
        if json_start >= 0 and json_end > json_start:
            json_str = output[json_start:json_end]
            data = json.loads(json_str)
            token = data[0].get('secretValue')
            if not token:
                print("エラー: Personal Access Tokenが取得できませんでした")
                sys.exit(1)
            # トークンの最初の20文字だけを表示（デバッグ用）
            token_preview = token[:20] + "..." if len(token) > 20 else token
            print(f"[OK] Personal Access Tokenを取得しました (プレビュー: {token_preview})\n")
            return token
        else:
            print("エラー: JSON形式のデータが見つかりませんでした")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"エラー: Personal Access Tokenの取得に失敗しました")
        print(f"エラー詳細: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)

def load_workflow_json():
    """ワークフローJSONファイルを読み込む"""
    workflow_path = Path("workflow-1-trial-onboarding.json")
    if not workflow_path.exists():
        print(f"エラー: ワークフローファイルが見つかりません: {workflow_path}")
        sys.exit(1)

    print(f"ワークフローファイルを読み込み中: {workflow_path}")
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # プロジェクトIDを追加
    workflow['projectId'] = N8N_PROJECT_ID
    # activeフラグをfalseに設定（テスト後に有効化）
    workflow['active'] = False

    return workflow

def import_workflow(workflow, token):
    """ワークフローをn8nにインポート"""
    print("\n=== ステップ1: ワークフローのインポート ===")
    url = f"{BASE_URL}/workflows"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("ワークフローをn8nにインポート中...")
    print(f"  URL: {url}")
    print(f"  ワークフロー名: {workflow['name']}")

    try:
        req = urllib.request.Request(url, data=json.dumps(workflow).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))

        workflow_id = data['data']['id']
        print("[OK] ワークフローのインポートに成功しました！")
        print(f"  ワークフローID: {workflow_id}")
        print(f"  ワークフロー名: {data['data']['name']}")
        print(f"  ステータス: {data['data']['active']}")
        print(f"\nワークフローURL: https://hadayalab.app.n8n.cloud/workflow/{workflow_id}?projectId={N8N_PROJECT_ID}\n")
        return workflow_id
    except urllib.error.HTTPError as e:
        print(f"[ERROR] ワークフローのインポートに失敗しました")
        print(f"エラー: {e}")
        error_body = e.read().decode('utf-8')
        print(f"レスポンス: {error_body}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] ワークフローのインポートに失敗しました")
        print(f"エラー: {e}")
        sys.exit(1)

def get_workflow_details(workflow_id, token):
    """ワークフローの詳細情報を取得"""
    print("=== ステップ2: ワークフローの詳細情報 ===")
    url = f"{BASE_URL}/workflows/{workflow_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("ワークフローの詳細を取得中...")
    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))

        workflow = data['data']
        print("[OK] ワークフローの詳細を取得しました")
        print(f"  ノード数: {len(workflow['nodes'])}")
        print(f"  接続数: {len(workflow.get('connections', {}))}")
        print("\nノード一覧:")
        for node in workflow['nodes']:
            print(f"  - {node['name']} ({node['type']})")
        print()

        # Webhook URLを取得
        webhook_node = next((n for n in workflow['nodes'] if n['type'] == 'n8n-nodes-base.webhook'), None)
        if webhook_node:
            webhook_path = webhook_node['parameters'].get('path', '')
            webhook_url = f"https://hadayalab.app.n8n.cloud/webhook/{webhook_path}"
            print("=== ステップ3: Webhook URLの確認 ===")
            print("[OK] Webhook URLを取得しました")
            print(f"  Webhook URL: {webhook_url}")
            print(f"  Path: {webhook_path}")
            print("\nテスト用curlコマンド:")
            print(f'curl -X POST {webhook_url} \\')
            print('  -H "Content-Type: application/json" \\')
            print('  -d \'{"user_email":"test@example.com","user_name":"Test User","market":"EN","membership_id":"test123"}\'')
            print()

        return workflow
    except urllib.error.HTTPError as e:
        print(f"[ERROR] ワークフローの詳細取得に失敗しました")
        print(f"エラー: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] ワークフローの詳細取得に失敗しました")
        print(f"エラー: {e}")
        return None

def get_executions(workflow_id, token):
    """実行履歴を取得"""
    print("=== ステップ4: 実行履歴の確認 ===")
    url = f"{BASE_URL}/executions?workflowId={workflow_id}&limit=5"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("実行履歴を取得中...")
    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))

        executions = data.get('data', [])
        if executions:
            print(f"[OK] 実行履歴を取得しました（最新{len(executions)}件）")
            for exec_item in executions:
                status = "完了" if exec_item.get('finished') else "実行中"
                print(f"  - {exec_item['id']}: {status} ({exec_item.get('mode', 'unknown')})")
        else:
            print("  （実行履歴がありません）")
        print()
    except urllib.error.HTTPError as e:
        print(f"[WARNING] 実行履歴の取得に失敗しました")
        print(f"エラー: {e}")
        print()
    except Exception as e:
        print(f"[WARNING] 実行履歴の取得に失敗しました")
        print(f"エラー: {e}")
        print()

def main():
    print("=== ワークフロー1のデプロイ・テスト・デバッグ ===")
    print(f"n8nプロジェクトID: {N8N_PROJECT_ID}\n")

    # Personal Access Tokenを取得
    token = get_personal_access_token()

    # ワークフローJSONを読み込む
    workflow = load_workflow_json()

    # ワークフローをインポート
    workflow_id = import_workflow(workflow, token)

    # ワークフローの詳細を取得
    get_workflow_details(workflow_id, token)

    # 実行履歴を取得
    get_executions(workflow_id, token)

    print("=== デプロイ・テスト完了 ===")
    print("\n次のステップ:")
    print(f"1. n8n Dashboardでワークフローを開く")
    print(f"   URL: https://hadayalab.app.n8n.cloud/workflow/{workflow_id}?projectId={N8N_PROJECT_ID}")
    print("2. 認証情報を設定（Gmail OAuth2、Whop API Key）")
    print("3. ワークフローをテスト実行")
    print("4. 問題がなければActive化")
    print()

if __name__ == "__main__":
    main()

