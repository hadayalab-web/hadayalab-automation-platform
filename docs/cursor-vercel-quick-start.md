# Cursor-Vercel連携 クイックスタート

このガイドは、CursorからVercelを制御するための最短セットアップ手順です。

## 🚀 5分で始める

### ステップ1: Vercel API Tokenの取得（1分）

1. [Vercel Dashboard](https://vercel.com/dashboard) → Settings → Tokens
2. 「Create Token」をクリック
3. Token名を入力（例: `cursor-control`）
4. Tokenをコピー（`vck_`で始まる文字列）

### ステップ2: n8n環境変数の設定（1分）

1. [n8n Cloud](https://hadayalab.app.n8n.cloud) → Settings → Environment Variables
2. 新しい環境変数を追加:
   - **Name**: `VERCEL_API_TOKEN`
   - **Value**: ステップ1で取得したToken

### ステップ3: ワークフローのインポート（2分）

#### 方法A: n8n Dashboardから

1. n8n Dashboard → Workflows → Import from File
2. `workflow-cursor-vercel-control.json` を選択
3. インポート完了

#### 方法B: Cursorから（n8n MCP経由）

```bash
# Cursor Chatで実行
@n8n workflow-cursor-vercel-control.jsonをインポートして
```

### ステップ4: ワークフローの有効化（1分）

1. n8n Dashboardでワークフローを開く
2. 右上の「Active」スイッチをON
3. Webhook URLを確認:
   - `https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-control`

## ✅ 動作確認

### Cursor Chatからテスト

```bash
# デプロイメント一覧を取得
@n8n cursor-vercel-controlワークフローを実行して、action=list, projectId=YOUR_PROJECT_ID, limit=5で
```

### 直接HTTPリクエストでテスト

```bash
curl -X POST https://hadayalab.app.n8n.cloud/webhook/cursor-vercel-control \
  -H "Content-Type: application/json" \
  -d '{
    "action": "list",
    "projectId": "YOUR_PROJECT_ID",
    "limit": 5
  }'
```

## 📖 次のステップ

詳細な使用方法は [Cursor-Vercel連携ガイド](./cursor-vercel-integration.md) を参照してください。

---

**所要時間**: 約5分
**最終更新**: 2025-01-24






