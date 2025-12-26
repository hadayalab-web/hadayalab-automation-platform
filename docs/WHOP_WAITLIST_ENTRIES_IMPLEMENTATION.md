# Whop Waitlist Entries実装計画

**作成日**: 2025-12-26
**目的**: Whop APIの`waitlist entries`機能を使用してアフィリエイター候補をデータベース化

---

## 📋 権限確認

### 現在付与されている権限 ✅

Whop API Keyに以下の権限が付与されています：

- ✅ `Manage waitlist entries` - Waitlistエントリーの管理
- ✅ `Export waitlist entries` - Waitlistエントリーのエクスポート
- ✅ `Read waitlist entries` - Waitlistエントリーの読み取り
- ✅ `Read changes to waitlist entries` - Waitlistエントリーの変更履歴の読み取り

---

## 🔍 Waitlist Entries API調査

### APIエンドポイント（推測）

**参照**: Whop API Documentation

**想定されるエンドポイント**:
```
GET    /api/v2/waitlist-entries          - Waitlistエントリー一覧取得
POST   /api/v2/waitlist-entries          - Waitlistエントリー作成
GET    /api/v2/waitlist-entries/{id}     - Waitlistエントリー詳細取得
PATCH  /api/v2/waitlist-entries/{id}     - Waitlistエントリー更新
DELETE /api/v2/waitlist-entries/{id}     - Waitlistエントリー削除
POST   /api/v2/waitlist-entries/{id}/export - Waitlistエントリーエクスポート
```

### 実装方針

**Waitlist Entriesを使用してアフィリエイター候補を管理**:
- Waitlist Entry = アフィリエイター候補
- Waitlist Entry承認 = アフィリエイター登録
- メタデータ = 候補情報（username, follower_count, match_score等）

---

## 🔧 実装計画

### Phase 1: API調査・テスト

**タスク**:
1. Whop API DocumentationでWaitlist Entries APIの詳細を確認
2. テストスクリプト作成: `scripts/test-whop-waitlist-entries-api.py`
3. APIエンドポイント、リクエスト/レスポンス構造の確認
4. メタデータ保存の可否確認

### Phase 2: アフィリエイター候補管理への統合

**タスク**:
1. Waitlist Entry作成機能実装
2. Waitlist Entry一覧取得機能実装
3. Waitlist Entry更新機能実装（ステータス管理）
4. Waitlist Entryエクスポート機能実装

### Phase 3: n8nワークフロー統合

**タスク**:
1. Grok AI X + Telegram解析結果をWaitlist Entryとして作成
2. Waitlist Entry承認時にWhop Affiliate作成
3. Google Sheetsとの同期（補助DBとして）

---

## 📊 データ構造設計

### Waitlist Entry構造（推測）

```json
{
  "id": "waitlist_entry_123",
  "product_id": "prod_xxxxxxxxxxxxxx",
  "user_email": "candidate@example.com",
  "status": "pending",
  "metadata": {
    "affiliate_candidate": {
      "username": "@cryptotrader123",
      "display_name": "Crypto Trader",
      "market": "EN",
      "follower_count": 15000,
      "engagement_rate": 3.5,
      "match_score": 8,
      "source_platform": "X",
      "source_type": "profile",
      "extraction_date": "2025-12-26T13:00:00Z"
    }
  },
  "created_at": "2025-12-26T13:00:00Z",
  "updated_at": "2025-12-26T13:00:00Z"
}
```

---

## 🚀 次のステップ

### 即時実行

1. **Whop API Documentation確認**
   - Waitlist Entries APIの詳細仕様を確認
   - エンドポイント、パラメータ、レスポンス構造を確認

2. **テストスクリプト作成**
   - `scripts/test-whop-waitlist-entries-api.py`
   - API呼び出しテスト
   - メタデータ保存テスト

3. **実装判断**
   - Waitlist Entries機能がアフィリエイター候補管理に適用可能か判断
   - 適用可能な場合、実装を進める
   - 適用不可な場合、ハイブリッドアプローチ（Google Sheets + Whop API）を継続

---

## 🔗 関連ドキュメント

- [whop-waitlist-entries-analysis.md](./whop-waitlist-entries-analysis.md) - Waitlist Entries機能分析
- [whop-affiliate-candidates-database-strategy.md](./whop-affiliate-candidates-database-strategy.md) - Whop DB化戦略
- [WHOP_API_CAPABILITIES_COMPLETE.md](./WHOP_API_CAPABILITIES_COMPLETE.md) - Whop API完全機能一覧

---

**最終更新**: 2025-12-26
**ステータス**: 🚧 API調査・テスト待ち

