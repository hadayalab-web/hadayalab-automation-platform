# n8nダッシュボードアクセステストスクリプト

$baseUrl = "https://hadayalab.app.n8n.cloud"
$mcpUrl = "https://hadayalab.app.n8n.cloud/mcp-server/http"
$accessToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ZDcxM2YyMS0wZDBiLTRhYmUtYWZjNy1kYjc2MmQ4YWUzMzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJtY3Atc2VydmVyLWFwaSIsImp0aSI6ImY4YjAwMzg0LTExMjAtNGNlNS04NjQ2LTNmZWY2N2RlZTEyOSIsImlhdCI6MTc2NjU2Mzg3OX0.AmAxwL2nY7oPJblEbLz5FRwXDpc4A5dSIfsP4Ha28Qw"

Write-Host "=== n8nダッシュボードアクセステスト ===" -ForegroundColor Cyan
Write-Host ""

# テスト1: ダッシュボードへの基本接続
Write-Host "テスト1: ダッシュボードへの基本接続" -ForegroundColor Yellow
Write-Host "URL: $baseUrl" -ForegroundColor Gray
try {
    $response = Invoke-WebRequest -Uri $baseUrl -Method Get -TimeoutSec 10 -UseBasicParsing
    Write-Host "  [OK] 接続成功 - ステータスコード: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "  [NG] 接続失敗: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        Write-Host "  HTTPステータス: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Yellow
    }
}
Write-Host ""

# テスト2: MCP Server URLへの接続（認証なし）
Write-Host "テスト2: MCP Server URLへの接続（認証なし）" -ForegroundColor Yellow
Write-Host "URL: $mcpUrl" -ForegroundColor Gray
try {
    $response = Invoke-WebRequest -Uri $mcpUrl -Method Get -TimeoutSec 10 -UseBasicParsing
    Write-Host "  [OK] 接続成功 - ステータスコード: $($response.StatusCode)" -ForegroundColor Green
} catch {
    $statusCode = $null
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
    }
    if ($statusCode -eq 401) {
        Write-Host "  [OK] 認証が必要（これは正常です） - ステータスコード: 401" -ForegroundColor Green
    } elseif ($statusCode -eq 404) {
        Write-Host "  [NG] エンドポイントが見つかりません - ステータスコード: 404" -ForegroundColor Red
    } else {
        Write-Host "  [WARN] 接続結果: $($_.Exception.Message)" -ForegroundColor Yellow
        if ($statusCode) {
            Write-Host "  HTTPステータス: $statusCode" -ForegroundColor Yellow
        }
    }
}
Write-Host ""

# テスト3: MCP Server URLへの接続（認証あり）
Write-Host "テスト3: MCP Server URLへの接続（認証あり）" -ForegroundColor Yellow
Write-Host "URL: $mcpUrl" -ForegroundColor Gray
Write-Host "認証トークンを使用" -ForegroundColor Gray
$headers = @{
    "Authorization" = "Bearer $accessToken"
}
try {
    $response = Invoke-WebRequest -Uri $mcpUrl -Method Get -Headers $headers -TimeoutSec 10 -UseBasicParsing
    Write-Host "  [OK] 認証成功 - ステータスコード: $($response.StatusCode)" -ForegroundColor Green
} catch {
    $statusCode = $null
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
    }
    if ($statusCode -eq 401) {
        Write-Host "  [NG] 認証失敗 - トークンが無効の可能性 - ステータスコード: 401" -ForegroundColor Red
    } elseif ($statusCode -eq 404) {
        Write-Host "  [NG] エンドポイントが見つかりません - ステータスコード: 404" -ForegroundColor Red
    } else {
        Write-Host "  [WARN] 接続結果: $($_.Exception.Message)" -ForegroundColor Yellow
        if ($statusCode) {
            Write-Host "  HTTPステータス: $statusCode" -ForegroundColor Yellow
        }
    }
}
Write-Host ""

Write-Host "=== テスト完了 ===" -ForegroundColor Cyan















