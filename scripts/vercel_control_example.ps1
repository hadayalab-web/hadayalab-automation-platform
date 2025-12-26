# Cursor-Vercel Control 使用例スクリプト (PowerShell)
# このスクリプトは、CursorからVercelを制御する方法の例を示します

# 環境変数の設定（実際の値に置き換えてください）
$env:VERCEL_API_TOKEN = "vck_xxxxx"
$PROJECT_ID = "prj_xxxxx"
$PROJECT_NAME = "my-project"
$REPOSITORY = "owner/repo"
$DEPLOYMENT_ID = "dpl_xxxxx"

Write-Host "=== Cursor-Vercel Control 使用例 ===" -ForegroundColor Cyan
Write-Host ""

# 1. デプロイメント作成
Write-Host "1. デプロイメント作成" -ForegroundColor Yellow
python scripts/vercel_control.py deploy `
  --project $PROJECT_NAME `
  --repo $REPOSITORY `
  --branch main
Write-Host ""

# 2. デプロイメントステータス確認
Write-Host "2. デプロイメントステータス確認" -ForegroundColor Yellow
python scripts/vercel_control.py status `
  --deployment-id $DEPLOYMENT_ID
Write-Host ""

# 3. デプロイメント一覧取得
Write-Host "3. デプロイメント一覧取得" -ForegroundColor Yellow
python scripts/vercel_control.py list `
  --project-id $PROJECT_ID `
  --limit 10
Write-Host ""

# 4. デプロイメントログ取得
Write-Host "4. デプロイメントログ取得" -ForegroundColor Yellow
python scripts/vercel_control.py logs `
  --deployment-id $DEPLOYMENT_ID
Write-Host ""

# 5. プロジェクト情報取得
Write-Host "5. プロジェクト情報取得" -ForegroundColor Yellow
python scripts/vercel_control.py project `
  --project-id $PROJECT_ID
Write-Host ""

# 6. プロジェクト一覧取得
Write-Host "6. プロジェクト一覧取得" -ForegroundColor Yellow
python scripts/vercel_control.py projects
Write-Host ""

# 7. 環境変数一覧取得
Write-Host "7. 環境変数一覧取得" -ForegroundColor Yellow
python scripts/vercel_control.py env list `
  --project-id $PROJECT_ID
Write-Host ""

# 8. 環境変数作成
Write-Host "8. 環境変数作成" -ForegroundColor Yellow
python scripts/vercel_control.py env create `
  --project-id $PROJECT_ID `
  --key EXAMPLE_KEY `
  --value example_value `
  --target production preview development
Write-Host ""

Write-Host "=== 完了 ===" -ForegroundColor Green















