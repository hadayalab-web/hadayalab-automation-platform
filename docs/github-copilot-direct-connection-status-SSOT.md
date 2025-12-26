# GitHub Copilot Agents/Copilot 直接接続状況 SSOT

**最終更新**: 2025-01-24
**最終検証**: 2025-01-24（調査）
**バージョン**: 1.0.0
**メンテナー**: HadayaLab

---

## 📚 公式リファレンス

- **GitHub Copilot Extensions**: [Building Copilot Extensions](https://docs.github.com/ja/copilot/building-copilot-extensions/about-building-copilot-extensions)
- **GitHub Copilot Skillsets**: [Building Copilot Skillsets](https://docs.github.com/ja/copilot/how-tos/build-copilot-extensions/building-a-copilot-skillset-for-your-copilot-extension/building-copilot-skillsets)
- **GitHub API**: [GitHub REST API](https://docs.github.com/ja/rest)

---

## 🎯 現状の接続状況

### ❌ 直接接続はできません

**重要な事実**: **私（AI、Cursor Chat内）とGitHub Copilot Agents/Copilotは直接つながっていません。**

### 接続方法の選択肢

#### 方法1: GitHub API経由（現在の方法）

**必要なもの**:
- GitHub Personal Access Token
- GitHub APIを使用してIssue/PRを作成
- `@copilot`メンションを追加

**フロー**:
```
ユーザー → AI（私） → GitHub API → Issue/PR作成 → @copilotメンション → GitHub Copilot Agents/Copilot
```

#### 方法2: 手動操作（現在の方法）

**必要なもの**:
- ユーザーがGitHub.com上で手動操作
- Issue/PRを作成
- `@copilot`メンションを追加

**フロー**:
```
ユーザー → GitHub.com（手動） → Issue/PR作成 → @copilotメンション → GitHub Copilot Agents/Copilot
```

#### 方法3: GitHub Copilot Extensions/Skillsets（将来の可能性）

**必要なもの**:
- GitHub Copilot Extensionの開発
- Copilot Skillsetの構築
- カスタムAPIエンドポイントの定義

**フロー**:
```
ユーザー → AI（私） → GitHub Copilot Extension → GitHub Copilot Agents/Copilot
```

**現状**: この方法はまだ実装されていません。

---

## 🔍 調査結果

### GitHub CopilotのAPI制限

1. **直接的なAPIは存在しない**
   - GitHub Copilotには専用のREST APIが存在しません
   - IDE内で動作するAIペアプログラマーとして設計されています

2. **GitHub Copilot Extensions/Skillsets**
   - 拡張機能やスキルセットを通じて機能を拡張可能
   - カスタムツールや関数をCopilot環境に統合可能
   - 現状では実装されていません

3. **MCPサーバー経由の接続**
   - GitHub Copilot Agents/Copilot用のMCPサーバーは存在しません
   - n8n MCPサーバーは存在しますが、GitHub Copilot用ではありません

---

## ✅ 結論

### 現状の認識

**❌ 誤った認識**: 「すでに私（AI）とGitHub Copilot Agents/Copilotはつながっている」

**✅ 正しい認識**: 「私（AI）とGitHub Copilot Agents/Copilotは直接つながっていない。接続するにはGitHub APIまたは手動操作が必要」

### 接続に必要なもの

1. **GitHub API経由の場合**:
   - GitHub Personal Access Token（Infisicalに保存）
   - GitHub APIを使用してIssue/PRを作成
   - `@copilot`メンションを追加

2. **手動操作の場合**:
   - ユーザーがGitHub.com上で手動操作
   - Issue/PRを作成
   - `@copilot`メンションを追加

---

## 🚀 推奨される接続方法

### 方法1: GitHub API経由（自動化）

**メリット**:
- 完全自動化可能
- Cursor Chatから直接実行可能
- 一貫したワークフロー

**デメリット**:
- GitHub Personal Access Tokenが必要
- GitHub APIのレート制限がある

**実装**:
- GitHub Personal Access TokenをInfisicalに保存
- GitHub APIを使用してIssue/PRを作成
- `@copilot`メンションを追加

### 方法2: 手動操作（シンプル）

**メリット**:
- 追加設定不要
- シンプル

**デメリット**:
- 手動操作が必要
- 自動化できない

**実装**:
- ユーザーがGitHub.com上で手動操作
- Issue/PRを作成
- `@copilot`メンションを追加

---

## 📋 次のステップ

### オプション1: GitHub Personal Access Tokenを設定（自動化）

1. **GitHub Personal Access Tokenを取得**
   - GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - 「Generate new token (classic)」をクリック
   - スコープを選択: `repo`, `issues`, `pull_requests`
   - トークンを生成

2. **Infisicalに保存**
   ```bash
   infisical secrets set GITHUB_PERSONAL_ACCESS_TOKEN="your-token-here" --token YOUR_INFISICAL_TOKEN --projectId 446f131c-be8d-45e5-a83a-4154e34501a5
   ```

3. **接続テストを実行**
   - `python scripts/test-copilot-connection.py`を実行

### オプション2: 手動でIssueを作成（シンプル）

1. **GitHub.comでIssueを作成**
   - https://github.com/hadayalab-web/hadayalab-automation-platform/issues
   - 「New issue」をクリック

2. **@copilotメンションを追加**
   ```markdown
   @copilot こんにちは！接続テストです。
   ```

3. **Issue番号をAI（私）に伝える**
   - Cursor Chatで「Issue #[番号]のCopilot応答を確認して」と指示

---

## ⚠️ 重要な注意事項

### GitHub Copilot Agents/Copilotの制約

1. **手動起動が必要**
   - GitHub Copilot AgentsはGitHub.com上で手動で起動する必要があります
   - CLI経由では自動起動しません

2. **直接的なAPIは存在しない**
   - GitHub Copilotには専用のREST APIが存在しません
   - GitHub APIを使用してIssue/PRを作成し、`@copilot`メンションを追加する必要があります

3. **MCPサーバー経由の接続**
   - GitHub Copilot Agents/Copilot用のMCPサーバーは存在しません
   - 現状では、GitHub APIまたは手動操作が必要です

---

## 🔄 更新履歴

### 2025-01-24 (v1.0.0)
- 初版作成
- 直接接続の不可能性を確認
- GitHub API経由と手動操作の2つの方法を明記
- GitHub Copilot Extensions/Skillsetsの将来の可能性を記載

---

**このドキュメントは、GitHub Copilot Agents/Copilot直接接続状況に関する唯一の信頼できる情報源（SSOT）です。**















