# Grok AI X解析によるアフィリエイター候補抽出・データベース化設計

**作成日**: 2025-12-26
**目的**: Grok AIを使用してX（Twitter）を解析し、6市場別のアフィリエイター候補を抽出・データベース化

---

## 🎯 概要

### 目的

1. **X（Twitter）解析**: Grok AIを使用してXの投稿・ユーザーを解析
2. **アフィリエイター候補抽出**: Tier 1 Affiliateペルソナに合致するユーザーを抽出
3. **データベース化**: Google Sheetsに構造化データとして保存
4. **6市場対応**: EN/AR/KO/JA/ES/PT-BR 各市場別に候補を抽出

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

**発見場所（X）**:
- X(Twitter): Crypto FinTwit（5K-50K followers）

---

## 🔍 X検索クエリ設計（6市場別）

### EN (English)

**検索クエリ例**:
- `crypto technical analysis BTC`
- `bitcoin trading loss recovery`
- `on-chain analysis tutorial`
- `crypto trap detection`
- `whale alert BTC trading`

**フィルタ条件**:
- Follower数: 5,000 - 50,000
- Engagement Rate: 3%以上
- 投稿頻度: 週3回以上
- コンテンツタイプ: Technical分析、Chart分析

### AR (Arabic)

**検索クエリ例**:
- `التحليل الفني للبتكوين` (Bitcoin technical analysis)
- `تداول العملات المشفرة` (Cryptocurrency trading)
- `تحليل سلسلة البلوكشين` (Blockchain chain analysis)

**フィルタ条件**:
- 言語: アラビア語
- Follower数: 5,000 - 50,000
- Engagement Rate: 3%以上

### KO (Korean)

**検索クエリ例**:
- `비트코인 기술적 분석`
- `암호화폐 거래 전략`
- `온체인 분석`
- `김치프리미엄 분석`

**フィルタ条件**:
- 言語: 韓国語
- Follower数: 5,000 - 50,000
- Engagement Rate: 3%以上

### JA (Japanese)

**検索クエリ例**:
- `ビットコイン テクニカル分析`
- `仮想通貨 取引戦略`
- `オンチェーン分析`
- `暗号資産 トレード`

**フィルタ条件**:
- 言語: 日本語
- Follower数: 5,000 - 50,000
- Engagement Rate: 3%以上

### ES (Spanish)

**検索クエリ例**:
- `análisis técnico bitcoin`
- `trading criptomonedas`
- `análisis on-chain`
- `estrategia trading BTC`

**フィルタ条件**:
- 言語: スペイン語
- Follower数: 5,000 - 50,000
- Engagement Rate: 3%以上

### PT-BR (Portuguese - BR)

**検索クエリ例**:
- `análise técnica bitcoin`
- `trading criptomoedas`
- `análise on-chain`
- `estratégia trading BTC`

**フィルタ条件**:
- 言語: ポルトガル語（ブラジル）
- Follower数: 5,000 - 50,000
- Engagement Rate: 3%以上

---

## 🤖 Grok AIプロンプト設計

### プロンプト1: ユーザー検索・抽出

```
You are an expert affiliate recruiter for CryptoTrade Academy, a crypto trading education platform.

Your task is to analyze X (Twitter) search results and identify potential Tier 1 Affiliate candidates.

**Affiliate Persona (Tier 1)**:
- Crypto YouTuber/Blogger (1K-50K subscribers)
- Technical analysis focused (Chart analysis)
- Existing loss experience (high credibility)
- B2B oriented (educational content)
- Engagement Rate: 3%+
- Audience: Retail Traders

**Search Query**: [QUERY]
**Market**: [MARKET_CODE] (EN/AR/KO/JA/ES/PT-BR)

**Instructions**:
1. Analyze the search results from X (Twitter)
2. Extract users who match the Tier 1 Affiliate persona
3. For each candidate, extract the following information:
   - Username (@handle)
   - Display Name
   - Follower Count (must be between 5,000-50,000)
   - Engagement Rate (estimated from recent posts)
   - Content Type (Technical analysis / Chart analysis / Educational / Other)
   - Recent Topics (last 10 posts topics)
   - Pain Points (inferred from posts)
   - Contact Method (Email if available, or DM)
   - Match Score (1-10, how well they match the persona)
   - Language (for market matching)

4. Return the results as a JSON array with the following structure:
```json
[
  {
    "username": "@handle",
    "display_name": "Display Name",
    "follower_count": 15000,
    "engagement_rate": 3.5,
    "content_type": "Technical analysis",
    "recent_topics": ["BTC technical analysis", "Chart patterns", "On-chain data"],
    "pain_points": ["Limited monetization", "Platform limitations"],
    "contact_method": "DM",
    "match_score": 8,
    "language": "en",
    "profile_url": "https://twitter.com/handle",
    "bio": "Bio text",
    "verified": false,
    "joined_date": "2020-01-01"
  }
]
```

5. Only include candidates with match_score >= 7
6. Maximum 20 candidates per search query
7. Prioritize candidates with high engagement rates and technical content focus
```

### プロンプト2: 詳細プロファイル分析（候補ごと）

```
You are analyzing a specific X (Twitter) user as a potential affiliate candidate for CryptoTrade Academy.

**User Information**:
- Username: @[USERNAME]
- Market: [MARKET_CODE]

**Analysis Tasks**:
1. Review the user's recent 20 posts
2. Analyze their content quality and technical depth
3. Identify their audience demographics
4. Assess their monetization potential
5. Evaluate their fit with CryptoTrade Academy's affiliate program

**Output Format (JSON)**:
```json
{
  "username": "@handle",
  "content_analysis": {
    "technical_depth": "High/Medium/Low",
    "chart_analysis_frequency": "Daily/Weekly/Rarely",
    "educational_content_ratio": 0.7,
    "crypto_loss_experience": true,
    "affiliate_experience": false
  },
  "audience_analysis": {
    "estimated_size": 15000,
    "engagement_rate": 3.5,
    "audience_type": "Retail traders",
    "geographic_distribution": "EN/US/UK"
  },
  "monetization_potential": {
    "estimated_monthly_reach": 50000,
    "conversion_probability": 0.05,
    "estimated_monthly_sales": 5,
    "estimated_monthly_revenue": 2500
  },
  "fit_assessment": {
    "persona_match_score": 8,
    "content_alignment": "High",
    "audience_alignment": "High",
    "recommendation": "Strong candidate"
  }
}
```
```

---

## 💾 データベース設計

### 推奨アプローチ: Google Sheets（メインDB）+ Whop API（承認後統合）

**理由**:
- ✅ 実装が簡単（既存のGoogle Sheets連携が利用可能）
- ✅ 検索・分析が容易
- ✅ Whop APIで正式なアフィリエイター登録が可能
- ✅ 現時点で最も実用的

**代替案**: Whop Entries機能（API Key権限設定後に対応可能）
- 参照: [whop-affiliate-candidates-database-strategy.md](./whop-affiliate-candidates-database-strategy.md)

### データベース設計（Google Sheets）

### シート構成

#### Sheet 1: Affiliate Candidates（メインシート）

| 列名 | 型 | 説明 |
|------|-----|------|
| extraction_date | Date | 抽出日時 |
| market | String | 市場コード（EN/AR/KO/JA/ES/PT-BR） |
| username | String | X Username（@handle） |
| display_name | String | 表示名 |
| profile_url | URL | プロフィールURL |
| follower_count | Number | フォロワー数 |
| engagement_rate | Number | エンゲージメント率（%） |
| content_type | String | コンテンツタイプ |
| recent_topics | String | 最近のトピック（カンマ区切り） |
| pain_points | String | 痛みポイント（カンマ区切り） |
| contact_method | String | 連絡方法（Email/DM） |
| email | String | Emailアドレス（取得できた場合） |
| match_score | Number | マッチスコア（1-10） |
| language | String | 言語コード |
| bio | String | プロフィールBio |
| verified | Boolean | 認証済みアカウントか |
| joined_date | Date | アカウント作成日 |
| status | String | ステータス（New/Contacted/Responded/Onboarded/Rejected） |
| notes | String | メモ |
| last_updated | Date | 最終更新日時 |

#### Sheet 2: Content Analysis（詳細分析）

| 列名 | 型 | 説明 |
|------|-----|------|
| username | String | X Username（@handle） |
| market | String | 市場コード |
| technical_depth | String | Technical深掘り度（High/Medium/Low） |
| chart_analysis_frequency | String | Chart分析頻度 |
| educational_content_ratio | Number | 教育的コンテンツ比率（0-1） |
| crypto_loss_experience | Boolean | 損失経験があるか |
| affiliate_experience | Boolean | アフィリエイト経験があるか |
| estimated_monthly_reach | Number | 推定月間リーチ |
| conversion_probability | Number | コンバージョン確率（0-1） |
| estimated_monthly_sales | Number | 推定月間売上数 |
| estimated_monthly_revenue | Number | 推定月間収益 |
| persona_match_score | Number | ペルソナマッチスコア（1-10） |
| content_alignment | String | コンテンツ適合度 |
| audience_alignment | String | オーディエンス適合度 |
| recommendation | String | 推奨（Strong candidate/Maybe/Reject） |
| analysis_date | Date | 分析日時 |

---

## 🔄 ワークフロー設計

### Option 1: n8nワークフロー（推奨）

```
1. Schedule Trigger（週次実行）
   - Cron: 0 9 * * 1（毎週月曜9時）
   ↓
2. Switch Node（市場分岐）
   - EN, AR, KO, JA, ES, PT-BR
   ↓
3. Code Node（検索クエリ生成）
   - 市場別検索クエリリスト生成
   ↓
4. Loop Node（各検索クエリをループ）
   ↓
5. HTTP Request Node（Grok AI API呼び出し）
   - Model: grok-beta
   - Endpoint: https://api.x.ai/v1/chat/completions
   - Prompt: プロンプト1（ユーザー検索・抽出）
   ↓
6. Code Node（JSON解析・整形）
   - Grok AIレスポンスから候補データ抽出
   ↓
7. Google Sheets Node（候補データ追加）
   - Operation: Append
   - Sheet: Affiliate Candidates
   ↓
8. Loop Node（各候補を詳細分析）
   ↓
9. HTTP Request Node（Grok AI API呼び出し）
   - Prompt: プロンプト2（詳細プロファイル分析）
   ↓
10. Google Sheets Node（詳細分析データ追加）
    - Operation: Append
    - Sheet: Content Analysis
```

### Option 2: Pythonスクリプト

**ファイル**: `scripts/grok-x-affiliate-extraction.py`

**機能**:
1. InfisicalからGrok AI API Key取得
2. 6市場別検索クエリを実行
3. Grok AIでX解析・候補抽出
4. Google Sheets APIでデータベース化

---

## 🔧 実装詳細

### Grok AI API呼び出し

```python
import requests
import json
import subprocess

def get_grok_api_key():
    """InfisicalからGrok AI API Keyを取得"""
    result = subprocess.run(
        ["infisical", "secrets", "get", "XAI_API_KEY", "--token", INFISICAL_TOKEN, "--projectId", PROJECT_ID, "--output", "json"],
        capture_output=True,
        text=True,
        check=True
    )
    secrets = json.loads(result.stdout.strip())
    return secrets[0]["secretValue"]

def extract_affiliate_candidates(search_query, market_code):
    """Grok AIを使用してアフィリエイター候補を抽出"""
    api_key = get_grok_api_key()

    prompt = f"""
    You are an expert affiliate recruiter for CryptoTrade Academy.

    Analyze X (Twitter) search results for: {search_query}
    Market: {market_code}

    Extract potential Tier 1 Affiliate candidates matching the persona:
    - Crypto YouTuber/Blogger (1K-50K subscribers)
    - Technical analysis focused
    - Engagement Rate: 3%+
    - Follower Count: 5,000-50,000

    Return results as JSON array with the structure defined in the design document.
    """

    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "grok-beta",  # GrokのX検索機能を使用
        "messages": [
            {
                "role": "system",
                "content": "You are an expert affiliate recruiter. Extract affiliate candidates from X (Twitter) search results."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 4000,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    result = response.json()
    candidates_json = result["choices"][0]["message"]["content"]

    # JSON解析
    candidates = json.loads(candidates_json)
    return candidates
```

### Google Sheets書き込み

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import gspread

def write_to_google_sheets(candidates, market_code):
    """Google Sheetsに候補データを書き込み"""
    # Google Sheets認証（OAuth2）
    gc = gspread.service_account(filename='credentials.json')
    sheet = gc.open("CryptoTrade Academy - Affiliate Candidates")
    worksheet = sheet.worksheet("Affiliate Candidates")

    # データ準備
    rows = []
    for candidate in candidates:
        row = [
            datetime.now().isoformat(),  # extraction_date
            market_code,  # market
            candidate.get("username", ""),
            candidate.get("display_name", ""),
            candidate.get("profile_url", ""),
            candidate.get("follower_count", 0),
            candidate.get("engagement_rate", 0),
            candidate.get("content_type", ""),
            ",".join(candidate.get("recent_topics", [])),
            ",".join(candidate.get("pain_points", [])),
            candidate.get("contact_method", ""),
            candidate.get("email", ""),
            candidate.get("match_score", 0),
            candidate.get("language", ""),
            candidate.get("bio", ""),
            candidate.get("verified", False),
            candidate.get("joined_date", ""),
            "New",  # status
            "",  # notes
            datetime.now().isoformat()  # last_updated
        ]
        rows.append(row)

    # 一括追加
    worksheet.append_rows(rows)
```

---

## 📊 実行スケジュール

### 週次実行（推奨）

- **頻度**: 毎週月曜 9:00 JST
- **市場**: 6市場すべてを実行
- **検索クエリ数**: 市場あたり5-10クエリ
- **推定候補数**: 市場あたり20-50候補

### 月次実行（オプション）

- **頻度**: 毎月1日 9:00 JST
- **目的**: 詳細分析（Content Analysis）の更新

---

## 🔗 関連ドキュメント

- [grok-telegram-affiliate-extraction-design.md](./grok-telegram-affiliate-extraction-design.md) ⭐ Telegram解析設計（追加）
- [Zero-Budget Affiliate DRM Strategy v1.1 + APDS v1.0](../../cryptosignal-ai/docs/CryptoTrade Academy - Zero-Budget Affiliate DRM Strategy v1.1 + APDS v1.0.md)
- [Grok AI Client Implementation](../../cryptosignal-ai/services/grok/client.js)
- [API制御状況サマリー](./API_CONTROL_STATUS_SUMMARY.md)

---

**最終更新**: 2025-12-26
**更新内容**: Telegram解析機能を追加（X + Telegram統合）

