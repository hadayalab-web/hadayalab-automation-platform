# Telegramリアルタイム監視 実装ガイド

**作成日**: 2025-12-26
**目的**: Telegram配信をリアルタイムで受信・監視するn8nワークフローの実装

---

## 🎯 実装概要

### 目的

1. **リアルタイム監視**: Telegramチャンネルへの配信をリアルタイムで受信
2. **整合性確認**: プログラム（cryptosignal-ai）からの配信内容を確認
3. **60-second reads検証**: メッセージが戦略要件（60-second reads）に準拠しているか自動検証
4. **ログ記録**: すべての配信メッセージを記録・分析可能にする

---

## 📋 前提条件

### 1. Infisical設定完了

- ✅ `TELEGRAM_BOT_TOKEN`（メインBot Token）
- ✅ `TELEGRAM_CHAT_ID`（メインChat ID）
- 🚧 `TELEGRAM_BOT_TOKEN_*`（6市場別Bot Token）← 設定必要
- 🚧 `TELEGRAM_CHAT_ID_*`（6市場別Chat ID）← 設定必要

**参照**: [Telegram多言語版キー設定ガイド](./telegram-multi-language-keys-setup-guide.md)

### 2. n8n Credentials設定

1. n8n Dashboard → Credentials → Add Credential
2. Telegram認証情報を追加
   - Name: `Telegram Bot (Main)` または `Telegram Bot (EN)`
   - Bot Token: Infisicalから取得（または直接入力）

### 3. Google Sheets準備（オプション）

ログ記録用のGoogle Sheetsを作成:
- シート名: `Telegram Messages`
- 列構成:
  - timestamp, message_id, chat_id, chat_title, chat_type
  - market, text_length, word_count, is_compliant
  - compliance_status, message_preview

---

## 🚀 実装手順

### Phase 1: ワークフローインポート

1. **ワークフローファイル確認**
   ```bash
   cd hadayalab-automation-platform
   cat workflows/telegram-monitor-realtime.json
   ```

2. **n8nにインポート**
   - n8n Dashboard → Workflows → Import from File
   - `workflows/telegram-monitor-realtime.json` を選択
   - ワークフロー名: `telegram-monitor-realtime`

### Phase 2: ノード設定

#### 1. Telegram Trigger Node設定

1. **Telegram Trigger Node**を開く
2. **Credentials**: `Telegram Bot (Main)` を選択
3. **Updates**: `message` を選択
4. **Additional Fields**: デフォルトのまま

**注意**:
- Telegram Trigger Nodeは**Webhook Mode**で動作します
- n8n Cloudの場合、自動的にWebhook URLが設定されます
- Self-hostedの場合、公開URLが必要です

#### 2. Format Message Data Node確認

- データ抽出ロジックを確認
- 必要に応じて調整

#### 3. Analyze Message Node調整

- 市場別の文字数/語数制限を確認
- 必要に応じて調整

#### 4. Google Sheets Node設定（オプション）

1. **Google Sheets Node**を開く
2. **Credentials**: Google Sheets OAuth2認証情報を選択
3. **Sheet ID**: 作成したGoogle SheetsのID
4. **Sheet Name**: `Telegram Messages`
5. **Columns Mapping**: 列マッピングを確認

#### 5. Slack通知Node設定（オプション）

1. **HTTP Request Node**を開く
2. **URL**: Slack Webhook URL
3. **Method**: POST
4. **Body**: JSON形式でメッセージを構成

---

### Phase 3: テスト実行

#### 1. Manual Triggerテスト

1. ワークフローを保存
2. **Execute Workflow** をクリック
3. Telegram Trigger Nodeが待機状態になることを確認

#### 2. 実際のメッセージでテスト

1. Telegramチャンネルにテストメッセージを送信
2. ワークフローがトリガーされることを確認
3. 各ノードの出力を確認

#### 3. ログ記録確認

1. Google Sheetsにメッセージが記録されることを確認
2. 60-second reads検証が正しく動作することを確認

---

## 📊 ワークフロー詳細

### ワークフロー構造

```
1. Telegram Trigger
   ↓ (メッセージ受信)
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

## 🔍 分析ロジック

### 60-second reads検証

**市場別要件**:
- **日本語（JA）**: 300文字以内（60秒読了）
- **その他（EN/AR/KO/ES/PT-BR）**: 150語以内（60-second reads）

**検証コード**（Analyze Message Node）:
```javascript
const text = $input.item.json.text || '';
const textLength = text.length;
const wordCount = text.split(/\s+/).filter(w => w.length > 0).length;
const market = $input.item.json.market || 'UNKNOWN';

let maxChars = 1500;
let maxWords = 500;
let requirement = 'Unknown';

if (market === 'JA') {
  maxChars = 300;
  requirement = '300文字以内（60秒読了）';
} else if (['EN', 'AR', 'KO', 'ES', 'PT-BR'].includes(market)) {
  maxWords = 150;
  requirement = '150語以内（60-second reads）';
}

const isCompliant = market === 'JA' ? textLength <= maxChars : wordCount <= maxWords;
const deviation = market === 'JA' ? textLength - maxChars : wordCount - maxWords;
```

---

## 📝 ログ記録フォーマット

### Google Sheets記録形式

| 列名 | 値 | 説明 |
|------|-----|------|
| timestamp | `2025-12-26T13:00:00Z` | メッセージ受信時刻 |
| message_id | `12345` | Telegram Message ID |
| chat_id | `-1003223165053` | Chat ID |
| chat_title | `CryptoSignal AI – Starter Signals (EN)` | チャンネル名 |
| chat_type | `supergroup` | チャンネルタイプ |
| market | `EN` | 市場コード |
| text_length | `450` | 文字数 |
| word_count | `85` | 語数 |
| is_compliant | `TRUE` | 要件準拠（TRUE/FALSE） |
| compliance_status | `✅ COMPLIANT` | ステータス |
| message_preview | `🛡️ EMERGENCY: Market trap...` | メッセージプレビュー |

---

## 🔔 通知設定（オプション）

### Slack通知

**通知条件**: 60-second reads要件違反検知時

**通知内容**:
```
❌ Telegram Message Deviation Detected

*Market*: EN
*Chat*: CryptoSignal AI – Starter Signals (EN)
*Requirement*: 150語以内（60-second reads）
*Status*: ❌ DEVIATION
*Deviation*: +25
*Text Length*: 520
*Word Count*: 175

*Message Preview*:
```
🛡️ EMERGENCY: Market trap detected...
```

**設定方法**:
1. Slack App作成: https://api.slack.com/apps
2. Incoming Webhooks有効化
3. Webhook URL取得
4. HTTP Request NodeのURLに設定

---

## 🐛 トラブルシューティング

### 問題1: Telegram Triggerが動作しない

**原因**:
- Bot Tokenが無効
- Botがチャンネルに追加されていない
- Webhook URLが設定されていない（Self-hostedの場合）

**解決方法**:
1. Bot Tokenを確認: `scripts/test-telegram-api.py`
2. Botがチャンネルに追加されているか確認
3. n8n Cloudの場合、自動的にWebhook URLが設定される
4. Self-hostedの場合、公開URLを設定

### 問題2: メッセージが記録されない

**原因**:
- Google Sheets認証情報が無効
- Sheet IDが間違っている
- 列マッピングが間違っている

**解決方法**:
1. Google Sheets認証情報を再設定
2. Sheet IDを確認
3. 列マッピングを確認

### 問題3: 60-second reads検証が正しく動作しない

**原因**:
- 市場判定ロジックが間違っている
- 文字数/語数カウントが間違っている

**解決方法**:
1. Analyze Message Nodeのコードを確認
2. 市場判定ロジックを確認
3. テストメッセージで検証

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

- [Telegramリアルタイム監視設計](./telegram-realtime-monitoring-design.md)
- [n8n + Whop + Telegram 統合戦略 SSOT](./n8n-whop-telegram-integration-SSOT.md)
- [TELEGRAM_API_CONTROL_VERIFIED.md](./TELEGRAM_API_CONTROL_VERIFIED.md)
- [Telegram多言語版キー設定ガイド](./telegram-multi-language-keys-setup-guide.md)

---

**最終更新**: 2025-12-26

