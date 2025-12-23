# MCP設定チェックリスト

このドキュメントは、MCPサーバーの設定状況を管理するためのチェックリストです。

## 📋 設定状況

### ✅ 設定済み
- [x] **n8n-mcp** - ワークフロー開発の中核（動作中）
- [x] **GitHub MCP** - Cursor標準搭載（設定不要）

---

## 🔧 現在の設定

### n8n MCP Server

**状況**: ✅ 動作中

**設定:**
```json
{
  "n8n": {
    "command": "npx",
    "args": ["-y", "n8n-mcp"],
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
Cursor Chat: @n8n 利用可能なツールを表示して
```

---

## 📝 注意事項

現在、プロジェクトでは**n8n MCPのみ**を使用しています。

その他のMCPサーバー（Vercel、Google Workspace、PostgreSQL等）が必要になった場合は、n8nの対応ノードを使用することで代替できます。

---

**最終更新**: 2025-12-23
**バージョン**: 2.0.0
