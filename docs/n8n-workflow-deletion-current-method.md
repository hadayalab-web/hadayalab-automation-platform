# n8nワークフロー削除（現状の方法）

## 📋 現状の確認

スクリーンショットから確認できる情報：
- **MCP Access Token**: Settings → MCP Access → Access Tokenタブ
- **用途**: MCPプロトコル経由（REST APIでは使用不可）
- **Personal Access Token**: Settings → API → Personal Access Tokens（メニューが存在しない可能性）

---

## ⚠️ 重要な発見

### `N8N_API_KEY`は古い情報

- **環境変数名**: `N8N_API_KEY`（n8n-mcpパッケージの設定で使用）
- **実際の値**: **Personal Access Token**を設定する
- **古い情報**: `N8N_API_KEY`という名前は古いが、実際にはPersonal Access Tokenを使用

### MCP Access TokenとPersonal Access Tokenの違い

| 項目 | MCP Access Token | Personal Access Token |
|------|-----------------|----------------------|
| **取得場所** | Settings → MCP Access → Access Tokenタブ | Settings → API → Personal Access Tokens |
| **用途** | MCPプロトコル経由 | REST API経由 |
| **n8n-mcpパッケージ** | ❌ 使用不可 | ✅ 使用可能 |
| **REST API** | ❌ 使用不可 | ✅ 使用可能 |

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

# ワークフロー情報を確認
$workflow = Invoke-RestMethod -Uri "$baseUrl/workflows/$workflowId" -Method Get -Headers $headers
Write-Host "ワークフロー名: $($workflow.name)" -ForegroundColor Green

# ワークフローを削除
Invoke-RestMethod -Uri "$baseUrl/workflows/$workflowId" -Method Delete -Headers $headers
Write-Host "✅ 削除成功" -ForegroundColor Green
```

### 方法2: n8n Dashboardから手動削除（最も確実）

Personal Access Tokenが取得できない場合：

1. n8n Cloud Dashboard → **Workflows**
2. ワークフロー「Cursor-Vercel Control API」を検索
3. ワークフローカードの「...」→ **Delete**

---

## 📚 参考リンク

- [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)
- [n8n認証方法の現状](./n8n-authentication-current-status.md)

---

**最終更新**: 2025-01-24






