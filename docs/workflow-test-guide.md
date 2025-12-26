# Cursor-Vercelワークフロー テストガイド

## テスト方法

### 方法1: n8n Dashboardで直接テスト（推奨）

1. **ワークフローを開く**
   - https://hadayalab.app.n8n.cloud/workflow/EE7Thl6p9Zsmfns4

2. **「Execute Workflow」をクリック**
   - これでテストモードが有効になります

3. **Webhook Triggerノードをクリック**
   - ノードを選択して「Test step」をクリック
   - または、手動でテストデータを入力

4. **実行結果を確認**
   - 各ノードの出力を確認
   - エラーがないか確認

### 方法2: 本番Webhook URLでテスト

ワークフローがActiveになっている場合、本番Webhook URLを使用できます：

```bash
curl -X POST https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-deploy \
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

### 方法3: 実行履歴で確認

1. **n8n Dashboard → Executions**
2. **最新の実行を確認**
   - 成功/失敗のステータス
   - 各ノードの実行結果
   - エラーメッセージ（あれば）

## 確認ポイント

### 1. 環境変数の確認
- [ ] `VERCEL_API_TOKEN` が設定されている
- [ ] 値が正しい（Vercel API Token）

### 2. ワークフローの状態
- [ ] ワークフローがActiveになっている
- [ ] すべてのノードが正しく接続されている

### 3. 実行結果の確認
- [ ] GitHub Webhook Triggerがデータを受信
- [ ] Parse GitHub Eventが正しく動作
- [ ] Check Deploy Conditionが正しく判定
- [ ] Trigger Vercel Deploymentが成功
- [ ] Vercel側でデプロイが開始されている

### 4. Vercel側の確認
- [ ] Vercel Dashboardでデプロイが表示されている
- [ ] デプロイが成功している
- [ ] デプロイURLが生成されている

## トラブルシューティング

### エラー: 404 Not Found
**原因**: テストWebhookが有効になっていない
**対処法**:
1. n8n Dashboardで「Execute Workflow」をクリック
2. すぐにテストWebhookを送信（1回だけ有効）
3. または、本番Webhook URLを使用

### エラー: 401 Unauthorized (Vercel API)
**原因**: Vercel API Tokenが正しく設定されていない
**対処法**:
1. n8n Dashboard → Settings → Environment Variables
2. `VERCEL_API_TOKEN` が正しく設定されているか確認
3. ワークフローを再保存

### エラー: デプロイが開始されない
**原因**: デプロイ条件が満たされていない
**対処法**:
1. ブランチ名が `main` か確認
2. イベントタイプが `push` か確認
3. `shouldDeploy` が `true` になっているか確認

## 次のステップ

テストが成功したら：

1. **GitHub Webhookを設定**
   - GitHubリポジトリ → Settings → Webhooks
   - URL: `https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-deploy`
   - Events: `push`, `pull_request`

2. **実際のGitHubイベントでテスト**
   - mainブランチにpush
   - n8n Dashboardで実行履歴を確認
   - Vercel Dashboardでデプロイを確認















