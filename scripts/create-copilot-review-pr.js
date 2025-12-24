#!/usr/bin/env node
// scripts/create-copilot-review-pr.js
// GitHub Copilot Agentレビュー用のPRを作成し、レビュー依頼コメントを追加

const { execSync } = require('child_process');

/**
 * Copilot Agentレビュー用のPR作成
 *
 * 使用方法:
 *   node scripts/create-copilot-review-pr.js [issue-number]
 */
async function createCopilotReviewPR(issueNumber = 1) {
  try {
    console.log(`🚀 Creating Pull Request for Copilot Agent review (Issue #${issueNumber})...\n`);

    // 現在のブランチを確認
    const currentBranch = execSync('git branch --show-current', { encoding: 'utf-8' }).trim();
    console.log(`📌 Current branch: ${currentBranch}`);

    // レビューブランチを作成
    const reviewBranch = `copilot-review-issue-${issueNumber}`;
    console.log(`\n🔀 Creating review branch: ${reviewBranch}`);

    try {
      execSync(`git checkout -b ${reviewBranch}`, { stdio: 'inherit' });
    } catch (error) {
      // ブランチが既に存在する場合
      console.log(`Branch ${reviewBranch} already exists, switching to it...`);
      execSync(`git checkout ${reviewBranch}`, { stdio: 'inherit' });
    }

    // 空のコミットを作成（PRを作成するため）
    try {
      execSync('git commit --allow-empty -m "chore: Trigger Copilot Agent review"', { stdio: 'inherit' });
    } catch (error) {
      console.log('No changes to commit or already committed');
    }

    // ブランチをプッシュ
    console.log(`\n📤 Pushing branch ${reviewBranch}...`);
    execSync(`git push -u origin ${reviewBranch}`, { stdio: 'inherit' });

    // PR作成用のbodyを作成
    const prBody = `## Copilot Agent Review Request

This PR is created for GitHub Copilot Agent code review.

### Related Issue
Closes #${issueNumber}

### Review Request for @copilot

Please review the following changes:

### Key Files to Review

- \`n8n-workflows-design.md\`
- \`workflow-1-trial-onboarding.json\`
- \`README-n8n-implementation.md\`

### Review Focus Areas

1. **Wait Node Implementation**: Are 6-hour and 12-hour waits appropriate?
2. **Switch Node Efficiency**: Is the 6-market branching efficient?
3. **Expressions**: Are expressions correctly written?
4. **Error Handling**: Is error handling sufficient?
5. **Security Settings**: Are security settings appropriate?

### Related Documentation

- Review request details: Issue #${issueNumber}

---

**Note**: This PR is specifically created for Copilot Agent review. Please review the code changes and provide feedback.

Thank you! 🙏`;

    // PRを作成
    console.log(`\n📝 Creating Pull Request...`);
    const prOutput = execSync(
      `gh pr create --title "Copilot Agent Review: Issue #${issueNumber} - n8n Workflow Documentation" --body "${prBody.replace(/"/g, '\\"')}" --base main --head ${reviewBranch}`,
      { encoding: 'utf-8' }
    );

    // PR URLを抽出
    const prUrlMatch = prOutput.match(/https:\/\/github\.com\/[^\s]+/);
    const prUrl = prUrlMatch ? prUrlMatch[0] : prOutput.trim();

    // PR番号を抽出
    const prNumberMatch = prUrl.match(/\/pull\/(\d+)/);
    const prNumber = prNumberMatch ? prNumberMatch[1] : null;

    console.log(`\n✅ Pull Request created successfully!`);
    console.log(`🔗 PR URL: ${prUrl}\n`);

    if (prNumber) {
      // PRにCopilot Agentをアサイン（可能な場合）
      const reviewComment = `@copilot Please review this PR and provide feedback on:

## Files to Review

- \`n8n-workflows-design.md\`
- \`workflow-1-trial-onboarding.json\`
- \`README-n8n-implementation.md\`

## Review Focus Areas

1. **Wait Node Implementation**: Are 6-hour and 12-hour waits appropriate?
   - Wait Nodeの長時間待機（6時間、12時間）の実装方法は適切ですか？

2. **Switch Node Efficiency**: Is the 6-market branching efficient?
   - Switch Nodeの6市場分岐は効率的ですか？

3. **Expressions**: Are expressions correctly written?
   - 式（expressions）に問題はありませんか？

4. **Error Handling**: Is error handling sufficient?
   - エラーハンドリングは十分ですか？

5. **Security Settings**: Are security settings appropriate?
   - セキュリティ上の懸念はありませんか？

## Specific Questions

- Wait Nodeの実装方法は適切ですか？
- Switch Nodeの分岐処理は効率的ですか？
- 式（expressions）の記述が正しいか確認してください
- エラーハンドリングが適切か確認してください
- セキュリティ設定が適切か確認してください

Please provide:
- Code quality feedback
- Improvement suggestions
- Specific fixes

Thank you! 🙏`;

      try {
        execSync(`gh pr comment ${prNumber} --body "${reviewComment.replace(/"/g, '\\"')}"`, { stdio: 'inherit' });
        console.log('✅ Added Copilot review comment to PR\n');
      } catch (error) {
        console.log('⚠️ Could not add Copilot comment (this is optional)\n');
      }

      console.log('📌 Next steps:');
      console.log(`   1. Check PR: ${prUrl}`);
      console.log('   2. Copilot Agent should automatically review the PR');
      console.log('   3. Monitor PR comments for review feedback\n');
    } else {
      console.log('⚠️ Could not extract PR number. Please add review comment manually.\n');
    }

    // 元のブランチに戻る
    console.log(`\n🔄 Switching back to ${currentBranch}...`);
    execSync(`git checkout ${currentBranch}`, { stdio: 'inherit' });

    return prUrl;
  } catch (error) {
    console.error('❌ Error creating PR:', error.message);
    process.exit(1);
  }
}

// メイン実行
const issueNumber = process.argv[2] ? parseInt(process.argv[2], 10) : 1;
createCopilotReviewPR(issueNumber);

module.exports = { createCopilotReviewPR };


