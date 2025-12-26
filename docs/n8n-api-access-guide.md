# n8n APIアクセスガイド

## 📋 概要

n8n CloudのREST APIにアクセスするには、**Personal Access Token**が必要です。現在Infisicalから取得している`N8N_API_KEY`はMCPサーバー用のため、通常のREST APIでは使用できません。

## 🔑 認証方法

### 方法1: Personal Access Token（推奨）

n8n Cloud DashboardからPersonal Access Tokenを取得して使用します。

#### 手順

1. **n8n Cloud Dashboardにアクセス**
   - URL: `https://hadayalab.app.n8n.cloud`
   - ログイン

2. **Personal Access Tokenを作成**
   - Settings → API → Personal Access Tokens
   - 「Create Token」をクリック
   - トークン名を入力（例: "API Access Token"）
   - トークンをコピー（一度しか表示されません）

3. **Infisicalに保存**
   - Infisical Dashboard → プロジェクト `hadayalab-automation-platform-c79-q`
   - シークレット `N8N_PERSONAL_ACCESS_TOKEN` を追加
   - トークンを保存

### 方法2: MCPサーバー経由（現在の方法）

MCPサーバー用のAPIキーを使用して、MCPプロトコル経由でn8nにアクセスします。
- 用途: Cursor MCP設定で使用
- 制限: 通常のREST APIとは異なるプロトコル

## 🌐 APIエンドポイント

### 基本URL
```
https://hadayalab.app.n8n.cloud/rest/
```

### 主要エンドポイント

| エンドポイント | 説明 | メソッド |
|--------------|------|---------|
| `/rest/workflows` | ワークフロー一覧取得 | GET |
| `/rest/workflows/{id}` | ワークフロー詳細取得 | GET |
| `/rest/workflows` | ワークフロー作成 | POST |
| `/rest/workflows/{id}` | ワークフロー更新 | PUT |
| `/rest/workflows/{id}` | ワークフロー削除 | DELETE |
| `/rest/workflows/{id}/activate` | ワークフロー有効化 | POST |
| `/rest/workflows/{id}/deactivate` | ワークフロー無効化 | POST |
| `/rest/executions` | 実行履歴一覧取得 | GET |
| `/rest/executions/{id}` | 実行詳細取得 | GET |

## 🔐 認証ヘッダー

### Personal Access Tokenを使用する場合

```http
Authorization: Bearer YOUR_PERSONAL_ACCESS_TOKEN
```

または

```http
X-N8N-API-KEY: YOUR_PERSONAL_ACCESS_TOKEN
```

## 📝 使用例

### PowerShellでのAPI呼び出し例

```powershell
# Personal Access Tokenを取得（Infisicalから）
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
$projectId = "446f131c-be8d-45e5-a83a-4154e34501a5"
$personalAccessTokenJson = infisical secrets get N8N_PERSONAL_ACCESS_TOKEN --token $token --projectId $projectId --output json 2>&1 | Out-String
$personalAccessTokenObj = $personalAccessTokenJson | ConvertFrom-Json
$personalAccessToken = $personalAccessTokenObj[0].secretValue

# APIエンドポイント
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"

# ヘッダー設定
$headers = @{
    "Authorization" = "Bearer $personalAccessToken"
    "Content-Type" = "application/json"
}

# ワークフロー一覧取得
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/workflows" -Method Get -Headers $headers
    Write-Host "ワークフロー数: $($response.data.Count)"
    foreach ($workflow in $response.data) {
        Write-Host "  - $($workflow.name) (ID: $($workflow.id), Active: $($workflow.active))"
    }
} catch {
    Write-Host "エラー: $($_.Exception.Message)"
}
```

### curlでのAPI呼び出し例

```bash
# Personal Access Tokenを設定
PERSONAL_ACCESS_TOKEN="your_personal_access_token"

# ワークフロー一覧取得
curl -X GET "https://hadayalab.app.n8n.cloud/rest/workflows" \
  -H "Authorization: Bearer $PERSONAL_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

## 🚀 次のステップ

1. **Personal Access Tokenを取得**
   - n8n Cloud Dashboard → Settings → API → Personal Access Tokens
   - トークンを作成してInfisicalに保存

2. **API接続テストスクリプトを実行**
   - `scripts/test-n8n-rest-api.ps1` を実行
   - 接続が成功することを確認

3. **ワークフロー1をAPI経由でインポート**
   - `scripts/import-workflow-1.ps1` を実行（作成予定）

## 📚 参考資料

- [n8n API Documentation](https://docs.n8n.io/api/)
- [n8n API Authentication](https://docs.n8n.io/api/authentication/)
- [n8n API Reference](https://docs.n8n.io/api/api-reference/)

---

**作成日**: 2025-01-23
**ステータス**: Personal Access Token取得後にAPIアクセス可能




















