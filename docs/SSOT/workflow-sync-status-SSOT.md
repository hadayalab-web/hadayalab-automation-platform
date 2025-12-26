# ワークフロー同期状況 SSOT（Single Source of Truth）

**最終更新**: 2025-12-24
**バージョン**: 3.0.0
**メンテナー**: HadayaLab

---

## 📍 概要

このドキュメントは、プロジェクト`hadayalab-automation-platform`内のワークフローファイルとn8n Cloudに実装されているワークフローの同期状況を管理する**唯一の信頼できる情報源（SSOT）**です。

---

## 🔄 同期スクリプト

### n8nからプロジェクトへ同期

```bash
# 特定のワークフローをn8nから取得してプロジェクトに保存
python scripts/sync-whop-control-from-n8n.py

# n8nのみに存在する全ワークフローをプロジェクトに取得
python scripts/sync-n8n-only-workflows.py
```

### 未実装ワークフローのリストアップ

```bash
# プロジェクト内のn8n未実装ワークフローをリストアップ
python scripts/list-unimplemented-workflows.py
```

### n8nからワークフローを削除

```bash
# n8nからワークフローを削除
python scripts/delete-workflow-from-n8n.py <workflow_name>
```

---

## ✅ n8nに実装済みワークフロー

以下のワークフローは、プロジェクト内にファイルがあり、n8n Cloudにも実装されています。

| ワークフロー名 | ファイル名 | n8n ID | ステータス |
|--------------|----------|--------|----------|
| `whop-control` | `whop-control.json` | `3LYMmEXrRpSVhuhE` | ✅ 実装済み（Active） |

### whop-control ワークフロー詳細

- **n8n Cloud URL**: https://hadayalab.app.n8n.cloud/workflow/3LYMmEXrRpSVhuhE
- **Webhook URL**: https://hadayalab.app.n8n.cloud/webhook/whop-control
- **最終同期**: 2025-12-24
- **詳細**: [whop-control-workflow-SSOT.md](./whop-control-workflow-SSOT.md) を参照

---

## ❌ n8nに未実装ワークフロー

**現在、未実装のワークフローはありません。**

すべてのプロジェクト内のワークフローがn8n Cloudに実装済みです。

---

## 🗑️ 削除されたワークフロー

以下のワークフローは、プロジェクトとn8nの両方から削除されました。

### 初回削除（2025-12-24）

| ワークフロー名 | 削除日 | 理由 |
|--------------|--------|------|
| `simple-time-check` | 2025-12-24 | 不要のため削除 |
| `GitHub Copilot AI補助レビュー` | 2025-12-24 | 未実装のため削除 |
| `GitHub Copilot AI補助レビュー（検証・追加指示機能付き）` | 2025-12-24 | 未実装のため削除 |
| `GitHub Copilot自動レビュー依頼` | 2025-12-24 | 未実装のため削除 |
| `manual-hello-world-test` | 2025-12-24 | 未実装のため削除 |

### n8nのみに存在していたワークフローの削除（2025-12-24）

以下のワークフローは、一度プロジェクトに取得されましたが、その後削除されました。

| ワークフロー名 | n8n ID | 削除日 | 理由 |
|--------------|--------|--------|------|
| `AI Agent workflow` | `vU6zw0Tgm9xh0ERh` | 2025-12-24 | 不要のため削除 |
| `Cursor-Vercel Control API` | `zUDOwmEtb3y81F3G` | 2025-12-24 | 不要のため削除 |
| `Cursor-Vercel Direct Deployment Automation` | `EE7Thl6p9Zsmfns4` | 2025-12-24 | 不要のため削除 |
| `GitHub Docs File Deletion via Pull Request Automation` | `p7SxbAZbmnGscON3` | 2025-12-24 | 不要のため削除 |
| `My workflow` | `C0gS9ttYQH5FlAcJ` | 2025-12-24 | 不要のため削除 |

---

## 📊 統計情報

**最終更新時点（2025-12-24）**:

- **n8n Cloudのワークフロー数**: 2件
- **プロジェクト内のワークフローファイル数**: 2件（`whop-control.json`, `whop-control-with-api-key.json`）
- **実装済み**: 1件（`whop-control`）
- **未実装**: 0件
- **削除済み**: 10件（初回5件 + n8nのみに存在していた5件）

---

## 🔄 定期同期の推奨

プロジェクトとn8n Cloudのワークフローを同期させるため、定期的に以下のスクリプトを実行することを推奨します：

```bash
# 1. n8nから最新のwhop-controlを取得
python scripts/sync-whop-control-from-n8n.py

# 2. 未実装ワークフローを確認
python scripts/list-unimplemented-workflows.py
```

---

## 📝 関連ドキュメント

- [whop-control-workflow-SSOT.md](./whop-control-workflow-SSOT.md)
- [n8n-workflow-full-control-SSOT.md](./n8n-workflow-full-control-SSOT.md)
- [direct-n8n-control-strategy-SSOT.md](./direct-n8n-control-strategy-SSOT.md)

---

## 🔄 更新履歴

### v3.0.0 (2025-12-24)
- **n8nのみに存在していた5件のワークフローを削除**:
  - `AI Agent workflow`をn8nとプロジェクトから削除
  - `Cursor-Vercel Control API`をn8nとプロジェクトから削除
  - `Cursor-Vercel Direct Deployment Automation`をn8nとプロジェクトから削除
  - `GitHub Docs File Deletion via Pull Request Automation`をn8nとプロジェクトから削除
  - `My workflow`をn8nとプロジェクトから削除
- 現在、`whop-control`のみが実装済みワークフローとして残存

### v2.0.0 (2025-12-24)
- **大規模クリーンアップ完了**:
  - `simple-time-check`をn8nとプロジェクトから削除
  - 未実装の4件のワークフローをプロジェクトから削除
  - n8nのみに存在していた5件のワークフローをプロジェクトに取得
- すべてのプロジェクト内ワークフローがn8nに実装済みの状態に
- 同期スクリプトを追加（`sync-n8n-only-workflows.py`, `delete-workflow-from-n8n.py`）

### v1.0.0 (2025-12-24)
- 初版作成
- whop-controlワークフローの同期完了
- 未実装ワークフローのリストアップ完了

