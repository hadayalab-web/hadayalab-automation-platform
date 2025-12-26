# アフィリエイター候補数確認計画

**作成日**: 2025-12-26
**目的**: Grok AIを使用して現状のアフィリエイター候補数を確認

---

## 🎯 確認項目

1. **X (Twitter)から抽出可能な候補数**
2. **Telegramから抽出可能な候補数**
3. **市場別（EN/AR/KO/JA/ES/PT-BR）の候補数**
4. **マッチスコア8以上の候補数**

---

## 🔧 実行方法

### スクリプト実行

```bash
cd C:\Users\chiba\hadayalab-automation-platform
python scripts\grok-x-affiliate-extraction.py
```

### 期待される出力

```
============================================================
Grok AI X + Telegram解析によるアフィリエイター候補抽出
============================================================

[STEP 1] Getting XAI_API_KEY from Infisical...
[OK] XAI_API_KEY retrieved

[INFO] Starting X (Twitter) analysis...
[INFO] Processing market: EN
...
[OK] Market EN (X): Extracted 25 candidates total

[INFO] Starting Telegram analysis...
[INFO] Processing market: EN (Telegram)
...
[OK] Market EN (Telegram): Extracted 15 candidates total

============================================================
抽出結果サマリー
============================================================
総候補数: 240
  X (Twitter): 120 候補
  Telegram: 120 候補

  EN: 40 候補 (X: 25, Telegram: 15)
  AR: 35 候補 (X: 20, Telegram: 15)
  KO: 30 候補 (X: 18, Telegram: 12)
  JA: 45 候補 (X: 25, Telegram: 20)
  ES: 45 候補 (X: 25, Telegram: 20)
  PT_BR: 45 候補 (X: 25, Telegram: 20)
```

---

## ⚠️ 注意事項

### Infisical API Key取得

**問題**: Infisical CLIで403エラーが発生する場合があります。

**回避策**:
1. 環境変数から直接取得（`XAI_API_KEY`環境変数を設定）
2. Infisical CLIの再認証
3. トークンの再生成

### Rate Limit対策

- Grok AI API呼び出し間に2秒待機
- 6市場 × 2プラットフォーム（X + Telegram）= 12回の解析
- 各市場で複数クエリ実行（X: 8クエリ、Telegram: 5クエリ）

**総API呼び出し数**: 約50-100回（クエリ数による）

---

## 📊 結果の解釈

### 期待される候補数

**予測**:
- **総候補数**: 200-500人（市場・プラットフォームによる）
- **マッチスコア8以上**: 50-150人（約30%）
- **Telegram DM可能な候補**: 全候補（Telegram一本足打法）

### 次のステップ

1. **候補数が100人以上**:
   - 週次実行を開始
   - Cold Outreach Wave 1（50人）を開始

2. **候補数が50-100人**:
   - 候補リストを充実化
   - 2週間後に再実行

3. **候補数が50人未満**:
   - 検索クエリを拡張
   - 新しいプラットフォーム（Reddit等）を追加

---

## 🔗 関連ドキュメント

- [grok-x-affiliate-extraction-design.md](./grok-x-affiliate-extraction-design.md)
- [affiliate-candidate-approach-optimal-strategy.md](./affiliate-candidate-approach-optimal-strategy.md)

---

**最終更新**: 2025-12-26
**ステータス**: 🚧 実行待ち

