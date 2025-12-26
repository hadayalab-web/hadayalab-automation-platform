# n8nワークフロー削除スクリプト（MCP Access Token使用）
# 使用方法: .\scripts\delete-n8n-workflows-with-mcp-token.ps1 -MCPToken "YOUR_MCP_ACCESS_TOKEN"

param(
    [Parameter(Mandatory=$true)]
    [string]$MCPToken,

    [Parameter(Mandatory=$false)]
    [string[]]$WorkflowIds = @("EE7Thl6p9Zsmfns4", "p7SxbAZbmnGscON3")
)

# APIエンドポイント
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"

Write-Host "=== n8nワークフロー削除（MCP Access Token使用） ===" -ForegroundColor Cyan
Write-Host ""

# 方法1: Bearer Token形式
$headers1 = @{
    "Authorization" = "Bearer $MCPToken"
    "Content-Type" = "application/json"
}

# 方法2: X-N8N-API-KEY形式
$headers2 = @{
    "X-N8N-API-KEY" = $MCPToken
    "Content-Type" = "application/json"
}

foreach ($workflowId in $workflowIds) {
    Write-Host "ワークフローID: $workflowId を削除中..." -ForegroundColor Yellow

    # まずワークフロー情報を取得して確認
    try {
        $workflowUrl = "$baseUrl/workflows/$workflowId"
        $workflow = Invoke-RestMethod -Uri $workflowUrl -Method Get -Headers $headers1 -ErrorAction SilentlyContinue

        if (-not $workflow) {
            $workflow = Invoke-RestMethod -Uri $workflowUrl -Method Get -Headers $headers2 -ErrorAction SilentlyContinue
        }

        if ($workflow) {
            Write-Host "  ワークフロー名: $($workflow.name)" -ForegroundColor Gray
            Write-Host "  状態: $(if ($workflow.active) { 'Active' } else { 'Inactive' })" -ForegroundColor Gray

            # ワークフローを削除（Bearer形式を試す）
            try {
                $response = Invoke-RestMethod -Uri $workflowUrl -Method Delete -Headers $headers1
                Write-Host "  ✅ 削除成功（Bearer形式）" -ForegroundColor Green
            } catch {
                # X-N8N-API-KEY形式を試す
                try {
                    $response = Invoke-RestMethod -Uri $workflowUrl -Method Delete -Headers $headers2
                    Write-Host "  ✅ 削除成功（X-N8N-API-KEY形式）" -ForegroundColor Green
                } catch {
                    Write-Host "  ❌ 削除失敗: $($_.Exception.Message)" -ForegroundColor Red
                }
            }
        } else {
            Write-Host "  ⚠️ ワークフロー情報を取得できませんでした" -ForegroundColor Yellow
        }
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        $errorMessage = $_.Exception.Message

        if ($statusCode -eq 404) {
            Write-Host "  ⚠️ ワークフローが見つかりません（既に削除されている可能性）" -ForegroundColor Yellow
        }
        elseif ($statusCode -eq 401) {
            Write-Host "  ❌ 認証エラー: MCP Access Tokenが無効です" -ForegroundColor Red
            Write-Host "  MCP Access Tokenを確認してください: Settings → MCP Access → Access Tokenタブ" -ForegroundColor Yellow
        }
        else {
            Write-Host "  ❌ エラー: $errorMessage (ステータスコード: $statusCode)" -ForegroundColor Red
        }
    }
    Write-Host ""
}

Write-Host "=== 削除処理完了 ===" -ForegroundColor Cyan
















