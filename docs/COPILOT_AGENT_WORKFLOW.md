# GitHub Copilot Agent レビュー依頼ワークフロー

## 📋 現状の制約

**重要**: GitHub Copilot AgentはCLI経由では自動起動しません。GitHub.com上で手動で起動する必要があります。

### なぜCLI経由ではできないか

1. **セキュリティ上の理由**
   - Copilot Agentは認証されたユーザーのコンテキストで動作
   - CLI経由の自動起動は、不正な自動化を防ぐため制限されている

2. **インタラクティブな処理**
   - Copilot Agentは人間との対話を前提として設計
   - 質問や追加情報の要求が発生する可能性がある

3. **リソース管理**
   - Agentは限られたリソースで動作
   - 手動起動により、不要な実行を防ぐ

---

## 🔄 推奨ワークフロー

### パターン1: Issue + Copilot Chat（推奨）

**適用場面**: 継続的なレビュー依頼、複数のファイルレビュー

**手順**:
1. Issueを作成または既存Issueを使用
2. GitHub.comでIssueを開く
3. GitHub Copilot Chatを開く（サイドバーのCopilotアイコン、またはコメント欄で`@copilot`）
4. レビュー依頼コマンドを送信

**メリット**:
- レビュー履歴がIssueに残る
- 複数のレビュー依頼を整理できる
- チーム内で共有しやすい

**デメリット**:
- 手動操作が必要
- 自動化できない

### パターン2: PR + Copilot Chat（cryptosignal-aiで使用）

**適用場面**: コード変更のレビュー

**手順**:
1. PRを作成
2. PRのコメント欄で`@copilot`をメンション
3. レビュー依頼コマンドを送信

**メリット**:
- コード差分が明確
- レビューコメントがコード行にリンク
- マージ前にレビューを実施

**デメリット**:
- PRが必要（小さな変更には不向き）

### パターン3: テンプレート化（効率化）

**適用場面**: 定型的なレビュー依頼

**手順**:
1. レビュー依頼テンプレートを作成
2. IssueまたはPRコメント欄で`@copilot`を呼び出し
3. テンプレートを貼り付け

**テンプレート例**:
```markdown
@copilot Please review the following files:

## Files to Review
1. path/to/file1.md
2. path/to/file2.json
3. path/to/file3.js

## Review Focus
- Implementation correctness
- Error handling
- Security considerations
- Performance optimization

## Specific Questions
1. Is the error handling sufficient?
2. Are there any security vulnerabilities?
3. Can performance be improved?

Thank you!
```

---

## 🛠️ 効率化のためのツール

### 1. レビュー依頼テンプレート

プロジェクトごとにレビュー依頼テンプレートを作成：

```markdown
# docs/copilot-review-template.md

@copilot Please review the following:

## Files
<!-- ファイル一覧を記入 -->

## Focus Areas
- [ ] Code quality
- [ ] Error handling
- [ ] Security
- [ ] Performance
- [ ] Documentation

## Specific Questions
<!-- 質問を記入 -->

## Context
<!-- 追加のコンテキスト情報 -->
```

### 2. Issue テンプレート

`.github/ISSUE_TEMPLATE/copilot-review.md`を作成：

```markdown
---
name: Copilot Review Request
about: Request a review from GitHub Copilot Agent
title: '[Review] '
labels: review, copilot
assignees: ''
---

## Review Request

@copilot Please review the following:

### Files to Review
<!-- ファイル一覧 -->

### Review Focus
<!-- レビューしてほしい点 -->

### Specific Questions
<!-- 具体的な質問 -->

### Related
<!-- 関連するIssueやPR -->
```

### 3. スクリプトによる準備（CLIで自動化できる部分）

CLIでできること：
- Issueの作成
- PRの作成
- レビュー依頼コメントの下書き作成

**例: レビュー依頼準備スクリプト**

```javascript
// scripts/prepare-copilot-review.js
const { execSync } = require('child_process');

function prepareReviewRequest(files, focusAreas, questions) {
  const template = `@copilot Please review the following:

## Files to Review
${files.map(f => `1. ${f}`).join('\n')}

## Review Focus
${focusAreas.map(a => `- ${a}`).join('\n')}

## Specific Questions
${questions.map((q, i) => `${i + 1}. ${q}`).join('\n')}

Thank you!`;

  console.log('\n📋 Copy the following and paste it in GitHub Copilot Chat:\n');
  console.log(template);
  console.log('\n📌 Next steps:');
  console.log('1. Open the Issue/PR on GitHub.com');
  console.log('2. Click the Copilot icon or type @copilot in comments');
  console.log('3. Paste the template above');
  console.log('4. Press Enter to send\n');
}

// 使用例
prepareReviewRequest(
  ['n8n-workflows-design.md', 'workflow-1-trial-onboarding.json'],
  ['Wait Node implementation', 'Error handling', 'Security'],
  ['Is the 6-hour wait appropriate?', 'Are there security concerns?']
);
```

---

## 📝 hadayalab-automation-platform での推奨方法

### Issue #1 へのレビュー依頼

**現在の状況**:
- Issue #1が作成済み
- レビュー依頼コメントが追加済み

**次のステップ**:

1. **GitHub.comでIssue #1を開く**
   ```
   https://github.com/hadayalab-web/hadayalab-automation-platform/issues/1
   ```

2. **GitHub Copilot Chatを開く**
   - 方法1: サイドバーのCopilotアイコンをクリック
   - 方法2: コメント欄で`@copilot`と入力
   - 方法3: コメント欄で`@`キーを押してCopilotを選択

3. **レビュー依頼コマンドを送信**
   ```markdown
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

4. **Enterキーで送信**

---

## 🔄 今後の改善提案

### 自動化できる部分

1. **レビュー依頼コメントの自動生成**
   - CLIスクリプトでテンプレートを生成
   - ファイル一覧を自動抽出
   - レビュー依頼コメントを標準出力

2. **Issue/PRの自動作成**
   - CLIでIssue/PRを作成
   - レビュー依頼テンプレートを含める

3. **レビュー依頼のドキュメント化**
   - レビュー依頼履歴を記録
   - レビュー結果を追跡

### 手動操作が必要な部分

1. **Copilot Chatの起動**
   - GitHub.com上で手動実行

2. **レビュー依頼コマンドの送信**
   - コピー&ペースト後、Enterで送信

---

## 💡 ベストプラクティス

### 1. レビュー依頼を明確にする

- 具体的なファイルを指定
- レビューしてほしい点を明確に
- 質問を具体的に

### 2. コンテキストを提供する

- 関連するIssueやPRをリンク
- 変更の目的を説明
- 懸念点を明記

### 3. レビュー結果を記録する

- レビュー結果をIssue/PRに記録
- 改善項目をTODOリストに追加
- 修正内容をドキュメント化

### 4. テンプレートを活用する

- プロジェクトごとにテンプレートを作成
- レビュー依頼を標準化
- 効率を向上

---

## 📚 関連ドキュメント

- [GitHub Copilot Agent ドキュメント](https://docs.github.com/ja/copilot/how-tos/use-copilot-agents)
- [cryptosignal-ai: Copilot Review Workflow](../cryptosignal-ai/docs/GITHUB_COPILOT_REVIEW_GUIDE.md)
- [Issue #1](https://github.com/hadayalab-web/hadayalab-automation-platform/issues/1)

---

## ❓ FAQ

### Q: CLI経由で自動化できないのは不便ではないか？

A: セキュリティとリソース管理のため、手動起動が必須です。ただし、準備作業（Issue作成、コメント生成）は自動化できます。

### Q: 複数のレビュー依頼を効率化する方法は？

A: テンプレートを作成し、レビュー依頼を標準化することで効率化できます。

### Q: レビュー依頼の履歴を管理するには？

A: IssueやPRを使用することで、レビュー履歴が自動的に記録されます。

---

**最終更新**: 2025年12月23日



















