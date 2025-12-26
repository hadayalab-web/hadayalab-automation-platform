#!/usr/bin/env python3
"""
n8n Cloudの既存ワークフローを更新するスクリプト
n8n APIを使用してワークフローを更新（PUTリクエスト）
"""

import json
import os
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

# .envファイルを読み込む（.env.envも確認）
env_path = Path(__file__).parent.parent / ".env"
if not env_path.exists():
    # .env.envも確認
    env_path = Path(__file__).parent.parent / ".env.env"
load_env_file(env_path)

# 環境変数から設定を取得
N8N_API_URL = os.getenv("N8N_API_URL", "https://hadayalab.app.n8n.cloud")
N8N_API_KEY = os.getenv("N8N_API_KEY")

if not N8N_API_KEY:
    print("ERROR: N8N_API_KEY環境変数が設定されていません")
    print("n8n Cloud Dashboard → Settings → API → Personal Access Tokens でトークンを取得してください")
    sys.exit(1)

def update_workflow(workflow_path: str, workflow_id: str):
    """既存のワークフローを更新"""
    
    # ワークフローファイルを読み込む
    workflow_file = Path(workflow_path)
    if not workflow_file.exists():
        print(f"ERROR: ワークフローファイルが見つかりません: {workflow_path}")
        sys.exit(1)
    
    with open(workflow_file, 'r', encoding='utf-8') as f:
        workflow_data = json.load(f)
    
    # まず既存のワークフローを取得
    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }
    
    get_endpoint = f"{N8N_API_URL}/api/v1/workflows/{workflow_id}"
    print(f"既存のワークフローを取得中: {workflow_id}")
    get_response = requests.get(get_endpoint, headers=headers)
    
    if get_response.status_code != 200:
        print(f"ERROR: ワークフローの取得に失敗しました")
        print(f"   ステータスコード: {get_response.status_code}")
        print(f"   エラーメッセージ: {get_response.text}")
        sys.exit(1)
    
    existing_workflow = get_response.json()
    print(f"既存のワークフロー名: {existing_workflow.get('name')}")
    
    # 更新するデータを準備
    # n8n APIが受け付けるプロパティのみを保持
    workflow_data_clean = {
        'name': workflow_data.get('name'),
        'nodes': workflow_data.get('nodes', []),
        'connections': workflow_data.get('connections', {}),
    }
    if 'settings' in workflow_data:
        workflow_data_clean['settings'] = workflow_data['settings']
    
    # 既存のワークフローのIDとバージョン情報を保持
    workflow_data_clean['id'] = workflow_id
    
    # n8n APIエンドポイント（PUTリクエスト）
    update_endpoint = f"{N8N_API_URL}/api/v1/workflows/{workflow_id}"
    
    # ワークフローを更新
    print(f"ワークフローを更新中: {workflow_data_clean.get('name', 'unknown')}")
    update_response = requests.put(update_endpoint, json=workflow_data_clean, headers=headers)
    
    if update_response.status_code in [200, 201]:
        workflow = update_response.json()
        print(f"[OK] ワークフローが正常に更新されました")
        print(f"   ID: {workflow.get('id')}")
        print(f"   名前: {workflow.get('name')}")
        print(f"   URL: {N8N_API_URL}/workflow/{workflow.get('id')}")
        return workflow
    else:
        print(f"ERROR: ワークフローの更新に失敗しました")
        print(f"   ステータスコード: {update_response.status_code}")
        print(f"   エラーメッセージ: {update_response.text}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("使用方法: python update-workflow-to-n8n.py <workflow.json> <workflow_id>")
        print("例: python update-workflow-to-n8n.py workflows/webhook-google-workspace-chatwork-control.json bELMAoceJ0vFNMaa")
        sys.exit(1)
    
    workflow_path = sys.argv[1]
    workflow_id = sys.argv[2]
    update_workflow(workflow_path, workflow_id)

