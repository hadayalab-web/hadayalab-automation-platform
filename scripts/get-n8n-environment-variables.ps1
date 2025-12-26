# n8n環境変数取得スクリプト
# 使用方法: .\scripts\get-n8n-environment-variables.ps1

$baseUrl = "https://hadayalab.app.n8n.cloud"
$accessToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ZDcxM2YyMS0wZDBiLTRhYmUtYWZjNy1kYjc2MmQ4YWUzMzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJtY3Atc2VydmVyLWFwaSIsImp0aSI6ImY4YjAwMzg0LTExMjAtNGNlNS04NjQ2LTNmZWY2N2RlZTEyOSIsImlhdCI6MTc2NjU2Mzg3OX0.AmAxwL2nY7oPJblEbLz5FRwXDpc4A5dSIfsP4Ha28Qw"

Write-Host "=== n8n環境変数取得 ===" -ForegroundColor Cyan
Write-Host ""

# n8n REST APIで環境変数を取得
# 注意: MCP Access TokenはREST APIでは使用できない可能性があります
# その場合は、n8n Dashboardから手動で確認する必要があります

$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type" = "application/json"
}

# 方法1: REST APIエンドポイントを試す
$endpoints = @(
    "$baseUrl/rest/variables",
    "$baseUrl/api/v1/variables",
    "$baseUrl/rest/environment-variables",
    "$baseUrl/api/v1/environment-variables"
)

$found = $false
foreach ($endpoint in $endpoints) {
    Write-Host "試行中: $endpoint" -ForegroundColor Gray
    try {
        $response = Invoke-RestMethod -Uri $endpoint -Method Get -Headers $headers -TimeoutSec 10 -ErrorAction Stop
        Write-Host "  [OK] 接続成功" -ForegroundColor Green
        Write-Host ""
        Write-Host "=== 環境変数一覧 ===" -ForegroundColor Cyan
        if ($response -is [Array]) {
            foreach ($var in $response) {
                if ($var.key) {
                    Write-Host "  $($var.key): $($var.value)" -ForegroundColor White
                } elseif ($var.name) {
                    Write-Host "  $($var.name): $($var.value)" -ForegroundColor White
                } else {
                    Write-Host "  $($var | ConvertTo-Json -Compress)" -ForegroundColor White
                }
            }
        } elseif ($response.data) {
            foreach ($var in $response.data) {
                if ($var.key) {
                    Write-Host "  $($var.key): $($var.value)" -ForegroundColor White
                } elseif ($var.name) {
                    Write-Host "  $($var.name): $($var.value)" -ForegroundColor White
                } else {
                    Write-Host "  $($var | ConvertTo-Json -Compress)" -ForegroundColor White
                }
            }
        } else {
            Write-Host $response | ConvertTo-Json -Depth 10 -ForegroundColor White
        }
        $found = $true
        break
    } catch {
        $statusCode = $null
        if ($_.Exception.Response) {
            $statusCode = $_.Exception.Response.StatusCode.value__
        }
        if ($statusCode -eq 401) {
            Write-Host "  [NG] 認証エラー (401)" -ForegroundColor Red
        } elseif ($statusCode -eq 404) {
            Write-Host "  [NG] エンドポイントが見つかりません (404)" -ForegroundColor Yellow
        } else {
            Write-Host "  [NG] エラー: $($_.Exception.Message)" -ForegroundColor Yellow
        }
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














