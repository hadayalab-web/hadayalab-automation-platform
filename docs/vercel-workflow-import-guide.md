# Cursor-Vercel連携ワークフロー インポートガイド

## クイックインポート手順

### 方法1: n8n Dashboardから直接インポート（推奨）

1. **n8n Dashboardを開く**
   - URL: https://hadayalab.app.n8n.cloud
   - プロジェクト: `9D29Es58GIo6IPkZ`

2. **ワークフローをインポート**
   - 左メニュー → Workflows
   - 「Import from File」をクリック
   - `workflow-cursor-vercel-deploy.json` を選択
   - インポート完了

3. **環境変数を設定**
   - Settings → Environment Variables
   - 以下を追加:
     - **Name**: `VERCEL_API_TOKEN`
     - **Value**: Vercel API Token（Infisicalから取得済み）

4. **ワークフローを有効化**
   - ワークフローを開く
   - 右上の「Active」スイッチをON

5. **Webhook URLを確認**
   - Production: `https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-deploy`
   - Test: `https://hadayalab.app.n8n.cloud/webhook-test/cursor-vercel-deploy`

## GitHub Webhook設定

1. **GitHubリポジトリを開く**
   - Settings → Webhooks → Add webhook

2. **設定内容**
   - **Payload URL**: `https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-deploy`
   - **Content type**: `application/json`
   - **Secret**: （オプション）セキュリティのため設定推奨
   - **Events**:
     - ✓ `push`
     - ✓ `pull_request`
   - **Active**: ✓

3. **保存**

## テスト方法

### 1. テストWebhookを送信

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

### 2. 実際のGitHubイベントでテスト

1. mainブランチにpush
2. n8n Dashboardで実行履歴を確認
3. Vercel Dashboardでデプロイを確認

## 動作確認ポイント

### n8n側
- ✅ ワークフローがActiveになっている
- ✅ 実行履歴にエラーがない
- ✅ Webhook URLが正しく設定されている

### Vercel側
- ✅ デプロイが開始されている
- ✅ デプロイが成功している
- ✅ デプロイURLが正しく生成されている

## トラブルシューティング

### エラー: 401 Unauthorized (Vercel API)
- n8nの環境変数 `VERCEL_API_TOKEN` が正しく設定されているか確認
- Vercel DashboardでTokenが有効か確認

### エラー: デプロイが開始されない
- GitHub Webhookが正しく設定されているか確認
- ブランチ名が `main` であることを確認
- PRイベントの場合、マージ済みか確認

### エラー: デプロイ状態が取得できない
- Vercel APIのレート制限を確認
- デプロイIDが正しく取得できているか確認

## 次のステップ

ワークフローが正常に動作することを確認したら：

1. **本番環境で有効化**
2. **GitHub Webhookを本番URLに設定**
3. **監視設定を追加**（オプション）
















