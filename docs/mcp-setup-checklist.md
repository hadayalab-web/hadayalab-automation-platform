# MCP設定チェックリスト

このドキュメントは、MCPサーバーの設定状況を管理するためのチェックリストです。

## 📋 設定状況

### ✅ 設定済み
- [x] **n8n-local** - ローカル開発用（n8n-mcp@3.3）
- [x] **n8n-cloud** - n8n Cloud実装用（supergateway経由）
- [x] **GitHub MCP** - Cursor標準搭載（設定不要）

---

## 🔧 現在の設定

### 1. n8n-local（ローカル開発用）

**状況**: ✅ 動作中

**最新バージョン**: 2.31.1（2025-01-24時点）

**設定:**
```json
{
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
```

**確認方法:**
```
Cursor Chat: @n8n-local 利用可能なツールを表示して
```

**用途**: ワークフロー作成・編集、ノード検索

---

### 2. n8n-cloud（n8n Cloud実装用）

**状況**: ✅ 動作中

**設定:**
```json
{
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
```

**確認方法:**
```
Cursor Chat: @n8n-cloud 利用可能なツールを表示して
```

**用途**: ワークフロー実行、環境変数管理、本番環境操作

---

## 📝 使い分け

### ローカル開発
- ワークフロー作成・編集: `@n8n-local`
- ノード検索: `@n8n-local`
- テンプレート検索: `@n8n-local`

### n8n Cloud実装
- ワークフロー実行: `@n8n-cloud`
- 環境変数管理: `@n8n-cloud`
- 実行履歴確認: `@n8n-cloud`

---

## 📝 注意事項

現在、プロジェクトでは**n8n MCPを2つ**（ローカル/Cloud）を使用しています。

その他のMCPサーバー（Vercel、Google Workspace、PostgreSQL等）が必要になった場合は、n8nの対応ノードを使用することで代替できます。

---

**最終更新**: 2025-12-23
**バージョン**: 2.0.0
