# n8nワークフロー削除スクリプト（簡易版）
# 使用方法: .\scripts\delete-n8n-workflow-simple.ps1 -WorkflowId "zUDOwmEtb3y81F3G" -ApiKey "YOUR_N8N_API_KEY"

param(
    [Parameter(Mandatory=$true)]
    [string]$WorkflowId,

    [Parameter(Mandatory=$true)]
    [string]$ApiKey
)

$baseUrl = "https://hadayalab.app.n8n.cloud/rest"
$headers = @{
    "Authorization" = "Bearer $ApiKey"
    "Content-Type" = "application/json"
}

Write-Host "=== n8nワークフロー削除 ===" -ForegroundColor Cyan
Write-Host "ワークフローID: $WorkflowId" -ForegroundColor Yellow
Write-Host ""

try {
    # まずワークフロー情報を取得
    $workflowUrl = "$baseUrl/workflows/$WorkflowId"
    $workflow = Invoke-RestMethod -Uri $workflowUrl -Method Get -Headers $headers

    Write-Host "ワークフロー名: $($workflow.name)" -ForegroundColor Gray
    Write-Host "状態: $(if ($workflow.active) { 'Active' } else { 'Inactive' })" -ForegroundColor Gray
    Write-Host ""

    # ワークフローを削除
    Invoke-RestMethod -Uri $workflowUrl -Method Delete -Headers $headers

    Write-Host "✅ 削除成功" -ForegroundColor Green
}
catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    $errorMessage = $_.Exception.Message

    if ($statusCode -eq 404) {
        Write-Host "⚠️ ワークフローが見つかりません（既に削除されている可能性）" -ForegroundColor Yellow
    }
    elseif ($statusCode -eq 401) {
        Write-Host "❌ 認証エラー: API Keyが無効です" -ForegroundColor Red
    }
    else {
        Write-Host "❌ エラー: $errorMessage (ステータスコード: $statusCode)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== 削除処理完了 ===" -ForegroundColor Cyan















