# Cursor-Vercel連携 セットアップ確認ガイド

## ✅ インポート完了確認

ワークフローID: `zUDOwmEtb3y81F3G`
URL: https://hadayalab.app.n8n.cloud/workflow/zUDOwmEtb3y81F3G

---

## 🔍 次のステップ: 動作確認

### ステップ1: 環境変数の設定確認（必須）

1. n8n Dashboard → **Settings** → **Environment Variables**
2. 以下の環境変数が設定されているか確認:
   - **Name**: `VERCEL_API_TOKEN`
   - **Value**: Vercel API Token（`vck_`で始まる文字列）

**⚠️ 未設定の場合:**
1. [Vercel Dashboard](https://vercel.com/dashboard) → Settings → Tokens
2. 新しいTokenを作成
3. n8n環境変数に追加

---

### ステップ2: ワークフローの設定確認

1. ワークフローを開く: https://hadayalab.app.n8n.cloud/workflow/zUDOwmEtb3y81F3G
2. 各ノードの設定を確認:
   - **Webhook Trigger**: Pathが `cursor-vercel-control` であることを確認
   - **HTTP Request ノード**: `VERCEL_API_TOKEN` 環境変数が使用されていることを確認

---

### ステップ3: ワークフローの有効化

1. ワークフロー画面右上の **「Active」** スイッチをON
2. Webhook URLを確認:
   - **Production**: `https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-control`
   - **Test**: `https://hadayalab.app.n8n.cloud/webhook-test/cursor-vercel-control`

---

### ステップ4: テスト実行

#### 方法A: n8n Dashboardから手動テスト

1. ワークフロー画面で **「Execute Workflow」** をクリック
2. Manual Triggerでテストデータを入力:
   ```json
   {
     "body": {
       "action": "list",
       "projectId": "YOUR_PROJECT_ID",
       "limit": 5
     }
   }
   ```
3. 実行結果を確認

#### 方法B: Webhook経由でテスト（推奨）

**PowerShell:**
```powershell
$body = @{
    action = "list"
    projectId = "YOUR_PROJECT_ID"
    limit = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://hadayalab.app.n8n.cloud/webhook-test/cursor-vercel-control" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**curl:**
```bash
curl -X POST https://hadayalab.app.n8n.cloud/webhook-test/cursor-vercel-control \
  -H "Content-Type: application/json" \
  -d '{
    "action": "list",
    "projectId": "YOUR_PROJECT_ID",
    "limit": 5
  }'
```

#### 方法C: Cursor Chatから実行

```bash
# n8n MCP経由でワークフローを実行
@n8n cursor-vercel-controlワークフローを実行して、action=list, projectId=YOUR_PROJECT_ID, limit=5で
```

---

## 🧪 テストケース

### テスト1: デプロイメント一覧取得（最も安全）

```json
{
  "action": "list",
  "projectId": "YOUR_PROJECT_ID",
  "limit": 5
}
```

**期待される結果:**
- `success: true`
- `action: "list"`
- `deployments` 配列が返される

### テスト2: プロジェクト情報取得

```json
{
  "action": "project",
  "projectId": "YOUR_PROJECT_ID"
}
```

**期待される結果:**
- `success: true`
- `action: "project"`
- `projectId` と `projectName` が返される

### テスト3: デプロイメントステータス確認

```json
{
  "action": "status",
  "deploymentId": "dpl_xxxxx"
}
```

**期待される結果:**
- `success: true`
- `action: "status"`
- `deploymentId` と `state` が返される

---

## ⚠️ トラブルシューティング

### エラー: 401 Unauthorized

**原因**: Vercel API Tokenが正しく設定されていない

**解決方法:**
1. n8n環境変数 `VERCEL_API_TOKEN` が設定されているか確認
2. Tokenが有効か確認（Vercel Dashboardで確認）
3. ワークフローを再保存

### エラー: 404 Not Found

**原因**: プロジェクトIDまたはデプロイメントIDが間違っている

**解決方法:**
1. Vercel Dashboardで正しいIDを確認
2. プロジェクト名ではなくプロジェクトIDを使用

### エラー: ワークフローが実行されない

**原因**: ワークフローがActive状態でない、またはWebhook URLが間違っている

**解決方法:**
1. ワークフローがActive状態か確認
2. Webhook URLが正しいか確認
3. テストWebhook URL（`/webhook-test/`）を使用

---

## ✅ 動作確認チェックリスト

- [ ] 環境変数 `VERCEL_API_TOKEN` が設定されている
- [ ] ワークフローがActive状態である
- [ ] Webhook URLが正しく表示されている
- [ ] テスト1（デプロイメント一覧取得）が成功
- [ ] テスト2（プロジェクト情報取得）が成功
- [ ] エラーが発生していない

---

## 🎯 次のステップ

動作確認が完了したら、以下のドキュメントを参照してください：

- [Cursor-Vercel連携ガイド](./cursor-vercel-integration.md) - 詳細な使用方法
- [クイックスタートガイド](./cursor-vercel-quick-start.md) - 基本的な使い方

---

**最終更新**: 2025-01-24
**ワークフローID**: zUDOwmEtb3y81F3G






