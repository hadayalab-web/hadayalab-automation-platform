# n8nワークフロー作成スクリプト
# 使用方法: .\create-n8n-workflow.ps1 -WorkflowPath "workflows/simple-time-check.json" -ApiKey "YOUR_PERSONAL_ACCESS_TOKEN"

param(
    [Parameter(Mandatory=$true)]
    [string]$WorkflowPath,

    [Parameter(Mandatory=$true)]
    [string]$ApiKey,

    [Parameter(Mandatory=$false)]
    [string]$BaseUrl = "https://hadayalab.app.n8n.cloud"
)

# エラーハンドリング
$ErrorActionPreference = "Stop"

try {
    # ワークフローファイルの存在確認
    if (-not (Test-Path $WorkflowPath)) {
        Write-Host "エラー: ワークフローファイルが見つかりません: $WorkflowPath" -ForegroundColor Red
        exit 1
    }

    # ワークフローJSONを読み込む
    Write-Host "ワークフローファイルを読み込んでいます: $WorkflowPath" -ForegroundColor Cyan
    $workflowJson = Get-Content -Path $WorkflowPath -Raw -Encoding UTF8
    $workflow = $workflowJson | ConvertFrom-Json

    # n8n REST APIエンドポイント
    $apiEndpoint = "$BaseUrl/rest/workflows"

    # ヘッダーを設定
    $headers = @{
        "Authorization" = "Bearer $ApiKey"
        "Content-Type" = "application/json"
    }

    # ワークフロー作成用のペイロードを準備
    # n8n APIは特定のフィールドのみを受け付けるため、必要なフィールドのみを含める
    $payload = @{
        name = $workflow.name
        nodes = $workflow.nodes
        connections = $workflow.connections
        settings = $workflow.settings
        staticData = $workflow.staticData
        tags = $workflow.tags
    } | ConvertTo-Json -Depth 100

    Write-Host "`nワークフローを作成しています..." -ForegroundColor Yellow
    Write-Host "ワークフロー名: $($workflow.name)" -ForegroundColor Gray

    # REST APIを呼び出してワークフローを作成
    $response = Invoke-RestMethod -Uri $apiEndpoint -Method Post -Headers $headers -Body $payload -ErrorAction Stop

    Write-Host "`n✅ ワークフローが正常に作成されました！" -ForegroundColor Green
    Write-Host "`nワークフロー情報:" -ForegroundColor Cyan
    Write-Host "  ID: $($response.id)" -ForegroundColor White
    Write-Host "  名前: $($response.name)" -ForegroundColor White
    Write-Host "  状態: $($response.active)" -ForegroundColor White
    Write-Host "  URL: $BaseUrl/workflow/$($response.id)" -ForegroundColor White

    # ワークフローがWebhook Triggerを使用している場合、Webhook URLを表示
    $webhookNode = $workflow.nodes | Where-Object { $_.type -eq "n8n-nodes-base.webhook" }
    if ($webhookNode) {
        $webhookId = $webhookNode.webhookId
        if (-not $webhookId) {
            $webhookId = $webhookNode.parameters.webhookId
        }
        if ($webhookId) {
            Write-Host "`n📎 Webhook URL:" -ForegroundColor Cyan
            Write-Host "  $BaseUrl/webhook/$webhookId" -ForegroundColor White
        }
    }

    return $response

} catch {
    Write-Host "`n❌ エラーが発生しました:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red

    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        $statusDescription = $_.Exception.Response.StatusDescription

        Write-Host "`nHTTPステータス: $statusCode $statusDescription" -ForegroundColor Red

        # エラーレスポンスの詳細を取得
        try {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $responseBody = $reader.ReadToEnd()
            $reader.Close()

            if ($responseBody) {
                Write-Host "`nエラーレスポンス:" -ForegroundColor Red
                Write-Host $responseBody -ForegroundColor Yellow
            }
        } catch {
            # エラーレスポンスの読み取りに失敗した場合は無視
        }
    }

    exit 1
}

