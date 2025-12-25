# n8n-mcpパッケージを使用したワークフロー削除

## 📋 概要

n8n-mcpパッケージの`delete_workflow`機能を使用してワークフローを削除する方法です。

**重要**: n8n-mcpパッケージは内部的にn8n REST APIを使用します。このドキュメントでは、n8n-mcpパッケージと同じREST APIエンドポイントを使用して削除を実行します。

---

## 🔧 n8n-mcpパッケージの機能

### ワークフロー削除ツール

- **ツール名**: `delete_workflow`
- **機能**: ワークフローを削除
- **パラメータ**:
  - `workflowId`: ワークフローID（必須）

### 内部実装

n8n-mcpパッケージは、内部的に以下のREST APIエンドポイントを使用します：

```
DELETE https://hadayalab.app.n8n.cloud/rest/workflows/{workflowId}
```

**認証**: `Authorization: Bearer {N8N_API_KEY}`

---

## 🚀 削除方法

### 方法1: n8n-mcpパッケージと同じREST APIを使用（推奨）

n8n-mcpパッケージが使用するのと同じREST APIエンドポイントを直接呼び出します。

#### ステップ1: n8n API Keyを取得

`C:\Users\chiba\.cursor\mcp.json`から`N8N_API_KEY`を取得します。

#### ステップ2: REST APIで削除

```powershell
# n8n API Keyを設定（mcp.jsonから取得）
$apiKey = "YOUR_N8N_API_KEY_FROM_MCP_JSON"
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"
$workflowId = "zUDOwmEtb3y81F3G"

# ヘッダー設定（n8n-mcpパッケージと同じ形式）
$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/json"
}

# ワークフロー情報を確認
Write-Host "=== ワークフロー情報を確認 ===" -ForegroundColor Cyan
try {
    $workflow = Invoke-RestMethod -Uri "$baseUrl/workflows/$workflowId" -Method Get -Headers $headers
    Write-Host "ワークフロー名: $($workflow.name)" -ForegroundColor Green
    Write-Host "状態: $(if ($workflow.active) { 'Active' } else { 'Inactive' })" -ForegroundColor Gray
    Write-Host ""

    # ワークフローを削除（n8n-mcpパッケージと同じエンドポイント）
    Write-Host "=== ワークフローを削除 ===" -ForegroundColor Cyan
    Invoke-RestMethod -Uri "$baseUrl/workflows/$workflowId" -Method Delete -Headers $headers
    Write-Host "✅ 削除成功" -ForegroundColor Green
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 404) {
        Write-Host "⚠️ ワークフローが見つかりません（既に削除されている可能性）" -ForegroundColor Yellow
    } elseif ($statusCode -eq 401) {
        Write-Host "❌ 認証エラー: API Keyが無効です" -ForegroundColor Red
    } else {
        Write-Host "❌ エラー: $($_.Exception.Message) (ステータスコード: $statusCode)" -ForegroundColor Red
    }
}
```

### 方法2: PowerShellスクリプトを使用

```powershell
.\scripts\delete-n8n-workflow-simple.ps1 -WorkflowId "zUDOwmEtb3y81F3G" -ApiKey "YOUR_N8N_API_KEY"
```

### 方法3: Cursor Chatでn8n-mcpパッケージを使用（将来の実装）

将来的には、Cursor Chatで以下のように実行できるようになる可能性があります：

```
@n8n-local ワークフロー zUDOwmEtb3y81F3G を削除して
```

**注意**: 現在、MCPツールを直接呼び出すことはできませんが、n8n-mcpパッケージが使用するREST APIエンドポイントを直接呼び出すことで、同等の機能を実現できます。

---

## 📊 n8n-mcpパッケージとREST APIの関係

### n8n-mcpパッケージの内部動作

```
Cursor Chat (@n8n-local)
  ↓
n8n-mcpパッケージ (MCP Server)
  ↓
n8n REST API
  ↓
n8n Cloud
```

### 直接REST API呼び出し

```
PowerShell Script
  ↓
n8n REST API (直接呼び出し)
  ↓
n8n Cloud
```

**結果**: どちらの方法も同じREST APIエンドポイントを使用するため、機能は同等です。

---

## ⚠️ 注意事項

### n8n-mcpパッケージの制限

- **MCPツールの直接呼び出し**: 現在、MCPツールを直接呼び出すことはできません
- **代替方法**: n8n-mcpパッケージが使用するREST APIエンドポイントを直接呼び出す

### 認証

- **n8n API Key**: `mcp.json`の`N8N_API_KEY`を使用
- **形式**: `Bearer {N8N_API_KEY}`

### 削除前の確認

- ✅ ワークフローが実行中でないこと
- ✅ 他のワークフローから参照されていないこと
- ✅ 削除後、必要に応じて再作成できること

---

## 📚 参考リンク

- [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)
- [n8n APIアクセスガイド](./n8n-api-access-guide.md)
- [n8n-mcpパッケージ Documentation](https://www.npmjs.com/package/n8n-mcp)

---

**最終更新**: 2025-01-24






