# Telegramリアルタイム監視設計

**作成日**: 2025-12-26
**目的**: Telegram配信をリアルタイムで受信・監視し、プログラムとの整合を図る

---

## 🎯 目的

1. **リアルタイム監視**: Telegramチャンネルへの配信をリアルタイムで受信
2. **整合性確認**: プログラム（cryptosignal-ai）からの配信内容を確認
3. **60-second reads検証**: メッセージが戦略要件（60-second reads）に準拠しているか自動検証
4. **ログ記録**: すべての配信メッセージを記録・分析可能にする

---

## 📊 監視対象

### 6市場別Telegramチャンネル

| 市場 | Telegram Channel | Chat ID (Infisical) |
|------|------------------|---------------------|
| EN | @cryptotradeacademy_en | `TELEGRAM_CHAT_ID_EN` |
| AR | @cryptotradeacademy_ar | `TELEGRAM_CHAT_ID_AR` |
| KO | @cryptotradeacademy_ko | `TELEGRAM_CHAT_ID_KO` |
| JA | @cryptotradeacademy_ja | `TELEGRAM_CHAT_ID_JA` |
| ES | @cryptotradeacademy_es | `TELEGRAM_CHAT_ID_ES` |
| PT-BR | @cryptotradeacademy_pt_br | `TELEGRAM_CHAT_ID_PT_BR` |

---

## 🔄 監視方法

### 方法1: Telegram Trigger Node（推奨）

**n8n Telegram Trigger Node**を使用して、Telegram Botが受信したメッセージをリアルタイムで取得。

**メリット**:
- ✅ リアルタイム受信
- ✅ n8nワークフローで処理可能
- ✅ 設定が簡単

**設定**:
1. n8n Dashboard → Workflows → Add Workflow
2. Telegram Trigger Nodeを追加
3. Credentials: Telegram Bot Token（Infisicalから取得）
4. Updates: `message` を選択

### 方法2: Telegram Webhook

**Telegram Webhook**を使用して、メッセージをn8n Webhook Triggerで受信。

**メリット**:
- ✅ より柔軟な設定
- ✅ 複数のBotに対応可能

**設定**:
1. Telegram Bot API: `setWebhook` を呼び出し
2. n8n Webhook Trigger URLを設定
3. Webhook Triggerでメッセージ受信

---

## 📋 ワークフロー設計

### ワークフロー名: `telegram-monitor-realtime`

**構造**:

```
1. Telegram Trigger
   ↓
2. Format Message Data
   - timestamp, message_id, chat_id, chat_title, text等を抽出
   ↓
3. Filter: Channels Only
   - channelタイプのメッセージのみ通過
   ↓
4. Analyze Message (60-sec reads)
   - 市場別文字数/語数制限チェック
   - 日本語: 300文字以内
   - その他: 150語以内
   ↓
5a. Filter: Deviations Only
    - 要件違反メッセージのみ通過
    ↓
5b. Format Log
    - すべてのメッセージをログ形式に整形
    ↓
6a. Notify: Slack (Deviations)
    - 偏差検知時にSlackに通知（オプション）
    ↓
6b. Log to Google Sheets
    - すべてのメッセージをGoogle Sheetsに記録
```

---

## 🔍 分析内容

### 60-second reads検証

**市場別要件**:
- **日本語（JA）**: 300文字以内（60秒読了）
- **その他（EN/AR/KO/ES/PT-BR）**: 150語以内（60-second reads）

**検証項目**:
- ✅ 文字数/語数カウント
- ✅ 要件準拠チェック
- ✅ 偏差量計算
- ✅ コンプライアンスステータス判定

**出力データ**:
```json
{
  "analysis": {
    "text_length": 450,
    "word_count": 85,
    "market": "EN",
    "requirement": "150語以内（60-second reads）",
    "max_words": 150,
    "is_compliant": true,
    "deviation": -65,
    "compliance_status": "✅ COMPLIANT",
    "message_preview": "🛡️ EMERGENCY: Market trap detected..."
  }
}
```

---

## 📝 ログ記録

### Google Sheets記録

**シート構成**:

| 列名 | 説明 |
|------|------|
| timestamp | メッセージ受信時刻 |
| message_id | Telegram Message ID |
| chat_id | Chat ID |
| chat_title | チャンネル名 |
| chat_type | チャンネルタイプ（channel/supergroup） |
| market | 市場コード（EN/AR/KO/JA/ES/PT-BR） |
| text_length | 文字数 |
| word_count | 語数 |
| is_compliant | 要件準拠（TRUE/FALSE） |
| compliance_status | ステータス（✅ COMPLIANT / ❌ DEVIATION） |
| message_preview | メッセージプレビュー（最初の100文字） |

**用途**:
- 配信履歴の可視化
- 60-second reads達成率の測定
- 偏差分析
- プログラムとの整合性確認

---

## 🔔 通知設定（オプション）

### Slack通知

**通知条件**:
- 60-second reads要件違反検知時
- 重大な偏差検知時

**通知内容**:
- 市場
- チャンネル名
- 要件
- 偏差量
- メッセージプレビュー

---

## 🚀 実装手順

### Phase 1: 基盤構築

1. **Infisical設定確認**
   ```bash
   python scripts/setup-telegram-multi-language-keys.py
   ```

2. **Telegram Bot Token確認**
   - 6市場分のBot TokenがInfisicalに設定されているか確認
   - 各Botが対応チャンネルに追加されているか確認

3. **n8n Credentials設定**
   - n8n Dashboard → Credentials → Telegram
   - 各市場別Bot Tokenを設定（または共通Bot Token使用）

### Phase 2: ワークフロー実装

1. **telegram-monitor-realtimeワークフロー作成**
   - `workflows/telegram-monitor-realtime.json`をn8nにインポート
   - Telegram Trigger Node設定
   - Credentials設定

2. **Google Sheets準備**
   - Google Sheets作成
   - 列構成を設定
   - n8n Credentials: Google Sheets OAuth2設定

3. **テスト実行**
   - Manual Triggerでテスト
   - 実際のTelegramメッセージで動作確認

### Phase 3: 監視開始

1. **ワークフロー有効化**
   - n8n DashboardでワークフローをActive化

2. **監視開始**
   - リアルタイムでメッセージ受信開始
   - Google Sheetsに記録開始

3. **偏差検知確認**
   - 要件違反メッセージが検知されるか確認
   - Slack通知（設定時）が動作するか確認

---

## 📊 KPI設定

### 監視KPI

| KPI | 目標値 | 測定方法 |
|-----|--------|---------|
| メッセージ受信率 | 100% | Google Sheets: 記録されたメッセージ数 / 実際の配信数 |
| 60-second reads達成率 | 100% | Google Sheets: is_compliant=TRUE / 総メッセージ数 |
| 偏差検知時間 | < 1秒 | Telegram Trigger → Google Sheets記録までの時間 |

---

## 🔗 関連ドキュメント

- [n8n + Whop + Telegram 統合戦略 SSOT](./n8n-whop-telegram-integration-SSOT.md)
- [TELEGRAM_API_CONTROL_VERIFIED.md](./TELEGRAM_API_CONTROL_VERIFIED.md)
- [CryptoTrade Academy - Complete SSOT v5.1](../../hadayalab-knowledge-base/literature/strategy/CryptoTrade Academy - Complete SSOT v5.1.md) - 60-second reads要件

---

**最終更新**: 2025-12-26

