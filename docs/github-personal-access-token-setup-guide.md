# GitHub Personal Access Token 取得・設定ガイド

**最終更新**: 2025-01-24
**バージョン**: 1.0.0

---

## 🎯 目的

GitHub APIを使用して、AI（私）からGitHub Copilot Agents/Copilotに指示を出すために、GitHub Personal Access Tokenを取得・設定します。

---

## 🚀 取得手順

### ステップ1: Developer Settingsにアクセス

1. **GitHub.comにログイン**
   - https://github.com

2. **Settingsにアクセス**
   - 右上のプロフィールアイコンをクリック
   - 「Settings」を選択

3. **Developer Settingsにアクセス**
   - 左サイドバーの一番下「Developer settings」をクリック
   - または、直接アクセス: https://github.com/settings/apps

### ステップ2: Personal Access Tokensにアクセス

1. **左サイドバーで「Personal access tokens」をクリック**
   - 現在のページで「Personal access tokens」が表示されているはずです

2. **「Tokens (classic)」を選択**
   - 「Fine-grained tokens」ではなく、「Tokens (classic)」を選択
   - 理由: GitHub APIで必要なスコープを設定しやすいため

### ステップ3: 新しいトークンを生成

1. **「Generate new token」をクリック**
   - 「Generate new token (classic)」をクリック

2. **Note（メモ）を入力**
   - 例: `Cursor AI - GitHub Copilot Agents Integration`
   - 用途を明確にするため、わかりやすい名前を付けます

3. **Expiration（有効期限）を設定**
   - 推奨: `90 days` または `No expiration`（セキュリティポリシーに応じて）
   - 注意: `No expiration`はセキュリティリスクが高いため、定期的に更新することを推奨

4. **Select scopes（スコープ）を選択**
   - 以下のスコープを選択:
     - ✅ **repo** (Full control of private repositories)
       - リポジトリへの完全アクセス
       - Issue/PRの作成・編集・削除に必要
     - ✅ **workflow** (Update GitHub Action workflows)
       - GitHub Actionsワークフローの更新に必要
     - ✅ **write:packages** (Upload packages to GitHub Package Registry)
       - パッケージのアップロードに必要（オプション）

5. **「Generate token」をクリック**

### ステップ4: トークンをコピー

1. **トークンが表示される**
   - ⚠️ **重要**: このトークンは一度しか表示されません
   - 必ずコピーして安全な場所に保存してください

2. **トークンをコピー**
   - 表示されたトークンをコピー
   - 例: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

3. **「Done」をクリック**
   - トークンが安全に保存されたことを確認

---

## 🔐 Infisicalへの保存

### ステップ1: Infisical CLIでトークンを保存

```bash
infisical secrets set GITHUB_PERSONAL_ACCESS_TOKEN="your-token-here" --token YOUR_INFISICAL_TOKEN --projectId 446f131c-be8d-45e5-a83a-4154e34501a5
```

### ステップ2: 保存確認

```bash
infisical secrets get GITHUB_PERSONAL_ACCESS_TOKEN --token YOUR_INFISICAL_TOKEN --projectId 446f131c-be8d-45e5-a83a-4154e34501a5 --output json
```

---

## ✅ 動作確認

### 接続テストを実行

```bash
python scripts/test-copilot-connection.py
```

**期待される結果**:
- ✅ GitHub API keyが取得できる
- ✅ Issueが作成される
- ✅ @copilotメンションが追加される

---

## ⚠️ セキュリティ注意事項

### トークンの管理

1. **トークンは秘密情報として扱う**
   - 他人と共有しない
   - 公開リポジトリにコミットしない
   - `.gitignore`に追加（必要に応じて）

2. **定期的に更新**
   - 90日ごとに更新することを推奨
   - 不要になったトークンは削除

3. **最小権限の原則**
   - 必要なスコープのみを選択
   - 不要なスコープは選択しない

### トークンの削除

不要になったトークンは削除してください：

1. **Developer Settings → Personal access tokens → Tokens (classic)**
2. 削除したいトークンの右側の「Delete」をクリック
3. 確認して削除

---

## 📋 必要なスコープ一覧

| スコープ | 説明 | 必須 |
|---------|------|------|
| **repo** | リポジトリへの完全アクセス | ✅ 必須 |
| **workflow** | GitHub Actionsワークフローの更新 | ✅ 必須（GitHub Actions使用時） |
| **write:packages** | パッケージのアップロード | ⚠️ オプション |

---

## 🔄 次のステップ

トークンを取得・設定したら：

1. **接続テストを実行**
   ```bash
   python scripts/test-copilot-connection.py
   ```

2. **GitHub Copilot Agents/Copilotへの指示をテスト**
   - Cursor Chatで「GitHub Copilot Agentsに、このコードをレビューするように指示して」と試す

3. **完全自動化ワークフローのテスト**
   - ユーザー → AI（私） → GitHub Copilot Agents/Copilot → Actions → n8nワークフロー

---

**このガイドは、GitHub Personal Access Token取得・設定に関する唯一の信頼できる情報源（SSOT）です。**














