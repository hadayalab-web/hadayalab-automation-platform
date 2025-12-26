#!/bin/bash
# Cursor-Vercel Control 使用例スクリプト
# このスクリプトは、CursorからVercelを制御する方法の例を示します

# 環境変数の設定（実際の値に置き換えてください）
export VERCEL_API_TOKEN="vck_xxxxx"
PROJECT_ID="prj_xxxxx"
PROJECT_NAME="my-project"
REPOSITORY="owner/repo"
DEPLOYMENT_ID="dpl_xxxxx"

echo "=== Cursor-Vercel Control 使用例 ==="
echo ""

# 1. デプロイメント作成
echo "1. デプロイメント作成"
python scripts/vercel_control.py deploy \
  --project "$PROJECT_NAME" \
  --repo "$REPOSITORY" \
  --branch main
echo ""

# 2. デプロイメントステータス確認
echo "2. デプロイメントステータス確認"
python scripts/vercel_control.py status \
  --deployment-id "$DEPLOYMENT_ID"
echo ""

# 3. デプロイメント一覧取得
echo "3. デプロイメント一覧取得"
python scripts/vercel_control.py list \
  --project-id "$PROJECT_ID" \
  --limit 10
echo ""

# 4. デプロイメントログ取得
echo "4. デプロイメントログ取得"
python scripts/vercel_control.py logs \
  --deployment-id "$DEPLOYMENT_ID"
echo ""

# 5. プロジェクト情報取得
echo "5. プロジェクト情報取得"
python scripts/vercel_control.py project \
  --project-id "$PROJECT_ID"
echo ""

# 6. プロジェクト一覧取得
echo "6. プロジェクト一覧取得"
python scripts/vercel_control.py projects
echo ""

# 7. 環境変数一覧取得
echo "7. 環境変数一覧取得"
python scripts/vercel_control.py env list \
  --project-id "$PROJECT_ID"
echo ""

# 8. 環境変数作成
echo "8. 環境変数作成"
python scripts/vercel_control.py env create \
  --project-id "$PROJECT_ID" \
  --key EXAMPLE_KEY \
  --value example_value \
  --target production preview development
echo ""

echo "=== 完了 ==="















