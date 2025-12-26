# SSOT（Single Source of Truth）ドキュメント

このフォルダには、hadayalab-automation-platformプロジェクトの**唯一の信頼できる情報源（SSOT）**ドキュメントが格納されています。

## 📚 SSOTドキュメント一覧

### Level 0: プロジェクト全体SSOT

- **[hadayalab-automation-platform-SSOT.md](./hadayalab-automation-platform-SSOT.md)** - **プロジェクト全体の唯一の信頼できる情報源（最初に参照）**

### Level 1: カテゴリ別SSOT

1. **[n8n完全統合SSOT](./n8n-complete-SSOT.md)** ⭐ **n8n関連のすべての情報を統合した唯一の信頼できる情報源**
   - MCP設定・機能比較
   - ワークフロー管理運用
   - ワークフロー開発ガイド
   - 認証情報・環境変数管理
   - トラブルシューティング
   - **注意**: 他のn8n関連SSOTは参照用として残していますが、基本的にはこのドキュメントを参照してください

2. **[n8n + Whop 完全活用戦略 SSOT](./n8n-whop-full-strategy-SSOT.md)** - n8n + Whop完全統合戦略
   - Whop API統合
   - ワークフロー設計
   - 実装計画

3. **[n8nワークフロー完全制御 SSOT](./n8n-workflow-full-control-SSOT.md)** - ワークフロー制御のSSOT（参照用）
   - REST API経由の制御
   - MCP経由の制御
   - 実証済みの操作
   - **注意**: 基本的には [n8n完全統合SSOT](./n8n-complete-SSOT.md) を参照してください

4. **[ワークフロー同期状況 SSOT](./workflow-sync-status-SSOT.md)** - 同期状況のSSOT
   - 実装済みワークフロー
   - 未実装ワークフロー
   - 同期スクリプト

5. **[whop-control-workflow SSOT](./whop-control-workflow-SSOT.md)** - Whop制御ワークフローのSSOT
   - ワークフロー詳細
   - 実装済み機能
   - API仕様

## 🎯 SSOTの優先順位

矛盾がある場合の優先順位：

1. **hadayalab-automation-platform-SSOT.md** - プロジェクト全体方針
2. **カテゴリ別SSOT** - 各カテゴリの詳細
3. **実装ガイド** - 具体的な実装手順

## 📝 更新方針

- SSOTドキュメントは、最新の情報のみを保持
- 重複内容は削除
- 参照関係を明確化
- 定期的にレビュー・更新

---

**最終更新**: 2025-12-26
**整理完了**: ✅

