# n8n API Key 代替取得方法

## 📋 状況

n8n Cloud Dashboardに「Settings → API → Personal Access Tokens」メニューが存在しない場合の代替方法です。

---

## 🔍 確認事項

### 1. MCP Accessから取得

画像を見ると、Settingsメニューに「MCP Access」という項目があります。ここからAPI Keyを取得できる可能性があります。

**手順:**
1. Settings → **MCP Access** をクリック
2. API KeyまたはAccess Tokenが表示されるか確認
3. 表示されれば、それをコピー

### 2. 既存のAPI Keyを使用

既にMCP用のAPI Keyが設定されている場合、それがREST APIでも使用できる可能性があります。

**確認方法:**
- `C:\Users\chiba\.cursor\mcp.json` を開く
- `N8N_API_KEY` の値を確認
- このAPI KeyでREST APIにアクセスしてみる

---

## 🚀 代替方法1: 既存のAPI Keyで試す

既存のMCP用API KeyがREST APIでも使えるかテスト：

```powershell
# 既存のAPI Keyを使用（mcp.jsonから取得）
$apiKey = "YOUR_EXISTING_N8N_API_KEY"
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"

# ヘッダー設定（両方の形式を試す）
$headers1 = @{
    "X-N8N-API-KEY" = $apiKey
    "Content-Type" = "application/json"
}

$headers2 = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/json"
}

# テスト: ワークフロー一覧取得
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/workflows" -Method Get -Headers $headers1
    Write-Host "✅ X-N8N-API-KEY形式で成功" -ForegroundColor Green
    $response.data | Select-Object id, name, active
} catch {
    Write-Host "❌ X-N8N-API-KEY形式で失敗: $($_.Exception.Message)" -ForegroundColor Red

    # もう一つの形式を試す
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl/workflows" -Method Get -Headers $headers2
        Write-Host "✅ Bearer形式で成功" -ForegroundColor Green
        $response.data | Select-Object id, name, active
    } catch {
        Write-Host "❌ Bearer形式でも失敗: $($_.Exception.Message)" -ForegroundColor Red
    }
}
```

---

## 🔍 代替方法2: MCP Accessから取得

Settings → **MCP Access** から取得：

1. Settings → **MCP Access** をクリック
2. 表示される情報を確認：
   - Access Token
   - API Key
   - その他の認証情報
3. 表示されれば、それをコピーして使用

---

## 🔍 代替方法3: n8n Cloudのバージョン確認

n8n Cloudのバージョンによっては、Personal Access Token機能がまだ実装されていない可能性があります。

**確認方法:**
1. Settings → **Personal** をクリック
2. バージョン情報を確認
3. または、n8n Cloudの管理画面でバージョンを確認

**対応:**
- 古いバージョンの場合、アップグレードが必要な可能性があります
- または、既存のAPI Keyを使用する方法を試す

---

## 🔍 代替方法4: 環境変数から取得

n8n Cloudの環境変数にAPI Keyが設定されている可能性があります。

**確認方法:**
- Settings → **External Secrets** を確認
- または、n8n Cloudの管理画面で環境変数を確認

---

## 📝 推奨手順

1. **まず、MCP Accessを確認**
   - Settings → **MCP Access** をクリック
   - 表示される情報を確認

2. **既存のAPI Keyでテスト**
   - `mcp.json`の`N8N_API_KEY`を使用
   - REST APIにアクセスしてみる

3. **それでもダメな場合**
   - n8n Cloudのサポートに問い合わせ
   - または、ワークフローを手動で削除（Dashboardから）

---

## 🎯 ワークフロー削除の代替方法

Personal Access Tokenが取得できない場合、以下の方法でワークフローを削除できます：

### 方法1: n8n Dashboardから手動削除

1. n8n Dashboard → **Workflows** を開く
2. 削除したいワークフローをクリック
3. 右上の「...」メニュー → **Delete** をクリック
4. 確認ダイアログで「Delete」をクリック

### 方法2: 既存のAPI Keyで削除を試す

```powershell
# mcp.jsonからAPI Keyを取得して使用
$apiKey = "YOUR_N8N_API_KEY_FROM_MCP_JSON"
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"

$headers = @{
    "X-N8N-API-KEY" = $apiKey
    "Content-Type" = "application/json"
}

# ワークフローを削除
$workflowId = "EE7Thl6p9Zsmfns4"
try {
    Invoke-RestMethod -Uri "$baseUrl/workflows/$workflowId" -Method Delete -Headers $headers
    Write-Host "✅ 削除成功" -ForegroundColor Green
} catch {
    Write-Host "❌ エラー: $($_.Exception.Message)" -ForegroundColor Red
}
```

---

**最終更新**: 2025-01-24
















