#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡単なワークフロー作成スクリプト
"""
import os
import json
import subprocess
import requests
import sys

# Infisical設定
INFISICAL_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
PROJECT_ID = "446f131c-be8d-45e5-a83a-4154e34501a5"

def get_infisical_secret(secret_name):
    """Infisicalからシークレットを取得"""
    try:
        result = subprocess.run(
            ["infisical", "secrets", "get", secret_name, "--token", INFISICAL_TOKEN, "--projectId", PROJECT_ID, "--output", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        # JSON配列から最初の要素を取得
        secrets = json.loads(output)
        if secrets and len(secrets) > 0:
            return secrets[0]["secretValue"]
        return None
    except Exception as e:
        print(f"[ERROR] Failed to get {secret_name} from Infisical: {e}")
        return None

def create_workflow(workflow_path, api_key):
    """n8n Cloudにワークフローを作成"""
    base_url = "https://hadayalab.app.n8n.cloud"
    # 正しいエンドポイント: /api/v1/workflows（/rest/workflowsではない）
    api_endpoint = f"{base_url}/api/v1/workflows"

    # ワークフローファイルを読み込む
    print(f"[INFO] Reading workflow file: {workflow_path}")
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # 正しい認証ヘッダー: X-N8N-API-KEY（Authorization: Bearerではない）
    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    # ペイロードを準備（n8n Cloudの形式に合わせる）
    # activeとtagsフィールドはread-onlyなので含めない
    payload = {
        "name": workflow["name"],
        "nodes": workflow["nodes"],
        "connections": workflow["connections"],
        "settings": workflow.get("settings", {}),
        "staticData": workflow.get("staticData")
    }

    print(f"[INFO] Creating workflow: {workflow['name']}")

    try:
        response = requests.post(api_endpoint, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()

        # n8n Cloudのレスポンス形式を確認（dataオブジェクトでラップされている可能性）
        if "data" in result:
            workflow_data = result["data"]
        else:
            workflow_data = result

        print(f"\n[OK] Workflow created successfully!")
        print(f"\nWorkflow Information:")
        print(f"  ID: {workflow_data['id']}")
        print(f"  Name: {workflow_data['name']}")
        print(f"  Active: {workflow_data.get('active', False)}")
        print(f"  URL: {base_url}/workflow/{workflow_data['id']}")

        # Webhook URLを表示
        webhook_node = next((node for node in workflow["nodes"] if node["type"] == "n8n-nodes-base.webhook"), None)
        if webhook_node:
            webhook_id = webhook_node.get("webhookId") or webhook_node.get("parameters", {}).get("webhookId")
            if webhook_id:
                print(f"\nWebhook URL:")
                print(f"  {base_url}/webhook/{webhook_id}")

        # ワークフローIDを保存
        with open("workflow-id.txt", "w", encoding="utf-8") as f:
            f.write(workflow_data["id"])

        return workflow_data

    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Failed to create workflow: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        sys.exit(1)

if __name__ == "__main__":
    # コマンドライン引数からワークフローファイルのパスを取得
    if len(sys.argv) < 2:
        print("[ERROR] Usage: python create_workflow_simple.py <workflow_file_path>")
        print("[EXAMPLE] python create_workflow_simple.py workflows/whop-control.json")
        sys.exit(1)

    workflow_path = sys.argv[1]

    # InfisicalからPersonal Access Tokenを取得
    print("[INFO] Getting N8N_API_KEY from Infisical...")
    api_key = get_infisical_secret("N8N_API_KEY")

    if not api_key:
        print("[ERROR] Failed to get N8N_API_KEY from Infisical")
        sys.exit(1)

    print(f"[OK] N8N_API_KEY retrieved (preview: {api_key[:20]}...)")

    # ワークフローを作成
    create_workflow(workflow_path, api_key)

