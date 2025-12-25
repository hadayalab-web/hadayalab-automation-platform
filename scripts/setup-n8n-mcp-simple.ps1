# n8n-MCP Setup Script
# Usage: .\scripts\setup-n8n-mcp-simple.ps1

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoTWV0aG9kIjoiZ29vZ2xlIiwiYXV0aFRva2VuVHlwZSI6ImFjY2Vzc1Rva2VuIiwidXNlcklkIjoiMjBhZTM5NjktODQ0NS00OWNhLTlkY2UtYzUwNmQ1YTMxMzI5IiwidG9rZW5WZXJzaW9uSWQiOiJmZTI0YWY0ZS0zNDZhLTRkZDYtYjZkNy00NWY3Y2JhNDRhNWQiLCJhY2Nlc3NWZXJzaW9uIjoxLCJvcmdhbml6YXRpb25JZCI6IjE2ZjQ0M2I1LWZhMTYtNGZhZC1hNGE5LTgwMjc4MDllZTM1NyIsImlhdCI6MTc2NjU0Njc0NSwiZXhwIjoxNzY3NDEwNzQ1fQ.wZnwKPLkAYBSpz9QBarfb8mcl0h3Fj2EfUbMzC0Q_4o"
$projectId = "446f131c-be8d-45e5-a83a-4154e34501a5"

Write-Host "=== n8n-MCP Setup ===" -ForegroundColor Green
Write-Host ""

# Create .cursor directory
$cursorDir = "$env:USERPROFILE\.cursor"
if (-not (Test-Path $cursorDir)) {
    New-Item -ItemType Directory -Path $cursorDir -Force | Out-Null
    Write-Host "Created .cursor directory: $cursorDir" -ForegroundColor Green
} else {
    Write-Host ".cursor directory exists: $cursorDir" -ForegroundColor Cyan
}

# Get N8N_API_KEY from Infisical
Write-Host ""
Write-Host "Getting N8N_API_KEY from Infisical..." -ForegroundColor Yellow
try {
    $n8nApiKeyOutput = infisical secrets get N8N_API_KEY --token $token --projectId $projectId --output json 2>&1
    # Extract JSON from output (remove warning messages)
    $jsonLines = $n8nApiKeyOutput | Where-Object { $_ -match '^\s*\[.*\]\s*$' -or $_ -match '^\s*\{.*\}\s*$' }
    if ($jsonLines.Count -eq 0) {
        # Try to find JSON in the output
        $jsonText = ($n8nApiKeyOutput | Out-String) -replace '.*(\[.*\]).*', '$1'
        if ($jsonText -match '\[.*\]') {
            $jsonText = $matches[0]
        } else {
            throw "No JSON found in output"
        }
    } else {
        $jsonText = $jsonLines -join "`n"
    }
    $n8nApiKeyObj = $jsonText | ConvertFrom-Json
    $n8nApiKey = $n8nApiKeyObj[0].secretValue

    if ([string]::IsNullOrEmpty($n8nApiKey)) {
        Write-Host "ERROR: Failed to get N8N_API_KEY" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please:" -ForegroundColor Yellow
        Write-Host "1. n8n Cloud Dashboard -> Settings -> API -> Generate API Key" -ForegroundColor Cyan
        Write-Host "2. Save API Key to Infisical (N8N_API_KEY)" -ForegroundColor Cyan
        exit 1
    }

    Write-Host "Got N8N_API_KEY (length: $($n8nApiKey.Length))" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to get N8N_API_KEY" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# MCP config path
$mcpJsonPath = "$cursorDir\mcp.json"

# Create MCP config
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

# Convert to JSON
$mcpJson = $mcpConfig | ConvertTo-Json -Depth 10

# Backup existing mcp.json
if (Test-Path $mcpJsonPath) {
    $backupPath = "$mcpJsonPath.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item $mcpJsonPath $backupPath
    Write-Host ""
    Write-Host "Backed up existing mcp.json: $backupPath" -ForegroundColor Cyan
}

# Write mcp.json
Write-Host ""
Write-Host "Creating mcp.json..." -ForegroundColor Yellow
try {
    $mcpJson | Out-File -FilePath $mcpJsonPath -Encoding UTF8 -Force
    Write-Host "Created mcp.json: $mcpJsonPath" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to create mcp.json" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Show config summary
Write-Host ""
Write-Host "=== Configuration ===" -ForegroundColor Green
Write-Host "File: $mcpJsonPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "MCP Server: n8n" -ForegroundColor Cyan
Write-Host "  Command: npx" -ForegroundColor Gray
Write-Host "  Args: -y n8n-mcp" -ForegroundColor Gray
Write-Host "  N8N_API_URL: https://hadayalab.app.n8n.cloud" -ForegroundColor Gray
Write-Host "  N8N_API_KEY: $($n8nApiKey.Substring(0, [Math]::Min(30, $n8nApiKey.Length)))..." -ForegroundColor Gray
Write-Host "  LOG_LEVEL: error" -ForegroundColor Gray
Write-Host "  NODE_NO_WARNINGS: 1" -ForegroundColor Gray
Write-Host ""

# Next steps
Write-Host "=== Next Steps ===" -ForegroundColor Green
Write-Host ""
Write-Host "1. Restart Cursor" -ForegroundColor Yellow
Write-Host "   - Close all Cursor windows" -ForegroundColor Gray
Write-Host "   - Wait 30 seconds" -ForegroundColor Gray
Write-Host "   - Restart Cursor" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Verify connection" -ForegroundColor Yellow
Write-Host "   - In Cursor AI chat, run:" -ForegroundColor Gray
Write-Host "     @n8n show available tools" -ForegroundColor Cyan
Write-Host ""

Write-Host "=== Setup Complete ===" -ForegroundColor Green

