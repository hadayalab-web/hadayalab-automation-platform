# n8n-MCP設定完了

## ✅ 設定状況

n8n-MCPサーバーの設定が完了しました。

### 設定ファイル

- **パス**: `C:\Users\chiba\.cursor\mcp.json`
- **バックアップ**: 既存のファイルは `mcp.json.backup.YYYYMMDD-HHMMSS` として保存されました

### 設定内容

```json
{
  "mcpServers": {
    "n8n": {
      "command": "npx",
      "args": ["-y", "n8n-mcp"],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
        "N8N_API_KEY": "（Infisicalから取得）",
        "LOG_LEVEL": "error",
        "NODE_NO_WARNINGS": "1"
      }
    }
  }
}
```

## 🔄 次のステップ

### 1. Cursorを再起動

1. **すべてのCursorウィンドウを閉じる**
2. **30秒待機**（MCPサーバーの接続を確実に切断）
3. **Cursorを再起動**

### 2. 動作確認

Cursor AIチャットで以下を実行：

```
@n8n show available tools
```

または

```
@n8n 利用可能なツールを表示して
```

### 3. 期待される結果

n8n-MCPサーバーが正常に接続されていれば、以下のようなツール一覧が表示されます：

- `n8n_create_workflow` - ワークフロー作成
- `n8n_update_workflow` - ワークフロー更新
- `n8n_delete_workflow` - ワークフロー削除
- `n8n_list_workflows` - ワークフロー一覧取得
- `n8n_get_workflow` - ワークフロー取得
- `n8n_search_nodes` - ノード検索
- `n8n_search_templates` - テンプレート検索
- その他20個のツール

## 🔧 トラブルシューティング

### MCPサーバーが接続されない場合

1. **Cursor Settingsで確認**
   - Cursor Settings → Tools & MCP
   - n8n MCPサーバーの状態を確認
   - "Show Output"でエラーメッセージを確認

2. **mcp.jsonの構文を確認**
   - JSON構文エラーがないか確認
   - カンマや引用符の位置を確認

3. **API Keyの確認**
   - Infisicalで `N8N_API_KEY` が正しく保存されているか確認
   - n8n Cloud DashboardでAPI Keyが有効か確認

### エラーメッセージが表示される場合

詳細は [mcp-error-fix-guide.md](./mcp-error-fix-guide.md) を参照してください。

## 📝 設定スクリプト

再設定が必要な場合は、以下のスクリプトを実行：

```powershell
.\scripts\setup-n8n-mcp-simple.ps1
```

このスクリプトは：
- Infisicalから `N8N_API_KEY` を取得
- `.cursor\mcp.json` を作成・更新
- 既存のファイルをバックアップ

---

**設定日**: 2025-01-24
**ステータス**: ✅ 設定完了、Cursor再起動待ち

