# Whop API 完全機能一覧

**作成日**: 2025-12-26
**最終更新**: 2025-12-26
**参照元**: [Whop API Documentation](https://docs.whop.com/api-reference)

---

## 📋 概要

このドキュメントは、Whop APIで利用可能なすべての機能をカテゴリー別にまとめた完全な一覧です。
Whop側の設定ですべてのAPIが有効になっている場合、以下のすべての操作が可能です。

---

## 🔐 認証

### APIキー認証
- **Authorization Header**: `Bearer YOUR_API_KEY`
- **取得先**: Whop Dashboard → Developer → API Keys
- **権限**: 各エンドポイントごとに必要な権限が異なる

---

## 1. Payins（支払い受信）

### 1.1 Products（製品）
- ✅ **GET** `/products` - 製品一覧取得
- ✅ **POST** `/products` - 製品作成
- ✅ **GET** `/products/{product_id}` - 製品詳細取得
- ✅ **PATCH** `/products/{product_id}` - 製品更新
- ✅ **DELETE** `/products/{product_id}` - 製品削除

**用途**:
- 製品情報の管理
- 製品の作成・更新・削除
- 製品リストの取得

### 1.2 Plans（プラン）
- **GET** `/plans` - プラン一覧取得
- **POST** `/plans` - プラン作成
- **GET** `/plans/{plan_id}` - プラン詳細取得
- **PATCH** `/plans/{plan_id}` - プラン更新
- **DELETE** `/plans/{plan_id}` - プラン削除

**用途**:
- サブスクリプションプランの管理
- 価格設定
- プランの作成・更新・削除

### 1.3 Payments（支払い）
- **GET** `/payments` - 支払い一覧取得
- **POST** `/payments` - 支払い作成
- **GET** `/payments/{payment_id}` - 支払い詳細取得

**用途**:
- 支払い履歴の確認
- 支払い処理
- 支払い情報の取得

### 1.4 Refunds（返金）
- **GET** `/refunds` - 返金一覧取得
- **POST** `/refunds` - 返金作成
- **GET** `/refunds/{refund_id}` - 返金詳細取得

**用途**:
- 返金処理
- 返金履歴の確認

### 1.5 Disputes（紛争）
- **GET** `/disputes` - 紛争一覧取得
- **GET** `/disputes/{dispute_id}` - 紛争詳細取得

**用途**:
- 紛争管理
- 紛争情報の確認

### 1.6 Checkout Configurations（チェックアウト設定）
- **GET** `/checkout-configurations` - チェックアウト設定一覧
- **POST** `/checkout-configurations` - チェックアウト設定作成
- **GET** `/checkout-configurations/{config_id}` - チェックアウト設定詳細
- **PATCH** `/checkout-configurations/{config_id}` - チェックアウト設定更新
- **DELETE** `/checkout-configurations/{config_id}` - チェックアウト設定削除

**用途**:
- チェックアウトページのカスタマイズ
- 支払いオプションの設定

### 1.7 Setup Intents（セットアップインテント）
- **GET** `/setup-intents` - セットアップインテント一覧
- **POST** `/setup-intents` - セットアップインテント作成
- **GET** `/setup-intents/{intent_id}` - セットアップインテント詳細

**用途**:
- 支払い方法のセットアップ
- 将来の支払いのための設定

### 1.8 Payment Methods（支払い方法）
- **GET** `/payment-methods` - 支払い方法一覧
- **POST** `/payment-methods` - 支払い方法作成
- **GET** `/payment-methods/{method_id}` - 支払い方法詳細
- **DELETE** `/payment-methods/{method_id}` - 支払い方法削除

**用途**:
- 支払い方法の管理
- クレジットカード情報の保存

### 1.9 Invoices（請求書）
- **GET** `/invoices` - 請求書一覧取得
- **GET** `/invoices/{invoice_id}` - 請求書詳細取得

**用途**:
- 請求書の発行
- 請求書履歴の確認

### 1.10 Promo Codes（プロモコード）
- **GET** `/promo-codes` - プロモコード一覧
- **POST** `/promo-codes` - プロモコード作成
- **GET** `/promo-codes/{code_id}` - プロモコード詳細
- **PATCH** `/promo-codes/{code_id}` - プロモコード更新
- **DELETE** `/promo-codes/{code_id}` - プロモコード削除

**用途**:
- 割引コードの作成・管理
- プロモーションキャンペーンの実行

---

## 2. Payouts（支払い送金）

### 2.1 Ledger Accounts（元帳アカウント）
- **GET** `/ledger-accounts` - 元帳アカウント一覧
- **GET** `/ledger-accounts/{account_id}` - 元帳アカウント詳細

**用途**:
- アカウント残高の確認
- 財務記録の管理

### 2.2 Transfers（転送）
- **GET** `/transfers` - 転送一覧取得
- **POST** `/transfers` - 転送作成
- **GET** `/transfers/{transfer_id}` - 転送詳細取得

**用途**:
- アカウント間の資金移動
- 転送履歴の確認

### 2.3 Withdrawals（引き出し）
- **GET** `/withdrawals` - 引き出し一覧取得
- **POST** `/withdrawals` - 引き出し作成
- **GET** `/withdrawals/{withdrawal_id}` - 引き出し詳細取得

**用途**:
- 資金の引き出し処理
- 引き出し履歴の確認

### 2.4 Payout Methods（支払い方法）
- **GET** `/payout-methods` - 支払い方法一覧
- **POST** `/payout-methods` - 支払い方法作成
- **GET** `/payout-methods/{method_id}` - 支払い方法詳細
- **DELETE** `/payout-methods/{method_id}` - 支払い方法削除

**用途**:
- 引き出し先の設定
- 銀行口座情報の管理

### 2.5 Topups（チャージ）
- **GET** `/topups` - チャージ一覧取得
- **POST** `/topups` - チャージ作成
- **GET** `/topups/{topup_id}` - チャージ詳細取得

**用途**:
- アカウントへの資金追加
- チャージ履歴の確認

---

## 3. Identity（身元）

### 3.1 Users（ユーザー）
- **GET** `/users` - ユーザー一覧取得
- **GET** `/users/{user_id}` - ユーザー詳細取得
- **PATCH** `/users/{user_id}` - ユーザー情報更新

**用途**:
- ユーザー情報の管理
- ユーザープロフィールの確認・更新

### 3.2 Companies（会社）
- **GET** `/companies` - 会社一覧取得
- **GET** `/companies/{company_id}` - 会社詳細取得
- **PATCH** `/companies/{company_id}` - 会社情報更新

**用途**:
- 会社情報の管理
- 会社プロフィールの確認・更新

### 3.3 Authorized Users（承認されたユーザー）
- **GET** `/authorized-users` - 承認ユーザー一覧
- **POST** `/authorized-users` - 承認ユーザー追加
- **GET** `/authorized-users/{user_id}` - 承認ユーザー詳細
- **DELETE** `/authorized-users/{user_id}` - 承認ユーザー削除

**用途**:
- アクセス権限の管理
- チームメンバーの管理

### 3.4 Fee Markups（手数料マークアップ）
- **GET** `/fee-markups` - 手数料マークアップ一覧
- **POST** `/fee-markups` - 手数料マークアップ作成
- **GET** `/fee-markups/{markup_id}` - 手数料マークアップ詳細
- **PATCH** `/fee-markups/{markup_id}` - 手数料マークアップ更新
- **DELETE** `/fee-markups/{markup_id}` - 手数料マークアップ削除

**用途**:
- 手数料設定の管理
- 価格調整の実行

---

## 4. CRM

### 4.1 Members（メンバー）
- **GET** `/members` - メンバー一覧取得
- **GET** `/members/{member_id}` - メンバー詳細取得
- **PATCH** `/members/{member_id}` - メンバー情報更新

**用途**:
- メンバー情報の管理
- メンバープロフィールの確認・更新

### 4.2 Memberships（メンバーシップ）✅ 実装済み
- ✅ **GET** `/memberships` - メンバーシップ一覧取得（実装済み）
- ✅ **GET** `/memberships/{membership_id}` - メンバーシップ詳細取得（実装済み）
- ✅ **POST** `/memberships/{membership_id}/cancel` - メンバーシップキャンセル（実装済み）
- ✅ **POST** `/memberships/{membership_id}/reactivate` - メンバーシップ再アクティブ化（実装済み）
- **PATCH** `/memberships/{membership_id}` - メンバーシップ更新（未実装）
- **POST** `/memberships` - メンバーシップ作成（未実装）
- **DELETE** `/memberships/{membership_id}` - メンバーシップ削除（未実装）

**用途**:
- サブスクリプション管理
- メンバーシップ状態の確認・更新
- キャンセル・再アクティブ化処理

**現在の実装状況**:
- `whop-control`ワークフローで4つの操作を実装済み
- Webhook URL: `https://hadayalab.app.n8n.cloud/webhook/whop-control`

### 4.3 Entries（エントリー）
- **GET** `/entries` - エントリー一覧取得
- **POST** `/entries` - エントリー作成
- **GET** `/entries/{entry_id}` - エントリー詳細取得
- **PATCH** `/entries/{entry_id}` - エントリー更新
- **POST** `/entries/{entry_id}/approve` - エントリー承認
- **DELETE** `/entries/{entry_id}` - エントリー削除

**用途**:
- アクセスリクエストの管理
- エントリー承認処理
- エントリー履歴の確認

### 4.4 Shipments（出荷）
- **GET** `/shipments` - 出荷一覧取得
- **POST** `/shipments` - 出荷作成
- **GET** `/shipments/{shipment_id}` - 出荷詳細取得
- **PATCH** `/shipments/{shipment_id}` - 出荷更新

**用途**:
- 物理商品の出荷管理
- 配送情報の追跡

### 4.5 Reviews（レビュー）
- **GET** `/reviews` - レビュー一覧取得
- **GET** `/reviews/{review_id}` - レビュー詳細取得
- **POST** `/reviews/{review_id}/approve` - レビュー承認
- **DELETE** `/reviews/{review_id}` - レビュー削除

**用途**:
- 顧客レビューの管理
- レビュー承認処理

---

## 5. Engagement（エンゲージメント）

### 5.1 Experiences（体験）
- **GET** `/experiences` - 体験一覧取得
- **POST** `/experiences` - 体験作成
- **GET** `/experiences/{experience_id}` - 体験詳細取得
- **PATCH** `/experiences/{experience_id}` - 体験更新
- **DELETE** `/experiences/{experience_id}` - 体験削除

**用途**:
- カスタム体験の作成・管理
- ユーザー体験の提供

### 5.2 Forums（フォーラム）
- **GET** `/forums` - フォーラム一覧取得
- **POST** `/forums` - フォーラム作成
- **GET** `/forums/{forum_id}` - フォーラム詳細取得
- **PATCH** `/forums/{forum_id}` - フォーラム更新
- **DELETE** `/forums/{forum_id}` - フォーラム削除

**用途**:
- コミュニティフォーラムの管理
- ディスカッションスペースの作成

### 5.3 Forum Posts（フォーラム投稿）
- **GET** `/forum-posts` - フォーラム投稿一覧
- **POST** `/forum-posts` - フォーラム投稿作成
- **GET** `/forum-posts/{post_id}` - フォーラム投稿詳細
- **PATCH** `/forum-posts/{post_id}` - フォーラム投稿更新
- **DELETE** `/forum-posts/{post_id}` - フォーラム投稿削除

**用途**:
- フォーラム投稿の管理
- コンテンツの投稿・編集

### 5.4 Chat Channels（チャットチャネル）
- **GET** `/chat-channels` - チャットチャネル一覧
- **POST** `/chat-channels` - チャットチャネル作成
- **GET** `/chat-channels/{channel_id}` - チャットチャネル詳細
- **PATCH** `/chat-channels/{channel_id}` - チャットチャネル更新
- **DELETE** `/chat-channels/{channel_id}` - チャットチャネル削除

**用途**:
- チャットチャネルの管理
- コミュニケーションスペースの作成

### 5.5 Support Channels（サポートチャネル）
- **GET** `/support-channels` - サポートチャネル一覧
- **POST** `/support-channels` - サポートチャネル作成
- **GET** `/support-channels/{channel_id}` - サポートチャネル詳細
- **PATCH** `/support-channels/{channel_id}` - サポートチャネル更新
- **DELETE** `/support-channels/{channel_id}` - サポートチャネル削除

**用途**:
- カスタマーサポートチャネルの管理
- サポートチケットの処理

### 5.6 Messages（メッセージ）
- **GET** `/messages` - メッセージ一覧取得
- **POST** `/messages` - メッセージ送信
- **GET** `/messages/{message_id}` - メッセージ詳細取得
- **DELETE** `/messages/{message_id}` - メッセージ削除

**用途**:
- メッセージの送信・受信
- チャット履歴の確認

### 5.7 Reactions（リアクション）
- **GET** `/reactions` - リアクション一覧
- **POST** `/reactions` - リアクション作成
- **DELETE** `/reactions/{reaction_id}` - リアクション削除

**用途**:
- メッセージへのリアクション
- エンゲージメントの管理

### 5.8 Notifications（通知）
- **GET** `/notifications` - 通知一覧取得
- **GET** `/notifications/{notification_id}` - 通知詳細取得
- **PATCH** `/notifications/{notification_id}/read` - 通知既読化

**用途**:
- 通知の管理
- 通知設定の制御

---

## 6. Courses（コース）

### 6.1 Courses（コース）
- **GET** `/courses` - コース一覧取得
- **POST** `/courses` - コース作成
- **GET** `/courses/{course_id}` - コース詳細取得
- **PATCH** `/courses/{course_id}` - コース更新
- **DELETE** `/courses/{course_id}` - コース削除

**用途**:
- オンラインコースの管理
- コースコンテンツの作成・更新

### 6.2 Course Chapters（コース章）
- **GET** `/course-chapters` - コース章一覧
- **POST** `/course-chapters` - コース章作成
- **GET** `/course-chapters/{chapter_id}` - コース章詳細
- **PATCH** `/course-chapters/{chapter_id}` - コース章更新
- **DELETE** `/course-chapters/{chapter_id}` - コース章削除

**用途**:
- コースの章構成管理
- 学習コンテンツの構造化

### 6.3 Course Lessons（コースレッスン）
- **GET** `/course-lessons` - コースレッスン一覧
- **POST** `/course-lessons` - コースレッスン作成
- **GET** `/course-lessons/{lesson_id}` - コースレッスン詳細
- **PATCH** `/course-lessons/{lesson_id}` - コースレッスン更新
- **DELETE** `/course-lessons/{lesson_id}` - コースレッスン削除

**用途**:
- レッスンコンテンツの管理
- 学習素材の作成・更新

### 6.4 Course Students（コース学生）
- **GET** `/course-students` - コース学生一覧
- **GET** `/course-students/{student_id}` - コース学生詳細
- **PATCH** `/course-students/{student_id}` - コース学生情報更新

**用途**:
- 学生の進捗管理
- 学習状況の確認

### 6.5 Course Lesson Interactions（コースレッスンのインタラクション）
- **GET** `/course-lesson-interactions` - インタラクション一覧
- **POST** `/course-lesson-interactions` - インタラクション作成
- **GET** `/course-lesson-interactions/{interaction_id}` - インタラクション詳細

**用途**:
- 学習活動の追跡
- エンゲージメント分析

---

## 7. Developer（開発者）

### 7.1 Apps（アプリ）
- **GET** `/apps` - アプリ一覧取得
- **POST** `/apps` - アプリ作成
- **GET** `/apps/{app_id}` - アプリ詳細取得
- **PATCH** `/apps/{app_id}` - アプリ更新
- **DELETE** `/apps/{app_id}` - アプリ削除

**用途**:
- カスタムアプリの管理
- アプリ開発の統合

### 7.2 App Builds（アプリビルド）
- **GET** `/app-builds` - アプリビルド一覧
- **POST** `/app-builds` - アプリビルド作成
- **GET** `/app-builds/{build_id}` - アプリビルド詳細

**用途**:
- アプリビルドの管理
- デプロイメントの追跡

### 7.3 Access Tokens（アクセストークン）
- **GET** `/access-tokens` - アクセストークン一覧
- **POST** `/access-tokens` - アクセストークン作成
- **DELETE** `/access-tokens/{token_id}` - アクセストークン削除

**用途**:
- APIアクセスの管理
- トークンの生成・削除

### 7.4 Account Links（アカウントリンク）
- **GET** `/account-links` - アカウントリンク一覧
- **POST** `/account-links` - アカウントリンク作成
- **GET** `/account-links/{link_id}` - アカウントリンク詳細
- **DELETE** `/account-links/{link_id}` - アカウントリンク削除

**用途**:
- 外部アカウントとの連携
- OAuth統合の管理

---

## 8. Webhooks

### 8.1 Webhook Events（Webhookイベント）

Whopは以下のイベントをWebhookとして送信可能：

- `membership.created` - メンバーシップ作成時
- `membership.updated` - メンバーシップ更新時
- `membership.cancelled` - メンバーシップキャンセル時
- `membership.reactivated` - メンバーシップ再アクティブ化時
- `membership.trial_started` - トライアル開始時
- `payment.created` - 支払い作成時
- `payment.succeeded` - 支払い成功時
- `payment.failed` - 支払い失敗時
- `refund.created` - 返金作成時
- `entry.approved` - エントリー承認時
- `entry.rejected` - エントリー拒否時

**用途**:
- リアルタイムイベントの受信
- 自動化ワークフローのトリガー

**設定方法**:
- Whop Dashboard → Settings → Webhooks
- Webhook URLを設定（例: `https://hadayalab.app.n8n.cloud/webhook/whop-events`）

---

## 📊 現在の実装状況

### ✅ 実装済み（whop-controlワークフロー）

| 機能 | エンドポイント | ステータス |
|------|---------------|----------|
| メンバーシップ一覧取得 | `GET /memberships` | ✅ 実装済み |
| メンバーシップ詳細取得 | `GET /memberships/{id}` | ✅ 実装済み |
| メンバーシップキャンセル | `POST /memberships/{id}/cancel` | ✅ 実装済み |
| メンバーシップ再アクティブ化 | `POST /memberships/{id}/reactivate` | ✅ 実装済み |

**ワークフロー**: `whop-control`
**Webhook URL**: `https://hadayalab.app.n8n.cloud/webhook/whop-control`
**n8n URL**: https://hadayalab.app.n8n.cloud/workflow/3LYMmEXrRpSVhuhE

### 🚧 優先実装候補

#### 高優先度
1. **Products管理** - 製品情報の取得・更新
2. **Plans管理** - プラン情報の取得・更新
3. **Affiliates管理** - アフィリエイト情報の取得・更新
4. **Entries管理** - エントリー承認処理
5. **Webhook受信** - イベント駆動の自動化

#### 中優先度
6. **Payments管理** - 支払い履歴の確認
7. **Refunds管理** - 返金処理
8. **Promo Codes管理** - プロモーションコードの作成・管理
9. **Members管理** - メンバー情報の取得・更新

#### 低優先度
10. **Engagement機能** - フォーラム、チャット、メッセージ
11. **Courses機能** - コース管理
12. **Payouts機能** - 引き出し処理

---

## 🔧 実装方法

### 1. 既存ワークフローの拡張

`whop-control`ワークフローに新しいアクションを追加：

```json
{
  "action": "get_products",
  "company_id": "biz_xxxxxxxxxxxxxx"
}
```

### 2. 新しいワークフローの作成

各カテゴリーごとに専用のワークフローを作成：

- `whop-products-control.json` - Products管理
- `whop-affiliates-control.json` - Affiliates管理
- `whop-webhooks.json` - Webhook受信

### 3. APIキーの管理

- **Infisical**: APIキーを一元管理（現在の実装）
- **n8n Credentials**: HTTP Header Authとして設定
- **環境変数**: ワークフロー内で動的に取得

---

## 📝 使用例

### 製品一覧を取得

```bash
curl -X POST https://hadayalab.app.n8n.cloud/webhook/whop-control \
  -H "Content-Type: application/json" \
  -d '{
    "action": "get_products",
    "company_id": "biz_xxxxxxxxxxxxxx",
    "page": 1,
    "per_page": 50
  }'
```

### メンバーシップをキャンセル

```bash
curl -X POST https://hadayalab.app.n8n.cloud/webhook/whop-control \
  -H "Content-Type: application/json" \
  -d '{
    "action": "cancel_membership",
    "membership_id": "membership_123"
  }'
```

---

## 🔗 関連ドキュメント

**⭐ 親戦略ドキュメント（最新）:**
- **[n8n + Whop 完全活用戦略 SSOT](./n8n-whop-full-strategy-SSOT.md)** - n8n + Whop完全統合戦略（**最初に参照**）

**権限・認証関連:**
- **[WHOP_API_PERMISSIONS_COMPLETE.md](./WHOP_API_PERMISSIONS_COMPLETE.md)** ⭐ **Whop API権限完全リスト（権限確認時に参照）**

**技術ドキュメント:**
- [Whop API Documentation](https://docs.whop.com/api-reference)
- [Whop API Getting Started](https://docs.whop.com/developer/api/getting-started)
- [whop-control-workflow-SSOT.md](./whop-control-workflow-SSOT.md)
- [api-integration-implementation-plan.md](./api-integration-implementation-plan.md)

---

**最終更新**: 2025-12-26
**バージョン**: 1.1.0（権限リスト統合）

