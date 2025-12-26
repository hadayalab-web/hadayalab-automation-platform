# Google Workspace / Chatwork Control ワークフロー

**作成日**: 2025-12-26
**目的**: CursorからGoogle Workspace（Gmail、Sheets）とChatworkを制御するためのWebhookワークフロー

---

## 📋 概要

このワークフローは、Webhook経由でGoogle Workspace（Gmail、Google Sheets）とChatworkの操作を実行するための統合インターフェースを提供します。

**対象フォルダ**: Personal（プロジェクトID: `fPT5foO8DCTDBr0k`）

---

## 🚀 サポートするアクション

### Google Workspace

#### `gmail_send` - Gmail送信

**リクエスト例**:
```json
{
  "action": "gmail_send",
  "to": "recipient@example.com",
  "subject": "Test Subject",
  "message": "Test message body",
  "replyTo": "optional@example.com"
}
```

**パラメータ**:
- `to` (必須): 送信先メールアドレス
- `subject` (必須): メール件名
- `message` (必須): メール本文
- `replyTo` (オプション): 返信先メールアドレス

#### `sheets_read` - Google Sheets読み取り

**リクエスト例**:
```json
{
  "action": "sheets_read",
  "spreadsheetId": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
  "sheetName": "Sheet1",
  "range": "A1:C10"
}
```

**パラメータ**:
- `spreadsheetId` (必須): Google SheetsのスプレッドシートID
- `sheetName` (必須): シート名
- `range` (必須): 読み取る範囲（例: "A1:C10"）

### Chatwork

#### `chatwork_send_message` - Chatworkメッセージ送信

**リクエスト例**:
```json
{
  "action": "chatwork_send_message",
  "roomId": "123456789",
  "message": "Hello from n8n!"
}
```

**パラメータ**:
- `roomId` (必須): ChatworkルームID
- `message` (必須): 送信するメッセージ本文

#### `chatwork_create_task` - Chatworkタスク作成

**リクエスト例**:
```json
{
  "action": "chatwork_create_task",
  "roomId": "123456789",
  "taskBody": "Task description",
  "toIds": "123456789,987654321",
  "limit": "2025-12-31T23:59:59Z"
}
```

**パラメータ**:
- `roomId` (必須): ChatworkルームID
- `taskBody` (必須): タスクの説明
- `toIds` (必須): 担当者IDのカンマ区切り（例: "123456789,987654321"）
- `limit` (必須): 期限（ISO 8601形式）

---

## 🔐 認証情報の設定

### Google Workspace

1. n8n Dashboard → Credentials → Add Credential
2. Gmail OAuth2 API / Google Sheets OAuth2 API を選択
3. `admin@cryptotradeacademy.io` の認証情報を設定

### Chatwork

Chatwork API Tokenは環境変数 `CHATWORK_API_TOKEN` として設定されています。

**n8n Cloud環境変数に設定**:
- `CHATWORK_API_TOKEN`: `e973fd7311ae06d1deb377bd1ecb7d8e`

**設定手順**:
1. n8n Dashboard → Settings → Environment Variables
2. `CHATWORK_API_TOKEN` を追加
3. 値: `e973fd7311ae06d1deb377bd1ecb7d8e`

---

## 📡 Webhook URL

ワークフローを有効化後、以下のURLでアクセスできます:

```
https://hadayalab.app.n8n.cloud/webhook/google-workspace-chatwork-control
```

---

## 📝 使用例

### cURL例

#### Gmail送信
```bash
curl -X POST https://hadayalab.app.n8n.cloud/webhook/google-workspace-chatwork-control \
  -H "Content-Type: application/json" \
  -d '{
    "action": "gmail_send",
    "to": "recipient@example.com",
    "subject": "Test Subject",
    "message": "Test message body"
  }'
```

#### Chatworkメッセージ送信
```bash
curl -X POST https://hadayalab.app.n8n.cloud/webhook/google-workspace-chatwork-control \
  -H "Content-Type: application/json" \
  -d '{
    "action": "chatwork_send_message",
    "roomId": "123456789",
    "message": "Hello from n8n!"
  }'
```

#### Chatworkタスク作成
```bash
curl -X POST https://hadayalab.app.n8n.cloud/webhook/google-workspace-chatwork-control \
  -H "Content-Type: application/json" \
  -d '{
    "action": "chatwork_create_task",
    "roomId": "123456789",
    "taskBody": "Task description",
    "toIds": "123456789",
    "limit": "2025-12-31T23:59:59Z"
  }'
```

---

## 🔄 レスポンス形式

### 成功時

```json
{
  "success": true,
  "data": {
    // 各アクションのレスポンスデータ
  }
}
```

### エラー時

```json
{
  "success": false,
  "error": "Error message"
}
```

---

## ⚠️ 注意事項

1. **環境変数の設定**: Chatwork API Tokenはn8n Cloud環境変数 `CHATWORK_API_TOKEN` として設定されている必要があります
2. **Google Workspace認証**: 各Google Workspaceノードの認証情報を設定する必要があります
3. **Chatwork Room ID**: ルームIDはChatworkのURLから取得できます（例: `https://www.chatwork.com/#!rid123456789` → Room ID: `123456789`）
4. **Personalフォルダ**: このワークフローはPersonalフォルダ（プロジェクトID: `fPT5foO8DCTDBr0k`）に配置されています

---

## 📚 関連ドキュメント

- [Google Workspace Control ワークフロー](./google-workspace-control-workflow.md) - Google Workspace専用ワークフロー
- [n8n完全SSOT](../SSOT/n8n-complete-SSOT.md) - n8n関連のすべての情報

---

**最終更新**: 2025-12-26
**作成者**: HadayaLab

