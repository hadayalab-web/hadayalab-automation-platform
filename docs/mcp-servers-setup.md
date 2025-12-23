# MCPサーバー導入ガイド

このドキュメントは、hadayalab-automation-platformプロジェクトで使用するMCP（Model Context Protocol）サーバーの設定方法を説明します。

## 📋 MCPサーバー一覧

### 設定済みMCPサーバー

#### 1. n8n-mcp

**状況**: ✅ 導入済み、動作中

**役割**: ワークフロー開発の中核

**統合対象**: 以下すべてのAPIをn8n経由で管理

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

**機能:**
- ワークフロー作成・更新・削除
- ノード検索（543個）
- テンプレート検索（2,700+）
- ワークフロー検証
- 実行管理

---

#### 2. GitHub MCP Server

**状況**: ✅ Cursor標準搭載

**役割**: リポジトリ管理、PR作成

**使用頻度**: 高

**設定**: Cursor標準機能のため、追加設定不要

**機能:**
- リポジトリ操作
- プルリクエスト作成・管理
- イシュー管理
- コードレビュー

---

## 🔧 完全なmcp.json設定例

```json
{
  "mcpServers": {
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
}
```

---

## 📝 設定手順

### 1. 認証情報の準備

必要な認証情報を取得：
- **n8n**: API Key（既に取得済み）

### 2. mcp.jsonの更新

1. `C:\Users\USERNAME\.cursor\mcp.json` を開く
2. 上記の設定例を参考に、認証情報を埋める
3. JSON構文を検証

### 3. Cursor再起動

1. すべてのCursorウィンドウを閉じる
2. 30秒待機
3. Cursorを再起動

### 4. 動作確認

MCPサーバーの接続を確認：

```bash
# Cursor AIチャットで実行
@n8n 利用可能なツールを表示して
```

---

## 🔗 n8nとの統合

MCPサーバーは、n8nワークフロー経由で統合管理されます：

### 統合フロー

```
Cursor AI
  ↓
n8n MCP Server
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
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

**最終更新**: 2025-12-23
**バージョン**: 2.0.0
