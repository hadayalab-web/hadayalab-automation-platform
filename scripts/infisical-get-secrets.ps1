# Infisicalからシークレットを取得するスクリプト
# 使用方法: .\scripts\infisical-get-secrets.ps1

# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Infisical設定
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
$projectId = "446f131c-be8d-45e5-a83a-4154e34501a5"

Write-Host "=== Infisicalからシークレットを取得 ===" -ForegroundColor Green
Write-Host ""

# N8N_API_KEYを取得
Write-Host "N8N_API_KEY を取得中..." -ForegroundColor Yellow
$n8nApiKey = (infisical secrets get N8N_API_KEY --token $token --projectId $projectId --output plain 2>&1 | Select-String -Pattern "N8N_API_KEY" | ForEach-Object { $_.Line -replace '.*N8N_API_KEY\s+', '' -replace '\s+shared.*', '' }).Trim()

# N8N_API_URLを取得
Write-Host "N8N_API_URL を取得中..." -ForegroundColor Yellow
$n8nApiUrl = (infisical secrets get N8N_API_URL --token $token --projectId $projectId --output plain 2>&1 | Select-String -Pattern "N8N_API_URL" | ForEach-Object { $_.Line -replace '.*N8N_API_URL\s+', '' -replace '\s+shared.*', '' }).Trim()

# 環境変数に設定
$env:N8N_API_KEY = $n8nApiKey
$env:N8N_API_URL = $n8nApiUrl

Write-Host ""
Write-Host "✓ シークレットを取得しました" -ForegroundColor Green
Write-Host ""
Write-Host "環境変数に設定されました:" -ForegroundColor Cyan
Write-Host "  N8N_API_KEY = $($env:N8N_API_KEY.Substring(0, [Math]::Min(50, $env:N8N_API_KEY.Length)))..." -ForegroundColor Gray
Write-Host "  N8N_API_URL = $env:N8N_API_URL" -ForegroundColor Gray
Write-Host ""
Write-Host "これらの環境変数は、現在のPowerShellセッションでのみ有効です。" -ForegroundColor Yellow
Write-Host "Cursorを起動する前に、このスクリプトを実行してください。" -ForegroundColor Yellow





















