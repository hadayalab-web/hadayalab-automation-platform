# GitHub Copilot Agents AI補助ワークフロー SSOT

**最終更新**: 2025-01-24
**最終検証**: 2025-01-24（設計）
**バージョン**: 2.0.0
**メンテナー**: HadayaLab

---

## 📚 公式リファレンス

- **GitHub Copilot Agents**: [GitHub Copilot Agents Documentation](https://docs.github.com/ja/copilot/responsible-use/copilot-coding-agent)
- **GitHub API**: [GitHub REST API](https://docs.github.com/ja/rest)
- **n8n MCP**: [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)

---

## 🎯 設計方針

**Cursor UIから完全制御できるAI補助システム**

このドキュメントは、Cursor Chatから指示を出すだけで、GitHub Copilot Agentsが自動的に動作し、AI（私）が中間層として検証・追加指示を行う仕組みを設計した**唯一の信頼できる情報源（SSOT）**です。

### 核心理念

**「ユーザー → AI（私） → GitHub Copilot Agents/Copilot → AI（私）検証 → 追加指示/完了報告 → ユーザー」**

すべての操作をCursor UIから実行可能にし、AI（Cursor Chat）がGitHub Copilot Agentsを補助ツールとして活用し、中間層として検証・追加指示を行うようにします。

---

## 🔄 完全自動化ワークフロー

### ワークフロー1: ユーザー → AI → GitHub Copilot Agents → AI検証 → 完了報告

**目的**: ユーザーがCursor Chatで指示を出すと、AI（私）がGitHub Copilot Agentsに指示を出し、結果を検証して、追加指示または完了報告を行う

**実行フロー**:

```
1. ユーザーがCursor Chatで指示
   「このコードをGitHub Copilotでレビューして」
   ↓
2. AI（私）がn8nワークフロー実行（@n8n-cloud経由）
   - 現在のファイル/変更を取得
   - GitHub APIでIssue/PRを作成
   - @copilotメンション付きコメントを自動追加
   - タスクIDを記録
   ↓
3. GitHub Copilot Agents自動起動
   - Issue/PRに@copilotメンションがあると自動起動
   - レビューを開始
   ↓
4. n8nワークフローで監視（AI（私）が制御）
   - Copilotの応答を定期的にチェック（5分間隔）
   - 応答があったら結果を取得
   ↓
5. AI（私）が結果を検証
   - レビュー結果の品質を確認
   - 不足している情報を特定
   - 追加指示が必要か判断
   ↓
6a. 追加指示が必要な場合
    - AI（私）がGitHub APIで追加コメントを送信
    - 「この点について詳しくレビューしてください」など
    - ステップ4に戻る（最大3回まで）
   ↓
6b. 完了した場合
    - AI（私）が結果を整理
    - ユーザーに完了報告
    - レビュー結果をCursor Chatに表示
```

**Cursor Chatコマンド例**:
```
このコードをGitHub Copilotでレビューして。特にセキュリティとパフォーマンスの観点から。
```

**AI（私）の動作**:
1. ファイルを取得
2. n8nワークフローを実行
3. GitHub APIでIssueを作成
4. `@copilot`メンション付きコメントを追加
5. Copilotの応答を監視
6. 結果を検証
7. 必要に応じて追加指示
8. 完了報告をユーザーに表示

### ワークフロー2: ユーザー → AI → GitHub Copilot → AI検証 → 完了報告

**目的**: ユーザーがCursor Chatで指示を出すと、AI（私）がGitHub Copilot Chatに指示を出し、結果を検証して、追加指示または完了報告を行う

**実行フロー**:

```
1. ユーザーがCursor Chatで指示
   「このプロジェクトをGitHub Copilotで分析して」
   ↓
2. AI（私）がn8nワークフロー実行（@n8n-cloud経由）
   - プロジェクトのファイル一覧を取得
   - GitHub APIでIssueを作成
   - @copilotメンション付き分析依頼を自動追加
   ↓
3. GitHub Copilot自動起動
   - Issueに@copilotメンションがあると自動起動
   - プロジェクト分析を開始
   ↓
4. n8nワークフローで監視（AI（私）が制御）
   - Copilotの応答を定期的にチェック
   - 応答があったら結果を取得
   ↓
5. AI（私）が結果を検証
   - 分析結果の完全性を確認
   - 不足している情報を特定
   - 追加指示が必要か判断
   ↓
6a. 追加指示が必要な場合
    - AI（私）がGitHub APIで追加コメントを送信
    - 「この点について詳しく分析してください」など
    - ステップ4に戻る（最大3回まで）
   ↓
6b. 完了した場合
    - AI（私）が結果を整理
    - ユーザーに完了報告
    - 分析結果をCursor Chatに表示
```

---

## 🔧 実装詳細

### n8nワークフロー設計

#### ワークフロー1: AI補助レビュー（検証・追加指示機能付き）

**トリガー**: Webhook（Cursor Chatから実行）

**ワークフロー構造**:

```
1. Webhook Trigger
   - パラメータ: file, focus, questions
   ↓
2. Code Node（ファイル内容取得）
   - 指定されたファイルの内容を取得
   - 変更差分を取得（Git経由）
   ↓
3. GitHub API Node（Issue作成）
   - Title: "AI補助レビュー依頼: {file}"
   - Body: "@copilot このコードをレビューしてください..."
   ↓
4. GitHub API Node（コメント追加）
   - @copilotメンション
   - レビュー依頼内容（ファイル内容、フォーカス項目）
   ↓
5. Wait Node（Copilot応答待機）
   - 5分間待機
   ↓
6. GitHub API Node（コメント取得）
   - Issueのコメントを取得
   - Copilotの応答を確認
   ↓
7. Code Node（AI検証ロジック）
   - レビュー結果の品質を確認
   - 不足している情報を特定
   - 追加指示が必要か判断
   ↓
8. IF Node（追加指示判定）
   - 追加指示が必要 → ステップ9へ
   - 完了 → ステップ11へ
   ↓
9. GitHub API Node（追加コメント送信）
   - 「この点について詳しくレビューしてください」など
   - 再試行カウンターをインクリメント
   ↓
10. IF Node（再試行回数チェック）
    - 3回未満 → ステップ5に戻る
    - 3回以上 → ステップ11へ
   ↓
11. Respond to Webhook Node
    - レビュー結果をCursor Chatに返す
    - AI（私）が結果を整理してユーザーに報告
```

#### ワークフロー2: AI補助プロジェクト分析（検証・追加指示機能付き）

**トリガー**: Webhook（Cursor Chatから実行）

**ワークフロー構造**:

```
1. Webhook Trigger
   - パラメータ: project, focus
   ↓
2. GitHub API Node（ファイル一覧取得）
   - プロジェクトのファイル一覧を取得
   ↓
3. GitHub API Node（Issue作成）
   - Title: "AI補助プロジェクト分析: {project}"
   - Body: "@copilot このプロジェクトを分析してください..."
   ↓
4. GitHub API Node（コメント追加）
   - @copilotメンション
   - 分析依頼内容（ファイル一覧、フォーカス項目）
   ↓
5. Wait Node（Copilot応答待機）
   - 10分間待機
   ↓
6. GitHub API Node（コメント取得）
   - Issueのコメントを取得
   - Copilotの応答を確認
   ↓
7. Code Node（AI検証ロジック）
   - 分析結果の完全性を確認
   - 不足している情報を特定
   - 追加指示が必要か判断
   ↓
8. IF Node（追加指示判定）
   - 追加指示が必要 → ステップ9へ
   - 完了 → ステップ11へ
   ↓
9. GitHub API Node（追加コメント送信）
   - 「この点について詳しく分析してください」など
   - 再試行カウンターをインクリメント
   ↓
10. IF Node（再試行回数チェック）
    - 3回未満 → ステップ5に戻る
    - 3回以上 → ステップ11へ
   ↓
11. Respond to Webhook Node
    - 分析結果をCursor Chatに返す
    - AI（私）が結果を整理してユーザーに報告
```

---

## 📋 Cursor Chatコマンド一覧

### 基本コマンド

| コマンド | 説明 | 使用例 |
|---------|------|--------|
| `このコードをGitHub Copilotでレビューして` | コードレビュー依頼（AI検証・追加指示付き） | `このコードをGitHub Copilotでレビューして。特にセキュリティとパフォーマンスの観点から。` |
| `このプロジェクトをGitHub Copilotで分析して` | プロジェクト分析依頼（AI検証・追加指示付き） | `このプロジェクトをGitHub Copilotで分析して。アーキテクチャの改善点を特定して。` |
| `このPRをGitHub Copilotでレビューして` | PRレビュー依頼（AI検証・追加指示付き） | `このPRをGitHub Copilotでレビューして。コード品質とセキュリティを確認して。` |

### パラメータ

| パラメータ | 説明 | 例 |
|-----------|------|-----|
| `file` | レビュー対象ファイル | `file=src/main.ts` |
| `focus` | レビューフォーカス項目 | `focus=security,performance` |
| `questions` | 具体的な質問 | `questions=エラーハンドリングは適切か？` |
| `project` | 分析対象プロジェクト | `project=hadayalab-automation-platform` |

---

## 🚀 実装手順

### ステップ1: n8nワークフローの作成

1. **Cursor Chatで指示**
   ```
   @n8n-local github-copilot-ai-review-assistantワークフローを作成して
   ```

2. **n8n-mcpパッケージが自動的にワークフローを作成**

3. **ワークフローをn8n Cloudにインポート**

### ステップ2: 環境変数の設定

1. **GitHub Personal Access Tokenを取得**
   - GitHub Settings → Developer settings → Personal access tokens
   - スコープ: `repo`, `issues`, `pull_requests`

2. **n8n Cloudに環境変数を設定**
   - `GITHUB_PERSONAL_ACCESS_TOKEN`: GitHub API認証用

### ステップ3: テスト実行

1. **Cursor Chatでテスト**
   ```
   このコードをGitHub Copilotでレビューして。特にセキュリティとパフォーマンスの観点から。
   ```

2. **AI（私）が自動的に処理**
   - GitHub Copilot Agentsに指示
   - 結果を検証
   - 必要に応じて追加指示
   - 完了報告をCursor Chatに表示

---

## 📊 制御可能な操作一覧

| 操作 | Cursor Chatコマンド | AI検証 | 追加指示 | 完了報告 | 実証状況 |
|------|-------------------|--------|---------|---------|---------|
| **コードレビュー依頼** | `このコードをGitHub Copilotでレビューして` | ✅ | ✅ | ✅ | ✅ 実装可能 |
| **プロジェクト分析依頼** | `このプロジェクトをGitHub Copilotで分析して` | ✅ | ✅ | ✅ | ✅ 実装可能 |
| **PRレビュー依頼** | `このPRをGitHub Copilotでレビューして` | ✅ | ✅ | ✅ | ✅ 実装可能 |
| **レビュー結果検証** | 自動（AI（私）が処理） | ✅ | ✅ | ✅ | ✅ 実装可能 |
| **追加指示送信** | 自動（AI（私）が処理） | ✅ | ✅ | ✅ | ✅ 実装可能 |

---

## 💡 使用例

### 例1: コードレビュー依頼（AI検証・追加指示付き）

**ユーザーがCursor Chatで指示**:
```
このコードをGitHub Copilotでレビューして。特にセキュリティとパフォーマンスの観点から。
```

**AI（私）の動作**:
1. 現在のファイルを取得
2. n8nワークフローを実行
3. GitHub APIでIssueを作成
4. `@copilot`メンション付きコメントを追加
5. Copilotの応答を待機（5分間隔でチェック）
6. **結果を検証**:
   - レビュー結果の品質を確認
   - セキュリティとパフォーマンスの観点が含まれているか確認
   - 不足している情報を特定
7. **追加指示が必要な場合**:
   - 「セキュリティの観点について、より詳しくレビューしてください」
   - GitHub APIで追加コメントを送信
   - ステップ5に戻る（最大3回まで）
8. **完了した場合**:
   - 結果を整理
   - ユーザーに完了報告:
     ```
     ✅ GitHub Copilot Agentsによるレビューが完了しました。

     **レビュー結果**:
     - セキュリティ: 3つの改善点を特定
     - パフォーマンス: 2つの最適化提案

     **Issue URL**: https://github.com/...

     **改善提案**:
     1. API keyの管理方法を改善
     2. データベースクエリの最適化
     ...
     ```

### 例2: プロジェクト分析依頼（AI検証・追加指示付き）

**ユーザーがCursor Chatで指示**:
```
このプロジェクト全体をGitHub Copilotで分析して。アーキテクチャの改善点を特定して。
```

**AI（私）の動作**:
1. プロジェクトのファイル一覧を取得
2. n8nワークフローを実行
3. GitHub APIでIssueを作成
4. `@copilot`メンション付き分析依頼を追加
5. Copilotの応答を待機（10分間隔でチェック）
6. **結果を検証**:
   - 分析結果の完全性を確認
   - アーキテクチャの改善点が含まれているか確認
   - 不足している情報を特定
7. **追加指示が必要な場合**:
   - 「データベース設計について、より詳しく分析してください」
   - GitHub APIで追加コメントを送信
   - ステップ5に戻る（最大3回まで）
8. **完了した場合**:
   - 結果を整理
   - ユーザーに完了報告:
     ```
     ✅ GitHub Copilotによるプロジェクト分析が完了しました。

     **分析結果**:
     - アーキテクチャ: 5つの改善点を特定
     - パフォーマンス: 3つのボトルネックを発見

     **Issue URL**: https://github.com/...

     **改善提案**:
     1. モジュール分割の最適化
     2. データベース設計の改善
     ...
     ```

---

## ⚠️ 制限事項と回避策

### 制限1: エージェントパネルの手動起動

**問題**: GitHub Copilot Agentsは手動で起動する必要がある

**回避策**:
- Issue/PR作成時に`@copilot`をメンションすることで、Copilotが自動的に応答する可能性がある
- コメントにレビュー依頼内容を記載することで、Copilotが自動的に処理を開始する可能性がある

### 制限2: Copilot応答のタイミング

**問題**: Copilotの応答タイミングが予測できない

**回避策**:
- Wait Nodeで一定時間待機（5分間隔）
- 定期的にコメントを取得して応答を確認
- タイムアウトを設定（例: 30分）

### 制限3: AI検証ロジックの精度

**問題**: AI検証ロジックの精度が不十分な場合がある

**回避策**:
- 検証ロジックを段階的に改善
- ユーザーフィードバックを反映
- 検証結果をログに記録

---

## 🔄 更新履歴

### 2025-01-24 (v2.0.0)
- **AI検証・追加指示機能を追加**: AI（私）が中間層として機能し、GitHub Copilot Agents/Copilotの結果を検証し、必要に応じて追加指示を出す機能を追加
- **完了報告機能を追加**: AI（私）が結果を整理してユーザーに完了報告する機能を追加
- **再試行機能を追加**: 追加指示が必要な場合、最大3回まで再試行する機能を追加

### 2025-01-24 (v1.0.0)
- 初版作成
- Cursor UIから完全制御できるAI補助システムを設計
- n8nワークフロー設計を追加
- Cursor Chatコマンド一覧を追加

---

**このドキュメントは、GitHub Copilot Agents AI補助ワークフローに関する唯一の信頼できる情報源（SSOT）です。**
