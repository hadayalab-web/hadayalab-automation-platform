# GitHub Copilotレビュー依頼スクリプト (PowerShell)

Write-Host "=== GitHub Copilotレビュー依頼 ===" -ForegroundColor Cyan
Write-Host ""

# レビュー依頼ファイルを確認
$ReviewRequestFile = "docs\github-copilot-review-request.md"

if (-not (Test-Path $ReviewRequestFile)) {
    Write-Host "エラー: $ReviewRequestFile が見つかりません" -ForegroundColor Red
    exit 1
}

Write-Host "レビュー依頼ファイル: $ReviewRequestFile" -ForegroundColor Green
Write-Host ""

# レビュー依頼メッセージ
$ReviewMessage = @"
以下のファイルをレビューしてください:

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
- README-n8n-implementation.md
"@

Write-Host "Cursor Agentにレビュー依頼を送信中..." -ForegroundColor Yellow
Write-Host ""

# Cursor Agentに送信
$ReviewMessage | cursor agent

Write-Host ""
Write-Host "レビュー依頼が送信されました。" -ForegroundColor Green


