# n8nダッシュボードアクセステスト
$apiKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ZDcxM2YyMS0wZDBiLTRhYmUtYWZjNy1kYjc2MmQ4YWUzMzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY2NTgyODI1LCJleHAiOjE3NjkwOTQwMDB9.Glz7mE73w8H-KlgIpeUgVi17-Y5ost_MnbGHGqwvYdo"

Write-Host "=== n8nダッシュボードアクセステスト ===" -ForegroundColor Cyan
Write-Host ""

$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/json"
}

# 1. ワークフロー一覧を取得
Write-Host "1. ワークフロー一覧を取得中..." -ForegroundColor Yellow
try {
    $workflows = Invoke-RestMethod -Uri "https://hadayalab.app.n8n.cloud/rest/workflows" -Method Get -Headers $headers -ErrorAction Stop

    if ($workflows.data) {
        Write-Host "  [OK] ワークフロー一覧取得成功" -ForegroundColor Green
        Write-Host "  ワークフロー数: $($workflows.data.Count)" -ForegroundColor White

        if ($workflows.data.Count -gt 0) {
            Write-Host "`n  既存のワークフロー:" -ForegroundColor Cyan
            foreach ($wf in $workflows.data) {
                Write-Host "    - $($wf.name) (ID: $($wf.id))" -ForegroundColor Gray
            }
        }
    } else {
        Write-Host "  [OK] APIアクセス成功（データ形式を確認中）" -ForegroundColor Green
        Write-Host "  レスポンス: $($workflows | ConvertTo-Json -Depth 2)" -ForegroundColor Gray
    }
} catch {
    Write-Host "  [NG] エラー: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "  ステータスコード: $statusCode" -ForegroundColor Red

        # エラーレスポンスを取得
        try {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $responseBody = $reader.ReadToEnd()
            $reader.Close()
            Write-Host "  エラーレスポンス: $responseBody" -ForegroundColor Yellow
        } catch {
            # エラーレスポンスの読み取りに失敗
        }
    }
}

Write-Host "`n=== テスト完了 ===" -ForegroundColor Cyan















