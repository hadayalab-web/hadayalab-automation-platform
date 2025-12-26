# n8n Personal Access Token（API Key）取得による拡張機能 SSOT

**最終更新**: 2025-01-24
**最終検証**: 2025-01-24（公式ドキュメントと最新リファレンス）
**バージョン**: 1.0.0
**メンテナー**: HadayaLab

---

## 📚 公式リファレンス

- **n8n API Documentation**: [n8n API Documentation](https://docs.n8n.io/api/)
- **n8n-mcpパッケージ**: [n8n-mcp on npm](https://www.npmjs.com/package/n8n-mcp)
- **n8n MCP機能比較 SSOT**: [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)

---

## 🎯 概要

Personal Access Token（API Key）が取得できると、MCP Access Tokenだけではできない多くの機能が利用可能になります。

### 現在の状況（MCP Access Tokenのみ）

- ✅ ワークフローの実行
- ✅ 実行履歴の確認
- ✅ 環境変数の管理
- ✅ ワークフローの検索・詳細取得
- ❌ ワークフローの作成・更新・削除
- ❌ REST APIへのアクセス
- ❌ ノード検索・テンプレート検索
- ❌ ワークフロー検証

---

## ✅ Personal Access Token（API Key）取得による拡張機能

### 1. n8n-mcpパッケージが使用可能になる

#### 現在の状況

- ❌ **使用不可**: Personal Access Tokenが存在しないため、n8n-mcpパッケージは動作しない

#### Personal Access Token取得後

- ✅ **使用可能**: Personal Access Tokenを環境変数`N8N_API_KEY`に設定することで、n8n-mcpパッケージが動作する

#### 設定方法

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

#### 利用可能になる機能

- ✅ **ワークフローの作成**: `create_workflow`
- ✅ **ワークフローの更新**: `update_workflow`
- ✅ **ワークフローの削除**: `delete_workflow`
- ✅ **ワークフローの検証**: `validate_workflow`
- ✅ **ノード検索**: `list_node_templates`（543個のノード）
- ✅ **テンプレート検索**: `search_templates`（2,700+テンプレート）

---

### 2. REST API経由でのワークフロー操作が可能

#### 現在の状況

- ❌ **REST API使用不可**: MCP Access TokenはREST APIでは使用不可（401エラー）

#### Personal Access Token取得後

- ✅ **REST API使用可能**: Personal Access Tokenを使用してREST APIにアクセス可能

#### 利用可能になる操作

##### ワークフローの作成

```powershell
$token = "YOUR_PERSONAL_ACCESS_TOKEN"
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$workflow = @{
    name = "新しいワークフロー"
    nodes = @(...)
    connections = @(...)
} | ConvertTo-Json -Depth 100

Invoke-RestMethod -Uri "$baseUrl/workflows" -Method Post -Headers $headers -Body $workflow
```

##### ワークフローの更新

```powershell
$workflowId = "WORKFLOW_ID"
$workflow = @{
    name = "更新されたワークフロー"
    nodes = @(...)
    connections = @(...)
} | ConvertTo-Json -Depth 100

Invoke-RestMethod -Uri "$baseUrl/workflows/$workflowId" -Method Put -Headers $headers -Body $workflow
```

##### ワークフローの削除

```powershell
$workflowId = "WORKFLOW_ID"
Invoke-RestMethod -Uri "$baseUrl/workflows/$workflowId" -Method Delete -Headers $headers
```

##### ワークフローの検索

```powershell
$workflows = Invoke-RestMethod -Uri "$baseUrl/workflows" -Method Get -Headers $headers
$workflows.data | Select-Object id, name, active
```

---

### 3. ワークフローの自動化が可能

#### 現在の状況

- ⚠️ **手動操作が必要**: ワークフローの作成・更新・削除はn8n Dashboardから手動で行う必要がある

#### Personal Access Token取得後

- ✅ **完全自動化**: プログラムからワークフローを完全に制御可能

#### 利用例

##### CI/CDパイプラインでの自動デプロイ

```yaml
# GitHub Actions例
- name: Deploy workflow to n8n
  run: |
    curl -X POST \
      "https://hadayalab.app.n8n.cloud/rest/workflows" \
      -H "Authorization: Bearer ${{ secrets.N8N_API_KEY }}" \
      -H "Content-Type: application/json" \
      -d @workflows/my-workflow.json
```

##### スクリプトからの一括操作

```powershell
# 複数のワークフローを一括作成
$workflows = Get-ChildItem workflows/*.json
foreach ($workflow in $workflows) {
    $content = Get-Content $workflow.FullName -Raw
    Invoke-RestMethod -Uri "$baseUrl/workflows" -Method Post -Headers $headers -Body $content
}
```

---

### 4. ノード検索とテンプレート検索が可能

#### 現在の状況

- ❌ **検索不可**: MCP Access Tokenではノード検索・テンプレート検索ができない

#### Personal Access Token取得後

- ✅ **543個のノードを検索可能**: `list_node_templates`
- ✅ **2,700+テンプレートを検索可能**: `search_templates`

#### 利用例

##### ノード検索

```bash
# Cursor Chatで実行
@n8n-local HTTP Requestノードを検索して
@n8n-local Slackノードを検索して
```

##### テンプレート検索

```bash
# Cursor Chatで実行
@n8n-local Slack通知テンプレートを検索して
@n8n-local CRM自動化テンプレートを検索して
```

---

### 5. ワークフロー検証が可能

#### 現在の状況

- ❌ **検証不可**: MCP Access Tokenではワークフロー検証ができない

#### Personal Access Token取得後

- ✅ **ワークフロー検証可能**: `validate_workflow`

#### 検証内容

- ✅ JSON構文の検証
- ✅ ノードの存在確認（543個のノードに対応）
- ✅ 接続の妥当性チェック

#### 利用例

```bash
# Cursor Chatで実行
@n8n-local workflows/simple-time-check.jsonを検証して
```

---

### 6. プログラムからの完全制御が可能

#### 現在の状況

- ⚠️ **制限あり**: MCP Access Tokenでは実行と確認のみ可能

#### Personal Access Token取得後

- ✅ **完全制御**: ワークフローのライフサイクル全体をプログラムから制御可能

#### 利用可能な操作

- ✅ **作成**: 新しいワークフローの作成
- ✅ **更新**: 既存ワークフローの更新
- ✅ **削除**: ワークフローの削除
- ✅ **検索**: ワークフローの検索
- ✅ **検証**: ワークフローの検証
- ✅ **実行**: ワークフローの実行（MCP Access Tokenでも可能）
- ✅ **確認**: 実行履歴の確認（MCP Access Tokenでも可能）

---

## 📊 機能拡張の比較表

| 機能 | MCP Access Tokenのみ | Personal Access Token取得後 |
|------|---------------------|---------------------------|
| **ワークフロー実行** | ✅ | ✅ |
| **実行履歴確認** | ✅ | ✅ |
| **環境変数管理** | ✅ | ✅ |
| **ワークフロー検索** | ✅ | ✅ |
| **ワークフロー詳細取得** | ✅ | ✅ |
| **ワークフロー作成** | ❌ | ✅ |
| **ワークフロー更新** | ❌ | ✅ |
| **ワークフロー削除** | ❌ | ✅ |
| **ワークフロー検証** | ❌ | ✅ |
| **ノード検索** | ❌ | ✅ |
| **テンプレート検索** | ❌ | ✅ |
| **REST APIアクセス** | ❌ | ✅ |
| **n8n-mcpパッケージ** | ❌ | ✅ |
| **プログラムからの完全制御** | ❌ | ✅ |
| **CI/CD統合** | ❌ | ✅ |

---

## 🎯 具体的な拡張シナリオ

### シナリオ1: ワークフローの自動デプロイ

#### 現在（MCP Access Tokenのみ）

1. ワークフローJSONをGitHubにコミット
2. n8n Dashboardに手動でログイン
3. Import from Fileで手動インポート
4. 認証情報を手動で設定

#### Personal Access Token取得後

1. ワークフローJSONをGitHubにコミット
2. GitHub Actionsが自動的にn8n Cloudにデプロイ
3. 認証情報の設定も自動化可能（環境変数を使用）

### シナリオ2: ワークフローの一括管理

#### 現在（MCP Access Tokenのみ）

- ワークフローの作成・更新・削除は手動操作が必要
- 複数のワークフローを管理する場合、時間がかかる

#### Personal Access Token取得後

- スクリプトから一括でワークフローを管理可能
- ワークフローのバックアップ・リストアが自動化可能
- ワークフローのバージョン管理が容易

### シナリオ3: ワークフローの自動生成

#### 現在（MCP Access Tokenのみ）

- AIがワークフローを生成しても、手動でインポートする必要がある

#### Personal Access Token取得後

- AIが生成したワークフローを自動的にn8n Cloudに作成
- ワークフローの検証も自動化
- エラーがあれば自動的に修正を試みる

### シナリオ4: ノードとテンプレートの活用

#### 現在（MCP Access Tokenのみ）

- ノードやテンプレートの情報を取得できない
- 手動でn8n Dashboardから確認する必要がある

#### Personal Access Token取得後

- 543個のノードを検索可能
- 2,700+テンプレートを検索可能
- AIが適切なノードやテンプレートを自動的に選択

---

## 🔄 現在の制限と拡張後の比較

### 現在の制限（MCP Access Tokenのみ）

#### ワークフロー管理

- ❌ ワークフローの作成: n8n Dashboardから手動操作
- ❌ ワークフローの更新: n8n Dashboardから手動操作
- ❌ ワークフローの削除: n8n Dashboardから手動操作
- ⚠️ 自動化不可: すべて手動操作が必要

#### 開発効率

- ❌ ワークフローの検証: 手動で確認
- ❌ ノード検索: n8n Dashboardから手動検索
- ❌ テンプレート検索: n8n Dashboardから手動検索
- ⚠️ 時間がかかる: すべて手動操作

#### CI/CD統合

- ❌ 自動デプロイ: 不可
- ❌ 自動テスト: 不可
- ❌ 自動バックアップ: 不可

### Personal Access Token取得後の拡張

#### ワークフロー管理

- ✅ ワークフローの作成: プログラムから自動化可能
- ✅ ワークフローの更新: プログラムから自動化可能
- ✅ ワークフローの削除: プログラムから自動化可能
- ✅ 完全自動化: すべてプログラムから制御可能

#### 開発効率

- ✅ ワークフローの検証: 自動検証可能
- ✅ ノード検索: プログラムから検索可能（543個）
- ✅ テンプレート検索: プログラムから検索可能（2,700+）
- ✅ 時間短縮: 自動化により大幅に時間短縮

#### CI/CD統合

- ✅ 自動デプロイ: GitHub Actionsなどで自動化可能
- ✅ 自動テスト: ワークフロー検証を自動化可能
- ✅ 自動バックアップ: ワークフローの自動バックアップが可能

---

## 🚀 実現可能になる自動化例

### 1. GitHub Actionsでの自動デプロイ

```yaml
name: Deploy to n8n Cloud

on:
  push:
    branches: [main]
    paths:
      - 'workflows/**/*.json'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy workflows
        run: |
          for workflow in workflows/*.json; do
            curl -X POST \
              "https://hadayalab.app.n8n.cloud/rest/workflows" \
              -H "Authorization: Bearer ${{ secrets.N8N_API_KEY }}" \
              -H "Content-Type: application/json" \
              -d @"$workflow"
          done
```

### 2. ワークフローの自動バックアップ

```powershell
# すべてのワークフローをバックアップ
$token = "YOUR_PERSONAL_ACCESS_TOKEN"
$baseUrl = "https://hadayalab.app.n8n.cloud/rest"
$headers = @{
    "Authorization" = "Bearer $token"
}

$workflows = Invoke-RestMethod -Uri "$baseUrl/workflows" -Method Get -Headers $headers

foreach ($workflow in $workflows.data) {
    $workflowJson = Invoke-RestMethod -Uri "$baseUrl/workflows/$($workflow.id)" -Method Get -Headers $headers
    $workflowJson | ConvertTo-Json -Depth 100 | Out-File "backups/$($workflow.name).json"
}
```

### 3. ワークフローの自動検証とデプロイ

```bash
# ワークフローを検証してからデプロイ
@n8n-local workflows/my-workflow.jsonを検証して
# 検証が成功したら
@n8n-local workflows/my-workflow.jsonをインポートしてn8n Cloudに作成して
```

---

## 📝 まとめ

### Personal Access Token（API Key）取得による拡張

1. **n8n-mcpパッケージが使用可能**
   - ワークフローの作成・更新・削除
   - ノード検索・テンプレート検索
   - ワークフロー検証

2. **REST API経由での完全制御**
   - プログラムからワークフローを完全に制御
   - CI/CDパイプラインとの統合
   - 自動デプロイ・バックアップ

3. **開発効率の向上**
   - 手動操作が不要
   - 自動化による時間短縮
   - エラーの早期発見

4. **スケーラビリティの向上**
   - 複数のワークフローを一括管理
   - ワークフローの自動生成
   - バージョン管理の容易化

### 推奨事項

Personal Access Token（API Key）を取得することで、n8nのワークフロー管理が**完全に自動化**され、開発効率が大幅に向上します。

**特に推奨される場合**:
- ✅ 複数のワークフローを管理している
- ✅ CI/CDパイプラインと統合したい
- ✅ ワークフローの自動生成・更新をしたい
- ✅ 開発効率を向上させたい

---

## 🔄 更新履歴

### 2025-01-24 (v1.0.0)
- 初版作成
- Personal Access Token（API Key）取得による拡張機能を徹底調査
- MCP Access Tokenのみの場合との比較を明確化
- 具体的な拡張シナリオと実現可能になる自動化例を追加

---

**このドキュメントは、n8n Personal Access Token（API Key）取得による拡張機能に関する唯一の信頼できる情報源（SSOT）です。**














