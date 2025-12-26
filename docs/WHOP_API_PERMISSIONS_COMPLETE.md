# Whop API 権限完全リスト

**作成日**: 2025-12-26
**最終更新**: 2025-12-26
**出典**: Whop Dashboard → Developer → API Keys

---

## 📋 概要

このドキュメントは、Whop APIで利用可能なすべての権限をカテゴリー別にまとめた完全な一覧です。
現在のAPI Keyに付与されている権限を管理・確認する際に参照してください。

---

## 🔍 権限カテゴリー別一覧

### 1. Products（製品）

- `Export products` - 製品のエクスポート
- `Read products` - 製品の読み取り
- `Manage product control center settings` - 製品コントロールセンター設定の管理
- `Create products` - 製品の作成
- `Delete products` - 製品の削除
- `Export product statistics` - 製品統計のエクスポート
- `Read product statistics` - 製品統計の読み取り
- `Update products` - 製品の更新

### 2. Ad Campaigns（広告キャンペーン）

- `ad_campaign:conversion:create` - 広告キャンペーンコンバージョンの作成
- `ad_campaign:create` - 広告キャンペーンの作成
- `ad_campaign:credit:create` - 広告キャンペーンクレジットの作成
- `ad_campaign:read` - 広告キャンペーンの読み取り
- `ad_campaign:update` - 広告キャンペーンの更新
- `ad_publisher:read` - 広告パブリッシャーの読み取り

### 3. Affiliates（アフィリエイト）

- `Read affiliates` - アフィリエイトの読み取り
- `Create affiliates` - アフィリエイトの作成
- `Update affiliates` - アフィリエイトの更新

### 4. Authorization（認可）

- `authorized_role:create` - 認可ロールの作成

### 5. Apps（アプリ）

- `Read app permissions` - アプリ権限の読み取り
- `Create apps` - アプリの作成
- `Manage OAuth settings` - OAuth設定の管理
- `Manage webhooks` - Webhookの管理
- `Manage app builds` - アプリビルドの管理
- `Update apps` - アプリの更新
- `Attach apps to products` - アプリを製品にアタッチ
- `Delete apps` - アプリの削除
- `Detach apps from products` - アプリを製品からデタッチ
- `Read hidden apps` - 非表示アプリの読み取り

### 6. Chat（チャット）

- `Manage chat webhooks` - チャットWebhookの管理
- `Moderate chats` - チャットのモデレート
- `Read chat messages` - チャットメッセージの読み取り
- `Read chats` - チャットの読み取り

### 7. Forum（フォーラム）

- `Create forum posts` - フォーラム投稿の作成
- `Read forum posts` - フォーラム投稿の読み取り
- `Moderate forum posts` - フォーラム投稿のモデレート

### 8. Team（チーム）

- `Read team members` - チームメンバーの読み取り
- `Read team member emails` - チームメンバーのメールアドレスの読み取り

### 9. Company（会社）

- `Read company balance` - 会社残高の読み取り
- `Read logs` - ログの読み取り
- `Manage checkout settings` - チェックアウト設定の管理
- `Manage legal settings` - 法的設定の管理
- `Read business information` - ビジネス情報の読み取り
- `Update business details` - ビジネス詳細の更新
- `company:create_child` - 子会社の作成
- `company:update_child_fees` - 子会社手数料の更新
- `child_company:basic:export` - 子会社基本情報のエクスポート
- `Update social links` - ソーシャルリンクの更新
- `custom_emoji:update` - カスタム絵文字の更新

### 10. Content Rewards（コンテンツ報酬）

- `Export content rewards` - コンテンツ報酬のエクスポート
- `Read content rewards` - コンテンツ報酬の読み取り
- `Create content rewards` - コンテンツ報酬の作成
- `Delete content rewards` - コンテンツ報酬の削除
- `Moderate content reward submissions` - コンテンツ報酬提出のモデレート
- `Update content rewards` - コンテンツ報酬の更新

### 11. Developer（開発者）

- `Read developer settings` - 開発者設定の読み取り

### 12. Livestreams（ライブストリーム）

- `Create livestreams` - ライブストリームの作成
- `Delete livestreams` - ライブストリームの削除
- `Manage livestream recordings` - ライブストリーム録画の管理
- `Read livestream chat` - ライブストリームチャットの読み取り
- `Moderate livestreams` - ライブストリームのモデレート

### 13. Members（メンバー）

- `Export members` - メンバーのエクスポート
- `Read members` - メンバーの読み取り
- `Read member emails` - メンバーのメールアドレスの読み取り
- `Read member phone numbers` - メンバーの電話番号の読み取り
- `Read member payment methods` - メンバーの支払い方法の読み取り
- `Manage members` - メンバーの管理
- `Update memberships` - メンバーシップの更新
- `Moderate members` - メンバーのモデレート
- `Export member statistics` - メンバー統計のエクスポート
- `Read member statistics` - メンバー統計の読み取り

### 14. Payments（支払い）

- `Export payments` - 支払いのエクスポート
- `Read payments` - 支払いの読み取り
- `payment:charge` - 支払いのチャージ
- `payment:dispute` - 支払いの紛争
- `Export disputes` - 紛争のエクスポート
- `Read disputes` - 紛争の読み取り
- `payment:setup_intent:read` - セットアップインテントの読み取り
- `Manage payments` - 支払いの管理
- `payment:resolution_center` - 解決センター
- `Export resolution center cases` - 解決センターケースのエクスポート
- `Read resolution center cases` - 解決センターケースの読み取り

### 15. Payouts（支払い送金）

- `Create payout destinations` - 支払い送金先の作成
- `Delete payout destinations` - 支払い送金先の削除
- `Read payout destinations` - 支払い送金先の読み取り
- `Transfer funds` - 資金の転送
- `Read transfers` - 転送の読み取り
- `payout:transfer:export` - 転送のエクスポート
- `Update payout destinations` - 支払い送金先の更新
- `Withdraw funds` - 資金の引き出し
- `Read withdrawals` - 引き出しの読み取り
- `payout:withdrawal:export` - 引き出しのエクスポート
- `Read payout accounts` - 支払い送金アカウントの読み取り
- `Update payout accounts` - 支払い送金アカウントの更新

### 16. Plans（プラン）

- `Export plans` - プランのエクスポート
- `Read plans` - プランの読み取り
- `Create plans` - プランの作成
- `Delete plans` - プランの削除
- `Export plan statistics` - プラン統計のエクスポート
- `Read plan statistics` - プラン統計の読み取り
- `Update plans` - プランの更新

### 17. Waitlist Entries（ウェイトリストエントリー）✅ 現在付与済み

- `Manage waitlist entries` - ウェイトリストエントリーの管理
- `Export waitlist entries` - ウェイトリストエントリーのエクスポート
- `Read waitlist entries` - ウェイトリストエントリーの読み取り
- `Read changes to waitlist entries` - ウェイトリストエントリーの変更履歴の読み取り

### 18. Promo Codes（プロモコード）

- `Export promo codes` - プロモコードのエクスポート
- `Read promo codes` - プロモコードの読み取り
- `Create promo codes` - プロモコードの作成
- `Delete promo codes` - プロモコードの削除
- `Update promo codes` - プロモコードの更新

### 19. Statistics（統計）

- `stats:read` - 統計の読み取り

### 20. Support（サポート）

- `Read support chats` - サポートチャットの読み取り
- `Create support chats` - サポートチャットの作成
- `Send messages in support chats` - サポートチャットへのメッセージ送信

### 21. Tracking Links（トラッキングリンク）

- `Export tracking links` - トラッキングリンクのエクスポート
- `Read tracking links` - トラッキングリンクの読み取り
- `Create tracking links` - トラッキングリンクの作成
- `Delete tracking links` - トラッキングリンクの削除
- `Export tracking link statistics` - トラッキングリンク統計のエクスポート
- `Read tracking link statistics` - トラッキングリンク統計の読み取り
- `Update tracking links` - トラッキングリンクの更新

### 22. Courses（コース）

- `Read courses` - コースの読み取り
- `Update courses` - コースの更新
- `Read student-lesson interactions` - 学生-レッスンインタラクションの読み取り
- `Read course analytics` - コース分析の読み取り
- `Read changes to courses` - コースの変更履歴の読み取り

### 23. Leads（リード）

- `Read leads` - リードの読み取り
- `Export leads` - リードのエクスポート

### 24. Invoices（請求書）

- `Create invoices` - 請求書の作成
- `Read invoices` - 請求書の読み取り
- `Export invoices` - 請求書のエクスポート
- `Update invoices` - 請求書の更新
- `Read changes to invoices` - 請求書の変更履歴の読み取り

### 25. Webhooks（Webhook）

- `webhook_receive:setup_intents` - セットアップインテントのWebhook受信
- `webhook_receive:withdrawals` - 引き出しのWebhook受信

### 26. Change Tracking（変更追跡）

- `Read changes to memberships` - メンバーシップの変更履歴の読み取り
- `Read changes to payments` - 支払いの変更履歴の読み取り
- `Read changes to refunds` - 返金の変更履歴の読み取り
- `Read changes to disputes` - 紛争の変更履歴の読み取り
- `Read changes to resolution center cases` - 解決センターケースの変更履歴の読み取り
- `Read changes to app payments` - アプリ支払いの変更履歴の読み取り
- `Read changes to app memberships` - アプリメンバーシップの変更履歴の読み取り

### 27. Shipments（出荷）

- `Create shipments` - 出荷の作成
- `Read shipments` - 出荷の読み取り

### 28. Checkout（チェックアウト）

- `Read checkout configurations` - チェックアウト設定の読み取り
- `Create checkout configurations` - チェックアウト設定の作成
- `Delete checkout configurations` - チェックアウト設定の削除
- `Create checkout requests` - チェックアウトリクエストの作成
- `Read checkout requests` - チェックアウトリクエストの読み取り

### 29. Airdrop Links（エアドロップリンク）

- `airdrop_link:basic:read` - エアドロップリンク基本情報の読み取り
- `airdrop_link:manage` - エアドロップリンクの管理

---

## ✅ 現在付与されている権限

**API Key**: `apik_KbyD0T3ENibNW_C...` (hadayalab-automation-platform)

**付与されている権限**:

1. **Waitlist Entries（ウェイトリストエントリー）**
   - ✅ `Manage waitlist entries`
   - ✅ `Export waitlist entries`
   - ✅ `Read waitlist entries`
   - ✅ `Read changes to waitlist entries`

---

## 🎯 主要機能別権限要件

### アフィリエイター管理

**必要な権限**:
- `Read affiliates` - アフィリエイターの読み取り
- `Create affiliates` - アフィリエイターの作成
- `Update affiliates` - アフィリエイターの更新

**現在の状況**: ⚠️ 未確認

### アフィリエイター候補管理（Waitlist Entries）

**必要な権限**:
- ✅ `Manage waitlist entries` - **付与済み**
- ✅ `Export waitlist entries` - **付与済み**
- ✅ `Read waitlist entries` - **付与済み**
- ✅ `Read changes to waitlist entries` - **付与済み**

**現在の状況**: ✅ **すべて付与済み**

### メンバーシップ管理

**必要な権限**:
- `Read members` - メンバーの読み取り
- `Manage members` - メンバーの管理
- `Update memberships` - メンバーシップの更新

**現在の状況**: ⚠️ 未確認

### 製品管理

**必要な権限**:
- `Read products` - 製品の読み取り
- `Create products` - 製品の作成
- `Update products` - 製品の更新
- `Delete products` - 製品の削除

**現在の状況**: ⚠️ 未確認

### プラン管理

**必要な権限**:
- `Read plans` - プランの読み取り
- `Create plans` - プランの作成
- `Update plans` - プランの更新
- `Delete plans` - プランの削除

**現在の状況**: ⚠️ 未確認

### 支払い管理

**必要な権限**:
- `Read payments` - 支払いの読み取り
- `Manage payments` - 支払いの管理

**現在の状況**: ⚠️ 未確認

### Webhook管理

**必要な権限**:
- `Manage webhooks` - Webhookの管理

**現在の状況**: ⚠️ 未確認

---

## 📊 権限統計

- **総権限数**: 152
- **カテゴリー数**: 29
- **現在付与済み**: 4（Waitlist Entries関連）

---

## 🔗 関連ドキュメント

- [WHOP_API_CAPABILITIES_COMPLETE.md](./WHOP_API_CAPABILITIES_COMPLETE.md) - Whop API完全機能一覧
- [whop-waitlist-entries-analysis.md](./whop-waitlist-entries-analysis.md) - Waitlist Entries機能分析
- [n8n-whop-full-strategy-SSOT.md](./n8n-whop-full-strategy-SSOT.md) - n8n + Whop完全活用戦略SSOT

---

**最終更新**: 2025-12-26
**ステータス**: ✅ 権限リスト完全版

