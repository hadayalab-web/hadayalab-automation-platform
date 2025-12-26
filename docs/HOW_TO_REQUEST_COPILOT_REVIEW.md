# GitHub Copilot Agent レビュー依頼方法 - 実践ガイド

このドキュメントでは、実際に使用している**PR経由でのCopilot Agentレビュー依頼方法**を説明します。

---

## 🎯 この方法の特徴

### ✅ メリット

1. **コード差分が明確**
   - PRで変更内容が一目瞭然
   - Copilot Agentが変更箇所を正確に把握

2. **レビューコメントがコード行にリンク**
   - 具体的な指摘がコードの該当箇所に紐づく
   - 修正が容易

3. **レビュー履歴が残る**
   - PRの会話履歴として保存される
   - チーム内で共有しやすい

4. **自動化可能**
   - CLI（GitHub CLI）でPR作成とコメント追加が可能
   - スクリプト化できる

### ⚠️ 注意点

- PRを作成する必要がある（小さな変更には不向きかも）
- Copilot Agentは手動で起動する必要がある（GitHub.com上）

---

## 📋 手順（私がcryptosignal-aiで実践した方法）

### ステップ1: レビューブランチの作成

```bash
# 現在のブランチを確認
git branch --show-current

# レビュー用ブランチを作成
git checkout -b copilot-review-issue-1

# 変更があればコミット
git add .
git commit -m "docs: Add n8n workflow documentation"
```

### ステップ2: ブランチをプッシュ

```bash
git push -u origin copilot-review-issue-1
```

### ステップ3: PRを作成

GitHub CLIを使用：

```bash
gh pr create \
  --title "docs: Add n8n workflow documentation for Copilot review" \
  --body "## Review Request

This PR contains documentation for n8n workflows that need review.

### Files to Review
- n8n-workflows-design.md
- workflow-1-trial-onboarding.json
- README-n8n-implementation.md

### Review Focus
- Wait Node implementation
- Switch Node efficiency
- Expression correctness
- Error handling
- Security settings

### Related
- Related to Issue #1

---

**Note**: This PR is created for GitHub Copilot Agent review." \
  --base main \
  --head copilot-review-issue-1
```

または、GitHub.com上で手動作成：

1. GitHub.comのリポジトリページを開く
2. 「Pull requests」タブをクリック
3. 「New pull request」をクリック
4. base: `main`、compare: `copilot-review-issue-1`を選択
5. タイトルと説明を入力
6. 「Create pull request」をクリック

### ステップ4: PRにCopilot Agentレビューコメントを追加

GitHub CLIを使用：

```bash
# PR番号を確認（例: PR #2）
gh pr list --head copilot-review-issue-1

# レビュー依頼コメントを追加
gh pr comment 2 --body "@copilot Please review this PR and provide feedback on:

## Files to Review
- n8n-workflows-design.md
- workflow-1-trial-onboarding.json
- README-n8n-implementation.md

## Review Focus
1. **Wait Node Implementation**: Are 6-hour and 12-hour waits appropriate?
2. **Switch Node Efficiency**: Is the 6-market branching efficient?
3. **Expressions**: Are expressions correctly written?
4. **Error Handling**: Is error handling sufficient?
5. **Security**: Are security settings appropriate?

## Specific Questions
- Wait Nodeの長時間待機（6時間、12時間）の実装方法は適切ですか？
- Switch Nodeの6市場分岐は効率的ですか？
- 式（expressions）に問題はありませんか？
- エラーハンドリングは十分ですか？
- セキュリティ上の懸念はありませんか？

Please provide improvement suggestions and specific fixes.

Thank you! 🙏"
```

### ステップ5: GitHub.comでCopilot Agentが起動するのを待つ

Copilot Agentは通常、コメントに`@copilot`が含まれると自動的に処理を開始します。
数分以内にレビューが開始されるはずです。

---

## 🔧 スクリプト化（推奨）

### スクリプト例: `scripts/create-copilot-review-pr.js`

```javascript
// scripts/create-copilot-review-pr.js
const { execSync } = require('child_process');

async function createCopilotReviewPR(issueNumber, files, focusAreas) {
  try {
    // 1. レビューブランチを作成
    const reviewBranch = `copilot-review-issue-${issueNumber}`;
    execSync(`git checkout -b ${reviewBranch}`, { stdio: 'inherit' });

    // 2. 空のコミットを作成（PRを作成するため）
    execSync('git commit --allow-empty -m "chore: Trigger Copilot Agent review"', { stdio: 'inherit' });

    // 3. ブランチをプッシュ
    execSync(`git push -u origin ${reviewBranch}`, { stdio: 'inherit' });

    // 4. PR本文を作成
    const prBody = `## Copilot Agent Review Request

This PR is created for GitHub Copilot Agent code review.

### Related Issue
Closes #${issueNumber}

### Files to Review
${files.map(f => `- \`${f}\``).join('\n')}

### Review Focus
${focusAreas.map(a => `- ${a}`).join('\n')}

---

**Note**: This PR is specifically created for Copilot Agent review.`;

    // 5. PRを作成
    const prUrl = execSync(
      `gh pr create --title "Copilot Agent Review: Issue #${issueNumber}" --body "${prBody.replace(/"/g, '\\"')}" --base main --head ${reviewBranch}`,
      { encoding: 'utf-8' }
    ).trim();

    console.log(`\n✅ Pull Request created: ${prUrl}\n`);

    // 6. PR番号を取得
    const prNumber = prUrl.match(/\/pull\/(\d+)/)?.[1];
    if (!prNumber) {
      throw new Error('Failed to extract PR number');
    }

    // 7. Copilot Agentレビューコメントを追加
    const reviewComment = `@copilot Please review this PR and provide feedback on:

## Files to Review
${files.map(f => `- \`${f}\``).join('\n')}

## Review Focus
${focusAreas.map((a, i) => `${i + 1}. ${a}`).join('\n')}

Please provide:
- Code quality feedback
- Improvement suggestions
- Specific fixes

Thank you! 🙏`;

    execSync(
      `gh pr comment ${prNumber} --body "${reviewComment.replace(/"/g, '\\"')}"`,
      { stdio: 'inherit' }
    );

    console.log(`\n✅ Review request comment added to PR #${prNumber}\n`);

    return prUrl;
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

// 使用例
const issueNumber = process.argv[2] || 1;
const files = [
  'n8n-workflows-design.md',
  'workflow-1-trial-onboarding.json',
  'README-n8n-implementation.md',
];
const focusAreas = [
  'Wait Node implementation (6-hour, 12-hour waits)',
  'Switch Node efficiency (6-market branching)',
  'Expression correctness',
  'Error handling',
  'Security settings',
];

createCopilotReviewPR(issueNumber, files, focusAreas);
```

**使用方法**:
```bash
node scripts/create-copilot-review-pr.js 1
```

---

## 📝 実際の例（cryptosignal-aiプロジェクト）

### 実装したスクリプト

1. **`scripts/create-copilot-review-pr.js`**
   - PR作成からレビュー依頼コメント追加まで自動化

2. **`scripts/request-copilot-review.js`**
   - 既存のIssueにレビュー依頼コメントを追加

### 使用したコマンド

```bash
# 1. PRを作成
gh pr create \
  --title "fix: Address critical issues from Copilot review" \
  --body "## Summary\n\nThis PR addresses critical issues..." \
  --base main

# 2. PR番号を取得してコメントを追加
gh pr comment 7 --body "@copilot Please review this PR..."
```

### 実際のPR例

**PR #7**: https://github.com/hadayalab-web/cryptosignal-ai/pull/7

- タイトル: "fix: Address critical issues from Copilot review"
- 本文: 修正内容の説明
- コメント: `@copilot`メンション付きレビュー依頼

---

## 🎓 ベストプラクティス

### 1. PR本文の書き方

**推奨する構成**:
- Summary（概要）
- Changes（変更内容）
- Files Changed（変更ファイル）
- Related（関連するIssue/PR）
- Testing（テスト状況）
- Next Steps（次のステップ）

### 2. レビュー依頼コメントの書き方

**必須要素**:
- `@copilot`メンション
- レビュー対象ファイルの明確な指定
- レビューフォーカス（何を見てほしいか）
- 具体的な質問

**推奨する構成**:
```markdown
@copilot Please review this PR and provide feedback on:

## Files to Review
- file1.md
- file2.js

## Review Focus
1. Specific area 1
2. Specific area 2

## Specific Questions
1. Question 1?
2. Question 2?

Please provide improvement suggestions and specific fixes.

Thank you! 🙏
```

### 3. ブランチ命名規則

推奨パターン:
- `copilot-review-issue-{issue_number}`
- `copilot-review-{description}`
- `review/{description}`

例:
- `copilot-review-issue-1`
- `copilot-review-n8n-workflows`
- `review/error-handling`

---

## 🔄 ワークフロー比較

### パターンA: Issue + Chat（手動）

1. Issueを作成
2. GitHub.comでIssueを開く
3. Copilot Chatで`@copilot`とメンション
4. レビュー依頼を送信

**メリット**: シンプル、PR不要
**デメリット**: コード差分が見えない、手動操作が必要

### パターンB: PR + Comment（推奨・自動化可能）

1. PRを作成（CLIで自動化可能）
2. PRに`@copilot`メンション付きコメントを追加（CLIで自動化可能）
3. Copilot Agentがレビュー開始

**メリット**: コード差分が明確、自動化可能、レビュー履歴が残る
**デメリット**: PRを作成する必要がある

---

## 💡 実践例（hadayalab-automation-platform用）

### Issue #1へのレビュー依頼

```bash
# 1. レビューブランチを作成
git checkout -b copilot-review-issue-1

# 2. 変更があればコミット（例: ドキュメント追加）
git add docs/
git commit -m "docs: Add n8n workflow documentation"

# 3. プッシュ
git push -u origin copilot-review-issue-1

# 4. PRを作成
gh pr create \
  --title "docs: Add n8n workflow documentation - Copilot review" \
  --body "## Review Request

This PR adds n8n workflow documentation for Copilot Agent review.

### Related
- Related to Issue #1

### Files to Review
- n8n-workflows-design.md
- workflow-1-trial-onboarding.json
- README-n8n-implementation.md" \
  --base main \
  --head copilot-review-issue-1

# 5. PR番号を確認（例: PR #2が作成されたと仮定）
PR_NUMBER=2

# 6. レビュー依頼コメントを追加
gh pr comment $PR_NUMBER --body "@copilot Please review this PR and provide feedback on:

## Files to Review
- n8n-workflows-design.md
- workflow-1-trial-onboarding.json
- README-n8n-implementation.md

## Review Focus
1. Wait Node implementation (6-hour, 12-hour waits)
2. Switch Node efficiency (6-market branching)
3. Expression correctness
4. Error handling
5. Security settings

## Specific Questions
- Wait Nodeの長時間待機の実装方法は適切ですか？
- Switch Nodeの分岐処理は効率的ですか？
- 式（expressions）に問題はありませんか？

Please provide improvement suggestions and specific fixes.

Thank you! 🙏"
```

---

## 📚 関連ドキュメント

- [Copilot Agent ワークフロー](./COPILOT_AGENT_WORKFLOW.md) - 全体的なワークフロー説明
- [cryptosignal-ai: Copilot Review Guide](../cryptosignal-ai/docs/GITHUB_COPILOT_REVIEW_GUIDE.md) - 実装例

---

**最終更新**: 2025年12月23日



















