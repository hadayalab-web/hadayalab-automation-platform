# Vercel & n8n ログアクセスワークフロー ガイド

## 概要

このワークフローは、Vercelのエラーログとn8nの実行履歴を取得して確認するためのものです。

## 機能

1. **Vercelログ取得**
   - デプロイメントのログを取得
   - エラーログをフィルタリング
   - エラーの詳細を表示

2. **n8n実行履歴取得**
   - ワークフローの実行履歴を取得
   - エラーが発生した実行を抽出
   - ノードレベルのエラーも確認

3. **ログ統合**
   - Vercelとn8nのログを統合
   - エラーのサマリーを表示

## セットアップ

### 1. ワークフローのインポート

1. n8n Dashboardを開く
2. Workflows → Import from File
3. `workflow-vercel-n8n-logs.json` を選択

### 2. 環境変数の設定

n8n Dashboard → Settings → Environment Variables で以下を設定：

- **VERCEL_API_TOKEN**: Vercel API Token
- **N8N_API_KEY**: n8n API Key（実行履歴取得用）

### 3. ワークフローの有効化

- ワークフローを開く
- 右上の「Active」スイッチをON

## 使用方法

### Webhookリクエスト

```bash
curl -X POST https://hadayalab.app.n8n.cloud/webhook/get-logs \
  -H "Content-Type: application/json" \
  -d '{
    "deploymentId": "dpl_xxxxx",
    "projectId": "prj_xxxxx",
    "workflowId": "EE7Thl6p9Zsmfns4",
    "limit": 10
  }'
```

### パラメータ

- **deploymentId** (オプション): VercelデプロイメントID
- **projectId** (オプション): VercelプロジェクトID
- **workflowId** (オプション): n8nワークフローID（デフォルト: EE7Thl6p9Zsmfns4）
- **limit** (オプション): 取得件数（デフォルト: 10）

## レスポンス形式

```json
{
  "timestamp": "2025-01-24T00:00:00.000Z",
  "vercel": {
    "totalLogs": 100,
    "errorLogs": 5,
    "errors": [
      {
        "timestamp": "2025-01-24T00:00:00.000Z",
        "level": "error",
        "message": "Error message",
        "source": "build",
        "raw": {}
      }
    ]
  },
  "n8n": {
    "totalExecutions": 10,
    "errorExecutions": 2,
    "errors": [
      {
        "id": "exec_xxxxx",
        "workflowId": "EE7Thl6p9Zsmfns4",
        "nodeName": "Trigger Vercel Deployment",
        "startedAt": "2025-01-24T00:00:00.000Z",
        "error": {
          "message": "Error message",
          "stack": "Stack trace"
        }
      }
    ]
  },
  "summary": {
    "totalErrors": 7,
    "hasVercelErrors": true,
    "hasN8nErrors": true
  }
}
```

## トラブルシューティング

### エラー: 401 Unauthorized (Vercel)
- `VERCEL_API_TOKEN` が正しく設定されているか確認
- Tokenが有効か確認

### エラー: 401 Unauthorized (n8n)
- `N8N_API_KEY` が正しく設定されているか確認
- API Keyに適切な権限があるか確認

### エラー: 404 Not Found
- デプロイメントIDまたはプロジェクトIDが正しいか確認
- ワークフローIDが正しいか確認

## 次のステップ

1. ワークフローをインポート
2. 環境変数を設定
3. テスト実行
4. エラーログを確認
















