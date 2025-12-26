# Google Workspace Control ワークフロー セットアップガイド

**作成日**: 2025-12-26
**ワークフロー**: `google-workspace-control`
**ファイル**: `workflows/webhook-google-workspace-control.json`

---

## 📋 概要

このワークフローは、Webhook経由でGoogle Workspaceサービスを制御するための統合ワークフローです。

**対応サービス**:
- ✅ **Gmail** - メール送信
- ✅ **Google Sheets** - 読み取り、書き込み、更新
- ✅ **Google Drive** - ファイル一覧、アップロード、ダウンロード
- ✅ **Google Calendar** - イベント一覧、作成、更新、削除
- ✅ **Google Docs** - ドキュメント作成、更新、読み取り

**アカウント**: `admin@cryptotradeacademy.io`

---

## 🔐 認証情報の設定（重要）

### 必要な認証情報

n8n Dashboardで以下の認証情報を作成してください：

#### 1. Gmail OAuth2

1. n8n Dashboard → **Credentials** → **Add Credential**
2. 「**Gmail OAuth2 API**」を選択
3. 名前: `Gmail OAuth2 account for admin@cryptotradeacademy.io`
4. Google Cloud Consoleで取得したClient IDとClient Secretを入力
5. 認証を完了（`admin@cryptotradeacademy.io`でログイン）

#### 2. Google Sheets OAuth2

1. n8n Dashboard → **Credentials** → **Add Credential**
2. 「**Google Sheets OAuth2 API**」を選択
3. 名前: `Google Sheets OAuth2 account for admin@cryptotradeacademy.io`
4. 同じClient IDとClient Secretを使用
5. 認証を完了（`admin@cryptotradeacademy.io`でログイン）

#### 3. Google Drive OAuth2

1. n8n Dashboard → **Credentials** → **Add Credential**
2. 「**Google Drive OAuth2 API**」を選択
3. 名前: `Google Drive OAuth2 account for admin@cryptotradeacademy.io`
4. 同じClient IDとClient Secretを使用
5. 認証を完了（`admin@cryptotradeacademy.io`でログイン）

#### 4. Google Calendar OAuth2

1. n8n Dashboard → **Credentials** → **Add Credential**
2. 「**Google Calendar OAuth2 API**」を選択
3. 名前: `Google Calendar OAuth2 account for admin@cryptotradeacademy.io`
4. 同じClient IDとClient Secretを使用
5. 認証を完了（`admin@cryptotradeacademy.io`でログイン）

#### 5. Google Docs OAuth2

1. n8n Dashboard → **Credentials** → **Add Credential**
2. 「**Google Docs OAuth2 API**」を選択
3. 名前: `Google Docs OAuth2 account for admin@cryptotradeacademy.io`
4. 同じClient IDとClient Secretを使用
5. 認証を完了（`admin@cryptotradeacademy.io`でログイン）

**参考**: `docs/setup/GOOGLE_WORKSPACE_API_SETUP_COMPLETE.md` を参照

---

## 🚀 ワークフローのインポート

### 方法1: GitHub URLからインポート（推奨）

1. n8n Dashboard → **Workflows** → **Import Workflow from URL**
2. 以下のURLを入力：
   ```
   https://raw.githubusercontent.com/hadayalab-web/hadayalab-automation-platform/main/workflows/webhook-google-workspace-control.json
   ```
3. 「Import」ボタンをクリック

### 方法2: ファイルから直接インポート

1. n8n Dashboard → **Workflows** → **Import from File**
2. `workflows/webhook-google-workspace-control.json` を選択
3. インポート完了を確認

---

## ⚙️ インポート後の設定

### 1. 認証情報の設定

**重要**: インポート後、各ノードで認証情報を選択する必要があります。

1. ワークフローを開く
2. 各ノードをクリックして認証情報を選択：
   - **Gmail Send** → `Gmail OAuth2 account for admin@cryptotradeacademy.io`
   - **Sheets Read/Write/Update** → `Google Sheets OAuth2 account for admin@cryptotradeacademy.io`
   - **Drive List/Upload/Download** → `Google Drive OAuth2 account for admin@cryptotradeacademy.io`
   - **Calendar List/Create/Update/Delete** → `Google Calendar OAuth2 account for admin@cryptotradeacademy.io`
   - **Docs Create/Update/Read** → `Google Docs OAuth2 account for admin@cryptotradeacademy.io`

### 2. ワークフローの保存

1. すべてのノードで認証情報を設定したら、「**Save**」をクリック
2. エラーがないことを確認

### 3. ワークフローの公開

1. 「**Publish**」ボタンをクリック
2. バージョン名を入力（例: "Initial version"）
3. 「**Publish**」をクリック

### 4. MCP経由でのアクセス設定

1. ワークフロー設定を開く（右上の⚙️アイコン）
2. 「**Available in MCP**」を**有効化**
3. 「**Save**」をクリック

---

## 📡 API使用方法

### Webhookエンドポイント

**URL**: `https://hadayalab.app.n8n.cloud/webhook/google-workspace-control`
**Method**: `POST`
**Content-Type**: `application/json`

### アクション一覧

#### Gmail

**`gmail_send`** - メール送信

```json
{
  "action": "gmail_send",
  "to": "recipient@example.com",
  "subject": "Subject",
  "body": "Message body"
}
```

#### Google Sheets

**`sheets_read`** - スプレッドシート読み取り

```json
{
  "action": "sheets_read",
  "spreadsheetId": "YOUR_SPREADSHEET_ID",
  "sheetName": "Sheet1",
  "range": "A1:B10"
}
```

**`sheets_write`** - スプレッドシート書き込み

```json
{
  "action": "sheets_write",
  "spreadsheetId": "YOUR_SPREADSHEET_ID",
  "sheetName": "Sheet1",
  "columns": [
    { "column": "A", "value": "Value1" },
    { "column": "B", "value": "Value2" }
  ]
}
```

**`sheets_update`** - スプレッドシート更新

```json
{
  "action": "sheets_update",
  "spreadsheetId": "YOUR_SPREADSHEET_ID",
  "sheetName": "Sheet1",
  "columnToMatchOn": "A",
  "valueToMatchOn": "Value1",
  "columns": [
    { "column": "B", "value": "New Value" }
  ]
}
```

#### Google Drive

**`drive_list`** - ファイル一覧取得

```json
{
  "action": "drive_list",
  "query": "name contains 'example'",
  "pageSize": 100
}
```

**`drive_upload`** - ファイルアップロード

```json
{
  "action": "drive_upload",
  "fileName": "example.txt",
  "folderId": "YOUR_FOLDER_ID",
  "fileContent": "base64 encoded content"
}
```

**`drive_download`** - ファイルダウンロード

```json
{
  "action": "drive_download",
  "fileId": "YOUR_FILE_ID"
}
```

#### Google Calendar

**`calendar_list`** - イベント一覧取得

```json
{
  "action": "calendar_list",
  "calendarId": "primary",
  "timeMin": "2025-12-26T00:00:00Z",
  "timeMax": "2025-12-31T23:59:59Z"
}
```

**`calendar_create`** - イベント作成

```json
{
  "action": "calendar_create",
  "calendarId": "primary",
  "summary": "Meeting",
  "start": "2025-12-26T10:00:00Z",
  "end": "2025-12-26T11:00:00Z",
  "description": "Meeting description"
}
```

**`calendar_update`** - イベント更新

```json
{
  "action": "calendar_update",
  "calendarId": "primary",
  "eventId": "YOUR_EVENT_ID",
  "summary": "Updated Meeting",
  "start": "2025-12-26T11:00:00Z",
  "end": "2025-12-26T12:00:00Z"
}
```

**`calendar_delete`** - イベント削除

```json
{
  "action": "calendar_delete",
  "calendarId": "primary",
  "eventId": "YOUR_EVENT_ID"
}
```

#### Google Docs

**`docs_create`** - ドキュメント作成

```json
{
  "action": "docs_create",
  "title": "New Document"
}
```

**`docs_update`** - ドキュメント更新

```json
{
  "action": "docs_update",
  "documentId": "YOUR_DOCUMENT_ID",
  "content": "Document content"
}
```

**`docs_read`** - ドキュメント読み取り

```json
{
  "action": "docs_read",
  "documentId": "YOUR_DOCUMENT_ID"
}
```

---

## ✅ 動作確認

### テスト方法

1. **ワークフローを有効化**
   - ワークフローを開く
   - 「**Activate**」ボタンをクリック

2. **Webhook URLを確認**
   - Webhook Triggerノードを開く
   - Webhook URLをコピー

3. **テストリクエストを送信**
   ```bash
   curl -X POST https://hadayalab.app.n8n.cloud/webhook/google-workspace-control \
     -H "Content-Type: application/json" \
     -d '{
       "action": "gmail_send",
       "to": "test@example.com",
       "subject": "Test Email",
       "body": "This is a test email"
     }'
   ```

4. **実行履歴を確認**
   - ワークフローの「Executions」タブを開く
   - 実行結果を確認

---

## 🔍 トラブルシューティング

### エラー: "Cannot read properties of undefined (reading 'execute')"

**原因**: 認証情報が設定されていない

**解決方法**:
1. 各ノードで認証情報が選択されているか確認
2. 認証情報が正しく作成されているか確認
3. 認証情報の認証が完了しているか確認

### エラー: "Node is not currently installed"

**原因**: ノードがインストールされていない、または無効

**解決方法**:
1. n8n Dashboard → Settings → Community Nodes
2. 必要なノードがインストールされているか確認
3. 必要に応じてノードをインストール

### エラー: "Invalid credentials"

**原因**: 認証情報が無効または期限切れ

**解決方法**:
1. 認証情報を削除して再作成
2. 認証を再度実行
3. アクセス権限が正しく設定されているか確認

---

**最終更新**: 2025-12-26
**作成者**: HadayaLab

