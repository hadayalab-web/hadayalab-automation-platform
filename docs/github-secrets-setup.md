# GitHub Secrets設定ガイド

このドキュメントは、GitHub Secretsを使用したAPIキー管理の設定方法を説明します。

## 🎯 概要

GitHub Secretsを使用することで、以下のメリットがあります：

- ✅ **セキュリティ**: キーが暗号化され、ログに表示されない
- ✅ **一元管理**: リポジトリ単位でキーを管理
- ✅ **CI/CD統合**: GitHub Actionsで自動的に使用可能
- ✅ **アクセス制御**: リポジトリの権限に基づいてアクセス制限

## 📋 必要な認証情報一覧

### 現在必要なSecrets

#### 1. N8N_API_KEY

- **説明**: n8n Cloud APIへのアクセスキー
- **取得先**: https://hadayalab.app.n8n.cloud → Settings → API
- **形式**: `n8n_api_xxxxxxxxxxxxx`
- **用途**:
  - GitHub Actionsでのn8nワークフロー自動デプロイ（将来実装）
  - CI/CDパイプラインでの検証

#### 2. N8N_API_URL

- **説明**: n8n CloudインスタンスのURL
- **値**: `https://hadayalab.app.n8n.cloud`
- **用途**: APIエンドポイントの指定

## 🔧 GitHub Secretsの設定手順

### 方法1: GitHub Web UIで設定（推奨）

1. **リポジトリにアクセス**
   - GitHubリポジトリのページを開く
   - 例: `https://github.com/hadayalab-web/hadayalab-automation-platform`

2. **Settingsに移動**
   - リポジトリページの上部メニューから「Settings」をクリック

3. **Secrets and variables → Actions に移動**
   - 左サイドバーから「Secrets and variables」→「Actions」を選択

4. **New repository secret をクリック**

5. **Secretを追加**
   - **Name**: `N8N_API_KEY`
   - **Secret**: 実際のn8n APIキーを貼り付け
   - 「Add secret」をクリック

6. **同様にN8N_API_URLも追加**
   - **Name**: `N8N_API_URL`
   - **Secret**: `https://hadayalab.app.n8n.cloud`
   - 「Add secret」をクリック

### 方法2: GitHub CLIで設定

```bash
# GitHub CLIのインストール（未インストールの場合）
# Windows: winget install GitHub.cli
# macOS: brew install gh
# Linux: 各ディストリビューションのパッケージマネージャーでインストール

# GitHub CLIにログイン
gh auth login

# Secretを設定
gh secret set N8N_API_KEY --body "実際のAPIキー"
gh secret set N8N_API_URL --body "https://hadayalab.app.n8n.cloud"

# 設定確認
gh secret list
```

## 🔍 Secretsの確認方法

### GitHub Web UIで確認

1. Settings → Secrets and variables → Actions
2. Repository secretsセクションに追加したSecretsが表示されます
3. **注意**: Secretの値は表示されません（セキュリティのため）

### GitHub CLIで確認

```bash
# Secrets一覧を表示（値は表示されない）
gh secret list
```

## 🚀 GitHub Actionsでの使用方法

### サンプルワークフロー

プロジェクトには、GitHub Secretsを使用するサンプルワークフローが含まれています：

- **ファイル**: `.github/workflows/deploy-to-n8n.example.yml`
- **内容**: n8n Cloudへの自動デプロイ例
- **使用方法**: このファイルをコピーして適切な名前にリネームし、実際のAPIエンドポイントに合わせて調整

### 基本的な使用方法

GitHub ActionsワークフローでSecretsを使用する例：

```yaml
name: Deploy to n8n

on:
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy workflow
        env:
          N8N_API_URL: ${{ secrets.N8N_API_URL }}
          N8N_API_KEY: ${{ secrets.N8N_API_KEY }}
        run: |
          # n8n APIを使用したデプロイスクリプト
          curl -X POST "$N8N_API_URL/api/v1/workflows" \
            -H "X-N8N-API-KEY: $N8N_API_KEY" \
            -H "Content-Type: application/json" \
            -d @workflows/example.json
```

### 環境変数として使用

```yaml
env:
  N8N_API_URL: ${{ secrets.N8N_API_URL }}
  N8N_API_KEY: ${{ secrets.N8N_API_KEY }}
```

### 条件付きで使用

```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main'
  env:
    N8N_API_KEY: ${{ secrets.N8N_API_KEY }}
  run: |
    # 本番環境へのデプロイ
```

## 🔐 セキュリティベストプラクティス

### ✅ 推奨事項

1. **最小権限の原則**: 必要な権限のみを付与
2. **定期的なローテーション**: APIキーを定期的に更新
3. **環境分離**: 本番環境と開発環境で異なるSecretsを使用
4. **アクセスログの確認**: 誰がSecretsにアクセスしたかを定期的に確認

### ❌ 避けるべきこと

1. **Secretsをコードに直接記述**: 絶対にしない
2. **Secretsをログに出力**: `echo $SECRET` などは使用しない
3. **Secretsをコミット**: `.env`ファイルをコミットしない
4. **不必要なアクセス権限**: 必要最小限の権限のみ

## 📝 ローカル開発環境との違い

### ローカル開発（Cursor）

- **設定場所**: `~/.cursor/mcp.json`
- **用途**: MCPサーバー経由でのn8n操作
- **管理方法**: ローカルファイル（Gitにコミットしない）

### CI/CD（GitHub Actions）

- **設定場所**: GitHub Secrets
- **用途**: 自動デプロイ、検証、テスト
- **管理方法**: GitHub Secrets（暗号化）

## 🔄 移行手順

既存の`mcp.json`からGitHub Secretsへの移行：

1. **現在のAPIキーを確認**
   ```bash
   # mcp.jsonからAPIキーを確認（ローカルのみ）
   cat ~/.cursor/mcp.json
   ```

2. **GitHub Secretsに追加**
   - 上記の「設定手順」を参照

3. **GitHub Actionsワークフローを更新**
   - Secretsを使用するようにワークフローファイルを更新

4. **動作確認**
   - GitHub Actionsを実行してSecretsが正しく使用されることを確認

## 🛠️ トラブルシューティング

### Secretsが認識されない

**症状**: GitHub Actionsで`${{ secrets.N8N_API_KEY }}`が空

**解決方法**:
1. Secret名のスペルミスを確認（大文字小文字を区別）
2. Settings → Secrets and variables → Actions でSecretが存在することを確認
3. ワークフローファイルの構文を確認

### 権限エラー

**症状**: GitHub ActionsでAPI呼び出しが403エラー

**解決方法**:
1. APIキーが有効か確認
2. APIキーに必要な権限があるか確認
3. n8n Cloudの設定でAPIアクセスが有効か確認

## 📚 参考リンク

- [GitHub Secrets公式ドキュメント](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitHub CLI公式ドキュメント](https://cli.github.com/manual/)
- [n8n API Documentation](https://docs.n8n.io/api/)

---

**最終更新**: 2025-01-23
**バージョン**: 1.0.0

