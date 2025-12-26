# Grok AI X + Telegram解析スクリプト実行用PowerShellスクリプト
# Cursorが固まらないように、出力をファイルにリダイレクトして実行

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
$outputFile = Join-Path $projectRoot "affiliate_extraction_output_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

# XAI_API_KEYを取得
$apiKeyFile = "C:\Users\chiba\Downloads\XAI_API_KEY.txt"
if (Test-Path $apiKeyFile) {
    $apiKeyContent = Get-Content $apiKeyFile -Raw
    $apiKey = ($apiKeyContent -split "`n" | Select-Object -Skip 1 -First 1).Trim()
    $env:XAI_API_KEY = $apiKey
    Write-Host "[OK] XAI_API_KEY loaded from file"
} else {
    Write-Host "[ERROR] XAI_API_KEY.txt not found at: $apiKeyFile"
    exit 1
}

# スクリプトを実行（出力をファイルにリダイレクト）
Write-Host "`n[INFO] Starting affiliate extraction..."
Write-Host "[INFO] Output will be saved to: $outputFile"
Write-Host "[INFO] This may take several minutes due to API rate limits...`n"

cd $projectRoot
python scripts\grok-x-affiliate-extraction.py 2>&1 | Tee-Object -FilePath $outputFile

Write-Host "`n[OK] Extraction completed. Results saved to: $outputFile"
Write-Host "[INFO] JSON file saved in project root: affiliate_candidates_*.json"

