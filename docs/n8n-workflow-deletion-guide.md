# n8nワークフロー削除ガイド

## 📋 削除対象ワークフロー

1. **Cursor-Vercel Direct Deployment Automation**
   - ID: `EE7Thl6p9Zsmfns4`
   - 状態: Active

2. **GitHub Docs File Deletion via Pull Request Automation**
   - ID: `p7SxbAZbmnGscON3`
   - 状態: Active

---

## 🔑 必要な認証情報

**Personal Access Token**が必要です。

### 取得方法

1. n8n Cloud Dashboardにアクセス: https://hadayalab.app.n8n.cloud
2. Settings → API → Personal Access Tokens
3. 「Create Token」をクリック
4. トークン名を入力（例: "Workflow Deletion"）
5. トークンをコピー（一度しか表示されません）

---

## 🚀 削除方法

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
    Write-Host "✅ ワークフロー1削除成功" -ForegroundColor Green
} catch {
    Write-Host "❌ エラー: $($_.Exception.Message)" -ForegroundColor Red
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

### 方法3: curlを使用

```bash
# Personal Access Tokenを設定
TOKEN="YOUR_PERSONAL_ACCESS_TOKEN"

# ワークフロー1を削除
curl -X DELETE "https://hadayalab.app.n8n.cloud/rest/workflows/EE7Thl6p9Zsmfns4" \
  -H "Authorization: Bearer $TOKEN"

# ワークフロー2を削除
curl -X DELETE "https://hadayalab.app.n8n.cloud/rest/workflows/p7SxbAZbmnGscON3" \
  -H "Authorization: Bearer $TOKEN"
```

---

## ⚠️ 注意事項

1. **削除は元に戻せません**
   - ワークフローを削除すると、すべての設定と実行履歴が失われます
   - 必要に応じて、削除前にワークフローをエクスポートしてください

2. **Active状態のワークフロー**
   - Active状態のワークフローも削除可能です
   - 削除後、Webhook URLは無効になります

3. **Personal Access Tokenの権限**
   - ワークフローの削除権限が必要です
   - 通常、Personal Access Tokenにはすべての権限が含まれます

---

## 📝 削除後の確認

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
















