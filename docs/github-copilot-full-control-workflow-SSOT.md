# GitHub Copilot Agents & Copilot 完全制御ワークフロー SSOT

**最終更新**: 2025-01-24
**最終検証**: 2025-01-24（公式ドキュメントと既存実装の調査）
**バージョン**: 1.0.0
**メンテナー**: HadayaLab

---

## 📚 公式リファレンス

- **GitHub Copilot Agents**: [GitHub Copilot Agents Documentation](https://docs.github.com/ja/copilot/responsible-use/copilot-coding-agent)
- **GitHub Copilot**: [GitHub Copilot Documentation](https://docs.github.com/ja/copilot)
- **GitHub API**: [GitHub REST API](https://docs.github.com/ja/rest)
- **GitHub CLI**: [GitHub CLI Documentation](https://cli.github.com/manual/)

---

## 🎯 概要

**GitHub Copilot AgentsとGitHub Copilotをn8nワークフローから完全に制御する設計方針**

このドキュメントは、n8nワークフローを使用してGitHub Copilot AgentsとGitHub Copilotを制御する方法をまとめた**唯一の信頼できる情報源（SSOT）**です。

---

## ⚠️ 重要な制約事項

### GitHub Copilot Agentsの制約

1. **手動起動が必要**: GitHub Copilot AgentsはGitHub.com上で手動で起動する必要があります
   - CLI経由では自動起動しません
   - セキュリティ上の理由により制限されています

2. **エージェントパネル**: GitHubのナビゲーションバーにある「Agents」ボタンからエージェントパネルを開く必要があります

3. **権限要件**: リポジトリへの書き込み権限を持つユーザーからの操作にのみ応答します

### GitHub Copilotの制約

1. **API制限**: GitHub Copilotには専用のREST APIが存在しません
2. **IDE統合**: Visual Studio CodeなどのIDEに統合して使用します
3. **Chat機能**: GitHub.com上のCopilot Chatを使用します

---

## 🔄 実装可能な制御方法

### 方法1: GitHub API経由での自動化（推奨）

**実装可能な操作**:

1. **Issue自動作成 + Copilotメンション**
   - GitHub APIでIssueを作成
   - コメントに`@copilot`をメンション
   - レビュー依頼内容を自動送信

2. **PR自動作成 + Copilotメンション**
   - GitHub APIでPRを作成
   - コメントに`@copilot`をメンション
   - コードレビュー依頼を自動送信

3. **コメント自動追加**
   - 既存のIssue/PRにコメントを追加
   - `@copilot`をメンションしてタスクを委託

4. **エージェントパネル状態の監視**
   - GitHub APIでIssue/PRのコメントを取得
   - Copilotの応答を監視

### 方法2: GitHub CLI経由での自動化

**実装可能な操作**:

1. **Issue作成**
   ```bash
   gh issue create --title "レビュー依頼" --body "@copilot [レビュー依頼内容]"
   ```

2. **PR作成**
   ```bash
   gh pr create --title "コードレビュー依頼" --body "@copilot [レビュー依頼内容]"
   ```

3. **コメント追加**
   ```bash
   gh issue comment <ISSUE_NUMBER> --body "@copilot [タスク内容]"
   ```

### 方法3: n8nワークフロー + GitHub API

**完全自動化ワークフロー**:

1. **トリガー**: Webhook、スケジュール、手動実行
2. **GitHub API**: Issue/PR作成、コメント追加
3. **監視**: Copilotの応答を監視
4. **通知**: 完了時に通知

---

## 📋 ワークフロー設計

### ワークフロー1: 自動レビュー依頼ワークフロー

**目的**: コード変更を自動的にGitHub Copilot Agentsにレビュー依頼

**トリガー**:
- Git Push（Webhook）
- スケジュール実行
- 手動実行

**ワークフロー構造**:

```
1. Webhook Trigger (Git Push)
   ↓
2. Switch Node (ブランチ判定)
   - mainブランチ → PR作成
   - featureブランチ → PR作成
   ↓
3. GitHub API Node (PR作成)
   - Title: "自動レビュー依頼: {ブランチ名}"
   - Body: "@copilot このPRをレビューしてください..."
   ↓
4. GitHub API Node (コメント追加)
   - @copilotメンション
   - レビュー依頼内容
   ↓
5. Wait Node (Copilot応答待機)
   - 5分間待機
   ↓
6. GitHub API Node (コメント取得)
   - PRのコメントを取得
   - Copilotの応答を確認
   ↓
7. IF Node (応答確認)
   - Copilot応答あり → 通知
   - Copilot応答なし → 再試行または通知
   ↓
8. Slack/Email Node (通知)
   - レビュー完了通知
```

### ワークフロー2: 定期コードレビューワークフロー

**目的**: 定期的にプロジェクト全体をGitHub Copilot Agentsにレビュー依頼

**トリガー**:
- スケジュール（毎週月曜日）

**ワークフロー構造**:

```
1. Schedule Trigger (毎週月曜日 9:00)
   ↓
2. GitHub API Node (Issue作成)
   - Title: "定期コードレビュー: {日付}"
   - Body: "@copilot 以下のファイルをレビューしてください..."
   ↓
3. GitHub API Node (ファイル一覧取得)
   - 変更されたファイルを取得
   ↓
4. GitHub API Node (コメント追加)
   - @copilotメンション
   - レビュー依頼内容（ファイル一覧）
   ↓
5. Wait Node (Copilot応答待機)
   - 10分間待機
   ↓
6. GitHub API Node (コメント取得)
   - Issueのコメントを取得
   ↓
7. IF Node (応答確認)
   - Copilot応答あり → 結果を保存
   - Copilot応答なし → 再試行
   ↓
8. Google Sheets/Database Node (結果保存)
   - レビュー結果を保存
```

### ワークフロー3: エージェントパネル監視ワークフロー

**目的**: GitHub Copilot Agentsのタスク実行状況を監視

**トリガー**:
- スケジュール（5分ごと）

**ワークフロー構造**:

```
1. Schedule Trigger (5分ごと)
   ↓
2. GitHub API Node (Issue一覧取得)
   - 最近作成されたIssueを取得
   ↓
3. GitHub API Node (コメント取得)
   - 各Issueのコメントを取得
   ↓
4. Filter Node (Copilot応答フィルタ)
   - Copilotの応答を含むコメントを抽出
   ↓
5. IF Node (新規応答確認)
   - 新規応答あり → 通知
   - 新規応答なし → 終了
   ↓
6. Slack/Email Node (通知)
   - Copilot応答通知
```

### ワークフロー4: カスタムエージェント制御ワークフロー

**目的**: AGENTS.mdファイルを使用したカスタムエージェントの制御

**トリガー**:
- Webhook（AGENTS.md更新時）
- 手動実行

**ワークフロー構造**:

```
1. Webhook Trigger (AGENTS.md更新)
   ↓
2. GitHub API Node (ファイル取得)
   - AGENTS.mdファイルを取得
   ↓
3. Code Node (AGENTS.md解析)
   - エージェント定義を解析
   ↓
4. GitHub API Node (Issue作成)
   - カスタムエージェント用のIssueを作成
   ↓
5. GitHub API Node (コメント追加)
   - @copilotメンション
   - カスタムエージェントのタスクを委託
```

---

## 🔧 実装詳細

### GitHub API認証

**認証方法**:
- **Personal Access Token (PAT)**: GitHub APIで使用
- **OAuth App**: より高度な権限が必要な場合

**n8n設定**:
```json
{
  "credentials": {
    "githubApi": {
      "accessToken": "{{ $env.GITHUB_PERSONAL_ACCESS_TOKEN }}"
    }
  }
}
```

### GitHub API エンドポイント

**Issue作成**:
```
POST /repos/{owner}/{repo}/issues
```

**PR作成**:
```
POST /repos/{owner}/{repo}/pulls
```

**コメント追加**:
```
POST /repos/{owner}/{repo}/issues/{issue_number}/comments
POST /repos/{owner}/{repo}/pulls/{pull_number}/comments
```

**コメント取得**:
```
GET /repos/{owner}/{repo}/issues/{issue_number}/comments
GET /repos/{owner}/{repo}/pulls/{pull_number}/comments
```

### Copilotメンション形式

**Issue/PR作成時**:
```markdown
@copilot 以下のファイルをレビューしてください:

1. file1.js
2. file2.js

特に以下の点を確認してください:
- コード品質
- セキュリティ
- パフォーマンス
```

**コメント追加時**:
```markdown
@copilot このPRをレビューしてください。

特に以下の点を確認してください:
- エラーハンドリング
- テストカバレッジ
- ドキュメント
```

---

## 📊 制御可能な操作一覧

| 操作 | 実装方法 | 自動化レベル | 実証状況 |
|------|---------|------------|---------|
| **Issue作成 + Copilotメンション** | GitHub API | ✅ 完全自動化 | ✅ 実装可能 |
| **PR作成 + Copilotメンション** | GitHub API | ✅ 完全自動化 | ✅ 実装可能 |
| **コメント追加 + Copilotメンション** | GitHub API | ✅ 完全自動化 | ✅ 実装可能 |
| **Copilot応答監視** | GitHub API | ✅ 完全自動化 | ✅ 実装可能 |
| **エージェントパネル起動** | ❌ 手動のみ | ⚠️ 手動必要 | ❌ 自動化不可 |
| **カスタムエージェント作成** | AGENTS.md + GitHub API | ✅ 完全自動化 | ✅ 実装可能 |
| **レビュー結果取得** | GitHub API | ✅ 完全自動化 | ✅ 実装可能 |
| **レビュー結果通知** | Slack/Email | ✅ 完全自動化 | ✅ 実装可能 |

---

## 🚀 実装手順

### ステップ1: GitHub Personal Access Tokenの取得

1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 「Generate new token (classic)」をクリック
3. スコープを選択:
   - `repo` (リポジトリへの完全アクセス)
   - `issues` (Issue管理)
   - `pull_requests` (PR管理)
4. トークンを生成し、Infisicalに保存

### ステップ2: n8nワークフローの作成

1. **Webhook Trigger**を追加
2. **GitHub API Node**を追加
3. **認証情報**を設定（Personal Access Token）
4. **エンドポイント**を設定
5. **リクエストボディ**を設定

### ステップ3: ワークフローのテスト

1. テスト用のIssueを作成
2. Copilotメンションを含むコメントを追加
3. Copilotの応答を確認
4. ワークフローの動作を確認

---

## ⚠️ 制限事項と回避策

### 制限1: エージェントパネルの手動起動

**問題**: GitHub Copilot Agentsは手動で起動する必要がある

**回避策**:
- Issue/PR作成時に`@copilot`をメンション
- コメントにレビュー依頼内容を記載
- Copilotが自動的に応答する可能性がある（GitHub.com上で確認が必要）

### 制限2: Copilot応答のタイミング

**問題**: Copilotの応答タイミングが予測できない

**回避策**:
- Wait Nodeで一定時間待機
- 定期的にコメントを取得して応答を確認
- タイムアウトを設定

### 制限3: API制限

**問題**: GitHub APIにはレート制限がある

**回避策**:
- リクエスト間隔を調整
- エラーハンドリングを実装
- レート制限エラーを検出して再試行

---

## 📝 実装例

### n8nワークフローJSON例

```json
{
  "name": "GitHub Copilot自動レビュー依頼",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "copilot-review-request",
        "responseMode": "responseNode"
      },
      "type": "n8n-nodes-base.webhook",
      "name": "Webhook Trigger"
    },
    {
      "parameters": {
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "httpMethod": "POST",
        "url": "=https://api.github.com/repos/hadayalab-web/hadayalab-automation-platform/issues",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Authorization",
              "value": "=Bearer {{ $env.GITHUB_PERSONAL_ACCESS_TOKEN }}"
            },
            {
              "name": "Accept",
              "value": "application/vnd.github.v3+json"
            }
          ]
        },
        "sendBody": true,
        "contentType": "json",
        "bodyParameters": {
          "parameters": [
            {
              "name": "title",
              "value": "=自動レビュー依頼: {{ $json.branch }}"
            },
            {
              "name": "body",
              "value": "=@copilot このPRをレビューしてください。\n\n特に以下の点を確認してください:\n- コード品質\n- セキュリティ\n- パフォーマンス"
            }
          ]
        }
      },
      "type": "n8n-nodes-base.httpRequest",
      "name": "GitHub API - Issue作成"
    }
  ]
}
```

---

## 🔄 更新履歴

### 2025-01-24 (v1.0.0)
- 初版作成
- GitHub Copilot AgentsとGitHub Copilotの制御方法を調査
- n8nワークフロー設計を考案
- 実装可能な操作と制限事項を明記

---

**このドキュメントは、GitHub Copilot Agents & Copilot完全制御ワークフローに関する唯一の信頼できる情報源（SSOT）です。**














