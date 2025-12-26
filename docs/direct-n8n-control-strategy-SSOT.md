# n8nワークフロー直接制御戦略 SSOT（Single Source of Truth）

**最終更新**: 2025-01-24
**最終検証**: 2025-01-24
**バージョン**: 1.0.0
**メンテナー**: HadayaLab

---

## 🎯 概要

**Cursor UIから直接n8nワークフローを制御する設計方針**

このドキュメントは、GitHub Copilot Agents/Copilotを経由せずに、Cursor UIから直接n8nワークフローを制御する方法をまとめた**唯一の信頼できる情報源（SSOT）**です。

---

## ✅ 実証済みの直接制御方法

以下の方法で、Cursor UIから直接n8nワークフローを制御できます：

### 1. REST API（Personal Access Token使用）✅

**実証済みの操作:**
- ✅ ワークフロー作成
- ✅ ワークフロー更新
- ✅ ワークフロー削除
- ✅ ワークフローアクティブ化
- ✅ ワークフロー無効化
- ✅ ワークフロー検索
- ✅ ワークフロー詳細取得

**エンドポイント例:**
- `POST /api/v1/workflows` - ワークフロー作成
- `PUT /api/v1/workflows/{id}` - ワークフロー更新
- `DELETE /api/v1/workflows/{id}` - ワークフロー削除
- `POST /api/v1/workflows/{id}/activate` - アクティブ化
- `POST /api/v1/workflows/{id}/deactivate` - 無効化

**認証**: `X-N8N-API-KEY` ヘッダー

**スクリプト例:**
- `scripts/create_workflow_simple.py`
- `scripts/update_workflow.py`
- `scripts/activate_workflow.py`
- `scripts/deactivate_workflow.py`

### 2. n8nネイティブMCP（supergateway経由）✅

**実証済みの操作:**
- ✅ ワークフロー実行
- ✅ 実行履歴確認
- ✅ 環境変数管理

**使用方法:**
- Cursor Chat内で `@n8n` を指定
- MCP経由でn8n Cloudに接続

### 3. n8n-mcpパッケージ ✅

**実証済みの操作:**
- ✅ ワークフロー作成
- ✅ ワークフロー編集
- ✅ ワークフロー削除
- ✅ ノード検索
- ✅ テンプレート検索
- ✅ ワークフロー検証

**使用方法:**
- Cursor Chat内で `@n8n-mcp` を指定
- パッケージ経由でn8n Cloudに接続

---

## 🔄 推奨ワークフロー

### 直接制御フロー（推奨）

```
User → AI (Cursor) → n8nワークフロー
```

**メリット:**
- ✅ シンプルで高速
- ✅ 中間層が不要
- ✅ エラーが少ない
- ✅ 完全に自動化可能
- ✅ 実証済み

**使用シーン:**
- ワークフローの作成・更新・削除
- ワークフローの実行
- ワークフローの管理全般

### GitHub Copilot経由フロー（オプション）

```
User → AI (Cursor) → GitHub Copilot Agents/Copilot → n8nワークフロー
```

**メリット:**
- ✅ GitHub Copilotのレビュー機能を活用
- ✅ Issue/PR管理と連携
- ✅ 複数AIエージェントの協調

**使用シーン:**
- コードレビューが必要な場合
- Issue/PR管理と連携したい場合
- 複数AIエージェントの協調が必要な場合

---

## 💡 実装例

### 例1: Cursor UIから直接ワークフローを作成

```python
# scripts/create_workflow_simple.py
import requests
import json
from infisical import InfisicalClient

# InfisicalからAPIキーを取得
client = InfisicalClient()
api_key = client.get_secret("N8N_API_KEY")

# ワークフローを作成
response = requests.post(
    "https://your-n8n-instance.com/api/v1/workflows",
    headers={"X-N8N-API-KEY": api_key},
    json={
        "name": "My Workflow",
        "nodes": [...],
        "connections": {...}
    }
)
```

### 例2: Cursor Chatから直接ワークフローを実行

```
@n8n execute workflow "my-workflow-id" with parameters {"key": "value"}
```

### 例3: Cursor Chatから直接ワークフローを検索

```
@n8n-mcp search workflows "slack notification"
```

---

## 📊 比較表

| 操作 | 直接制御 | GitHub Copilot経由 |
|------|---------|-------------------|
| **ワークフロー作成** | ✅ 即座に実行 | ⚠️ Issue作成→待機→実行 |
| **ワークフロー更新** | ✅ 即座に実行 | ⚠️ Issue作成→待機→実行 |
| **ワークフロー削除** | ✅ 即座に実行 | ⚠️ Issue作成→待機→実行 |
| **ワークフロー実行** | ✅ 即座に実行 | ⚠️ Issue作成→待機→実行 |
| **コードレビュー** | ❌ 不可 | ✅ 可能 |
| **Issue/PR連携** | ❌ 不可 | ✅ 可能 |
| **複数AI協調** | ❌ 不可 | ✅ 可能 |
| **エラー率** | ✅ 低い | ⚠️ 中間層によるエラー |
| **実行速度** | ✅ 高速 | ⚠️ 遅い（待機時間あり） |

---

## 🎯 推奨事項

### 基本方針

**直接制御を優先し、必要に応じてGitHub Copilot経由を使用**

1. **通常のワークフロー操作**: 直接制御を使用
   - 作成、更新、削除、実行、管理

2. **レビューが必要な場合**: GitHub Copilot経由を使用
   - コードレビュー
   - アーキテクチャ分析
   - ベストプラクティス検証

3. **Issue/PR管理と連携**: GitHub Copilot経由を使用
   - Issue作成と自動化
   - PRレビューと自動化

---

## 📝 関連ドキュメント

- [n8nワークフロー完全制御 SSOT](./n8n-workflow-full-control-SSOT.md)
- [GitHub Copilot AI Assistant Workflow SSOT](./github-copilot-ai-assistant-workflow-SSOT.md)
- [n8n MCP Capabilities Comparison SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)

---

## 🔄 更新履歴

### v1.0.0 (2025-01-24)
- 初版作成
- 直接制御方法の実証結果を反映
- GitHub Copilot経由との比較を追加













