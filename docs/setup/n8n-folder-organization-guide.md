# n8n Cloud フォルダ整理ガイド

**作成日**: 2025-12-26
**目的**: n8n Cloudのワークフローをフォルダで整理するためのガイド

---

## 📁 推奨フォルダ構成

### Personal
- **用途**: 私の使用用途（個人的なワークフロー）
- **説明**: 個人的な自動化や実験的なワークフローを保存

### hadayalab-automation-platform
- **用途**: プロジェクト用途（hadayalab-automation-platformプロジェクト関連）
- **説明**: hadayalab-automation-platformプロジェクトで使用するワークフローを保存

---

## 🚀 フォルダ作成手順

### 1. n8n Dashboardにアクセス

https://hadayalab.app.n8n.cloud にログイン

### 2. フォルダを作成

1. 左側のサイドバーで「**Workflows**」をクリック
2. 「**+ New**」ボタンをクリック
3. 「**Folder**」を選択
4. フォルダ名を入力:
   - `Personal`
   - `hadayalab-automation-platform`
5. 「**Create**」をクリック

---

## 📦 ワークフローの移動手順

### 方法1: ドラッグ&ドロップ（推奨）

1. ワークフロー一覧画面で、移動したいワークフローを見つける
2. ワークフローをクリック&ドラッグ
3. 移動先のフォルダにドロップ

### 方法2: メニューから移動

1. 移動したいワークフロー名の右側にある「**⋮**」（3つの点）をクリック
2. 「**Move**」または「**Move to folder**」を選択
3. 移動先のフォルダを選択
4. 「**Move**」をクリック

---

## 📋 ワークフロー分類基準

### Personalフォルダに移動するワークフロー

- 個人的な自動化
- 実験的なワークフロー
- テスト用ワークフロー
- プロジェクト外のワークフロー

### hadayalab-automation-platformフォルダに移動するワークフロー

- `google-workspace-control` - Google Workspace制御ワークフロー
- `whop-control` - Whop API制御ワークフロー（プロジェクト関連）
- その他、hadayalab-automation-platformプロジェクトで使用するワークフロー

---

## 🔍 現在のワークフロー確認

現在のワークフロー一覧を確認するには:

```bash
python scripts/n8n-folder-management.py list
```

---

## ⚠️ 注意事項

- n8n Cloudのフォルダ機能は、n8n Dashboardから手動で作成・移動する必要があります
- API経由でのフォルダ作成・移動は、n8n Cloudの有料プランで利用可能な場合があります
- ワークフローを移動しても、ワークフローの設定や実行履歴は影響を受けません

---

## 📝 次のステップ

1. フォルダを作成（Personal、hadayalab-automation-platform）
2. 既存のワークフローを適切なフォルダに移動
3. 新しいワークフローを作成する際は、適切なフォルダを選択して保存

---

**最終更新**: 2025-12-26
**作成者**: HadayaLab

