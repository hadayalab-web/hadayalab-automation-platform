# Whop制御ワークフロー設定ガイド

**最終更新**: 2025-01-24
**バージョン**: 1.0.0

---

## ✅ 現在の状況

- ✅ ワークフロー作成完了: `whop-control` (ID: `3LYMmEXrRpSVhuhE`)
- ✅ ワークフローアクティブ化完了
- ✅ Whop APIキー取得完了（Infisicalから取得可能）
- ✅ Webhook URL確認: https://hadayalab.app.n8n.cloud/webhook/whop-control
- ⚠️ n8n Dashboardでの認証情報設定が必要

---

## 🔧 設定手順

### ステップ1: Whop APIキーを取得

```bash
python scripts/setup-whop-api-credentials.py
```

このスクリプトを実行すると、InfisicalからWhop APIキーを取得し、設定手順が表示されます。

### ステップ2: n8n Dashboardで認証情報を設定

1. **n8n Dashboardにアクセス**
   - URL: https://hadayalab.app.n8n.cloud
   - ログイン

2. **Settings → Credentials に移動**

3. **「Add Credential」をクリック**

4. **「HTTP Header Auth」を選択**

5. **以下の情報を入力**:
   - **Name**: `Whop API Key`
   - **Header Name**: `Authorization`
   - **Header Value**: `Bearer apik_KbyD0T3ENibNW_C...`（スクリプトで表示された完全なAPIキー）

6. **「Save」をクリック**

### ステップ3: ワークフローで認証情報を設定

1. **ワークフロー「whop-control」を開く**
   - URL: https://hadayalab.app.n8n.cloud/workflow/3LYMmEXrRpSVhuhE

2. **各HTTP Requestノードを開く**:
   - **Get Members** ノード
   - **Get Member Details** ノード
   - **Cancel Membership** ノード
   - **Reactivate Membership** ノード

3. **各ノードで認証情報を設定**:
   - 「Credential to connect with」セクションを開く
   - 「Whop API Key」を選択
   - 「Save」をクリック

4. **ワークフローを保存**

### ステップ4: テスト実行

```bash
python scripts/test-whop-workflow.py
```

このスクリプトは以下をテストします：
- Whop APIキーの有効性
- ワークフローのWebhook動作

---

## 🧪 手動テスト

### メンバー一覧取得

```bash
curl -X POST https://hadayalab.app.n8n.cloud/webhook/whop-control \
  -H "Content-Type: application/json" \
  -d '{
    "action": "get_members",
    "page": 1,
    "per_page": 10
  }'
```

### メンバー詳細取得

```bash
curl -X POST https://hadayalab.app.n8n.cloud/webhook/whop-control \
  -H "Content-Type: application/json" \
  -d '{
    "action": "get_member",
    "membership_id": "YOUR_MEMBERSHIP_ID"
  }'
```

---

## 📊 実行結果の確認

### n8n Dashboardで確認

1. **Executions に移動**
   - URL: https://hadayalab.app.n8n.cloud/executions

2. **最新の実行を確認**
   - 成功: 緑色のチェックマーク
   - 失敗: 赤色のエラーアイコン

3. **実行詳細を確認**
   - 各ノードの実行結果
   - エラーメッセージ（ある場合）

---

## ⚠️ トラブルシューティング

### エラー: 401 Unauthorized

**原因**: 認証情報が設定されていない、または間違っている

**解決方法**:
1. n8n Dashboard → Credentials で「Whop API Key」が存在するか確認
2. Header Valueが `Bearer YOUR_API_KEY` 形式になっているか確認
3. 各HTTP Requestノードで認証情報が選択されているか確認

### エラー: 404 Not Found

**原因**: ワークフローがアクティブでない、またはWebhook URLが間違っている

**解決方法**:
1. ワークフローがアクティブか確認
2. Webhook URLが正しいか確認: https://hadayalab.app.n8n.cloud/webhook/whop-control

### エラー: 500 Internal Server Error

**原因**: ワークフロー内のノード設定に問題がある

**解決方法**:
1. n8n Dashboard → Executions でエラー詳細を確認
2. 各ノードの設定を確認
3. 認証情報が正しく設定されているか確認

---

## 📝 次のステップ

設定が完了したら：

1. ✅ テスト実行で動作確認
2. ✅ 実際のWhopデータでテスト
3. ✅ 他のアクション（cancel_membership, reactivate_membership）をテスト
4. ✅ 本番環境での使用開始

---

## 🔗 関連ドキュメント

- [Whop制御ワークフロー SSOT](./whop-control-workflow-SSOT.md)
- [n8nワークフロー完全制御 SSOT](./n8n-workflow-full-control-SSOT.md)













