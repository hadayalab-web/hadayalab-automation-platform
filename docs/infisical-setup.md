# Infisical設定ガイド

このドキュメントは、Infisicalを使用したシークレット一元管理の設定方法を説明します。

## 🎯 概要

Infisicalは、アプリケーションのシークレット、証明書、SSHキー、設定情報などを安全に一元管理するためのプラットフォームです。

### Infisicalの主なメリット

- ✅ **一元管理**: ローカル開発、CI/CD、本番環境など、すべての環境でシークレットを一元管理
- ✅ **セキュリティ**: エンドツーエンドの暗号化、RBAC（ロールベースアクセス制御）、監査ログ
- ✅ **動的シークレット**: オンデマンドでシークレットを生成し、セキュリティリスクを低減
- ✅ **シークレットローテーション**: 自動的なシークレットのローテーション
- ✅ **多様な統合**: Kubernetes、Terraform、CI/CDパイプライン、ローカル開発環境など
- ✅ **セキュリティアドバイザー**: AIを活用したセキュリティ問題の特定と予防

### 他の管理方法との比較

| 機能 | Infisical | GitHub Secrets | ローカルファイル |
|------|-----------|----------------|-----------------|
| 一元管理 | ✅ | ❌（リポジトリ単位） | ❌ |
| 動的シークレット | ✅ | ❌ | ❌ |
| ローテーション | ✅ | ❌ | ❌ |
| アクセス制御 | ✅（RBAC） | ✅（リポジトリ権限） | ❌ |
| 監査ログ | ✅ | ✅ | ❌ |
| ローカル開発 | ✅ | ❌ | ✅ |
| CI/CD統合 | ✅ | ✅ | ❌ |

## 📋 必要な認証情報一覧

### 現在必要なSecrets

#### 1. N8N_API_KEY

- **説明**: n8n Cloud APIへのアクセスキー
- **取得先**: https://hadayalab.app.n8n.cloud → Settings → API
- **形式**: `n8n_api_xxxxxxxxxxxxx`
- **用途**:
  - ローカル開発（Cursor MCP）
  - GitHub Actionsでのn8nワークフロー自動デプロイ
  - CI/CDパイプラインでの検証

#### 2. N8N_API_URL

- **説明**: n8n CloudインスタンスのURL
- **値**: `https://hadayalab.app.n8n.cloud`
- **用途**: APIエンドポイントの指定

## 🚀 セットアップ手順

### ステップ1: Infisicalアカウントの作成

1. **Infisicalにアクセス**
   - https://infisical.com にアクセス
   - 「Sign Up」をクリック

2. **アカウント作成**
   - メールアドレスとパスワードでアカウントを作成
   - または、GitHubアカウントでサインアップ

3. **組織の作成**
   - 初回ログイン時に組織を作成
   - 組織名: `hadayalab` など

### ステップ2: プロジェクトの作成

1. **プロジェクト作成**
   - Infisicalダッシュボードで「New Project」をクリック
   - プロジェクト名: `hadayalab-automation-platform`
   - 環境: `development`, `staging`, `production` など

2. **プロジェクト設定**
   - プロジェクトのスラッグを確認
   - 後でCLIで使用します

### ステップ3: Infisical CLIのインストール

#### Windows

```powershell
# Chocolateyを使用
choco install infisical

# または、直接ダウンロード
# https://github.com/Infisical/infisical/releases
```

#### macOS

```bash
# Homebrewを使用
brew install infisical

# または、直接ダウンロード
# https://github.com/Infisical/infisical/releases
```

#### Linux

```bash
# スクリプトでインストール
curl -1sLf 'https://dl.cloudsmith.io/public/infisical/infisical-cli/setup.deb.sh' | sudo -E bash
sudo apt-get install infisical

# または、直接ダウンロード
# https://github.com/Infisical/infisical/releases
```

### ステップ4: Infisical CLIの認証

```bash
# Infisicalにログイン
infisical login

# ブラウザが開き、認証が完了します
# または、サービストークンを使用
infisical auth login --service-token YOUR_SERVICE_TOKEN
```

### ステップ5: プロジェクトの初期化

```bash
# プロジェクトディレクトリに移動
cd hadayalab-automation-platform

# Infisicalプロジェクトを初期化
infisical init

# プロンプトが表示されます:
# - プロジェクトを選択
# - 環境を選択（development, staging, production）
# - .infisical.json が作成されます
```

### ステップ6: シークレットの追加

#### 方法1: Infisical Web UIで追加（推奨）

1. **Infisicalダッシュボードにアクセス**
   - https://app.infisical.com にログイン
   - プロジェクトを選択

2. **シークレットを追加**
   - 「Secrets」タブをクリック
   - 「Add Secret」をクリック
   - 以下のシークレットを追加:

   | Key | Value | Environment |
   |-----|-------|-------------|
   | `N8N_API_KEY` | `n8n_api_xxxxxxxxxxxxx` | All |
   | `N8N_API_URL` | `https://hadayalab.app.n8n.cloud` | All |

3. **環境ごとに設定**
   - 必要に応じて、環境ごとに異なる値を設定可能
   - 例: `development`環境と`production`環境で異なるAPIキー

#### 方法2: Infisical CLIで追加

```bash
# シークレットを追加
infisical secrets set N8N_API_KEY "n8n_api_xxxxxxxxxxxxx"
infisical secrets set N8N_API_URL "https://hadayalab.app.n8n.cloud"

# 特定の環境に設定
infisical secrets set N8N_API_KEY "n8n_api_dev_xxxxx" --env development
infisical secrets set N8N_API_KEY "n8n_api_prod_xxxxx" --env production

# シークレット一覧を確認
infisical secrets list
```

## 🔧 ローカル開発環境での使用方法

### 方法1: Infisical CLIで環境変数を読み込む（推奨）

#### mcp.jsonの更新

`~/.cursor/mcp.json`を更新して、Infisicalからシークレットを読み込む:

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

#### 環境変数の読み込み

```bash
# Infisicalからシークレットを読み込んで環境変数として設定
eval $(infisical secrets export)

# または、.envファイルとして出力
infisical secrets export --format dotenv > .env.local

# Cursorを起動
# 環境変数が自動的に読み込まれます
```

#### PowerShellでの使用方法（Windows）

```powershell
# Infisicalからシークレットを取得して環境変数に設定
$secrets = infisical secrets export --format json | ConvertFrom-Json
$env:N8N_API_KEY = $secrets.N8N_API_KEY
$env:N8N_API_URL = $secrets.N8N_API_URL

# Cursorを起動
```

### 方法2: Infisical CLIを直接使用

```bash
# シークレットを直接取得
N8N_API_KEY=$(infisical secrets get N8N_API_KEY)
N8N_API_URL=$(infisical secrets get N8N_API_URL)

# コマンドを実行
N8N_API_KEY=$N8N_API_KEY N8N_API_URL=$N8N_API_URL npx -y n8n-mcp
```

### 方法3: .envファイルの自動生成

```bash
# .env.localファイルを自動生成（.gitignoreに追加済み）
infisical secrets export --format dotenv > .env.local

# アプリケーションが.env.localを自動的に読み込みます
```

## 🚀 GitHub Actionsでの使用方法

### ステップ1: Infisicalサービストークンの作成

1. **Infisicalダッシュボードにアクセス**
   - プロジェクト → Settings → Service Tokens

2. **サービストークンを作成**
   - 「Create Service Token」をクリック
   - 名前: `github-actions`
   - 環境: `production`（または適切な環境）
   - 権限: `Read`（読み取りのみ）

3. **トークンをコピー**
   - 作成されたトークンをコピー（一度しか表示されません）

### ステップ2: GitHub Secretsにサービストークンを追加

1. **GitHubリポジトリにアクセス**
   - Settings → Secrets and variables → Actions

2. **INFISICAL_TOKENを追加**
   - **Name**: `INFISICAL_TOKEN`
   - **Secret**: Infisicalサービストークン

3. **INFISICAL_PROJECT_IDを追加**（オプション）
   - **Name**: `INFISICAL_PROJECT_ID`
   - **Secret**: InfisicalプロジェクトID（`.infisical.json`に記載）

### ステップ3: GitHub Actionsワークフローの更新

プロジェクトには、Infisicalを使用するサンプルワークフローが含まれています：

- **ファイル**: `.github/workflows/deploy-to-n8n-infisical.example.yml`
- **内容**: Infisicalからシークレットを読み込んでn8n Cloudにデプロイする例
- **使用方法**: このファイルをコピーして適切な名前にリネームし、実際のAPIエンドポイントに合わせて調整

#### Infisical Actionを使用する方法

```yaml
name: Deploy to n8n Cloud

on:
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Load secrets from Infisical
        uses: infisical/get-secrets@v2.2.0
        with:
          path: ./.env
          env-slug: production
          infisical-token: ${{ secrets.INFISICAL_TOKEN }}
          project-id: ${{ secrets.INFISICAL_PROJECT_ID }}

      - name: Deploy workflow
        env:
          N8N_API_URL: ${{ secrets.N8N_API_URL }}
          N8N_API_KEY: ${{ secrets.N8N_API_KEY }}
        run: |
          # .envファイルから環境変数を読み込む
          source .env

          # n8n APIを使用したデプロイスクリプト
          curl -X POST "$N8N_API_URL/api/v1/workflows" \
            -H "X-N8N-API-KEY: $N8N_API_KEY" \
            -H "Content-Type: application/json" \
            -d @workflows/example.json
```

#### Infisical CLIを使用する方法

```yaml
name: Deploy to n8n Cloud

on:
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Infisical CLI
        run: |
          curl -1sLf 'https://dl.cloudsmith.io/public/infisical/infisical-cli/setup.deb.sh' | sudo -E bash
          sudo apt-get install infisical

      - name: Load secrets from Infisical
        env:
          INFISICAL_TOKEN: ${{ secrets.INFISICAL_TOKEN }}
        run: |
          # Infisical CLIで認証
          infisical auth login --service-token $INFISICAL_TOKEN

          # シークレットを環境変数としてエクスポート
          eval $(infisical secrets export --env production)

      - name: Deploy workflow
        run: |
          # 環境変数が自動的に読み込まれます
          curl -X POST "$N8N_API_URL/api/v1/workflows" \
            -H "X-N8N-API-KEY: $N8N_API_KEY" \
            -H "Content-Type: application/json" \
            -d @workflows/example.json
```

## 🔐 セキュリティベストプラクティス

### ✅ 推奨事項

1. **最小権限の原則**: サービストークンには必要最小限の権限のみを付与
2. **環境分離**: 開発、ステージング、本番環境で異なるシークレットを使用
3. **定期的なローテーション**: APIキーを定期的に更新
4. **監査ログの確認**: Infisicalダッシュボードでアクセスログを定期的に確認
5. **RBACの活用**: チームメンバーに適切なロールを割り当て

### ❌ 避けるべきこと

1. **サービストークンをコードに直接記述**: 絶対にしない
2. **サービストークンをログに出力**: `echo $INFISICAL_TOKEN` などは使用しない
3. **過剰な権限**: 読み取りのみ必要な場合は`Read`権限のみ
4. **本番環境のシークレットを開発環境で使用**: 環境を分離

## 📝 移行手順

### 既存のmcp.jsonからInfisicalへの移行

1. **現在のAPIキーを確認**
   ```bash
   # mcp.jsonからAPIキーを確認（ローカルのみ）
   cat ~/.cursor/mcp.json
   ```

2. **Infisicalにシークレットを追加**
   - InfisicalダッシュボードまたはCLIでシークレットを追加
   - 上記の「シークレットの追加」セクションを参照

3. **Infisical CLIをインストール・認証**
   - 上記の「セットアップ手順」を参照

4. **mcp.jsonを更新**
   - `N8N_API_KEY`を空にするか、Infisicalから読み込むように変更

5. **動作確認**
   - Infisicalからシークレットを読み込んで動作確認

### GitHub SecretsからInfisicalへの移行

1. **GitHub Secretsからシークレットをエクスポート**
   ```bash
   # GitHub CLIを使用
   gh secret list
   ```

2. **Infisicalにシークレットをインポート**
   - InfisicalダッシュボードまたはCLIでシークレットを追加

3. **GitHub Actionsワークフローを更新**
   - Infisicalを使用するようにワークフローファイルを更新

4. **GitHub Secretsを削除**（オプション）
   - 移行が完了したら、GitHub Secretsを削除可能

## 🛠️ トラブルシューティング

### Infisical CLIが認識されない

**症状**: `infisical: command not found`

**解決方法**:
1. CLIが正しくインストールされているか確認
2. PATH環境変数にInfisicalが含まれているか確認
3. 再インストールを試す

### 認証エラー

**症状**: `authentication failed` または `unauthorized`

**解決方法**:
1. `infisical login`を再実行
2. サービストークンが有効か確認
3. サービストークンの権限を確認

### シークレットが読み込まれない

**症状**: 環境変数が空

**解決方法**:
1. プロジェクトと環境が正しく設定されているか確認（`.infisical.json`）
2. シークレット名のスペルミスを確認（大文字小文字を区別）
3. 環境が正しいか確認（`--env`オプション）

### GitHub Actionsでシークレットが取得できない

**症状**: GitHub ActionsでInfisicalからシークレットを取得できない

**解決方法**:
1. `INFISICAL_TOKEN`が正しく設定されているか確認
2. サービストークンの権限を確認（`Read`権限が必要）
3. プロジェクトIDが正しいか確認

## 📚 参考リンク

- [Infisical公式サイト](https://infisical.com)
- [Infisical CLIドキュメント](https://infisical.com/docs/cli/usage)
- [Infisical GitHub Actions統合](https://infisical.com/docs/documentation/platform/integrations/cloud/github-actions)
- [Infisicalセキュリティ](https://infisical.com/docs/documentation/security/overview)

## 🔗 関連ドキュメント

- [API Keys設定ガイド](./api-keys-setup.md) - 基本的なAPIキー設定
- [GitHub Secrets設定ガイド](./github-secrets-setup.md) - GitHub Secretsでの管理
- [MCPサーバー設定](./mcp-servers-setup.md) - MCPサーバーの設定

---

**最終更新**: 2025-01-23
**バージョン**: 1.0.0

