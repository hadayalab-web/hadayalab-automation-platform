#!/usr/bin/env node
// scripts/prepare-copilot-review.js
// GitHub Copilot Agentレビュー依頼テンプレートを生成

/**
 * GitHub Copilot Agentレビュー依頼テンプレート生成スクリプト
 *
 * 使用方法:
 *   node scripts/prepare-copilot-review.js
 *   node scripts/prepare-copilot-review.js --issue 1
 *   node scripts/prepare-copilot-review.js --files "file1.md,file2.json"
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// デフォルトのレビュー依頼テンプレート
const DEFAULT_TEMPLATE = {
  files: [
    'n8n-workflows-design.md',
    'workflow-1-trial-onboarding.json',
    'README-n8n-implementation.md',
  ],
  focusAreas: [
    'Wait Nodeの長時間待機（6時間、12時間）の実装方法',
    'Switch Nodeの6市場分岐の効率性',
    '式（expressions）の記述が正しいか',
    'エラーハンドリングが適切か',
    'セキュリティ設定が適切か',
  ],
  questions: [
    'Wait Nodeの実装方法は適切ですか？',
    'Switch Nodeの分岐処理は効率的ですか？',
    '式（expressions）に問題はありませんか？',
    'エラーハンドリングは十分ですか？',
    'セキュリティ上の懸念はありませんか？',
  ],
};

/**
 * レビュー依頼テンプレートを生成
 */
function generateReviewTemplate(config) {
  const { files, focusAreas, questions, issueNumber } = config;

  let template = '@copilot ';

  if (issueNumber) {
    template += `Issue #${issueNumber}のレビュー依頼内容を確認して、以下のファイルをレビューしてください:\n\n`;
  } else {
    template += '以下のファイルをレビューしてください:\n\n';
  }

  // ファイル一覧
  template += '## Files to Review\n';
  files.forEach((file, index) => {
    template += `${index + 1}. ${file}\n`;
  });

  // レビューフォーカス
  template += '\n## Review Focus\n';
  focusAreas.forEach(area => {
    template += `- ${area}\n`;
  });

  // 具体的な質問
  if (questions && questions.length > 0) {
    template += '\n## Specific Questions\n';
    questions.forEach((question, index) => {
      template += `${index + 1}. ${question}\n`;
    });
  }

  template += '\n改善提案と具体的な修正方法を教えてください。\n\n';
  template += 'Thank you! 🙏';

  return template;
}

/**
 * メイン処理
 */
function main() {
  const args = process.argv.slice(2);

  // コマンドライン引数の解析
  let issueNumber = null;
  let customFiles = null;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--issue' && args[i + 1]) {
      issueNumber = args[i + 1];
    } else if (args[i] === '--files' && args[i + 1]) {
      customFiles = args[i + 1].split(',').map(f => f.trim());
    }
  }

  // 設定を準備
  const config = {
    files: customFiles || DEFAULT_TEMPLATE.files,
    focusAreas: DEFAULT_TEMPLATE.focusAreas,
    questions: DEFAULT_TEMPLATE.questions,
    issueNumber,
  };

  // テンプレートを生成
  const template = generateReviewTemplate(config);

  // 出力
  console.log('\n' + '='.repeat(60));
  console.log('📋 GitHub Copilot Agent レビュー依頼テンプレート');
  console.log('='.repeat(60) + '\n');
  console.log(template);
  console.log('\n' + '='.repeat(60));
  console.log('📌 Next Steps:');
  console.log('='.repeat(60));
  console.log('1. 上記のテンプレートをコピーしてください');

  if (issueNumber) {
    console.log(`2. Issue #${issueNumber}を開いてください`);
    console.log(`   https://github.com/hadayalab-web/hadayalab-automation-platform/issues/${issueNumber}`);
  } else {
    console.log('2. レビューを依頼するIssueまたはPRを開いてください');
  }

  console.log('3. GitHub Copilot Chatを開いてください');
  console.log('   - サイドバーのCopilotアイコンをクリック');
  console.log('   - または、コメント欄で @copilot と入力');
  console.log('4. テンプレートを貼り付けてEnterキーで送信');
  console.log('='.repeat(60) + '\n');

  // クリップボードにコピー（オプション）
  try {
    if (process.platform === 'win32') {
      execSync(`echo ${JSON.stringify(template)} | clip`, { stdio: 'ignore' });
      console.log('✅ テンプレートをクリップボードにコピーしました\n');
    } else if (process.platform === 'darwin') {
      execSync(`echo ${JSON.stringify(template)} | pbcopy`, { stdio: 'ignore' });
      console.log('✅ テンプレートをクリップボードにコピーしました\n');
    } else if (process.platform === 'linux') {
      execSync(`echo ${JSON.stringify(template)} | xclip -selection clipboard`, { stdio: 'ignore' });
      console.log('✅ テンプレートをクリップボードにコピーしました\n');
    }
  } catch (error) {
    // クリップボードコピーに失敗しても続行
  }
}

if (require.main === module) {
  main();
}

module.exports = { generateReviewTemplate };











