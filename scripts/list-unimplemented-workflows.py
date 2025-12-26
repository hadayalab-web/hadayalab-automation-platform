#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
プロジェクト内のn8n未実装ワークフローをリストアップ
"""
import requests
import json
import subprocess
import sys
import os
import glob

# UTF-8エンコーディング設定
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

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
        secrets = json.loads(output)
        if secrets and len(secrets) > 0:
            return secrets[0]["secretValue"]
        return None
    except Exception as e:
        print(f"[ERROR] Failed to get {secret_name} from Infisical: {e}")
        return None

def get_n8n_workflows(api_key):
    """n8nから全ワークフロー一覧を取得"""
    base_url = "https://hadayalab.app.n8n.cloud"
    api_endpoint = f"{base_url}/api/v1/workflows"

    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(api_endpoint, headers=headers, timeout=10)
        response.raise_for_status()

        result = response.json()

        if "data" in result:
            workflows = result["data"]
        else:
            workflows = result if isinstance(result, list) else []

        return workflows

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to list workflows: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return []

def get_local_workflows():
    """プロジェクト内のワークフローファイルを取得"""
    workflows_dir = "workflows"
    workflow_files = glob.glob(os.path.join(workflows_dir, "*.json"))

    local_workflows = []
    for filepath in workflow_files:
        # README.mdやindexファイルは除外
        filename = os.path.basename(filepath)
        if filename in ["README.md", "workflow-index.md"]:
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                workflow = json.load(f)
                workflow_name = workflow.get("name", filename.replace(".json", ""))
                local_workflows.append({
                    "name": workflow_name,
                    "file": filepath,
                    "filename": filename
                })
        except Exception as e:
            print(f"[WARNING] Failed to read {filepath}: {e}")

    return local_workflows

def compare_workflows(n8n_workflows, local_workflows):
    """n8nとローカルのワークフローを比較"""
    n8n_names = {wf.get("name") for wf in n8n_workflows}
    local_names = {wf["name"] for wf in local_workflows}

    # n8nに実装されているワークフロー
    implemented = local_names & n8n_names

    # n8nに未実装のワークフロー
    unimplemented = local_names - n8n_names

    # n8nにあるがローカルにないワークフロー
    n8n_only = n8n_names - local_names

    return {
        "implemented": implemented,
        "unimplemented": unimplemented,
        "n8n_only": n8n_only,
        "local_workflows": {wf["name"]: wf for wf in local_workflows}
    }

if __name__ == "__main__":
    print("=" * 60)
    print("n8n未実装ワークフローリストアップ")
    print("=" * 60)
    print()

    # InfisicalからAPIキーを取得
    print("[INFO] Getting N8N_API_KEY from Infisical...")
    api_key = get_infisical_secret("N8N_API_KEY")

    if not api_key:
        print("[ERROR] Failed to get N8N_API_KEY from Infisical")
        sys.exit(1)

    print(f"[OK] N8N_API_KEY retrieved (preview: {api_key[:20]}...)\n")

    # n8nからワークフロー一覧を取得
    print("[INFO] Fetching workflows from n8n Cloud...")
    n8n_workflows = get_n8n_workflows(api_key)
    print(f"[OK] Found {len(n8n_workflows)} workflows in n8n\n")

    # ローカルのワークフローを取得
    print("[INFO] Scanning local workflow files...")
    local_workflows = get_local_workflows()
    print(f"[OK] Found {len(local_workflows)} workflow files locally\n")

    # 比較
    comparison = compare_workflows(n8n_workflows, local_workflows)

    # 結果を表示
    print("=" * 60)
    print("📊 比較結果")
    print("=" * 60)
    print()

    # n8nに実装済み
    if comparison["implemented"]:
        print(f"✅ n8nに実装済み ({len(comparison['implemented'])}件):")
        for name in sorted(comparison["implemented"]):
            workflow_info = comparison["local_workflows"][name]
            print(f"   - {name}")
            print(f"     ファイル: {workflow_info['filename']}")
        print()

    # n8nに未実装
    if comparison["unimplemented"]:
        print(f"❌ n8nに未実装 ({len(comparison['unimplemented'])}件):")
        for name in sorted(comparison["unimplemented"]):
            workflow_info = comparison["local_workflows"][name]
            print(f"   - {name}")
            print(f"     ファイル: {workflow_info['filename']}")
        print()
    else:
        print("✅ すべてのローカルワークフローがn8nに実装済みです\n")

    # n8nのみに存在
    if comparison["n8n_only"]:
        print(f"ℹ️  n8nのみに存在 ({len(comparison['n8n_only'])}件):")
        for name in sorted(comparison["n8n_only"]):
            # n8nのワークフロー情報を取得
            n8n_wf = next((wf for wf in n8n_workflows if wf.get("name") == name), None)
            if n8n_wf:
                print(f"   - {name} (ID: {n8n_wf.get('id')}, Active: {n8n_wf.get('active', False)})")
        print()

    print("=" * 60)













