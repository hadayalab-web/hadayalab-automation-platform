# n8n Personal Access Token 取得ガイド

## 📋 概要

n8n CloudのPersonal Access Tokenは、n8n REST APIにアクセスするために使用します。ワークフローの削除、実行、環境変数の管理などに必要です。

**注意**: これはGitリポジトリ用のPersonal Access Token（GitHub、GitLabなど）とは異なります。

---

## 🔑 n8n Cloud Personal Access Tokenの取得方法

### ステップ1: n8n Cloud Dashboardにアクセス

1. n8n Cloud Dashboardを開く: https://hadayalab.app.n8n.cloud
2. ログイン

### ステップ2: Personal Access Tokenを作成

1. **Settings** → **API** → **Personal Access Tokens** に移動
2. **「Create Token」** ボタンをクリック
3. トークン名を入力（例: "API Access Token" または "Workflow Management"）
4. **「Create」** をクリック
5. **トークンをコピー**（一度しか表示されません！）

### ステップ3: トークンを安全に保存

- トークンは一度しか表示されないため、必ずコピーして安全な場所に保存してください
- 推奨: Infisicalなどのシークレット管理ツールに保存

---

## 🔗 Gitリポジトリ用Personal Access Tokenとの違い

### n8n Cloud Personal Access Token
- **用途**: n8n REST APIへのアクセス
- **取得先**: n8n Cloud Dashboard → Settings → API → Personal Access Tokens
- **使用例**: ワークフロー削除、実行、環境変数管理

### Gitリポジトリ用Personal Access Token
- **用途**: Gitリポジトリへのアクセス（Source Control機能）
- **取得先**: GitHub/GitLab/BitbucketなどのGitプロバイダー
- **使用例**: ワークフローのGit同期
- **参考**: [n8n Source Control Setup](https://docs.n8n.io/source-control-environments/setup/#https-authentication-using-personal-access-tokens)

---

## 📝 使用例

### ワークフロー削除

```powershell
$token = "YOUR_N8N_PERSONAL_ACCESS_TOKEN"
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

# ワークフローを削除
Invoke-RestMethod -Uri "$baseUrl/workflows/WORKFLOW_ID" -Method Delete -Headers $headers
```

### ワークフロー一覧取得

```powershell
$token = "YOUR_N8N_PERSONAL_ACCESS_TOKEN"
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$workflows = Invoke-RestMethod -Uri "$baseUrl/workflows" -Method Get -Headers $headers
$workflows.data | Select-Object id, name, active
```

---

## 🔐 セキュリティのベストプラクティス

1. **トークンの保護**
   - トークンをGitにコミットしない
   - 環境変数やシークレット管理ツール（Infisicalなど）で管理

2. **トークンの有効期限**
   - 定期的にトークンをローテーション
   - 不要になったトークンは削除

3. **権限の最小化**
   - 必要な権限のみを持つトークンを作成
   - 用途ごとに異なるトークンを使用

---

## 📚 参考リンク

- [n8n API Documentation](https://docs.n8n.io/api/)
- [n8n API Authentication](https://docs.n8n.io/api/authentication/)
- [n8n Source Control Setup](https://docs.n8n.io/source-control-environments/setup/#https-authentication-using-personal-access-tokens) - Gitリポジトリ用PATについて

---

## ⚠️ トラブルシューティング

### エラー: "Unauthorized" または "401"

**原因**: Personal Access Tokenが無効または間違っている

**解決方法**:
1. トークンが正しくコピーされているか確認
2. トークンが有効期限内か確認
3. 新しいトークンを作成

### エラー: "Forbidden" または "403"

**原因**: トークンに必要な権限がない

**解決方法**:
1. トークンに適切な権限があるか確認
2. 管理者に権限の確認を依頼

---

**最終更新**: 2025-01-24















