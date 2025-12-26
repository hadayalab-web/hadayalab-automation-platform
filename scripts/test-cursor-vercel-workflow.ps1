# Cursor-Vercelワークフローのテストスクリプト

$webhookUrl = "https://hadayalab.app.n8n.cloud/webhook-test/cursor-vercel-deploy"

Write-Host "=== Cursor-Vercelワークフローテスト ===" -ForegroundColor Cyan
Write-Host ""

# テストデータを準備
$testData = @{
    ref = "refs/heads/main"
    repository = @{
        name = "hadayalab-automation-platform"
        full_name = "hadayalab-web/hadayalab-automation-platform"
    }
    head_commit = @{
        id = "abc123def456"
        message = "Test: Cursor-Vercel workflow test"
        author = @{
            name = "Test User"
            email = "test@example.com"
        }
    }
} | ConvertTo-Json -Depth 10

Write-Host "[INFO] テストWebhookを送信しています..." -ForegroundColor Yellow
Write-Host "  URL: $webhookUrl" -ForegroundColor Gray
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri $webhookUrl `
        -Method POST `
        -ContentType "application/json" `
        -Headers @{
            "X-GitHub-Event" = "push"
        } `
        -Body $testData

    Write-Host "[OK] ワークフローが正常に実行されました！" -ForegroundColor Green
    Write-Host ""
    Write-Host "レスポンス:" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 10 | Write-Host
    Write-Host ""
    Write-Host "[INFO] 次のステップ:" -ForegroundColor Yellow
    Write-Host "1. n8n Dashboard → Executions で実行履歴を確認" -ForegroundColor Gray
    Write-Host "2. Vercel Dashboard でデプロイが開始されているか確認" -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "[ERROR] テスト実行に失敗しました" -ForegroundColor Red
    Write-Host "エラー: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "詳細: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "[INFO] トラブルシューティング:" -ForegroundColor Yellow
    Write-Host "1. ワークフローがActiveになっているか確認" -ForegroundColor Gray
    Write-Host "2. 環境変数 VERCEL_API_TOKEN が正しく設定されているか確認" -ForegroundColor Gray
    Write-Host "3. n8n Dashboard → Executions でエラーログを確認" -ForegroundColor Gray
    Write-Host ""
}
















