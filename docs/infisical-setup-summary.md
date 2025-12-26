# Infisical セットアップ完了サマリー

## ✅ 完了したステップ

- [x] Infisicalアカウントの作成
- [x] Infisical CLIのインストール（Windows）
- [x] Infisicalに必要なキーをすべて格納完了
- [x] プロジェクト情報の確認
  - プロジェクト名: `hadayalab-automation-platform-c79-q`
  - プロジェクトID: `446f131c-be8d-45e5-a83a-4154e34501a5`
- [x] `.infisical.json` ファイルの作成
- [x] シークレットの取得確認
  - `N8N_API_KEY`: 取得成功 ✅
  - `N8N_API_URL`: 取得成功 ✅

## 📋 現在の設定

### プロジェクト情報

- **プロジェクト名**: `hadayalab-automation-platform-c79-q`
- **プロジェクトID**: `446f131c-be8d-45e5-a83a-4154e34501a5`
- **環境**: `development`
- **設定ファイル**: `.infisical.json`

### シークレット

- **N8N_API_KEY**: Infisicalから取得可能
- **N8N_API_URL**: `https://hadayalab.app.n8n.cloud/mcp-server/http`

## 🚀 シークレットの取得方法

### 方法1: スクリプトを使用（推奨）

作成したスクリプトを使用して、シークレットを環境変数として読み込みます：

```powershell
# スクリプトを実行
.\scripts\infisical-get-secrets.ps1
```

このスクリプトは：
- Infisicalからシークレットを取得
- 環境変数として設定
- 現在のPowerShellセッションで使用可能

### 方法2: コマンドを直接実行

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# トークンとプロジェクトIDを設定
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
$projectId = "446f131c-be8d-45e5-a83a-4154e34501a5"

# シークレットを取得
infisical secrets get N8N_API_KEY --token $token --projectId $projectId
infisical secrets get N8N_API_URL --token $token --projectId $projectId
```

### 方法3: infisical init を使用（将来的に推奨）

トークンをローカルに保存して、より簡単に使用できるようにする：

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# プロジェクトを初期化
infisical init
```

**プロンプトで以下を選択:**
1. ホスティングオプション: `Infisical Cloud (US Region)`
2. プロジェクト: `hadayalab-automation-platform-c79-q`
3. 環境: `development`

これにより、以降はトークンなしでシークレットを取得できます。

## 🔧 ローカル開発環境での使用

### Cursor MCPでの使用

`~/.cursor/mcp.json`を更新して、Infisicalからシークレットを読み込む：

```json
{
  "mcpServers": {
    "n8n": {
      "command": "npx",
      "args": ["-y", "n8n-mcp"],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud/mcp-server/http",
        "N8N_API_KEY": "",
        "LOG_LEVEL": "error",
        "NODE_NO_WARNINGS": "1"
      }
    }
  }
}
```

**注意**: `N8N_API_KEY`は空にしておき、Infisicalから読み込みます。

Cursor起動前に、PowerShellで以下を実行：

```powershell
# スクリプトを実行してシークレットを読み込む
.\scripts\infisical-get-secrets.ps1

# または、手動で環境変数を設定
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
$projectId = "446f131c-be8d-45e5-a83a-4154e34501a5"
$env:N8N_API_KEY = (infisical secrets get N8N_API_KEY --token $token --projectId $projectId --output plain 2>&1 | Select-String -Pattern "N8N_API_KEY" | ForEach-Object { $_.Line -replace '.*N8N_API_KEY\s+', '' -replace '\s+shared.*', '' }).Trim()
$env:N8N_API_URL = (infisical secrets get N8N_API_URL --token $token --projectId $projectId --output plain 2>&1 | Select-String -Pattern "N8N_API_URL" | ForEach-Object { $_.Line -replace '.*N8N_API_URL\s+', '' -replace '\s+shared.*', '' }).Trim()

# Cursorを起動
```

## 📝 次のステップ

1. **スクリプトの使用**
   - `scripts\infisical-get-secrets.ps1` を実行してシークレットを読み込む

2. **infisical init の実行**（オプション）
   - より簡単に使用できるように、`infisical init`を実行することを検討

3. **GitHub Actionsとの統合**
   - [Infisical設定ガイド](./infisical-setup.md#-github-actionsでの使用方法) を参照
   - サービストークンの作成
   - GitHub Secretsへの追加

## 📚 参考リンク

- [Infisical設定ガイド](./infisical-setup.md) - 詳細な設定方法
- [Infisical クイックスタート](./infisical-quick-start.md) - 初期設定手順
- [Infisical セットアップ完了ガイド](./infisical-setup-complete.md) - セットアップ完了後の手順
- [Infisical プロジェクト初期化ガイド](./infisical-init-guide.md) - プロジェクト初期化の詳細

---

**最終更新**: 2025-01-23
**バージョン**: 1.0.0





















