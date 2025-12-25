# n8n-MCP險ｭ螳壹せ繧ｯ繝ｪ繝励ヨ
# 菴ｿ逕ｨ譁ｹ豕・ .\scripts\setup-n8n-mcp.ps1

# 迺ｰ蠅・､画焚繧呈峩譁ｰ
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Infisical險ｭ螳・$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
$projectId = "446f131c-be8d-45e5-a83a-4154e34501a5"

Write-Host "=== n8n-MCP險ｭ螳壹せ繧ｯ繝ｪ繝励ヨ ===" -ForegroundColor Green
Write-Host ""

# .cursor繝・ぅ繝ｬ繧ｯ繝医Μ縺ｮ遒ｺ隱阪・菴懈・
$cursorDir = "$env:USERPROFILE\.cursor"
if (-not (Test-Path $cursorDir)) {
    New-Item -ItemType Directory -Path $cursorDir -Force | Out-Null
    Write-Host "笨・.cursor繝・ぅ繝ｬ繧ｯ繝医Μ繧剃ｽ懈・縺励∪縺励◆: $cursorDir" -ForegroundColor Green
} else {
    Write-Host "笨・.cursor繝・ぅ繝ｬ繧ｯ繝医Μ縺ｯ譌｢縺ｫ蟄伜惠縺励∪縺・ $cursorDir" -ForegroundColor Cyan
}

# N8N_API_KEY繧貞叙蠕・Write-Host ""
Write-Host "Infisical縺九ｉN8N_API_KEY繧貞叙蠕嶺ｸｭ..." -ForegroundColor Yellow
try {
    $n8nApiKeyJson = infisical secrets get N8N_API_KEY --token $token --projectId $projectId --output json 2>&1 | Out-String
    $n8nApiKeyObj = $n8nApiKeyJson | ConvertFrom-Json
    $n8nApiKey = $n8nApiKeyObj[0].secretValue

    if ([string]::IsNullOrEmpty($n8nApiKey)) {
        Write-Host "笨・繧ｨ繝ｩ繝ｼ: N8N_API_KEY縺悟叙蠕励〒縺阪∪縺帙ｓ縺ｧ縺励◆" -ForegroundColor Red
        Write-Host ""
        Write-Host "谺｡縺ｮ謇矩・ｒ螳溯｡後＠縺ｦ縺上□縺輔＞:" -ForegroundColor Yellow
        Write-Host "1. n8n Cloud Dashboard 竊・Settings 竊・API 竊・Generate API Key" -ForegroundColor Cyan
        Write-Host "2. API Key繧棚nfisical縺ｫ菫晏ｭ・(N8N_API_KEY)" -ForegroundColor Cyan
        exit 1
    }

    Write-Host "笨・N8N_API_KEY繧貞叙蠕励＠縺ｾ縺励◆ (髟ｷ縺・ $($n8nApiKey.Length))" -ForegroundColor Green
} catch {
    Write-Host "笨・繧ｨ繝ｩ繝ｼ: N8N_API_KEY縺ｮ蜿門ｾ励↓螟ｱ謨励＠縺ｾ縺励◆" -ForegroundColor Red
    Write-Host "繧ｨ繝ｩ繝ｼ隧ｳ邏ｰ: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# MCP險ｭ螳壹ヵ繧｡繧､繝ｫ縺ｮ繝代せ
$mcpJsonPath = "$cursorDir\mcp.json"

# MCP險ｭ螳壹が繝悶ず繧ｧ繧ｯ繝医ｒ菴懈・
$mcpConfig = @{
    mcpServers = @{
        n8n = @{
            command = "npx"
            args = @("-y", "n8n-mcp")
            env = @{
                N8N_API_URL = "https://hadayalab.app.n8n.cloud"
                N8N_API_KEY = $n8nApiKey
                LOG_LEVEL = "error"
                NODE_NO_WARNINGS = "1"
            }
        }
    }
}

# JSON縺ｫ螟画鋤
$mcpJson = $mcpConfig | ConvertTo-Json -Depth 10

# 譌｢蟄倥・mcp.json縺後≠繧句ｴ蜷医・繝舌ャ繧ｯ繧｢繝・・
if (Test-Path $mcpJsonPath) {
    $backupPath = "$mcpJsonPath.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item $mcpJsonPath $backupPath
    Write-Host ""
    Write-Host "笨・譌｢蟄倥・mcp.json繧偵ヰ繝・け繧｢繝・・縺励∪縺励◆: $backupPath" -ForegroundColor Cyan
}

# mcp.json繧呈嶌縺崎ｾｼ縺ｿ
Write-Host ""
Write-Host "mcp.json繧剃ｽ懈・荳ｭ..." -ForegroundColor Yellow
try {
    $mcpJson | Out-File -FilePath $mcpJsonPath -Encoding UTF8 -Force
    Write-Host "笨・mcp.json繧剃ｽ懈・縺励∪縺励◆: $mcpJsonPath" -ForegroundColor Green
} catch {
    Write-Host "笨・繧ｨ繝ｩ繝ｼ: mcp.json縺ｮ菴懈・縺ｫ螟ｱ謨励＠縺ｾ縺励◆" -ForegroundColor Red
    Write-Host "繧ｨ繝ｩ繝ｼ隧ｳ邏ｰ: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 險ｭ螳壼・螳ｹ繧堤｢ｺ隱搾ｼ・PI Key縺ｯ荳驛ｨ縺ｮ縺ｿ陦ｨ遉ｺ・・Write-Host ""
Write-Host "=== 險ｭ螳壼・螳ｹ ===" -ForegroundColor Green
Write-Host "繝輔ぃ繧､繝ｫ: $mcpJsonPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "MCP繧ｵ繝ｼ繝舌・: n8n" -ForegroundColor Cyan
Write-Host "  Command: npx" -ForegroundColor Gray
Write-Host "  Args: -y n8n-mcp" -ForegroundColor Gray
Write-Host "  N8N_API_URL: https://hadayalab.app.n8n.cloud" -ForegroundColor Gray
Write-Host "  N8N_API_KEY: $($n8nApiKey.Substring(0, [Math]::Min(30, $n8nApiKey.Length)))..." -ForegroundColor Gray
Write-Host "  LOG_LEVEL: error" -ForegroundColor Gray
Write-Host "  NODE_NO_WARNINGS: 1" -ForegroundColor Gray
Write-Host ""

# 谺｡縺ｮ繧ｹ繝・ャ繝励ｒ陦ｨ遉ｺ
Write-Host "=== 谺｡縺ｮ繧ｹ繝・ャ繝・===" -ForegroundColor Green
Write-Host ""
Write-Host "1. Cursor繧貞・襍ｷ蜍輔＠縺ｦ縺上□縺輔＞" -ForegroundColor Yellow
Write-Host "   - 縺吶∋縺ｦ縺ｮCursor繧ｦ繧｣繝ｳ繝峨え繧帝哩縺倥ｋ" -ForegroundColor Gray
Write-Host "   - 30遘貞ｾ・ｩ・ -ForegroundColor Gray
Write-Host "   - Cursor繧貞・襍ｷ蜍・ -ForegroundColor Gray
Write-Host ""
Write-Host "2. 蜍穂ｽ懃｢ｺ隱・ -ForegroundColor Yellow
Write-Host "   - Cursor AI繝√Ε繝・ヨ縺ｧ莉･荳九ｒ螳溯｡・" -ForegroundColor Gray
Write-Host "     @n8n 蛻ｩ逕ｨ蜿ｯ閭ｽ縺ｪ繝・・繝ｫ繧定｡ｨ遉ｺ縺励※" -ForegroundColor Cyan
Write-Host ""

Write-Host "=== Setup Complete ===" -ForegroundColor Green

