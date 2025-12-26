# Infisical クイックスタートガイド

このガイドは、Infisicalアカウント作成後の初期設定を迅速に行うための手順です。

## ✅ 完了したステップ

- [x] Infisicalアカウントの作成

## 📋 次のステップ

### ステップ1: プロジェクトの作成（Infisicalダッシュボード）

1. **Infisicalダッシュボードにアクセス**
   - https://app.infisical.com にログイン

2. **プロジェクトを作成**
   - 「New Project」または「Create Project」をクリック
   - プロジェクト名: `hadayalab-automation-platform`
   - 説明（オプション）: `HadayaLab Automation Platform - n8nワークフロー管理`
   - 「Create Project」をクリック

3. **環境の確認**
   - デフォルトで以下の環境が作成されます:
     - `development`（開発環境）
     - `staging`（ステージング環境）
     - `production`（本番環境）
   - 必要に応じて環境を追加・削除可能

### ステップ2: Infisical CLIのインストール

#### Windows（PowerShell）

```powershell
# Chocolateyを使用（推奨）
choco install infisical

# または、Wingetを使用
winget install Infisical.Infisical

# インストール確認
infisical --version
```

#### macOS

```bash
# Homebrewを使用
brew install infisical

# インストール確認
infisical --version
```

#### Linux

```bash
# Debian/Ubuntu
curl -1sLf 'https://dl.cloudsmith.io/public/infisical/infisical-cli/setup.deb.sh' | sudo -E bash
sudo apt-get install infisical

# インストール確認
infisical --version
```

### ステップ3: Infisical CLIの認証

```bash
# Infisicalにログイン
infisical login

# ブラウザが自動的に開きます
# ブラウザで認証を完了してください
```

**注意**: ブラウザが開かない場合は、表示されたURLを手動でブラウザに貼り付けてください。

### ステップ4: プロジェクトの初期化

```bash
# プロジェクトディレクトリに移動（既にいる場合は不要）
cd hadayalab-automation-platform

# Infisicalプロジェクトを初期化
infisical init
```

**プロンプトで以下を選択:**

1. **プロジェクトを選択**
   - 先ほど作成した `hadayalab-automation-platform` を選択

2. **環境を選択**
   - 通常は `development` を選択（後で変更可能）

3. **確認**
   - `.infisical.json` ファイルが作成されます

**作成されるファイル:**

```json
{
  "projectId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "projectSlug": "hadayalab-automation-platform",
  "environment": "development"
}
```

### ステップ5: シークレットの追加

#### 方法A: Infisical Web UIで追加（推奨・簡単）

1. **Infisicalダッシュボードにアクセス**
   - https://app.infisical.com にログイン
   - プロジェクト `hadayalab-automation-platform` を選択

2. **シークレットを追加**
   - 左サイドバーから「Secrets」をクリック
   - 環境を選択（例: `development`）
   - 「Add Secret」ボタンをクリック

3. **N8N_API_KEYを追加**
   - **Key**: `N8N_API_KEY`
   - **Value**: 実際のn8n APIキー（`n8n_api_xxxxxxxxxxxxx`）
   - **Type**: `Shared`（すべての環境で共有）または`Personal`（個人用）
   - 「Save」をクリック

4. **N8N_API_URLを追加**
   - **Key**: `N8N_API_URL`
   - **Value**: `https://hadayalab.app.n8n.cloud`
   - **Type**: `Shared`
   - 「Save」をクリック

5. **他の環境にも設定**（オプション）
   - 環境を切り替えて（`staging`, `production`）、同様にシークレットを追加
   - または、`Shared`タイプにすることで全環境で共有

#### 方法B: Infisical CLIで追加

```bash
# 現在の環境を確認
infisical status

# シークレットを追加
infisical secrets set N8N_API_KEY "n8n_api_xxxxxxxxxxxxx"
infisical secrets set N8N_API_URL "https://hadayalab.app.n8n.cloud"

# 特定の環境に設定
infisical secrets set N8N_API_KEY "n8n_api_dev_xxxxx" --env development
infisical secrets set N8N_API_KEY "n8n_api_prod_xxxxx" --env production

# シークレット一覧を確認
infisical secrets list
```

### ステップ6: 動作確認

```bash
# シークレットを取得して確認
infisical secrets get N8N_API_KEY
infisical secrets get N8N_API_URL

# すべてのシークレットを環境変数としてエクスポート（確認用）
infisical secrets export

# .envファイルとして出力（確認用）
infisical secrets export --format dotenv
```

## 🔧 ローカル開発環境での使用

### 方法1: 環境変数として読み込む（推奨）

```bash
# Bash/Zsh
eval $(infisical secrets export)

# PowerShell（Windows）
$secrets = infisical secrets export --format json | ConvertFrom-Json
$env:N8N_API_KEY = $secrets.N8N_API_KEY
$env:N8N_API_URL = $secrets.N8N_API_URL
```

### 方法2: .envファイルを生成

```bash
# .env.localファイルを生成（.gitignoreに追加済み）
infisical secrets export --format dotenv > .env.local

# アプリケーションが自動的に.env.localを読み込みます
```

### 方法3: Cursor MCPでの使用

`~/.cursor/mcp.json`を更新して、Infisicalからシークレットを読み込む：

```json
{
  "mcpServers": {
    "n8n": {
      "command": "npx",
      "args": ["-y", "n8n-mcp"],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
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
# Infisicalからシークレットを読み込む
$secrets = infisical secrets export --format json | ConvertFrom-Json
$env:N8N_API_KEY = $secrets.N8N_API_KEY
$env:N8N_API_URL = $secrets.N8N_API_URL

# Cursorを起動
```

## ✅ チェックリスト

セットアップが完了したら、以下を確認してください：

- [ ] Infisicalプロジェクトが作成されている
- [ ] Infisical CLIがインストールされている（`infisical --version`で確認）
- [ ] Infisical CLIでログインできている（`infisical login`）
- [ ] プロジェクトが初期化されている（`.infisical.json`が存在）
- [ ] `N8N_API_KEY`がInfisicalに追加されている
- [ ] `N8N_API_URL`がInfisicalに追加されている
- [ ] シークレットが取得できる（`infisical secrets get N8N_API_KEY`）

## 🚀 次のステップ

セットアップが完了したら：

1. **GitHub Actionsとの統合**
   - [Infisical設定ガイド](./infisical-setup.md#-github-actionsでの使用方法) を参照
   - サービストークンの作成
   - GitHub Secretsへの追加

2. **環境の切り替え**
   ```bash
   # 環境を切り替える
   infisical init
   # プロンプトで環境を選択
   ```

3. **詳細な設定**
   - [Infisical設定ガイド](./infisical-setup.md) を参照
   - セキュリティベストプラクティス
   - トラブルシューティング

## 🛠️ トラブルシューティング

### CLIがインストールできない

**Windowsの場合:**
- Chocolateyがインストールされていない場合は、[公式サイト](https://github.com/Infisical/infisical/releases)から直接ダウンロード

**macOSの場合:**
- Homebrewがインストールされていない場合は、[公式サイト](https://github.com/Infisical/infisical/releases)から直接ダウンロード

### ログインできない

- ブラウザが開かない場合は、表示されたURLを手動でブラウザに貼り付け
- 認証後、CLIに戻ってEnterキーを押す

### プロジェクトが見つからない

- `infisical init`を実行する前に、Infisicalダッシュボードでプロジェクトが作成されているか確認
- プロジェクト名のスペルミスを確認

### シークレットが取得できない

- 現在の環境を確認: `infisical status`
- シークレットが正しい環境に追加されているか確認
- シークレット名のスペルミスを確認（大文字小文字を区別）

## 📚 参考リンク

- [Infisical設定ガイド](./infisical-setup.md) - 詳細な設定方法
- [API Keys設定ガイド](./api-keys-setup.md) - APIキーの取得方法
- [Infisical公式ドキュメント](https://infisical.com/docs)

---

**最終更新**: 2025-01-23
**バージョン**: 1.0.0






















