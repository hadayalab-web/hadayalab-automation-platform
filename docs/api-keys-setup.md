# API Keys設定ガイド

このドキュメントは、MCPサーバーとGitHub Copilot Pro連携に必要な認証情報の取得・設定方法を説明します。

## ⚠️ 重要なセキュリティ注意事項

### .envファイルは共有しない

**❌ やってはいけないこと:**
- `.env`ファイルをGitにコミット
- `.env`ファイルを直接共有
- APIキーをチャットやメッセージで送信

**✅ 正しい方法:**
- `.env.example`をテンプレートとして使用
- 実際のAPIキーは`mcp.json`に直接設定（ローカルのみ）
- **Infisicalで一元管理**（推奨） - [Infisical設定ガイド](./infisical-setup.md) を参照
- **GitHub Secretsで管理**（CI/CD用） - [GitHub Secrets設定ガイド](./github-secrets-setup.md) を参照
- 環境変数として管理

---

## 📋 必要な認証情報一覧

### 必須（既に設定済み）

#### 1. n8n API Key

- **状況**: ✅ 既に設定済み
- **取得先**: https://hadayalab.app.n8n.cloud → Settings → API
- **設定場所**: `~/.cursor/mcp.json` の `N8N_API_KEY`
- **形式**: `n8n_api_xxxxxxxxxxxxx`

---

## 🔧 設定方法

### mcp.jsonに直接設定（推奨）

**ファイル**: `C:\Users\chiba\.cursor\mcp.json`

```json
{
  "mcpServers": {
    "n8n": {
      "command": "npx",
      "args": ["-y", "n8n-mcp"],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
        "N8N_API_KEY": "実際のAPIキーをここに",
        "LOG_LEVEL": "error",
        "NODE_NO_WARNINGS": "1"
      }
    }
  }
}
```

**メリット:**
- シンプル
- 環境変数の管理が不要
- すぐに使用可能

**デメリット:**
- ファイルに平文で保存（セキュリティリスク）
- バックアップ時に注意が必要

---

## 🔗 シークレット管理方法の選択

### Infisical（推奨）

**Infisical**を使用することで、ローカル開発、CI/CD、本番環境など、すべての環境でシークレットを一元管理できます。

**メリット:**
- ✅ 一元管理（ローカル開発、CI/CD、本番環境）
- ✅ 動的シークレットとローテーション
- ✅ 高度なアクセス制御（RBAC）
- ✅ 監査ログ

詳細は [Infisical設定ガイド](./infisical-setup.md) を参照してください。

### GitHub Secrets

CI/CDやGitHub ActionsでAPIキーを使用する場合は、**GitHub Secrets**も使用できます。

詳細は [GitHub Secrets設定ガイド](./github-secrets-setup.md) を参照してください。

### ローカル開発 vs CI/CD

- **ローカル開発（Cursor）**:
  - `mcp.json`に直接設定（簡易）
  - または Infisicalから読み込み（推奨）
- **CI/CD（GitHub Actions）**:
  - Infisicalを使用（推奨）
  - または GitHub Secretsを使用

## 📝 注意事項

現在、プロジェクトでは**n8n API Keyのみ**が必要です。

その他のMCPサーバー（Vercel、Google Workspace、PostgreSQL等）が必要になった場合は、n8nの対応ノードを使用することで代替できます。

---

**最終更新**: 2025-01-23
**バージョン**: 2.1.0
