# GitHub Copilot Agents レビュー開始手順

## 🚀 手動でGitHub Copilot Agentsを起動する方法

GitHub Copilot Agentsは、GitHub.com上で手動で起動する必要があります。

### 方法1: GitHub.com上で直接起動（推奨）

1. **Issue #1を開く**
   - https://github.com/hadayalab-web/hadayalab-automation-platform/issues/1

2. **GitHub Copilot Chatを開く**
   - サイドバーのCopilotアイコンをクリック
   - または、`@` キーを押す

3. **レビュー依頼を入力**
   ```
   @copilot Issue #1のレビュー依頼内容を確認して、以下のファイルをレビューしてください:

   1. n8n-workflows-design.md
   2. workflow-1-trial-onboarding.json
   3. README-n8n-implementation.md

   特に以下の点を重点的にレビューしてください:
   - Wait Nodeの長時間待機（6時間、12時間）の実装方法
   - Switch Nodeの6市場分岐の効率性
   - 式（expressions）の記述が正しいか
   - エラーハンドリングが適切か
   - セキュリティ設定が適切か

   改善提案もお願いします。
   ```

4. **送信**
   - GitHub Copilot Agentsが自動でレビューを開始

### 方法2: Issueコメントで直接依頼

1. **Issue #1のコメント欄を開く**
   - https://github.com/hadayalab-web/hadayalab-automation-platform/issues/1

2. **以下のコメントを入力**
   ```markdown
   @copilot このIssueのレビュー依頼内容を確認して、n8n-workflows-design.md、workflow-1-trial-onboarding.json、README-n8n-implementation.mdをレビューしてください。

   特に以下の点を重点的にレビューしてください:
   1. Wait Nodeの長時間待機（6時間、12時間）の実装方法が適切か
   2. Switch Nodeの6市場分岐の実装が効率的か
   3. 式（expressions）の記述が正しいか
   4. エラーハンドリングが適切か
   5. セキュリティ設定（API Key管理、Webhook認証）が適切か

   改善提案と具体的な修正方法を教えてください。
   ```

3. **コメントを投稿**
   - GitHub Copilot Agentsが自動でレビューを開始

### 方法3: GitHub Copilot Agentsパネルから起動

1. **GitHub.comのナビゲーションバーで「Agents」をクリック**
   - または、https://github.com/hadayalab-web/hadayalab-automation-platform/issues/1 を開いて「Agents」タブをクリック

2. **新しいタスクを作成**
   - 「New task」をクリック
   - タスク名: "n8nワークフロー実装レビュー"

3. **タスク内容を入力**
   ```
   以下のファイルをレビューしてください:
   - n8n-workflows-design.md
   - workflow-1-trial-onboarding.json
   - README-n8n-implementation.md

   重点レビュー項目:
   1. Wait Nodeの長時間待機実装
   2. Switch Nodeの6市場分岐
   3. 式（expressions）の記述
   4. エラーハンドリング
   5. セキュリティ設定

   改善提案もお願いします。
   ```

4. **タスクを開始**
   - GitHub Copilot Agentsが自動でレビューを開始

## ⚠️ 注意事項

### Copilotが起動しない場合の確認事項

1. **GitHub Copilot Proの有効化**
   - GitHub Copilot Proのサブスクリプションが必要
   - Settings → Copilot で確認

2. **リポジトリへのアクセス権限**
   - 書き込み権限が必要
   - リポジトリの設定を確認

3. **Issueの割り当て**
   - IssueにCopilotが割り当てられているか確認
   - 割り当てられていない場合は手動で割り当て

4. **コメントの形式**
   - `@copilot` を必ずメンション
   - 明確な指示を含める

## 📋 現在の状況

- **Issue #1**: OPEN
- **URL**: https://github.com/hadayalab-web/hadayalab-automation-platform/issues/1
- **コメント**: レビュー依頼コメント追加済み（2件）
- **Copilot割り当て**: 試行済み

## 🎯 次のアクション

1. **GitHub.comでIssue #1を開く**
2. **GitHub Copilot Chatを開く**（サイドバーのCopilotアイコン）
3. **上記のレビュー依頼コマンドを入力**
4. **送信してレビュー開始**

---

**作成日**: 2025-12-23
**目的**: GitHub Copilot Agentsを手動で起動するためのガイド





















