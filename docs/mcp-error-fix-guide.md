# MCP設定エラー修正ガイド

このドキュメントは、MCPサーバーのエラーを診断・修正する手順を説明します。

## 🔍 現在の状況

### ✅ 動作中のMCPサーバー

- ✅ **n8n** - 20 tools enabled（動作中）
- ✅ **GitHub MCP** - Cursor標準搭載（設定不要）

---

## 🔧 トラブルシューティング

### n8n MCP Serverのエラー

#### エラー: "Invalid API Key" または "Unauthorized"

**原因**: n8n API Keyが正しく設定されていない、または無効

**修正手順**:
1. n8n Cloudにログイン: https://hadayalab.app.n8n.cloud
2. Settings → API → Generate API Key（または既存のAPI Keyを確認）
3. API Keyをコピー
4. `C:\Users\chiba\.cursor\mcp.json`を開く
5. `N8N_API_KEY`の値を実際のAPI Keyに置き換え
6. Cursorを再起動

**設定例**:
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

#### エラー: "Connection timeout" または "Network error"

**原因**: n8n Cloudへの接続ができない

**確認事項**:
1. インターネット接続を確認
2. `N8N_API_URL`が正しいか確認（https://hadayalab.app.n8n.cloud）
3. n8n Cloudが稼働しているか確認

---

## 📝 動作確認手順

### 各MCPサーバーの動作確認

1. **Cursor Settingsで確認**
   - Cursor Settings → Tools & MCP
   - 各MCPサーバーの状態を確認
   - "Show Output"でエラーメッセージを確認

2. **Cursor Chatで確認**
   ```
   @n8n 利用可能なツールを表示して
   ```

3. **ログを確認**
   - Cursor Settings → Tools & MCP → [MCP名] → "Show Output"
   - エラーメッセージが表示される場合は、内容を確認

---

## ⚠️ 注意事項

- API Keyを設定した後は**必ずCursorを再起動**
- エラーメッセージを必ず確認してから次へ進む
- 一つずつ修正して動作確認してから次へ

---

## 🔗 参考リンク

- [MCPサーバー設定](./mcp-servers-setup.md) - 基本的な設定方法
- [MCPトラブルシューティング](./mcp-troubleshooting.md) - より詳細なトラブルシューティング

---

**最終更新**: 2025-12-23
**バージョン**: 2.0.0
