# Cursor → Gmail/Chatwork/Calendar → Cursor ワークフローデバッグレポート

**作成日**: 2025-12-26
**問題**: ワークフローのパブリッシュ不可、「Available in MCP」が有効化できない

---

## 🔍 問題の特定

### 発見された問題

1. **Chatwork Create Taskノードの認証設定**
   - 問題: `genericCredentialType` と `genericAuthType` を使用していた
   - 修正: `headerAuth` に統一し、環境変数 `CHATWORK_API_TOKEN` を使用するように変更

2. **HTTP Requestノードの`webhookId`フィールド**
   - 問題: HTTP Requestノードに不要な `webhookId` フィールドが含まれていた
   - 修正: `webhookId: ""` を追加（空文字列で明示的に設定）

3. **認証情報の`type`フィールド**
   - 問題: `credentials` に `type` フィールドが含まれていた可能性
   - 修正: `type` フィールドを削除（`name` のみを保持）

---

## ✅ 修正内容

### 修正1: Chatwork Create Taskノードの認証設定

**変更前**:
```json
{
  "parameters": {
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    ...
    "headerParameters": {
      "parameters": [
        {
          "name": "X-ChatWorkToken",
          "value": "=e973fd7311ae06d1deb377bd1ecb7d8e"
        }
      ]
    }
  }
}
```

**変更後**:
```json
{
  "parameters": {
    "authentication": "headerAuth",
    ...
    "headerParameters": {
      "parameters": [
        {
          "name": "X-ChatWorkToken",
          "value": "={{ $env.CHATWORK_API_TOKEN }}"
        }
      ]
    }
  },
  "webhookId": ""
}
```

### 修正2: 認証情報の`type`フィールド削除

**変更前**:
```json
{
  "credentials": {
    "gmailOAuth2": {
      "name": "Gmail OAuth2 account for admin@cryptotradeacademy.io",
      "type": "gmailOAuth2"
    }
  }
}
```

**変更後**:
```json
{
  "credentials": {
    "gmailOAuth2": {
      "name": "Gmail OAuth2 account for admin@cryptotradeacademy.io"
    }
  }
}
```

---

## 🧪 テスト結果

### ワークフローインポート

- ✅ ワークフローが正常にインポートされた
- ✅ ワークフローID: `IIjHbK68YmVYhlj8`
- ✅ URL: https://hadayalab.app.n8n.cloud/workflow/IIjHbK68YmVYhlj8

### 次のステップ（人間の役割）

1. **Personalフォルダに移動**
   - n8n Dashboardでワークフローを開く
   - Personalフォルダ（プロジェクトID: `fPT5foO8DCTDBr0k`）にドラッグ&ドロップ

2. **各ノードの確認**
   - すべてのノードが正しく表示されているか確認
   - エラーアイコンがないか確認

3. **認証情報の設定**
   - Gmail OAuth2認証情報を設定
   - Google Calendar OAuth2認証情報を設定

4. **パブリッシュとMCP有効化**
   - 「Publish」ボタンが利用可能か確認
   - 「Available in MCP」が有効化できるか確認

---

## 🔄 トラブルシューティング

### パブリッシュができない場合

1. **ノードのエラー確認**
   - 各ノードを開いて、エラーメッセージを確認
   - 特に認証情報が必要なノード（Gmail、Google Calendar）を確認

2. **接続の確認**
   - すべてのノードが正しく接続されているか確認
   - Switch Actionからすべての出力が接続されているか確認

3. **必須パラメータの確認**
   - 各ノードの必須パラメータが設定されているか確認

### 「Available in MCP」が有効化できない場合

1. **ワークフローの公開状態確認**
   - ワークフローが公開（Published）されている必要があります

2. **n8n Cloudの有料プラン確認**
   - MCP機能は有料プランで利用可能です

---

**最終更新**: 2025-12-26

