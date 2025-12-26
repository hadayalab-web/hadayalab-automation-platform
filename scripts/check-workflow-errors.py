#!/usr/bin/env python3
"""
n8nワークフローの構造を検証するスクリプト
"""

import json
import sys
from pathlib import Path

# 標準出力のエンコーディングをUTF-8に設定
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def validate_workflow(workflow_path: str):
    """ワークフローの構造を検証"""
    
    workflow_file = Path(workflow_path)
    if not workflow_file.exists():
        print(f"ERROR: ワークフローファイルが見つかりません: {workflow_path}")
        sys.exit(1)
    
    with open(workflow_file, 'r', encoding='utf-8') as f:
        workflow_data = json.load(f)
    
    print(f"ワークフロー名: {workflow_data.get('name')}")
    print(f"ノード数: {len(workflow_data.get('nodes', []))}")
    print()
    
    # 各ノードを検証
    errors = []
    
    for node in workflow_data.get('nodes', []):
        node_name = node.get('name', 'Unknown')
        node_type = node.get('type', 'Unknown')
        node_id = node.get('id', 'Unknown')
        
        # 認証情報が必要なノードをチェック
        if node_type in ['n8n-nodes-base.gmail', 'n8n-nodes-base.googleCalendar', 'n8n-nodes-base.googleDrive']:
            if 'credentials' not in node:
                errors.append(f"{node_name} ({node_id}): credentialsフィールドがありません")
            else:
                for cred_type, cred_data in node['credentials'].items():
                    if 'name' not in cred_data:
                        errors.append(f"{node_name} ({node_id}): {cred_type}のnameフィールドがありません")
                    if 'type' in cred_data:
                        print(f"WARNING: {node_name} ({node_id}): {cred_type}にtypeフィールドが含まれています（削除推奨）")
        
        # HTTP Requestノードのチェック
        if node_type == 'n8n-nodes-base.httpRequest':
            params = node.get('parameters', {})
            if 'authentication' in params:
                auth_type = params.get('authentication')
                if auth_type == 'genericCredentialType':
                    if 'genericAuthType' not in params:
                        errors.append(f"{node_name} ({node_id}): genericCredentialTypeが設定されていますが、genericAuthTypeがありません")
                elif auth_type == 'headerAuth':
                    if 'headerParameters' not in params:
                        errors.append(f"{node_name} ({node_id}): headerAuthが設定されていますが、headerParametersがありません")
    
    # 接続をチェック
    connections = workflow_data.get('connections', {})
    node_names = {node.get('id'): node.get('name') for node in workflow_data.get('nodes', [])}
    
    for source_node_id, conn_data in connections.items():
        source_name = node_names.get(source_node_id, source_node_id)
        if 'main' not in conn_data:
            errors.append(f"{source_name} ({source_node_id}): 接続データがありません")
    
    # 結果を表示
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  ❌ {error}")
        print()
        return False
    else:
        print("[OK] ワークフローの構造は正常です")
        print()
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python check-workflow-errors.py <workflow.json>")
        sys.exit(1)
    
    workflow_path = sys.argv[1]
    if validate_workflow(workflow_path):
        sys.exit(0)
    else:
        sys.exit(1)

