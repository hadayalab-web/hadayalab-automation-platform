#!/usr/bin/env python3
"""
n8n Cloudのフォルダ管理スクリプト
フォルダの作成とワークフローの移動
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

# .envファイルを読み込む
env_path = Path(__file__).parent.parent / ".env"
load_env_file(env_path)

# 環境変数から設定を取得
N8N_API_URL = os.getenv("N8N_API_URL", "https://hadayalab.app.n8n.cloud")
N8N_API_KEY = os.getenv("N8N_API_KEY")

if not N8N_API_KEY:
    print("ERROR: N8N_API_KEY環境変数が設定されていません")
    sys.exit(1)

def get_workflows():
    """ワークフロー一覧を取得"""
    api_endpoint = f"{N8N_API_URL}/api/v1/workflows"
    headers = {"X-N8N-API-KEY": N8N_API_KEY}
    response = requests.get(api_endpoint, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', []) if isinstance(data, dict) and 'data' in data else data
    return []

def create_folder(name):
    """フォルダを作成"""
    # n8n Cloud APIでフォルダ作成を試行（複数のエンドポイントを試す）
    api_endpoints = [
        f"{N8N_API_URL}/api/v1/folders",
        f"{N8N_API_URL}/api/v1/workflows/folders",
    ]
    
    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }
    
    for endpoint in api_endpoints:
        try:
            response = requests.post(endpoint, json={"name": name}, headers=headers)
            if response.status_code in [200, 201]:
                folder = response.json()
                print(f"[OK] フォルダを作成しました: {name}")
                return folder.get('data') if isinstance(folder, dict) and 'data' in folder else folder
        except Exception as e:
            continue
    
    print(f"[WARN] フォルダ作成APIが見つかりませんでした。n8n Dashboardで手動作成してください: {name}")
    return None

def move_workflow_to_folder(workflow_id, folder_id):
    """ワークフローをフォルダに移動"""
    api_endpoint = f"{N8N_API_URL}/api/v1/workflows/{workflow_id}"
    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }
    
    # ワークフローを取得
    response = requests.get(api_endpoint, headers=headers)
    if response.status_code != 200:
        print(f"[ERROR] ワークフローの取得に失敗: {workflow_id}")
        return False
    
    workflow = response.json()
    
    # folderIdを更新
    workflow_data = {
        'name': workflow.get('name'),
        'nodes': workflow.get('nodes', []),
        'connections': workflow.get('connections', {}),
        'settings': workflow.get('settings', {}),
        'folderId': folder_id
    }
    
    # ワークフローを更新
    response = requests.put(api_endpoint, json=workflow_data, headers=headers)
    if response.status_code in [200, 201]:
        print(f"[OK] ワークフローを移動しました: {workflow.get('name')} → フォルダID: {folder_id}")
        return True
    else:
        print(f"[ERROR] ワークフローの移動に失敗: {workflow.get('name')}")
        print(f"   ステータスコード: {response.status_code}")
        print(f"   エラーメッセージ: {response.text}")
        return False

def main():
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python n8n-folder-management.py list")
        print("  python n8n-folder-management.py setup")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        workflows = get_workflows()
        print(f"\nワークフロー一覧 ({len(workflows)}個):\n")
        for wf in workflows:
            folder = wf.get('folder', {})
            folder_name = folder.get('name', 'なし') if folder else 'なし'
            status = "[Active]" if wf.get('active') else "[Inactive]"
            print(f"{status} {wf.get('name')} (ID: {wf.get('id')}) [フォルダ: {folder_name}]")
    
    elif command == "setup":
        print("フォルダ設定を開始します...")
        print("\n注意: n8n Cloudのフォルダ機能はn8n Dashboardで手動作成・移動する必要があります。")
        print("このスクリプトはワークフロー一覧を表示するのみです。\n")
        
        workflows = get_workflows()
        
        print("=" * 80)
        print("推奨フォルダ構成:")
        print("=" * 80)
        print("[Personal] - 私の使用用途")
        print("[hadayalab-automation-platform] - プロジェクト用途")
        print("\n現在のワークフロー一覧:")
        print("=" * 80)
        
        for wf in workflows:
            folder = wf.get('folder', {})
            folder_name = folder.get('name', 'なし') if folder else 'なし'
            status = "[Active]" if wf.get('active') else "[Inactive]"
            print(f"{status} {wf.get('name')} (ID: {wf.get('id')}) [フォルダ: {folder_name}]")
        
        print("\n" + "=" * 80)
        print("次のステップ:")
        print("1. n8n Dashboard (https://hadayalab.app.n8n.cloud) にログイン")
        print("2. 左側のサイドバーで「Workflows」をクリック")
        print("3. 「+ New」→「Folder」をクリックしてフォルダを作成")
        print("   - Personal")
        print("   - hadayalab-automation-platform")
        print("4. 各ワークフローをドラッグ&ドロップで適切なフォルダに移動")
        print("=" * 80)
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()

