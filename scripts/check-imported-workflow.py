#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
インポートされたワークフローのチェックスクリプト
"""

import json
import subprocess
import sys
import urllib.request
import urllib.error

# Infisical設定
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
PROJECT_ID = "446f131c-be8d-45e5-a83a-4154e34501a5"
N8N_PROJECT_ID = "9D29Es58GIo6IPkZ"
BASE_URL = "https://hadayalab.app.n8n.cloud/rest"

def get_personal_access_token():
    """InfisicalからPersonal Access Tokenを取得"""
    print("[INFO] Personal Access Tokenを取得中...")
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
            if not token or token == '*not found*':
                print("[ERROR] Personal Access Tokenが取得できませんでした")
                print("[INFO] n8n Dashboard → Settings → Personal Access Tokens で作成してください")
                return None
            print(f"[OK] Personal Access Tokenを取得しました\n")
            return token
        else:
            print("[ERROR] JSON形式のデータが見つかりませんでした")
            return None
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Personal Access Tokenの取得に失敗しました")
        print(f"エラー詳細: {e.stderr}")
        return None
    except Exception as e:
        print(f"[ERROR] {e}")
        return None

def list_workflows(token):
    """ワークフロー一覧を取得"""
    print("=== ワークフロー一覧 ===")
    url = f"{BASE_URL}/workflows?projectId={N8N_PROJECT_ID}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))

        workflows = data.get('data', [])
        print(f"[OK] {len(workflows)}個のワークフローが見つかりました\n")

        for wf in workflows:
            print(f"  - ID: {wf.get('id', 'N/A')}")
            print(f"    名前: {wf.get('name', 'N/A')}")
            print(f"    ステータス: {'Active' if wf.get('active') else 'Inactive'}")
            print(f"    作成日: {wf.get('createdAt', 'N/A')}")
            print()

        return workflows
    except urllib.error.HTTPError as e:
        print(f"[ERROR] ワークフロー一覧の取得に失敗しました")
        print(f"エラー: {e}")
        error_body = e.read().decode('utf-8')
        print(f"レスポンス: {error_body}")
        return []
    except Exception as e:
        print(f"[ERROR] {e}")
        return []

def check_workflow(workflow_id, token):
    """ワークフローの詳細をチェック"""
    print(f"=== ワークフロー詳細チェック (ID: {workflow_id}) ===")
    url = f"{BASE_URL}/workflows/{workflow_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))

        workflow = data.get('data', {})

        print(f"[OK] ワークフロー詳細を取得しました\n")
        print(f"名前: {workflow.get('name', 'N/A')}")
        print(f"ステータス: {'Active' if workflow.get('active') else 'Inactive'}")
        print(f"ノード数: {len(workflow.get('nodes', []))}")
        print(f"接続数: {len(workflow.get('connections', {}))}")

        # ノード一覧
        print("\n=== ノード一覧 ===")
        nodes = workflow.get('nodes', [])
        for i, node in enumerate(nodes, 1):
            print(f"{i}. {node.get('name', 'N/A')} ({node.get('type', 'N/A')})")

        # Webhookノードを確認
        print("\n=== Webhook設定 ===")
        webhook_nodes = [n for n in nodes if n.get('type') == 'n8n-nodes-base.webhook']
        if webhook_nodes:
            for webhook in webhook_nodes:
                params = webhook.get('parameters', {})
                path = params.get('path', 'N/A')
                method = params.get('httpMethod', 'N/A')
                print(f"  Path: {path}")
                print(f"  Method: {method}")
                print(f"  Webhook URL: https://hadayalab.app.n8n.cloud/webhook/{path}")
        else:
            print("  [WARNING] Webhookノードが見つかりません")

        # Vercel APIノードを確認
        print("\n=== Vercel API設定 ===")
        http_nodes = [n for n in nodes if 'vercel' in n.get('name', '').lower() or 'deploy' in n.get('name', '').lower()]
        if http_nodes:
            for node in http_nodes:
                params = node.get('parameters', {})
                url_param = params.get('url', 'N/A')
                print(f"  {node.get('name', 'N/A')}:")
                print(f"    URL: {url_param}")
                # 認証設定を確認
                auth = params.get('authentication', 'N/A')
                print(f"    認証: {auth}")
        else:
            print("  [WARNING] Vercel APIノードが見つかりません")

        # 環境変数の確認
        print("\n=== 環境変数チェック ===")
        print("  [INFO] n8n Dashboard → Settings → Environment Variables で以下を確認:")
        print("    - VERCEL_API_TOKEN: 設定されているか確認")

        # 接続の確認
        print("\n=== 接続確認 ===")
        connections = workflow.get('connections', {})
        if connections:
            print(f"  [OK] {len(connections)}個の接続が設定されています")
            # 主要な接続を表示
            for source, targets in list(connections.items())[:5]:
                print(f"    {source} → {len(targets.get('main', [[]])[0])}個のノードに接続")
        else:
            print("  [WARNING] 接続が設定されていません")

        print(f"\nワークフローURL: https://hadayalab.app.n8n.cloud/workflow/{workflow_id}?projectId={N8N_PROJECT_ID}")

        return workflow
    except urllib.error.HTTPError as e:
        print(f"[ERROR] ワークフロー詳細の取得に失敗しました")
        print(f"エラー: {e}")
        error_body = e.read().decode('utf-8')
        print(f"レスポンス: {error_body}")
        return None
    except Exception as e:
        print(f"[ERROR] {e}")
        return None

def main():
    print("=== インポートされたワークフローのチェック ===\n")

    # Personal Access Tokenを取得
    token = get_personal_access_token()
    if not token:
        print("[ERROR] Personal Access Tokenが取得できませんでした")
        sys.exit(1)

    # ワークフロー一覧を取得
    workflows = list_workflows(token)

    # Cursor-Vercelワークフローを検索
    target_workflow = None
    for wf in workflows:
        if 'cursor' in wf.get('name', '').lower() or 'vercel' in wf.get('name', '').lower():
            target_workflow = wf
            break

    if target_workflow:
        print(f"[OK] Cursor-Vercelワークフローが見つかりました: {target_workflow.get('name')}\n")
        check_workflow(target_workflow.get('id'), token)
    else:
        print("[WARNING] Cursor-Vercelワークフローが見つかりませんでした")
        print("[INFO] ワークフロー名を確認してください")
        print("[INFO] または、ワークフローIDを指定してチェックできます")

        # 最新のワークフローをチェック
        if workflows:
            print(f"\n最新のワークフローをチェックします: {workflows[-1].get('name')}")
            check_workflow(workflows[-1].get('id'), token)

if __name__ == "__main__":
    main()






