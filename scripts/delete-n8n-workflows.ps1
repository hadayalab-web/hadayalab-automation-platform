# n8nワークフロー削除スクリプト
# 使用方法: .\scripts\delete-n8n-workflows.ps1 -Token "YOUR_PERSONAL_ACCESS_TOKEN"

param(
    [Parameter(Mandatory=$true)]
    [string]$Token,

    [Parameter(Mandatory=$false)]
    [string[]]$WorkflowIds = @("EE7Thl6p9Zsmfns4", "p7SxbAZbmnGscON3")
)

# APIエンドポイント
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"

# ヘッダー設定
$headers = @{
    "Authorization" = "Bearer $Token"
    "Content-Type" = "application/json"
}

Write-Host "=== n8nワークフロー削除 ===" -ForegroundColor Cyan
Write-Host ""

foreach ($workflowId in $WorkflowIds) {
    Write-Host "ワークフローID: $workflowId を削除中..." -ForegroundColor Yellow

    try {
        # まずワークフロー情報を取得
        $workflowUrl = "$baseUrl/workflows/$workflowId"
        $workflow = Invoke-RestMethod -Uri $workflowUrl -Method Get -Headers $headers

        Write-Host "  ワークフロー名: $($workflow.name)" -ForegroundColor Gray
        Write-Host "  状態: $(if ($workflow.active) { 'Active' } else { 'Inactive' })" -ForegroundColor Gray

        # ワークフローを削除
        $response = Invoke-RestMethod -Uri $workflowUrl -Method Delete -Headers $headers

        Write-Host "  ✅ 削除成功" -ForegroundColor Green
        Write-Host ""
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        $errorMessage = $_.Exception.Message

        if ($statusCode -eq 404) {
            Write-Host "  ⚠️ ワークフローが見つかりません（既に削除されている可能性）" -ForegroundColor Yellow
        }
        elseif ($statusCode -eq 401) {
            Write-Host "  ❌ 認証エラー: Personal Access Tokenが無効です" -ForegroundColor Red
        }
        else {
            Write-Host "  ❌ エラー: $errorMessage (ステータスコード: $statusCode)" -ForegroundColor Red
        }
        Write-Host ""
    }
}

Write-Host "=== 削除処理完了 ===" -ForegroundColor Cyan
















