# CryptoTrade Academy - n8nワークフロー設計ドキュメント

## 概要

このドキュメントは、3つの戦略ドキュメントに基づいてn8nで実装するワークフローの設計をまとめています。

**⭐ 親戦略ドキュメント（最新）:**
- **[n8n + Whop 完全活用戦略 SSOT](./docs/n8n-whop-full-strategy-SSOT.md)** - n8n + Whop完全統合戦略（**最初に参照**）

**参照ドキュメント:**
- CryptoTrade Academy - Creative Execution Master Guide v1.0
- CryptoTrade Academy - Sales Strategy Doping v2.0 FINAL
- CryptoTrade Academy - Zero-Budget Affiliate DRM Strategy v1.1 + APDS v1.0

**Make.comからの置き換え:**
- Make.comの記述はすべてn8nに置き換え
- 同等の機能をn8nノードで実装

---

## ワークフロー1: Trial Onboarding Automation

### 目的
1-Day Free Trialの完全自動化（Nudge Feedback Loop実装）

### トリガー
- **Webhook Trigger** (n8n-nodes-base.webhook)
  - Path: `whop-trial-started`
  - Method: POST
  - 受信データ: `user_email`, `user_name`, `market`, `trial_start_time`, `membership_id`

### ワークフロー構造

```
1. Webhook Trigger (Whop Trial Started)
   ↓
2. Switch Node (Market Router) - 6市場分岐
   - EN, AR, KO, JA, ES, PT-BR
   ↓
3. Gmail Node (Welcome Email) - 即座送信
   - Subject: "Welcome to CryptoTrade Academy 🎓"
   - Body: HTML形式（Telegram Link含む）
   ↓
4. Wait Node (6時間待機)
   - Resume: After Time Interval
   - Amount: 6
   - Unit: hours
   ↓
5. Gmail Node (Value Email) - 6時間後送信
   - Subject: "Your first briefing is live 🛡️"
   - Body: HTML形式（価値体験メッセージ）
   ↓
6. Wait Node (12時間待機)
   - Resume: After Time Interval
   - Amount: 12
   - Unit: hours
   ↓
7. Gmail Node (Trial End Notification) - 18時間後送信
   - Subject: "Your trial ends in 6 hours"
   - Body: HTML形式（Loss Aversion + CTA）
   ↓
8. HTTP Request Node (Whop API - Payment Status確認)
   - Method: GET
   - URL: `https://api.whop.com/api/v2/memberships/{{membership_id}}`
   - Headers: Authorization Bearer Token
   ↓
9. Switch Node (Payment Status Router)
   - Branch 1: status = "active" → Thank You Email
   - Branch 2: status = "cancelled" → Feedback Request Email
   ↓
10a. Gmail Node (Thank You Email - Paid)
    - Subject: "You're now protected 🛡️"

10b. Gmail Node (Feedback Request - Cancelled)
    - Subject: "We're sorry to see you go"
```

### 実装ノード詳細

#### 1. Webhook Trigger
```json
{
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 2.1,
  "parameters": {
    "httpMethod": "POST",
    "path": "whop-trial-started",
    "responseMode": "onReceived"
  }
}
```

#### 2. Market Router (Switch)
```json
{
  "type": "n8n-nodes-base.switch",
  "typeVersion": 3.1,
  "parameters": {
    "mode": "rules",
    "rules": {
      "values": [
        {
          "conditions": {
            "conditions": [
              {
                "leftValue": "={{ $json.body.market || $json.body.data?.market }}",
                "rightValue": "EN",
                "operator": {
                  "type": "string",
                  "operation": "equals"
                }
              }
            ]
          },
          "renameOutput": true,
          "outputKey": "EN"
        }
        // AR, KO, JA, ES, PT-BR も同様に追加
      ]
    }
  }
}
```

#### 3. Welcome Email (Gmail)
```json
{
  "type": "n8n-nodes-base.gmail",
  "typeVersion": 2.2,
  "parameters": {
    "resource": "message",
    "operation": "send",
    "sendTo": "={{ $json.body.user_email || $json.body.data?.user_email }}",
    "subject": "Welcome to CryptoTrade Academy 🎓",
    "emailType": "html",
    "message": "<p>Hi {{ $json.body.user_name || $json.body.data?.user_name }},</p><p>Your 1-Day Free Trial just started.</p><p>Your first briefing arrives in 6 hours. Join Telegram now:<br>[Telegram Link]</p><p>What to expect:<br>- 2-6 briefings today<br>- 60-second reads<br>- BUG STANDBY alerts</p><p>Cancel anytime in Dashboard → Settings.</p><p>See you in 6 hours.<br>CryptoTrade Academy</p>"
  }
}
```

#### 4. Wait Node (6 Hours)
```json
{
  "type": "n8n-nodes-base.wait",
  "typeVersion": 1.1,
  "parameters": {
    "resume": "timeInterval",
    "amount": 6,
    "unit": "hours"
  }
}
```

### 市場別Email Template

各市場（EN/AR/KO/JA/ES/PT-BR）用に、Switch Nodeの各ブランチに専用のGmail Nodeを配置。

**EN市場例:**
- Welcome Email: 英語版
- Value Email: 英語版
- Trial End: 英語版

**AR市場例:**
- Welcome Email: アラビア語版（右から左）
- Value Email: アラビア語版
- Trial End: アラビア語版

### 必要な認証情報
- Gmail OAuth2認証
- Whop API Key（HTTP Request用）

---

## ワークフロー2: Affiliate Auto-Management

### 目的
3-Tier Affiliate自動昇格（Growth Engine v1.2実装）

### トリガー
- **Webhook Trigger** (n8n-nodes-base.webhook)
  - Path: `whop-affiliate-conversion`
  - Method: POST
  - 受信データ: `affiliate_id`, `conversion_count`, `commission_tier`

### ワークフロー構造

```
1. Webhook Trigger (Whop Affiliate Conversion)
   ↓
2. Google Sheets Node (Affiliate Performance読み込み)
   - Operation: Get Row(s)
   - Range: A:F
   - Filter: affiliate_id で検索
   ↓
3. Switch Node (Tier判定Router)
   - Branch 1: monthly_conversions >= 50 → Tier 1 (40%)
   - Branch 2: monthly_conversions >= 20 → Tier 2 (25%)
   - Branch 3: monthly_conversions < 20 → Tier 3 (15%)
   ↓
4a. Gmail Node (Tier 1 Congratulations Email)
    - Subject: "🎉 You're now Tier 1 Affiliate!"

4b. Gmail Node (Tier 2 Congratulations Email)
    - Subject: "🎉 You're now Tier 2 Affiliate!"

4c. (Tier 3は維持のためEmail送信なし)
   ↓
5. HTTP Request Node (Whop API - Tier更新)
   - Method: PATCH
   - URL: `https://api.whop.com/api/v2/affiliates/{{affiliate_id}}/tier`
   - Body: { "tier": 1, "commission": 0.40 }
   ↓
6. Google Sheets Node (Tier更新)
   - Operation: Update Row
   - Update: current_tier, commission
```

### 実装ノード詳細

#### 1. Google Sheets (読み込み)
```json
{
  "type": "n8n-nodes-base.googleSheets",
  "typeVersion": 4.7,
  "parameters": {
    "operation": "read",
    "documentId": {
      "mode": "id",
      "value": "YOUR_SHEET_ID"
    },
    "sheetName": {
      "mode": "name",
      "value": "Affiliate Performance Tracker"
    },
    "range": "A:F",
    "options": {
      "useFirstRowAsHeaders": true
    }
  }
}
```

#### 2. Tier判定Router (Switch)
```json
{
  "type": "n8n-nodes-base.switch",
  "typeVersion": 3.1,
  "parameters": {
    "mode": "rules",
    "rules": {
      "values": [
        {
          "conditions": {
            "conditions": [
              {
                "leftValue": "={{ $json.monthly_conversions }}",
                "rightValue": 50,
                "operator": {
                  "type": "number",
                  "operation": "gte"
                }
              }
            ]
          },
          "renameOutput": true,
          "outputKey": "Tier1"
        },
        {
          "conditions": {
            "conditions": [
              {
                "leftValue": "={{ $json.monthly_conversions }}",
                "rightValue": 20,
                "operator": {
                  "type": "number",
                  "operation": "gte"
                }
              }
            ]
          },
          "renameOutput": true,
          "outputKey": "Tier2"
        }
      ]
    },
    "fallbackOutput": "Tier3"
  }
}
```

#### 3. Whop API (Tier更新)
```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.3,
  "parameters": {
    "method": "PATCH",
    "url": "={{ 'https://api.whop.com/api/v2/affiliates/' + $json.affiliate_id + '/tier' }}",
    "sendBody": true,
    "contentType": "json",
    "bodyParameters": {
      "parameters": [
        {
          "name": "tier",
          "value": "={{ $json.new_tier }}"
        },
        {
          "name": "commission",
          "value": "={{ $json.new_commission }}"
        }
      ]
    },
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "Authorization",
          "value": "Bearer YOUR_WHOP_API_KEY"
        }
      ]
    }
  }
}
```

### 必要な認証情報
- Google Sheets OAuth2認証
- Whop API Key
- Gmail OAuth2認証

---

## ワークフロー3: Emergency Briefing Trigger

### 目的
イベント駆動配信トリガー（Technical Supplement v2.0連動）

### トリガー
- **Webhook Trigger** (n8n-nodes-base.webhook)
  - Path: `vercel-emergency-trigger`
  - Method: POST
  - 受信データ: `market`, `triggerType`, `reason`, `briefing` (title, context, decision, watch, confidence)

### ワークフロー構造

```
1. Webhook Trigger (Vercel Emergency Trigger)
   ↓
2. Switch Node (Market Router) - 6市場分岐
   - EN, AR, KO, JA, ES, PT-BR
   ↓
3a-3f. Telegram Node (並列配信)
    - Operation: sendMessage
    - Chat ID: 市場別Telegram Channel
    - Message: Briefing内容（市場別言語）
    ↓
4. Wait Node (30秒待機) - Rate Limit対策
   - Amount: 30
   - Unit: seconds
   ↓
5. (次の市場配信)
```

### 実装ノード詳細

#### 1. Telegram Node (EN市場)
```json
{
  "type": "n8n-nodes-base.telegram",
  "typeVersion": 1.2,
  "parameters": {
    "resource": "message",
    "operation": "sendMessage",
    "chatId": "@cryptotradeacademy_en",
    "text": "={{ '🛡️ EMERGENCY: ' + $json.body.briefing.title + '\\n\\n' + 'Context: ' + $json.body.briefing.context + '\\n\\n' + 'Decision: ' + $json.body.briefing.decision + '\\n\\n' + 'What to watch: ' + $json.body.briefing.watch }}"
  }
}
```

#### 2. Wait Node (Rate Limit対策)
```json
{
  "type": "n8n-nodes-base.wait",
  "typeVersion": 1.1,
  "parameters": {
    "resume": "timeInterval",
    "amount": 30,
    "unit": "seconds"
  }
}
```

### 並列処理の実装

n8nでは、Switch Nodeの各ブランチが並列実行されるため、6市場同時配信が可能。

### 必要な認証情報
- Telegram Bot Token（6市場分）

---

## ワークフロー4: Affiliate DRM Cold Outreach

### 目的
アフィリエイター獲得Cold Outreach自動化（Zero-Budget Affiliate DRM Strategy実装）

### トリガー
- **Schedule Trigger** (n8n-nodes-base.scheduleTrigger)
  - Cron: `0 9 * * 1` (毎週月曜9時)
  - または Manual Trigger

### ワークフロー構造

```
1. Schedule Trigger (Weekly)
   ↓
2. Google Sheets Node (Affiliate List読み込み)
   - Operation: Get Row(s)
   - Filter: Status = "Pending"
   ↓
3. Code Node (Email Template選択)
   - Template A: Fan Approach
   - Template B: Partnership Approach
   - Template C: Gift Approach
   ↓
4. Gmail Node (Cold Email送信)
   - Subject: 動的生成
   - Body: Template + Personalization
   ↓
5. Google Sheets Node (Outreach Log更新)
   - Operation: Update Row
   - Update: Outreach Date, Template Used
   ↓
6. Wait Node (4日待機)
   - Amount: 4
   - Unit: days
   ↓
7. Google Sheets Node (未レスポンス者確認)
   - Filter: Response = "Pending"
   ↓
8. Gmail Node (Follow-Up Email送信)
   - Subject: "Following up..."
   - Body: Follow-Up Template
```

### 実装ノード詳細

#### 1. Google Sheets (Affiliate List)
```json
{
  "type": "n8n-nodes-base.googleSheets",
  "typeVersion": 4.7,
  "parameters": {
    "operation": "read",
    "documentId": {
      "mode": "id",
      "value": "YOUR_SHEET_ID"
    },
    "sheetName": {
      "mode": "name",
      "value": "Affiliate List"
    },
    "range": "A:J",
    "options": {
      "useFirstRowAsHeaders": true,
      "filters": {
        "conditions": [
          {
            "column": "Status",
            "condition": "equals",
            "value": "Pending"
          }
        ]
      }
    }
  }
}
```

#### 2. Code Node (Template選択)
```javascript
// Template A: Fan Approach
const templateA = `Hi {{Name}},

I watched your video on {{Topic}} yesterday. The part about {{Specific Point}} hit hard.

That's exactly why we built CryptoTrade Academy.

We run a small, invite-only affiliate program for crypto educators who actually understand trap detection. Partners earn 40% recurring commissions (not the usual 15%) because we value quality over quantity.

Since you're already teaching this stuff, we'd love to give you your own link and code through our Whop-powered portal.

If you're open to it, I can send over the details and your personal signup link (takes 2 minutes).

Does that sound interesting?

[Your Name]
Partner Lead, CryptoTrade Academy`;

// Template B, C も同様に定義

// 条件に応じてTemplate選択
const selectedTemplate = items[0].json.template_preference || 'A';
const template = selectedTemplate === 'A' ? templateA :
                 selectedTemplate === 'B' ? templateB : templateC;

return [{
  json: {
    ...items[0].json,
    email_template: template,
    email_subject: selectedTemplate === 'A' ?
      `Loved your recent video on ${items[0].json.recent_topic}` :
      selectedTemplate === 'B' ?
      `Partnership idea for ${items[0].json.channel_name}` :
      `Would love to give you free access (no strings attached)`
  }
}];
```

#### 3. Gmail Node (Cold Email)
```json
{
  "type": "n8n-nodes-base.gmail",
  "typeVersion": 2.2,
  "parameters": {
    "resource": "message",
    "operation": "send",
    "sendTo": "={{ $json.email }}",
    "subject": "={{ $json.email_subject }}",
    "emailType": "html",
    "message": "={{ $json.email_template.replace('{{Name}}', $json.name).replace('{{Topic}}', $json.recent_topic) }}"
  }
}
```

### Email Template (3種類)

#### Template A: Fan Approach
- 件名: "Loved your recent video on [Topic]"
- 本文: 138語（ドキュメント参照）

#### Template B: Partnership Approach
- 件名: "Partnership idea for [Channel/Blog Name]"
- 本文: 145語（ドキュメント参照）

#### Template C: Gift Approach
- 件名: "Would love to give you free access (no strings attached)"
- 本文: 128語（ドキュメント参照）

### Follow-Up自動化

- Day 4: Follow-Up 1
- Day 8: Follow-Up 2
- Day 15: 最終Follow-Up

各Follow-Upは、Wait Node + Google Sheets確認 + Gmail送信のループで実装。

### 必要な認証情報
- Google Sheets OAuth2認証
- Gmail OAuth2認証

---

## ワークフロー5: Affiliate Performance Tracking

### 目的
Affiliate Performance Dashboard自動更新（APDS v1.0実装）

### トリガー
- **Schedule Trigger** (n8n-nodes-base.scheduleTrigger)
  - Cron: `0 9 * * 1` (毎週月曜9時)

### ワークフロー構造

```
1. Schedule Trigger (Weekly)
   ↓
2. HTTP Request Node (Whop API - Affiliate Stats取得)
   - Method: GET
   - URL: `https://api.whop.com/api/v2/affiliates`
   ↓
3. Code Node (Performance計算)
   - Click Source別集計
   - Content Type別集計
   - Conversion Rate計算
   ↓
4. Google Sheets Node (Performance Dashboard更新)
   - Operation: Update Row
   - Sheet 1: Overview
   - Sheet 2: Source Analysis
   - Sheet 3: Content Analysis
   ↓
5. Code Node (Recommendations生成)
   - Best Source抽出
   - Best Content抽出
   - Next Action提案
   ↓
6. Gmail Node (Weekly Report送信)
   - Subject: "Your Weekly Performance Report"
   - Body: Dashboard + Recommendations
```

### 実装ノード詳細

#### 1. Whop API (Affiliate Stats)
```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.3,
  "parameters": {
    "method": "GET",
    "url": "https://api.whop.com/api/v2/affiliates",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "Authorization",
          "value": "Bearer YOUR_WHOP_API_KEY"
        }
      ]
    }
  }
}
```

#### 2. Code Node (Performance計算)
```javascript
const affiliateData = items[0].json;

// Source別集計
const sourceStats = {
  X: { clicks: 0, conversions: 0 },
  Reddit: { clicks: 0, conversions: 0 },
  YouTube: { clicks: 0, conversions: 0 },
  Email: { clicks: 0, conversions: 0 }
};

// Content Type別集計
const contentStats = {
  Thread: { clicks: 0, conversions: 0 },
  Comment: { clicks: 0, conversions: 0 },
  Video: { clicks: 0, conversions: 0 },
  Article: { clicks: 0, conversions: 0 }
};

// データ処理（実際のデータ構造に応じて調整）
affiliateData.clicks?.forEach(click => {
  const source = click.source;
  const contentType = click.content_type;

  if (sourceStats[source]) {
    sourceStats[source].clicks++;
    if (click.converted) sourceStats[source].conversions++;
  }

  if (contentStats[contentType]) {
    contentStats[contentType].clicks++;
    if (click.converted) contentStats[contentType].conversions++;
  }
});

// Conversion Rate計算
Object.keys(sourceStats).forEach(source => {
  sourceStats[source].conversionRate =
    sourceStats[source].clicks > 0 ?
    (sourceStats[source].conversions / sourceStats[source].clicks * 100).toFixed(2) : 0;
});

return [{
  json: {
    affiliate_id: affiliateData.id,
    source_stats: sourceStats,
    content_stats: contentStats,
    total_clicks: affiliateData.total_clicks || 0,
    total_conversions: affiliateData.total_conversions || 0,
    overall_conversion_rate: affiliateData.total_clicks > 0 ?
      (affiliateData.total_conversions / affiliateData.total_clicks * 100).toFixed(2) : 0
  }
}];
```

---

## 実装優先順位

### Phase 1 (即実装)
1. **Trial Onboarding Automation** - 最重要
2. **Emergency Briefing Trigger** - コア機能

### Phase 2 (1週間以内)
3. **Affiliate Auto-Management** - Tier管理自動化
4. **Affiliate DRM Cold Outreach** - 獲得自動化

### Phase 3 (1ヶ月以内)
5. **Affiliate Performance Tracking** - 最適化支援

---

## 必要な認証情報まとめ

### 必須
- **Gmail OAuth2** - Email送信用
- **Telegram Bot Token** - 6市場分（EN/AR/KO/JA/ES/PT-BR）
- **Whop API Key** - Webhook受信 + API呼び出し
- **Google Sheets OAuth2** - データ管理用

### オプション
- **Vercel API Key** - Emergency Trigger連携用

---

## n8n設定手順

### 1. 認証情報設定
1. n8n Dashboard → Credentials
2. 各サービス（Gmail, Telegram, Google Sheets, HTTP Request）の認証情報を追加

### 2. ワークフロー作成
1. n8n Dashboard → Workflows → Add Workflow
2. 上記の設計に基づいてノードを追加
3. 接続を設定
4. 各ノードのパラメータを設定

### 3. テスト実行
1. Manual Triggerでテスト
2. Webhook URLをWhop/Vercelに設定
3. 実際のデータで動作確認

### 4. 本番有効化
1. ワークフローをActive化
2. 監視設定
3. エラーハンドリング追加

---

## Make.comからの移行メモ

### 主な違い
- **Make.com**: Scenario = n8n: Workflow
- **Make.com**: Module = n8n: Node
- **Make.com**: Sleep module = n8n: Wait Node
- **Make.com**: Router = n8n: Switch Node
- **Make.com**: Webhook = n8n: Webhook Trigger

### 機能マッピング
| Make.com | n8n |
|----------|-----|
| Custom Webhook | Webhook Trigger |
| Gmail / SendGrid | Gmail Node |
| Sleep | Wait Node |
| Router | Switch Node |
| HTTP Request | HTTP Request Node |
| Google Sheets | Google Sheets Node |
| Telegram Bot API | Telegram Node |

---

## 次のステップ

1. **n8nインスタンス確認**
   - 接続確認
   - 認証情報設定

2. **ワークフロー1から順次実装**
   - Trial Onboarding Automation
   - テスト実行
   - 本番有効化

3. **監視と最適化**
   - エラーログ確認
   - パフォーマンス測定
   - 改善実施

---

**作成日**: 2025-01-XX
**バージョン**: 1.0
**ステータス**: 設計完了 - 実装待ち





















