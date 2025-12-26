# n8nワークフロー削除実行手順

## 📋 削除対象

1. **Cursor-Vercel Direct Deployment Automation**
   - ID: `EE7Thl6p9Zsmfns4`

2. **GitHub Docs File Deletion via Pull Request Automation**
   - ID: `p7SxbAZbmnGscON3`

---

## 🔑 ステップ1: Personal Access Tokenの取得

1. n8n Cloud Dashboardにアクセス: https://hadayalab.app.n8n.cloud
2. Settings → API → Personal Access Tokens
3. 「Create Token」をクリック
4. トークン名を入力（例: "Workflow Deletion"）
5. トークンをコピー（一度しか表示されません）

---

## 🚀 ステップ2: 削除の実行

### 方法1: PowerShellスクリプトを使用（推奨）

```powershell
# Personal Access Tokenを設定
$token = "YOUR_PERSONAL_ACCESS_TOKEN"

# スクリプトを実行
.\scripts\delete-n8n-workflows.ps1 -Token $token
```

### 方法2: 直接API呼び出し

```powershell
# Personal Access Tokenを設定
$token = "YOUR_PERSONAL_ACCESS_TOKEN"
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"

# ヘッダー設定
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

# ワークフロー1を削除
$workflowId1 = "EE7Thl6p9Zsmfns4"
try {
    Invoke-RestMethod -Uri "$baseUrl/workflows/$workflowId1" -Method Delete -Headers $headers
    Write-Host "✅ ワークフロー1削除成功: Cursor-Vercel Direct Deployment Automation" -ForegroundColor Green
} catch {
    Write-Host "❌ エラー: $($_.Exception.Message)" -ForegroundColor Red
}

# ワークフロー2を削除
$workflowId2 = "p7SxbAZbmnGscON3"
try {
    Invoke-RestMethod -Uri "$baseUrl/workflows/$workflowId2" -Method Delete -Headers $headers
    Write-Host "✅ ワークフロー2削除成功: GitHub Docs File Deletion via Pull Request Automation" -ForegroundColor Green
} catch {
    Write-Host "❌ エラー: $($_.Exception.Message)" -ForegroundColor Red
}
```

---

## ✅ 削除後の確認

削除後、ワークフロー一覧を確認：

```powershell
$token = "YOUR_PERSONAL_ACCESS_TOKEN"
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$workflows = Invoke-RestMethod -Uri "$baseUrl/workflows" -Method Get -Headers $headers
$workflows.data | Select-Object id, name, active | Format-Table
```

---

**最終更新**: 2025-01-24















