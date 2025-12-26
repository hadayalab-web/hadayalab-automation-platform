# Infisical セットアップ完了ガイド

## ✅ 完了したステップ

- [x] Infisicalアカウントの作成
- [x] Infisical CLIのインストール（Windows）
- [x] Infisicalに必要なキーをすべて格納完了

## 🚀 次のステップ

### ステップ1: Infisical CLIにログイン

PowerShellで以下を実行：

```powershell
# 環境変数を更新（新しいシェルセッションの場合）
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Infisicalにログイン
infisical login
```

**手順:**
1. コマンドを実行すると、ブラウザが自動的に開きます
2. ブラウザでInfisicalアカウントにログイン
3. 「Authorize」をクリックしてCLIへのアクセスを許可
4. PowerShellに戻り、認証が完了したことを確認

**注意**: ブラウザが開かない場合は、表示されたURLを手動でブラウザに貼り付けてください。

### ステップ2: プロジェクトの初期化

プロジェクトディレクトリで以下を実行：

```powershell
# プロジェクトディレクトリに移動（既にいる場合は不要）
cd C:\Users\chiba\hadayalab-automation-platform

# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Infisicalプロジェクトを初期化
infisical init
```

**プロンプトで以下を選択:**

1. **プロジェクトを選択**
   - 先ほど作成した `hadayalab-automation-platform` を選択
   - 矢印キーで選択し、Enterキーで確定

2. **環境を選択**
   - 通常は `development` を選択（後で変更可能）
   - 矢印キーで選択し、Enterキーで確定

3. **確認**
   - `.infisical.json` ファイルが作成されます

### ステップ3: シークレットの確認

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# シークレット一覧を確認
infisical secrets list

# 個別のシークレットを確認
infisical secrets get N8N_API_KEY
infisical secrets get N8N_API_URL
```

### ステップ4: 動作確認

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# すべてのシークレットを環境変数としてエクスポート（確認用）
infisical secrets export

# .envファイルとして出力（確認用）
infisical secrets export --format dotenv
```

## 🔧 ローカル開発環境での使用

### 方法1: 環境変数として読み込む（推奨）

PowerShellで以下を実行：

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Infisicalからシークレットを取得して環境変数に設定
$secrets = infisical secrets export --format json | ConvertFrom-Json
$env:N8N_API_KEY = $secrets.N8N_API_KEY
$env:N8N_API_URL = $secrets.N8N_API_URL

# 確認
echo $env:N8N_API_KEY
echo $env:N8N_API_URL
```

### 方法2: .envファイルを生成

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# .env.localファイルを生成（.gitignoreに追加済み）
infisical secrets export --format dotenv > .env.local

# 確認
cat .env.local
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
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Infisicalからシークレットを読み込む
$secrets = infisical secrets export --format json | ConvertFrom-Json
$env:N8N_API_KEY = $secrets.N8N_API_KEY
$env:N8N_API_URL = $secrets.N8N_API_URL

# Cursorを起動
```

## 📝 便利なコマンド

### 環境の切り替え

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# プロジェクトを再初期化して環境を切り替え
infisical init
# プロンプトで環境を選択（development, staging, production）
```

### シークレットの追加・更新

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# シークレットを追加
infisical secrets set KEY_NAME "value"

# 特定の環境に設定
infisical secrets set KEY_NAME "value" --env production

# シークレットを削除
infisical secrets delete KEY_NAME
```

### ログアウト

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# ログアウト（すべてのInfisicalデータを削除）
infisical reset
```

## ✅ チェックリスト

セットアップが完了したら、以下を確認してください：

- [ ] Infisical CLIでログインできている（`infisical login`）
- [ ] プロジェクトが初期化されている（`.infisical.json`が存在）
- [ ] シークレット一覧が表示できる（`infisical secrets list`）
- [ ] `N8N_API_KEY`が取得できる（`infisical secrets get N8N_API_KEY`）
- [ ] `N8N_API_URL`が取得できる（`infisical secrets get N8N_API_URL`）
- [ ] 環境変数としてエクスポートできる（`infisical secrets export`）

## 🚀 次のステップ

セットアップが完了したら：

1. **GitHub Actionsとの統合**
   - [Infisical設定ガイド](./infisical-setup.md#-github-actionsでの使用方法) を参照
   - サービストークンの作成
   - GitHub Secretsへの追加

2. **詳細な設定**
   - [Infisical設定ガイド](./infisical-setup.md) を参照
   - セキュリティベストプラクティス
   - トラブルシューティング

## 🛠️ トラブルシューティング

### コマンドが見つからない

**症状**: `infisical: command not found`

**解決方法**:
```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# または、PowerShellを再起動
```

### ログインできない

**症状**: ブラウザが開かない、認証エラー

**解決方法**:
- 表示されたURLを手動でブラウザに貼り付ける
- Infisicalアカウントにログインしているか確認
- ブラウザのポップアップブロッカーを確認

### プロジェクトが見つからない

**症状**: `infisical init`でプロジェクトが表示されない

**解決方法**:
- Infisicalダッシュボードでプロジェクトが作成されているか確認
- プロジェクト名のスペルミスを確認
- 組織が正しいか確認

### シークレットが取得できない

**症状**: `infisical secrets get`でエラー

**解決方法**:
- シークレットが正しい環境に追加されているか確認
- シークレット名のスペルミスを確認（大文字小文字を区別）
- プロジェクトが正しく初期化されているか確認（`.infisical.json`が存在）

## 📚 参考リンク

- [Infisical設定ガイド](./infisical-setup.md) - 詳細な設定方法
- [Infisical クイックスタート](./infisical-quick-start.md) - 初期設定手順
- [API Keys設定ガイド](./api-keys-setup.md) - APIキーの取得方法
- [Infisical公式ドキュメント](https://infisical.com/docs)

---

**最終更新**: 2025-01-23
**バージョン**: 1.0.0






















