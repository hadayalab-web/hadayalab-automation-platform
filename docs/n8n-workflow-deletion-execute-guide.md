# n8nワークフロー削除実行ガイド

## 📋 概要

n8n MCPパッケージの機能を使用してワークフローを削除する方法です。

**ワークフローID**: `zUDOwmEtb3y81F3G`
**ワークフローURL**: https://hadayalab.app.n8n.cloud/workflow/zUDOwmEtb3y81F3G

---

## 🚀 削除方法

### 方法1: PowerShellスクリプトを使用（推奨）

#### ステップ1: n8n API Keyを取得

n8n API Keyは以下のいずれかから取得できます：

1. **mcp.jsonから取得**
   - ファイル: `C:\Users\chiba\.cursor\mcp.json`
   - `N8N_API_KEY`の値をコピー

2. **Infisicalから取得**
   ```powershell
   $token = "YOUR_INFISICAL_TOKEN"
   $projectId = "446f131c-be8d-45e5-a83a-4154e34501a5"
   infisical secrets get N8N_API_KEY --token $token --projectId $projectId
   ```

#### ステップ2: スクリプトを実行

```powershell
# スクリプトを実行
.\scripts\delete-n8n-workflow-simple.ps1 -WorkflowId "zUDOwmEtb3y81F3G" -ApiKey "YOUR_N8N_API_KEY"
```

### 方法2: 直接API呼び出し

```powershell
# n8n API Keyを設定
$apiKey = "YOUR_N8N_API_KEY"
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"
$workflowId = "zUDOwmEtb3y81F3G"

# ヘッダー設定
$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/json"
}

# ワークフロー情報を確認
$workflow = Invoke-RestMethod -Uri "$baseUrl/workflows/$workflowId" -Method Get -Headers $headers
Write-Host "ワークフロー名: $($workflow.name)" -ForegroundColor Green

# ワークフローを削除
Invoke-RestMethod -Uri "$baseUrl/workflows/$workflowId" -Method Delete -Headers $headers
Write-Host "✅ 削除成功" -ForegroundColor Green
```

### 方法3: n8n Dashboardから手動削除

1. n8n Cloud Dashboardにアクセス: https://hadayalab.app.n8n.cloud
2. **Workflows**をクリック
3. ワークフロー「Cursor-Vercel Control API」を検索
4. ワークフローカードの右上の「...」（三点メニュー）をクリック
5. **Delete**を選択
6. 確認ダイアログで**Delete**をクリック

---

## ⚠️ 注意事項

### 削除前の確認

- ✅ ワークフローが実行中でないこと
- ✅ 他のワークフローから参照されていないこと
- ✅ 削除後、必要に応じて再作成できること

### 削除後の確認

削除後、以下のURLにアクセスして404エラーが返されることを確認：

```
https://hadayalab.app.n8n.cloud/workflow/zUDOwmEtb3y81F3G
```

---

## 📚 参考リンク

- [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)
- [n8n APIアクセスガイド](./n8n-api-access-guide.md)

---

**最終更新**: 2025-01-24















