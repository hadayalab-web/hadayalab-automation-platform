#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grok AI X + Telegram解析によるアフィリエイター候補抽出スクリプト
6市場別にX（Twitter）とTelegramを解析し、アフィリエイター候補を抽出・Google Sheetsに保存
"""
import requests
import json
import subprocess
import sys
from datetime import datetime
from typing import List, Dict, Any
import time

# UTF-8エンコーディング設定
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Infisical設定
INFISICAL_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2luIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
PROJECT_ID = "446f131c-be8d-45e5-a83a-4154e34501a5"

# 市場別検索クエリ
# X (Twitter)検索クエリ
MARKET_X_SEARCH_QUERIES = {
    'EN': [
        'crypto technical analysis BTC',
        'bitcoin trading loss recovery',
        'on-chain analysis tutorial',
        'crypto trap detection',
        'whale alert BTC trading',
        'BTC chart analysis',
        'crypto trading strategy',
        'bitcoin on-chain metrics'
    ],
    'AR': [
        'التحليل الفني للبتكوين',
        'تداول العملات المشفرة',
        'تحليل سلسلة البلوكشين',
        'استراتيجية تداول البتكوين'
    ],
    'KO': [
        '비트코인 기술적 분석',
        '암호화폐 거래 전략',
        '온체인 분석',
        '김치프리미엄 분석',
        '비트코인 차트 분석'
    ],
    'JA': [
        'ビットコイン テクニカル分析',
        '仮想通貨 取引戦略',
        'オンチェーン分析',
        '暗号資産 トレード',
        'BTC チャート分析'
    ],
    'ES': [
        'análisis técnico bitcoin',
        'trading criptomonedas',
        'análisis on-chain',
        'estrategia trading BTC',
        'análisis chart bitcoin'
    ],
    'PT_BR': [
        'análise técnica bitcoin',
        'trading criptomoedas',
        'análise on-chain',
        'estratégia trading BTC',
        'análise chart bitcoin'
    ]
}

# Telegram検索クエリ
MARKET_TELEGRAM_SEARCH_QUERIES = {
    'EN': [
        'crypto signals channel',
        'bitcoin trading group',
        'on-chain analysis telegram',
        'crypto education channel'
    ],
    'AR': [
        'قناة إشارات العملات الرقمية',
        'مجموعة تداول البيتكوين',
        'تحليل العملات المشفرة تيليجرام'
    ],
    'KO': [
        '암호화폐 시그널 채널',
        '비트코인 트레이딩 그룹',
        '온체인 분석 텔레그램'
    ],
    'JA': [
        '仮想通貨 シグナル チャンネル',
        'ビットコイン トレード グループ',
        'オンチェーン分析 テレグラム'
    ],
    'ES': [
        'canal de señales cripto',
        'grupo de trading bitcoin',
        'análisis on-chain telegram'
    ],
    'PT_BR': [
        'canal de sinais cripto',
        'grupo de trading bitcoin',
        'análise on-chain telegram'
    ]
}

def get_secret_from_infisical(secret_name: str) -> str:
    """Infisicalからシークレットを取得（全シークレット取得後に検索）"""
    try:
        # list-infisical-secrets.pyと同じ方法を使用
        result = subprocess.run(
            ["infisical", "secrets", "--token", INFISICAL_TOKEN, "--projectId", PROJECT_ID, "--output", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        secrets = json.loads(output)

        # 指定されたシークレット名で検索
        for secret in secrets:
            if secret.get("secretKey") == secret_name:
                secret_value = secret.get("secretValue") or secret.get("value")
                if secret_value:
                    return secret_value

        print(f"[WARNING] Secret '{secret_name}' not found in Infisical")
        print(f"[INFO] Available secrets: {[s.get('secretKey') for s in secrets]}")
        return None
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Infisical CLI error: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to get {secret_name}: {e}")
        return None

def create_extraction_prompt(search_query: str, market_code: str, source_platform: str = "X") -> str:
    """アフィリエイター候補抽出用プロンプトを作成"""
    if source_platform == "Telegram":
        platform_description = "Telegram channel/group"
        search_description = f"Telegram channel/group: {search_query}"
    else:
        platform_description = "X (Twitter)"
        search_description = f"X (Twitter) search results for the query: \"{search_query}\""

    prompt = f"""You are an expert affiliate recruiter for CryptoTrade Academy, a crypto trading education platform.

Your task is to analyze {platform_description} and identify potential Tier 1 Affiliate candidates.

**Affiliate Persona (Tier 1)**:
- Crypto YouTuber/Blogger (1K-50K subscribers)
- Technical analysis focused (Chart analysis)
- Existing loss experience (high credibility)
- B2B oriented (educational content)
- Engagement Rate: 3%+
- Audience: Retail Traders
- Follower Count: 5,000-50,000

**Source**: {search_description}
**Market**: {market_code}
**Platform**: {source_platform}

**Instructions**:
1. Analyze {platform_description} based on: {search_query}
2. Extract users who match the Tier 1 Affiliate persona
3. For each candidate, extract the following information:
   - Username (@handle)
   - Display Name
   - Follower Count (must be between 5,000-50,000)
   - Engagement Rate (estimated from recent posts)
   - Content Type (Technical analysis / Chart analysis / Educational / Other)
   - Recent Topics (last 10 posts topics as array)
   - Pain Points (inferred from posts as array)
   - Contact Method (Email if available, or DM)
   - Match Score (1-10, how well they match the persona)
   - Language (for market matching)
   - Profile URL
   - Bio
   - Verified status (true/false)
   - Joined Date (if available)

4. Return the results as a JSON array ONLY, no other text. Maximum 20 candidates per query.
5. Only include candidates with match_score >= 7
6. Prioritize candidates with high engagement rates and technical content focus

**JSON Format**:
[
  {{
    "username": "@handle",
    "display_name": "Display Name",
    "follower_count": 15000,
    "engagement_rate": 3.5,
    "content_type": "Technical analysis",
    "recent_topics": ["BTC technical analysis", "Chart patterns"],
    "pain_points": ["Limited monetization", "Platform limitations"],
    "contact_method": "DM",
    "match_score": 8,
    "language": "{market_code.lower()}",
    "profile_url": "https://twitter.com/handle",
    "bio": "Bio text",
    "verified": false,
    "joined_date": "2020-01-01"
  }}
]"""
    return prompt

def extract_affiliate_candidates(search_query: str, market_code: str, api_key: str, source_platform: str = "X") -> List[Dict[str, Any]]:
    """Grok AIを使用してアフィリエイター候補を抽出"""
    base_url = "https://api.x.ai/v1"
    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = create_extraction_prompt(search_query, market_code, source_platform)

    # cryptosignal-aiと同じモデル名を使用
    model_name = "grok-4-0709"  # Reasoningモデル（デフォルト）

    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": f"You are an expert affiliate recruiter. Extract affiliate candidates from {source_platform}. Always return valid JSON arrays only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 4000,
        "temperature": 0.7
    }

    try:
        # 簡潔な出力（Cursorが固まらないように）
        print(f"[INFO] Query: {search_query[:40]}... (Market: {market_code})")
        # タイムアウトを短縮（30秒）し、リトライ機能を追加
        max_retries = 2
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=30)
                response.raise_for_status()
                break
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"[WARNING] Timeout, retrying ({attempt + 1}/{max_retries})...")
                    time.sleep(5)
                    continue
                else:
                    raise

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        # JSON抽出（コードブロック内のJSONを抽出）
        if "```json" in content:
            json_start = content.find("```json") + 7
            json_end = content.find("```", json_start)
            content = content[json_start:json_end].strip()
        elif "```" in content:
            json_start = content.find("```") + 3
            json_end = content.find("```", json_start)
            content = content[json_start:json_end].strip()

        candidates = json.loads(content)

        # 市場コードとプラットフォーム情報を追加
        for candidate in candidates:
            candidate["market"] = market_code
            candidate["extraction_date"] = datetime.now().isoformat()
            candidate["search_query"] = search_query
            candidate["source_platform"] = source_platform
            candidate["source_type"] = "channel" if source_platform == "Telegram" else "profile"

        print(f"[OK] Extracted {len(candidates)} candidates")
        return candidates

    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON parse failed for query: {search_query[:40]}...")
        # デバッグ情報は最小限に
        return []
    except requests.exceptions.Timeout:
        print(f"[ERROR] Timeout for query: {search_query[:40]}...")
        return []
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API error: {type(e).__name__}")
        return []
    except Exception as e:
        print(f"[ERROR] Unexpected error: {type(e).__name__}")
        return []

def format_for_google_sheets(candidates: List[Dict[str, Any]]) -> List[List[Any]]:
    """Google Sheets用にデータをフォーマット"""
    rows = []
    for candidate in candidates:
        row = [
            candidate.get("extraction_date", datetime.now().isoformat()),
            candidate.get("market", ""),
            candidate.get("username", ""),
            candidate.get("display_name", ""),
            candidate.get("profile_url", ""),
            candidate.get("follower_count", 0),
            candidate.get("engagement_rate", 0),
            candidate.get("content_type", ""),
            ",".join(candidate.get("recent_topics", [])) if isinstance(candidate.get("recent_topics"), list) else candidate.get("recent_topics", ""),
            ",".join(candidate.get("pain_points", [])) if isinstance(candidate.get("pain_points"), list) else candidate.get("pain_points", ""),
            candidate.get("contact_method", ""),
            candidate.get("email", ""),
            candidate.get("match_score", 0),
            candidate.get("language", ""),
            candidate.get("bio", ""),
            candidate.get("verified", False),
            candidate.get("joined_date", ""),
            candidate.get("source_platform", ""),  # source_platform
            candidate.get("source_type", ""),  # source_type
            candidate.get("source_name", ""),  # source_name
            candidate.get("source_url", ""),  # source_url
            "New",  # status
            "",  # notes
            datetime.now().isoformat()  # last_updated
        ]
        rows.append(row)
    return rows

def main():
    # 簡潔なヘッダー（Cursorが固まらないように）
    print("=" * 60)
    print("Grok AI アフィリエイター候補抽出")
    print("=" * 60)

    # Grok AI API Keyを取得（環境変数優先、次にInfisical）
    import os
    print("[STEP 1] Getting XAI_API_KEY...")
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        print("[INFO] XAI_API_KEY not found in environment, trying Infisical...")
        api_key = get_secret_from_infisical("XAI_API_KEY")
    if not api_key:
        print("[ERROR] Failed to get XAI_API_KEY from both environment and Infisical")
        print("[INFO] Please set XAI_API_KEY as environment variable or configure Infisical")
        sys.exit(1)
    print(f"[OK] XAI_API_KEY retrieved (preview: {api_key[:20]}...)\n")

    # 6市場別に候補抽出（X + Telegram）
    all_candidates = []

    # X解析
    print("[INFO] Starting X (Twitter) analysis...")
    for market_code, search_queries in MARKET_X_SEARCH_QUERIES.items():
        print(f"[INFO] Processing market: {market_code}")
        print(f"[INFO] Search queries: {len(search_queries)}")

        market_candidates = []

        for search_query in search_queries:
            candidates = extract_affiliate_candidates(search_query, market_code, api_key, source_platform="X")
            market_candidates.extend(candidates)

            # Rate Limit対策（リクエスト間に待機）
            time.sleep(2)

        print(f"[OK] Market {market_code} (X): Extracted {len(market_candidates)} candidates total\n")
        all_candidates.extend(market_candidates)

    # Telegram解析
    print("[INFO] Starting Telegram analysis...")
    for market_code, search_queries in MARKET_TELEGRAM_SEARCH_QUERIES.items():
        print(f"[INFO] Processing market: {market_code} (Telegram)")
        print(f"[INFO] Search queries: {len(search_queries)}")

        market_candidates = []

        for search_query in search_queries:
            candidates = extract_affiliate_candidates(search_query, market_code, api_key, source_platform="Telegram")
            market_candidates.extend(candidates)

            # Rate Limit対策（リクエスト間に待機）
            time.sleep(2)

        print(f"[OK] Market {market_code} (Telegram): Extracted {len(market_candidates)} candidates total\n")
        all_candidates.extend(market_candidates)

    # 結果サマリー
    print("=" * 60)
    print("抽出結果サマリー")
    print("=" * 60)
    print(f"総候補数: {len(all_candidates)}")
    print()

    # プラットフォーム別サマリー
    x_count = sum(1 for c in all_candidates if c.get("source_platform") == "X")
    telegram_count = sum(1 for c in all_candidates if c.get("source_platform") == "Telegram")
    print(f"  X (Twitter): {x_count} 候補")
    print(f"  Telegram: {telegram_count} 候補")
    print()

    # 市場別サマリー
    for market_code in MARKET_X_SEARCH_QUERIES.keys():
        market_count = sum(1 for c in all_candidates if c.get("market") == market_code)
        market_x_count = sum(1 for c in all_candidates if c.get("market") == market_code and c.get("source_platform") == "X")
        market_telegram_count = sum(1 for c in all_candidates if c.get("market") == market_code and c.get("source_platform") == "Telegram")
        print(f"  {market_code}: {market_count} 候補 (X: {market_x_count}, Telegram: {market_telegram_count})")

    print()

    # Google Sheets用データフォーマット
    print("[STEP 2] Formatting data for Google Sheets...")
    rows = format_for_google_sheets(all_candidates)
    print(f"[OK] Formatted {len(rows)} rows\n")

    # JSONファイルに保存（Google Sheets API実装前の一時的な保存）
    output_file = f"affiliate_candidates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_candidates, f, ensure_ascii=False, indent=2)

    print(f"[OK] Saved to {output_file}")
    print()
    print("=" * 60)
    print("次のステップ")
    print("=" * 60)
    print("1. Google Sheets APIを実装してデータベース化")
    print("2. n8nワークフローとして実装（週次自動実行）")
    print("3. 重複排除ロジックの実装")
    print()

if __name__ == "__main__":
    main()

