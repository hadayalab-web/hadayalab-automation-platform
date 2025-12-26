# n8n REST API接続テストスクリプト
# 使用方法: .\scripts\test-n8n-rest-api.ps1

# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Infisical設定
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
$projectId = "446f131c-be8d-45e5-a83a-4154e34501a5"

Write-Host "=== n8n REST API接続テスト ===" -ForegroundColor Green
Write-Host ""

# Personal Access Tokenを取得
Write-Host "Personal Access Tokenを取得中..." -ForegroundColor Yellow
try {
    $personalAccessTokenJson = infisical secrets get N8N_PERSONAL_ACCESS_TOKEN --token $token --projectId $projectId --output json 2>&1 | Out-String
    $personalAccessTokenObj = $personalAccessTokenJson | ConvertFrom-Json
    $personalAccessToken = $personalAccessTokenObj[0].secretValue

    if ([string]::IsNullOrEmpty($personalAccessToken)) {
        Write-Host "エラー: Personal Access Tokenが取得できませんでした" -ForegroundColor Red
        Write-Host ""
        Write-Host "次の手順を実行してください:" -ForegroundColor Yellow
        Write-Host "1. n8n Cloud Dashboard → Settings → API → Personal Access Tokens" -ForegroundColor Cyan
        Write-Host "2. トークンを作成してInfisicalに保存 (N8N_PERSONAL_ACCESS_TOKEN)" -ForegroundColor Cyan
        exit 1
    }

    Write-Host "✓ Personal Access Tokenを取得しました" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "エラー: Personal Access Tokenの取得に失敗しました" -ForegroundColor Red
    Write-Host "エラー詳細: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "次の手順を実行してください:" -ForegroundColor Yellow
    Write-Host "1. n8n Cloud Dashboard → Settings → API → Personal Access Tokens" -ForegroundColor Cyan
    Write-Host "2. トークンを作成してInfisicalに保存 (N8N_PERSONAL_ACCESS_TOKEN)" -ForegroundColor Cyan
    exit 1
}

# APIエンドポイント
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"

# ヘッダー設定
$headers = @{
    "Authorization" = "Bearer $personalAccessToken"
    "Content-Type" = "application/json"
}

Write-Host "API Base URL: $baseUrl" -ForegroundColor Cyan
Write-Host ""

# テスト1: ワークフロー一覧取得
Write-Host "テスト1: ワークフロー一覧取得" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/workflows" -Method Get -Headers $headers -ErrorAction Stop
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
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "  レスポンス: $responseBody" -ForegroundColor Gray
    }
    Write-Host ""
}

# テスト2: インスタンス情報取得（存在する場合）
Write-Host "テスト2: インスタンス情報取得" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/instance" -Method Get -Headers $headers -ErrorAction Stop
    Write-Host "✓ インスタンス情報取得成功！" -ForegroundColor Green
    Write-Host "  インスタンス名: $($response.data.instanceName)" -ForegroundColor Cyan
    Write-Host "  バージョン: $($response.data.version)" -ForegroundColor Cyan
    Write-Host ""
} catch {
    Write-Host "✗ インスタンス情報取得失敗: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  （このエンドポイントが存在しない可能性があります）" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "=== テスト完了 ===" -ForegroundColor Green





















