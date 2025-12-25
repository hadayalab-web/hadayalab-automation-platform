# GitHub Copilot設定 - 接続テスト用

**最終更新**: 2025-01-24
**バージョン**: 1.0.0

---

## 🎯 接続テストに必要な設定

**ユーザー → AI（私、司令塔） → GitHub Copilot Agents/Copilot** の接続テストを実行するために、以下の設定を確認・有効化してください。

---

## ✅ 必須設定（既に有効化されている可能性が高い）

### 1. Copilot coding agent
- **設定場所**: Settings → Copilot → Features → Copilot coding agent
- **状態**: **Enabled** であることを確認
- **説明**: GitHub Copilot Agentsが動作するために必要
- **確認方法**: 画像の設定画面で「Copilot coding agent」が「Enabled」になっているか確認

### 2. Copilot Chat in GitHub.com
- **設定場所**: Settings → Copilot → Features → Copilot Chat in GitHub.com
- **状態**: **Enabled** であることを確認
- **説明**: GitHub.com上でCopilot Chatを使用するために必要
- **確認方法**: 画像の設定画面で「Copilot Chat in GitHub.com」が「Enabled」になっているか確認

### 3. MCP servers in Copilot
- **設定場所**: Settings → Copilot → Features → MCP servers in Copilot
- **状態**: **Enabled** であることを確認
- **説明**: MCPサーバーとの連携に必要（n8n MCPなど）
- **確認方法**: 画像の設定画面で「MCP servers in Copilot」が「Enabled」になっているか確認

---

## 🔧 推奨設定（接続テストの品質向上のため）

### 4. Copilot code review
- **設定場所**: Settings → Copilot → Features → Copilot code review
- **状態**: **Enabled** であることを確認
- **説明**: コードレビュー機能を使用するために必要
- **確認方法**: 画像の設定画面で「Copilot code review」が「Enabled」になっているか確認

### 5. Copilot Chat in the IDE
- **設定場所**: Settings → Copilot → Features → Copilot Chat in the IDE
- **状態**: **Enabled** であることを確認
- **説明**: IDE内でCopilot Chatを使用するために必要
- **確認方法**: 画像の設定画面で「Copilot Chat in the IDE」が「Enabled」になっているか確認

### 6. Copilot can search the web
- **設定場所**: Settings → Copilot → Features → Copilot can search the web
- **状態**: **Enabled** であることを確認
- **説明**: Web検索機能を使用するために必要
- **確認方法**: 画像の設定画面で「Copilot can search the web」が「Enabled」になっているか確認

---

## 📋 設定確認チェックリスト

接続テストを実行する前に、以下の設定を確認してください：

- [ ] **Copilot coding agent**: Enabled
- [ ] **Copilot Chat in GitHub.com**: Enabled
- [ ] **MCP servers in Copilot**: Enabled
- [ ] **Copilot code review**: Enabled（推奨）
- [ ] **Copilot Chat in the IDE**: Enabled（推奨）
- [ ] **Copilot can search the web**: Enabled（推奨）

---

## 🚀 接続テストの実行

設定が確認できたら、以下の手順で接続テストを実行してください：

### ステップ1: Issueを作成

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

## ⚠️ 注意事項

### 設定変更後の再起動

設定を変更した場合、以下のメッセージが表示されます：
> "It can take up to 30 minutes for the changes to take effect. Restart your code editor for the changes to take effect."

**対処方法**:
1. 設定変更後、30分待つ
2. コードエディタ（Cursor）を再起動
3. 接続テストを実行

### Copilot coding agentの動作確認

「Copilot coding agent」が有効化されていても、GitHub.com上で手動で起動する必要がある場合があります。

**確認方法**:
1. Issueを開く
2. サイドバーの「Agents」ボタンを確認
3. Copilot Agentが利用可能か確認

---

## 📊 設定状態の確認方法

### 画像から確認できる設定

画像の説明から、以下の設定が確認できます：

- ✅ **Copilot coding agent**: Enabled
- ✅ **Copilot Chat in GitHub.com**: Enabled
- ✅ **MCP servers in Copilot**: Enabled
- ✅ **Copilot code review**: Enabled
- ✅ **Copilot Chat in the IDE**: Enabled
- ✅ **Copilot can search the web**: Enabled

**結論**: 必要な設定は既に有効化されているようです！

---

## 🔄 次のステップ

設定が確認できたら：

1. **接続テストを実行**
   - Issueを作成して@copilotメンション
   - GitHub Copilot Agents/Copilotの応答を確認

2. **AI（私）が応答を検証**
   - Cursor Chatで応答確認を依頼
   - 結果を報告

3. **n8nワークフロー実行テスト**
   - GitHub Copilot Agents/Copilot → GitHub Actions → n8nワークフロー

---

**このガイドは、GitHub Copilot設定（接続テスト用）に関する唯一の信頼できる情報源（SSOT）です。**





