# Cursor-Vercelワークフロー インポート確認チェックリスト

## ✅ 基本確認項目

### 1. ワークフローが正しくインポートされているか
- [ ] ワークフロー名: "Cursor-Vercel Direct Deployment Automation"
- [ ] ワークフローが表示されている
- [ ] エラーなくインポート完了

### 2. ノードの確認（全14ノード）

#### 必須ノード
- [ ] **GitHub Webhook Trigger** (n8n-nodes-base.webhook)
  - Path: `cursor-vercel-deploy`
  - Method: POST
  - Response Mode: responseNode

- [ ] **Parse GitHub Event** (n8n-nodes-base.code)
  - JavaScriptコードが正しく設定されているか

- [ ] **Check Deploy Condition** (n8n-nodes-base.if)
  - shouldDeploy条件が設定されているか

- [ ] **Trigger Vercel Deployment** (n8n-nodes-base.httpRequest)
  - URL: `https://api.vercel.com/v13/deployments`
  - Method: POST
  - Authorization Header: `Bearer {{ $env.VERCEL_API_TOKEN }}`

- [ ] **Parse Deploy Response** (n8n-nodes-base.code)
  - デプロイレスポンス解析コードが設定されているか

- [ ] **Wait 10 Seconds** (n8n-nodes-base.wait)
  - Amount: 10, Unit: seconds

- [ ] **Check Deploy Status** (n8n-nodes-base.httpRequest)
  - URL: `https://api.vercel.com/v13/deployments/{{ $json.deploymentId }}`
  - Method: GET
  - Authorization Header: `Bearer {{ $env.VERCEL_API_TOKEN }}`

- [ ] **Route Deploy Status** (n8n-nodes-base.switch)
  - 3つの出力: ready, error, building

- [ ] **Wait 30 Seconds (Retry)** (n8n-nodes-base.wait)
  - Amount: 30, Unit: seconds

- [ ] **Build Success Response** (n8n-nodes-base.set)
- [ ] **Build Error Response** (n8n-nodes-base.set)
- [ ] **Build Skip Response** (n8n-nodes-base.set)
- [ ] **Respond to Webhook** (n8n-nodes-base.respondToWebhook)

### 3. 接続の確認

#### 主要な接続パス
- [ ] GitHub Webhook Trigger → Parse GitHub Event
- [ ] Parse GitHub Event → Check Deploy Condition
- [ ] Check Deploy Condition → Trigger Vercel Deployment (true)
- [ ] Check Deploy Condition → Build Skip Response (false)
- [ ] Trigger Vercel Deployment → Parse Deploy Response
- [ ] Parse Deploy Response → Wait 10 Seconds
- [ ] Wait 10 Seconds → Check Deploy Status
- [ ] Check Deploy Status → Route Deploy Status
- [ ] Route Deploy Status → Build Success Response (ready)
- [ ] Route Deploy Status → Build Error Response (error)
- [ ] Route Deploy Status → Wait 30 Seconds (Retry) (building)
- [ ] Wait 30 Seconds (Retry) → Check Deploy Status (ループ)
- [ ] Build Success Response → Respond to Webhook
- [ ] Build Error Response → Respond to Webhook
- [ ] Build Skip Response → Respond to Webhook

## 🔧 設定確認項目

### 1. 環境変数の設定
- [ ] **VERCEL_API_TOKEN** が設定されている
  - n8n Dashboard → Settings → Environment Variables
  - 変数名: `VERCEL_API_TOKEN`
  - 値: Vercel API Token（Infisicalから取得済み）

### 2. Vercel APIノードの認証設定
- [ ] **Trigger Vercel Deployment**ノード
  - Authorization Header: `Bearer {{ $env.VERCEL_API_TOKEN }}`
  - 正しく設定されているか確認

- [ ] **Check Deploy Status**ノード
  - Authorization Header: `Bearer {{ $env.VERCEL_API_TOKEN }}`
  - 正しく設定されているか確認

### 3. Webhook URLの確認
- [ ] Webhook URLが生成されている
  - Production: `https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-deploy`
  - Test: `https://hadayalab.app.n8n.cloud/webhook-test/cursor-vercel-deploy`

## 🧪 テスト項目

### 1. テストWebhook送信
```bash
curl -X POST https://hadayalab.app.n8n.cloud/webhook-test/cursor-vercel-deploy \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: push" \
  -d '{
    "ref": "refs/heads/main",
    "repository": {
      "name": "hadayalab-automation-platform",
      "full_name": "hadayalab-web/hadayalab-automation-platform"
    },
    "head_commit": {
      "id": "abc123",
      "message": "Test commit",
      "author": {
        "name": "Test User"
      }
    }
  }'
```

### 2. 実行履歴の確認
- [ ] n8n Dashboard → Executions
- [ ] テスト実行が成功しているか確認
- [ ] エラーログがないか確認

### 3. Vercel側の確認
- [ ] Vercel Dashboardでデプロイが開始されているか
- [ ] デプロイが成功しているか
- [ ] デプロイURLが正しく生成されているか

## ⚠️ よくある問題と対処法

### 問題1: 環境変数が認識されない
**症状**: `{{ $env.VERCEL_API_TOKEN }}` が空になる
**対処法**:
1. n8n Dashboard → Settings → Environment Variables で確認
2. 変数名が正確に `VERCEL_API_TOKEN` か確認
3. ワークフローを再保存

### 問題2: Vercel API認証エラー
**症状**: 401 Unauthorized
**対処法**:
1. Vercel API Tokenが有効か確認
2. Tokenに適切な権限があるか確認
3. 環境変数が正しく設定されているか確認

### 問題3: デプロイが開始されない
**症状**: GitHub Webhookを受信してもデプロイが開始されない
**対処法**:
1. ブランチ名が `main` か確認
2. イベントタイプが `push` または `pull_request` か確認
3. `shouldDeploy` 条件が `true` になっているか確認

### 問題4: デプロイ状態が取得できない
**症状**: デプロイIDが取得できない、または状態が取得できない
**対処法**:
1. Vercel APIレスポンスの構造を確認
2. `deploymentId` の取得方法を確認
3. APIレート制限を確認

## 📋 次のステップ

1. ✅ 上記のチェックリストをすべて確認
2. ✅ テスト実行を実施
3. ✅ エラーがなければワークフローをActive化
4. ✅ GitHub Webhookを設定
5. ✅ 実際のGitHubイベントでテスト

## 🔗 参考リンク

- ワークフローJSON: `workflow-cursor-vercel-deploy.json`
- セットアップガイド: `docs/cursor-vercel-workflow-setup.md`
- インポートガイド: `docs/vercel-workflow-import-guide.md`
















