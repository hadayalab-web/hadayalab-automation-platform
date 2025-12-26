# Cursor-Vercel連携 MCP経由確認結果

## 📋 確認日時
2025-01-24

## ✅ MCP経由で確認した内容

### 1. ワークフロー基本情報

**ワークフローID**: `zUDOwmEtb3y81F3G`
**名前**: Cursor-Vercel Control API
**状態**: ✅ Active（有効化済み）
**MCP利用可能**: ✅ `availableInMCP: true`
**作成日時**: 2025-12-24T09:53:50.652Z
**更新日時**: 2025-12-24T10:03:00.414Z
**トリガー数**: 1回

### 2. Webhook Trigger情報

**Base URL**: `https://hadayalab.app.n8n.cloud/`
**Production Path**: `/webhook/cursor-vercel-control`
**Test Path**: `/webhook-test/cursor-vercel-control`
**HTTP Method**: POST
**Response Mode**: Respond to Webhook nodeを使用
**認証**: 不要

**完全なURL**:
- Production: `https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-control`
- Test: `https://hadayalab.app.n8n.cloud/webhook-test/cursor-vercel-control`

### 3. ワークフロー構造（13ノード）

#### トリガー層
1. **Webhook Trigger** - POSTリクエストを受信

#### 処理層
2. **Parse Request** - リクエストボディを解析
3. **Route Action** - アクションタイプで分岐（6つの出力）

#### アクション層（Route Actionから分岐）
4. **Deploy to Vercel** - `action: "deploy"` の場合
5. **Get Deployment Status** - `action: "status"` の場合
6. **List Deployments** - `action: "list"` の場合
7. **Get Deployment Logs** - `action: "logs"` の場合
8. **Get Project Info** - `action: "project"` の場合
9. **Get Environment Variables** - `action: "env"` の場合
10. **Create Environment Variable** - 環境変数作成用（未使用）

#### レスポンス層
11. **Format Response** - レスポンスを整形
12. **Respond to Webhook** - Webhookレスポンスを返却
13. **Error Response** - エラーレスポンス用

### 4. 利用可能なアクション

| アクション | 説明 | 必須パラメータ | オプションパラメータ |
|-----------|------|---------------|-------------------|
| `deploy` | デプロイメント作成 | `projectName`, `repository` | `branch` (default: "main") |
| `status` | デプロイメントステータス確認 | `deploymentId` | - |
| `list` | デプロイメント一覧取得 | - | `projectId`, `limit` (default: 10) |
| `logs` | デプロイメントログ取得 | `deploymentId` | - |
| `project` | プロジェクト情報取得 | `projectId` または `projectName` | - |
| `env` | 環境変数一覧取得 | `projectId` または `projectName` | - |

### 5. ノード接続関係

```
Webhook Trigger
    ↓
Parse Request
    ↓
Route Action
    ├─→ Deploy to Vercel → Format Response
    ├─→ Get Deployment Status → Format Response
    ├─→ List Deployments → Format Response
    ├─→ Get Deployment Logs → Format Response
    ├─→ Get Project Info → Format Response
    └─→ Get Environment Variables → Format Response
                ↓
        Respond to Webhook
```

## 🔧 環境変数の確認

### 必須環境変数
- **VERCEL_API_TOKEN**: Vercel API Token（`vck_`で始まる）
  - すべてのHTTP Requestノードで使用: `Bearer {{ $env.VERCEL_API_TOKEN }}`

### 確認方法
n8n Dashboard → Settings → Environment Variables で確認

## 📊 テスト実行方法

### MCP経由での実行制限

Webhook Triggerを使用しているワークフローは、MCP経由で直接実行することができません。代わりに、Webhook URLに直接リクエストを送信する必要があります。

### 推奨テスト方法

#### 方法1: PowerShell経由（推奨）

```powershell
$body = @{
    action = "list"
    limit = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-control" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

#### 方法2: curl経由

```bash
curl -X POST https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-control \
  -H "Content-Type: application/json" \
  -d '{
    "action": "list",
    "limit": 5
  }'
```

#### 方法3: n8n Dashboard経由

1. ワークフロー画面で「Execute Workflow」をクリック
2. 以下のJSONを入力：
```json
{
  "body": {
    "action": "list",
    "limit": 5
  }
}
```

## ✅ 確認完了項目

- [x] ワークフローがActive状態である
- [x] MCP経由でワークフロー情報を取得可能
- [x] Webhook URLが正しく生成されている
- [x] ワークフロー構造が正しい
- [x] すべてのノードが正しく接続されている
- [x] 環境変数の参照が正しい（`{{ $env.VERCEL_API_TOKEN }}`）
- [ ] 環境変数 `VERCEL_API_TOKEN` が実際に設定されている（要確認）
- [ ] 実際のプロジェクトIDでテスト成功（要確認）

## 🎯 次のステップ

1. **環境変数の設定確認**
   - n8n Dashboardで `VERCEL_API_TOKEN` が設定されているか確認

2. **実際のプロジェクトIDでテスト**
   - VercelプロジェクトIDを指定してテスト実行

3. **各アクションの動作確認**
   - `list`, `project`, `status` などの各アクションをテスト

---

**最終更新**: 2025-01-24
**確認方法**: n8n MCP API経由
















