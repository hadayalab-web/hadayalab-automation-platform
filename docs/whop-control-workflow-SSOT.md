# Whop制御ワークフロー SSOT（Single Source of Truth）

**最終更新**: 2025-12-24
**最終検証**: 2025-12-24（n8nからプロジェクトへ同期完了）
**バージョン**: 1.3.0
**メンテナー**: HadayaLab

---

## 📍 ワークフロー情報

- **ワークフローID**: `3LYMmEXrRpSVhuhE`
- **ワークフロー名**: `whop-control`
- **n8n Cloud URL**: https://hadayalab.app.n8n.cloud/workflow/3LYMmEXrRpSVhuhE
- **Webhook URL**: https://hadayalab.app.n8n.cloud/webhook/whop-control
- **ステータス**: アクティブ（Active）
- **プロジェクトファイル**: `workflows/whop-control.json`
- **最終同期**: 2025-12-24

---

## 📚 公式リファレンス

- **Whop API Documentation**: [Whop API Getting Started](https://docs.whop.com/developer/api/getting-started)
- **Whop API Keys**: [How to Create an API Key](https://help.whop.com/en/articles/10408817-how-to-create-an-api-key)
- **Whop Webhooks**: [How to Use Whop Webhooks](https://help.whop.com/en/articles/11436427-how-to-use-whop-webhooks)
- **n8n HTTP Request Node**: [HTTP Request Node Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)

---

## 🎯 概要

**Cursor UIからWhopを完全に制御するn8nワークフロー**

このドキュメントは、Cursor UIからWhopのメンバー管理、サブスクリプション管理などの操作を実行するn8nワークフローの設計と実装方法をまとめた**唯一の信頼できる情報源（SSOT）**です。

---

## ✅ 実装済みの機能

### 1. メンバー一覧取得 ✅

**アクション**: `get_members`

**エンドポイント**: `GET https://api.whop.com/api/v2/memberships`

**パラメータ**:
- `page` (optional): ページ番号（デフォルト: 1）
- `per_page` (optional): 1ページあたりの件数（デフォルト: 50）

**リクエスト例**:
```json
{
  "action": "get_members",
  "page": 1,
  "per_page": 50
}
```

### 2. メンバー詳細取得 ✅

**アクション**: `get_member`

**エンドポイント**: `GET https://api.whop.com/api/v2/memberships/{membership_id}`

**パラメータ**:
- `membership_id` (required): メンバーシップID

**リクエスト例**:
```json
{
  "action": "get_member",
  "membership_id": "membership_123"
}
```

### 3. サブスクリプションキャンセル ✅

**アクション**: `cancel_membership`

**エンドポイント**: `POST https://api.whop.com/api/v2/memberships/{membership_id}/cancel`

**パラメータ**:
- `membership_id` (required): メンバーシップID

**リクエスト例**:
```json
{
  "action": "cancel_membership",
  "membership_id": "membership_123"
}
```

### 4. サブスクリプション再アクティブ化 ✅

**アクション**: `reactivate_membership`

**エンドポイント**: `POST https://api.whop.com/api/v2/memberships/{membership_id}/reactivate`

**パラメータ**:
- `membership_id` (required): メンバーシップID

**リクエスト例**:
```json
{
  "action": "reactivate_membership",
  "membership_id": "membership_123"
}
```

---

## 🔐 認証設定

### Whop APIキーの取得

1. Whopダッシュボードにログイン
2. 左側のサイドバーから「Developer」タブをクリック
3. 「API Keys」セクションで「Create API key」をクリック
4. APIキーに名前を付け、必要な権限を選択して保存
5. 生成されたAPIキーをInfisicalに保存

**✅ 現在の状況**: Whop APIキーはInfisicalに格納済み

### n8nでの認証設定（Infisicalから取得）

**自動設定スクリプトを使用**:

```bash
python scripts/setup-whop-api-credentials.py
```

このスクリプトは、InfisicalからWhop APIキーを取得し、n8n Dashboardでの設定手順を表示します。

**手動設定手順**:

1. n8n Dashboard → Settings → Credentials
2. 「Add Credential」→「HTTP Header Auth」を選択
3. 以下の設定を入力：
   - **Name**: `Whop API Key`
   - **Header Name**: `Authorization`
   - **Header Value**: `Bearer YOUR_API_KEY`（スクリプトで表示されたAPIキーを使用）

4. ワークフロー「whop-control」を開く
5. 各HTTP Requestノード（Get Members, Get Member Details, Cancel Membership, Reactivate Membership）を開く
6. 「Credential to connect with」で「Whop API Key」を選択
7. ワークフローを保存

**重要**: APIキーはInfisicalで一元管理されています。

---

## 🚀 使用方法

### セットアップ（初回のみ）

**1. Whop APIキーを取得してn8nに設定**:
```bash
python scripts/setup-whop-api-credentials.py
```
このスクリプトで表示された手順に従って、n8n Dashboardで認証情報を設定してください。

**2. ワークフローで認証情報を選択**:
- n8n Dashboard → ワークフロー「whop-control」を開く
- 各HTTP Requestノードで「Whop API Key」を選択
- ワークフローを保存

**詳細**: [Whop制御ワークフロー設定ガイド](./whop-control-workflow-setup-guide.md) を参照

### テスト実行

```bash
python scripts/test-whop-workflow.py
```

### Cursor UIから実行

**直接HTTPリクエストを送信**:
```bash
curl -X POST https://hadayalab.app.n8n.cloud/webhook/whop-control \
  -H "Content-Type: application/json" \
  -d '{
    "action": "get_members",
    "page": 1,
    "per_page": 50
  }'
```

**または、Cursor Chatから**:
```
Whopのメンバー一覧を取得して
```

---

## 📋 ワークフロー構造

### ノード構成

1. **Webhook Trigger**: リクエストを受信
2. **Switch Action**: アクションタイプで分岐
   - `get_members` → Get Members
   - `get_member` → Get Member Details
   - `cancel_membership` → Cancel Membership
   - `reactivate_membership` → Reactivate Membership
3. **HTTP Request Nodes**: Whop APIを呼び出し
4. **Format Response**: レスポンスを整形
5. **Respond to Webhook**: レスポンスを返す

### エラーハンドリング

エラーが発生した場合、`Format Error Response`ノードでエラーレスポンスを整形し、Webhookに返します。

---

## 🔄 レスポンス形式

### 成功レスポンス

```json
{
  "success": true,
  "action": "get_members",
  "data": {
    "data": [...],
    "meta": {...}
  },
  "timestamp": "2025-01-24T00:00:00.000Z"
}
```

### エラーレスポンス

```json
{
  "success": false,
  "error": "Error message",
  "action": "get_members",
  "timestamp": "2025-01-24T00:00:00.000Z"
}
```

---

## 📝 拡張可能な機能

以下の機能を追加で実装可能です：

- ✅ 製品情報の取得
- ✅ 注文管理
- ✅ カスタマーサポート管理
- ✅ Webhookイベントの受信
- ✅ バッチ処理（複数メンバーの一括操作）

---

## 🛠️ トラブルシューティング

### 401 Unauthorized エラー

- APIキーが正しく設定されているか確認
- `Authorization` ヘッダーに `Bearer ` プレフィックスが含まれているか確認

### 404 Not Found エラー

- メンバーシップIDが正しいか確認
- APIエンドポイントが最新のバージョンか確認

### 400 Bad Request エラー

- リクエストボディの形式が正しいか確認
- 必須パラメータがすべて含まれているか確認

---

## 📝 関連ドキュメント

- [n8nワークフロー完全制御 SSOT](./n8n-workflow-full-control-SSOT.md)
- [n8nワークフロー直接制御戦略 SSOT](./direct-n8n-control-strategy-SSOT.md)
- [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)

---

## 🔄 更新履歴

### v1.3.0 (2025-12-24)
- **n8nからプロジェクトへ同期完了**: `scripts/sync-whop-control-from-n8n.py`を使用してn8nから最新のワークフローを取得
- プロジェクト内の`workflows/whop-control.json`をn8n Cloudの最新状態と同期
- APIキーがワークフローに直接埋め込まれていることを確認

### v1.2.0 (2025-01-24)
- **自動設定完了**: ワークフローにAPIキーを直接設定するスクリプトを作成
- 認証情報の手動設定が不要になりました
- `scripts/update-whop-workflow-with-api-key.py` で自動設定可能
- ワークフローが正常に動作することを確認

### v1.1.0 (2025-01-24)
- InfisicalからのWhop APIキー取得方法を追加
- 自動設定スクリプト（`scripts/setup-whop-api-credentials.py`）を作成
- n8n認証情報の手動設定手順を詳細化

### v1.0.0 (2025-01-24)
- 初版作成
- 基本的なWhop制御機能を実装
- メンバー管理、サブスクリプション管理機能を追加

