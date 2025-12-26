# 🔐 Google Workspace API OAuth設定ガイド

## 📋 概要

このドキュメントは、n8nでGoogle Workspace API（Drive, Calendar, Gmail, Sheets, YouTube Data API v3）を連携するためのOAuth設定手順を説明します。

---

## 🎯 必要なAPIとScope

### 実装対象API

```yaml
1. Google Drive API
   - ファイルアップロード/ダウンロード
   - フォルダ管理
   - 共有リンク生成

2. Google Calendar API
   - カレンダーイベント作成/更新
   - カレンダー一覧取得

3. Gmail API
   - メール送信
   - メール受信
   - ラベル管理

4. Google Sheets API
   - スプレッドシート読み込み/更新
   - 行の追加/削除

5. YouTube Data API v3
   - 動画情報取得
   - チャンネル情報取得
```

---

## 📝 n8n認証設定手順

### Step 1: Scope設定（最重要）

n8nの「Google account」設定画面で、**Scope**フィールドに以下を入力：

```
https://www.googleapis.com/auth/drive
https://www.googleapis.com/auth/calendar
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/spreadsheets
https://www.googleapis.com/auth/youtube.readonly
```

**入力方法**:
1. n8nの「Google account」設定画面を開く
2. 「Connection」タブを選択
3. **Scope**フィールドに上記のScopeを1行ずつ入力（改行区切り）
   - または、カンマ区切りでも可: `https://www.googleapis.com/auth/drive, https://www.googleapis.com/auth/calendar, ...`

### Step 2: 設定内容確認

スクリーンショットから確認できる設定：

```yaml
OAuth Redirect URL:
  https://oauth.n8n.cloud/oauth2/callback
  → Google Cloud Console側でもこのURLを設定済み

Client ID:
  135718974606-htnvh8mlcfmofnh8reqk81b734j6fk8b.apps.googleusercontent.com
  → 既に入力済み

Client Secret:
  ..................（マスク表示）
  → 既に入力済み

Scope:
  （空欄）← ここに上記のScopeを入力する必要がある
```

### Step 3: Google Cloud Console側の設定確認

#### OAuth同意画面の設定

スクリーンショット1から確認できる設定：

```yaml
アプリ名: n8n
ユーザーサポートメール: admin@cryptotradeacademy.io
デベロッパーの連絡先情報: hadayalab@gmail.com

必要な追加設定:
  - アプリケーションのホームページ: （設定推奨）
  - プライバシーポリシーリンク: （設定推奨）
  - 利用規約リンク: （設定推奨）
```

#### OAuth 2.0 クライアントIDの設定（重要！）

**エラー**: `redirect_uri_mismatch`が発生している場合、以下を確認・設定してください。

**Google Cloud Console側の設定手順**:

1. **Google Cloud Consoleにアクセス**
   - https://console.cloud.google.com/
   - プロジェクトを選択（n8n用のプロジェクト）

2. **APIs & Services → Credentials に移動**
   - 左メニューから「APIs & Services」→「Credentials」を選択

3. **OAuth 2.0 クライアントIDを編集**
   - 既存のOAuth 2.0 クライアントIDをクリック
   - または、新規作成する場合は「+ CREATE CREDENTIALS」→「OAuth client ID」

4. **承認済みのリダイレクトURIを追加**
   - 「承認済みのリダイレクト URI」セクションを探す
   - 「+ URI を追加」をクリック
   - 以下を入力：
     ```
     https://oauth.n8n.cloud/oauth2/callback
     ```
   - 「保存」をクリック

5. **設定確認**
   ```yaml
   承認済みのリダイレクト URI:
     https://oauth.n8n.cloud/oauth2/callback
     → このURLが設定されていることを確認
   ```

**注意**:
- リダイレクトURIは完全一致する必要があります（末尾のスラッシュも含めて）
- 複数のリダイレクトURIを設定する場合は、1行ずつ追加してください

---

## 🔧 各APIの詳細Scope

### Google Drive API

```yaml
基本Scope:
  https://www.googleapis.com/auth/drive
  → ファイルの読み書き、削除、共有

読み取り専用:
  https://www.googleapis.com/auth/drive.readonly
  → ファイルの読み取りのみ

メタデータのみ:
  https://www.googleapis.com/auth/drive.metadata.readonly
  → ファイル情報の読み取りのみ
```

### Google Calendar API

```yaml
基本Scope:
  https://www.googleapis.com/auth/calendar
  → カレンダーの読み書き、イベント管理

読み取り専用:
  https://www.googleapis.com/auth/calendar.readonly
  → カレンダーの読み取りのみ
```

### Gmail API

```yaml
送信のみ:
  https://www.googleapis.com/auth/gmail.send
  → メール送信のみ（n8nワークフローで使用）

読み取り専用:
  https://www.googleapis.com/auth/gmail.readonly
  → メールの読み取りのみ

完全アクセス:
  https://www.googleapis.com/auth/gmail
  → メールの送受信、ラベル管理、削除など全操作
```

### Google Sheets API

```yaml
基本Scope:
  https://www.googleapis.com/auth/spreadsheets
  → スプレッドシートの読み書き

読み取り専用:
  https://www.googleapis.com/auth/spreadsheets.readonly
  → スプレッドシートの読み取りのみ
```

### YouTube Data API v3

```yaml
読み取り専用:
  https://www.googleapis.com/auth/youtube.readonly
  → 動画情報、チャンネル情報の読み取り

完全アクセス:
  https://www.googleapis.com/auth/youtube
  → 動画のアップロード、チャンネル管理など全操作
```

---

## 📋 推奨Scope設定（最小権限の原則）

### 最小権限での設定

```yaml
推奨Scope（最小権限）:
  https://www.googleapis.com/auth/drive
  https://www.googleapis.com/auth/calendar
  https://www.googleapis.com/auth/gmail.send
  https://www.googleapis.com/auth/gmail.readonly
  https://www.googleapis.com/auth/spreadsheets
  https://www.googleapis.com/auth/youtube.readonly
```

### 完全アクセスが必要な場合

```yaml
完全アクセスScope（必要に応じて）:
  https://www.googleapis.com/auth/drive
  https://www.googleapis.com/auth/calendar
  https://www.googleapis.com/auth/gmail
  https://www.googleapis.com/auth/spreadsheets
  https://www.googleapis.com/auth/youtube
```

---

## 🚀 設定手順（詳細）

### Step 1: n8nでのScope設定

1. n8n Dashboard → Credentials → Google account を開く
2. 「Connection」タブを選択
3. **Scope**フィールドに以下を入力：

```
https://www.googleapis.com/auth/drive
https://www.googleapis.com/auth/calendar
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/spreadsheets
https://www.googleapis.com/auth/youtube.readonly
```

4. 「保存」をクリック

### Step 2: Google認証の実行

1. 「Sign in with Google」ボタンをクリック
2. Googleアカウントでログイン
3. 許可画面で「許可」をクリック
   - 各APIへのアクセス許可が表示される
   - すべてのScopeが承認される

### Step 3: 接続テスト

各APIノードで接続テストを実行：

```yaml
Google Drive Node:
  - Operation: List Files
  - フォルダ一覧が取得できればOK

Google Calendar Node:
  - Operation: Get All Calendars
  - カレンダー一覧が取得できればOK

Gmail Node:
  - Operation: Send Message
  - テストメール送信ができればOK

Google Sheets Node:
  - Operation: Read Rows
  - スプレッドシートが読み込めればOK

YouTube Node:
  - Operation: Get Video
  - 動画情報が取得できればOK
```

---

## ⚠️ よくある問題と解決方法

### 問題1: Scopeが空欄のまま

**症状**: Scopeフィールドが空欄で、認証が失敗する

**解決方法**:
1. Scopeフィールドに必要なScopeを入力
2. 改行区切りまたはカンマ区切りで入力
3. 保存後に「Sign in with Google」を再度実行

### 問題2: `redirect_uri_mismatch`エラー（最重要）

**症状**: Google認証時に「エラー 400: redirect_uri_mismatch」が表示される

**原因**: Google Cloud Console側で承認済みのリダイレクトURIが設定されていない、または不一致

**解決方法**:
1. **Google Cloud Console → APIs & Services → Credentials に移動**
2. **OAuth 2.0 クライアントIDを編集**
3. **「承認済みのリダイレクト URI」セクションを確認**
4. **以下を追加**:
   ```
   https://oauth.n8n.cloud/oauth2/callback
   ```
5. **「保存」をクリック**
6. **n8n側で再度「Sign in with Google」を実行**

**確認ポイント**:
- リダイレクトURIは完全一致する必要があります
- 末尾のスラッシュ（/）も含めて正確に入力
- 大文字小文字も区別されます

### 問題3: 「アクセスが拒否されました」エラー

**症状**: Google認証時に「アクセスが拒否されました」と表示される

**解決方法**:
1. Google Cloud ConsoleでOAuth同意画面の設定を確認
2. 承認済みのリダイレクトURIが正しく設定されているか確認
3. アプリの公開ステータスを確認（内部使用の場合は「テスト中」でOK）

### 問題3: 特定のAPIが動作しない

**症状**: 一部のAPIノードが動作しない

**解決方法**:
1. Scopeに該当APIのScopeが含まれているか確認
2. Google Cloud Consoleで該当APIが有効化されているか確認
   - APIs & Services → Enabled APIs
   - 必要なAPIを有効化

### 問題4: 「このアプリは確認されていません」警告

**症状**: Google認証時に警告が表示される

**解決方法**:
1. 「詳細」をクリック
2. 「[アプリ名]（安全ではないページ）に移動」をクリック
3. これは開発中は正常な動作
4. 本番環境ではGoogleのアプリ検証が必要

---

## 📚 参考資料

### Google公式ドキュメント

- [Google OAuth 2.0 Scopes](https://developers.google.com/identity/protocols/oauth2/scopes)
- [Google Drive API Scopes](https://developers.google.com/drive/api/guides/api-specific-auth)
- [Google Calendar API Scopes](https://developers.google.com/calendar/api/guides/auth)
- [Gmail API Scopes](https://developers.google.com/gmail/api/auth/scopes)
- [Google Sheets API Scopes](https://developers.google.com/sheets/api/guides/authorizing)
- [YouTube Data API v3 Scopes](https://developers.google.com/youtube/v3/guides/auth)

### n8n公式ドキュメント

- [Google OAuth2 API Node](https://docs.n8n.io/integrations/builtin/credentials/google/oauth2-api/)
- [Google Drive Node](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googledrive/)
- [Google Calendar Node](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googlecalendar/)
- [Gmail Node](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/)
- [Google Sheets Node](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googlesheets/)

---

## ✅ 設定チェックリスト

### Google Cloud Console側

- [ ] OAuth同意画面の設定完了
  - [ ] アプリ名: n8n
  - [ ] ユーザーサポートメール設定
  - [ ] デベロッパー連絡先情報設定
- [ ] OAuth 2.0 クライアントID作成
  - [ ] Client ID取得
  - [ ] Client Secret取得
  - [ ] 承認済みのリダイレクトURI設定: `https://oauth.n8n.cloud/oauth2/callback`
- [ ] 必要なAPIを有効化
  - [ ] Google Drive API
  - [ ] Google Calendar API
  - [ ] Gmail API
  - [ ] Google Sheets API
  - [ ] YouTube Data API v3

### n8n側

- [ ] Google OAuth2 API認証情報作成
  - [ ] Client ID入力
  - [ ] Client Secret入力
  - [ ] **Scope入力（最重要）**
- [ ] Google認証実行
  - [ ] 「Sign in with Google」クリック
  - [ ] 許可画面で「許可」クリック
- [ ] 接続テスト
  - [ ] Google Drive Nodeテスト
  - [ ] Google Calendar Nodeテスト
  - [ ] Gmail Nodeテスト
  - [ ] Google Sheets Nodeテスト
  - [ ] YouTube Nodeテスト

---

**作成日**: 2025-12-25
**バージョン**: 1.0
**ステータス**: 設定ガイド完了

