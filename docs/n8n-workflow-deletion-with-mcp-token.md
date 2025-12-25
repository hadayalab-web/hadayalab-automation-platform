# n8nワークフロー削除（MCP Access Token使用）

## 📋 概要

n8n MCP Access Tokenを使用してワークフローを削除する方法です。

**参考**: [n8n MCP Server Documentation](https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/)

---

## 🔑 MCP Access Tokenの取得

### 手順

1. n8n Cloud Dashboard → **Settings** → **MCP Access**
2. **「Access Token」タブ**をクリック
3. 表示されるAccess Tokenをコピー（`******28Qw`のようにマスクされている場合は、リフレッシュアイコンをクリックして再生成）
4. Tokenを安全な場所に保存

---

## 🚀 削除の実行

### 方法1: PowerShellスクリプトを使用（推奨）

```powershell
# MCP Access Tokenを設定
$mcpToken = "YOUR_MCP_ACCESS_TOKEN"

# スクリプトを実行
.\scripts\delete-n8n-workflows-with-mcp-token.ps1 -MCPToken $mcpToken
```

### 方法2: 直接API呼び出し

```powershell
# MCP Access Tokenを設定
$mcpToken = "YOUR_MCP_ACCESS_TOKEN"
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"

# ヘッダー設定（Bearer形式を試す）
$headers = @{
    "Authorization" = "Bearer $mcpToken"
    "Content-Type" = "application/json"
}

# ワークフロー1を削除
$workflowId1 = "EE7Thl6p9Zsmfns4"
try {
    Invoke-RestMethod -Uri "$baseUrl/workflows/$workflowId1" -Method Delete -Headers $headers
    Write-Host "✅ ワークフロー1削除成功" -ForegroundColor Green
} catch {
    Write-Host "❌ エラー: $($_.Exception.Message)" -ForegroundColor Red
    # X-N8N-API-KEY形式を試す
    $headers2 = @{
        "X-N8N-API-KEY" = $mcpToken
        "Content-Type" = "application/json"
    }
    try {
        Invoke-RestMethod -Uri "$baseUrl/workflows/$workflowId1" -Method Delete -Headers $headers2
        Write-Host "✅ ワークフロー1削除成功（X-N8N-API-KEY形式）" -ForegroundColor Green
    } catch {
        Write-Host "❌ エラー: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# ワークフロー2を削除
$workflowId2 = "p7SxbAZbmnGscON3"
try {
    Invoke-RestMethod -Uri "$baseUrl/workflows/$workflowId2" -Method Delete -Headers $headers
    Write-Host "✅ ワークフロー2削除成功" -ForegroundColor Green
} catch {
    Write-Host "❌ エラー: $($_.Exception.Message)" -ForegroundColor Red
}
```

---

## ⚠️ 注意事項

### MCP Access TokenとREST API

n8n MCP Access Tokenは、MCPプロトコル経由でのアクセス用に設計されています。REST APIでも使用できるかどうかは、n8nのバージョンや設定によって異なる可能性があります。

**確認方法**:
1. MCP Access TokenでREST APIにアクセスしてみる
2. 401エラーが返ってきた場合、Personal Access Tokenが必要な可能性があります

### 代替方法

MCP Access TokenがREST APIで使用できない場合：

1. **n8n Dashboardから手動削除**
   - Workflows → 削除したいワークフローをクリック
   - 「...」メニュー → Delete

2. **Personal Access Tokenを取得**
   - Settings → API → Personal Access Tokens（存在する場合）

---

## 📚 参考リンク

- [n8n MCP Server Documentation](https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/)
- [n8n API Documentation](https://docs.n8n.io/api/)

---

**最終更新**: 2025-01-24






