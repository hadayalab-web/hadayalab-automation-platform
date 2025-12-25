# n8n MCP補完方法 SSOT（Single Source of Truth）

**最終更新**: 2025-01-24
**最終検証**: 2025-01-24（公式ドキュメントと最新リファレンス）
**バージョン**: 1.0.0
**メンテナー**: HadayaLab

---

## 📚 公式リファレンス

- **n8n-mcpパッケージ**: [n8n-mcp on npm](https://www.npmjs.com/package/n8n-mcp)
- **n8n-mcp GitHub**: [n8n-io/n8n-mcp](https://github.com/n8n-io/n8n-mcp)
- **n8n公式ドキュメント**: [Accessing n8n MCP server](https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/)
- **n8n Dashboard**: https://hadayalab.app.n8n.cloud

---

## 🎯 概要

n8n MCP Access Tokenではできない操作を補完する方法をまとめます。

### 重要な結論

**n8n-mcpパッケージは無料でセルフホスト版で利用したい人向け**

- ✅ **n8n Self-hosted版**: 無料でPersonal Access Tokenが取得可能 → n8n-mcpパッケージが使用可能
- ❌ **n8n Cloud**: Personal Access Token取得には有料プラン（Starter以上、24€/mo）が必要

### MCP Access Tokenでできないこと

1. ❌ ワークフローの作成・編集・削除
2. ❌ REST APIへのアクセス
3. ❌ ノード検索・テンプレート検索
4. ❌ ワークフロー検証

---

## ✅ 補完方法1: n8n-mcpパッケージ

### 📝 概要

npmパッケージとして提供されるMCPサーバーで、n8n REST APIを使用してワークフローを操作します。

### 🔧 設定

**ファイル**: `C:\Users\chiba\.cursor\mcp.json`

```json
{
  "mcpServers": {
    "n8n-local": {
      "command": "npx",
      "args": ["-y", "n8n-mcp@latest"],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
        "N8N_API_KEY": "<YOUR_PERSONAL_ACCESS_TOKEN>",
        "LOG_LEVEL": "error",
        "NODE_NO_WARNINGS": "1"
      }
    }
  }
}
```

### ✅ できること

#### 1. ワークフロー作成

- **ツール**: `create_workflow`
- **機能**: 新しいワークフローを作成
- **パラメータ**: ワークフローJSON（ノード、接続、設定など）
- **例**:
  ```bash
  @n8n-local workflow.jsonをインポートしてn8n Cloudに作成して
  ```

#### 2. ワークフロー更新

- **ツール**: `update_workflow`
- **機能**: 既存のワークフローを更新
- **パラメータ**:
  - `workflowId`: ワークフローID（必須）
  - ワークフローJSON（更新内容）

#### 3. ワークフロー削除

- **ツール**: `delete_workflow`
- **機能**: ワークフローを削除
- **パラメータ**:
  - `workflowId`: ワークフローID（必須）

#### 4. ワークフロー検証

- **ツール**: `validate_workflow`
- **機能**: ワークフローJSONの構文とノードを検証
- **検証内容**:
  - JSON構文の検証
  - ノードの存在確認（543個のノードに対応）
  - 接続の妥当性チェック
- **例**:
  ```bash
  @n8n-local workflow.jsonを検証して
  ```

#### 5. ノード検索

- **ツール**: `list_node_templates`
- **機能**: 利用可能なノードを検索
- **対応ノード数**: **543個**
- **カテゴリ**:
  - HTTP Request、Code、データ処理ノード
  - Slack、Gmail、Google Drive、Salesforce、Stripe、HubSpot、Jira、GitHub 等
  - PostgreSQL、MySQL、MongoDB、Snowflake、BigQuery
  - OpenAI、Claude、Gemini、LangChain 等
- **パラメータ**:
  - `query`: 検索クエリ（オプション）
  - `category`: カテゴリでフィルタ（オプション）

#### 6. テンプレート検索

- **ツール**: `search_templates`
- **機能**: ワークフローテンプレートを検索
- **対応テンプレート数**: **2,700+**
- **カテゴリ**:
  - CRM自動化、マーケティング自動化、営業支援
  - HR・採用、財務・会計、カスタマーサポート
  - データ分析、開発者向けツール
- **パラメータ**:
  - `query`: 検索クエリ（オプション）
  - `category`: カテゴリでフィルタ（オプション）

#### 7. ワークフロー検索

- **ツール**: `search_workflows`
- **機能**: ワークフロー名や説明で検索
- **パラメータ**:
  - `query`: 検索クエリ（オプション）
  - `limit`: 結果数の上限

### ⚠️ 制限事項

#### 1. 認証情報が必要

- **要件**: Personal Access Tokenが必要（環境変数`N8N_API_KEY`に設定）
- **n8n Cloud**: Personal Access Token取得には有料プラン（Starter以上、24€/mo）が必要
- **n8n Self-hosted**: 無料でPersonal Access Tokenが取得可能
- **結論**: **n8n-mcpパッケージは無料でセルフホスト版で利用したい人向け**

#### 2. コスト比較

| 環境 | Personal Access Token取得 | n8n-mcpパッケージ使用 | 月額コスト |
|------|-------------------------|-------------------|----------|
| **n8n Cloud** | ✅ 可能（Starterプラン以上） | ✅ 可能 | 24€/mo以上 |
| **n8n Self-hosted** | ✅ 可能（無料） | ✅ 可能 | サーバー費用のみ |

**推奨**: 無料でn8n-mcpパッケージを使用したい場合は、**n8n Self-hosted版**を使用

#### 2. ワークフロー実行は不可

- **制限**: ワークフローの直接実行はできません
- **代替方法**:
  - n8nネイティブMCPを使用
  - Webhook URLに直接リクエストを送信
  - n8n Dashboardから手動実行

#### 3. 環境変数管理は不可

- **制限**: 環境変数管理機能は提供されていない
- **代替方法**:
  - n8nネイティブMCPを使用
  - n8n Dashboardから手動設定

---

## ✅ 補完方法2: n8n Dashboard（手動操作）

### 📝 概要

n8n Cloud Dashboardから直接操作する方法です。最も確実で、すべての機能にアクセス可能です。

### 🔧 アクセス方法

1. n8n Cloud Dashboardにアクセス: https://hadayalab.app.n8n.cloud
2. ログイン
3. 各機能にアクセス

### ✅ できること

#### 1. ワークフローの作成

- **手順**:
  1. **Workflows** → **Add Workflow**
  2. ノードを追加してワークフローを構築
  3. 接続を設定
  4. 各ノードのパラメータを設定
  5. 保存

#### 2. ワークフローの編集

- **手順**:
  1. **Workflows** → 編集したいワークフローを選択
  2. ノードを追加・編集・削除
  3. 接続を変更
  4. パラメータを更新
  5. 保存

#### 3. ワークフローの削除

- **手順**:
  1. **Workflows** → 削除したいワークフローを選択
  2. **Delete** をクリック
  3. 確認

#### 4. ワークフローのインポート/エクスポート

- **インポート**:
  1. **Workflows** → **Import from File**
  2. JSONファイルを選択
  3. インポート完了を確認

- **エクスポート**:
  1. **Workflows** → エクスポートしたいワークフローを選択
  2. **Export** をクリック
  3. JSONファイルをダウンロード

#### 5. 環境変数の管理

- **手順**:
  1. **Settings** → **Environment Variables**
  2. 環境変数の追加・編集・削除
  3. 値の設定

#### 6. 実行履歴の確認

- **手順**:
  1. **Workflows** → ワークフローを選択
  2. **Executions** タブをクリック
  3. 実行履歴を確認

#### 7. ワークフローの実行

- **手順**:
  1. **Workflows** → ワークフローを選択
  2. **Execute Workflow** をクリック
  3. 実行結果を確認

### ⚠️ 制限事項

- **手動操作が必要**: 自動化できない
- **時間がかかる**: 複雑なワークフローの作成には時間がかかる
- **エラーの可能性**: 手動操作によるエラーの可能性がある

---

## ✅ 補完方法3: REST API（将来の可能性）

### 📝 概要

n8n REST APIを使用してワークフローを操作する方法です。現在はPersonal Access Tokenが存在しないため使用不可ですが、将来的に使用可能になる可能性があります。

### 🔧 設定

**認証**: Personal Access Tokenが必要

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_PERSONAL_ACCESS_TOKEN"
    "Content-Type" = "application/json"
}
```

### ✅ できること（Personal Access Tokenが利用可能になった場合）

#### 1. ワークフローの作成

- **エンドポイント**: `POST /rest/workflows`
- **機能**: 新しいワークフローを作成
- **パラメータ**: ワークフローJSON

#### 2. ワークフローの更新

- **エンドポイント**: `PUT /rest/workflows/{id}`
- **機能**: 既存のワークフローを更新
- **パラメータ**: ワークフローID、ワークフローJSON

#### 3. ワークフローの削除

- **エンドポイント**: `DELETE /rest/workflows/{id}`
- **機能**: ワークフローを削除
- **パラメータ**: ワークフローID

#### 4. ワークフローの検索

- **エンドポイント**: `GET /rest/workflows`
- **機能**: ワークフロー一覧を取得
- **パラメータ**: 検索クエリ（オプション）

### ⚠️ 制限事項

#### 1. Personal Access Tokenが必要

- **現状**: Personal Access Tokenは現在存在しない
- **影響**: REST APIは現在使用不可

#### 2. MCP Access Tokenは使用不可

- **制限**: MCP Access TokenはREST APIでは使用不可（401エラー）
- **理由**: MCP Access TokenはMCPプロトコル専用

---

## ✅ 補完方法4: n8n-skills（AIワークフロー生成）

### 📝 概要

n8n-skillsは、AIを使用してワークフローを自動生成するツールです。n8n-mcpと組み合わせて使用することで、AIがワークフローの設計から実装、実行、デバッグまでを一貫して行えます。

### 🔧 機能

#### 1. AIによるワークフロー生成

- **機能**: 自然言語の指示からワークフローを自動生成
- **例**: "Slackにメッセージを送信するワークフローを作成して"

#### 2. ワークフローの自動デバッグ

- **機能**: エラーを自動的に検出して修正
- **例**: 実行エラーを分析して、適切な修正を提案

#### 3. ワークフローの最適化

- **機能**: ワークフローのパフォーマンスを分析して最適化
- **例**: 不要なノードの削除、効率的な接続の提案

### ⚠️ 制限事項

- **追加ツールが必要**: n8n-skillsの導入が必要
- **設定が複雑**: 初期設定が複雑な場合がある

---

## 📊 補完方法比較表

| 機能 | n8n-mcpパッケージ | n8n Dashboard | REST API | n8n-skills |
|------|------------------|---------------|----------|------------|
| **ワークフロー作成** | ✅ | ✅ | ✅ | ✅ |
| **ワークフロー更新** | ✅ | ✅ | ✅ | ✅ |
| **ワークフロー削除** | ✅ | ✅ | ✅ | ❌ |
| **ワークフロー検証** | ✅ | ⚠️ 手動 | ❌ | ✅ |
| **ノード検索** | ✅ | ✅ | ❌ | ✅ |
| **テンプレート検索** | ✅ | ✅ | ❌ | ✅ |
| **環境変数管理** | ❌ | ✅ | ✅ | ❌ |
| **実行履歴確認** | ⚠️ 基本のみ | ✅ | ✅ | ⚠️ 基本のみ |
| **ワークフロー実行** | ❌ | ✅ | ✅ | ❌ |
| **自動化** | ✅ | ❌ | ✅ | ✅ |
| **現在の使用可能性** | ❌ 認証情報なし | ✅ | ❌ 認証情報なし | ⚠️ 要設定 |

---

## 🎯 推奨補完方法

### 現在の状況

- ✅ **n8n Dashboard**: 使用可能（手動操作）
- ❌ **n8n-mcpパッケージ**: 使用不可（Personal Access Tokenが必要）
- ❌ **REST API**: 使用不可（Personal Access Tokenが必要）

### 推奨される補完方法

#### 1. ワークフローの作成・編集・削除

**推奨**: n8n Dashboardから手動操作

**理由**:
- ✅ 確実に動作する
- ✅ すべての機能にアクセス可能
- ✅ 視覚的に確認しながら操作できる

**代替方法**（将来）:
- n8n-mcpパッケージ（Personal Access Tokenが利用可能になった場合）
- REST API（Personal Access Tokenが利用可能になった場合）

#### 2. ワークフローの検証

**推奨**: n8n Dashboardから手動確認

**理由**:
- ✅ 視覚的に確認できる
- ✅ エラーを即座に確認できる

**代替方法**（将来）:
- n8n-mcpパッケージの`validate_workflow`（Personal Access Tokenが利用可能になった場合）

#### 3. ノード検索・テンプレート検索

**推奨**: n8n Dashboardから検索

**理由**:
- ✅ 視覚的に確認できる
- ✅ 詳細情報を確認できる

**代替方法**（将来）:
- n8n-mcpパッケージの`list_node_templates`、`search_templates`（Personal Access Tokenが利用可能になった場合）

---

## 📝 まとめ

### 重要な結論

**n8n-mcpパッケージは無料でセルフホスト版で利用したい人向け**

#### n8n Cloudの場合

- **Personal Access Token取得**: 有料プラン（Starter以上、24€/mo）が必要
- **n8n-mcpパッケージ使用**: Personal Access Tokenが必要 → 有料プランが必要
- **推奨**: コストをかけてでもCloud版を使いたい場合

#### n8n Self-hosted版の場合

- **Personal Access Token取得**: 無料で取得可能
- **n8n-mcpパッケージ使用**: Personal Access Tokenが必要 → 無料で使用可能
- **推奨**: 無料でn8n-mcpパッケージを使用したい場合

### 現在使用可能な補完方法

1. ✅ **n8n Dashboard**: すべての機能にアクセス可能（手動操作）
2. ⚠️ **n8n-mcpパッケージ**:
   - n8n Cloud: 有料プランが必要（現在使用不可）
   - n8n Self-hosted: 無料で使用可能
3. ⚠️ **REST API**:
   - n8n Cloud: 有料プランが必要（現在使用不可）
   - n8n Self-hosted: 無料で使用可能

### 推奨事項

1. **無料でn8n-mcpパッケージを使用したい場合**:
   - ✅ **n8n Self-hosted版**を使用
   - ✅ Personal Access Tokenを無料で取得
   - ✅ n8n-mcpパッケージを無料で使用

2. **n8n Cloudを使用したい場合**:
   - ⚠️ Starterプラン以上（24€/mo）が必要
   - ✅ Personal Access Tokenを取得
   - ✅ n8n-mcpパッケージを使用

3. **コストを抑えたい場合**:
   - ✅ **n8n Self-hosted版**を使用（サーバー費用のみ）
   - ✅ Personal Access Tokenを無料で取得
   - ✅ n8n-mcpパッケージを無料で使用

---

## 🔄 更新履歴

### 2025-01-24 (v1.0.0)
- 初版作成
- n8n MCP Access Tokenでできないことを補完する方法を徹底調査
- n8n-mcpパッケージ、n8n Dashboard、REST API、n8n-skillsの機能と制限をまとめ
- 現在の使用可能性と将来の可能性を明確化

---

**このドキュメントは、n8n MCP補完方法に関する唯一の信頼できる情報源（SSOT）です。**

