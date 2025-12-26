# CryptoTrade Academy - n8n自動化実装ガイド

## 📋 概要

このプロジェクトは、3つの戦略ドキュメントに基づいて、Make.comの記述をn8nに置き換えて実装した自動化ワークフローのセットです。

### 参照ドキュメント
1. **Creative Execution Master Guide v1.0** - Whop/Make/HeyGen/Adobe完全実装
2. **Sales Strategy Doping v2.0 FINAL** - セールス戦略理論実装
3. **Zero-Budget Affiliate DRM Strategy v1.1 + APDS v1.0** - アフィリエイト戦略

### Make.com → n8n 置き換え
- Make.comのすべての記述をn8nに置き換え
- 同等の機能をn8nノードで実装
- ワークフローを複数に分割して設計

---

## 🚀 実装されたワークフロー

### 1. Trial Onboarding Automation
**目的**: 1-Day Free Trialの完全自動化（Nudge Feedback Loop実装）

**機能**:
- Whop Trial開始Webhook受信
- 6市場別（EN/AR/KO/JA/ES/PT-BR）分岐
- Welcome Email即座送信
- 6時間後: Value Email送信
- 18時間後: Trial終了通知
- 課金状況確認 → Thank You / Feedback Request Email

**ファイル**: `workflow-1-trial-onboarding.json`

### 2. Affiliate Auto-Management
**目的**: 3-Tier Affiliate自動昇格（Growth Engine v1.2実装）

**機能**:
- Whop Affiliate Conversion Webhook受信
- Google SheetsからAffiliate Performance読み込み
- Tier判定（50+ = Tier 1, 20+ = Tier 2, <20 = Tier 3）
- Congratulations Email送信
- Whop APIでTier更新
- Google Sheets更新

**設計**: `n8n-workflows-design.md` 参照

### 3. Emergency Briefing Trigger
**目的**: イベント駆動配信トリガー（Technical Supplement v2.0連動）

**機能**:
- Vercel Emergency Trigger Webhook受信
- 6市場別分岐
- Telegram並列配信（30秒間隔でRate Limit対策）
- EMERGENCY判定 → 60秒以内全市場配信完了

**設計**: `n8n-workflows-design.md` 参照

### 4. Affiliate DRM Cold Outreach
**目的**: アフィリエイター獲得Cold Outreach自動化

**機能**:
- 週次スケジュール実行
- Google SheetsからAffiliate List読み込み
- Email Template選択（Fan/Partnership/Gift Approach）
- Cold Email送信
- Follow-Up自動化（Day 4, 8, 15）

**設計**: `n8n-workflows-design.md` 参照

### 5. Affiliate Performance Tracking
**目的**: Affiliate Performance Dashboard自動更新（APDS v1.0実装）

**機能**:
- 週次スケジュール実行
- Whop APIからAffiliate Stats取得
- Click Source別 / Content Type別集計
- Google Sheets Dashboard更新
- Recommendations生成
- Weekly Report Email送信

**設計**: `n8n-workflows-design.md` 参照

---

## 📁 ファイル構成

```
.
├── README-n8n-implementation.md     # このファイル
├── n8n-workflows-design.md          # 詳細設計ドキュメント
├── workflow-1-trial-onboarding.json # ワークフロー1 JSON
└── docs/                            # 元の戦略ドキュメント
    ├── CryptoTrade Academy - Creative Execution Master Guide v1.0.md
    ├── CryptoTrade Academy - Sales Strategy Doping v2.0 FINAL.md
    └── CryptoTrade Academy - Zero-Budget Affiliate DRM Strategy v1.1 + APDS v1.0.md
```

---

## 🛠️ セットアップ手順

### 1. n8nインスタンス準備
- n8n Cloud または Self-hosted インスタンス
- バージョン: 2.30.2以上推奨

### 2. 認証情報設定

#### Gmail OAuth2
1. n8n Dashboard → Credentials → Add Credential
2. Gmail OAuth2 API を選択
3. Google Cloud ConsoleでOAuth2認証情報を作成
4. Client ID / Client Secret を入力

#### Telegram Bot Token
1. @BotFather でBot作成
2. Bot Tokenを取得
3. n8n Credentials → Telegram → Bot Token入力
4. 6市場分（EN/AR/KO/JA/ES/PT-BR）のBot Tokenが必要

#### Google Sheets OAuth2
1. n8n Credentials → Google Sheets OAuth2 API
2. Google Cloud Consoleで認証情報作成
3. Client ID / Client Secret を入力

#### Whop API Key
1. Whop Dashboard → API Settings
2. API Keyを生成
3. n8n Credentials → HTTP Request → Generic Credential Type
4. Header: `Authorization: Bearer YOUR_WHOP_API_KEY`

### 3. ワークフローインポート

#### 方法1: JSONファイルからインポート
1. n8n Dashboard → Workflows → Import from File
2. `workflow-1-trial-onboarding.json` を選択
3. 認証情報を設定（Gmail, Whop API）
4. 各ノードのパラメータを確認・調整

#### 方法2: 手動作成
1. `n8n-workflows-design.md` を参照
2. 各ノードを手動で追加
3. 接続を設定
4. パラメータを設定

### 4. 環境変数設定

#### Whop Webhook URL取得
1. ワークフロー1を有効化
2. Webhook Triggerノードを開く
3. Webhook URLをコピー
4. Whop Dashboard → Settings → Webhooks に設定
   - Event: `membership.trial_started`
   - URL: n8n Webhook URL

#### Vercel Webhook URL取得
1. ワークフロー3を有効化
2. Webhook Triggerノードを開く
3. Webhook URLをコピー
4. Vercel `api/cron.js` に設定

### 5. Google Sheets準備

#### Affiliate Performance Tracker
列構成:
- affiliate_id
- monthly_conversions
- current_tier
- lifetime_conversions
- commission

#### Affiliate List
列構成:
- Name
- Email
- Platform
- Profile URL
- Status (Pending/Active/Inactive)
- Template Preference (A/B/C)
- Recent Topic
- Outreach Date
- Response

---

## 🔧 カスタマイズ

### Email Template編集
各Gmail Nodeの `message` パラメータを編集:
- HTML形式で記述
- `{{ $json.body.user_name }}` などの変数を使用
- 市場別に異なるTemplateを設定可能

### 待機時間調整
Wait Nodeの `amount` と `unit` を変更:
- 6時間 → 3時間に短縮可能
- 12時間 → 18時間に延長可能

### 市場追加
Market Router (Switch Node) に新しい条件を追加:
- 新しい市場コード（例: "FR"）
- 対応するEmail Template作成

---

## 📊 監視と最適化

### エラーログ確認
1. n8n Dashboard → Executions
2. 失敗した実行を確認
3. エラーメッセージを確認
4. ノードを修正

### パフォーマンス測定
- 実行時間: n8n Executionsで確認
- Email送信率: Gmail送信ログで確認
- Webhook受信率: n8n Webhook Logで確認

### 改善ポイント
1. **Wait Node最適化**: 長時間待機はResume URL使用を検討
2. **並列処理**: Switch Nodeの各ブランチは並列実行
3. **エラーハンドリング**: Try-Catch Node追加を検討

---

## 🎯 実装優先順位

### Phase 1 (即実装)
1. ✅ **Trial Onboarding Automation** - 最重要
2. ⏳ **Emergency Briefing Trigger** - コア機能

### Phase 2 (1週間以内)
3. ⏳ **Affiliate Auto-Management** - Tier管理自動化
4. ⏳ **Affiliate DRM Cold Outreach** - 獲得自動化

### Phase 3 (1ヶ月以内)
5. ⏳ **Affiliate Performance Tracking** - 最適化支援

---

## 📚 参考資料

### n8n公式ドキュメント
- [Webhook Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)
- [Gmail Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.gmail/)
- [Telegram Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.telegram/)
- [Google Sheets Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.googlesheets/)
- [Wait Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait/)

### 戦略ドキュメント
- `docs/CryptoTrade Academy - Creative Execution Master Guide v1.0.md`
- `docs/CryptoTrade Academy - Sales Strategy Doping v2.0 FINAL.md`
- `docs/CryptoTrade Academy - Zero-Budget Affiliate DRM Strategy v1.1 + APDS v1.0.md`

---

## ⚠️ 注意事項

### セキュリティ
- API Keyは環境変数またはn8n Credentialsで管理
- Webhook URLはHTTPS必須
- Gmail認証はOAuth2推奨（パスワード認証非推奨）

### レート制限
- Gmail: 1日500通制限
- Telegram: 30メッセージ/秒
- Whop API: レート制限確認要

### コスト
- n8n Cloud: プランに応じた実行回数制限
- Self-hosted: サーバーリソース使用

---

## 🐛 トラブルシューティング

### Webhookが受信できない
1. Webhook URLが正しいか確認
2. n8nワークフローがActiveか確認
3. Whop/Vercel側のWebhook設定確認

### Email送信失敗
1. Gmail認証情報確認
2. 送信先Emailアドレス確認
3. Gmail送信制限確認（1日500通）

### Wait Nodeが動作しない
1. n8nインスタンスが継続実行中か確認
2. Resume URL方式への変更を検討

---

## 📞 サポート

### ドキュメント
- 詳細設計: `n8n-workflows-design.md`
- 戦略ドキュメント: `docs/` フォルダ

### 次のステップ
1. ワークフロー1から順次実装
2. テスト実行で動作確認
3. 本番環境で有効化
4. 監視と最適化

---

**作成日**: 2025-01-XX
**バージョン**: 1.0
**ステータス**: 設計完了 - 実装準備完了





















