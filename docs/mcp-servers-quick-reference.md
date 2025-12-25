# MCPサーバー クイックリファレンス

## 📋 設定の選択

### ローカル開発用（n8n-mcp@latest）

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

**用途**: ワークフロー作成・編集、ノード検索

### n8n Cloud実装用（supergateway経由）

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

**用途**: ワークフロー実行、環境変数管理、本番環境操作

### 両方を使用する場合

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

## 🎯 使い分けガイド

| 操作 | 使用するMCP | コマンド例 |
|------|------------|-----------|
| ワークフロー作成 | `@n8n-local` | `@n8n-local 新しいワークフローを作成して` |
| ワークフロー編集 | `@n8n-local` | `@n8n-local workflow.jsonを更新して` |
| ワークフロー実行 | `@n8n-cloud` | `@n8n-cloud cursor-vercel-controlワークフローを実行して` |
| ノード検索 | `@n8n-local` | `@n8n-local HTTP Requestノードを検索して` |
| 環境変数確認 | `@n8n-cloud` | `@n8n-cloud 環境変数一覧を表示して` |
| 実行履歴確認 | `@n8n-cloud` | `@n8n-cloud 実行履歴を表示して` |

## 🔑 認証情報の取得

### n8n API Key（ローカル開発用）
1. n8n Cloud Dashboard → Settings → API
2. Generate API Key
3. Tokenをコピー

### Personal Access Token（Cloud実装用）
1. n8n Cloud Dashboard → Settings → API
2. Personal Access Tokens → Create Token
3. Tokenをコピー

## 📝 設定ファイルの場所

**Windows**: `C:\Users\chiba\.cursor\mcp.json`

## 🔄 Cursor再起動

設定変更後は必ずCursorを再起動：
1. すべてのCursorウィンドウを閉じる
2. 30秒待機
3. Cursorを再起動

---

**最終更新**: 2025-01-24

