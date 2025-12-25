# n8n Cloud同期運用

## 概要

このリポジトリは **n8n Cloud** (https://hadayalab.app.n8n.cloud) の
ワークフローSSOT（Single Source of Truth）です。

## 環境構成

- **実行環境**: n8n Cloud
- **開発ツール**: Cursor + n8n-mcp
- **バージョン管理**: GitHub

## 運用方針

- **パターン1（GitHub→Cloud一方向）を採用**
- **GitHubが唯一の信頼できる情報源（SSOT）**
- **n8n Cloud UIは動作確認・モニタリング用途**

## 標準フロー（GitHub→Cloud）

### 方法1: URLからインポート（推奨）

1. Cursorでワークフロー編集
2. ローカル検証
   - `npm run format`（自動整形）
   - `npm run format:check`（確認）
3. GitHubへコミット・プッシュ
   ```bash
   git add workflows/your-workflow.json
   git commit -m "Add/Update workflow: your-workflow"
   git push origin main
   ```
4. GitHub Actions自動検証
   - ※push後、GitHub Actionsが自動実行されgreenになることを確認してから次のステップへ（推奨）
5. n8n DashboardでURLからインポート
   - n8n Dashboardで「Import Workflow from URL」を開く
   - 以下の形式のURLを入力：
     ```
     https://raw.githubusercontent.com/hadayalab-web/hadayalab-automation-platform/main/workflows/your-workflow.json
     ```
   - 「Import」ボタンをクリック
   - ワークフローがインポートされたら、必要に応じて「Activate」ボタンで有効化
6. Cloud UIで動作確認

**重要**: ファイルがGitHubにプッシュされていない場合、URLからのインポートは404エラーになります。必ずコミット・プッシュを完了してからインポートしてください。

### 方法2: ファイルから直接インポート

1. Cursorでワークフロー編集
2. ローカル検証
   - `npm run format`（自動整形）
   - `npm run format:check`（確認）
3. n8n Dashboardで「Import from File」を選択
4. `workflows/your-workflow.json` ファイルを選択してインポート
5. 必要に応じて「Activate」ボタンで有効化
6. Cloud UIで動作確認

**注意**: 方法2は緊急時のみ使用（SSOT設計方針では方法1を推奨）

### 方法3: n8n-mcp経由でCloud反映（将来実装予定）

1. Cursorでワークフロー編集
2. ローカル検証
3. GitHubへpush
4. GitHub Actions自動検証
5. n8n-mcp経由でCloud反映（`@n8n-local`を使用）
6. Cloud UIで動作確認

## 例外フロー（Cloud→GitHub取り込み）

緊急時にCloud UIで編集した場合の手順:

1. Cloud UIで編集実施
2. 直後にExport（JSONダウンロード）
3. `workflows/`へ保存（命名規約準拠）
4. `npm run format`（自動整形）
5. GitHubへpush（取り込み）
6. 以降GitHubを正とする

## 重要な注意事項

- **同じワークフローをCloudとGitHub両方で同時編集禁止**
- **UI編集後は必ず取り込みコミット作成**
- **Credentials/Secretsは環境依存（JSON非含有）**

#### Import/Deployの違い

- n8n Cloud UIでの「Import」は上書き（デプロイ）
- Cloud変更のGitHub反映は必ずExport→取り込み手順を実施

#### Export JSONの特性

- Export時にメタデータ（updatedAt等）含有
- 差分が荒れるのは仕様
- Prettierで整形されるが、重要な変更のみに注目

## なぜGitHub Actionsが必要か

- CloudからのExport JSONはフォーマット揺れあり
- 壊れたJSONがSSOTに混入するのを防止
- Prettierで差分を読みやすく保持

## ワークフローインポート手順（実証済み）

### ✅ 成功した手順

以下の手順で、GitHubのワークフローファイルをn8n Cloudに正常にインポートできることを確認済みです：

1. **ワークフローファイルをGitHubにコミット・プッシュ**
   ```bash
   git add workflows/simple-time-check.json
   git commit -m "Add simple-time-check workflow"
   git push origin main
   ```

2. **n8n DashboardでURLからインポート**
   - n8n Dashboardで「Import Workflow from URL」を開く
   - 以下のURLを入力：
     ```
     https://raw.githubusercontent.com/hadayalab-web/hadayalab-automation-platform/main/workflows/simple-time-check.json
     ```
   - 「Import」ボタンをクリック
   - ワークフローが正常にインポートされることを確認

3. **ワークフローを有効化**
   - インポートされたワークフローを開く
   - 「Activate」ボタン（または「Publish」ボタン）をクリックして有効化

4. **動作確認**
   - Webhook URLを確認
   - ワークフローを実行して動作を確認

### ⚠️ よくあるエラーと対処法

- **「The URL does not point to valid JSON file!」エラー**
  - **原因**: ファイルがGitHubにプッシュされていない、またはJSON形式が無効
  - **対処**: ファイルをコミット・プッシュし、JSON形式を確認（`_comment`などの非標準フィールドを削除）

- **404エラー**
  - **原因**: ファイルがGitHubに存在しない、またはブランチ名が間違っている
  - **対処**: GitHubでファイルの存在を確認し、正しいブランチ名を使用

- **「Conflicting Webhook Path」エラー（Publishできない）**
  - **原因**: 同じWebhookパスを使用するワークフローが既にActive状態
  - **対処方法1**: 既存のワークフローを無効化
    ```bash
    python scripts/deactivate_workflow.py
    ```
  - **対処方法2**: 新しいワークフローのWebhookパスを変更
    - ワークフローファイルの`webhookId`と`path`パラメータを変更
    - GitHubにコミット・プッシュ
    - 再度インポート

## Import時の注意事項

### URLからのインポート

- **前提条件**: ワークフローファイルがGitHubにコミット・プッシュされている必要があります
- **URL形式**: `https://raw.githubusercontent.com/hadayalab-web/hadayalab-automation-platform/main/workflows/{workflow-name}.json`
- **ブランチ名**: `main`ブランチを使用（他のブランチの場合は、`main`をブランチ名に置き換え）
- **404エラー**: ファイルがGitHubにプッシュされていない場合、404エラーが発生します。その場合は、まずコミット・プッシュを完了してください

### ファイルからのインポート

- **推奨度**: 緊急時のみ（SSOT設計方針ではURLからのインポートを推奨）
- **手順**: n8n Dashboardで「Import from File」を選択し、ローカルファイルを選択

### 共通の注意事項

- **上書き vs 新規**: n8n Cloud UIでImportする際、既存ワークフローを上書きするか、新規作成するかを選択できます
- **有効化状態**: Importされたワークフローはデフォルトで無効（Inactive）状態です。必要に応じて「Activate」ボタンで有効化してください
- **資格情報（Credentials）**: JSONに含まれません。Import後、手動で設定が必要です
- **Webhook URL**: n8n Cloud固有のURLが自動生成されます
- **JSON形式**: 有効なJSON形式である必要があります（`_comment`などの非標準フィールドは削除してください）

## セットアップ

### Cursor MCP設定

`~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "n8n": {
      "command": "n8n-mcp",
      "args": [],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
        "N8N_API_KEY": "your_api_key"
      }
    }
  }
}
```

参考: `.env.example`

