# n8nワークフロー削除ガイド（手動削除）

## 📋 削除対象ワークフロー

以下の2つのワークフローを削除する必要があります：

1. **Cursor-Vercel Direct Deployment Automation**
   - ワークフローID: `EE7Thl6p9Zsmfns4`

2. **GitHub Docs File Deletion via Pull Request Automation**
   - ワークフローID: `p7SxbAZbmnGscON3`

---

## 🖱️ n8n Dashboardから手動削除（推奨）

### 手順

1. **n8n Cloud Dashboardにアクセス**
   - URL: https://hadayalab.app.n8n.cloud

2. **Workflowsページを開く**
   - 左サイドバーから「Workflows」をクリック

3. **ワークフロー1を削除**
   - 「Cursor-Vercel Direct Deployment Automation」を検索またはスクロールして見つける
   - ワークフローカードの右上の「...」（三点メニュー）をクリック
   - 「Delete」を選択
   - 確認ダイアログで「Delete」をクリック

4. **ワークフロー2を削除**
   - 「GitHub Docs File Deletion via Pull Request Automation」を検索またはスクロールして見つける
   - ワークフローカードの右上の「...」（三点メニュー）をクリック
   - 「Delete」を選択
   - 確認ダイアログで「Delete」をクリック

---

## 🔑 REST APIで削除（Personal Access Tokenが必要）

### Personal Access Tokenの取得

n8n Cloudでは、Personal Access TokenがSettings → APIメニューに存在しない場合があります。

**代替方法**:
1. n8n Cloud Dashboard → **Settings** → **API**
2. 「Personal Access Tokens」セクションがあるか確認
3. ない場合は、n8n Cloudのサポートに問い合わせるか、手動削除を使用

### API削除スクリプト

Personal Access Tokenを取得できた場合：

```powershell
# Personal Access Tokenを設定
$pat = "YOUR_PERSONAL_ACCESS_TOKEN"
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"

# ヘッダー設定
$headers = @{
    "Authorization" = "Bearer $pat"
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

---

## ⚠️ 注意事項

### MCP Access Tokenについて

- **MCP Access Token**は、MCPプロトコル経由でのアクセスのみに使用されます
- REST APIでは使用できません（401エラーが返されます）
- REST APIには**Personal Access Token**が必要です

### 削除前の確認

削除する前に、以下の点を確認してください：

1. ✅ ワークフローが実行中でないこと
2. ✅ 他のワークフローから参照されていないこと
3. ✅ 削除後、必要に応じて再作成できること

---

## 📚 参考リンク

- [n8n API Documentation](https://docs.n8n.io/api/)
- [n8n MCP Server Documentation](https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/)

---

**最終更新**: 2025-01-24






