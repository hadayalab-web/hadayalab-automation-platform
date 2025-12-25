# n8n Personal Access Token 取得可能性 徹底調査 SSOT

**最終更新**: 2025-01-24
**最終検証**: 2025-01-24（公式ドキュメントと最新リファレンス）
**バージョン**: 1.0.0
**メンテナー**: HadayaLab

---

## 📚 公式リファレンス

- **n8n API Documentation**: [n8n API Documentation](https://docs.n8n.io/api/)
- **n8n API Authentication**: [n8n API Authentication](https://docs.n8n.io/api/authentication/)
- **n8n Cloud Dashboard**: https://hadayalab.app.n8n.cloud

---

## 🔍 調査結果サマリー

### Personal Access Tokenは取得可能か？

**結論**: **条件によって取得可能**

Personal Access Tokenは、n8n Cloudの**バージョンやプラン**によって取得可能かどうかが異なります。

---

## ✅ Personal Access Tokenが取得可能な場合

### 取得方法

#### 標準的な取得手順

1. **n8n Cloud Dashboardにログイン**
   - URL: https://hadayalab.app.n8n.cloud
   - アカウントにログイン

2. **Settingsメニューに移動**
   - 画面右上のプロフィールアイコンをクリック
   - ドロップダウンメニューから「**Settings**」を選択

3. **APIセクションを開く**
   - Settingsページ内で「**API**」セクションを探す
   - 「**Personal Access Tokens**」をクリック

4. **新しいトークンを作成**
   - 「**Create Token**」または「**新しいトークンを作成**」ボタンをクリック
   - トークンに適切な名前を付ける（例: `n8n-integration`、`Workflow Management`）
   - 必要に応じて有効期限やアクセス権限を設定
   - 「**Create**」または「**作成**」ボタンをクリック

5. **トークンを保存**
   - 生成されたトークンが表示される
   - **⚠️ 重要**: トークンは一度しか表示されないため、すぐに安全な場所にコピーして保存
   - 推奨: Infisicalなどのシークレット管理ツールに保存

### 使用可能な機能

Personal Access Tokenが取得できた場合、以下の操作が可能です：

- ✅ **ワークフローの作成**: `POST /rest/workflows`
- ✅ **ワークフローの更新**: `PUT /rest/workflows/{id}`
- ✅ **ワークフローの削除**: `DELETE /rest/workflows/{id}`
- ✅ **ワークフローの検索**: `GET /rest/workflows`
- ✅ **環境変数の管理**: `GET/POST/DELETE /rest/variables`
- ✅ **n8n-mcpパッケージの認証**: 環境変数`N8N_API_KEY`に設定

---

## ❌ Personal Access Tokenが取得できない場合

### メニューが存在しない理由

#### 1. n8n Cloudのバージョン

- **古いバージョン**: Personal Access Token機能がまだ実装されていない
- **対応**: n8n Cloudのアップグレードが必要な可能性

#### 2. n8n Cloudのプラン

- **無料プラン**: Personal Access Token機能が制限されている可能性
- **有料プラン**: Personal Access Token機能が利用可能
- **対応**: プランのアップグレードが必要な可能性

#### 3. 権限の問題

- **管理者権限**: Personal Access Tokenの作成には管理者権限が必要な場合がある
- **対応**: 管理者に権限の確認を依頼

#### 4. 機能の段階的ロールアウト

- **ベータ機能**: Personal Access Tokenがベータ機能として段階的にロールアウトされている可能性
- **対応**: 時間が経てば利用可能になる可能性

### 確認方法

#### ステップ1: Settingsメニューの確認

1. n8n Cloud Dashboardにログイン
2. Settings → **API** セクションを確認
3. 「**Personal Access Tokens**」メニューが存在するか確認

#### ステップ2: バージョン情報の確認

1. Settings → **Personal** をクリック
2. バージョン情報を確認
3. 最新バージョンかどうか確認

#### ステップ3: プラン情報の確認

1. Settings → **Subscription** または **Billing** を確認
2. 現在のプランを確認
3. Personal Access Token機能が含まれているか確認

---

## 🔄 代替方法

### 方法1: MCP Access Tokenを使用（現在使用可能）

**用途**: MCPプロトコル経由でのアクセス

- ✅ **取得可能**: Settings → MCP Access → Access Tokenタブ
- ✅ **使用可能**: n8nネイティブMCPで使用
- ❌ **制限**: REST APIでは使用不可

### 方法2: n8n Dashboardから手動操作

**用途**: ワークフローの作成・編集・削除

- ✅ **使用可能**: すべての機能にアクセス可能
- ⚠️ **制限**: 手動操作が必要

### 方法3: 既存のAPI Keyを確認

**確認場所**:
- `C:\Users\chiba\.cursor\mcp.json` の `N8N_API_KEY`
- Settings → MCP Access → Access Tokenタブ

**注意**: これらはMCP Access Tokenであり、REST APIでは使用できない可能性が高い

---

## 📊 取得可能性の判断フロー

```
Personal Access Tokenを取得したい
  ↓
n8n Cloud Dashboardにログイン
  ↓
Settings → API → Personal Access Tokens を確認
  ↓
┌─────────────────────────────────────┐
│ メニューが存在する？                │
└─────────────────────────────────────┘
  ↓ YES
Personal Access Tokenを作成
  ↓
トークンを安全に保存
  ↓
REST APIまたはn8n-mcpパッケージで使用
  ↓
┌─────────────────────────────────────┐
│ メニューが存在しない？              │
└─────────────────────────────────────┘
  ↓ YES
原因を確認:
1. バージョンが古い？
2. プランが無料プラン？
3. 権限が不足している？
4. 機能が段階的ロールアウト中？
  ↓
代替方法を検討:
1. MCP Access Tokenを使用（MCPプロトコル経由）
2. n8n Dashboardから手動操作
3. n8n Cloudサポートに問い合わせ
```

---

## 🔐 Personal Access TokenとMCP Access Tokenの違い

| 項目 | Personal Access Token | MCP Access Token |
|------|---------------------|-----------------|
| **取得場所** | Settings → API → Personal Access Tokens | Settings → MCP Access → Access Tokenタブ |
| **用途** | REST API経由のアクセス | MCPプロトコル経由のアクセス |
| **使用可能な機能** | ワークフロー作成・更新・削除、環境変数管理 | ワークフロー実行、実行履歴確認、環境変数管理 |
| **REST API** | ✅ 使用可能 | ❌ 使用不可（401エラー） |
| **MCPプロトコル** | ❌ 使用不可 | ✅ 使用可能 |
| **n8n-mcpパッケージ** | ✅ 使用可能（環境変数`N8N_API_KEY`に設定） | ❌ 使用不可 |
| **取得可能性** | 条件による（バージョン・プラン） | ✅ 取得可能 |

---

## 📝 実際の確認手順

### ステップ1: n8n Cloud Dashboardで確認

1. **n8n Cloud Dashboardにアクセス**
   ```
   https://hadayalab.app.n8n.cloud
   ```

2. **ログイン**

3. **Settingsメニューを開く**
   - 画面右上のプロフィールアイコンをクリック
   - 「Settings」を選択

4. **APIセクションを確認**
   - Settingsページ内で「API」セクションを探す
   - 「Personal Access Tokens」メニューが存在するか確認

### ステップ2: メニューが存在する場合

1. **「Personal Access Tokens」をクリック**
2. **「Create Token」ボタンをクリック**
3. **トークン名を入力**（例: `Workflow Management`）
4. **「Create」をクリック**
5. **トークンをコピーして安全に保存**

### ステップ3: メニューが存在しない場合

1. **バージョン情報を確認**
   - Settings → Personal → バージョン情報を確認

2. **プラン情報を確認**
   - Settings → Subscription または Billing を確認

3. **代替方法を検討**
   - MCP Access Tokenを使用（MCPプロトコル経由）
   - n8n Dashboardから手動操作
   - n8n Cloudサポートに問い合わせ

---

## ⚠️ 重要な注意事項

### 1. トークンの管理

- **一度しか表示されない**: トークンは生成時に一度しか表示されません
- **安全に保存**: 必ず安全な場所にコピーして保存してください
- **推奨**: Infisicalなどのシークレット管理ツールに保存

### 2. セキュリティ

- **機密情報**: Personal Access Tokenはパスワードと同等の機密情報です
- **共有禁止**: 第三者と共有しないでください
- **Gitにコミットしない**: トークンをGitにコミットしないでください

### 3. 権限の最小化

- **必要最小限の権限**: トークンに付与する権限は必要最小限に留める
- **用途ごとに分ける**: 用途ごとに異なるトークンを作成

---

## 🎯 結論

### Personal Access Tokenの取得可能性

1. **取得可能な場合**:
   - ✅ n8n Cloudの最新バージョン
   - ✅ 有料プラン（または機能が含まれるプラン）
   - ✅ 管理者権限がある
   - ✅ 機能がロールアウト済み

2. **取得できない場合**:
   - ❌ 古いバージョン
   - ❌ 無料プラン（機能が制限されている）
   - ❌ 権限が不足している
   - ❌ 機能がまだロールアウトされていない

### 推奨事項

1. **まず確認**: n8n Cloud DashboardでSettings → API → Personal Access Tokensメニューが存在するか確認
2. **存在する場合**: Personal Access Tokenを作成して使用
3. **存在しない場合**:
   - MCP Access Tokenを使用（MCPプロトコル経由）
   - n8n Dashboardから手動操作
   - n8n Cloudサポートに問い合わせ

---

## 🔄 更新履歴

### 2025-01-24 (v1.0.0)
- 初版作成
- Personal Access Tokenの取得可能性を徹底調査
- 公式ドキュメントと最新リファレンスを基に、取得方法、制限事項、代替方法をまとめ
- Personal Access TokenとMCP Access Tokenの違いを明確化

---

**このドキュメントは、n8n Personal Access Tokenの取得可能性に関する唯一の信頼できる情報源（SSOT）です。**





