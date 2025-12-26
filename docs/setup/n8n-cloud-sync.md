# n8n Cloud同期運用（インポート・エクスポート手順）

## 📋 役割分担

### 人間の役割: n8n Cloud UIでのインポート・エクスポート操作のみ

このドキュメントは、**人間が実行するインポート・エクスポート手順**を説明します。

- ✅ n8n Cloud UIでのインポート・エクスポート操作（オプション）

### Cursorの役割: すべて（n8n APIを使用したインポート/エクスポート、オプションでGitHubへのコミット・プッシュ）

Cursorは以下の作業を自動的に実行します：

- ✅ ワークフローの作成・編集
- ✅ コード生成・リファクタリング
- ✅ バグ修正
- ✅ テスト実行
- ✅ **n8n APIを使用したワークフローのインポート/エクスポート（GitHub経由不要）**
- ✅ **GitHubへのコミット・プッシュ（オプション・バックアップとして）**

**原則**: ワークフローのインポート/エクスポートはGitHub経由でなくてもよい。n8n APIを使用して直接実行できる。

**詳細**: [hadayalab-automation-platform-SSOT.md](../SSOT/hadayalab-automation-platform-SSOT.md) を参照

---

## 概要

このリポジトリは **n8n Cloud** (https://hadayalab.app.n8n.cloud) の
ワークフローSSOT（Single Source of Truth）です。

## 環境構成

- **実行環境**: n8n Cloud
- **開発ツール**: Cursor + n8n-mcp
- **バージョン管理**: GitHub

## 運用方針

- **ワークフローのインポート/エクスポートはGitHub経由でなくてもよい**
- **n8n APIを使用して直接インポート/エクスポート可能**
- **GitHubはバックアップ/バージョン管理として使用（必須ではない）**
- **n8n Cloud UIは動作確認・モニタリング用途**

## 標準フロー（Cursor → n8n Cloud）

### 方法1: n8n APIを使用したインポート（推奨・Cursorの役割）

**前提条件**: Cursorでワークフローの編集が完了していること（GitHubへのプッシュは不要）

#### ステップ1-3: Cursorの役割（自動実行）

1. **Cursorでワークフロー編集**
2. **ローカル検証**
   - `npm run format`（自動整形）
   - `npm run format:check`（確認）
3. **n8n APIを使用してインポート**
   - インポートスクリプトを使用: `python scripts/import-workflow-to-n8n.py workflows/workflow-name.json`
   - またはn8n-MCPパッケージを使用: `@n8n-local workflows/workflow-name.jsonをインポートして`
   - ワークフローIDとURLを確認

4. **GitHubへコミット・プッシュ（オプション・バックアップとして）**
   - Cursorが自動的にコミット・プッシュを実行
   - GitHubはバックアップ/バージョン管理として使用

**重要**: ワークフローのインポート/エクスポートはGitHub経由でなくてもよい。n8n APIを使用して直接インポート/エクスポートできる。

### 方法2: n8n Cloud UIからインポート（オプション・人間の役割）

**注意**: 方法2はオプション。方法1（n8n API）が推奨。

#### ステップ1-2: Cursorの役割（自動化）

**原則**: CursorはGitHubにシームレスにつながっているため、以下の作業を自動的に実行します。

1. **Cursorでワークフロー編集**
2. **ローカル検証**
   - `npm run format`（自動整形）
   - `npm run format:check`（確認）
3. **GitHubへコミット・プッシュ（自動実行）**
   - Cursorが自動的にコミット・プッシュを実行
   - 人間の操作は不要

#### ステップ3-6: 人間の役割（手動実行）

3. **n8n Dashboardで「Import from File」を選択**
   - n8n Dashboard (https://hadayalab.app.n8n.cloud) にログイン
   - 「Workflows」メニューをクリック
   - 「Import from File」をクリック
4. **`workflows/your-workflow.json` ファイルを選択してインポート**
5. **必要に応じて「Activate」ボタンで有効化**
6. **Cloud UIで動作確認**

---

## ワークフローファイルのURL一覧（人間がインポート時に使用）

以下のURLは、n8n Cloud UIの「Import Workflow from URL」で使用してください：

### 基本形式

```
https://raw.githubusercontent.com/hadayalab-web/hadayalab-automation-platform/main/workflows/{workflow-name}.json
```

### 利用可能なワークフロー

- `whop-control.json`: `https://raw.githubusercontent.com/hadayalab-web/hadayalab-automation-platform/main/workflows/whop-control.json`
- `webhook-google-workspace-control.json`: `https://raw.githubusercontent.com/hadayalab-web/hadayalab-automation-platform/main/workflows/webhook-google-workspace-control.json`
- その他のワークフロー: `workflows/README.md` を参照

**重要**: ファイルがGitHubにプッシュされていない場合、URLからのインポートは404エラーになります。必ずコミット・プッシュを完了してからインポートしてください。

## 例外フロー（Cloud→GitHub取り込み・人間の役割）

**注意**: このフローは緊急時のみ使用。原則としてGitHub→Cloudの一方向フローを維持してください。

### ステップ1-2: 人間の役割（手動実行）

1. **Cloud UIで編集実施**
   - n8n Cloud Dashboardでワークフローを編集

2. **直後にExport（JSONダウンロード）**
   - ワークフローを開く
   - 「Export」ボタンをクリック
   - JSONファイルをダウンロード

### ステップ3-6: Cursorの役割（自動化）

**原則**: CursorはGitHubにシームレスにつながっているため、以下の作業を自動的に実行します。

3. **`workflows/`へ保存（命名規約準拠）**
   - ダウンロードしたJSONファイルを `workflows/` に保存
   - ファイル名は命名規約に従う（`docs/workflows/workflow-conventions.md` を参照）

4. **`npm run format`（自動整形）**
   - Cursorが自動的に実行

5. **GitHubへpush（取り込み・自動実行）**
   - Cursorが自動的にコミット・プッシュを実行
   - コミットメッセージ: "Import from Cloud: your-workflow"
   - 人間の操作は不要

6. **以降GitHubを正とする**
   - GitHubがSSOTとして機能
   - 今後は方法1（URLからインポート）を使用

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

---

## 📚 関連ドキュメント

- **n8n MCP設定**: `docs/setup/n8n-mcp-setup-complete.md`
- **ワークフロー命名規約**: `docs/workflows/workflow-conventions.md`
- **プロジェクトSSOT**: `docs/SSOT/hadayalab-automation-platform-SSOT.md`

