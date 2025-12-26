# Cursor-Vercel連携ワークフロー セットアップガイド

## 概要

このワークフローは、GitHubのイベント（push、PR merge）をトリガーに、Vercelへの自動デプロイを実行します。

## ワークフロー機能

1. **GitHub Webhook受信**: GitHubからのpush/PRイベントを受信
2. **イベント解析**: イベントタイプとブランチを解析
3. **デプロイ条件判定**: mainブランチへのpushまたはマージされたPRのみデプロイ
4. **Vercelデプロイ実行**: Vercel APIを使用してデプロイをトリガー
5. **デプロイ状態監視**: デプロイ完了までポーリング
6. **結果通知**: デプロイ結果をWebhookレスポンスで返却

## セットアップ手順

### 1. ワークフローのインポート

#### 方法A: n8n Dashboardからインポート

1. n8n Dashboardを開く
2. Workflows → Import from File
3. `workflow-cursor-vercel-deploy.json` を選択
4. インポート完了

#### 方法B: MCPツール経由（推奨）

```bash
# ワークフローJSONを読み込んでMCPツールで作成
# （MCPツールが対応している場合）
```

### 2. Vercel API Tokenの設定

1. Vercel Dashboard → Settings → Tokens
2. 新しいTokenを作成
3. n8nの環境変数に設定:
   - 変数名: `VERCEL_API_TOKEN`
   - 値: 作成したToken

### 3. GitHub Webhookの設定

1. GitHubリポジトリ → Settings → Webhooks
2. Add webhook
3. 設定:
   - Payload URL: `https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-deploy`
   - Content type: `application/json`
   - Events: `push`, `pull_request`
   - Active: ✓

### 4. ワークフローの有効化

1. n8n Dashboardでワークフローを開く
2. 右上の「Active」スイッチをON
3. Webhook URLを確認:
   - Production: `https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-deploy`
   - Test: `https://hadayalab.app.n8n.cloud/webhook-test/cursor-vercel-deploy`

## テスト方法

### 1. テストWebhookの送信

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

## トラブルシューティング

### エラー: 401 Unauthorized

- Vercel API Tokenが正しく設定されているか確認
- Tokenに適切な権限があるか確認

### エラー: デプロイが開始されない

- GitHub Webhookが正しく設定されているか確認
- ブランチ名が`main`であることを確認
- PRイベントの場合、マージ済みか確認

### エラー: デプロイ状態が取得できない

- Vercel APIのレート制限を確認
- デプロイIDが正しく取得できているか確認

## カスタマイズ

### デプロイ条件の変更

`Parse GitHub Event`ノードのJavaScriptコードを編集:

```javascript
// 例: developブランチもデプロイ対象にする
if (eventType === 'push' && (branch === 'main' || branch === 'develop')) {
  shouldDeploy = true;
  deployReason = `Push to ${branch} branch: ${body.head_commit?.message || 'No message'}`;
}
```

### ポーリング間隔の変更

- `Wait 10 Seconds`ノード: 初回待機時間
- `Wait 30 Seconds (Retry)`ノード: リトライ間隔

### デプロイタイムアウトの設定

`Route Deploy Status`ノードにタイムアウト条件を追加

## 参考資料

- [Vercel API Documentation](https://vercel.com/docs/rest-api)
- [GitHub Webhooks Documentation](https://docs.github.com/en/webhooks)
- [n8n Documentation](https://docs.n8n.io/)















