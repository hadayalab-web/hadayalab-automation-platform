# n8n MCP Server (supergateway経由) セットアップガイド

## 📋 概要

`supergateway`を使用してn8n CloudのMCPサーバーにHTTP経由で直接接続する方法です。この方法により、より多くの機能にアクセスでき、ワークフローの実行なども可能になります。

## 🚀 設定方法

### 1. n8n Access Tokenの取得

1. n8n Cloud Dashboardにログイン: https://hadayalab.app.n8n.cloud
2. Settings → API → Personal Access Tokens
3. 新しいTokenを作成
4. Tokenをコピー（`n8n_api_`で始まる文字列）

### 2. mcp.jsonの設定

**ファイル**: `C:\Users\chiba\.cursor\mcp.json`

```json
{
  "mcpServers": {
    "n8n-mcp": {
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

**重要**: `<YOUR_ACCESS_TOKEN_HERE>` を実際のn8n Access Tokenに置き換えてください。

### 3. 完全な設定例

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "supergateway",
        "--streamableHttp",
        "https://hadayalab.app.n8n.cloud/mcp-server/http",
        "--header",
        "authorization:Bearer n8n_api_xxxxxxxxxxxxxxxxxxxxx"
      ]
    }
  }
}
```

## ✅ この方法の利点

### 1. より多くの機能にアクセス可能
- n8n Cloudが提供するネイティブなMCPサーバーに直接接続
- ワークフローの実行、環境変数の管理など、より高度な操作が可能

### 2. 直接接続
- n8n-mcpパッケージを経由せず、n8n CloudのMCPサーバーに直接接続
- より高速で安定した接続

### 3. ワークフロー実行
- Webhook Triggerのワークフローも直接実行可能
- より柔軟なワークフロー制御

## 🔄 従来の方法との比較

### 従来の方法（n8n-mcpパッケージ経由）

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

**特徴**:
- n8n-mcpパッケージを経由
- 基本的なワークフロー操作（作成、更新、削除、検索）
- Webhook Triggerのワークフローは直接実行不可

### 新しい方法（supergateway経由）

```json
{
  "mcpServers": {
    "n8n-mcp": {
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

**特徴**:
- n8n CloudのMCPサーバーに直接接続
- より多くの機能にアクセス可能
- ワークフローの実行も可能

## 📝 セットアップ手順

### ステップ1: Access Tokenの取得

1. n8n Cloud Dashboard → Settings → API
2. Personal Access Tokens → Create Token
3. Token名を入力（例: `cursor-mcp`）
4. Tokenをコピー

### ステップ2: mcp.jsonの更新

1. `C:\Users\chiba\.cursor\mcp.json` を開く
2. 上記の設定例を参考に、Access Tokenを設定
3. JSON構文を検証

### ステップ3: Cursor再起動

1. すべてのCursorウィンドウを閉じる
2. 30秒待機
3. Cursorを再起動

### ステップ4: 動作確認

```bash
# Cursor Chatで実行
@n8n-mcp 利用可能なツールを表示して
```

## 🔧 トラブルシューティング

### エラー: "Invalid token" または "Unauthorized"

**原因**: Access Tokenが正しく設定されていない、または無効

**解決方法**:
1. n8n Cloud DashboardでTokenが有効か確認
2. `mcp.json`の`authorization:Bearer`の後に正しいTokenが設定されているか確認
3. Tokenに適切な権限があるか確認

### エラー: "Connection failed"

**原因**: n8n Cloudへの接続ができない

**確認事項**:
1. インターネット接続を確認
2. `https://hadayalab.app.n8n.cloud/mcp-server/http` が正しいか確認
3. n8n Cloudが稼働しているか確認

### エラー: "supergateway not found"

**原因**: supergatewayパッケージがインストールされていない

**解決方法**:
```bash
npm install -g supergateway
```

または、`npx -y supergateway`を使用（推奨）

## 📚 参考リンク

- [n8n MCP Server Documentation](https://docs.n8n.io/integrations/mcp/)
- [supergateway Documentation](https://www.npmjs.com/package/supergateway)

---

**最終更新**: 2025-01-24
**推奨**: ✅ この方法を推奨（より多くの機能にアクセス可能）






