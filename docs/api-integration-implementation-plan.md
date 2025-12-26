# 🔌 6API統合自動化インフラ実装計画

## 🚀 戦略的ビジョン

**「Cursor × n8n × 理論 = 無双システム」**

この実装計画は、以下の3つの統合要素による圧倒的な競争優位性を確立するためのものです：

1. **Cursor**: AI駆動開発による超高速実装
2. **n8n**: 自動化インフラによる超速PDCAサイクル
3. **6理論**: 科学的根拠に基づく最適化（Nudge, Influence, MECLABS, Scientific Advertising, Hooked, The Lean Startup）

**詳細**: `docs/strategic-vision-cursor-n8n-theory.md` を参照

---

## 📋 実装対象API

1. **Whop API** - 販売プラットフォーム統合
2. **HeyGen API** - AI Avatar VSL生成
3. **Google Workspace API** - Gmail, Google Sheets, Google Drive, Calendar, YouTube
4. **Adobe Creative Cloud API** - クリエイティブアセット生成
5. **Telegram Bot API** - メッセージ配信
6. **X (Twitter) API** - ソーシャルメディア統合

**実装期限**: 明日完了

**重要**: この実装計画は「自律実行型インフラ」に合わせて設計されています。
- 高レベルな指示から自動実行
- 意思決定が必要な時だけ人間に確認
- 詳細は `docs/autonomous-execution-infrastructure.md` を参照

**成果**: 6理論統合の発見は成果として大きい。各ツールをn8nで回せれば超速PDCAになる。Crypto×グローバルなので可能性が無限大。

---

## 🎯 実装優先順位

### Phase 1: コア統合（即実装）

```yaml
1. Whop API
   優先度: 最高
   理由: Trial Onboarding, Affiliate管理の基盤

2. Telegram Bot API
   優先度: 最高
   理由: Briefing配信のコア機能

3. Google Workspace API
   優先度: 高
   理由: Email自動化、データ管理の基盤
```

### Phase 2: クリエイティブ統合（同日実装）

```yaml
4. HeyGen API
   優先度: 高
   理由: VSL生成自動化

5. Adobe Creative Cloud API
   優先度: 中
   理由: クリエイティブアセット生成
```

### Phase 3: ソーシャル統合（同日実装）

```yaml
6. X (Twitter) API
   優先度: 中
   理由: ソーシャルメディア統合
```

---

## 1. Whop API統合

### 認証設定

```yaml
認証方法: API Key (Bearer Token)
取得方法:
  1. Whop Dashboard → Settings → API
  2. API Key生成
  3. n8n Credentials → HTTP Header Auth
     - Header Name: Authorization
     - Header Value: Bearer YOUR_WHOP_API_KEY

必要な権限:
  - memberships:read (会員情報取得)
  - memberships:write (会員情報更新)
  - affiliates:read (アフィリエイト情報取得)
  - affiliates:write (アフィリエイト情報更新)
  - products:read (商品情報取得)
```

### n8nノード実装

#### 1.1 Whop API - Membership取得

```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.3,
  "parameters": {
    "method": "GET",
    "url": "https://api.whop.com/api/v2/memberships/{{$json.membership_id}}",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "Authorization",
          "value": "Bearer {{$credentials.whopApiKey}}"
        }
      ]
    },
    "options": {}
  }
}
```

#### 1.2 Whop API - Affiliate Tier更新

```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.3,
  "parameters": {
    "method": "PATCH",
    "url": "https://api.whop.com/api/v2/affiliates/{{$json.affiliate_id}}/tier",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendBody": true,
    "contentType": "json",
    "bodyParameters": {
      "parameters": [
        {
          "name": "tier",
          "value": "={{$json.new_tier}}"
        },
        {
          "name": "commission",
          "value": "={{$json.new_commission}}"
        }
      ]
    },
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "Authorization",
          "value": "Bearer {{$credentials.whopApiKey}}"
        }
      ]
    }
  }
}
```

### 実装ワークフロー

```yaml
既存ワークフロー:
  - workflow-1-trial-onboarding.json (Whop Webhook受信)
  - n8n-workflows-design.md (Affiliate Auto-Management)

新規追加:
  - Whop Product情報取得ワークフロー
  - Whop Membership一覧取得ワークフロー
  - Whop Webhook設定ワークフロー
```

---

## 2. HeyGen API統合

### 認証設定

```yaml
認証方法: API Key
取得方法:
  1. HeyGen Dashboard → Settings → API
  2. API Key生成
  3. n8n Credentials → HTTP Header Auth
     - Header Name: X-API-KEY
     - Header Value: YOUR_HEYGEN_API_KEY

必要な権限:
  - video:create (VSL生成)
  - video:read (VSL情報取得)
  - avatar:read (Avatar情報取得)
```

### n8nノード実装

#### 2.1 HeyGen API - VSL生成

```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.3,
  "parameters": {
    "method": "POST",
    "url": "https://api.heygen.com/v1/video.generate",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "X-API-KEY",
          "value": "{{$credentials.heygenApiKey}}"
        },
        {
          "name": "Content-Type",
          "value": "application/json"
        }
      ]
    },
    "sendBody": true,
    "contentType": "json",
    "bodyParameters": {
      "parameters": [
        {
          "name": "avatar_id",
          "value": "={{$json.avatar_id}}"
        },
        {
          "name": "script",
          "value": "={{$json.script}}"
        },
        {
          "name": "background",
          "value": "={{$json.background}}"
        },
        {
          "name": "voice_id",
          "value": "={{$json.voice_id}}"
        }
      ]
    }
  }
}
```

#### 2.2 HeyGen API - VSL状態確認

```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.3,
  "parameters": {
    "method": "GET",
    "url": "https://api.heygen.com/v1/video.get?video_id={{$json.video_id}}",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "X-API-KEY",
          "value": "{{$credentials.heygenApiKey}}"
        }
      ]
    }
  }
}
```

### 実装ワークフロー

```yaml
新規ワークフロー:
  - workflow-heygen-vsl-generation.json
    目的: 市場別VSL自動生成
    トリガー: Manual / Schedule
    機能:
      - 市場別スクリプト読み込み
      - HeyGen APIでVSL生成
      - 生成完了待機（Polling）
      - Whop ProductにVSL URL埋め込み
```

---

## 3. Google Workspace API統合

### 認証設定

```yaml
認証方法: OAuth2
取得方法:
  1. Google Cloud Console → APIs & Services → Credentials
  2. OAuth 2.0 Client ID作成
  3. n8n Credentials → Google OAuth2 API
     - Client ID: YOUR_CLIENT_ID
     - Client Secret: YOUR_CLIENT_SECRET
     - Scope: （重要！以下を入力）
       - https://www.googleapis.com/auth/drive
       - https://www.googleapis.com/auth/calendar
       - https://www.googleapis.com/auth/gmail.send
       - https://www.googleapis.com/auth/gmail.readonly
       - https://www.googleapis.com/auth/spreadsheets
       - https://www.googleapis.com/auth/youtube.readonly

必要なAPI:
  - Google Drive API
  - Google Calendar API
  - Gmail API
  - Google Sheets API
  - YouTube Data API v3

詳細設定手順:
  - docs/google-workspace-oauth-setup.md を参照
```

**重要**: n8nの「Google account」設定画面で、**Scope**フィールドに上記のScopeを入力する必要があります。
スクリーンショットでScopeが空欄になっている場合は、必ず入力してください。

### n8nノード実装

#### 3.1 Gmail Node（既存実装確認）

```yaml
既存実装:
  - workflow-1-trial-onboarding.json
  - n8n-workflows-design.md

確認項目:
  - OAuth2認証設定
  - Email送信機能
  - HTML形式対応
```

#### 3.2 Google Sheets Node（既存実装確認）

```yaml
既存実装:
  - n8n-workflows-design.md (Affiliate Auto-Management)

確認項目:
  - OAuth2認証設定
  - 行の読み込み/更新
  - フィルタリング機能
```

#### 3.3 Google Drive Node（新規追加）

```json
{
  "type": "n8n-nodes-base.googleDrive",
  "typeVersion": 3.1,
  "parameters": {
    "operation": "upload",
    "name": "={{$json.file_name}}",
    "parents": {
      "values": ["={{$json.folder_id}}"]
    },
    "binaryData": true,
    "fileContent": "={{$binary.data}}",
    "options": {}
  }
}
```

### 実装ワークフロー

```yaml
既存ワークフロー:
  - workflow-1-trial-onboarding.json (Gmail)
  - n8n-workflows-design.md (Google Sheets)

新規追加:
  - workflow-google-drive-asset-upload.json
    目的: Adobe生成アセットをGoogle Driveに保存
    機能:
      - Adobe生成アセット取得
      - Google Driveにアップロード
      - 共有リンク生成
```

---

## 4. Adobe Creative Cloud API統合

### 認証設定

```yaml
認証方法: OAuth2
取得方法:
  1. Adobe Developer Console → Project作成
  2. OAuth2認証情報作成
  3. n8n Credentials → HTTP Header Auth
     - Header Name: Authorization
     - Header Value: Bearer YOUR_ADOBE_ACCESS_TOKEN

必要な権限:
  - asset_library:read
  - asset_library:write
  - creative_sdk:use

注意:
  - Adobe Creative Cloud APIは制限が多い
  - 代替案: Adobe Express API / Adobe Firefly API
  - または: ローカルAdobe Script実行 + n8n HTTP Request
```

### n8nノード実装

#### 4.1 Adobe Creative Cloud API - アセット生成（代替案）

```yaml
制約:
  - Adobe Creative Cloud APIは直接的な画像生成APIがない
  - Adobe Firefly API（AI生成）またはAdobe Express APIを使用

代替案1: Adobe Firefly API
  - 画像生成: POST /v1/images/generate
  - テキストから画像生成

代替案2: Adobe Express API
  - テンプレートベースの画像生成
  - バナー、サムネイル生成

代替案3: ローカルAdobe Script実行
  - Adobe Photoshop Script実行
  - n8n HTTP Requestでローカルサーバー経由
```

#### 4.2 Adobe Firefly API - 画像生成

```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.3,
  "parameters": {
    "method": "POST",
    "url": "https://firefly-api.adobe.io/v1/images/generate",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "Authorization",
          "value": "Bearer {{$credentials.adobeAccessToken}}"
        },
        {
          "name": "X-API-KEY",
          "value": "{{$credentials.adobeApiKey}}"
        }
      ]
    },
    "sendBody": true,
    "contentType": "json",
    "bodyParameters": {
      "parameters": [
        {
          "name": "prompt",
          "value": "={{$json.prompt}}"
        },
        {
          "name": "size",
          "value": "={{$json.size || '1024x1024'}}"
        }
      ]
    }
  }
}
```

### 実装ワークフロー

```yaml
新規ワークフロー:
  - workflow-adobe-asset-generation.json
    目的: 市場別クリエイティブアセット自動生成
    トリガー: Manual / Schedule
    機能:
      - 市場別テンプレート読み込み
      - Adobe Firefly APIで画像生成
      - Google Driveに保存
      - Whop ProductにアセットURL設定
```

---

## 5. Telegram Bot API統合

### 認証設定

```yaml
認証方法: Bot Token
取得方法:
  1. @BotFather でBot作成
  2. Bot Token取得
  3. n8n Credentials → Telegram
     - Bot Token: YOUR_TELEGRAM_BOT_TOKEN

必要なBot数:
  - 6市場分（EN/AR/KO/JA/ES/PT-BR）
  - 各市場1Bot推奨
```

### n8nノード実装

#### 5.1 Telegram Node（既存実装確認）

```yaml
既存実装:
  - n8n-workflows-design.md (Emergency Briefing Trigger)

確認項目:
  - Bot Token設定（6市場分）
  - メッセージ送信機能
  - チャットID設定
```

#### 5.2 Telegram Node - メッセージ送信

```json
{
  "type": "n8n-nodes-base.telegram",
  "typeVersion": 1.2,
  "parameters": {
    "resource": "message",
    "operation": "sendMessage",
    "chatId": "={{$json.chat_id}}",
    "text": "={{$json.message}}",
    "parseMode": "Markdown",
    "options": {}
  }
}
```

### 実装ワークフロー

```yaml
既存ワークフロー:
  - n8n-workflows-design.md (Emergency Briefing Trigger)

新規追加:
  - workflow-telegram-broadcast.json
    目的: 全市場一斉配信
    機能:
      - 6市場並列配信
      - Rate Limit対策（30秒間隔）
      - 配信結果ログ記録
```

---

## 6. X (Twitter) API統合

### 認証設定

```yaml
認証方法: OAuth 1.0a / OAuth 2.0
取得方法:
  1. Twitter Developer Portal → App作成
  2. API Key / API Secret取得
  3. Access Token / Access Token Secret取得
  4. n8n Credentials → Twitter OAuth1 API
     - Consumer Key: YOUR_API_KEY
     - Consumer Secret: YOUR_API_SECRET
     - Access Token: YOUR_ACCESS_TOKEN
     - Access Token Secret: YOUR_ACCESS_TOKEN_SECRET

必要な権限:
  - tweet:read
  - tweet:write
  - users:read

注意:
  - X API v2推奨
  - Rate Limit: 300 requests/15min (User Auth)
```

### n8nノード実装

#### 6.1 X API - ツイート投稿

```json
{
  "type": "n8n-nodes-base.twitter",
  "typeVersion": 2.1,
  "parameters": {
    "operation": "tweet",
    "text": "={{$json.tweet_text}}",
    "additionalFields": {
      "inReplyToStatusId": "={{$json.reply_to_id}}",
      "mediaIds": "={{$json.media_ids}}"
    }
  }
}
```

#### 6.2 X API - タイムライン取得

```json
{
  "type": "n8n-nodes-base.twitter",
  "typeVersion": 2.1,
  "parameters": {
    "operation": "search",
    "searchText": "={{$json.search_query}}",
    "additionalFields": {
      "resultType": "recent",
      "count": 100
    }
  }
}
```

### 実装ワークフロー

```yaml
新規ワークフロー:
  - workflow-x-social-sentiment.json
    目的: X上のセンチメント分析
    機能:
      - キーワード検索
      - センチメント分析
      - cryptosignal-aiにデータ送信

  - workflow-x-briefing-share.json
    目的: BriefingをXで共有
    機能:
      - Briefing内容をX形式に変換
      - 画像生成（Adobe Firefly）
      - Xに投稿
```

---

## 📊 統合ワークフロー一覧

### 既存ワークフロー（確認・更新）

```yaml
1. workflow-1-trial-onboarding.json
   - Whop Webhook受信
   - Gmail送信
   - ✅ 実装済み（確認・更新）

2. n8n-workflows-design.md
   - Emergency Briefing Trigger (Telegram)
   - Affiliate Auto-Management (Whop, Google Sheets)
   - ✅ 設計済み（実装確認）
```

### 新規ワークフロー（実装必要）

```yaml
3. workflow-heygen-vsl-generation.json
   - HeyGen API統合
   - 市場別VSL自動生成
   - Whop Product更新
   - 自律実行: 目標達成に必要な場合に自動実行

4. workflow-adobe-asset-generation.json
   - Adobe Firefly API統合
   - クリエイティブアセット生成
   - Google Drive保存
   - 自律実行: アセット更新が必要な場合に自動実行

5. workflow-google-drive-asset-upload.json
   - Google Drive API統合
   - アセットアップロード
   - 共有リンク生成
   - 自律実行: アセット生成後に自動実行

6. workflow-telegram-broadcast.json
   - Telegram Bot API統合
   - 全市場一斉配信
   - Rate Limit対策
   - 自律実行: Briefing配信時に自動実行

7. workflow-x-social-sentiment.json
   - X API統合
   - センチメント分析
   - cryptosignal-ai連携
   - 自律実行: 定期実行（日次/週次）

8. workflow-x-briefing-share.json
   - X API統合
   - Briefing共有
   - 画像生成連携
   - 自律実行: Briefing配信後に自動実行

9. workflow-goal-parser.json 【新規・自律実行型】
   - 高レベル指示の解析
   - 目標分解
   - ワークフロー選択
   - 意思決定ポイント検出

10. workflow-auto-executor.json 【新規・自律実行型】
    - ワークフロー自動実行
    - 進捗監視
    - 自動調整

11. workflow-decision-handler.json 【新規・自律実行型】
    - 意思決定ポイント検出
    - 人間への通知
    - 判断反映
```

---

## ✅ 実装チェックリスト

### 認証設定

- [ ] Whop API Key設定
- [ ] HeyGen API Key設定
- [ ] Google Workspace OAuth2設定（Gmail, Sheets, Drive）
- [ ] Adobe Creative Cloud API設定（Firefly API推奨）
- [ ] Telegram Bot Token設定（6市場分）
- [ ] X API認証設定（OAuth 1.0a / OAuth 2.0）

### ワークフロー実装

- [ ] workflow-1-trial-onboarding.json確認・更新
- [ ] workflow-heygen-vsl-generation.json実装
- [ ] workflow-adobe-asset-generation.json実装
- [ ] workflow-google-drive-asset-upload.json実装
- [ ] workflow-telegram-broadcast.json実装
- [ ] workflow-x-social-sentiment.json実装
- [ ] workflow-x-briefing-share.json実装
- [ ] workflow-goal-parser.json実装【自律実行型】
- [ ] workflow-auto-executor.json実装【自律実行型】
- [ ] workflow-decision-handler.json実装【自律実行型】

### テスト

- [ ] Whop API接続テスト
- [ ] HeyGen API接続テスト
- [ ] Google Workspace API接続テスト
- [ ] Adobe Firefly API接続テスト
- [ ] Telegram Bot API接続テスト
- [ ] X API接続テスト

### ドキュメント

- [ ] API認証設定ガイド作成
- [ ] ワークフロー実装ガイド作成
- [ ] トラブルシューティングガイド作成

---

## 🚀 実装手順

### Step 1: 認証設定（30分）

```yaml
1. n8n Dashboard → Credentials
2. 各APIの認証情報を設定
3. 接続テスト実行
```

### Step 2: 既存ワークフロー確認（30分）

```yaml
1. workflow-1-trial-onboarding.json確認
2. n8n-workflows-design.mdの実装状況確認
3. 必要な更新を実施
```

### Step 3: 新規ワークフロー実装（5時間）

```yaml
1. workflow-heygen-vsl-generation.json (1時間)
2. workflow-adobe-asset-generation.json (1時間)
3. workflow-google-drive-asset-upload.json (30分)
4. workflow-telegram-broadcast.json (30分)
5. workflow-x-social-sentiment.json (30分)
6. workflow-x-briefing-share.json (30分)
7. workflow-goal-parser.json (1時間) 【自律実行型】
8. workflow-auto-executor.json (30分) 【自律実行型】
9. workflow-decision-handler.json (30分) 【自律実行型】
```

### Step 4: テスト・デバッグ（1時間）

```yaml
1. 各ワークフローの実行テスト
2. エラーハンドリング確認
3. Rate Limit対策確認
```

### Step 5: ドキュメント作成（30分）

```yaml
1. API認証設定ガイド
2. ワークフロー実装ガイド
3. トラブルシューティングガイド
```

**合計時間**: 約8時間

**自律実行型機能追加**:
- Goal Parser Workflow: 高レベル指示から自動実行
- Auto Executor: ワークフロー自動実行・監視
- Decision Handler: 意思決定ポイント処理

---

## 📚 参考資料

### API公式ドキュメント

- [Whop API](https://docs.whop.com/api-reference)
- [HeyGen API](https://docs.heygen.com/api-reference)
- [Google Workspace API](https://developers.google.com/workspace)
- [Adobe Firefly API](https://developer.adobe.com/firefly-api/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [X API v2](https://developer.twitter.com/en/docs/twitter-api)

### n8n公式ドキュメント

- [HTTP Request Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)
- [Gmail Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.gmail/)
- [Google Sheets Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.googlesheets/)
- [Telegram Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.telegram/)
- [Twitter Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.twitter/)

---

**作成日**: 2025-12-25
**実装期限**: 明日完了
**ステータス**: 実装準備完了

