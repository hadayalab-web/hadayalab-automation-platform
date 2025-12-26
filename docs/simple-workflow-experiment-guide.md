# 簡単なワークフロー実験ガイド

## 📋 概要

このガイドでは、Cursor UIから簡単なn8nワークフローを作成・実行する実験を行います。

## 🎯 実験するワークフロー

**ワークフロー名**: `simple-time-check`

**機能**:
- Webhook TriggerでHTTPリクエストを受け取る
- World Time APIから東京の現在時刻を取得
- 整形したレスポンスをJSONで返す

## 🚀 実験手順

### ステップ1: ワークフローの検証

Cursor Chatで以下を実行：

```
@n8n-local workflows/simple-time-check.jsonを検証して
```

**期待される結果**:
- ✅ JSON構文が正しい
- ✅ ノードが存在する（Webhook, HTTP Request, Set, Respond to Webhook）
- ✅ 接続が妥当

### ステップ2: ワークフローの作成

Cursor Chatで以下を実行：

```
@n8n-local workflows/simple-time-check.jsonをインポートしてn8n Cloudに作成して
```

**期待される結果**:
- ✅ ワークフローがn8n Cloudに作成される
- ✅ ワークフローIDが返される

### ステップ3: ワークフローの詳細確認

Cursor Chatで以下を実行：

```
@n8n-cloud simple-time-checkワークフローの詳細を取得して
```

**期待される結果**:
- ✅ ワークフローの詳細情報が表示される
- ✅ Webhook URLが表示される

### ステップ4: ワークフローの実行

#### 方法1: Webhook URLで直接実行（推奨）

1. ステップ3で取得したWebhook URLをコピー
2. ブラウザまたはcurlでアクセス：

```bash
curl https://hadayalab.app.n8n.cloud/webhook/simple-time-check
```

**期待される結果**:
```json
{
  "message": "Current time in Tokyo: 2025-01-24T12:00:00+09:00",
  "timezone": "Asia/Tokyo"
}
```

#### 方法2: n8nネイティブMCPで実行

Cursor Chatで以下を実行：

```
@n8n-cloud simple-time-checkワークフローを実行して、webhookタイプで
```

**注意**: Webhook Triggerのワークフローは、MCP経由での直接実行が難しい場合があります。その場合は、方法1を使用してください。

### ステップ5: 実行履歴の確認

Cursor Chatで以下を実行：

```
@n8n-cloud simple-time-checkワークフローの実行履歴を表示して
```

**期待される結果**:
- ✅ 実行履歴が表示される
- ✅ 実行結果が確認できる

## 📊 実験結果の確認

### 成功の確認

- ✅ ワークフローが正常に作成された
- ✅ Webhook URLが取得できた
- ✅ ワークフローが正常に実行された
- ✅ 期待通りのレスポンスが返された

### トラブルシューティング

#### エラー: "Invalid workflow JSON"

**原因**: JSON構文エラーまたはノードの型バージョンが不正

**解決方法**:
1. `workflows/simple-time-check.json`の構文を確認
2. ノードの型バージョンが正しいか確認
3. 再度検証を実行

#### エラー: "Workflow not found"

**原因**: ワークフローが作成されていない、または名前が間違っている

**解決方法**:
1. ワークフロー一覧を確認: `@n8n-local ワークフロー一覧を表示して`
2. 正しいワークフロー名を使用
3. 必要に応じて再作成

#### エラー: "Webhook URL not found"

**原因**: ワークフローがアクティブになっていない、またはWebhook Triggerが正しく設定されていない

**解決方法**:
1. n8n Cloud Dashboardでワークフローがアクティブか確認
2. Webhook Triggerの設定を確認
3. ワークフローを再保存

## 🔄 次のステップ

実験が成功したら、以下の拡張を試してみましょう：

1. **パラメータの追加**: タイムゾーンをパラメータで指定できるようにする
2. **エラーハンドリング**: API呼び出し失敗時の処理を追加
3. **ログ出力**: 実行ログをSlackに通知
4. **スケジュール実行**: Schedule Triggerで定期的に実行

## 📚 参考リンク

- [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)
- [n8n Cloud同期運用](./n8n-cloud-sync.md)
- [ワークフロー命名規約](./workflow-conventions.md)

---

**最終更新**: 2025-01-24
















