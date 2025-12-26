# GitHub Personal Access Token スコープ検証ガイド

**最終更新**: 2025-01-24
**バージョン**: 1.0.0

---

## ✅ 現在の設定確認

画像から確認できた設定：

### 基本設定
- ✅ **Note**: `Cursor AI - GitHub Copilot Agents Integration` - 適切
- ✅ **Expiration**: `90 days (Mar 24, 2026)` - 適切

### 選択されたスコープ
- ✅ **`repo`** (Full control of private repositories) - ✅ チェック済み
  - `repo:status` - ✅ チェック済み
  - `repo:invite` - ✅ チェック済み
- ✅ **`workflow`** (Update GitHub Action workflows) - ✅ チェック済み

### 未選択のスコープ（確認が必要）
- ❓ **`copilot`** (Full control of GitHub Copilot settings and seat assignments) - 未チェック
  - 説明: GitHub Copilotの設定とシート割り当ての完全制御
  - 確認: Issue/PRに@copilotメンションを追加するために必要か？

---

## 🔍 スコープの必要性確認

### `repo`スコープ
- ✅ **必須**: Issue/PRの作成・編集・削除に必要
- ✅ **選択済み**: 問題なし

### `workflow`スコープ
- ✅ **必須**: GitHub Actionsワークフローの更新に必要
- ✅ **選択済み**: 問題なし

### `copilot`スコープ
- ❓ **確認が必要**: Issue/PRに@copilotメンションを追加するために必要か？
- **調査結果**:
  - `@copilot`メンション自体は`repo`スコープで可能
  - `copilot`スコープは、Copilotの設定やシート割り当てを管理するためのもの
  - **結論**: 基本的な接続テストには不要

---

## ✅ 結論

### 現在の設定で問題ありません

**選択されたスコープ**:
- ✅ `repo` - Issue/PRの作成・編集に必要
- ✅ `workflow` - GitHub Actionsワークフローの更新に必要

**未選択のスコープ**:
- ⚠️ `copilot` - 基本的な接続テストには不要（将来必要になる可能性あり）

### 推奨される次のステップ

1. **「Generate token」をクリック**
   - 現在の設定で問題ありません

2. **トークンをコピー**
   - ⚠️ 重要: このトークンは一度しか表示されません

3. **Infisicalに保存**
   ```bash
   infisical secrets set GITHUB_PERSONAL_ACCESS_TOKEN="your-token-here" --token YOUR_INFISICAL_TOKEN --projectId 446f131c-be8d-45e5-a83a-4154e34501a5
   ```

4. **接続テストを実行**
   ```bash
   python scripts/test-copilot-connection.py
   ```

---

## 💡 将来の拡張（オプション）

もし将来、GitHub Copilotの設定を管理する必要がある場合は、`copilot`スコープも追加できます：

- `copilot`: Full control of GitHub Copilot settings and seat assignments
  - `manage_billing:copilot`: View and edit Copilot Business seat assignments

**現時点では不要**: 基本的な接続テスト（Issue作成、@copilotメンション）には`repo`と`workflow`で十分です。

---

**このガイドは、GitHub Personal Access Tokenスコープ検証に関する唯一の信頼できる情報源（SSOT）です。**















