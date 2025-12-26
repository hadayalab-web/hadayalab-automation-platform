# Whopアフィリエイター候補データベース化戦略

**作成日**: 2025-12-26
**目的**: Whopの機能を使用してアフィリエイター候補をデータベース化する方法を検討

---

## 🎯 検討結果サマリー

Whopには専用の「データベース」機能はありませんが、以下の方法でデータを保存・管理できる可能性があります：

1. **Entries機能を活用** ⚠️ 権限設定が必要
2. **Metadata機能を活用**（Memberships/Members経由） ✅ 推奨
3. **Whop Apps機能を活用** 🚧 調査中
4. **外部DB + Whop統合**（ハイブリッド） ✅ 実用的

---

## ⚠️ 検証結果: Entries API

### テスト結果

**エラー**: `401 Client Error: Unauthorized`
**メッセージ**: "The API Key supplied does not have permission to access this route."

**原因**:
- API Keyに`entries`エンドポイントへのアクセス権限がない可能性
- Whop DashboardでAPI Keyの権限設定が必要

### 解決方法

1. **Whop Dashboard → Developer → API Keys**
2. 使用中のAPI Keyを選択
3. 権限設定で`entries:read`, `entries:write`を有効化
4. API Keyを再生成（必要に応じて）

---

## 方法1: Entries機能を活用 ⚠️ 権限設定後に対応

### 概要

WhopのEntries機能を使用して、アフィリエイター候補を「エントリー」として作成・管理します。

### 実装方法

#### 1. Entry作成（アフィリエイター候補登録）

**APIエンドポイント**:
```
POST /api/v2/entries
```

**リクエストボディ例**:
```json
{
  "product_id": "prod_xxxxxxxxxxxxxx",
  "user_email": "candidate@example.com",
  "metadata": {
    "username": "@cryptotrader123",
    "display_name": "Crypto Trader",
    "market": "EN",
    "follower_count": 15000,
    "engagement_rate": 3.5,
    "content_type": "Technical analysis",
    "match_score": 8,
    "profile_url": "https://twitter.com/cryptotrader123",
    "extraction_date": "2025-12-26T13:00:00Z",
    "status": "New"
  },
  "auto_approve": false
}
```

**特徴**:
- ✅ `metadata`フィールドにカスタムデータを保存可能
- ✅ エントリー状態（approved/rejected/pending）で管理
- ✅ Productに紐づけられるため、組織化しやすい
- ✅ エントリー承認機能を使用して、実際のアフィリエイター登録プロセスに統合可能

### メリット

1. ✅ **Whop内で完結**: 外部データベース不要
2. ✅ **メタデータ保存**: カスタムフィールドを`metadata`に保存可能
3. ✅ **状態管理**: Entryステータス（pending/approved/rejected）で管理
4. ✅ **統合性**: Whopの既存システムと統合しやすい

### デメリット

1. ⚠️ **API権限が必要**: `entries:read`, `entries:write`権限の設定が必要
2. ⚠️ **メタデータの制限**: `metadata`フィールドの構造やサイズ制限が不明

---

## 方法2: Metadata機能を活用（Members経由） ✅ 推奨

### 概要

WhopのMembers/Memberships機能の`metadata`フィールドを使用して、アフィリエイター候補情報を保存します。

### 実装方法

#### 1. Member作成（候補登録）

**APIエンドポイント**:
```
POST /api/v2/members
```

**リクエストボディ例**:
```json
{
  "email": "candidate@example.com",
  "metadata": {
    "type": "affiliate_candidate",
    "username": "@cryptotrader123",
    "display_name": "Crypto Trader",
    "market": "EN",
    "follower_count": 15000,
    "engagement_rate": 3.5,
    "match_score": 8,
    "profile_url": "https://twitter.com/cryptotrader123",
    "extraction_date": "2025-12-26T13:00:00Z",
    "status": "New"
  }
}
```

**注意**: Members機能は実際のメンバーシップ管理用のため、候補管理には適していない可能性があります。

---

## 方法3: 外部DB + Whop統合（ハイブリッド） ✅ 実用的

### 概要

**Google Sheetsまたは軽量DB（Supabase/Firebase）をメインデータベースとして使用**し、Whop APIは**アフィリエイター登録後の管理**に使用します。

### データフロー

```
Grok AI X解析
  ↓
候補抽出（JSON）
  ↓
Google Sheets / Supabase（メインDB）
  - 候補リスト管理
  - 検索・分析
  - ステータス管理
  ↓
Cold Outreach（n8n経由）
  - Email送信
  - DM送信
  ↓
レスポンス・承認
  ↓
Whop API: Affiliate登録
  - Affiliate作成
  - Tier設定
  - Commission設定
```

### メリット

1. ✅ **検索・分析が容易**: Google Sheetsで複雑な検索・分析が可能
2. ✅ **データ構造が明確**: 自由にカラム設計が可能
3. ✅ **Whop統合**: 承認後、Whop APIで正式にアフィリエイター登録
4. ✅ **実装が簡単**: 既存のGoogle Sheets連携が利用可能

### デメリット

1. ⚠️ **外部DB**: Whop外の管理
2. ⚠️ **統合性**: 2つのシステムを管理する必要

---

## 方法4: Whop Apps機能を活用 🚧 調査中

### 概要

Whop Apps機能を使用して、カスタムアプリを作成し、その中でデータベース機能を実装します。

### 現状

- **Apps API**: `GET/POST/PATCH/DELETE /apps` が利用可能
- **App Builds API**: `GET/POST /app-builds` が利用可能
- **詳細仕様**: 不明確（カスタムアプリの実装方法が不明）

### 今後の調査項目

1. Whop Appsの開発方法
2. App内データストレージ機能の有無
3. 外部データベース連携の可否

---

## 📊 推奨アプローチ

### 優先順位1: ハイブリッドアプローチ（Google Sheets + Whop API） ✅

**理由**:
- ✅ 実装が簡単（既存のGoogle Sheets連携が利用可能）
- ✅ 検索・分析が容易
- ✅ Whop APIで正式なアフィリエイター登録が可能
- ✅ 現時点で最も実用的

**実装内容**:
1. Google Sheets: アフィリエイター候補リスト（メインDB）
2. Grok AI X解析: 候補抽出 → Google Sheets書き込み
3. n8nワークフロー: ステータス管理、Cold Outreach
4. Whop API: 承認後、正式なアフィリエイター登録

### 優先順位2: Entries機能（権限設定後） ⚠️

**理由**:
- ✅ Whop内で完結できる可能性
- ✅ 既存システムと統合しやすい

**前提条件**:
- Whop DashboardでAPI Keyに`entries:read`, `entries:write`権限を付与

---

## 🔧 実装設計（ハイブリッドアプローチ）

### Google Sheets構成

#### Sheet 1: Affiliate Candidates（メインシート）

| 列名 | 型 | 説明 |
|------|-----|------|
| extraction_date | Date | 抽出日時 |
| market | String | 市場コード |
| username | String | X Username |
| display_name | String | 表示名 |
| profile_url | URL | プロフィールURL |
| follower_count | Number | フォロワー数 |
| engagement_rate | Number | エンゲージメント率 |
| content_type | String | コンテンツタイプ |
| match_score | Number | マッチスコア（1-10） |
| status | String | ステータス（New/Contacted/Responded/Approved/Rejected） |
| contact_date | Date | コンタクト日 |
| response_date | Date | レスポンス日 |
| whop_affiliate_id | String | Whop Affiliate ID（承認後） |
| notes | String | メモ |

### Whop API統合（承認後）

#### Affiliate作成

**APIエンドポイント**:
```
POST /api/v2/affiliates
```

**リクエストボディ例**:
```json
{
  "product_id": "prod_xxxxxxxxxxxxxx",
  "user_email": "candidate@example.com",
  "tier": 1,
  "commission": 0.40
}
```

---

## 📋 実装手順（ハイブリッドアプローチ）

### Phase 1: Google Sheets準備

1. Google Sheets作成: "CryptoTrade Academy - Affiliate Candidates"
2. 列構成を設定（上記参照）
3. n8n Credentials: Google Sheets OAuth2設定

### Phase 2: Grok AI X解析統合

1. `grok-x-affiliate-extraction.py`実行
2. 候補抽出（JSON形式）
3. Google Sheets APIで一括書き込み

### Phase 3: n8nワークフロー実装

1. Schedule Trigger（週次実行）
2. Grok AI API呼び出し
3. Google Sheets書き込み
4. 重複排除ロジック

### Phase 4: Whop API統合（承認後）

1. Entry承認時にWhop APIでAffiliate作成
2. Google Sheetsの`whop_affiliate_id`を更新

---

## 🔍 Entries API権限設定方法

### Whop Dashboardでの設定

1. **Whop Dashboardにアクセス**
2. **Developer → API Keys**
3. **使用中のAPI Keyを選択**
4. **Permissions（権限）設定**:
   - ✅ `entries:read` - Entry一覧・詳細取得
   - ✅ `entries:write` - Entry作成・更新
   - ✅ `entries:approve` - Entry承認

5. **API Keyを保存**（または再生成）

### 権限設定後のテスト

```bash
python scripts/test-whop-entries-api.py
```

---

## 📊 比較表

| 方法 | Whop内完結 | 実装の容易さ | 検索・分析 | 統合性 | 推奨度 |
|------|-----------|------------|-----------|--------|--------|
| **Entries機能** | ✅ | ⚠️ 権限設定必要 | ⚠️ 限定的 | ✅ 高い | ⭐⭐⭐⭐ |
| **Metadata（Members）** | ✅ | ⚠️ 適切でない可能性 | ⚠️ 限定的 | ✅ 高い | ⭐⭐ |
| **外部DB + Whop** | ❌ | ✅ 簡単 | ✅ 容易 | ⚠️ 中程度 | ⭐⭐⭐⭐⭐ |
| **Whop Apps** | ✅ | ⚠️ 開発必要 | ✅ 可能 | ✅ 高い | ⭐⭐⭐（調査中） |

---

## 🚀 推奨実装アプローチ

### 即時実装: ハイブリッドアプローチ（Google Sheets + Whop API）

**理由**:
- 実装が最も簡単
- 既存のGoogle Sheets連携が利用可能
- 検索・分析が容易
- Whop APIで正式なアフィリエイター登録が可能

### 将来的な改善: Entries機能の活用

**前提条件**:
- Whop DashboardでAPI Key権限設定
- Entries APIの動作確認

**メリット**:
- Whop内で完結
- 既存システムとの統合性が高い

---

## 🔗 関連ドキュメント

- [WHOP_API_CAPABILITIES_COMPLETE.md](./WHOP_API_CAPABILITIES_COMPLETE.md)
- [grok-x-affiliate-extraction-design.md](./grok-x-affiliate-extraction-design.md)
- [n8n-whop-full-strategy-SSOT.md](./n8n-whop-full-strategy-SSOT.md)

---

**最終更新**: 2025-12-26
**ステータス**: ✅ ハイブリッドアプローチ推奨 ⚠️ Entries API権限設定後に対応可能
