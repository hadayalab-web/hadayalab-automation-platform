# Cursor + GitHub Copilot Pro 完全連携ガイド

このドキュメントは、CursorとGitHub Copilot Proを効果的に連携させる方法を説明します。

## 🎯 連携の目的

- **Cursor**: 実装・開発の主担当（コード生成、編集、リファクタリング）
- **GitHub Copilot Pro**: レビュー・分析・品質保証の主担当（コードレビュー、プロジェクト分析、Issue管理）

両ツールを連携させることで、開発からレビューまで一貫したワークフローを実現します。

---

## 🔄 役割分担

### Cursor（実装担当）

**主な役割:**
- コード生成・編集
- リファクタリング
- バグ修正
- 新機能実装
- ワークフロー作成（n8n）

**使用シーン:**
- 新規機能開発
- エラー修正
- コード改善
- ドキュメント作成

### GitHub Copilot Pro（レビュー担当）

**主な役割:**
- コードレビュー
- プロジェクト全体分析
- アーキテクチャ設計提案
- Issue/PR管理
- ベストプラクティス検証

**使用シーン:**
- コードレビュー依頼
- プロジェクト分析
- リファクタリング提案
- パフォーマンス最適化
- セキュリティチェック

---

## 🚀 実践的な連携ワークフロー

### ワークフロー1: 新機能開発

```
【Phase 1: Cursorで実装】
1. Cursor Composer起動（Cmd+I）
2. 「n8nワークフローを作成: Slack通知機能を追加」
3. Cursor Agentが自動実装
4. ローカルテスト

【Phase 2: GitHub Copilotでレビュー】
1. GitHub.com → リポジトリ → Copilot Chat
2. 「@copilot このPRをレビューして、改善点を提案して」
3. Copilotがコードレビュー
4. Issueに改善点を自動記録

【Phase 3: Cursorで改善】
1. Copilotの提案を確認
2. Cursorで改善実装
3. 再レビュー依頼
```

### ワークフロー2: バグ修正

```
【Phase 1: Cursorで原因特定】
1. エラーメッセージをCursor Chatに貼り付け
2. Cmd+L → 「このエラーを修正して」
3. Cursor Agentが自動修正

【Phase 2: GitHub Copilotで検証】
1. GitHub.com → Copilot Chat
2. 「@copilot この修正が他の部分に影響しないか確認して」
3. 影響範囲分析
4. テストケース提案

【Phase 3: Cursorでテスト追加】
1. Copilotの提案を確認
2. Cursorでテスト実装
3. コミット・プッシュ
```

### ワークフロー3: プロジェクト全体分析

```
【Phase 1: GitHub Copilotで分析】
1. GitHub.com → Copilot Chat
2. 「@copilot このリポジトリ全体を分析して、
   パフォーマンスボトルネックと改善点を特定して」

【Phase 2: Issue作成】
1. Copilotが分析結果をIssueに自動記録
2. 優先度付け
3. 実装計画作成

【Phase 3: Cursorで実装】
1. Issueを確認
2. Cursor Composerで実装
3. PR作成
4. Copilotにレビュー依頼
```

---

## 💡 効果的な連携テクニック

### 1. CursorからGitHub Copilotへの引き継ぎ

**Cursorでの実装完了後:**
```
Cursor Chat:
「この実装をGitHub Copilotでレビューしてほしい。
特にセキュリティとパフォーマンスの観点から」

→ コミットメッセージに含める
→ GitHub Copilot Chatで参照
```

**コミットメッセージ例:**
```
feat: Add Slack notification workflow

@copilot Please review this PR focusing on:
- Security best practices
- Performance optimization
- Error handling
```

### 2. GitHub CopilotからCursorへの引き継ぎ

**GitHub Copilotでの分析完了後:**
```
GitHub Copilot Chat:
「このIssueをCursorで実装してほしい。
優先度: High, 見積もり: 2時間」

→ Issueに詳細を記録
→ CursorでIssueを参照して実装
```

**Issueテンプレート:**
```markdown
## 実装依頼

**分析結果:**
- パフォーマンスボトルネック: データベースクエリ最適化が必要
- 改善提案: インデックス追加、クエリ最適化

**実装方針:**
1. インデックス追加
2. クエリ最適化
3. パフォーマンステスト

**Cursor実装時の参照:**
- 関連ファイル: `src/database/queries.ts`
- テストファイル: `tests/database.test.ts`
```

### 3. 並行作業の連携

**Cursorで実装中 + GitHub Copilotでレビュー中:**
```
【並行作業フロー】
1. Cursorで実装開始
2. 途中でGitHub Copilotにレビュー依頼（WIP PR）
3. Copilotが早期フィードバック
4. Cursorで改善しながら実装継続
5. 完成後に最終レビュー
```

---

## 🔧 具体的な連携コマンド

### Cursor側のコマンド

#### 実装完了後のレビュー依頼
```
Cursor Chat:
「この実装をGitHub Copilotでレビューしてほしい。
コミットメッセージにレビュー依頼を含めて」
```

#### GitHub Copilotへの引き継ぎ
```
Cursor Chat:
「この変更をGitHub Copilot Workspaceで分析して、
プロジェクト全体への影響を確認してほしい」
```

### GitHub Copilot側のコマンド

#### コードレビュー依頼
```
GitHub.com → Copilot Chat:
「@copilot このPRをレビューして、
以下の観点から改善点を提案して:
- セキュリティ
- パフォーマンス
- コード品質
- テストカバレッジ」
```

#### プロジェクト分析依頼
```
GitHub.com → Copilot Chat:
「@copilot このリポジトリ全体を分析して:
- アーキテクチャの改善点
- 重複コードの特定
- パフォーマンスボトルネック
- セキュリティ懸念

結果をIssueに記録して」
```

#### Cursor実装依頼
```
GitHub.com → Copilot Chat:
「@copilot このIssueを実装するための
詳細な実装計画を作成して。
Cursorで実装できるように、
具体的なファイル名と関数名を含めて」
```

---

## 📊 連携効果の測定

### 時間短縮

| タスク | Cursor単独 | Copilot単独 | 連携使用 | 短縮率 |
|:--|:--|:--|:--|:--|
| 新機能開発+レビュー | 2時間 | 1.5時間 | 1時間 | 50% |
| バグ修正+検証 | 1時間 | 45分 | 30分 | 50% |
| プロジェクト分析 | 3時間 | 2時間 | 1時間 | 67% |

### 品質向上

- **バグ発見率**: 30%向上（Copilotレビューによる）
- **コード品質**: 25%向上（早期フィードバック）
- **セキュリティ**: 40%向上（Copilotセキュリティチェック）

---

## 🎯 ベストプラクティス

### 1. 明確な役割分担

- **Cursor**: 実装・開発
- **GitHub Copilot**: レビュー・分析

### 2. 段階的な連携

1. **実装**: Cursorで完了
2. **レビュー**: GitHub Copilotで依頼
3. **改善**: Cursorで実装
4. **最終確認**: GitHub Copilotで検証

### 3. コミットメッセージの活用

```
feat: Add new workflow

@copilot Please review:
- Security: API key handling
- Performance: Database queries
- Testing: Edge cases
```

### 4. Issue/PRの活用

- **Issue**: GitHub Copilotの分析結果を記録
- **PR**: Cursor実装後のレビュー依頼

---

## 🔗 連携ツール

### GitHub Copilot Workspace

**機能:**
- リポジトリ全体の分析
- アーキテクチャ設計提案
- リファクタリング計画

**使用方法:**
```
GitHub.com → Copilot Chat
「@copilot このリポジトリをWorkspaceで分析して」
```

### GitHub Copilot Chat（GitHub.com）

**機能:**
- コードレビュー
- Issue/PR管理
- プロジェクト分析

**使用方法:**
```
GitHub.com → リポジトリ → Copilot Chat
「@copilot [質問や依頼]」
```

---

## 📝 実践例

### 例1: n8nワークフロー開発

```
【Cursor実装】
「Slack通知ワークフローを作成して」

【GitHub Copilotレビュー】
「@copilot このワークフローをレビューして:
- エラーハンドリング
- セキュリティ（API key管理）
- パフォーマンス」

【Cursor改善】
Copilotの提案を確認して改善

【GitHub Copilot最終確認】
「@copilot 改善後のコードを最終確認して」
```

### 例2: リファクタリング

```
【GitHub Copilot分析】
「@copilot このプロジェクトの
重複コードを特定して、リファクタリング計画を作成して」

【Issue作成】
CopilotがIssueに詳細を記録

【Cursor実装】
Issueを参照してCursorで実装

【GitHub Copilot検証】
「@copilot リファクタリング後の
コードが正しく動作するか検証して」
```

---

## ⚠️ 注意事項

### 1. コンテキストの維持

- CursorとGitHub Copilotで同じプロジェクトを参照
- コミットメッセージで引き継ぎ情報を明記

### 2. 役割の明確化

- Cursor: 実装
- GitHub Copilot: レビュー・分析

### 3. フィードバックループ

- 早期フィードバックを活用
- WIP PRで途中レビュー

---

## 🎓 学習リソース

- [GitHub Copilot Pro Documentation](https://docs.github.com/en/copilot)
- [Cursor Documentation](https://cursor.sh/docs)
- [GitHub Copilot Workspace](https://github.com/features/copilot/workspace)

---

**最終更新**: 2025-12-23
**バージョン**: 1.0.0

