# Google Workspace / Chatwork Control ワークフロー インポートガイド

**作成日**: 2025-12-26
**対象フォルダ**: Personal（プロジェクトID: `fPT5foO8DCTDBr0k`）

---

## 📋 概要

このガイドでは、Google Workspace / Chatwork Controlワークフローをn8n CloudのPersonalフォルダにインポートする手順を説明します。

---

## 🚀 インポート手順

### ステップ1: GitHubからワークフローファイルを取得

ワークフローファイルは以下の場所にあります：
- **ファイル**: `workflows/webhook-google-workspace-chatwork-control.json`
- **GitHub URL**: https://github.com/hadayalab-web/hadayalab-automation-platform/blob/main/workflows/webhook-google-workspace-chatwork-control.json
- **Raw URL**: https://raw.githubusercontent.com/hadayalab-web/hadayalab-automation-platform/main/workflows/webhook-google-workspace-chatwork-control.json

### ステップ2: n8n Cloudにインポート

#### 方法1: n8n Dashboardからインポート（推奨）

1. **Personalフォルダに移動**
   - n8n Dashboard: https://hadayalab.app.n8n.cloud
   - Personalフォルダ: https://hadayalab.app.n8n.cloud/projects/fPT5foO8DCTDBr0k/workflows

2. **ワークフローをインポート**
   - 「+」ボタンをクリック → 「Import from URL」または「Import from File」を選択
   - Raw URLを入力: `https://raw.githubusercontent.com/hadayalab-web/hadayalab-automation-platform/main/workflows/webhook-google-workspace-chatwork-control.json`
   - または、ローカルファイルをダウンロードしてインポート

#### 方法2: API経由でインポート

```bash
python scripts/import-workflow-to-n8n.py workflows/webhook-google-workspace-chatwork-control.json
```

**注意**: API経由でインポートした場合、Personalフォルダに移動する必要があります（n8n Dashboardで手動移動）。

### ステップ3: 認証情報の設定

#### Google Workspace認証情報

各Google Workspaceノードに認証情報を設定：

1. **Gmail Sendノード**
   - ノードを開く
   - Credentials → 「Gmail OAuth2 account for admin@cryptotradeacademy.io」を選択

2. **Google Sheets Readノード**
   - ノードを開く
   - Credentials → 「Google Sheets OAuth2 account for admin@cryptotradeacademy.io」を選択

**注意**: 認証情報が存在しない場合は、先に作成する必要があります。

#### Chatwork API Token

Chatwork API Tokenはワークフローに直接設定されています：
- Token: `e973fd7311ae06d1deb377bd1ecb7d8e`

**セキュリティ**: 将来的には環境変数またはCredentialsに移行することを推奨します。

### ステップ4: ワークフローを有効化

1. ワークフローを開く
2. 「Activate」ボタンをクリック
3. 「Available in MCP」を有効化（MCP経由でアクセスする場合）

---

## ✅ 確認事項

インポート後、以下の項目を確認してください：

- [ ] ワークフローがPersonalフォルダに存在する
- [ ] すべてのノードが正しく接続されている
- [ ] Google Workspace認証情報が設定されている
- [ ] Chatwork API Tokenが正しく設定されている
- [ ] ワークフローが有効化されている
- [ ] Webhook URLが生成されている

---

## 🔗 関連ドキュメント

- [Google Workspace / Chatwork Control ワークフロー詳細](./google-workspace-chatwork-control-workflow.md)
- [n8n完全SSOT](../SSOT/n8n-complete-SSOT.md)
- [フォルダ整理ガイド](../setup/n8n-folder-organization-guide.md)

---

**最終更新**: 2025-12-26

