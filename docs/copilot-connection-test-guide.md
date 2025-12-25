# GitHub Copilot Agents/Copilot 接続テストガイド

**最終更新**: 2025-01-24
**バージョン**: 1.0.0

---

## 🎯 テスト目的

**ユーザー → AI（私、司令塔） → GitHub Copilot Agents/Copilot** の基本接続を検証します。

---

## 🔄 テストフロー

```
1. ユーザーがCursor Chatで指示
   ↓
2. AI（私、司令塔）がGitHub APIでIssueを作成
   - @copilotメンション付きコメントを自動追加
   ↓
3. GitHub Copilot Agents/Copilotが応答
   - Issueに@copilotメンションがあると自動起動
   - 応答をコメントとして追加
   ↓
4. AI（私）が応答を検証
   - 応答の品質を確認
   - ユーザーに結果を報告
```

---

## 🚀 手動テスト手順

### ステップ1: GitHub.comでIssueを作成

1. **GitHub.comにアクセス**
   - https://github.com/hadayalab-web/hadayalab-automation-platform/issues

2. **「New issue」をクリック**

3. **以下の内容でIssueを作成**:

   **タイトル**:
   ```
   [接続テスト] AI -> GitHub Copilot Agents
   ```

   **本文**:
   ```markdown
   ## 接続テスト

   このIssueは、**ユーザー → AI（私、司令塔） → GitHub Copilot Agents/Copilot** の基本接続を検証するためのテストです。

   ### テスト内容

   @copilot こんにちは！接続テストです。以下の質問に答えてください：

   1. このメッセージを受信できましたか？
   2. あなたはGitHub Copilot AgentsまたはGitHub Copilotですか？
   3. 現在の日時を教えてください。

   ### 期待される動作

   1. ✅ Issueが作成される
   2. ✅ @copilotメンションが認識される
   3. ✅ GitHub Copilot Agents/Copilotが応答する
   4. ✅ AI（私）が応答を検証する
   5. ✅ ユーザーに結果を報告する
   ```

4. **「Submit new issue」をクリック**

### ステップ2: GitHub Copilot Agents/Copilotの応答を確認

1. **作成したIssueを開く**

2. **GitHub Copilot Chatを開く**
   - サイドバーのCopilotアイコンをクリック
   - または、コメント欄で`@`キーを押す

3. **応答を待つ**
   - GitHub Copilot Agents/Copilotが自動的に応答する可能性があります
   - 数分待ってからコメント欄を確認

### ステップ3: AI（私）が応答を検証

**Cursor Chatで以下を実行**:
```
GitHub Copilot Agents/Copilotの応答を確認して。Issue番号は[作成したIssue番号]です。
```

**AI（私）の動作**:
1. GitHub APIでIssueのコメントを取得
2. Copilotの応答を検証
3. 結果をユーザーに報告

---

## 📊 期待される結果

### 成功パターン

- ✅ Issueが作成される
- ✅ @copilotメンションが認識される
- ✅ GitHub Copilot Agents/Copilotが応答する
- ✅ AI（私）が応答を検証する
- ✅ ユーザーに結果を報告する

### 失敗パターン

- ❌ Issueが作成されない → GitHub Personal Access Tokenが必要
- ❌ @copilotメンションが認識されない → メンション形式を確認
- ❌ GitHub Copilot Agents/Copilotが応答しない → 手動でCopilot Chatを開く必要がある可能性

---

## 🔧 トラブルシューティング

### 問題1: GitHub Personal Access Tokenがない

**解決方法**:
1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 「Generate new token (classic)」をクリック
3. スコープを選択: `repo`, `issues`, `pull_requests`
4. トークンを生成
5. Infisicalに保存: `GITHUB_PERSONAL_ACCESS_TOKEN`

### 問題2: GitHub Copilot Agents/Copilotが応答しない

**解決方法**:
1. Issueを開く
2. GitHub Copilot Chatを手動で開く
3. コメント欄で`@copilot`と入力
4. 質問を送信

### 問題3: AI（私）が応答を検証できない

**解決方法**:
1. GitHub Personal Access Tokenが正しく設定されているか確認
2. Issue番号が正しいか確認
3. コメントが存在するか確認

---

## 📝 次のステップ

接続テストが成功したら：

1. **n8nワークフロー実行テスト**
   - GitHub Copilot Agents/Copilot → GitHub Actions → n8nワークフロー

2. **完全自動化テスト**
   - ユーザー → AI（私） → GitHub Copilot Agents/Copilot → Actions → n8nワークフロー → 結果報告

---

**このガイドは、GitHub Copilot Agents/Copilot接続テストに関する唯一の信頼できる情報源（SSOT）です。**





