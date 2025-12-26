# GitHub Copilot 最初のタスク

GitHub Copilotを活用するための最初のタスクガイドです。

## 🎯 今すぐ実行できる最初のタスク

### ステップ1: GitHub.comにアクセス

1. https://github.com/hadayalab-web/hadayalab-automation-platform にアクセス
2. Copilot Chatを開く（サイドバーのCopilotアイコン、または `@` キーを押す）

### ステップ2: プロジェクト全体分析を依頼

Copilot Chatに以下のプロンプトを貼り付けて実行：

```
@copilot このリポジトリ全体を分析して、以下の観点から改善点を特定して:

1. **アーキテクチャの改善点**
   - n8nワークフローJSONの構造
   - ディレクトリ構成の最適化

2. **コード品質**
   - 既存ワークフロー（workflows/manual-hello-world-test.json）のレビュー
   - ベストプラクティスの適用状況
   - workflow-conventions.mdへの準拠状況

3. **ドキュメントの完全性**
   - 不足しているドキュメント
   - 古くなった情報の特定
   - READMEの充実度

4. **テストカバレッジ**
   - テストワークフローの不足
   - CI/CDパイプラインの改善点

5. **セキュリティ懸念**
   - API key管理のベストプラクティス
   - 機密情報の漏洩リスク

6. **パフォーマンス最適化**
   - ワークフローの最適化機会
   - GitHub Actionsの最適化

分析結果を以下の形式でIssueとして作成してください:
- タイトル: "Project Analysis: [カテゴリ] - [概要]"
- 優先度: High/Medium/Low
- ラベル: analysis, improvement, [カテゴリ]

各Issueには以下を含めてください:
- 問題の概要
- 影響範囲
- 提案する解決策
- 関連ファイル
- 見積もり（時間）

docs/hadayalab-automation-platform-SSOT.mdとdocs/workflow-conventions.mdを参照してください。
```

---

## 📋 次のステップ

分析が完了したら、以下のタスクを順次実行：

### タスク2: 既存ワークフローのレビュー

```
@copilot workflows/manual-hello-world-test.jsonをレビューして:
- エラーハンドリングの実装
- ノードの最適化
- 命名規則の遵守（workflow-conventions.mdに基づく）
- セキュリティ
- 可読性とメンテナンス性

改善提案をIssueとして作成してください。
```

### タスク3: テスト戦略の提案

```
@copilot このプロジェクトのテスト戦略を提案して:
- n8nワークフローのテスト方法
- テストワークフローの設計
- 統合テストの計画
- CI/CDパイプラインの改善

具体的な実装計画をIssueに記録してください。
```

---

## 🔗 参考リンク

- [GitHub Copilot タスク一覧](./github-copilot-tasks.md) - すべてのタスクリスト
- [Cursor + GitHub Copilot連携](./cursor-copilot-integration.md) - 連携ワークフロー

---

**最終更新**: 2025-12-23
**バージョン**: 1.0.0



















