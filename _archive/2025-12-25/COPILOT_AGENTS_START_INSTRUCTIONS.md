# ⚠️ GitHub Copilot Agents レビュー開始手順

## 🎯 重要: GitHub Copilot Agentsは手動で起動が必要です

GitHub Copilot Agentsは、**GitHub.com上で手動で起動する必要があります**。CLI経由では自動起動しません。

## 🚀 今すぐレビューを開始する方法

### 方法1: GitHub Copilot Chatから起動（推奨）

1. **Issue #1を開く**
   ```
   https://github.com/hadayalab-web/hadayalab-automation-platform/issues/1
   ```

2. **GitHub Copilot Chatを開く**
   - サイドバーの **Copilotアイコン** をクリック
   - または、コメント欄で `@` キーを押す

3. **以下のコマンドをコピー＆ペースト**
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

   改善提案と具体的な修正方法を教えてください。
   ```

4. **Enterキーを押して送信**
   - GitHub Copilot Agentsが自動でレビューを開始

### 方法2: Issueコメント欄から直接依頼

1. **Issue #1のコメント欄を開く**
   - https://github.com/hadayalab-web/hadayalab-automation-platform/issues/1

2. **以下のコメントを入力**
   ```markdown
   @copilot このIssueのレビュー依頼内容を確認して、n8n-workflows-design.md、workflow-1-trial-onboarding.json、README-n8n-implementation.mdをレビューしてください。

   特に以下の点を重点的にレビューしてください:
   1. Wait Nodeの長時間待機（6時間、12時間）の実装方法
   2. Switch Nodeの6市場分岐の効率性
   3. 式（expressions）の記述が正しいか
   4. エラーハンドリングが適切か
   5. セキュリティ設定が適切か

   改善提案と具体的な修正方法を教えてください。
   ```

3. **コメントを投稿**
   - GitHub Copilot Agentsが自動でレビューを開始

## ✅ レビュー開始の確認

### 確認方法

1. **GitHub Copilot Chatで応答が表示される**
   - "Reviewing..." などのメッセージ
   - レビューが進行中であることが確認できる

2. **Issue #1のコメント欄に新しいコメントが追加される**
   - GitHub Copilot Agentsからの回答がコメントとして追加

3. **GitHub Copilot Agentsパネルでタスクが表示される**
   - ナビゲーションバーの「Agents」をクリック
   - 実行中のタスクが表示される

## ⚠️ レビューが開始されない場合

### 確認事項

1. **GitHub Copilot Proの有効化**
   - Settings → Copilot で確認
   - https://github.com/settings/copilot

2. **リポジトリへのアクセス権限**
   - 書き込み権限が必要

3. **コメントの形式**
   - `@copilot` を必ずメンション
   - 明確な指示を含める

## 📋 現在の状況

- **Issue #1**: OPEN
- **URL**: https://github.com/hadayalab-web/hadayalab-automation-platform/issues/1
- **コメント**: レビュー依頼コメント追加済み（2件）
- **次のステップ**: **GitHub.com上でGitHub Copilot Chatを開いてレビュー依頼を送信**

---

**重要**: GitHub Copilot Agentsは、GitHub.com上で手動で起動する必要があります。上記の手順に従って、GitHub.comでレビューを開始してください。





















