# 簡単なワークフロー作成スクリプト
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
$projectId = "446f131c-be8d-45e5-a83a-4154e34501a5"

# InfisicalからPersonal Access Tokenを取得
Write-Host "Personal Access Tokenを取得中..." -ForegroundColor Yellow
$resultJson = infisical secrets get N8N_API_KEY --token $token --projectId $projectId --output json 2>&1 | Select-String -Pattern '\[.*\]' | ForEach-Object { $_.Matches.Value }
$result = $resultJson | ConvertFrom-Json
$apiKey = $result.secretValue

# ワークフローファイルを読み込む
Write-Host "ワークフローファイルを読み込んでいます..." -ForegroundColor Cyan
$workflowJson = Get-Content -Path "workflows/simple-time-check.json" -Raw -Encoding UTF8
$workflow = $workflowJson | ConvertFrom-Json

# n8n REST APIエンドポイント
$apiEndpoint = "https://hadayalab.app.n8n.cloud/rest/workflows"

# ヘッダーを設定
$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/json"
}

# ペイロードを準備
$payload = @{
    name = $workflow.name
    nodes = $workflow.nodes
    connections = $workflow.connections
    settings = $workflow.settings
    staticData = $workflow.staticData
    tags = $workflow.tags
} | ConvertTo-Json -Depth 100

# ワークフローを作成
Write-Host "`nワークフローを作成しています..." -ForegroundColor Yellow
Write-Host "ワークフロー名: $($workflow.name)" -ForegroundColor Gray

try {
    $response = Invoke-RestMethod -Uri $apiEndpoint -Method Post -Headers $headers -Body $payload -ErrorAction Stop

    Write-Host "`nワークフローが正常に作成されました！" -ForegroundColor Green
    Write-Host "`nワークフロー情報:" -ForegroundColor Cyan
    Write-Host "  ID: $($response.id)" -ForegroundColor White
    Write-Host "  名前: $($response.name)" -ForegroundColor White
    Write-Host "  状態: $($response.active)" -ForegroundColor White
    Write-Host "  URL: https://hadayalab.app.n8n.cloud/workflow/$($response.id)" -ForegroundColor White

    # Webhook URLを表示
    $webhookNode = $workflow.nodes | Where-Object { $_.type -eq "n8n-nodes-base.webhook" }
    if ($webhookNode) {
        $webhookId = $webhookNode.webhookId
        if ($webhookId) {
            Write-Host "`nWebhook URL:" -ForegroundColor Cyan
            Write-Host "  https://hadayalab.app.n8n.cloud/webhook/$webhookId" -ForegroundColor White
        }
    }

    # ワークフローIDを保存（後でテスト用に使用）
    $response.id | Out-File -FilePath "workflow-id.txt" -Encoding UTF8

} catch {
    Write-Host "`nエラーが発生しました:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red

    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "HTTPステータス: $statusCode" -ForegroundColor Red
    }
}















