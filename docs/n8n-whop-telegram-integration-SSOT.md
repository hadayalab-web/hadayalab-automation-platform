# n8n + Whop + Telegram 統合戦略 SSOT

**最終更新**: 2025-12-26
**バージョン**: 1.0.0
**メンテナー**: HadayaLab
**親SSOT**: [n8n + Whop 完全活用戦略 SSOT](./n8n-whop-full-strategy-SSOT.md)

---

## 📍 ドキュメント位置づけ

### SSOT階層構造

```
hadayalab-automation-platform SSOT
  └─ n8n + Whop 完全活用戦略 SSOT
      └─ n8n + Whop + Telegram 統合戦略 SSOT（本ドキュメント）
```

### 親戦略ドキュメント

- **[n8n + Whop 完全活用戦略 SSOT](./n8n-whop-full-strategy-SSOT.md)** - 親戦略SSOT
- **[CryptoTrade Academy - Complete SSOT v5.1](../../hadayalab-knowledge-base/literature/strategy/CryptoTrade Academy - Complete SSOT v5.1.md)** - 戦略SSOT

---

## 🎯 統合ビジョン

### 目標

**「Whopで管理されているTelegramチャンネルを、n8nワークフローから完全制御し、メンバーシップ状態に応じた自動アクセス管理を実現する」**

### 3層統合アーキテクチャ

```
┌─────────────────────────────────────────────────┐
│  Layer 1: Cursor UI（統一開発環境）              │
│  - n8n-mcp（ワークフロー作成・編集）            │
│  - n8nネイティブMCP（ワークフロー実行）          │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│  Layer 2: n8n Cloud（実行エンジン）              │
│  - Whop Webhook受信                            │
│  - Whop API呼び出し                            │
│  - Telegram Bot API呼び出し                    │
└───────┬───────────────────┬─────────────────────┘
        │                   │
┌───────▼────────┐  ┌───────▼────────┐
│  Whop Platform │  │  Telegram API  │
│  - Memberships │  │  - Channels    │
│  - Products    │  │  - Messages    │
│  - Experiences │  │  - Access      │
│  - Entries     │  │                │
└────────────────┘  └────────────────┘
```

---

## 🔌 Whop + Telegram統合の仕組み

### WhopでのTelegram統合方法

**Whop Dashboard設定**:
1. Whop Dashboard → Products → [Product選択]
2. Settings → Experiences
3. "Connect Telegram" を選択
4. Telegramチャンネル/グループを接続
5. アクセス権限設定（Membership状態に応じて自動管理）

**Whop APIでの制御**:
- **Experiences API**: Telegramチャンネル/グループへのアクセス管理
- **Entries API**: メンバーのTelegramアクセス承認・拒否
- **Memberships API**: メンバーシップ状態に応じた自動アクセス管理

### アクセス管理フロー

```
1. ユーザーがWhopでメンバーシップ取得
   ↓
2. Whop Webhook: membership.activated 発火
   ↓
3. n8nワークフロー: whop-webhooks-receiver 受信
   ↓
4. Whop API: Entry作成（Telegramアクセスリクエスト）
   ↓
5. Whop API: Entry承認（自動承認または手動承認）
   ↓
6. Telegram: ユーザーがチャンネルに追加される
   ↓
7. n8nワークフロー: Telegram Welcome Message送信（オプション）
```

---

## 🔄 n8nワークフロー統合設計

### 1. Telegramチャンネルアクセス自動管理ワークフロー

#### ワークフロー名: `whop-telegram-access-management`

**目的**:
- Whopメンバーシップ状態に応じてTelegramチャンネルへのアクセスを自動管理
- メンバーシップ有効化 → Telegramチャンネル追加
- メンバーシップキャンセル → Telegramチャンネル削除

**トリガー**:
- **Whop Webhook**: `membership.activated`, `membership.cancelled`, `membership.deactivated`

**ワークフロー構造**:

```
1. Webhook Trigger (Whop Membership Events)
   ↓
2. Switch Node (Event Router)
   - membership.activated → Add to Telegram
   - membership.cancelled → Remove from Telegram
   - membership.deactivated → Remove from Telegram
   ↓
3a. Whop API: Get Membership Details
    - membership_id取得
    - user情報取得
    ↓
3b. Whop API: Get Product Details
    - product_idからExperiences取得
    - Telegram Experience ID取得
    ↓
4a. Whop API: Create Entry (membership.activated時)
    - Experience ID: Telegram Experience
    - User ID: membership.user.id
    - Auto approve: true
    ↓
4b. Whop API: Delete Entry (membership.cancelled時)
    - Entry ID取得
    - Entry削除
    ↓
5. Telegram Bot API: Send Welcome Message（オプション）
   - Chat ID: ユーザーのTelegram User ID
   - Message: Welcome Message（市場別言語）
```

**実装ノード詳細**:

#### 1. Webhook Trigger (Whop Membership Events)

```json
{
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 2.1,
  "parameters": {
    "httpMethod": "POST",
    "path": "whop-telegram-access",
    "responseMode": "responseNode"
  }
}
```

#### 2. Switch Node (Event Router)

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
                "leftValue": "={{ $json.body.type }}",
                "rightValue": "membership.activated",
                "operator": {
                  "type": "string",
                  "operation": "equals"
                }
              }
            ]
          },
          "renameOutput": true,
          "outputKey": "activated"
        },
        {
          "conditions": {
            "conditions": [
              {
                "leftValue": "={{ $json.body.type }}",
                "rightValue": "membership.cancelled",
                "operator": {
                  "type": "string",
                  "operation": "equals"
                }
              }
            ]
          },
          "renameOutput": true,
          "outputKey": "cancelled"
        }
      ]
    }
  }
}
```

#### 3. Whop API: Get Membership Details

```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "parameters": {
    "method": "GET",
    "url": "=https://api.whop.com/api/v2/memberships/{{ $json.body.data.id }}",
    "options": {
      "headers": {
        "Authorization": "Bearer YOUR_WHOP_API_KEY"
      }
    }
  }
}
```

#### 4. Whop API: Create Entry (Telegramアクセス追加)

```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "parameters": {
    "method": "POST",
    "url": "=https://api.whop.com/api/v2/entries",
    "sendBody": true,
    "contentType": "json",
    "bodyParameters": {
      "parameters": [
        {
          "name": "experience_id",
          "value": "={{ $json.product.experiences[0].id }}"
        },
        {
          "name": "user_id",
          "value": "={{ $json.user.id }}"
        },
        {
          "name": "auto_approve",
          "value": "true"
        }
      ]
    },
    "options": {
      "headers": {
        "Authorization": "Bearer YOUR_WHOP_API_KEY"
      }
    }
  }
}
```

#### 5. Telegram Bot API: Send Welcome Message

```json
{
  "type": "n8n-nodes-base.telegram",
  "typeVersion": 1.2,
  "parameters": {
    "resource": "message",
    "operation": "sendMessage",
    "chatId": "={{ $json.user.telegram_user_id }}",
    "text": "={{ 'Welcome to CryptoTrade Academy! 🎓\\n\\n' + 'Your Telegram channel access has been activated.\\n\\n' + 'Join here: ' + $json.product.telegram_channel_url }}"
  }
}
```

---

### 2. Telegram配信ワークフロー（既存設計拡張）

#### ワークフロー名: `telegram-briefing-delivery`

**目的**:
- VercelからのEmergency Briefing Trigger受信
- 6市場別Telegramチャンネルへの配信
- Whopメンバーシップ状態に応じた配信制御

**統合ポイント**:
- Whop APIでメンバーシップ状態を確認
- アクティブメンバーのみに配信
- キャンセル済みメンバーは除外

**ワークフロー構造（拡張版）**:

```
1. Webhook Trigger (Vercel Emergency Briefing)
   ↓
2. Whop API: Get Active Memberships
   - Filter: status = "active"
   - Filter: product_id = [6市場別Product ID]
   ↓
3. Switch Node (Market Router)
   - EN → @cryptotradeacademy_en
   - AR → @cryptotradeacademy_ar
   - KO → @cryptotradeacademy_ko
   - JA → @cryptotradeacademy_ja
   - ES → @cryptotradeacademy_es
   - PT-BR → @cryptotradeacademy_pt_br
   ↓
4. Telegram Node: Send Message to Channel
   - Chat ID: 市場別Telegram Channel
   - Message: Briefing内容（市場別言語）
   ↓
5. Wait Node (30秒待機) - Rate Limit対策
   ↓
6. (次の市場配信)
```

---

### 3. Trial Onboarding + Telegram統合ワークフロー

#### ワークフロー名: `trial-onboarding-with-telegram`

**目的**:
- Trial開始時にTelegramチャンネルアクセスを自動付与
- Welcome Email + Telegram Welcome Message
- 6時間後: Value Email + Telegram Value Message

**Complete SSOT v5.1 Section 3準拠**:
- Nudge Feedback Loop実装
- マルチチャネル（Email + Telegram）での価値体験

**ワークフロー構造**:

```
1. Webhook Trigger (Whop Trial Started)
   ↓
2. Whop API: Create Entry (Telegramアクセス追加)
   ↓
3. Switch Node (Market Router) - 6市場分岐
   ↓
4a. Gmail Node: Welcome Email送信
4b. Telegram Node: Welcome Message送信（同期）
   ↓
5. Wait Node (6時間待機)
   ↓
6a. Gmail Node: Value Email送信
6b. Telegram Node: Value Message送信（同期）
   ↓
7. Wait Node (12時間待機)
   ↓
8a. Gmail Node: Trial End Notification
8b. Telegram Node: Trial End Reminder（同期）
```

---

## 📊 市場別Telegramチャンネル設定

### CryptoTrade Academy 6市場別チャンネル

| 市場 | Telegram Channel | Product ID (Whop) | Experience ID (Telegram) | ステータス |
|------|------------------|-------------------|--------------------------|----------|
| EN | @cryptotradeacademy_en | `prod_xxxxx_en` | `exp_xxxxx_en` | 🚧 Whop設定待ち |
| AR | @cryptotradeacademy_ar | `prod_xxxxx_ar` | `exp_xxxxx_ar` | 🚧 Whop設定待ち |
| KO | @cryptotradeacademy_ko | `prod_xxxxx_ko` | `exp_xxxxx_ko` | 🚧 Whop設定待ち |
| JA | @cryptotradeacademy_ja | `prod_xxxxx_ja` | `exp_xxxxx_ja` | 🚧 Whop設定待ち |
| ES | @cryptotradeacademy_es | `prod_xxxxx_es` | `exp_xxxxx_es` | 🚧 Whop設定待ち |
| PT-BR | @cryptotradeacademy_pt_br | `prod_xxxxx_pt_br` | `exp_xxxxx_pt_br` | 🚧 Whop設定待ち |

**現在アクセス可能なチャンネル**:
- ✅ **メインチャンネル（EN市場）**: CryptoSignal AI – Starter Signals (EN)
  - Chat ID: `-1003223165053` (Infisical: `TELEGRAM_CHAT_ID`)
  - Bot: @CryptoSignal_AI_Official_bot
  - アクセス確認済み

**設定方法**:
1. Whop Dashboard → Products → [市場別Product選択]
2. Settings → Experiences → "Connect Telegram"
3. Telegramチャンネルを接続
4. Experience IDをメモ（APIで使用）
5. BotをチャンネルにAdminとして追加
6. Infisicalに`TELEGRAM_CHAT_ID_*`を設定（オプション）

---

## 🔐 認証・認可設定

### 必要な認証情報

#### 1. Whop API Key ✅ Infisical管理済み

**取得方法**:
- Whop Dashboard → Developer → API Keys
- 権限: `memberships:read`, `memberships:write`, `entries:read`, `entries:write`, `experiences:read`

**Infisical管理**:
- ✅ Key: `WHOP_API_KEY` - Infisical管理済み
- 参照: [Infisical設定ガイド](./infisical-setup.md)

#### 2. Telegram Bot Token ✅ Infisical管理済み・制御確認済み

**取得方法**:
- @BotFather → /newbot → Bot作成
- Bot Token取得
- 各チャンネルにBotをAdminとして追加

**Infisical管理**:
- ✅ `TELEGRAM_BOT_TOKEN` - メインBot Token（Infisical管理済み・制御確認済み）
  - Bot Username: @CryptoSignal_AI_Official_bot
  - Bot Name: CryptoSignal AI EN
  - Bot ID: 8155351788
- ✅ `TELEGRAM_CHAT_ID` - メインChat ID（Infisical管理済み・制御確認済み）
  - Chat ID: -1003223165053
  - Chat Title: CryptoSignal AI – Starter Signals (EN)
  - Chat Type: supergroup
- ✅ `TELEGRAM_ADMIN_ID` - Admin User ID（Infisical管理済み）

**取得方法（Pythonスクリプト）**:
```python
from scripts.telegram_channel_control import get_secret_from_infisical
bot_token = get_secret_from_infisical("TELEGRAM_BOT_TOKEN")
chat_id = get_secret_from_infisical("TELEGRAM_CHAT_ID")
```

**テストスクリプト**:
- ✅ `scripts/test-telegram-api.py` - Telegram API接続テスト
- ✅ `scripts/telegram-channel-control.py` - チャンネル制御テスト（動作確認済み）
- ✅ `scripts/list-infisical-secrets.py` - Infisicalシークレット一覧

**制御確認結果（2025-12-26）**:
- ✅ InfisicalからTelegram Bot Token取得成功
- ✅ Bot情報取得成功（getMe API）
- ✅ メインチャンネル（TELEGRAM_CHAT_ID）へのアクセス成功
- ✅ チャンネル情報取得成功（getChat API）

#### 3. Telegram Channel ID（6市場分）

**取得方法**:
- チャンネル作成後、チャンネルIDを取得
- または: `@channel_username` を使用
- Whop Dashboard → Products → Experiences → Telegram Experience設定から取得

**設定場所**:
- Infisical: `TELEGRAM_CHAT_ID_*` （市場別に設定予定）
- n8n Credentials: Telegram Node設定
- または: ワークフロー内で動的に取得

**現在の状況**:
- ✅ メインチャンネル（EN市場）: TELEGRAM_CHAT_ID設定済み・アクセス確認済み
- 🚧 6市場別チャンネル: Whop Experience設定後にBot追加予定

---

## 🔄 データフロー設計

### メンバーシップ有効化フロー

```
Whop Platform
  └─→ membership.activated Webhook
      └─→ n8n: whop-telegram-access-management
          └─→ Whop API: Get Membership Details
              └─→ Whop API: Get Product/Experience Details
                  └─→ Whop API: Create Entry (Telegram Experience)
                      └─→ Whop: Telegramチャンネルにユーザー追加（自動）
                          └─→ n8n: Telegram Welcome Message送信（オプション）
```

### Briefing配信フロー

```
Vercel (cryptosignal-ai)
  └─→ Emergency Briefing Trigger
      └─→ n8n: telegram-briefing-delivery
          └─→ Whop API: Get Active Memberships
              └─→ Filter: status = "active", product_id = [市場別]
                  └─→ Telegram: Send Message to Channel（アクティブメンバーのみ）
```

---

## ✅ 実装チェックリスト

### Phase 1: 基盤構築

- [ ] Whop DashboardでTelegramチャンネル接続（6市場分）
- [ ] Experience ID取得（6市場分）
- [ ] Telegram Bot作成・チャンネル追加（6市場分）
- [ ] Infisicalに認証情報設定
- [ ] n8n Credentials設定

### Phase 2: アクセス管理ワークフロー

- [ ] whop-telegram-access-managementワークフロー作成
- [ ] Whop Webhook設定（membership.activated, membership.cancelled）
- [ ] Whop API: Entry作成・削除実装
- [ ] Telegram Welcome Message実装（オプション）

### Phase 3: 配信ワークフロー拡張

- [ ] telegram-briefing-deliveryワークフロー作成
- [ ] Whop API: アクティブメンバー取得実装
- [ ] 市場別チャンネル配信実装
- [ ] Rate Limit対策実装

### Phase 4: Trial Onboarding統合

- [ ] trial-onboarding-with-telegramワークフロー作成
- [ ] Email + Telegram同期配信実装
- [ ] Nudge Feedback Loop実装

---

## 📊 KPI設定

### Telegram統合KPI

| KPI | 目標値 | 測定方法 |
|-----|--------|---------|
| Telegramアクセス付与率 | 100% | Whop API: Entry作成成功数 / membership.activated数 |
| Telegram Welcome Message到達率 | 95%+ | Telegram API: Message Delivery Status |
| Briefing配信到達率 | 99%+ | Telegram API: Channel Message Delivery |
| アクティブメンバー配信精度 | 100% | Whop API: アクティブメンバーフィルタリング |

---

## 🔗 関連ドキュメント

**親戦略ドキュメント**:
- [n8n + Whop 完全活用戦略 SSOT](./n8n-whop-full-strategy-SSOT.md) - 親戦略SSOT
- [CryptoTrade Academy - Complete SSOT v5.1](../../hadayalab-knowledge-base/literature/strategy/CryptoTrade Academy - Complete SSOT v5.1.md) - 戦略SSOT

**技術ドキュメント**:
- **[TELEGRAM_API_CONTROL_VERIFIED.md](./TELEGRAM_API_CONTROL_VERIFIED.md)** - Telegram API制御確認済みレポート ⭐
- **[telegram-realtime-monitoring-design.md](./telegram-realtime-monitoring-design.md)** - Telegramリアルタイム監視設計 ⭐ 新規追加
- [WHOP_API_CAPABILITIES_COMPLETE.md](./WHOP_API_CAPABILITIES_COMPLETE.md) - Whop API完全機能一覧
- [whop-control-workflow SSOT](./whop-control-workflow-SSOT.md) - Whop制御ワークフローのSSOT
- [n8n-workflows-design.md](../n8n-workflows-design.md) - ワークフロー設計ドキュメント

**設定ガイド**:
- [Infisical設定ガイド](./infisical-setup.md) - シークレット一元管理
- [n8n Cloud同期運用](./n8n-cloud-sync.md) - GitHub⇔n8n Cloud同期詳細

**テストスクリプト**:
- `scripts/test-telegram-api.py` - Telegram API接続テスト
- `scripts/telegram-channel-control.py` - チャンネル制御テスト
- `scripts/list-infisical-secrets.py` - Infisicalシークレット一覧
- `scripts/setup-telegram-multi-language-keys.py` - 6市場別キー設定確認 ⭐ 新規追加
- `scripts/verify-telegram-multi-language-keys.py` - 6市場別キー実値確認 ⭐ 新規追加

**ワークフロー**:
- `workflows/telegram-monitor-realtime.json` - Telegramリアルタイム監視ワークフロー ⭐ 新規追加

---

## 🔄 更新履歴

### v1.0.0 (2025-12-26)

- 初版作成
- n8n + Whop + Telegram統合戦略の体系化
- アクセス管理ワークフロー設計
- 配信ワークフロー拡張設計

---

**最終更新**: 2025-12-26
**バージョン**: 1.0.0
**メンテナー**: HadayaLab

