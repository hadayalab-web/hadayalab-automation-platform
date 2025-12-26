# n8n環境変数取得スクリプト（簡易版）

$baseUrl = "https://hadayalab.app.n8n.cloud"
$accessToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ZDcxM2YyMS0wZDBiLTRhYmUtYWZjNy1kYjc2MmQ4YWUzMzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJtY3Atc2VydmVyLWFwaSIsImp0aSI6ImY4YjAwMzg0LTExMjAtNGNlNS04NjQ2LTNmZWY2N2RlZTEyOSIsImlhdCI6MTc2NjU2Mzg3OX0.AmAxwL2nY7oPJblEbLz5FRwXDpc4A5dSIfsP4Ha28Qw"

Write-Host "=== n8n環境変数取得 ===" -ForegroundColor Cyan
Write-Host ""

$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type" = "application/json"
}

$endpoint1 = "$baseUrl/rest/variables"
$endpoint2 = "$baseUrl/api/v1/variables"
$endpoint3 = "$baseUrl/rest/environment-variables"
$endpoint4 = "$baseUrl/api/v1/environment-variables"

$found = $false

Write-Host "エンドポイント1を試行中: $endpoint1" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod -Uri $endpoint1 -Method Get -Headers $headers -TimeoutSec 10 -ErrorAction Stop
    Write-Host "  [OK] 接続成功" -ForegroundColor Green
    Write-Host ""
    Write-Host "=== 環境変数一覧 ===" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 10
    $found = $true
} catch {
    Write-Host "  [NG] エラー: $($_.Exception.Message)" -ForegroundColor Yellow
}

if (-not $found) {
    Write-Host ""
    Write-Host "エンドポイント2を試行中: $endpoint2" -ForegroundColor Gray
    try {
        $response = Invoke-RestMethod -Uri $endpoint2 -Method Get -Headers $headers -TimeoutSec 10 -ErrorAction Stop
        Write-Host "  [OK] 接続成功" -ForegroundColor Green
        Write-Host ""
        Write-Host "=== 環境変数一覧 ===" -ForegroundColor Cyan
        $response | ConvertTo-Json -Depth 10
        $found = $true
    } catch {
        Write-Host "  [NG] エラー: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

if (-not $found) {
    Write-Host ""
    Write-Host "⚠️ REST API経由での環境変数取得に失敗しました" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "代替方法:" -ForegroundColor Cyan
    Write-Host "1. n8n Dashboardから確認:" -ForegroundColor White
    Write-Host "   https://hadayalab.app.n8n.cloud → Settings → Environment Variables" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. n8nネイティブMCPを使用:" -ForegroundColor White
    Write-Host "   Cursor Chatで @n8n-cloud 環境変数を取得して" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== テスト完了 ===" -ForegroundColor Cyan















