# n8n API接続テストスクリプト
# 使用方法: .\scripts\test-n8n-connection.ps1

# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Infisical設定
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
$projectId = "446f131c-be8d-45e5-a83a-4154e34501a5"

Write-Host "=== n8n API接続テスト ===" -ForegroundColor Green
Write-Host ""

# シークレットを取得
Write-Host "シークレットを取得中..." -ForegroundColor Yellow
$n8nApiKeyJson = infisical secrets get N8N_API_KEY --token $token --projectId $projectId --output json 2>&1 | Out-String
$n8nApiUrlJson = infisical secrets get N8N_API_URL --token $token --projectId $projectId --output json 2>&1 | Out-String

# JSONをパース
$n8nApiKeyObj = $n8nApiKeyJson | ConvertFrom-Json
$n8nApiUrlObj = $n8nApiUrlJson | ConvertFrom-Json

$n8nApiKey = $n8nApiKeyObj[0].secretValue
$n8nApiUrl = $n8nApiUrlObj[0].secretValue

Write-Host "✓ シークレットを取得しました" -ForegroundColor Green
Write-Host "  N8N_API_URL: $n8nApiUrl" -ForegroundColor Gray
Write-Host "  N8N_API_KEY: $($n8nApiKey.Substring(0, [Math]::Min(50, $n8nApiKey.Length)))..." -ForegroundColor Gray
Write-Host ""

# n8n APIエンドポイントを推測
# MCPサーバーのURLから通常のAPIエンドポイントを推測
if ($n8nApiUrl -match "https://([^/]+)\.app\.n8n\.cloud") {
    $instanceName = $matches[1]
    $n8nApiBaseUrl = "https://$instanceName.app.n8n.cloud/api/v1"
    Write-Host "推測されたAPIエンドポイント: $n8nApiBaseUrl" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "⚠️  APIエンドポイントを推測できませんでした" -ForegroundColor Yellow
    Write-Host ""
}

# テスト1: ワークフロー一覧取得（通常のAPIエンドポイント）
Write-Host "テスト1: ワークフロー一覧取得（通常のAPIエンドポイント）" -ForegroundColor Yellow
try {
    $headers = @{
        "X-N8N-API-KEY" = $n8nApiKey
        "Content-Type" = "application/json"
    }

    $response = Invoke-RestMethod -Uri "$n8nApiBaseUrl/workflows" -Method Get -Headers $headers -ErrorAction Stop
    Write-Host "✓ 接続成功！" -ForegroundColor Green
    Write-Host "  ワークフロー数: $($response.data.Count)" -ForegroundColor Cyan
    if ($response.data.Count -gt 0) {
        Write-Host "  ワークフロー一覧:" -ForegroundColor Cyan
        foreach ($workflow in $response.data) {
            Write-Host "    - $($workflow.name) (ID: $($workflow.id), Active: $($workflow.active))" -ForegroundColor Gray
        }
    }
    Write-Host ""
} catch {
    Write-Host "✗ 接続失敗: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

# テスト2: MCPサーバーエンドポイント（参考）
Write-Host "テスト2: MCPサーバーエンドポイント（参考）" -ForegroundColor Yellow
Write-Host "  MCPサーバーURL: $n8nApiUrl" -ForegroundColor Gray
Write-Host "  （このエンドポイントはMCPサーバー用です）" -ForegroundColor Gray
Write-Host ""

# テスト3: インスタンス情報取得
Write-Host "テスト3: インスタンス情報取得" -ForegroundColor Yellow
try {
    $headers = @{
        "X-N8N-API-KEY" = $n8nApiKey
        "Content-Type" = "application/json"
    }

    $response = Invoke-RestMethod -Uri "$n8nApiBaseUrl/instance" -Method Get -Headers $headers -ErrorAction Stop
    Write-Host "✓ インスタンス情報取得成功！" -ForegroundColor Green
    Write-Host "  インスタンス名: $($response.data.instanceName)" -ForegroundColor Cyan
    Write-Host "  バージョン: $($response.data.version)" -ForegroundColor Cyan
    Write-Host ""
} catch {
    Write-Host "✗ インスタンス情報取得失敗: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

Write-Host "=== テスト完了 ===" -ForegroundColor Green

