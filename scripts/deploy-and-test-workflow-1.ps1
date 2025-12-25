# ワークフロー1のデプロイ・テスト・デバッグスクリプト
# 使用方法: .\scripts\deploy-and-test-workflow-1.ps1

# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Infisical設定
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
$projectId = "446f131c-be8d-45e5-a83a-4154e34501a5"

# n8nプロジェクトID
$n8nProjectId = "9D29Es58GIo6IPkZ"

Write-Host "=== ワークフロー1のデプロイ・テスト・デバッグ ===" -ForegroundColor Green
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
        Write-Host ""
        Write-Host "次の手順を実行してください:" -ForegroundColor Yellow
        Write-Host "1. n8n Cloud Dashboard -> Settings -> API -> Personal Access Tokens" -ForegroundColor Cyan
        Write-Host "2. トークンを作成してInfisicalに保存 (N8N_PERSONAL_ACCESS_TOKEN)" -ForegroundColor Cyan
        exit 1
    }

    Write-Host "✓ Personal Access Tokenを取得しました" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "エラー: Personal Access Tokenの取得に失敗しました" -ForegroundColor Red
    Write-Host "エラー詳細: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# APIエンドポイント
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"

# ヘッダー設定
$headers = @{
    "Authorization" = "Bearer $personalAccessToken"
    "Content-Type" = "application/json"
}

# ワークフローJSONファイルを読み込む
$workflowJsonPath = "workflow-1-trial-onboarding.json"
if (-not (Test-Path $workflowJsonPath)) {
    Write-Host "エラー: ワークフローファイルが見つかりません: $workflowJsonPath" -ForegroundColor Red
    exit 1
}

Write-Host "ワークフローファイルを読み込み中: $workflowJsonPath" -ForegroundColor Yellow
$workflowJson = Get-Content $workflowJsonPath -Raw -Encoding UTF8 | ConvertFrom-Json

# プロジェクトIDを追加
if ($workflowJson.PSObject.Properties.Name -notcontains "projectId") {
    $workflowJson | Add-Member -MemberType NoteProperty -Name "projectId" -Value $n8nProjectId
} else {
    $workflowJson.projectId = $n8nProjectId
}

# activeフラグをfalseに設定（テスト後に有効化）
if ($workflowJson.PSObject.Properties.Name -notcontains "active") {
    $workflowJson | Add-Member -MemberType NoteProperty -Name "active" -Value $false
} else {
    $workflowJson.active = $false
}

# ステップ1: ワークフローをインポート
Write-Host ""
Write-Host "=== ステップ1: ワークフローのインポート ===" -ForegroundColor Green
try {
    $body = $workflowJson | ConvertTo-Json -Depth 100
    $uri = "$baseUrl/workflows"

    Write-Host "ワークフローをn8nにインポート中..." -ForegroundColor Yellow
    Write-Host "  URL: $uri" -ForegroundColor Gray
    Write-Host "  ワークフロー名: $($workflowJson.name)" -ForegroundColor Gray

    $response = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body -ErrorAction Stop

    $workflowId = $response.data.id
    Write-Host "✓ ワークフローのインポートに成功しました！" -ForegroundColor Green
    Write-Host "  ワークフローID: $workflowId" -ForegroundColor Cyan
    Write-Host "  ワークフロー名: $($response.data.name)" -ForegroundColor Cyan
    Write-Host "  ステータス: $($response.data.active)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "ワークフローURL: https://hadayalab.app.n8n.cloud/workflow/$workflowId?projectId=$n8nProjectId" -ForegroundColor Cyan
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

# ステップ2: ワークフローの検証
Write-Host "=== ステップ2: ワークフローの検証 ===" -ForegroundColor Green
try {
    $validateUri = "$baseUrl/workflows/$workflowId/validate"
    Write-Host "ワークフローを検証中..." -ForegroundColor Yellow

    $validateResponse = Invoke-RestMethod -Uri $validateUri -Method Post -Headers $headers -ErrorAction Stop

    if ($validateResponse.valid) {
        Write-Host "✓ ワークフローは有効です" -ForegroundColor Green
    } else {
        Write-Host "⚠ ワークフローに問題があります" -ForegroundColor Yellow
        if ($validateResponse.errors) {
            Write-Host "エラー:" -ForegroundColor Red
            $validateResponse.errors | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
        }
    }
    Write-Host ""
} catch {
    Write-Host "⚠ ワークフローの検証に失敗しました（このエンドポイントが存在しない可能性があります）" -ForegroundColor Yellow
    Write-Host "エラー: $($_.Exception.Message)" -ForegroundColor Gray
    Write-Host ""
}

# ステップ3: ワークフローの詳細情報を取得
Write-Host "=== ステップ3: ワークフローの詳細情報 ===" -ForegroundColor Green
try {
    $getUri = "$baseUrl/workflows/$workflowId"
    Write-Host "ワークフローの詳細を取得中..." -ForegroundColor Yellow

    $workflowDetails = Invoke-RestMethod -Uri $getUri -Method Get -Headers $headers -ErrorAction Stop

    Write-Host "✓ ワークフローの詳細を取得しました" -ForegroundColor Green
    Write-Host "  ノード数: $($workflowDetails.data.nodes.Count)" -ForegroundColor Cyan
    Write-Host "  接続数: $($workflowDetails.data.connections.PSObject.Properties.Count)" -ForegroundColor Cyan
    Write-Host ""

    # ノード一覧を表示
    Write-Host "ノード一覧:" -ForegroundColor Yellow
    foreach ($node in $workflowDetails.data.nodes) {
        Write-Host "  - $($node.name) ($($node.type))" -ForegroundColor Gray
    }
    Write-Host ""
} catch {
    Write-Host "✗ ワークフローの詳細取得に失敗しました" -ForegroundColor Red
    Write-Host "エラー: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

# ステップ4: Webhook URLの取得
Write-Host "=== ステップ4: Webhook URLの確認 ===" -ForegroundColor Green
try {
    $webhookNode = $workflowDetails.data.nodes | Where-Object { $_.type -eq "n8n-nodes-base.webhook" }
    if ($webhookNode) {
        $webhookPath = $webhookNode.parameters.path
        $webhookUrl = "https://hadayalab.app.n8n.cloud/webhook/$webhookPath"
        Write-Host "✓ Webhook URLを取得しました" -ForegroundColor Green
        Write-Host "  Webhook URL: $webhookUrl" -ForegroundColor Cyan
        Write-Host "  Path: $webhookPath" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "テスト用curlコマンド:" -ForegroundColor Yellow
        Write-Host "curl -X POST $webhookUrl \`" -ForegroundColor Gray
        Write-Host "  -H `"Content-Type: application/json`" \`" -ForegroundColor Gray
        Write-Host "  -d '{`"user_email`":`"test@example.com`",`"user_name`":`"Test User`",`"market`":`"EN`",`"membership_id`":`"test123`"}'" -ForegroundColor Gray
        Write-Host ""
    } else {
        Write-Host "⚠ Webhookノードが見つかりませんでした" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠ Webhook URLの取得に失敗しました" -ForegroundColor Yellow
    Write-Host ""
}

# ステップ5: 実行履歴の確認
Write-Host "=== ステップ5: 実行履歴の確認 ===" -ForegroundColor Green
try {
    $executionsUri = "$baseUrl/executions?workflowId=$workflowId&limit=5"
    Write-Host "実行履歴を取得中..." -ForegroundColor Yellow

    $executions = Invoke-RestMethod -Uri $executionsUri -Method Get -Headers $headers -ErrorAction Stop

    if ($executions.data.Count -gt 0) {
        Write-Host "✓ 実行履歴を取得しました（最新$($executions.data.Count)件）" -ForegroundColor Green
        foreach ($execution in $executions.data) {
            $status = if ($execution.finished) { "完了" } else { "実行中" }
            $statusColor = if ($execution.finished -and $execution.stoppedAt) { "Green" } else { "Yellow" }
            Write-Host "  - $($execution.id): $status ($($execution.mode))" -ForegroundColor $statusColor
        }
    } else {
        Write-Host "  （実行履歴がありません）" -ForegroundColor Gray
    }
    Write-Host ""
} catch {
    Write-Host "⚠ 実行履歴の取得に失敗しました" -ForegroundColor Yellow
    Write-Host "エラー: $($_.Exception.Message)" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "=== デプロイ・テスト完了 ===" -ForegroundColor Green
Write-Host ""
Write-Host "次のステップ:" -ForegroundColor Yellow
Write-Host "1. n8n Dashboardでワークフローを開く" -ForegroundColor Cyan
Write-Host "   URL: https://hadayalab.app.n8n.cloud/workflow/$workflowId?projectId=$n8nProjectId" -ForegroundColor Cyan
Write-Host "2. 認証情報を設定（Gmail OAuth2、Whop API Key）" -ForegroundColor Cyan
Write-Host "3. ワークフローをテスト実行" -ForegroundColor Cyan
Write-Host "4. 問題がなければActive化" -ForegroundColor Cyan
Write-Host ""









