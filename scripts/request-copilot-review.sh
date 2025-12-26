#!/bin/bash
# GitHub Copilotレビュー依頼スクリプト

echo "=== GitHub Copilotレビュー依頼 ==="
echo ""

# レビュー依頼ファイルを読み込む
REVIEW_REQUEST_FILE="docs/github-copilot-review-request.md"

if [ ! -f "$REVIEW_REQUEST_FILE" ]; then
    echo "エラー: $REVIEW_REQUEST_FILE が見つかりません"
    exit 1
fi

echo "レビュー依頼ファイル: $REVIEW_REQUEST_FILE"
echo ""

# Cursor Agentにレビュー依頼を送信
echo "Cursor Agentにレビュー依頼を送信中..."
echo ""

# レビュー依頼メッセージ
REVIEW_MESSAGE="以下のファイルをレビューしてください:

@docs/github-copilot-review-request.md

特に以下の点を確認してください:
1. n8nワークフロー設計の妥当性
2. JSON形式の正確性（n8nでインポート可能か）
3. 式（expressions）の記述が正しいか
4. エラーハンドリングが適切か
5. セキュリティ設定が適切か

改善提案もお願いします。

レビュー対象ファイル:
- n8n-workflows-design.md
- workflow-1-trial-onboarding.json
- README-n8n-implementation.md"

# Cursor Agentに送信（標準入力経由）
echo "$REVIEW_MESSAGE" | cursor agent

echo ""
echo "レビュー依頼が送信されました。"





















