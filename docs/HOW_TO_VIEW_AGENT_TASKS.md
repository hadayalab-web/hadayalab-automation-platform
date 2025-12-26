# GitHub Copilot Agent タスクの確認方法

## 🎯 概要

GitHub Copilot Agentがレビューやタスクを実行した際、そのタスクの詳細とログを確認する方法です。

---

## 📋 基本的な確認方法

### 1. タスクリストを表示

```bash
# 最近のタスクを一覧表示
gh agent-task list --limit 10

# 特定のリポジトリのタスクを表示
gh agent-task list --repo owner/repo --limit 10
```

**出力例**:
```
Reviewing and updating n8n workflow documentation	#3	hadayalab-web/hadayalab-automation-platform	Ready for review	2025-12-23T16:52:39Z
Addressing critical security issues from Copilot review	#8	hadayalab-web/cryptosignal-ai	Ready for review	2025-12-23T16:36:53Z
```

### 2. タスクの詳細を表示

```bash
# タスクIDで詳細を表示
gh agent-task view <TASK_ID>

# ログも含めて表示
gh agent-task view <TASK_ID> --log
```

**タスクIDの取得方法**:
- `gh agent-task list` の出力から取得
- PRページのAgent Sessionsセクションから取得
- GitHub URLから取得（例: `e53ed81a-f26a-4854-acc2-034a3db4e9af`）

### 3. タスクのログを表示

```bash
# 詳細ログを表示（大量の出力になる可能性があります）
gh agent-task view <TASK_ID> --log

# 例
gh agent-task view e53ed81a-f26a-4854-acc2-034a3db4e9af --log
```

---

## 🔍 実際の使用例

### 例1: cryptosignal-aiプロジェクトのPR #8のレビュー結果を確認

```bash
# タスクIDを取得
gh agent-task list --repo hadayalab-web/cryptosignal-ai --limit 5

# タスクの詳細を表示
gh agent-task view e53ed81a-f26a-4854-acc2-034a3db4e9af

# ログを確認
gh agent-task view e53ed81a-f26a-4854-acc2-034a3db4e9af --log
```

**出力例**:
```
Ready for review • Addressing critical security issues from Copilot review
Started on behalf of hadayalab-web about 27 minutes ago
Used 1 premium request(s) • Duration 8m37s

hadayalab-web/cryptosignal-ai#8 • fix: resolve undefined variable and complete error tracking in deepMetrics

For detailed session logs, try:
gh agent-task view 'e53ed81a-f26a-4854-acc2-034a3db4e9af' --log

View this session on GitHub:
https://github.com/hadayalab-web/cryptosignal-ai/pull/8/agent-sessions/e53ed81a-f26a-4854-acc2-034a3db4e9af
```

### 例2: hadayalab-automation-platformプロジェクトのタスクを確認

```bash
# タスクリストを表示
gh agent-task list --repo hadayalab-web/hadayalab-automation-platform --limit 5

# 特定のタスクを確認（タスクIDがわかっている場合）
gh agent-task view <TASK_ID>
```

---

## 📊 タスクの状態

Copilot Agentタスクには以下の状態があります：

- **Ready for review**: レビュー準備完了
- **In progress**: 作業中
- **Completed**: 完了
- **Failed**: 失敗
- **Cancelled**: キャンセル

---

## 🔗 関連コマンド

### PR経由でタスクを確認

```bash
# PRの詳細を表示（Agent Sessionsのリンクが含まれる場合がある）
gh pr view <PR_NUMBER> --repo owner/repo

# PRをWebブラウザで開く（Agent Sessionsセクションを確認）
gh pr view <PR_NUMBER> --repo owner/repo --web
```

### GitHub.comで確認

1. PRページを開く
2. 「Agent Sessions」セクションを探す
3. セッションをクリックして詳細を確認

---

## 💡 ヒント

### タスクIDの見つけ方

1. **`gh agent-task list`の出力から**
   - タスクIDは通常、UUID形式（例: `e53ed81a-f26a-4854-acc2-034a3db4e9af`）

2. **GitHub URLから**
   - PRページのAgent SessionsセクションのURLに含まれる
   - 例: `https://github.com/owner/repo/pull/8/agent-sessions/e53ed81a-f26a-4854-acc2-034a3db4e9af`

3. **PRのコメントから**
   - Copilot AgentのコメントにタスクIDやリンクが含まれる場合がある

### ログの見方

`--log`オプションを使用すると、大量の出力が表示されることがあります。以下を確認：

- **開始時間と終了時間**: タスクの実行時間
- **実行されたコマンド**: Copilot Agentが実行したコマンド
- **変更内容**: コードの変更や修正
- **レビュー結果**: コードレビューの結果とフィードバック
- **エラーや警告**: 問題があった場合のエラーメッセージ

---

## 📝 実際のレビュー結果の例

### cryptosignal-ai PR #8のレビュー結果

Copilot Agentは以下のことを実施しました：

1. **バグ修正**
   - `binanceData`変数の未定義バグを発見して修正
   - `binanceDataForTrap`に修正

2. **エラートラッキングの改善**
   - `console.warn`を`ErrorTracker.trackError`に置き換え
   - エラーハンドリングの一貫性を向上

3. **4つのCRITICAL修正の確認**
   - ✅ セキュリティ: Debug Bypass修正
   - ✅ 入力検証の追加
   - ✅ エラートラッキングの実装
   - ✅ 機能フラグシステムの実装

4. **セキュリティスキャン**
   - CodeQLスキャンを実行
   - 0件の脆弱性を確認

---

## 🔄 ワークフロー

### レビュー依頼から結果確認まで

1. **PRを作成してレビュー依頼**
   ```bash
   gh pr create --title "..." --body "@copilot Please review..."
   ```

2. **タスクリストで確認**
   ```bash
   gh agent-task list --limit 10
   ```

3. **タスクの詳細を確認**
   ```bash
   gh agent-task view <TASK_ID>
   ```

4. **ログを確認（必要に応じて）**
   ```bash
   gh agent-task view <TASK_ID> --log
   ```

5. **PRを確認**
   ```bash
   gh pr view <PR_NUMBER> --web
   ```

---

## 📚 関連ドキュメント

- [Copilot Agent レビュー依頼方法](./HOW_TO_REQUEST_COPILOT_REVIEW.md)
- [Copilot Agent ワークフロー](./COPILOT_AGENT_WORKFLOW.md)
- [GitHub CLI ドキュメント](https://cli.github.com/manual/)

---

**最終更新**: 2025年12月23日



















