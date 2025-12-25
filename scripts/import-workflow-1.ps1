# ワークフロー1をn8nにインポートするスクリプト
# 使用方法: .\scripts\import-workflow-1.ps1

# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Infisical設定
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
$projectId = "446f131c-be8d-45e5-a83a-4154e34501a5"

# n8nプロジェクトID
$n8nProjectId = "9D29Es58GIo6IPkZ"

Write-Host "=== ワークフロー1をn8nにインポート ===" -ForegroundColor Green
Write-Host "n8nプロジェクトID: $n8nProjectId" -ForegroundColor Cyan
Write-Host ""

# Personal Access Tokenを取得
Write-Host "Personal Access Tokenを取得中..." -ForegroundColor Yellow
try {
    $personalAccessTokenJson = infisical secrets get N8N_PERSONAL_ACCESS_TOKEN --token $token --projectId $projectId --output json 2>&1 | Out-String
    $personalAccessTokenObj = $personalAccessTokenJson | ConvertFrom-Json
    $personalAccessToken = $personalAccessTokenObj[0].secretValue

    if ([string]::IsNullOrEmpty($personalAccessToken)) {
        Write-Host "エラー: Personal Access Tokenが取得できませんでした" -ForegroundColor Red
        exit 1
    }

    Write-Host "✓ Personal Access Tokenを取得しました" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "エラー: Personal Access Tokenの取得に失敗しました" -ForegroundColor Red
    exit 1
}

# ワークフローJSONファイルを読み込む
$workflowJsonPath = "workflow-1-trial-onboarding.json"
if (-not (Test-Path $workflowJsonPath)) {
    Write-Host "エラー: ワークフローファイルが見つかりません: $workflowJsonPath" -ForegroundColor Red
    exit 1
}

Write-Host "ワークフローファイルを読み込み中: $workflowJsonPath" -ForegroundColor Yellow
$workflowJson = Get-Content $workflowJsonPath -Raw | ConvertFrom-Json

# プロジェクトIDを追加
if ($workflowJson.PSObject.Properties.Name -notcontains "projectId") {
    $workflowJson | Add-Member -MemberType NoteProperty -Name "projectId" -Value $n8nProjectId
} else {
    $workflowJson.projectId = $n8nProjectId
}

# APIエンドポイント
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"

# ヘッダー設定
$headers = @{
    "Authorization" = "Bearer $personalAccessToken"
    "Content-Type" = "application/json"
}

# ワークフローをインポート
Write-Host "ワークフローをn8nにインポート中..." -ForegroundColor Yellow
try {
    $body = $workflowJson | ConvertTo-Json -Depth 100
    $uri = "$baseUrl/workflows"

    Write-Host "  URL: $uri" -ForegroundColor Gray
    Write-Host "  ワークフロー名: $($workflowJson.name)" -ForegroundColor Gray

    $response = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body -ErrorAction Stop

    Write-Host "✓ ワークフローのインポートに成功しました！" -ForegroundColor Green
    Write-Host "  ワークフローID: $($response.data.id)" -ForegroundColor Cyan
    Write-Host "  ワークフロー名: $($response.data.name)" -ForegroundColor Cyan
    Write-Host "  ステータス: $($response.data.active)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "ワークフローURL: https://hadayalab.app.n8n.cloud/workflow/$($response.data.id)?projectId=$n8nProjectId" -ForegroundColor Cyan
    Write-Host ""
} catch {
    Write-Host "✗ ワークフローのインポートに失敗しました" -ForegroundColor Red
    Write-Host "エラー: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "レスポンス: $responseBody" -ForegroundColor Gray
    }
    Write-Host ""
    exit 1
}

Write-Host "=== インポート完了 ===" -ForegroundColor Green











