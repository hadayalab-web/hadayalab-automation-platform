# MCPサーバー導入ガイド

このドキュメントは、hadayalab-automation-platformプロジェクトで使用するMCP（Model Context Protocol）サーバーの設定方法を説明します。

## 📋 MCPサーバー一覧

### 設定方法の選択

用途に応じて2つの設定方法から選択できます：

1. **ローカル開発用**: n8n-mcpパッケージ（最新版: 2.31.1）を使用
2. **n8n Cloud実装用**: supergateway経由でネイティブMCPサーバーに接続

---

## 🛠️ ローカル開発用: n8n-mcpパッケージ

### 用途
- ローカル環境でのワークフロー開発
- ワークフローの作成・更新・削除
- ノード検索、テンプレート検索
- ワークフロー検証

### 設定

**ファイル**: `C:\Users\chiba\.cursor\mcp.json`

```json
{
  "mcpServers": {
    "n8n-local": {
      "command": "npx",
      "args": ["-y", "n8n-mcp@latest"],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
        "N8N_API_KEY": "<YOUR_N8N_API_KEY>",
        "LOG_LEVEL": "error",
        "NODE_NO_WARNINGS": "1"
      }
    }
  }
}
```

### 機能
- ✅ ワークフロー作成・更新・削除
- ✅ ノード検索（543個）
- ✅ テンプレート検索（2,700+）
- ✅ ワークフロー検証
- ✅ 実行履歴の確認

### 使用例

```bash
# Cursor Chatで実行
@n8n-local ワークフロー一覧を表示して
@n8n-local workflow-cursor-vercel-control.jsonをインポートして
```

---

## ☁️ n8n Cloud実装用: ネイティブMCPサーバー（supergateway経由）

### 用途
- n8n Cloudでの本番環境運用
- ワークフローの実行
- 環境変数の管理
- より高度な操作

### 設定

**ファイル**: `C:\Users\chiba\.cursor\mcp.json`

```json
{
  "mcpServers": {
    "n8n-cloud": {
      "command": "npx",
      "args": [
        "-y",
        "supergateway",
        "--streamableHttp",
        "https://hadayalab.app.n8n.cloud/mcp-server/http",
        "--header",
        "authorization:Bearer <YOUR_ACCESS_TOKEN_HERE>"
      ]
    }
  }
}
```

### 機能
- ✅ ワークフローの実行
- ✅ 環境変数の管理
- ✅ 実行履歴の詳細確認
- ✅ Webhook Triggerのワークフローも直接実行可能
- ✅ より多くの機能にアクセス可能

### 使用例

```bash
# Cursor Chatで実行
@n8n-cloud cursor-vercel-controlワークフローを実行して、action=list, projectId=xxxで
@n8n-cloud 環境変数一覧を表示して
```

### セットアップ手順

1. **Access Tokenの取得**
   - n8n Cloud Dashboard → Settings → API → Personal Access Tokens
   - Create Token → Tokenをコピー

2. **mcp.jsonの更新**
   - `<YOUR_ACCESS_TOKEN_HERE>` を実際のTokenに置き換え

3. **Cursor再起動**

**詳細**: [n8n MCP Server (supergateway経由) セットアップガイド](./n8n-mcp-supergateway-setup.md) を参照

---

## 🔧 両方を同時に使用する設定

ローカル開発とn8n Cloud実装の両方を使用する場合：

```json
{
  "mcpServers": {
    "n8n-local": {
      "command": "npx",
      "args": ["-y", "n8n-mcp@latest"],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
        "N8N_API_KEY": "<YOUR_N8N_API_KEY>",
        "LOG_LEVEL": "error",
        "NODE_NO_WARNINGS": "1"
      }
    },
    "n8n-cloud": {
      "command": "npx",
      "args": [
        "-y",
        "supergateway",
        "--streamableHttp",
        "https://hadayalab.app.n8n.cloud/mcp-server/http",
        "--header",
        "authorization:Bearer <YOUR_ACCESS_TOKEN_HERE>"
      ]
    }
  }
}
```

### 使い分け

- **ローカル開発**: `@n8n-local` を使用
  - ワークフローの作成・編集
  - ノード検索
  - テンプレート検索

- **n8n Cloud実装**: `@n8n-cloud` を使用
  - ワークフローの実行
  - 環境変数の管理
  - 本番環境での操作

---

## 📋 設定方法の比較

| 機能 | n8n-mcp (ローカル) | supergateway (Cloud) |
|------|-------------------|---------------------|
| ワークフロー作成 | ✅ | ✅ |
| ワークフロー更新 | ✅ | ✅ |
| ワークフロー削除 | ✅ | ✅ |
| ワークフロー実行 | ❌ | ✅ |
| ノード検索 | ✅ | ✅ |
| テンプレート検索 | ✅ | ✅ |
| 環境変数管理 | ❌ | ✅ |
| Webhook実行 | ❌ | ✅ |
| 実行履歴詳細 | ⚠️ 基本 | ✅ 詳細 |

---

## 📝 セットアップ手順

### 1. 認証情報の準備

#### ローカル開発用
- **n8n API Key**: n8n Cloud Dashboard → Settings → API → Generate API Key

#### n8n Cloud実装用
- **Personal Access Token**: n8n Cloud Dashboard → Settings → API → Personal Access Tokens → Create Token

### 2. mcp.jsonの更新

1. `C:\Users\chiba\.cursor\mcp.json` を開く
2. 上記の設定例を参考に、認証情報を埋める
3. JSON構文を検証

### 3. Cursor再起動

1. すべてのCursorウィンドウを閉じる
2. 30秒待機
3. Cursorを再起動

### 4. 動作確認

```bash
# ローカル開発用
@n8n-local 利用可能なツールを表示して

# n8n Cloud実装用
@n8n-cloud 利用可能なツールを表示して
```

---

## 🔗 n8nとの統合

MCPサーバーは、n8nワークフロー経由で統合管理されます：

### 統合フロー

```
Cursor AI
  ↓
n8n MCP Server (ローカル/Cloud)
  ↓
n8n Workflows
  ↓
Automated Actions
```

---

## ⚠️ 注意事項

### セキュリティ

- **認証情報の管理**: `.env`ファイルや環境変数で管理
- **mcp.json**: Gitにコミットしない（`.gitignore`に追加）
- **トークンの有効期限**: 定期的に更新

### パフォーマンス

- **LOG_LEVEL**: `"error"`に設定
- **NODE_NO_WARNINGS**: `"1"`に設定して警告を抑制

### トラブルシューティング

詳細は [mcp-troubleshooting.md](./mcp-troubleshooting.md) を参照

---

## 📚 参考リンク

- [n8n-mcp Documentation](https://www.npmjs.com/package/n8n-mcp)
- [n8n MCP Server (supergateway経由) セットアップガイド](./n8n-mcp-supergateway-setup.md)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

## 🎯 推奨設定

### 開発環境
- **ローカル開発**: `n8n-local` (n8n-mcp@3.3)
- **本番環境**: `n8n-cloud` (supergateway経由)

### 使用シーン別

| シーン | 使用するMCP |
|--------|------------|
| ワークフロー作成・編集 | `@n8n-local` |
| ワークフロー実行 | `@n8n-cloud` |
| ノード検索 | `@n8n-local` |
| 環境変数管理 | `@n8n-cloud` |
| 実行履歴確認 | `@n8n-cloud` |

---

**最終更新**: 2025-01-24
**バージョン**: 3.0.0
