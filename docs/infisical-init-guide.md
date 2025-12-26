# Infisical プロジェクト初期化ガイド

## 現在の状況

- ✅ Infisical CLIのインストール完了
- ✅ Infisicalに必要なキーをすべて格納完了
- ⏳ プロジェクトの初期化が必要

## プロジェクト初期化の手順

### ステップ1: infisical init を実行

PowerShellで以下を実行：

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# プロジェクトディレクトリに移動（既にいる場合は不要）
cd C:\Users\chiba\hadayalab-automation-platform

# Infisicalプロジェクトを初期化
infisical init
```

### ステップ2: プロンプトで選択

#### 1. ホスティングオプションの選択

```
? Select your hosting option:
  > Infisical Cloud (US Region)
    Infisical Cloud (EU Region)
    Self-Hosting or Dedicated Instance
```

**選択**: 矢印キー（↑↓）で「Infisical Cloud (US Region)」を選択し、Enterキーを押す

#### 2. プロジェクトの選択

```
? Select a project:
  > hadayalab-automation-platform
    (他のプロジェクトがあれば表示されます)
```

**選択**: 矢印キー（↑↓）で「hadayalab-automation-platform」を選択し、Enterキーを押す

#### 3. 環境の選択

```
? Select an environment:
  > development
    staging
    production
```

**選択**: 矢印キー（↑↓）で「development」を選択し、Enterキーを押す

### ステップ3: 初期化の確認

初期化が完了すると、以下のメッセージが表示されます：

```
✓ Successfully initialized Infisical project
```

また、プロジェクトディレクトリに `.infisical.json` ファイルが作成されます：

```json
{
  "projectId": "正しいプロジェクトID",
  "projectSlug": "hadayalab-automation-platform",
  "environment": "development"
}
```

## 初期化後の確認

### シークレットの取得

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# シークレットを取得
infisical secrets get N8N_API_KEY
infisical secrets get N8N_API_URL
```

### すべてのシークレットを確認

```powershell
# 環境変数を更新
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# JSON形式でエクスポート
infisical secrets export --output json

# または、.env形式でエクスポート
infisical secrets export --output dotenv
```

## トラブルシューティング

### プロジェクトが表示されない

**症状**: `infisical init`でプロジェクトが表示されない

**解決方法**:
1. Infisicalダッシュボードでプロジェクトが作成されているか確認
2. プロジェクト名のスペルミスを確認
3. 組織が正しいか確認
4. `infisical login`を再実行して認証を確認

### 認証エラー

**症状**: 認証に失敗する

**解決方法**:
1. `infisical login`を再実行
2. ブラウザでInfisicalアカウントにログインしているか確認
3. トークンの有効期限を確認

### 環境が表示されない

**症状**: 環境が表示されない

**解決方法**:
1. Infisicalダッシュボードで環境が作成されているか確認
2. デフォルト環境（development, staging, production）が存在するか確認

## 次のステップ

初期化が完了したら：

1. **シークレットの確認**
   - `infisical secrets get N8N_API_KEY` でシークレットが取得できるか確認

2. **ローカル開発環境での使用**
   - [Infisical設定ガイド](./infisical-setup.md) を参照
   - 環境変数として読み込む方法
   - .envファイルを生成する方法

3. **GitHub Actionsとの統合**
   - [Infisical設定ガイド](./infisical-setup.md#-github-actionsでの使用方法) を参照
   - サービストークンの作成
   - GitHub Secretsへの追加

## 参考リンク

- [Infisical設定ガイド](./infisical-setup.md) - 詳細な設定方法
- [Infisical クイックスタート](./infisical-quick-start.md) - 初期設定手順
- [Infisical セットアップ完了ガイド](./infisical-setup-complete.md) - セットアップ完了後の手順

---

**最終更新**: 2025-01-23
**バージョン**: 1.0.0





















