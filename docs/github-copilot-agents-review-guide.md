# GitHub Copilot Agents レビュー依頼ガイド

## 🎯 GitHub Copilot Agentsとは

GitHub Copilot Agentsは、GitHub.com上で利用できるAIエージェント機能です。IssueやPull Requestに対して、コードレビュー、プロジェクト分析、改善提案などを自動で実行できます。

## 🚀 レビュー依頼方法

### 方法1: Issueコメント経由（推奨）

#### ステップ1: Issueを作成または既存Issueを使用
```bash
gh issue create --title "レビュー依頼" --body "レビュー依頼内容"
```

#### ステップ2: IssueにコメントでGitHub Copilot Agentsをメンション
```markdown
@copilot 以下のファイルをレビューしてください:

1. n8n-workflows-design.md
2. workflow-1-trial-onboarding.json
3. README-n8n-implementation.md

特に以下の点を確認してください:
- ワークフロー設計の妥当性
- JSON形式の正確性
- エラーハンドリング
- セキュリティ設定

改善提案もお願いします。
```

#### ステップ3: GitHub CLIでコメント追加
```bash
gh issue comment <ISSUE_NUMBER> --body "@copilot [レビュー依頼内容]"
```

### 方法2: Pull Request経由

#### ステップ1: ブランチを作成
```bash
git checkout -b feature/n8n-workflows-review
git push origin feature/n8n-workflows-review
```

#### ステップ2: Pull Requestを作成
```bash
gh pr create --title "n8nワークフロー実装 - レビュー依頼" --body "@copilot このPRをレビューしてください"
```

#### ステップ3: PRコメントでレビュー依頼
GitHub.com上でPRを開き、コメント欄に以下を入力：
```markdown
@copilot このPRをレビューしてください。

特に以下の点を確認してください:
- コード品質
- セキュリティ
- パフォーマンス
- エラーハンドリング
```

### 方法3: GitHub.com上で直接依頼

1. **GitHub.comにアクセス**
   - https://github.com/hadayalab-web/hadayalab-automation-platform

2. **Issue #1を開く**
   - https://github.com/hadayalab-web/hadayalab-automation-platform/issues/1

3. **コメント欄に以下を入力**
   ```markdown
   @copilot このIssueのレビュー依頼内容を確認して、以下のファイルをレビューしてください:

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

4. **コメントを投稿**
   - GitHub Copilot Agentsが自動でレビューを開始

## 📋 レビュー依頼テンプレート

### 基本テンプレート
```markdown
@copilot 以下のファイルをレビューしてください:

**レビュー対象ファイル:**
- [ファイル名1]
- [ファイル名2]

**重点レビュー項目:**
1. [項目1]
2. [項目2]
3. [項目3]

**既知の問題:**
- [問題1]
- [問題2]

改善提案もお願いします。
```

### n8nワークフロー専用テンプレート
```markdown
@copilot このn8nワークフロー実装をレビューしてください:

**レビュー対象:**
- n8n-workflows-design.md（設計ドキュメント）
- workflow-1-trial-onboarding.json（実装JSON）

**確認ポイント:**
1. **ワークフロー設計**
   - ノードの接続が適切か
   - エラーハンドリングが考慮されているか
   - パフォーマンス最適化が考慮されているか

2. **JSON実装**
   - JSON形式が正しいか（n8nでインポート可能か）
   - 式（expressions）の記述が正しいか
   - 認証情報の参照が適切か

3. **セキュリティ**
   - API Keyの管理方法
   - Webhook認証の設定
   - データの取り扱い

**既知の問題:**
- Wait Nodeの長時間待機（6時間、12時間）の実装方法
- エラーハンドリングノードが未実装
- API Keyのプレースホルダー使用

改善提案と具体的な修正方法を教えてください。
```

## 🔧 CLI経由でのレビュー依頼

### GitHub CLIを使用
```bash
# Issueコメントでレビュー依頼
gh issue comment <ISSUE_NUMBER> --body "@copilot [レビュー依頼内容]"

# ファイルから読み込んでコメント追加
gh issue comment <ISSUE_NUMBER> --body-file review-request.txt
```

### 実装例
```bash
# Issue #1にレビュー依頼コメントを追加
gh issue comment 1 --body "@copilot このIssueのレビュー依頼内容を確認して、n8n-workflows-design.md、workflow-1-trial-onboarding.json、README-n8n-implementation.mdをレビューしてください。特にWait Nodeの長時間待機、Switch Nodeの分岐、エラーハンドリング、セキュリティ設定を重点的に確認してください。改善提案もお願いします。"
```

## 📊 レビュー結果の確認

### GitHub.com上で確認
1. Issue #1を開く
2. コメント欄でGitHub Copilot Agentsの回答を確認
3. 改善提案をIssueに記録

### CLI経由で確認
```bash
# Issueのコメントを確認
gh issue view <ISSUE_NUMBER> --comments

# 最新のコメントを確認
gh issue view <ISSUE_NUMBER> --comments | tail -20
```

## 💡 ベストプラクティス

### 1. 明確な依頼内容
- レビュー対象ファイルを明記
- 重点レビュー項目をリスト化
- 既知の問題を事前に記載

### 2. コンテキストの提供
- 関連ドキュメントへの参照
- 実装の背景や目的
- 制約条件や要件

### 3. フォローアップ
- レビュー結果を確認
- 改善提案を実装
- 再レビュー依頼（必要に応じて）

## 🎯 現在のレビュー依頼状況

### Issue #1
- **URL**: https://github.com/hadayalab-web/hadayalab-automation-platform/issues/1
- **状態**: OPEN
- **コメント**: レビュー依頼コメント追加済み
- **次のステップ**: GitHub Copilot Agentsの回答を待つ

### レビュー依頼コメント
- **追加日**: 2025-12-23
- **内容**: `@copilot` メンション付きレビュー依頼
- **対象ファイル**:
  - n8n-workflows-design.md
  - workflow-1-trial-onboarding.json
  - README-n8n-implementation.md

## 📚 参考リンク

- [GitHub Copilot Agents Documentation](https://docs.github.com/en/copilot/github-copilot-agents)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Issue #1](https://github.com/hadayalab-web/hadayalab-automation-platform/issues/1)

---

**作成日**: 2025-12-23
**目的**: GitHub Copilot Agentsへのレビュー依頼方法をまとめたガイド












