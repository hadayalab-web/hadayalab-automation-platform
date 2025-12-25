# CryptoQuant ドキュメント保存スクリプト
# ブラウザから手動で取得したドキュメントを保存するためのヘルパースクリプト

param(
    [Parameter(Mandatory=$false)]
    [string]$DocsPath = "",

    [Parameter(Mandatory=$false)]
    [string]$CatalogPath = "",

    [switch]$Help
)

$OutputDir = Join-Path $PSScriptRoot "..\docs\cryptoquant-docs"

if ($Help) {
    Write-Host @"
CryptoQuant ドキュメント保存スクリプト

使用方法:
  1. ブラウザで https://cryptoquant.com/docs にアクセス
  2. Cloudflareのチャレンジを通過
  3. ページを右クリック → 「名前を付けて保存」でHTMLを保存
  4. このスクリプトを実行して、保存したファイルを指定

例:
  .\save-cryptoquant-docs.ps1 -DocsPath "C:\Users\...\Downloads\cryptoquant-docs.html"
  .\save-cryptoquant-docs.ps1 -DocsPath "docs.html" -CatalogPath "catalog.html"

"@
    exit 0
}

# 出力ディレクトリを作成
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    Write-Host "✅ 出力ディレクトリを作成しました: $OutputDir" -ForegroundColor Green
}

# ドキュメントをコピー
if ($DocsPath -ne "") {
    if (Test-Path $DocsPath) {
        $destPath = Join-Path $OutputDir "docs.html"
        Copy-Item -Path $DocsPath -Destination $destPath -Force
        Write-Host "✅ ドキュメントを保存しました: $destPath" -ForegroundColor Green
    } else {
        Write-Host "❌ ファイルが見つかりません: $DocsPath" -ForegroundColor Red
    }
}

# カタログをコピー
if ($CatalogPath -ne "") {
    if (Test-Path $CatalogPath) {
        $destPath = Join-Path $OutputDir "catalog.html"
        Copy-Item -Path $CatalogPath -Destination $destPath -Force
        Write-Host "✅ カタログを保存しました: $destPath" -ForegroundColor Green
    } else {
        Write-Host "❌ ファイルが見つかりません: $CatalogPath" -ForegroundColor Red
    }
}

if ($DocsPath -eq "" -and $CatalogPath -eq "") {
    Write-Host "`n💡 使用方法:" -ForegroundColor Cyan
    Write-Host "  .\save-cryptoquant-docs.ps1 -Help" -ForegroundColor White
    Write-Host "`nまたは、手動でファイルを以下のディレクトリにコピーしてください:" -ForegroundColor Yellow
    Write-Host "  $OutputDir" -ForegroundColor White
    Write-Host "  - docs.html" -ForegroundColor Gray
    Write-Host "  - catalog.html" -ForegroundColor Gray
}

Write-Host "`n✨ 完了しました！" -ForegroundColor Green
Write-Host "Cursorは以下のディレクトリ内のファイルを自動的に参照できます:" -ForegroundColor Cyan
Write-Host "  $OutputDir" -ForegroundColor White












