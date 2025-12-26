# n8n + Whop 完全活用戦略 SSOT

**最終更新**: 2025-12-26
**バージョン**: 1.0.0
**メンテナー**: HadayaLab
**親SSOT**: [hadayalab-automation-platform SSOT](./hadayalab-automation-platform-SSOT.md)

---

## 📍 ドキュメント位置づけ

### SSOT階層構造

```
hadayalab-automation-platform SSOT（プロジェクト全体SSOT）
  └─ n8n + Whop 完全活用戦略 SSOT（本ドキュメント）
      ├─ n8n + Whop + Telegram 統合戦略 SSOT ⭐ 新規追加
      ├─ n8n MCP機能比較 SSOT
      ├─ whop-control-workflow SSOT
      └─ WHOP_API_CAPABILITIES_COMPLETE.md
```

### 戦略ドキュメントとの連携

**親戦略ドキュメント**:
- **[CryptoTrade Academy - Complete SSOT v5.1](../../hadayalab-knowledge-base/literature/strategy/CryptoTrade Academy - Complete SSOT v5.1.md)**（戦略SSOT）

**参照戦略ドキュメント**:
- **Sales Strategy Doping v2.0 FINAL**（セールス戦略理論）
- **Zero-Budget Affiliate DRM Strategy v1.1 + APDS v1.0**（アフィリエイト戦略）
- **Creative Execution Master Guide v1.0**（Whop/Make/HeyGen/Adobe完全実装）

**関連SSOTドキュメント**:
- [hadayalab-automation-platform SSOT](./hadayalab-automation-platform-SSOT.md)
- **[n8n + Whop + Telegram 統合戦略 SSOT](./n8n-whop-telegram-integration-SSOT.md)** - Telegram統合戦略 ⭐ 新規追加
- [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)
- [whop-control-workflow SSOT](./whop-control-workflow-SSOT.md)

**権限・API関連ドキュメント**:
- **[WHOP_API_PERMISSIONS_COMPLETE.md](./WHOP_API_PERMISSIONS_COMPLETE.md)** ⭐ **Whop API権限完全リスト（152権限）**
- [WHOP_API_CAPABILITIES_COMPLETE.md](./WHOP_API_CAPABILITIES_COMPLETE.md) - Whop API完全機能一覧

---

## 🎯 戦略概要

### ビジョン

**「n8nの543ノード×2,700テンプレート + Whop APIの全機能を統合活用し、CryptoTrade Academyの完全自動化プラットフォームを構築する」**

### 戦略目標

1. **100%自動化**: 手作業ゼロのビジネスプロセス実現
2. **リアルタイム対応**: イベント駆動の即座な反応
3. **スケーラブル**: 6市場→グローバル展開に対応
4. **データ駆動**: 全プロセスの計測と最適化

### 戦略原則

1. **Cursor UIから完全制御**: すべての操作をCursor UIから実行
2. **SSOT準拠**: Complete SSOT v5.1を唯一の真実とする
3. **APIファースト**: Whop APIで全操作を自動化
4. **ワークフロー駆動**: n8nワークフローで全プロセスを連鎖

---

## 🏗️ アーキテクチャ

### 3層構造

```
┌─────────────────────────────────────────────────┐
│  Layer 1: Cursor UI（統一開発環境）              │
│  - n8n-mcp（ワークフロー作成・編集）            │
│  - n8nネイティブMCP（ワークフロー実行）          │
│  - Whop API制御（Webhook経由）                  │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│  Layer 2: n8n Cloud（実行エンジン）              │
│  - 543個ノード × 2,700テンプレート             │
│  - ワークフロー実行・スケジューリング           │
│  - Webhook受信・API呼び出し                     │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│  Layer 3: Whop Platform（ビジネスロジック）     │
│  - 全API機能（100+エンドポイント）              │
│  - Webhook送信（10+イベント）                   │
│  - データ管理（Memberships、Products、Plans）   │
└─────────────────────────────────────────────────┘
```

---

## 📊 n8nの完全活用

### 543ノードの戦略的分類

#### 1. 統合ノード（高優先度）

**Whop統合**:
- ✅ HTTP Request（Whop API呼び出し）
- ✅ Webhook Trigger（Whop Webhook受信）

**通信**:
- ✅ Gmail（Email送信）
- ✅ Telegram（緊急配信）
- ✅ Slack（通知）

**データ管理**:
- ✅ Google Sheets（Affiliate Performance Tracker）
- ✅ Google Drive（ファイル管理）

#### 2. データ処理ノード（中優先度）

- ✅ Code（JavaScript処理）
- ✅ Switch（条件分岐）
- ✅ Set（データ整形）
- ✅ Merge（データ結合）
- ✅ Filter（データフィルタリング）

#### 3. スケジューリングノード（高優先度）

- ✅ Schedule Trigger（定期実行）
- ✅ Wait（待機処理）
- ✅ Cron（複雑なスケジュール）

#### 4. 拡張ノード（低優先度）

- PostgreSQL、MySQL（データベース連携）
- OpenAI、Claude（AI処理）
- Salesforce、HubSpot（CRM連携）

### 2,700テンプレートの戦略的活用

#### 参考テンプレート（高優先度）

1. **CRM自動化テンプレート**
   - 顧客オンボーディング
   - 顧客フォローアップ
   - チャーン防止

2. **マーケティング自動化テンプレート**
   - Email Sequence
   - ソーシャルメディア投稿
   - コンテンツ配信

3. **営業支援テンプレート**
   - リード管理
   - パイプライン管理
   - レポート生成

4. **財務・会計テンプレート**
   - 請求書管理
   - 支払い処理
   - レポート生成

---

## 🔌 Whop APIの完全活用

### 8大カテゴリーの戦略的活用

#### 1. Payins（支払い受信）✅ 高優先度

**Products管理**:
- 製品作成・更新・削除
- 製品情報取得・一覧表示
- **戦略的価値**: 6市場別製品管理の完全自動化

**Plans管理**:
- プラン作成・更新・削除
- 価格設定の動的変更
- **戦略的価値**: 市場別価格戦略の実装

**Payments管理**:
- 支払い履歴の確認
- 支払い処理の自動化
- **戦略的価値**: Trial→有料化の完全追跡

**Promo Codes管理**:
- プロモーションコードの作成・管理
- 割引キャンペーンの実行
- **戦略的価値**: アフィリエイター向け割引の自動適用

#### 2. CRM（顧客管理）✅ 最高優先度

**Memberships管理**:
- ✅ メンバーシップ一覧・詳細取得（実装済み）
- ✅ メンバーシップキャンセル・再アクティブ化（実装済み）
- 🚧 メンバーシップ更新（未実装・優先実装候補）
- 🚧 メンバーシップ一時停止・再開（未実装・優先実装候補）
- **戦略的価値**: Trial Onboarding Automationの完全実装

**Entries管理**:
- エントリー承認・拒否処理
- アクセスリクエスト管理
- **戦略的価値**: アフィリエイター承認プロセスの自動化

**Members管理**:
- メンバー情報取得・更新
- **戦略的価値**: 顧客プロフィール管理の自動化

#### 3. Identity（身元管理）🔶 中優先度

**Users管理**:
- ユーザー情報取得・更新
- **戦略的価値**: アカウント管理の自動化

**Companies管理**:
- 会社情報管理
- **戦略的価値**: マルチアカウント管理（将来拡張）

#### 4. Engagement（エンゲージメント）🔶 中優先度

**Forums・Chat・Messages**:
- コミュニティ管理の自動化
- **戦略的価値**: 6市場別コミュニティ運営（将来拡張）

#### 5. Courses（コース管理）🔶 中優先度

**Courses・Lessons管理**:
- オンラインコースの管理
- **戦略的価値**: 教育コンテンツ配信の自動化（将来拡張）

#### 6. Payouts（支払い送金）🔶 低優先度

**Transfers・Withdrawals**:
- アフィリエイター報酬の自動支払い
- **戦略的価値**: APDS（Affiliate Performance Dashboard）との統合

#### 7. Developer（開発者機能）✅ 高優先度

**Apps・Access Tokens**:
- カスタムアプリ統合
- APIアクセス管理
- **戦略的価値**: 外部システムとの統合

#### 8. Webhooks（イベント受信）✅ 最高優先度

**実装済みイベント**:
- `membership.created` - メンバーシップ作成時
- `membership.trial_started` - トライアル開始時

**未実装イベント（優先実装候補）**:
- `membership.activated` - メンバーシップ有効化時
- `membership.deactivated` - メンバーシップ無効化時
- `membership.cancelled` - メンバーシップキャンセル時
- `payment.succeeded` - 支払い成功時
- `payment.failed` - 支払い失敗時
- `entry.approved` - エントリー承認時

**戦略的価値**: リアルタイムイベント駆動の完全自動化

---

## 🔄 統合ワークフロー戦略

### Phase 1: 基盤構築（完了）

#### ✅ 実装済みワークフロー

1. **whop-control**
   - メンバーシップ一覧・詳細取得
   - メンバーシップキャンセル・再アクティブ化
   - Webhook URL: `https://hadayalab.app.n8n.cloud/webhook/whop-control`

#### 🚧 優先実装ワークフロー（Phase 2）

2. **whop-products-management**
   - Products API完全統合
   - 製品作成・更新・削除
   - 製品情報取得・一覧表示

3. **whop-memberships-full-control**
   - Memberships API完全統合
   - メンバーシップ更新・一時停止・再開
   - メンバーシップ状態変更の完全管理

4. **whop-webhooks-receiver**
   - 全Webhookイベント受信
   - イベント駆動ワークフローのトリガー
   - リアルタイム対応の基盤

5. **whop-affiliates-management**
   - Affiliates API完全統合
   - Tier管理・報酬計算
   - APDS（Affiliate Performance Dashboard）連携

### Phase 2: Trial Onboarding完全自動化（設計済み・実装待ち）

#### 6. trial-onboarding-automation

**Complete SSOT v5.1 Section 3準拠**:
- Whop Trial開始Webhook受信
- 6市場別（EN/AR/KO/JA/ES/PT-BR）分岐
- Welcome Email即座送信
- 6時間後: Value Email送信
- 18時間後: Trial終了通知
- 課金状況確認 → Thank You / Feedback Request Email

**戦略的価値**:
- Nudge Feedback Loop実装（Sales Strategy Doping v2.0準拠）
- Trial開始率: 65%目標（Complete SSOT v5.1準拠）
- 課金率: 30%目標（Complete SSOT v5.1準拠）

### Phase 3: Affiliate管理完全自動化（設計済み・実装待ち）

#### 7. affiliate-auto-management

**Zero-Budget Affiliate DRM Strategy v1.1準拠**:
- Whop Affiliate Conversion Webhook受信
- Google SheetsからAffiliate Performance読み込み
- Tier判定（50+ = Tier 1, 20+ = Tier 2, <20 = Tier 3）
- Congratulations Email送信
- Whop APIでTier更新
- Google Sheets更新

**戦略的価値**:
- 3-Tier Affiliate自動昇格
- Elite 10 Method実装（Zero-Budget Affiliate DRM Strategy準拠）
- APDS（Affiliate Performance Dashboard）自動更新

#### 8. affiliate-drm-cold-outreach

**Zero-Budget Affiliate DRM Strategy v1.1準拠**:
- Google SheetsからAffiliate List読み込み
- Grok AIでX（Twitter）分析
- テンプレート選択（Fan/Partnership/Gift Approach）
- Gmail送信
- Follow-Up自動化（Day 4, 8, 15）

**戦略的価値**:
- ゼロ予算でのアフィリエイター獲得
- Grok AIによるピンポイントターゲティング
- DRMマーケティング戦略の完全実装

### Phase 4: Emergency Briefing完全自動化（設計済み・実装待ち）

#### 9. emergency-briefing-trigger

**Complete SSOT v5.1 Section 2.1準拠**:
- Vercel Emergency Trigger Webhook受信
- 6市場別分岐
- Telegram並列配信（30秒間隔でRate Limit対策）
- EMERGENCY判定 → 60秒以内全市場配信完了

**戦略的価値**:
- イベント駆動配信の完全自動化
- cryptosignal-aiとの完全統合

---

## 🎯 戦略的ワークフロー統合マップ

### ワークフロー連鎖構造

```
┌─────────────────────────────────────────────────┐
│  Whop Webhook Events（イベント発生源）          │
│  - membership.trial_started                     │
│  - membership.activated                         │
│  - membership.cancelled                         │
│  - payment.succeeded                            │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│  whop-webhooks-receiver                         │
│  （イベント受信・ルーティング）                  │
└───┬───────┬───────┬───────┬───────────────────┘
    │       │       │       │
    │       │       │       └─→ payment.succeeded
    │       │       │            └─→ affiliate-auto-management
    │       │       │                 └─→ Tier判定・更新
    │       │       │
    │       │       └─→ membership.cancelled
    │       │            └─→ churn-prevention
    │       │                 └─→ Retention Email Sequence
    │       │
    │       └─→ membership.activated
    │            └─→ trial-onboarding-automation
    │                 └─→ Welcome Email → Value Email → Trial End
    │
    └─→ membership.trial_started
         └─→ trial-onboarding-automation
              └─→ Welcome Email → Value Email → Trial End
                   └─→ whop-memberships-full-control（課金状況確認）
```

### Cursor UIからの完全制御フロー

```
Cursor Chat
  └─→ @n8n-local（ワークフロー作成・編集）
       └─→ workflows/whop-*.json
            └─→ GitHub push
                 └─→ n8n Cloud Import
                      └─→ Webhook URL取得
                           └─→ Whop Dashboard設定
                                └─→ 自動化開始
```

---

## 📈 戦略的KPI

### Complete SSOT v5.1準拠KPI

#### Trial Onboarding Automation

| KPI | 目標値 | 測定方法 |
|-----|--------|---------|
| Trial開始率 | 65% | Whop API: membership.trial_started / 訪問数 |
| 課金率 | 30% | Whop API: payment.succeeded / trial_started |
| Email開封率 | 80%+ | Gmail API / n8n Metrics |
| 60-second reads達成率 | 100% | Message Length Validation |

#### Affiliate Management

| KPI | 目標値 | 測定方法 |
|-----|--------|---------|
| Tier 1 Affiliate数 | 10人 | Whop API: affiliates list + tier filter |
| Tier 1 Affiliate獲得率 | 1人/月 | Google Sheets: Affiliate List |
| Cold Outreach応答率 | 10% | Gmail API: Reply Rate |
| Affiliate経由売上 | +$100K/年 | Whop API: Payments by affiliate |

#### Emergency Briefing

| KPI | 目標値 | 測定方法 |
|-----|--------|---------|
| 配信完了時間 | 60秒以内 | n8n Metrics: Workflow Execution Time |
| 配信成功率 | 99%+ | Telegram API: Message Delivery Status |
| 緊急配信頻度 | 適時 | Vercel Cron: Emergency Detection Rate |

---

## 🔐 セキュリティ・運用戦略

### APIキー管理

**Infisical統合（実装済み）**:
- ✅ Whop API Key: Infisical管理
- ✅ n8n API Key: Infisical管理
- ✅ すべてのシークレットをInfisicalで一元管理

**参照**: [Infisical設定ガイド](./infisical-setup.md)

### Whop API権限管理

**権限リスト**:
- **[WHOP_API_PERMISSIONS_COMPLETE.md](./WHOP_API_PERMISSIONS_COMPLETE.md)** ⭐ **Whop API権限完全リスト（152権限）**

**現在付与されている権限**:
- ✅ Waitlist Entries（4権限）:
  - `Manage waitlist entries`
  - `Export waitlist entries`
  - `Read waitlist entries`
  - `Read changes to waitlist entries`

**主要機能別権限要件**:
- アフィリエイター管理: `Read affiliates`, `Create affiliates`, `Update affiliates`（未確認）
- メンバーシップ管理: `Read members`, `Manage members`, `Update memberships`（未確認）
- 製品管理: `Read products`, `Create products`, `Update products`（未確認）
- プラン管理: `Read plans`, `Create plans`, `Update plans`（未確認）
- 支払い管理: `Read payments`, `Manage payments`（未確認）
- Webhook管理: `Manage webhooks`（未確認）

**参照**: [WHOP_API_PERMISSIONS_COMPLETE.md](./WHOP_API_PERMISSIONS_COMPLETE.md) - 全152権限の詳細

### エラーハンドリング

**n8nワークフロー**:
- ✅ Error Handlerノードで全エラーを捕捉
- ✅ Error Notification（Slack/Gmail）送信
- ✅ Retry Logic実装

**Whop API**:
- ✅ Rate Limit対策（30秒間隔）
- ✅ Timeout設定（30秒）
- ✅ Fallback処理（Safe Default値返却）

### 監視・ログ

**n8n Cloud Metrics**:
- ワークフロー実行回数
- エラー率
- 実行時間

**Whop API Metrics**:
- API呼び出し回数
- 成功率
- Response Time

**Google Sheets（APDS）**:
- Affiliate Performance Tracker
- 全KPIの可視化

---

## 🚀 実装ロードマップ

### Phase 1: 基盤構築（完了）

- ✅ whop-controlワークフロー実装
- ✅ Infisical統合
- ✅ n8n MCP設定

### Phase 2: Core機能実装（優先度：最高）

**目標期間**: 1-2週間

1. **whop-products-management**
   - Products API完全統合
   - 製品作成・更新・削除

2. **whop-memberships-full-control**
   - Memberships API完全統合
   - メンバーシップ更新・一時停止・再開

3. **whop-webhooks-receiver**
   - 全Webhookイベント受信
   - イベントルーティング

### Phase 3: Trial Onboarding（優先度：最高）

**目標期間**: 1-2週間

4. **trial-onboarding-automation**
   - Complete SSOT v5.1 Section 3準拠
   - Nudge Feedback Loop実装

### Phase 4: Affiliate管理（優先度：高）

**目標期間**: 2-3週間

5. **affiliate-auto-management**
   - 3-Tier Affiliate自動昇格
   - APDS連携

6. **affiliate-drm-cold-outreach**
   - Grok AI統合
   - Cold Outreach自動化

### Phase 5: Emergency Briefing（優先度：中）

**目標期間**: 1週間

7. **emergency-briefing-trigger**
   - Vercel連携
   - Telegram並列配信

### Phase 6: 拡張機能（優先度：低）

**目標期間**: 継続的

8. **churn-prevention**
   - チャーン防止Email Sequence

9. **affiliate-rewards-automation**
   - 報酬自動計算・支払い

10. **multi-market-expansion**
    - 新市場追加（FR, DE, IT等）

---

## 📚 参照ドキュメント

### 親SSOTドキュメント

- [hadayalab-automation-platform SSOT](./hadayalab-automation-platform-SSOT.md) - プロジェクト全体SSOT
- [CryptoTrade Academy - Complete SSOT v5.1](../../hadayalab-knowledge-base/literature/strategy/CryptoTrade Academy - Complete SSOT v5.1.md) - 戦略SSOT

### 関連SSOTドキュメント

- [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md) - n8n MCP機能の完全ガイド
- [whop-control-workflow SSOT](./whop-control-workflow-SSOT.md) - whop-controlワークフローのSSOT
- [WHOP_API_CAPABILITIES_COMPLETE.md](./WHOP_API_CAPABILITIES_COMPLETE.md) - Whop API完全機能一覧

### 戦略ドキュメント

- [Sales Strategy Doping v2.0 FINAL](../../hadayalab-knowledge-base/literature/strategy/CryptoTrade Academy - Sales Strategy Doping v2.0 FINAL.md) - セールス戦略理論
- [Zero-Budget Affiliate DRM Strategy v1.1 + APDS v1.0](../../hadayalab-knowledge-base/literature/strategy/CryptoTrade Academy - Zero-Budget Affiliate DRM Strategy v1.1 + APDS v1.0.md) - アフィリエイト戦略
- [Creative Execution Master Guide v1.0](../../hadayalab-knowledge-base/literature/strategy/CryptoTrade Academy - Creative Execution Master Guide v1.0.md) - Whop/Make/HeyGen/Adobe完全実装

### 技術ドキュメント

- [n8n Cloud同期運用](./n8n-cloud-sync.md) - GitHub⇔n8n Cloud同期詳細
- [Infisical設定ガイド](./infisical-setup.md) - シークレット一元管理
- [n8n-workflows-design.md](../n8n-workflows-design.md) - ワークフロー設計ドキュメント

---

## ✅ 実装チェックリスト

### Phase 2: Core機能実装

- [ ] whop-products-managementワークフロー作成
- [ ] Products API完全統合
- [ ] whop-memberships-full-controlワークフロー作成
- [ ] Memberships API完全統合（更新・一時停止・再開）
- [ ] whop-webhooks-receiverワークフロー作成
- [ ] 全Webhookイベント受信実装

### Phase 3: Trial Onboarding

- [ ] trial-onboarding-automationワークフロー作成
- [ ] 6市場別分岐実装
- [ ] Welcome Email実装
- [ ] Value Email実装（6時間後）
- [ ] Trial End通知実装（18時間後）
- [ ] 課金状況確認実装

### Phase 4: Affiliate管理

- [ ] affiliate-auto-managementワークフロー作成
- [ ] Tier判定ロジック実装
- [ ] APDS連携実装
- [ ] affiliate-drm-cold-outreachワークフロー作成
- [ ] Grok AI統合実装
- [ ] Cold Outreachテンプレート実装

### Phase 5: Emergency Briefing

- [ ] emergency-briefing-triggerワークフロー作成
- [ ] Vercel連携実装
- [ ] Telegram並列配信実装

---

## 🔄 更新履歴

### v1.0.0 (2025-12-26)

- 初版作成
- n8n + Whop完全活用戦略の体系化
- Complete SSOT v5.1との連携確立
- 実装ロードマップ作成

---

**最終更新**: 2025-12-26
**バージョン**: 1.0.0
**メンテナー**: HadayaLab

