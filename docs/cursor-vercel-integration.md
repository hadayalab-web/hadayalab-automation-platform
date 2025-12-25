# Cursor-Vercel連携ガイド

このドキュメントは、CursorからVercel APIを制御する方法を説明します。

## 📋 概要

CursorからVercelを制御する方法は2つあります：

1. **n8nワークフロー経由**（推奨）- 既存のn8n MCPを活用
2. **Pythonスクリプト経由** - 直接Vercel APIを呼び出し

---

## 🚀 方法1: n8nワークフロー経由（推奨）

### セットアップ

#### 1. Vercel API Tokenの取得

1. Vercel Dashboard → Settings → Tokens
2. 新しいTokenを作成（`vck_`で始まるトークン）
3. Tokenをコピー

#### 2. n8n環境変数の設定

1. n8n Dashboard → Settings → Environment Variables
2. 以下の環境変数を追加：
   - 変数名: `VERCEL_API_TOKEN`
   - 値: 作成したVercel API Token

#### 3. ワークフローのインポート

**方法A: n8n Dashboardからインポート**

1. n8n Dashboardを開く
2. Workflows → Import from File
3. `workflow-cursor-vercel-control.json` を選択
4. インポート完了

**方法B: n8n MCP経由（Cursorから）**

```bash
# Cursor Chatで実行
@n8n workflow-cursor-vercel-control.jsonをインポートして
```

#### 4. ワークフローの有効化

1. n8n Dashboardでワークフローを開く
2. 右上の「Active」スイッチをON
3. Webhook URLを確認:
   - Production: `https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-control`
   - Test: `https://hadayalab.app.n8n.cloud/webhook-test/cursor-vercel-control`

### 使用方法

#### Cursor Chatから呼び出し

```bash
# n8n MCP経由でワークフローを実行
@n8n cursor-vercel-controlワークフローを実行して、action=deploy, projectName=my-project, repository=owner/repo, branch=mainで
```

#### 直接HTTPリクエスト

```bash
curl -X POST https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-control \
  -H "Content-Type: application/json" \
  -d '{
    "action": "deploy",
    "projectName": "my-project",
    "repository": "owner/repo",
    "branch": "main"
  }'
```

### 利用可能なアクション

#### 1. deploy - デプロイメント作成

```json
{
  "action": "deploy",
  "projectName": "my-project",
  "repository": "owner/repo",
  "branch": "main"
}
```

**レスポンス例:**
```json
{
  "success": true,
  "action": "deploy",
  "deploymentId": "dpl_xxxxx",
  "deploymentUrl": "https://my-project.vercel.app",
  "state": "BUILDING",
  "timestamp": "2025-01-24T00:00:00.000Z"
}
```

#### 2. status - デプロイメントステータス確認

```json
{
  "action": "status",
  "deploymentId": "dpl_xxxxx"
}
```

**レスポンス例:**
```json
{
  "success": true,
  "action": "status",
  "deploymentId": "dpl_xxxxx",
  "deploymentUrl": "https://my-project.vercel.app",
  "state": "READY",
  "createdAt": "2025-01-24T00:00:00.000Z"
}
```

#### 3. list - デプロイメント一覧取得

```json
{
  "action": "list",
  "projectId": "prj_xxxxx",
  "limit": 10
}
```

**レスポンス例:**
```json
{
  "success": true,
  "action": "list",
  "count": 10,
  "deployments": [
    {
      "id": "dpl_xxxxx",
      "url": "https://my-project.vercel.app",
      "state": "READY"
    }
  ]
}
```

#### 4. logs - デプロイメントログ取得

```json
{
  "action": "logs",
  "deploymentId": "dpl_xxxxx"
}
```

**レスポンス例:**
```json
{
  "success": true,
  "action": "logs",
  "count": 50,
  "logs": [
    {
      "type": "stdout",
      "payload": "Build started..."
    }
  ]
}
```

#### 5. project - プロジェクト情報取得

```json
{
  "action": "project",
  "projectId": "prj_xxxxx"
}
```

**レスポンス例:**
```json
{
  "success": true,
  "action": "project",
  "projectId": "prj_xxxxx",
  "projectName": "my-project",
  "domains": ["my-project.vercel.app"]
}
```

#### 6. env - 環境変数管理

**環境変数一覧取得:**
```json
{
  "action": "env",
  "projectId": "prj_xxxxx"
}
```

**レスポンス例:**
```json
{
  "success": true,
  "action": "env",
  "count": 5,
  "envVars": [
    {
      "key": "API_KEY",
      "value": "***",
      "target": ["production", "preview"]
    }
  ]
}
```

---

## 🐍 方法2: Pythonスクリプト経由

### セットアップ

#### 1. 依存パッケージのインストール

```bash
pip install requests
```

#### 2. 環境変数の設定

```bash
# Windows PowerShell
$env:VERCEL_API_TOKEN = "vck_xxxxx"

# Windows CMD
set VERCEL_API_TOKEN=vck_xxxxx

# macOS/Linux
export VERCEL_API_TOKEN=vck_xxxxx
```

または、`.env`ファイルを作成（推奨）:
```
VERCEL_API_TOKEN=vck_xxxxx
```

### 使用方法

#### デプロイメント作成

```bash
python scripts/vercel_control.py deploy \
  --project my-project \
  --repo owner/repo \
  --branch main
```

#### デプロイメントステータス確認

```bash
python scripts/vercel_control.py status \
  --deployment-id dpl_xxxxx
```

#### デプロイメント一覧取得

```bash
python scripts/vercel_control.py list \
  --project-id prj_xxxxx \
  --limit 10
```

#### デプロイメントログ取得

```bash
python scripts/vercel_control.py logs \
  --deployment-id dpl_xxxxx
```

#### プロジェクト情報取得

```bash
python scripts/vercel_control.py project \
  --project-id prj_xxxxx
```

#### プロジェクト一覧取得

```bash
python scripts/vercel_control.py projects
```

#### 環境変数一覧取得

```bash
python scripts/vercel_control.py env list \
  --project-id prj_xxxxx
```

#### 環境変数作成

```bash
python scripts/vercel_control.py env create \
  --project-id prj_xxxxx \
  --key API_KEY \
  --value secret_value \
  --target production preview development
```

### Cursorから実行

Cursor Chatで以下のように実行できます：

```bash
# ターミナルコマンドとして実行
python scripts/vercel_control.py deploy --project my-project --repo owner/repo --branch main
```

---

## 🔄 実践的な使用例

### 例1: コード変更後の自動デプロイ

```bash
# 1. コードをコミット・プッシュ
git add .
git commit -m "Update feature"
git push origin main

# 2. Cursor Chatからデプロイ実行
@n8n cursor-vercel-controlワークフローを実行して、action=deploy, projectName=my-project, repository=owner/repo, branch=mainで
```

### 例2: デプロイメントステータスの監視

```bash
# Cursor Chatから実行
@n8n cursor-vercel-controlワークフローを実行して、action=status, deploymentId=dpl_xxxxxで
```

### 例3: エラーログの確認

```bash
# Cursor Chatから実行
@n8n cursor-vercel-controlワークフローを実行して、action=logs, deploymentId=dpl_xxxxxで
```

### 例4: 環境変数の一括管理

```bash
# Pythonスクリプトで環境変数を一括設定
python scripts/vercel_control.py env create \
  --project-id prj_xxxxx \
  --key DATABASE_URL \
  --value postgres://... \
  --target production

python scripts/vercel_control.py env create \
  --project-id prj_xxxxx \
  --key API_KEY \
  --value secret_key \
  --target production preview
```

---

## 🔧 トラブルシューティング

### エラー: 401 Unauthorized

**原因**: Vercel API Tokenが正しく設定されていない

**解決方法**:
1. Vercel DashboardでTokenが有効か確認
2. n8n環境変数または環境変数`VERCEL_API_TOKEN`が正しく設定されているか確認
3. Tokenに適切な権限があるか確認

### エラー: 404 Not Found

**原因**: プロジェクトIDまたはデプロイメントIDが間違っている

**解決方法**:
1. Vercel Dashboardで正しいIDを確認
2. プロジェクト名ではなくプロジェクトIDを使用

### エラー: デプロイが開始されない

**原因**: リポジトリがVercelに接続されていない

**解決方法**:
1. Vercel Dashboard → Projects → Add New Project
2. GitHubリポジトリを接続
3. 初回デプロイを実行

### エラー: ワークフローが見つからない

**原因**: ワークフローがインポートされていない、または無効化されている

**解決方法**:
1. n8n Dashboardでワークフローが存在するか確認
2. ワークフローがActive状態か確認
3. Webhook URLが正しいか確認

---

## 📚 参考資料

- [Vercel API Documentation](https://vercel.com/docs/rest-api)
- [Vercel API Reference](https://vercel.com/docs/rest-api/endpoints)
- [n8n Documentation](https://docs.n8n.io/)
- [n8n MCP Setup Guide](./mcp-servers-setup.md)

---

## 🎯 次のステップ

1. **ワークフローのカスタマイズ**: プロジェクトに合わせてワークフローを調整
2. **自動化の拡張**: GitHub ActionsやCI/CDパイプラインと統合
3. **モニタリング**: デプロイメントの自動監視とアラート設定
4. **環境管理**: 複数環境（staging, production）の管理

---

**最終更新**: 2025-01-24
**バージョン**: 1.0.0






