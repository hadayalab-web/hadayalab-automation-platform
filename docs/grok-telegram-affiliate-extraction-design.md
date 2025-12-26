# Grok AI Telegram解析によるアフィリエイター候補抽出設計

**作成日**: 2025-12-26
**目的**: Grok AIを使用してTelegram（TG）を解析し、アフィリエイター候補を抽出

---

## 🎯 概要

### 目的

1. **Telegram解析**: Grok AIを使用してTelegramチャンネル・グループを解析
2. **アフィリエイター候補抽出**: Tier 1 Affiliateペルソナに合致するユーザーを抽出
3. **X解析との統合**: X（Twitter）とTelegramの両方から候補を抽出

---

## 📋 アフィリエイター候補ペルソナ（参照: Zero-Budget Affiliate DRM Strategy v1.1）

### Tier 1 Affiliate（10人目標）

**プロファイル**:
- Crypto YouTuber/Blogger（1K-50K subscribers）
- Technical分析特化（Chart分析者）
- 既存損失経験者（信頼性高い）
- B2B指向（教育的コンテンツ）

**見極め指標**:
- ✅ Engagement Rate: 3%以上
- ✅ Content Quality: Technical深掘り
- ✅ Audience Fit: Retail Trader（EN/AR/KO/JA/LATAM）
- ✅ Platform Limit経験: "YouTubeだけでは限界"
- ✅ 収益化意欲: 既存Affiliate経験あり

**発見場所（Telegram）**:
- Telegram Channel: Crypto分析チャンネル運営者（5K-50K subscribers）
- Telegram Group: Crypto trading groups（アクティブなメンバー）
- Telegram Bot: Crypto分析Bot運営者

---

## 🔍 Telegram検索戦略

### 検索対象

#### 1. Telegram Channels（チャンネル）

**検索方法**:
- Telegram Search: `crypto technical analysis`
- Telegram Search: `bitcoin trading signals`
- Telegram Search: `on-chain analysis`

**フィルタ条件**:
- Subscribers: 5,000 - 50,000
- 投稿頻度: 週3回以上
- コンテンツタイプ: Technical分析、Chart分析

#### 2. Telegram Groups（グループ）

**検索方法**:
- Telegram Search: `crypto trading group`
- Telegram Search: `bitcoin analysis group`

**フィルタ条件**:
- Members: 1,000 - 50,000
- アクティビティ: 高（日次投稿あり）
- コンテンツ品質: Technical分析、Educational

#### 3. Telegram Bots（ボット）

**検索方法**:
- Telegram Search: `crypto analysis bot`
- Telegram Search: `trading signal bot`

**フィルタ条件**:
- Users: 5,000 - 50,000
- 機能: Technical分析、Signal配信

---

## 🤖 Grok AIプロンプト設計（Telegram解析）

### プロンプト: Telegram Channel/Group解析

```
You are an expert affiliate recruiter for CryptoTrade Academy, a crypto trading education platform.

Your task is to analyze Telegram channels/groups and identify potential Tier 1 Affiliate candidates.

**Affiliate Persona (Tier 1)**:
- Crypto YouTuber/Blogger (1K-50K subscribers)
- Technical analysis focused (Chart analysis)
- Existing loss experience (high credibility)
- B2B oriented (educational content)
- Engagement Rate: 3%+
- Audience: Retail Traders
- Follower/Subscriber Count: 5,000-50,000

**Telegram Source**: [CHANNEL_NAME] or [GROUP_NAME]
**Market**: [MARKET_CODE] (EN/AR/KO/JA/ES/PT-BR)

**Instructions**:
1. Analyze the Telegram channel/group based on the provided information
2. Extract channel/group administrators and active contributors who match the Tier 1 Affiliate persona
3. For each candidate, extract the following information:
   - Username (@username)
   - Display Name
   - Subscriber/Member Count (must be between 5,000-50,000)
   - Engagement Rate (estimated from recent posts)
   - Content Type (Technical analysis / Chart analysis / Educational / Signal provider)
   - Recent Topics (last 10 posts topics as array)
   - Pain Points (inferred from posts as array)
   - Contact Method (Email if available, or Telegram)
   - Match Score (1-10, how well they match the persona)
   - Language (for market matching)
   - Profile URL (Telegram link)
   - Bio/Description

4. Return the results as a JSON array ONLY, no other text. Maximum 20 candidates per channel/group.
5. Only include candidates with match_score >= 7
6. Prioritize candidates with high engagement rates and technical content focus

**JSON Format**:
[
  {
    "username": "@channel_admin",
    "display_name": "Crypto Analysis Channel",
    "subscriber_count": 15000,
    "engagement_rate": 3.5,
    "content_type": "Technical analysis",
    "recent_topics": ["BTC technical analysis", "Chart patterns"],
    "pain_points": ["Limited monetization", "Platform limitations"],
    "contact_method": "Telegram",
    "match_score": 8,
    "language": "en",
    "profile_url": "https://t.me/channel_name",
    "bio": "Daily crypto technical analysis",
    "source_type": "telegram_channel",
    "source_name": "Crypto Analysis Channel"
  }
]
```

---

## 📊 データベース設計（X + Telegram統合）

### Google Sheets構成

#### Sheet 1: Affiliate Candidates（メインシート）

**既存列に追加**:
- `source_platform` - 抽出元プラットフォーム（X/Twitter, Telegram）
- `source_type` - ソースタイプ（channel, group, bot, profile）
- `source_name` - ソース名（チャンネル名、グループ名等）
- `source_url` - ソースURL

**全列構成**:
- extraction_date, market, username, display_name, profile_url
- follower_count, engagement_rate, content_type, recent_topics, pain_points
- contact_method, email, match_score, language, bio
- source_platform, source_type, source_name, source_url
- status (New/Contacted/Responded/Approved/Rejected)
- contact_date, response_date, whop_affiliate_id, notes

---

## 🔄 ワークフロー設計（X + Telegram統合）

### n8nワークフロー構造

```
1. Schedule Trigger（週次実行）
   - Cron: 0 9 * * 1（毎週月曜9時）
   ↓
2. Switch Node（プラットフォーム分岐）
   - Branch 1: X (Twitter)
   - Branch 2: Telegram
   ↓
3a. X解析ブランチ
    - Code Node（X検索クエリ生成）
    - HTTP Request Node（Grok AI API - X解析）
    ↓
3b. Telegram解析ブランチ
    - Code Node（Telegram検索クエリ生成）
    - HTTP Request Node（Grok AI API - Telegram解析）
    ↓
4. Merge Node（X + Telegram結果をマージ）
   ↓
5. Code Node（重複排除・データ整形）
   ↓
6. Google Sheets Node（候補データ追加）
   - Operation: Append
   - Sheet: Affiliate Candidates
   ↓
7. （オプション）Whop API: Waitlist Entry作成
   - POST /api/v2/waitlist-entries（権限確認後）
```

---

## 🔧 実装詳細

### Telegram検索クエリ（6市場別）

#### EN (English)

**Telegram Channels**:
- `crypto technical analysis`
- `bitcoin trading signals`
- `on-chain analysis`

**Telegram Groups**:
- `crypto trading group`
- `bitcoin analysis group`

#### AR (Arabic)

**Telegram Channels**:
- `التحليل الفني للعملات المشفرة`
- `إشارات تداول البتكوين`

#### KO (Korean)

**Telegram Channels**:
- `암호화폐 기술적 분석`
- `비트코인 거래 신호`

#### JA (Japanese)

**Telegram Channels**:
- `仮想通貨 テクニカル分析`
- `ビットコイン 取引シグナル`

#### ES (Spanish)

**Telegram Channels**:
- `análisis técnico criptomonedas`
- `señales trading bitcoin`

#### PT-BR (Portuguese - BR)

**Telegram Channels**:
- `análise técnica criptomoedas`
- `sinais trading bitcoin`

---

## 📝 Grok AI API呼び出し（Telegram解析）

### Python実装例

```python
def extract_affiliate_candidates_from_telegram(channel_name, market_code, api_key):
    """Grok AIを使用してTelegramからアフィリエイター候補を抽出"""
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""You are an expert affiliate recruiter for CryptoTrade Academy.

Analyze the Telegram channel/group: {channel_name}
Market: {market_code}

Extract potential Tier 1 Affiliate candidates matching the persona:
- Crypto YouTuber/Blogger (1K-50K subscribers)
- Technical analysis focused
- Engagement Rate: 3%+
- Subscriber/Member Count: 5,000-50,000

Return results as a JSON array with the structure defined in the design document."""

    data = {
        "model": "grok-beta",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert affiliate recruiter. Extract affiliate candidates from Telegram channels/groups. Always return valid JSON arrays only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 4000,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()

    result = response.json()
    content = result["choices"][0]["message"]["content"]

    # JSON抽出
    if "```json" in content:
        json_start = content.find("```json") + 7
        json_end = content.find("```", json_start)
        content = content[json_start:json_end].strip()

    candidates = json.loads(content)

    # プラットフォーム情報を追加
    for candidate in candidates:
        candidate["source_platform"] = "Telegram"
        candidate["source_type"] = "channel"  # または "group", "bot"
        candidate["source_name"] = channel_name
        candidate["market"] = market_code
        candidate["extraction_date"] = datetime.now().isoformat()

    return candidates
```

---

## 🔄 X + Telegram統合スクリプト

### 更新: grok-x-telegram-affiliate-extraction.py

既存の`grok-x-affiliate-extraction.py`を拡張して、Telegram解析も追加します。

**機能**:
1. X解析（既存機能）
2. Telegram解析（新規追加）
3. 結果マージ・重複排除
4. Google Sheets書き込み

---

## 📊 データフロー（統合版）

```
週次実行（毎週月曜9時）
  ↓
┌─────────────────┬─────────────────┐
│  X解析ブランチ   │ Telegram解析ブランチ │
│                 │                 │
│ 1. 検索クエリ生成│ 1. チャンネル/グループ検索 │
│ 2. Grok AI解析  │ 2. Grok AI解析  │
│ 3. 候補抽出     │ 3. 候補抽出     │
└─────────────────┴─────────────────┘
  ↓
Merge Node（結果マージ）
  ↓
重複排除（username + source_platformで判定）
  ↓
Google Sheets書き込み
  ↓
（オプション）Whop Waitlist Entry作成
```

---

## 🔗 関連ドキュメント

- [grok-x-affiliate-extraction-design.md](./grok-x-affiliate-extraction-design.md) - X解析設計
- [whop-affiliate-candidates-database-strategy.md](./whop-affiliate-candidates-database-strategy.md) - Whop DB化戦略
- [whop-waitlist-entries-analysis.md](./whop-waitlist-entries-analysis.md) - Waitlist Entries機能分析

---

**最終更新**: 2025-12-26
**ステータス**: ✅ 設計完了 🚧 実装待ち

