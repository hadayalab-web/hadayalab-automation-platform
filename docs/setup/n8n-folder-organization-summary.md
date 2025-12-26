# n8n Cloud フォルダ整理サマリー

**作成日**: 2025-12-26
**現状**: 全ワークフローがフォルダなし（整理が必要）

---

## 📋 現在のワークフロー一覧（8個）

すべてのワークフローがフォルダに所属していません。以下のように整理することを推奨します。

### hadayalab-automation-platform フォルダに移動すべきワークフロー

以下のワークフローはプロジェクト用途のため、`hadayalab-automation-platform`フォルダに移動:

1. **google-workspace-control** (ID: `be75hW5uhXjZcWxw`) - Google Workspace制御ワークフロー（最新版）
2. **google-workspace-control** (ID: `QDUPvadwLEPA1m9U`) - Google Workspace制御ワークフロー
3. **google-workspace-control** (ID: `ntCS2BEsby6QBeg8`) - Google Workspace制御ワークフロー
4. **whop-control** (ID: `3LYMmEXrRpSVhuhE`) - Whop API制御ワークフロー
5. **whop-control** (ID: `RBPtSpOANaqqltV3`) - Whop API制御ワークフロー

**注意**: 重複したワークフロー（google-workspace-control、whop-control）があるため、最新版のみを残し、古いバージョンは削除することを推奨します。

### Personal フォルダに移動すべきワークフロー

以下のワークフローは個人的な使用用途のため、`Personal`フォルダに移動:

1. **My workflow** (ID: `1ng74p8xYGkjwSGM`)
2. **My workflow 2** (ID: `wIYuCviGXKrCNrBn`)
3. **My workflow 3** (ID: `R09LEt3uEeBkzYWD`)

---

## 🎯 整理手順

### ステップ1: フォルダを作成

1. n8n Dashboard (https://hadayalab.app.n8n.cloud) にログイン
2. 左側のサイドバーで「**Workflows**」をクリック
3. 「**+ New**」→「**Folder**」をクリック
4. 以下のフォルダを作成:
   - `Personal`
   - `hadayalab-automation-platform`

### ステップ2: ワークフローを移動

#### hadayalab-automation-platformフォルダに移動

1. **google-workspace-control** (ID: `be75hW5uhXjZcWxw`) - 最新版のみ残す
2. **whop-control** (ID: `3LYMmEXrRpSVhuhE`) - 最新版のみ残す

**重複ワークフローの削除**（推奨）:
- `google-workspace-control` (ID: `QDUPvadwLEPA1m9U`) - 削除
- `google-workspace-control` (ID: `ntCS2BEsby6QBeg8`) - 削除
- `whop-control` (ID: `RBPtSpOANaqqltV3`) - 削除

#### Personalフォルダに移動

1. **My workflow** (ID: `1ng74p8xYGkjwSGM`)
2. **My workflow 2** (ID: `wIYuCviGXKrCNrBn`)
3. **My workflow 3** (ID: `R09LEt3uEeBkzYWD`)

### ステップ3: 移動方法

各ワークフローをドラッグ&ドロップで適切なフォルダに移動するか、ワークフローメニュー（⋮）から「Move」を選択して移動先のフォルダを選択。

---

## 📝 整理後の推奨構成

```
hadayalab-automation-platform/
  ├── google-workspace-control (ID: be75hW5uhXjZcWxw) [Active]
  └── whop-control (ID: 3LYMmEXrRpSVhuhE) [Active]

Personal/
  ├── My workflow (ID: 1ng74p8xYGkjwSGM)
  ├── My workflow 2 (ID: wIYuCviGXKrCNrBn)
  └── My workflow 3 (ID: R09LEt3uEeBkzYWD)
```

---

## 🔗 関連ドキュメント

- [フォルダ整理ガイド](./n8n-folder-organization-guide.md) - 詳細な手順

---

**最終更新**: 2025-12-26

