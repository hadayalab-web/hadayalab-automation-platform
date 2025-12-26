# n8nワークフロー作成ガイド

## 📋 概要

このガイドでは、Cursor UIからn8n Cloudにワークフローを作成する方法を説明します。

## 🎯 作成方法

### 方法1: n8n-mcpパッケージを使用（推奨）

**Cursor Chatで実行**:

```
@n8n-local workflows/simple-time-check.jsonをインポートしてn8n Cloudに作成して
```

または

```
@n8n-local simple-time-checkワークフローを作成して
```

**メリット**:
- ✅ Cursor UIから直接実行可能
- ✅ ワークフローの検証も同時に実行
- ✅ エラーハンドリングが自動

### 方法2: REST APIスクリプトを使用

**前提条件**:
- Personal Access Tokenが必要
- PowerShellが利用可能

**実行手順**:

1. **Personal Access Tokenを取得**:
   - n8n Cloud Dashboard → Settings → API → Personal Access Tokens
   - 新しいトークンを作成してコピー

2. **スクリプトを実行**:
   ```powershell
   .\scripts\create-n8n-workflow.ps1 -WorkflowPath "workflows/simple-time-check.json" -ApiKey "YOUR_PERSONAL_ACCESS_TOKEN"
   ```

**スクリプトの機能**:
- ✅ ワークフローファイルの読み込み
- ✅ JSON構文の検証
- ✅ n8n Cloudへの作成
- ✅ 作成されたワークフローの情報表示
- ✅ Webhook URLの表示（Webhook Trigger使用時）

### 方法3: n8n Dashboardから手動インポート

**手順**:

1. n8n Cloud Dashboardを開く: https://hadayalab.app.n8n.cloud
2. **Workflows** → **Import from File**
3. `workflows/simple-time-check.json` を選択
4. インポート完了を確認

**注意**: この方法は緊急時のみ使用（SSOT設計方針に反する）

## 🔧 必要な認証情報

### Personal Access Token

**取得方法**:
1. n8n Cloud Dashboard → **Settings** → **API** → **Personal Access Tokens**
2. **「Create Token」** をクリック
3. トークン名を入力（例: "Workflow Creation Token"）
4. **「Create」** をクリック
5. **トークンをコピー**（一度しか表示されません！）

**詳細**: [n8n Personal Access Token 取得ガイド](./n8n-personal-access-token-guide.md)

## 📝 ワークフロー作成後の確認

### 1. ワークフローの存在確認

**Cursor Chatで実行**:

```
@n8n-local simple-time-checkワークフローを検索して
```

または

```
@n8n-cloud simple-time-checkワークフローの詳細を取得して
```

### 2. Webhook URLの確認

Webhook Triggerを使用している場合、Webhook URLを確認:

```
@n8n-cloud simple-time-checkワークフローの詳細を取得して、Webhook URLを表示して
```

### 3. ワークフローの有効化

**注意**: インポートされたワークフローはデフォルトで無効（Inactive）状態です。

**有効化方法**:
- n8n Dashboardで手動で有効化
- または、REST APIで更新（`active: true`）

## ⚠️ トラブルシューティング

### エラー: "Invalid workflow JSON"

**原因**: JSON構文エラーまたはノードの型バージョンが不正

**解決方法**:
1. ワークフローファイルの構文を確認
2. `@n8n-local workflows/simple-time-check.jsonを検証して` で検証
3. エラーを修正して再実行

### エラー: "Unauthorized" または "401"

**原因**: Personal Access Tokenが無効または間違っている

**解決方法**:
1. トークンが正しくコピーされているか確認
2. トークンが有効期限内か確認
3. 新しいトークンを作成

### エラー: "Workflow already exists"

**原因**: 同じ名前のワークフローが既に存在する

**解決方法**:
1. 既存のワークフローを確認: `@n8n-local ワークフロー一覧を表示して`
2. 既存のワークフローを削除するか、名前を変更
3. 再実行

## 🔄 ワークフローの更新

既存のワークフローを更新する場合:

**Cursor Chatで実行**:

```
@n8n-local workflows/simple-time-check.jsonを更新して
```

または、REST APIスクリプトを使用（更新機能を追加予定）

## 📚 関連ドキュメント

- [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)
- [n8n Personal Access Token 取得ガイド](./n8n-personal-access-token-guide.md)
- [簡単なワークフロー実験ガイド](./simple-workflow-experiment-guide.md)
- [n8n Cloud同期運用](./n8n-cloud-sync.md)

---

**最終更新**: 2025-01-24














