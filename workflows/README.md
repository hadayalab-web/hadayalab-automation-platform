# n8n Workflows

管理方法:
- Cursor + n8n-mcp で作成
- GitHubにコミット・プッシュ後、n8n Cloud UIでURLからインポート

## 📋 ワークフロー一覧

### cursor-gmail-chatwork-calendar-control
- **ファイル**: `workflows/webhook-google-workspace-chatwork-calendar-cursor-control.json`
- **目的**: CursorからGmail、Chatwork、Google Calendarを制御
- **フォルダ**: Personal
- **ドキュメント**: `docs/workflows/cursor-gmail-chatwork-calendar-control-workflow.md`

### google-workspace-control
- **ファイル**: `workflows/webhook-google-workspace-control.json`
- **対象フォルダ**: hadayalab-automation-platform
- **説明**: Google Workspace（Gmail、Sheets、Drive、Calendar）制御ワークフロー

### google-workspace-chatwork-control
- **ファイル**: `workflows/webhook-google-workspace-chatwork-control.json`
- **対象フォルダ**: Personal
- **説明**: Google Workspace（Gmail、Sheets）とChatwork統合ワークフロー
- **説明**: CursorからMCP経由でGoogle Workspace（Gmail、Google Sheets、Google Drive）を制御
- **アカウント**: `admin@cryptotradeacademy.io`
- **ドキュメント**: `docs/workflows/google-workspace-control-workflow.md`

### @simple-time-check
- **ファイル**: `workflows/simple-time-check.json`
- **説明**: 簡単な実験用ワークフロー（現在時刻取得）
- **機能**: Webhook TriggerでHTTPリクエストを受け取り、World Time APIから東京の現在時刻を取得してJSONで返す
- **タグ**: test, experiment, simple
- **参照方法**: `@workflows/simple-time-check.json` または `@simple-time-check`
- **n8n Cloudへのインポート方法**:

  **方法1: ファイルから直接インポート（推奨）**
  1. n8n Dashboardで「Import from File」を選択
  2. `workflows/simple-time-check.json` ファイルを選択してインポート

  **方法2: URLからインポート（GitHubにコミット・プッシュ後）**
  1. このファイルをGitHubにコミット・プッシュしてください：
     ```bash
     git add workflows/simple-time-check.json
     git commit -m "Add simple-time-check workflow"
     git push origin main
     ```
  2. n8n Dashboardで「Import Workflow from URL」を開き、以下のURLを入力してください：
     ```
     https://raw.githubusercontent.com/hadayalab-web/hadayalab-automation-platform/main/workflows/simple-time-check.json
     ```

  **注意**: ファイルがGitHubにプッシュされていない場合、URLからのインポートは404エラーになります。その場合は方法1を使用してください。

### @github-copilot-ai-review-assistant
- **ファイル**: `workflows/github-copilot-ai-review-assistant.json`
- **説明**: GitHub Copilot Agents AI補助レビューワークフロー
- **機能**:
  - Cursor Chatから指示を受けて、GitHub Copilot Agentsに自動レビュー依頼
  - Issueを作成し、`@copilot`メンション付きレビュー依頼を自動送信
  - Copilotの応答を監視し、結果をCursor Chatに返す
- **タグ**: github, copilot, ai-assistant, automation, review
- **参照方法**: `@workflows/github-copilot-ai-review-assistant.json` または `@github-copilot-ai-review-assistant`
- **必要な環境変数**:
  - `GITHUB_PERSONAL_ACCESS_TOKEN`: GitHub API認証用のPersonal Access Token
- **Cursor Chatでの使用方法**:
  ```
  @n8n-cloud github-copilot-ai-review-assistantワークフローを実行して、file=src/main.ts, focus=security,performance
  ```
- **n8n Cloudへのインポート**:
  1. このファイルをGitHubにコミット・プッシュしてください
  2. n8n Dashboardで「Import Workflow from URL」を開き、以下のURLを入力してください：
     ```
     https://raw.githubusercontent.com/hadayalab-web/hadayalab-automation-platform/main/workflows/github-copilot-ai-review-assistant.json
     ```
  3. 環境変数`GITHUB_PERSONAL_ACCESS_TOKEN`をn8n Cloudに設定してください

### @manual-hello-world-test
- **ファイル**: `workflows/manual-hello-world-test.json`
- **説明**: MCPテスト用ワークフロー
- **機能**: Manual Triggerで「Hello from n8n-mcp!」メッセージを返す
- **タグ**: test, mcp, validated
- **参照方法**: `@workflows/manual-hello-world-test.json` または `@manual-hello-world-test`

## 🔍 Cursor Chatでの使用方法

### ワークフローを参照する

```
@workflows/simple-time-check.json を検証して
@workflows/simple-time-check.json をn8n Cloudにインポートして
@simple-time-check ワークフローを実行して
```

### ワークフロー一覧を確認する

```
@workflows/workflow-index.md を参照して、利用可能なワークフローを表示して
```

詳細は [Cursor Chatでワークフローをメンションする方法](../docs/cursor-workflow-mention-guide.md) を参照してください。

