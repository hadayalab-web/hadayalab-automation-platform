# n8n環境変数確認ガイド

## 📋 概要

n8n Cloudに設定されている環境変数を確認する方法を説明します。

## 🔍 確認方法

### 方法1: n8n Dashboardから確認（推奨）

**手順**:

1. n8n Cloud Dashboardにアクセス: https://hadayalab.app.n8n.cloud
2. ログイン
3. **Settings** → **Environment Variables** に移動
4. 設定されている環境変数の一覧を確認

**メリット**:
- ✅ 最も確実な方法
- ✅ すべての環境変数を確認可能
- ✅ 値の編集も可能

### 方法2: n8nネイティブMCPを使用

**Cursor Chatで実行**:

```
@n8n-cloud 環境変数を取得して
```

または

```
@n8n-cloud 設定されている環境変数の一覧を表示して
```

**注意**: n8nネイティブMCPで環境変数を取得する機能が利用可能かどうか確認が必要です。

### 方法3: REST APIを使用（制限あり）

**注意**: MCP Access Token（`N8N_ACCESS_TOKEN`）はREST APIでは使用できない可能性があります。

**試行可能なエンドポイント**:
- `https://hadayalab.app.n8n.cloud/rest/variables`
- `https://hadayalab.app.n8n.cloud/api/v1/variables`
- `https://hadayalab.app.n8n.cloud/rest/environment-variables`
- `https://hadayalab.app.n8n.cloud/api/v1/environment-variables`

**認証**:
- Personal Access Tokenが必要（現在存在しない）
- MCP Access Tokenでは401エラーが返される可能性が高い

## ⚠️ 制限事項

### REST APIの制限

- **MCP Access Token**: REST APIでは使用不可（MCPプロトコル専用）
- **Personal Access Token**: 現在存在しない
- **結果**: REST API経由での環境変数取得は現在困難

### 推奨方法

✅ **n8n Dashboardから直接確認**が最も確実です。

## 📝 環境変数の一般的な用途

n8n Cloudで設定される環境変数の例:

- **API Keys**: 外部サービスへのアクセス用
- **Database Credentials**: データベース接続情報
- **Webhook URLs**: 外部サービスのWebhook URL
- **Configuration Values**: ワークフロー設定値

## 🔐 セキュリティ注意事項

- ⚠️ 環境変数には機密情報が含まれる可能性があります
- ⚠️ 環境変数の値は安全に管理してください
- ⚠️ 環境変数をGitにコミットしないでください

## 📚 関連ドキュメント

- [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)
- [n8nダッシュボードアクセステスト結果](./n8n-dashboard-access-test-results.md)

---

**最終更新**: 2025-01-24














