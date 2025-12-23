# n8n-MCP設定エラーの診断と修正ガイド

## 問題の分析

### エラーの原因

1. **JSONパースエラー**: INFOレベルのログメッセージがstdoutに出力され、JSONレスポンスに混入
2. **プロトコルバージョン警告**: MCPクライアントとサーバーのバージョン不一致
3. **ログ出力の制御不足**: デフォルトでINFOレベルのログが出力される

## 修正内容

### 1. MCP設定ファイルの最適化

**修正前:**
```json
{
  "mcpServers": {
    "n8n": {
      "command": "n8n-mcp",
      "args": [],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
        "N8N_API_KEY": "eyJhb6ciOiJIUzI1NiIsInR5cCI6IkpXCJ9.eyJzdW..."
      }
    }
  }
}
```

**修正後:**
```json
{
  "mcpServers": {
    "n8n": {
      "command": "npx",
      "args": ["-y", "n8n-mcp"],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
        "N8N_API_KEY": "eyJhb6ciOiJIUzI1NiIsInR5cCI6IkpXCJ9.eyJzdW...",
        "LOG_LEVEL": "error",
        "NODE_NO_WARNINGS": "1"
      }
    }
  }
}
```

### 2. 修正の理由

#### `command: "npx"` と `args: ["-y", "n8n-mcp"]` を使用
- **理由**: Windows環境での実行を確実にするため
- **効果**: 最新版のn8n-mcpを自動的に使用

#### `LOG_LEVEL: "error"` を追加
- **理由**: INFOレベルのログがJSONレスポンスに混入するのを防止
- **効果**: JSONパースエラーの解消

#### `NODE_NO_WARNINGS: "1"` を追加
- **理由**: Node.jsの警告メッセージを抑制
- **効果**: クリーンな出力を確保

## トラブルシューティング手順

### a) MCPキャッシュのリセット

```powershell
# プロジェクトディレクトリ内のMCPキャッシュを確認
Get-ChildItem -Path . -Filter "*mcp*" -Recurse -ErrorAction SilentlyContinue

# キャッシュファイルが見つかった場合、内容を確認
# 空または破損している場合は {} に修正
```

### b) n8n-mcpバージョンの確認

```powershell
# 最新バージョンの確認
npx n8n-mcp@latest --version

# インストール済みバージョンの確認
npm list n8n-mcp
```

### c) 手動接続テスト

```powershell
# ログレベルをerrorに設定してテスト
$env:LOG_LEVEL="error"
$env:NODE_NO_WARNINGS="1"
npx -y n8n-mcp
```

### d) 設定の検証

```powershell
# JSON構文の検証
Get-Content C:\Users\chiba\.cursor\mcp.json | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

## 追加で実行すべきコマンド

### 1. Cursorの完全再起動

1. すべてのCursorウィンドウを閉じる
2. タスクマネージャーでCursorプロセスが残っていないか確認
3. Cursorを再起動

### 2. MCPサーバーの再初期化

Cursor再起動後、MCPサーバーが自動的に再初期化されます。

### 3. 動作確認

Cursor再起動後、以下を確認：
- MCPツールが正常に動作するか
- JSONパースエラーが発生しないか
- ワークフロー検証ツールが使用可能か

## エラーが解決しない場合の代替案

### 代替案1: グローバルインストールを使用

```json
{
  "mcpServers": {
    "n8n": {
      "command": "n8n-mcp",
      "args": [],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
        "N8N_API_KEY": "<YOUR_API_KEY>",
        "LOG_LEVEL": "error",
        "NODE_NO_WARNINGS": "1"
      }
    }
  }
}
```

### 代替案2: cmd /c を使用（Windows環境）

```json
{
  "mcpServers": {
    "n8n": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "n8n-mcp"],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
        "N8N_API_KEY": "<YOUR_API_KEY>",
        "LOG_LEVEL": "error",
        "NODE_NO_WARNINGS": "1"
      }
    }
  }
}
```

### 代替案3: 環境変数の確認

```powershell
# 環境変数の確認
$env:N8N_API_URL
$env:N8N_API_KEY
$env:LOG_LEVEL
$env:NODE_NO_WARNINGS
```

## 期待される成果物

✅ **修正されたMCP設定ファイル**: `C:\Users\chiba\.cursor\mcp.json`
✅ **修正理由の説明**: 上記の「修正の理由」セクションを参照
✅ **追加コマンドリスト**: 上記の「追加で実行すべきコマンド」を参照
✅ **代替案**: 上記の「エラーが解決しない場合の代替案」を参照

## 注意事項

- 実際のAPI KEYは `<YOUR_API_KEY>` のようにプレースホルダーとして表示
- Windows環境に適したパス形式を使用
- 段階的に問題を切り分けながら進める

## 次のステップ

1. ✅ MCP設定ファイルを修正済み
2. ⏭️ Cursorを完全に再起動
3. ⏭️ 動作確認を実施
4. ⏭️ エラーが解決しない場合は代替案を試す


