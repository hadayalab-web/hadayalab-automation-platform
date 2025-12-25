# Infisical トークンを使用したログイン方法

## 状況

Infisical CLIにトークンを使用してログインする場合、以下の情報が必要です：

1. **アクセストークン** - 提供済み ✅
2. **プロジェクトID** - Infisicalダッシュボードから取得が必要

## 方法1: プロジェクトIDを取得して使用（推奨）

### ステップ1: プロジェクトIDの取得

1. **Infisicalダッシュボードにアクセス**
   - https://app.infisical.com にログイン
   - プロジェクト `hadayalab-automation-platform` を選択

2. **プロジェクトIDを確認**
   - プロジェクトのSettingsまたはURLからプロジェクトIDを確認
   - プロジェクトIDは通常、UUID形式（例: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）

### ステップ2: トークンとプロジェクトIDを使用

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# トークンとプロジェクトIDを設定
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
$projectId = "your-project-id-here"

# シークレットを取得
infisical secrets get N8N_API_KEY --token $token --projectId $projectId
infisical secrets get N8N_API_URL --token $token --projectId $projectId
```

## 方法2: infisical init を使用（最も簡単）

トークンを使用する代わりに、`infisical init`を実行してプロジェクトを初期化する方法が最も簡単です。

### ステップ1: プロジェクトの初期化

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# プロジェクトディレクトリに移動
cd C:\Users\chiba\hadayalab-automation-platform

# Infisicalプロジェクトを初期化
infisical init
```

**プロンプトで以下を選択:**
1. ホスティングオプション: `Infisical Cloud (US Region)` を選択
2. プロジェクト: `hadayalab-automation-platform` を選択
3. 環境: `development` を選択

### ステップ2: シークレットの確認

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# シークレットを取得
infisical secrets get N8N_API_KEY
infisical secrets get N8N_API_URL

# すべてのシークレットをエクスポート
infisical secrets export --output json
```

## 方法3: ブラウザでログイン（標準的な方法）

トークンを使用する代わりに、標準的なログイン方法を使用することもできます。

### ステップ1: ログイン

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Infisicalにログイン
infisical login
```

**手順:**
1. ホスティングオプションを選択（通常は `Infisical Cloud (US Region)`）
2. ブラウザが開くので、Infisicalアカウントにログイン
3. 「Authorize」をクリックしてCLIへのアクセスを許可

### ステップ2: プロジェクトの初期化

ログイン後、`infisical init`を実行してプロジェクトを初期化します。

## 推奨される方法

**最も簡単で確実な方法は、`infisical init`を使用することです。**

この方法では：
- ブラウザでの認証が不要（既にトークンを持っている場合）
- プロジェクトIDを手動で入力する必要がない
- 環境の選択が簡単

## トラブルシューティング

### プロジェクトIDが見つからない

**解決方法:**
- Infisicalダッシュボードでプロジェクトを開く
- URLからプロジェクトIDを確認（例: `https://app.infisical.com/project/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）
- または、プロジェクトのSettingsからプロジェクトIDを確認

### トークンが無効

**解決方法:**
- トークンの有効期限を確認（JWTトークンには有効期限があります）
- 新しいトークンを取得
- `infisical login`を実行して新しいトークンを取得

### 認証エラー

**解決方法:**
- Infisicalアカウントにログインしているか確認
- トークンが正しいか確認
- `infisical login`を再実行

## 次のステップ

プロジェクトの初期化が完了したら：

1. **シークレットの確認**
   ```powershell
   infisical secrets get N8N_API_KEY
   infisical secrets get N8N_API_URL
   ```

2. **ローカル開発環境での使用**
   - [Infisical設定ガイド](./infisical-setup.md) を参照
   - 環境変数として読み込む方法
   - .envファイルを生成する方法

3. **GitHub Actionsとの統合**
   - [Infisical設定ガイド](./infisical-setup.md#-github-actionsでの使用方法) を参照

---

**最終更新**: 2025-01-23
**バージョン**: 1.0.0












