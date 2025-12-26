# アフィリエイター候補抽出スクリプト 実行状況

**作成日**: 2025-12-26
**目的**: Grok AIを使用してX + Telegramからアフィリエイター候補を抽出

---

## ⚠️ 現在の状況

### APIエンドポイントとモデル名の修正完了

**修正内容**:
1. ✅ `MARKET_TELEGRAM_SEARCH_QUERIES`の定義を追加（6市場分）
2. ✅ APIエンドポイント: `https://api.x.ai/v1/chat/completions`（正しい形式）
3. ✅ モデル名: `grok-4-0709`（cryptosignal-aiと同じ）
4. ✅ 環境変数からのAPI Key取得に対応

---

## 🚀 実行方法

### 1. XAI_API_KEYの設定

**方法1: ファイルから取得（現在の方法）**:
```powershell
$apiKeyContent = Get-Content "C:\Users\chiba\Downloads\XAI_API_KEY.txt" -Raw
$apiKey = ($apiKeyContent -split "`n" | Select-Object -Skip 1 -First 1).Trim()
$env:XAI_API_KEY = $apiKey
```

**方法2: 環境変数として直接設定**:
```powershell
$env:XAI_API_KEY = "xai-xxxxxxxxxxxxx"
```

---

### 2. スクリプト実行

```powershell
cd C:\Users\chiba\hadayalab-automation-platform
python scripts\grok-x-affiliate-extraction.py
```

---

## 📊 期待される結果

### 抽出対象

**X (Twitter)**: 6市場 × 4-8クエリ = 約30-50クエリ
**Telegram**: 6市場 × 3クエリ = 18クエリ

**総API呼び出し数**: 約50-70回

### 予測候補数

**総候補数**: 200-500人
- X (Twitter): 100-250人
- Telegram: 100-250人

**市場別内訳**:
- EN: 40-80人
- AR: 30-60人
- KO: 30-60人
- JA: 40-80人
- ES: 40-80人
- PT-BR: 40-80人

**マッチスコア8以上**: 50-150人（約30%）

---

## ⚠️ 注意事項

### API Rate Limit

- Grok AI API呼び出し間に2秒待機を実装
- 総API呼び出し数が多い場合、実行時間が長くなる可能性

### モデル名について

- `grok-4-0709`: Reasoningモデル（デフォルト）
- X検索機能は`grok-beta`モデルで使用可能だが、本スクリプトでは`grok-4-0709`を使用

---

## 🔗 関連ドキュメント

- [grok-x-affiliate-extraction-design.md](./grok-x-affiliate-extraction-design.md)
- [grok-telegram-affiliate-extraction-design.md](./grok-telegram-affiliate-extraction-design.md)
- [affiliate-candidate-approach-optimal-strategy.md](./affiliate-candidate-approach-optimal-strategy.md)
- [affiliate-outreach-enhancement-with-samples.md](./affiliate-outreach-enhancement-with-samples.md)

---

**最終更新**: 2025-12-26
**ステータス**: ✅ スクリプト修正完了、実行準備完了

