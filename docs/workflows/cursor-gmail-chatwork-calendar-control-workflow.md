# Cursor → Gmail/Chatwork/Calendar → Cursor ワークフロー

**作成日**: 2025-12-26
**目的**: CursorからGoogle Workspace（Gmail）とChatwork、Google Calendarを制御し、結果をCursorに返すためのWebhookワークフロー

**対象フォルダ**: Personal（プロジェクトID: `fPT5foO8DCTDBr0k`）

---

## 📋 概要

このワークフローは、Cursorから実行できるGoogle Workspace（Gmail）、Chatwork、Google Calendarの操作を提供します。Webhook経由でリクエストを受け取り、結果をJSON形式で返します。

**ワークフローID**: `RQpJoa8rd2ROZaP2`  
**Webhook URL**: `https://hadayalab.app.n8n.cloud/webhook/cursor-gmail-chatwork-calendar-control`

---

## 🚀 サポートするアクション

### Gmail

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

### Chatwork

#### `chatwork_send_message` - Chatworkメッセージ送信

**リクエスト例**:
```json
{
  "action": "chatwork_send_message",
  "roomId": "123456789",
  "message": "Hello from Cursor!"
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

### Google Calendar

#### `calendar_list` - カレンダーイベント一覧取得

**リクエスト例**:
```json
{
  "action": "calendar_list",
  "calendarId": "primary",
  "timeMin": "2025-12-26T00:00:00Z",
  "timeMax": "2025-12-31T23:59:59Z",
  "maxResults": 50
}
```

**パラメータ**:
- `calendarId` (オプション): カレンダーID（デフォルト: `primary`）
- `timeMin` (オプション): 開始時刻（ISO 8601形式）
- `timeMax` (オプション): 終了時刻（ISO 8601形式）
- `maxResults` (オプション): 最大取得件数（デフォルト: 250）
- `query` (オプション): 検索クエリ

#### `calendar_create` - カレンダーイベント作成

**リクエスト例**:
```json
{
  "action": "calendar_create",
  "calendarId": "primary",
  "summary": "Meeting",
  "description": "Meeting description",
  "location": "Tokyo",
  "start": "2025-12-27T10:00:00Z",
  "end": "2025-12-27T11:00:00Z",
  "attendees": ["attendee1@example.com", "attendee2@example.com"],
  "sendUpdates": "all"
}
```

**パラメータ**:
- `calendarId` (オプション): カレンダーID（デフォルト: `primary`）
- `summary` (必須): イベントのタイトル
- `description` (オプション): イベントの説明
- `location` (オプション): 場所
- `start` (必須): 開始時刻（ISO 8601形式）
- `end` (必須): 終了時刻（ISO 8601形式）
- `attendees` (オプション): 参加者のメールアドレス配列
- `sendUpdates` (オプション): 更新通知の送信方法（`none`, `all`, `externalOnly`）

#### `calendar_update` - カレンダーイベント更新

**リクエスト例**:
```json
{
  "action": "calendar_update",
  "calendarId": "primary",
  "eventId": "event-id-here",
  "summary": "Updated Meeting",
  "start": "2025-12-27T11:00:00Z",
  "end": "2025-12-27T12:00:00Z"
}
```

**パラメータ**:
- `calendarId` (オプション): カレンダーID（デフォルト: `primary`）
- `eventId` (必須): 更新するイベントのID
- `summary` (オプション): イベントのタイトル
- `description` (オプション): イベントの説明
- `location` (オプション): 場所
- `start` (オプション): 開始時刻（ISO 8601形式）
- `end` (オプション): 終了時刻（ISO 8601形式）
- `attendees` (オプション): 参加者のメールアドレス配列
- `sendUpdates` (オプション): 更新通知の送信方法

#### `calendar_delete` - カレンダーイベント削除

**リクエスト例**:
```json
{
  "action": "calendar_delete",
  "calendarId": "primary",
  "eventId": "event-id-here",
  "sendUpdates": "all"
}
```

**パラメータ**:
- `calendarId` (オプション): カレンダーID（デフォルト: `primary`）
- `eventId` (必須): 削除するイベントのID
- `sendUpdates` (オプション): 更新通知の送信方法

---

## 📡 Webhook URL

ワークフローを有効化後、以下のURLでアクセスできます:

```
https://hadayalab.app.n8n.cloud/webhook/cursor-gmail-chatwork-calendar-control
```

---

## 📝 レスポンス形式

### 成功レスポンス

```json
{
  "success": true,
  "action": "gmail_send",
  "data": {
    // アクション固有のデータ
  },
  "timestamp": "2025-12-26T23:00:00.000Z"
}
```

### エラーレスポンス

```json
{
  "success": false,
  "action": "gmail_send",
  "error": "Error message here",
  "timestamp": "2025-12-26T23:00:00.000Z"
}
```

---

## 🔐 認証情報の設定

### Google Workspace

1. n8n Dashboard → Credentials → Add Credential
2. Gmail OAuth2 API / Google Calendar OAuth2 API を選択
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

## 🚀 使用方法（Cursorから実行）

### n8n-MCPを使用した実行

```bash
@n8n-cloud cursor-gmail-chatwork-calendar-controlワークフローを実行して、action=gmail_send, to=test@example.com, subject=Test, message=Helloで
```

### HTTP Requestでの実行（Python例）

```python
import requests

url = "https://hadayalab.app.n8n.cloud/webhook/cursor-gmail-chatwork-calendar-control"
payload = {
    "action": "gmail_send",
    "to": "recipient@example.com",
    "subject": "Test Subject",
    "message": "Test message"
}

response = requests.post(url, json=payload)
print(response.json())
```

---

## 📋 次のステップ（人間の役割）

1. **Personalフォルダに移動**
   - n8n Dashboard: https://hadayalab.app.n8n.cloud/workflow/RQpJoa8rd2ROZaP2
   - ワークフローをPersonalフォルダ（プロジェクトID: `fPT5foO8DCTDBr0k`）にドラッグ&ドロップ

2. **認証情報の設定**
   - Gmail OAuth2認証情報を設定
   - Google Calendar OAuth2認証情報を設定

3. **ワークフローの有効化**
   - 「Activate」ボタンをクリック
   - 「Available in MCP」を有効化（MCP経由でアクセスする場合）

---

**最終更新**: 2025-12-26

