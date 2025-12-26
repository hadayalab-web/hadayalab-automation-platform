# n8n-mcp パッケージ バージョン情報

## 📦 最新バージョン

**最新バージョン**: `2.31.1`（2025-01-24時点）

## 🔍 バージョン確認方法

### npm経由で確認

```bash
# 最新バージョンを確認
npm view n8n-mcp version

# すべてのバージョンを確認
npm view n8n-mcp versions

# 最新の10バージョンを確認
npm view n8n-mcp versions --json | tail -10
```

### PowerShell経由で確認

```powershell
# 最新バージョンを確認
npm view n8n-mcp version

# すべてのバージョンを確認
npm view n8n-mcp versions --json | ConvertFrom-Json | Select-Object -Last 10
```

## 📋 バージョン履歴（最近の10バージョン）

- 2.31.1（最新）
- 2.31.0
- 2.30.2
- 2.30.1
- 2.30.0
- 2.29.5
- 2.29.0
- 2.28.9
- 2.28.8
- 2.28.7

## 🔧 設定での指定方法

### 最新版を使用（推奨）

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

### 特定のバージョンを指定

```json
{
  "mcpServers": {
    "n8n-local": {
      "command": "npx",
      "args": ["-y", "n8n-mcp@2.31.1"],
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

## 📚 参考リンク

- [n8n-mcp npm package](https://www.npmjs.com/package/n8n-mcp)
- [n8n-mcp GitHub](https://github.com/n8n-io/n8n-mcp)

---

**最終更新**: 2025-01-24
**最新バージョン**: 2.31.1















