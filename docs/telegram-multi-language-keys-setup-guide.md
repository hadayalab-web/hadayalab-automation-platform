# Telegram多言語版キー設定ガイド

**作成日**: 2025-12-26
**目的**: 6市場別Telegram Bot Token/Chat IDをInfisicalに設定

---

## 📋 必要なキー

### 6市場別キー

| 市場 | Bot Token Key | Chat ID Key |
|------|---------------|-------------|
| EN | `TELEGRAM_BOT_TOKEN_EN` | `TELEGRAM_CHAT_ID_EN` |
| AR | `TELEGRAM_BOT_TOKEN_AR` | `TELEGRAM_CHAT_ID_AR` |
| KO | `TELEGRAM_BOT_TOKEN_KO` | `TELEGRAM_CHAT_ID_KO` |
| JA | `TELEGRAM_BOT_TOKEN_JA` | `TELEGRAM_CHAT_ID_JA` |
| ES | `TELEGRAM_BOT_TOKEN_ES` | `TELEGRAM_CHAT_ID_ES` |
| PT-BR | `TELEGRAM_BOT_TOKEN_PT_BR` | `TELEGRAM_CHAT_ID_PT_BR` |

**合計**: 12個のキー（6市場 × 2種類）

---

## 🔑 Bot Token取得方法

### ステップ1: @BotFatherでBot作成

1. Telegramで@BotFatherを開く
2. `/newbot` コマンドを送信
3. Bot名を入力（例: `CryptoTrade Academy EN Bot`）
4. Bot usernameを入力（例: `cryptotrade_academy_en_bot`）
5. Bot Tokenを取得（例: `8155351788:AAGS0S1Bnuw8Ma4TH_C...`）

### ステップ2: チャンネルにBot追加

1. 各市場のTelegramチャンネルを開く
2. Channel Settings → Administrators → Add Administrator
3. BotをAdminとして追加
4. 権限設定:
   - ✅ Post Messages
   - ✅ Edit Messages（オプション）
   - ✅ Delete Messages（オプション）

### ステップ3: Chat ID取得方法

#### 方法1: チャンネル情報から取得

1. Botをチャンネルに追加後、Botにメッセージを送信
2. `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates` にアクセス
3. `chat.id` を確認（例: `-1003223165053`）

#### 方法2: @userinfobotを使用

1. チャンネルに@userinfobotを追加
2. Botが返すメッセージからChat IDを確認

#### 方法3: Telegram API使用

```bash
curl https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
```

---

## 🔧 Infisical設定方法

### コマンドライン設定

```bash
# Infisical設定
INFISICAL_TOKEN="your_infisical_token"
PROJECT_ID="446f131c-be8d-45e5-a83a-4154e34501a5"

# EN市場のBot Token設定
infisical secrets set TELEGRAM_BOT_TOKEN_EN "8155351788:AAGS0S1Bnuw8Ma4TH_C..." \
  --token $INFISICAL_TOKEN \
  --projectId $PROJECT_ID

# EN市場のChat ID設定
infisical secrets set TELEGRAM_CHAT_ID_EN "-1003223165053" \
  --token $INFISICAL_TOKEN \
  --projectId $PROJECT_ID

# 他の市場も同様に設定
# AR, KO, JA, ES, PT_BR
```

### 一括設定スクリプト

`scripts/setup-telegram-multi-language-keys-batch.sh` を作成（オプション）

---

## ✅ 設定確認

### 確認スクリプト実行

```bash
cd hadayalab-automation-platform
python scripts/verify-telegram-multi-language-keys.py
```

**期待される出力**:
- ✅ 各市場のBot Token: `✅ [token_preview]...`
- ✅ 各市場のChat ID: `✅ [chat_id]`
- ✅ Bot Token有効: `6/6 市場`
- ✅ Chat ID有効: `6/6 市場`

---

## 📊 現在の設定状況

### メインチャンネル（EN市場）

**現在設定済み**:
- ✅ `TELEGRAM_BOT_TOKEN`: `8155351788:AAGS0S1Bn...`
  - Bot Username: `@CryptoSignal_AI_Official_bot`
  - Bot Name: `CryptoSignal AI EN`
- ✅ `TELEGRAM_CHAT_ID`: `-1003223165053`
  - Chat Title: `CryptoSignal AI – Starter Signals (EN)`
  - Chat Type: `supergroup`

**注意**: メインチャンネルは`TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`として設定済み。
他の市場は`TELEGRAM_BOT_TOKEN_*`/`TELEGRAM_CHAT_ID_*`として個別に設定する必要があります。

---

## 🔄 設定後の動作確認

### 1. Bot Token検証

```python
from scripts.telegram_channel_control import get_secret_from_infisical, get_bot_info

bot_token = get_secret_from_infisical("TELEGRAM_BOT_TOKEN_EN")
bot_info = get_bot_info(bot_token)
print(f"Bot Username: @{bot_info.get('username')}")
```

### 2. チャンネルアクセス検証

```python
from scripts.telegram_channel_control import get_chat_info

chat_id = get_secret_from_infisical("TELEGRAM_CHAT_ID_EN")
chat_info = get_chat_info(bot_token, chat_id)
print(f"Chat Title: {chat_info.get('title')}")
```

### 3. メッセージ送信テスト

```python
from scripts.telegram_channel_control import send_message

result = send_message(
    bot_token,
    chat_id,
    "🤖 Test message from n8n automation platform"
)
print(f"Message ID: {result.get('message_id')}")
```

---

## 🔗 関連ドキュメント

- [Telegram API制御確認済みレポート](./TELEGRAM_API_CONTROL_VERIFIED.md)
- [n8n + Whop + Telegram 統合戦略 SSOT](./n8n-whop-telegram-integration-SSOT.md)
- [Infisical設定ガイド](./infisical-setup.md)

---

**最終更新**: 2025-12-26

