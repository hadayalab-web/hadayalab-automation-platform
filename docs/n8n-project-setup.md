# n8nプロジェクトセットアップガイド

## 📋 プロジェクト情報

- **プロジェクトID**: `9D29Es58GIo6IPkZ`
- **ワークフロー一覧URL**: https://hadayalab.app.n8n.cloud/projects/9D29Es58GIo6IPkZ/workflows
- **新規ワークフロー作成URL**: https://hadayalab.app.n8n.cloud/workflow/new?projectId=9D29Es58GIo6IPkZ

## 🔑 Personal Access Tokenの取得（必須）

API経由でワークフローを操作するには、Personal Access Tokenが必要です。

### 手順

1. **n8n Cloud Dashboardにアクセス**
   - URL: `https://hadayalab.app.n8n.cloud`
   - ログイン

2. **Personal Access Tokenを作成**
   - 右上のユーザーアイコンをクリック
   - 「Settings」を選択
   - 左メニューから「API」を選択
   - 「Personal Access Tokens」セクションで「Create Token」をクリック
   - トークン名を入力（例: "API Access Token"）
   - 「Create」をクリック
   - **トークンをコピー**（一度しか表示されません！）

3. **Infisicalに保存**
   - Infisical Dashboard → プロジェクト `hadayalab-automation-platform-c79-q`
   - 「Secrets」タブを開く
   - 「Add Secret」をクリック
   - シークレット名: `N8N_PERSONAL_ACCESS_TOKEN`
   - 値: コピーしたトークンを貼り付け
   - 「Save」をクリック

## 🚀 API接続テスト

Personal Access Tokenを取得したら、以下のコマンドで接続テストを実行：

```powershell
.\scripts\test-n8n-rest-api-with-project.ps1
```

このスクリプトは：
- InfisicalからPersonal Access Tokenを取得
- プロジェクトID `9D29Es58GIo6IPkZ` を含むAPIエンドポイントに接続
- ワークフロー一覧を取得して表示

## 📥 ワークフロー1のインポート

API接続が成功したら、ワークフロー1をインポート：

```powershell
.\scripts\import-workflow-1.ps1
```

このスクリプトは：
- `workflow-1-trial-onboarding.json` を読み込む
- プロジェクトIDを設定
- n8n REST API経由でワークフローを作成

## 🔄 代替方法: Dashboard経由でインポート

API経由でのインポートが難しい場合は、Dashboard経由でインポート：

1. **ワークフロー一覧ページにアクセス**
   - https://hadayalab.app.n8n.cloud/projects/9D29Es58GIo6IPkZ/workflows

2. **ワークフローをインポート**
   - 「Import from File」をクリック
   - `workflow-1-trial-onboarding.json` を選択
   - インポート完了を確認

3. **認証情報を設定**
   - ワークフローを開く
   - 各ノードで認証情報を設定：
     - Gmail Node: Gmail OAuth2認証
     - HTTP Request Node: Whop API Key認証

## 📝 次のステップ

1. ✅ Personal Access Tokenを取得してInfisicalに保存
2. ✅ API接続テストを実行
3. ✅ ワークフロー1をインポート
4. ✅ 認証情報を設定
5. ✅ テスト実行

---

**作成日**: 2025-01-23
**ステータス**: プロジェクト作成完了、Personal Access Token取得待ち





















