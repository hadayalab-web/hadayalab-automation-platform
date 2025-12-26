# n8n認証方法の現状（2025-01-24）

## 📋 概要

n8n Cloudの認証方法について、現在利用可能な方法を整理します。

---

## 🔑 利用可能な認証方法

### 1. MCP Access Token（MCPプロトコル専用）

**取得場所**: Settings → MCP Access → Access Tokenタブ

**用途**:
- ✅ n8nネイティブMCPサーバーへの接続（supergateway経由）
- ❌ REST APIでは使用不可

**形式**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`（JWT形式）

**使用例**:
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
        "authorization:Bearer <MCP_ACCESS_TOKEN>"
      ]
    }
  }
}
```

### 2. Personal Access Token（REST API用）

**取得場所**: Settings → API → Personal Access Tokens

**用途**:
- ✅ REST APIへのアクセス
- ✅ n8n-mcpパッケージが使用（REST API経由）

**注意**:
- Settings → API → Personal Access Tokensメニューが存在しない場合がある
- その場合は、MCP Access Tokenのみが利用可能

### 3. n8n-mcpパッケージの認証

**現在の状況**:
- `N8N_API_KEY`という環境変数は**古い情報**
- 最新のn8nでは**Personal Access Token**を使用

**n8n-mcpパッケージの設定**:
```json
{
  "mcpServers": {
    "n8n-local": {
      "command": "npx",
      "args": ["-y", "n8n-mcp@latest"],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
        "N8N_API_KEY": "<PERSONAL_ACCESS_TOKEN>",  // 実際にはPersonal Access Token
        "LOG_LEVEL": "error",
        "NODE_NO_WARNINGS": "1"
      }
    }
  }
}
```

**重要**: `N8N_API_KEY`という名前ですが、実際には**Personal Access Token**を設定します。

---

## ⚠️ 重要な注意事項

### MCP Access TokenとPersonal Access Tokenの違い

| 項目 | MCP Access Token | Personal Access Token |
|------|-----------------|----------------------|
| **取得場所** | Settings → MCP Access | Settings → API → Personal Access Tokens |
| **用途** | MCPプロトコル経由 | REST API経由 |
| **n8n-mcpパッケージ** | ❌ 使用不可 | ✅ 使用可能 |
| **REST API** | ❌ 使用不可 | ✅ 使用可能 |

### n8n-mcpパッケージの認証

n8n-mcpパッケージは、内部的にn8n REST APIを使用します。そのため、**Personal Access Token**が必要です。

**環境変数名**: `N8N_API_KEY`（名前は古いが、Personal Access Tokenを設定）

---

## 🚀 ワークフロー削除の実行

### 方法1: Personal Access Tokenを使用（推奨）

Personal Access Tokenを取得して、REST APIで削除：

```powershell
# Personal Access Tokenを設定
$personalAccessToken = "YOUR_PERSONAL_ACCESS_TOKEN"
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"
$workflowId = "zUDOwmEtb3y81F3G"

$headers = @{
    "Authorization" = "Bearer $personalAccessToken"
    "Content-Type" = "application/json"
}

# ワークフローを削除
Invoke-RestMethod -Uri "$baseUrl/workflows/$workflowId" -Method Delete -Headers $headers
```

### 方法2: n8n Dashboardから手動削除

1. n8n Cloud Dashboard → Workflows
2. ワークフロー「Cursor-Vercel Control API」を検索
3. ワークフローカードの「...」→ Delete

---

## 📚 参考リンク

- [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)
- [n8n APIアクセスガイド](./n8n-api-access-guide.md)

---

**最終更新**: 2025-01-24















