# Infisical Webダッシュボードでのシークレット確認方法

## 現在表示しているページについて

現在表示している「Secret Sharing」ページは、**シークレットを共有リンクで共有する機能**です。通常のシークレット管理とは異なります。

## 正しい手順: プロジェクトページに移動

### ステップ1: プロジェクトページに移動

1. **左サイドバーから「Projects」をクリック**
   - 現在の「Secret Sharing」の上または下に「Projects」メニューがあるはずです
   - または、上部の「HadayaLab」ロゴの近くにプロジェクト一覧があるかもしれません

2. **プロジェクトを選択**
   - 「hadayalab-automation-platform」プロジェクトをクリック

### ステップ2: シークレットの確認

プロジェクトページに移動すると：

1. **左サイドバーに「Secrets」メニューが表示されます**
2. **「Secrets」をクリック**
3. **環境を選択**（development, staging, production）
4. **シークレット一覧が表示されます**
   - `N8N_API_KEY`
   - `N8N_API_URL`

## より簡単な方法: CLIで初期化

Webダッシュボードで確認するよりも、**CLIで`infisical init`を実行する方が簡単**です。

### 手順

PowerShellで以下を実行：

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# プロジェクトディレクトリに移動
cd C:\Users\chiba\hadayalab-automation-platform

# Infisicalプロジェクトを初期化
infisical init
```

**プロンプトで以下を選択:**
1. ホスティングオプション: `Infisical Cloud (US Region)`
2. プロジェクト: `hadayalab-automation-platform`
3. 環境: `development`

これで、`.infisical.json`ファイルが作成され、以降はCLIでシークレットを簡単に取得できます。

## シークレットの確認方法

### 方法1: Webダッシュボードで確認

1. プロジェクトページに移動
2. 「Secrets」をクリック
3. 環境を選択
4. シークレット一覧を確認

### 方法2: CLIで確認（推奨）

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# プロジェクトを初期化（初回のみ）
infisical init

# シークレットを取得
infisical secrets get N8N_API_KEY
infisical secrets get N8N_API_URL
```

## 推奨される方法

**CLIで`infisical init`を実行することを強く推奨します。**

理由：
- ✅ より簡単で迅速
- ✅ プロジェクトIDが自動的に取得される
- ✅ 以降のコマンドで認証が不要
- ✅ 自動化やスクリプトで使用しやすい

## 次のステップ

1. **CLIで初期化**（推奨）
   ```powershell
   infisical init
   ```

2. **または、Webダッシュボードで確認**
   - プロジェクトページに移動
   - 「Secrets」をクリック
   - シークレットを確認

どちらの方法でも、シークレットが正しく設定されていることを確認できます。

---

**最終更新**: 2025-01-23
**バージョン**: 1.0.0






















