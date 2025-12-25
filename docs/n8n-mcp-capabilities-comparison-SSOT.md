# n8n MCP機能比較 SSOT（Single Source of Truth）

**最終更新**: 2025-01-24
**最終検証**: 2025-01-24（公式ドキュメントと実機テスト）
**バージョン**: 1.7.0
**メンテナー**: HadayaLab

---

## ⚠️ 重要な注意事項

**n8nのタスクを実行する際は、最初に必ず以下のリファレンスを参照してください。**

### 🎯 設計方針：すべてのn8nワークフローをCursor UIから直接制御

**重要な仕様**: **n8nのワークフローはすべてCursorのUIから直接制御できる仕様にする**

**推奨フロー**: `User → AI (Cursor) → n8nワークフロー`（直接制御）

この設計方針により、以下のメリットが実現されます：

- ✅ **統一された開発環境**: n8n Dashboardへの切り替え不要
- ✅ **コンテキストの維持**: Cursor内で完結するワークフロー管理
- ✅ **効率的な開発**: Cursor Chatから直接n8nワークフローを操作
- ✅ **自動化の推進**: AIエージェントによるワークフロー自動生成・管理
- ✅ **シンプルで高速**: 中間層（GitHub Copilot Agents/Copilot）を経由しないため、即座に実行可能
- ✅ **エラーが少ない**: 直接制御により、中間層によるエラーを回避

#### 実装方法

**3つの方法**を組み合わせて、すべてのn8nワークフロー操作をCursor UIから実行可能：

1. **REST API**（Personal Access Token使用）- ワークフロー作成・更新・削除・アクティブ化・無効化 ✅ **実証済み**
2. **n8nネイティブMCP**（supergateway経由）- ワークフロー実行・実行履歴・環境変数管理に特化 ✅ **実証済み**
3. **n8n-mcpパッケージ** - ワークフロー作成・編集・削除・ノード検索・テンプレート検索に特化 ✅ **使用可能**

**重要**: REST APIを使用することで、n8n-mcpパッケージが使用できない場合でも、すべてのワークフロー操作が可能です。

#### Cursor UIから実行可能な操作一覧

| 操作 | 使用する方法 | Cursor Chatコマンド例 / スクリプト | 実証状況 |
|------|------------|---------------------|---------|
| **ワークフロー作成** | REST API / n8n-mcpパッケージ | `scripts/create_workflow_simple.py` / `@n8n-local` | ✅ 実証済み |
| **ワークフロー更新** | REST API / n8n-mcpパッケージ | `scripts/update_workflow.py` / `@n8n-local` | ✅ 実証済み |
| **ワークフロー削除** | REST API / n8n-mcpパッケージ | REST API `/api/v1/workflows/{id}` DELETE / `@n8n-local` | ✅ 実証済み |
| **ワークフローアクティブ化** | REST API | `scripts/activate_workflow.py` | ✅ 実証済み |
| **ワークフロー無効化** | REST API | `scripts/deactivate_workflow.py` | ✅ 実証済み |
| **ワークフロー実行** | n8nネイティブMCP | `@n8n-cloud ワークフローを実行して` | ✅ 完全対応 |
| **実行履歴確認** | n8nネイティブMCP | `@n8n-cloud 実行履歴を表示して` | ✅ 完全対応 |
| **環境変数管理** | n8nネイティブMCP | `@n8n-cloud 環境変数を設定して` | ✅ 完全対応 |
| **ワークフロー検索** | REST API / 両方のMCP | REST API `/api/v1/workflows` GET / `@n8n-local` / `@n8n-cloud` | ✅ 実証済み |
| **ワークフロー詳細取得** | REST API / 両方のMCP | REST API `/api/v1/workflows/{id}` GET / `@n8n-cloud` | ✅ 実証済み |
| **URLからのインポート** | n8n Dashboard | GitHub raw URLをn8n Dashboardでインポート | ✅ 実証済み |
| **ノード検索** | n8n-mcpパッケージ | `@n8n-local HTTP Requestノードを検索して` | ✅ 完全対応 |
| **テンプレート検索** | n8n-mcpパッケージ | `@n8n-local Slack通知テンプレートを検索して` | ✅ 完全対応 |
| **ワークフロー検証** | n8n-mcpパッケージ | `@n8n-local workflow.jsonを検証して` | ✅ 完全対応 |

#### 禁止事項

- ❌ **n8n Dashboardでの直接編集は原則禁止**（緊急時のみ例外）
- ❌ **n8n Dashboardでのワークフロー作成は原則禁止**（緊急時のみ例外）
- ⚠️ **緊急時は例外フロー（Cloud→GitHub取り込み）を実施**（[n8n Cloud同期運用](../docs/n8n-cloud-sync.md)参照）

---

### 📚 公式リファレンス

#### n8nネイティブMCP
- **公式ドキュメント**: [Accessing n8n MCP server](https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/)
- **MCP Server URL**: `https://hadayalab.app.n8n.cloud/mcp-server/http`
- **認証**: MCP Access Token（Settings → MCP Access → Access Tokenタブ）

#### n8n-mcpパッケージ
- **npmパッケージ**: [n8n-mcp on npm](https://www.npmjs.com/package/n8n-mcp)
- **GitHubリポジトリ**: [n8n-io/n8n-mcp](https://github.com/n8n-io/n8n-mcp)
- **認証**: Personal Access Tokenが必要
- **結論**: **無料でセルフホスト版で利用したい人向け**
  - n8n Cloud: Personal Access Token取得には有料プラン（Starter以上、24€/mo）が必要
  - n8n Self-hosted: Personal Access Tokenを無料で取得可能

### 🔍 タスク実行前の確認手順

n8nのタスクを実行する前に、以下を必ず確認してください：

1. **リファレンスを参照**
   - 上記の公式ドキュメントを確認
   - 最新の機能と制限を把握

2. **認証方法の確認**
   - ネイティブMCP: MCP Access Tokenが必要（`N8N_ACCESS_TOKEN`）
   - n8n-mcpパッケージ: Personal Access Tokenが必要（Infisicalから`N8N_PERSONAL_ACCESS_TOKEN`として取得可能）

3. **機能の確認**
   - このSSOTドキュメントで、使用するMCP実装方法が目的の機能をサポートしているか確認

### 🔐 n8n認証情報（正しい情報）

**重要**: 以下の情報のみが正しい認証方法です。

#### n8nネイティブMCP認証情報

- **N8N_SERVER_URL**: `https://hadayalab.app.n8n.cloud/mcp-server/http`
- **N8N_ACCESS_TOKEN**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ZDcxM2YyMS0wZDBiLTRhYmUtYWZjNy1kYjc2MmQ4YWUzMzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJtY3Atc2VydmVyLWFwaSIsImp0aSI6ImY4YjAwMzg0LTExMjAtNGNlNS04NjQ2LTNmZWY2N2RlZTEyOSIsImlhdCI6MTc2NjU2Mzg3OX0.AmAxwL2nY7oPJblEbLz5FRwXDpc4A5dSIfsP4Ha28Qw`

#### n8n-mcpパッケージ認証情報（Infisicalから取得）

- **N8N_API_URL**: `https://hadayalab.app.n8n.cloud`
- **N8N_API_KEY**: Infisicalから取得（`N8N_PERSONAL_ACCESS_TOKEN`として保存）
  - Infisicalプロジェクト: `hadayalab-automation-platform-c79-q`
  - 取得方法: `infisical secrets get N8N_PERSONAL_ACCESS_TOKEN`

#### 重要な注意事項

- ✅ **Personal Access Tokenが取得可能になりました**（Infisicalに保存済み）
- ✅ **n8n-mcpパッケージが使用可能になりました**
- ✅ **n8nネイティブMCPも引き続き使用可能**（上記の`N8N_SERVER_URL`と`N8N_ACCESS_TOKEN`を使用）

---

### 🎯 ネイティブMCPとn8n-mcpパッケージの適正な使い分け

n8nのタスクを実行する際は、目的に応じて適切なMCP実装方法を選択してください。

#### n8nネイティブMCPを使用する場合

- ✅ **ワークフローの実行**
  - 既存のワークフローを実行したい
  - Webhook/Schedule/Chat/Form Triggerのワークフローを実行したい
  - 実行結果を取得したい

- ✅ **実行履歴の確認**
  - ワークフローの実行履歴を詳細に確認したい
  - エラーログを確認したい

- ✅ **環境変数の管理**
  - 環境変数を取得・設定・削除したい

- ✅ **ワークフローの検索・詳細取得**
  - ワークフローを検索したい
  - ワークフローの詳細情報を取得したい

#### n8n-mcpパッケージを使用する場合

- ✅ **ワークフローの作成・編集**
  - 新しいワークフローを作成したい
  - 既存のワークフローを更新したい
  - ワークフローを削除したい

- ✅ **ノード検索**
  - 利用可能なノードを検索したい（543個）
  - ノードの詳細情報を取得したい

- ✅ **テンプレート検索**
  - ワークフローテンプレートを検索したい（2,700+）
  - テンプレートの詳細情報を取得したい

- ✅ **ワークフロー検証**
  - ワークフローJSONの構文を検証したい
  - ノードの存在を確認したい
  - 接続の妥当性をチェックしたい

#### 使い分けの判断フロー

```
n8nのタスクを実行する
  ↓
何をしたいか？
  ↓
┌─────────────────────────────────────┐
│ ワークフローを実行したい？          │
│ 実行履歴を確認したい？              │
│ 環境変数を管理したい？              │
└─────────────────────────────────────┘
  ↓ YES
n8nネイティブMCPを使用
  ↓
┌─────────────────────────────────────┐
│ ワークフローを作成・編集・削除したい？│
│ ノードを検索したい？                │
│ テンプレートを検索したい？          │
│ ワークフローを検証したい？          │
└─────────────────────────────────────┘
  ↓ YES
n8n-mcpパッケージを使用
```

---

## 📋 概要

このドキュメントは、n8nの2つのMCP実装方法（**ネイティブMCP**と**n8n-mcpパッケージ**）の機能と制限を徹底的に調査し、比較した**唯一の信頼できる情報源（SSOT）**です。

### 2つの実装方法

1. **n8nネイティブMCP**（supergateway経由）
   - n8n Cloudが提供するネイティブなMCPサーバー
   - `supergateway`を使用してHTTP経由で直接接続

2. **n8n-mcpパッケージ**
   - npmパッケージとして提供されるMCPサーバー
   - n8n REST APIを使用してワークフローを操作

---

## 🎯 クイックリファレンス

**最終検証日**: 2025-01-24
**検証元**: 公式ドキュメントと実機テスト

| 機能 | n8nネイティブMCP | n8n-mcpパッケージ | 検証状況 |
|------|-----------------|------------------|---------|
| **ワークフロー検索** | ✅ | ✅ | ✅ 両方で確認済み |
| **ワークフロー詳細取得** | ✅ | ✅ | ✅ 両方で確認済み |
| **ワークフロー実行** | ✅ | ❌ | ✅ 公式ドキュメント確認済み |
| **ワークフロー作成** | ❌ | ✅ | ✅ 公式ドキュメント確認済み |
| **ワークフロー更新** | ❌ | ✅ | ✅ 公式ドキュメント確認済み |
| **ワークフロー削除** | ❌ | ✅ | ✅ 公式ドキュメント確認済み |
| **ノード検索** | ❌ | ✅ | ✅ 公式ドキュメント確認済み |
| **テンプレート検索** | ❌ | ✅ | ✅ 公式ドキュメント確認済み |
| **ワークフロー検証** | ❌ | ✅ | ✅ 公式ドキュメント確認済み |
| **実行履歴確認** | ✅ 詳細 | ⚠️ 基本のみ | ✅ 実機テスト確認済み |
| **環境変数管理** | ✅ | ❌ | ✅ 公式ドキュメント確認済み |
| **Webhook実行** | ✅ | ❌ | ✅ 実機テスト確認済み |

---

## ☁️ n8nネイティブMCP（supergateway経由）

### 📝 概要

n8n Cloudが提供するネイティブなMCPサーバーに、`supergateway`を使用してHTTP経由で直接接続する方法です。

### 🔧 設定

**ファイル**: `C:\Users\chiba\.cursor\mcp.json`

```json
{
  "mcpServers": {
    "n8n-cloud": {
      "command": "npx",
      "args": [
        "-y",
        "supergateway",
        "--streamableHttp",
        "https://hadayalab.app.n8n.cloud/mcp-server/http",
        "--header",
        "authorization:Bearer <YOUR_ACCESS_TOKEN_HERE>"
      ]
    }
  }
}
```

### ✅ できること

#### 1. ワークフロー検索
- **ツール**: `mcp_n8n_search_workflows`
- **機能**: ワークフロー名や説明で検索
- **パラメータ**:
  - `query`: 検索クエリ（オプション）
  - `limit`: 結果数の上限（デフォルト: 10、最大: 200）
  - `projectId`: プロジェクトID（オプション）
- **例**:
  ```bash
  @n8n-cloud "Cursor-Vercel"という名前のワークフローを検索して
  ```

#### 2. ワークフロー詳細取得
- **ツール**: `mcp_n8n_get_workflow_details`
- **機能**: ワークフローの詳細情報（ノード、接続、設定など）を取得
- **パラメータ**:
  - `workflowId`: ワークフローID（必須）
- **返却情報**:
  - ワークフロー名、説明、状態
  - ノード一覧と接続情報
  - トリガー情報（Webhook URL、HTTPメソッドなど）
  - 設定（`availableInMCP`など）

#### 3. ワークフロー実行
- **ツール**: `mcp_n8n_execute_workflow`
- **機能**: 公開されたワークフローを直接実行
- **パラメータ**:
  - `workflowId`: ワークフローID（必須）
  - `inputs`: 入力データ（必須）
    - `type`: `"chat"`, `"form"`, `"webhook"`のいずれか
    - タイプに応じた入力データ
- **対応トリガー**:
  - ✅ Webhook Trigger
  - ✅ Schedule Trigger
  - ✅ Chat Trigger
  - ✅ Form Trigger
- **例**:
  ```bash
  @n8n-cloud cursor-vercel-controlワークフローを実行して、action=list, projectId=xxxで
  ```

#### 4. 実行履歴の確認
- **機能**: ワークフローの実行履歴を確認可能
- **詳細**: 実行結果、エラー情報、実行時間など

#### 5. 環境変数の管理
- **機能**: n8n Cloudの環境変数を管理可能
- **詳細**: 環境変数の取得、設定、削除など

### ❌ できないこと

#### 1. ワークフローの作成
- **理由**: ネイティブMCPはワークフローの実行に特化
- **代替方法**: n8n-mcpパッケージを使用するか、n8n Dashboardから手動作成

#### 2. ワークフローの更新
- **理由**: ワークフローの編集機能は提供されていない
- **代替方法**: n8n-mcpパッケージを使用するか、n8n Dashboardから手動編集

#### 3. ワークフローの削除
- **理由**: ワークフロー削除機能は提供されていない
- **代替方法**: n8n Dashboardから手動削除、またはREST APIを使用

#### 4. ノード検索
- **理由**: ノード検索機能は提供されていない
- **代替方法**: n8n-mcpパッケージの`list_node_templates`を使用

#### 5. テンプレート検索
- **理由**: テンプレート検索機能は提供されていない
- **代替方法**: n8n-mcpパッケージの`search_templates`を使用

#### 6. ワークフロー検証
- **理由**: ワークフロー検証機能は提供されていない
- **代替方法**: n8n-mcpパッケージの`validate_workflow`を使用

### ⚠️ 制限事項

#### 1. ワークフローの公開条件
- **要件**: MCPクライアントからアクセス可能にするには、ワークフローが以下の条件を満たす必要があります：
  - ✅ ワークフローが**公開済み**であること
  - ✅ 以下のいずれかのトリガーノードを含むこと：
    - Webhook Trigger
    - Schedule Trigger
    - Chat Trigger
    - Form Trigger
  - ✅ ワークフロー設定で「**Available in MCP**」が有効になっていること

#### 2. 実行タイムアウト
- **制限**: MCPクライアントからトリガーされたワークフローは、**5分のタイムアウト**が適用されます
- **影響**: 5分以内に完了しない場合、n8nは実行を停止し、エラーを返します
- **注意**: この制限は、ワークフロー設定で設定されたタイムアウトよりも優先されます

#### 3. 入力データの制限
- **制限**: MCPクライアントは、ワークフローに対して**テキストベースの入力のみ**を提供できます
- **影響**: バイナリデータ（画像、ファイルなど）の入力はサポートされていません

#### 4. 複数トリガーの制限
- **制限**: ワークフローに複数のサポートされているトリガーノードが含まれている場合、MCPクライアントは**最初のトリガーのみ**を使用してワークフローをトリガーする可能性があります

#### 5. 人間の介入が必要なワークフロー
- **制限**: 複数ステップのフォームや人間の介入が必要なワークフローの実行はサポートされていません
- **影響**: このようなワークフローは、MCP経由で実行できません

#### 6. MCP Access Tokenの制限
- **制限**: MCP Access Token（`N8N_ACCESS_TOKEN`）は、**MCPプロトコル経由でのアクセスのみ**に使用できます
- **影響**: REST APIでは使用できません（401エラーが返されます）
- **注意**: Personal Access TokenやN8N_API_KEYは存在しないため、REST APIは使用できません

### 🔐 認証

#### 正しい認証情報

- **N8N_SERVER_URL**: `https://hadayalab.app.n8n.cloud/mcp-server/http`
- **N8N_ACCESS_TOKEN**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ZDcxM2YyMS0wZDBiLTRhYmUtYWZjNy1kYjc2MmQ4YWUzMzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJtY3Atc2VydmVyLWFwaI`（トークン全体は上記参照）

#### mcp.json設定例

```json
{
  "mcpServers": {
    "n8n-cloud": {
      "command": "npx",
      "args": [
        "-y",
        "supergateway",
        "--streamableHttp",
        "https://hadayalab.app.n8n.cloud/mcp-server/http",
        "--header",
        "authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ZDcxM2YyMS0wZDBiLTRhYmUtYWZjNy1kYjc2MmQ4YWUzMzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJtY3Atc2VydmVyLWFwaSIsImp0aSI6ImY4YjAwMzg0LTExMjAtNGNlNS04NjQ2LTNmZWY2N2RlZTEyOSIsImlhdCI6MTc2NjU2Mzg3OX0.AmAxwL2nY7oPJblEbLz5FRwXDpc4A5dSIfsP4Ha28Qw"
      ]
    }
  }
}
```

---

## 🛠️ n8n-mcpパッケージ

### 📝 概要

npmパッケージとして提供されるMCPサーバーで、n8n REST APIを使用してワークフローを操作します。

### 🔧 設定

**✅ 重要**: n8n-mcpパッケージが使用可能になりました。

**認証情報**:
- Personal Access Tokenが取得され、Infisicalに保存されています
- Infisicalから`N8N_PERSONAL_ACCESS_TOKEN`として取得可能です

**設定方法**:
- `mcp.json`で`N8N_API_KEY`環境変数にInfisicalから取得したPersonal Access Tokenを設定
- 詳細は「n8n-mcpパッケージの設定」セクションを参照

### ✅ できること

#### 1. ワークフロー作成
- **ツール**: `create_workflow`
- **機能**: 新しいワークフローを作成
- **パラメータ**:
  - ワークフローJSON（ノード、接続、設定など）
- **例**:
  ```bash
  @n8n-local workflow-cursor-vercel-control.jsonをインポートして
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

#### 4. ワークフロー検索
- **ツール**: `search_workflows`
- **機能**: ワークフロー名や説明で検索
- **パラメータ**:
  - `query`: 検索クエリ（オプション）
  - `limit`: 結果数の上限

#### 5. ワークフロー検証
- **ツール**: `validate_workflow`
- **機能**: ワークフローJSONの構文とノードを検証
- **検証内容**:
  - JSON構文の検証
  - ノードの存在確認（543個のノードに対応）
  - 接続の妥当性チェック
- **例**:
  ```bash
  @n8n-local workflow-cursor-vercel-control.jsonを検証して
  ```

#### 6. ノード検索
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

#### 7. テンプレート検索
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

#### 8. 実行履歴の確認
- **ツール**: `get_execution`
- **機能**: 実行履歴の基本情報を確認
- **制限**: 詳細情報は限定的

### ❌ できないこと

#### 1. ワークフローの直接実行
- **理由**: n8n-mcpパッケージは、ワークフローの作成・編集に特化
- **代替方法**:
  - n8nネイティブMCPを使用
  - Webhook URLに直接リクエストを送信
  - n8n Dashboardから手動実行

#### 2. Webhook Triggerの直接実行
- **理由**: Webhook Triggerのワークフローは、Webhook URLに直接リクエストを送信する必要がある
- **代替方法**:
  - n8nネイティブMCPの`execute_workflow`を使用
  - Webhook URLに直接HTTPリクエストを送信

#### 3. 環境変数の管理
- **理由**: 環境変数管理機能は提供されていない
- **代替方法**:
  - n8nネイティブMCPを使用
  - n8n Dashboardから手動設定
  - REST APIを使用

#### 4. 実行履歴の詳細確認
- **理由**: 実行履歴の詳細情報は限定的
- **代替方法**:
  - n8nネイティブMCPを使用
  - n8n Dashboardから確認

### ⚠️ 制限事項

#### 1. Personal Access Tokenが必要
- **状況**: ✅ Personal Access Tokenが取得され、Infisicalに保存済み
- **取得方法**: Infisicalから`N8N_PERSONAL_ACCESS_TOKEN`として取得可能
- **設定方法**: `mcp.json`の`N8N_API_KEY`環境変数に設定

#### 2. ワークフロー実行の制限
- **制限**: ワークフローの直接実行はできません
- **影響**: ワークフローを実行するには、n8nネイティブMCPを使用する必要があります

#### 3. バージョン管理
- **最新バージョン**: `2.31.1`（2025-01-24時点）
- **注意**: Personal Access Tokenが取得可能になったため、使用可能になりました

### 🔐 認証

**✅ 重要**: n8n-mcpパッケージが使用可能になりました。

**認証情報**:
- **Personal Access Token**: Infisicalに保存済み（`N8N_PERSONAL_ACCESS_TOKEN`として取得可能）
- **N8N_API_URL**: `https://hadayalab.app.n8n.cloud`

**設定方法**:
- `mcp.json`で`N8N_API_KEY`環境変数にInfisicalから取得したPersonal Access Tokenを設定
- 詳細は「n8n-mcpパッケージの設定」セクションを参照

**Infisicalからの取得方法**:
```powershell
# InfisicalからPersonal Access Tokenを取得
$token = "YOUR_INFISICAL_TOKEN"
$projectId = "446f131c-be8d-45e5-a83a-4154e34501a5"
$personalAccessToken = (infisical secrets get N8N_PERSONAL_ACCESS_TOKEN --token $token --projectId $projectId --output plain 2>&1 | Select-String -Pattern "N8N_PERSONAL_ACCESS_TOKEN" | ForEach-Object { $_.Line -replace '.*N8N_PERSONAL_ACCESS_TOKEN\s+', '' -replace '\s+shared.*', '' }).Trim()
```

---

## 📊 詳細比較表

### 機能比較

| 機能 | n8nネイティブMCP | n8n-mcpパッケージ | 備考 |
|------|-----------------|------------------|------|
| **ワークフロー検索** | ✅ | ✅ | 両方で利用可能 |
| **ワークフロー詳細取得** | ✅ | ✅ | 両方で利用可能 |
| **ワークフロー実行** | ✅ | ❌ | ネイティブMCPのみ |
| **ワークフロー作成** | ❌ | ✅ | n8n-mcpパッケージのみ |
| **ワークフロー更新** | ❌ | ✅ | n8n-mcpパッケージのみ |
| **ワークフロー削除** | ❌ | ✅ | n8n-mcpパッケージのみ |
| **ノード検索** | ❌ | ✅ | n8n-mcpパッケージのみ（543個） |
| **テンプレート検索** | ❌ | ✅ | n8n-mcpパッケージのみ（2,700+） |
| **ワークフロー検証** | ❌ | ✅ | n8n-mcpパッケージのみ |
| **実行履歴確認** | ✅ 詳細 | ⚠️ 基本のみ | ネイティブMCPが詳細 |
| **環境変数管理** | ✅ | ❌ | ネイティブMCPのみ |
| **Webhook実行** | ✅ | ❌ | ネイティブMCPのみ |

### 認証比較

| 認証方法 | n8nネイティブMCP | n8n-mcpパッケージ |
|---------|-----------------|------------------|
| **N8N_ACCESS_TOKEN** | ✅ | ❌ |
| **Personal Access Token** | ❌ | ✅ Infisicalから取得可能 |
| **N8N_API_KEY** | ❌ | ✅ Personal Access Tokenを使用 |
| **OAuth2** | ✅ | ❌ |

### 制限比較

| 制限事項 | n8nネイティブMCP | n8n-mcpパッケージ |
|---------|-----------------|------------------|
| **実行タイムアウト** | 5分 | N/A（実行不可） |
| **入力データ制限** | テキストのみ | N/A（実行不可） |
| **公開条件** | 必須 | N/A |
| **複数トリガー** | 最初のトリガーのみ | N/A |
| **人間の介入** | サポートなし | N/A |

---

## 🎯 使い分けガイド

### 推奨使用シーン

#### n8nネイティブMCPを使用する場合

- ✅ **ワークフローの実行**
  - Webhook Triggerのワークフローを実行
  - スケジュールTriggerのワークフローを実行
  - Chat Triggerのワークフローを実行
  - Form Triggerのワークフローを実行

- ✅ **実行履歴の詳細確認**
  - 実行結果の詳細を確認
  - エラー情報の確認
  - 実行時間の確認

- ✅ **環境変数の管理**
  - 環境変数の取得
  - 環境変数の設定
  - 環境変数の削除

#### n8n-mcpパッケージを使用する場合

- ✅ **ワークフローの作成・編集**
  - 新しいワークフローの作成
  - 既存のワークフローの更新
  - ワークフローの削除

- ✅ **ノード検索**
  - 利用可能なノードの検索（543個）
  - ノードの詳細情報の取得

- ✅ **テンプレート検索**
  - ワークフローテンプレートの検索（2,700+）
  - テンプレートの詳細情報の取得

- ✅ **ワークフロー検証**
  - ワークフローJSONの構文検証
  - ノードの存在確認
  - 接続の妥当性チェック

### 同時使用の推奨

両方を同時に使用することで、すべての機能にアクセスできます：

```json
{
  "mcpServers": {
    "n8n-cloud": {
      "command": "npx",
      "args": [
        "-y",
        "supergateway",
        "--streamableHttp",
        "https://hadayalab.app.n8n.cloud/mcp-server/http",
        "--header",
        "authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ZDcxM2YyMS0wZDBiLTRhYmUtYWZjNy1kYjc2MmQ4YWUzMzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJtY3Atc2VydmVyLWFwaSIsImp0aSI6ImY4YjAwMzg0LTExMjAtNGNlNS04NjQ2LTNmZWY2N2RlZTEyOSIsImlhdCI6MTc2NjU2Mzg3OX0.AmAxwL2nY7oPJblEbLz5FRwXDpc4A5dSIfsP4Ha28Qw"
      ]
    },
    "n8n-local": {
      "command": "npx",
      "args": ["-y", "n8n-mcp@latest"],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
        "N8N_API_KEY": "（Infisicalから取得したPersonal Access Token）",
        "LOG_LEVEL": "error",
        "NODE_NO_WARNINGS": "1"
      }
    }
  }
}
```

**⚠️ 重要**: `N8N_API_KEY`には、Infisicalから取得したPersonal Access Tokenを設定してください。

**Infisicalからの取得方法**:

```powershell
# Infisical設定
$token = "YOUR_INFISICAL_TOKEN"
$projectId = "446f131c-be8d-45e5-a83a-4154e34501a5"

# Personal Access Tokenを取得
$personalAccessToken = (infisical secrets get N8N_PERSONAL_ACCESS_TOKEN --token $token --projectId $projectId --output plain 2>&1 | Select-String -Pattern "N8N_PERSONAL_ACCESS_TOKEN" | ForEach-Object { $_.Line -replace '.*N8N_PERSONAL_ACCESS_TOKEN\s+', '' -replace '\s+shared.*', '' }).Trim()

# mcp.jsonのN8N_API_KEYに設定
Write-Host "Personal Access Token: $($personalAccessToken.Substring(0, [Math]::Min(30, $personalAccessToken.Length)))..."
```

**または、スクリプトを使用**:

```powershell
# scripts/infisical-get-secrets.ps1 を実行
.\scripts\infisical-get-secrets.ps1
```

**✅ 注意**: n8n-mcpパッケージ（`n8n-local`）が使用可能になりました。

**使用可能な機能**:
- **ワークフロー実行**: `@n8n-cloud` を使用
- **ワークフロー作成・編集・削除**: `@n8n-local` を使用（Personal Access Tokenが必要）
- **ノード検索・テンプレート検索**: `@n8n-local` を使用

---

## 📚 参考リンク

### 公式ドキュメント

- [n8n MCP Server Documentation](https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/)
- [n8n-mcp npm package](https://www.npmjs.com/package/n8n-mcp)
- [n8n-mcp GitHub](https://github.com/n8n-io/n8n-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)

### プロジェクト内ドキュメント

- [MCPサーバー導入ガイド](./mcp-servers-setup.md)
- [n8n MCP Server (supergateway経由) セットアップガイド](./n8n-mcp-supergateway-setup.md)
- [n8n-mcp パッケージ バージョン情報](./n8n-mcp-version-info.md)

---

## 🔄 更新履歴

### 2025-01-24 (v1.7.0)
- **直接制御の推奨**: GitHub Copilot Agents/Copilotを経由せず、Cursor UIから直接n8nワークフローを制御する設計方針を推奨
  - 直接制御フロー（`User → AI (Cursor) → n8nワークフロー`）のメリットを明記
  - 直接制御戦略SSOTドキュメントへのリンクを追加
  - 設計方針セクションを更新（直接制御を推奨）

### 2025-01-24 (v1.6.0)
- **完全制御の実現**: Cursor UIからn8nワークフローを完全に制御できることを実証
  - REST API経由でのワークフロー作成・更新・削除・アクティブ化・無効化を実証
  - GitHub URLからのインポート手順を実証
  - Webhookパス競合の解決方法を追加
  - すべての主要操作がCursor UIから実行可能であることを確認
  - 操作一覧テーブルを更新（実証済みの方法を明記）

### 2025-01-24 (v1.5.0)
- **Personal Access Token取得完了**: Personal Access Tokenが取得され、Infisicalに保存されたことを反映
  - n8n-mcpパッケージが使用可能になったことを明記
  - Infisicalからの取得方法を追加
  - 認証情報の設定方法を更新

### 2025-01-24 (v1.3.0)
- **設計方針の追加**: すべてのn8nワークフローをCursor UIから制御する仕様を追加
  - 設計方針とメリットを明記
  - Cursor UIから実行可能な操作一覧を追加
  - 禁止事項（n8n Dashboardでの直接編集は原則禁止）を明記
  - 実装方法（2つのMCP実装方法の組み合わせ）を説明

### 2025-01-24 (v1.5.0)
- **Personal Access Token取得完了**: Personal Access Tokenが取得され、Infisicalに保存されたことを反映
  - n8n-mcpパッケージが使用可能になったことを明記
  - Infisicalからの取得方法を追加
  - 認証情報の設定方法を更新

### 2025-01-24 (v1.4.0)
- **認証情報の修正**: 正しい認証情報を追記
  - `N8N_SERVER_URL`: `https://hadayalab.app.n8n.cloud/mcp-server/http`
  - `N8N_ACCESS_TOKEN`: 正しいトークンを追記
  - Personal Access TokenやN8N_API_KEYは存在しないことを明記（v1.5.0で更新）

### 2025-01-24 (v1.2.0)
- **トークン運用ガイドの追加**: n8nのトークン運用に関する最新情報を冒頭に追加（削除済み：誤った情報のため）

### 2025-01-24 (v1.1.0)
- **機能比較の検証**: 公式ドキュメントと実機テストで全機能を検証
- **使い分けガイドの追加**: 冒頭に適正な使い分けフローを追加
- **検証状況の明記**: クイックリファレンス表に検証状況を追加
- **リファレンスURLの追加**: 公式ドキュメントへのリンクを冒頭に追加

### 2025-01-24 (v1.0.0)
- 初版作成
- n8nネイティブMCPとn8n-mcpパッケージの機能比較を追加
- 制限事項と使い分けガイドを追加

---

**このドキュメントは、n8n MCP機能に関する唯一の信頼できる情報源（SSOT）です。**

**関連ドキュメント**:
- [n8nワークフロー直接制御戦略 SSOT](./direct-n8n-control-strategy-SSOT.md) - **直接制御の推奨設計方針**
- [n8nワークフロー完全制御 SSOT](./n8n-workflow-full-control-SSOT.md) - 実証済みの完全制御方法
- [n8n MCP Access Token 機能と制限 SSOT](./n8n-mcp-access-token-capabilities-SSOT.md) - MCP Access Tokenの詳細な機能と制限
- [n8n MCP補完方法 SSOT](./n8n-mcp-complementary-methods-SSOT.md) - MCP Access Tokenでできないことを補完する方法
- [n8n Personal Access Token 取得可能性 徹底調査 SSOT](./n8n-personal-access-token-investigation-SSOT.md) - Personal Access Tokenの取得可能性を徹底調査
- [n8n Cloud Personal Access Token 取得条件 徹底調査 SSOT](./n8n-cloud-personal-access-token-conditions-SSOT.md) - Personal Access Tokenの取得条件を徹底調査（プラン、バージョン、権限など）
- [n8n Personal Access Token 取得による拡張機能 SSOT](./n8n-personal-access-token-extensions-SSOT.md) - Personal Access Token取得により実現可能になる拡張機能
- [n8n Cloud vs Self-hosted 比較 SSOT](./n8n-cloud-vs-self-hosted-SSOT.md) - n8n CloudとSelf-hosted版の徹底比較

