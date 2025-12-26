# n8n完全統合SSOT（Single Source of Truth）

**最終更新**: 2025-12-26
**バージョン**: 1.0.0
**メンテナー**: HadayaLab

---

## ⚠️ 重要な注意事項

**このドキュメントは、n8nに関するすべての情報の唯一の信頼できる情報源（SSOT）です。**

n8nに関する作業を行う前に、必ずこのドキュメントを参照してください。

---

## 📋 目次

1. [概要・設計方針](#1-概要設計方針)
2. [役割分担](#2-役割分担)
3. [MCP設定](#3-mcp設定)
4. [ワークフロー管理運用](#4-ワークフロー管理運用)
5. [ワークフロー開発ガイド](#5-ワークフロー開発ガイド)
6. [MCP機能比較](#6-mcp機能比較)
7. [認証情報](#7-認証情報)
8. [環境変数・シークレット管理](#8-環境変数シークレット管理)
9. [トラブルシューティング](#9-トラブルシューティング)

---

## 1. 概要・設計方針

### プロジェクト情報

- **実行環境**: n8n Cloud (https://hadayalab.app.n8n.cloud)
- **バージョン管理**: GitHub
- **リポジトリ**: https://github.com/hadayalab-web/hadayalab-automation-platform

### フォルダ（プロジェクト）構成

n8n Cloudのワークフローは以下の2つのフォルダ（プロジェクト）で整理されています:

#### Personal - 私の使用用途

- **URL**: https://hadayalab.app.n8n.cloud/projects/fPT5foO8DCTDBr0k/workflows
- **プロジェクトID**: `fPT5foO8DCTDBr0k`
- **用途**: 個人的な自動化や実験的なワークフロー
- **説明**: 個人的な使用目的のワークフローを保存

#### hadayalab-automation-platform - プロジェクト用途

- **URL**: https://hadayalab.app.n8n.cloud/projects/9D29Es58GIo6IPkZ/workflows
- **プロジェクトID**: `9D29Es58GIo6IPkZ`
- **用途**: hadayalab-automation-platformプロジェクト関連のワークフロー
- **説明**: プロジェクトで使用する本番ワークフローを保存
- **ワークフローディレクトリ**: `workflows/`

### 🎯 設計方針：すべてのn8nワークフローをCursor UIから直接制御

**重要な仕様**: **n8nのワークフローはすべてCursorのUIから直接制御できる仕様にする**

**推奨フロー**: `User → AI (Cursor) → n8nワークフロー`（直接制御）

この設計方針により、以下のメリットが実現されます：

- ✅ **統一された開発環境**: n8n Dashboardへの切り替え不要
- ✅ **コンテキストの維持**: Cursor内で完結するワークフロー管理
- ✅ **効率的な開発**: Cursor Chatから直接n8nワークフローを操作
- ✅ **自動化の推進**: AIエージェントによるワークフロー自動生成・管理
- ✅ **シンプルで高速**: 中間層を経由しないため、即座に実行可能
- ✅ **エラーが少ない**: 直接制御により、中間層によるエラーを回避

### SSOT原則

- **GitHubが唯一の信頼できる情報源（Single Source of Truth）**
- すべての変更はGitHubを起点とする
- n8n Cloud UIは動作確認・モニタリング用途のみ
- ワークフローの真実の状態は常にGitHubリポジトリに存在

### 禁止事項

- ❌ **n8n Dashboardでの直接編集は原則禁止**（緊急時のみ例外）
- ❌ **n8n Dashboardでのワークフロー作成は原則禁止**（緊急時のみ例外）
- ⚠️ **緊急時は例外フロー（Cloud→GitHub取り込み）を実施**

---

## 2. 役割分担

### 人間の役割: なし（すべてCursorの役割）

### Cursorの役割: すべて（n8n APIを使用したインポート/エクスポート、オプションでGitHubへのコミット・プッシュ）

- ✅ ワークフローの作成・編集・削除
- ✅ **n8n Cloudへのインポート（n8n-MCPパッケージを使用）**
- ✅ コード生成・リファクタリング
- ✅ バグ修正
- ✅ テスト実行
- ✅ **GitHubへのコミット・プッシュ（CursorはGitHubにシームレスにつながっているため自動実行）**

**原則**: Cursorはワークフローの作成・編集後、n8n APIを使用してn8n Cloudに直接インポートできる。GitHubはバックアップ/バージョン管理として使用するが、必須ではない。

---

## 3. MCP設定

### 設定ファイル

**パス**: `C:\Users\chiba\.cursor\mcp.json`

### 設定内容（最新版を使用）

```json
{
  "mcpServers": {
    "n8n-local": {
      "command": "npx",
      "args": ["-y", "n8n-mcp@latest"],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
        "N8N_API_KEY": "<YOUR_N8N_API_KEY>",
        "LOG_LEVEL": "error",
        "NODE_NO_WARNINGS": "1"
      }
    },
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

**重要な設定**:
- ✅ `@latest` を使用して常に最新版のn8n-mcpパッケージを使用
- ✅ `n8n-local`: ワークフロー開発・ノード検索・テンプレート検索用
- ✅ `n8n-cloud`: ワークフロー実行・環境変数管理用（ネイティブMCP）

### MCPサーバーの使い分け

#### n8n-local（ローカル開発用・n8n-mcpパッケージ）

**用途**:
- ✅ ワークフローの作成・編集・削除
- ✅ ノード検索（543個）
- ✅ テンプレート検索（2,700+）
- ✅ ワークフロー検証

**使用方法**:
```
@n8n-local ワークフロー一覧を表示して
@n8n-local Gmailノードを検索して
@n8n-local テンプレートを検索して、keyword=email
@n8n-local workflow.jsonを検証して
```

#### n8n-cloud（n8n Cloud実装用・ネイティブMCP）

**重要**: **n8nを有料プランにすると、ネイティブのn8n-MCPでほとんどのオペレーションができるようになります**

**用途**（有料プラン）:
- ✅ ワークフローの作成・更新・削除（有料プラン）
- ✅ ワークフローの実行
- ✅ 環境変数の管理
- ✅ 実行履歴の詳細確認
- ✅ Webhook Triggerのワークフローも直接実行可能
- ✅ その他ほとんどのn8n操作

**使用方法**:
```
@n8n-cloud whop-controlワークフローを実行して、action=get_members
@n8n-cloud 環境変数一覧を表示して
@n8n-cloud 実行履歴を確認して
@n8n-cloud ワークフローを作成して（有料プラン）
@n8n-cloud ワークフローを更新して（有料プラン）
```

**有料プランでの推奨**: n8nを有料プランにする場合、ネイティブMCPでほとんどのオペレーションが可能になるため、n8n-mcpパッケージ（n8n-local）は主にノード検索・テンプレート検索用途として使用することを推奨します。

### セットアップ手順

#### 1. 認証情報の準備

##### n8n-local用（Personal Access Token）

1. n8n Cloud Dashboard → Settings → API → Personal Access Tokens
2. 「Create Token」をクリック
3. Tokenをコピー

**注意**: Personal Access Token取得には有料プラン（Starter以上、24€/mo）が必要

##### n8n-cloud用（MCP Access Token）

1. n8n Cloud Dashboard → Settings → MCP Access → Access Tokenタブ
2. Tokenをコピー

#### 2. mcp.jsonの更新

1. `C:\Users\chiba\.cursor\mcp.json` を開く
2. 上記の設定例を参考に、認証情報を埋める
3. JSON構文を検証

#### 3. Cursor再起動

1. すべてのCursorウィンドウを閉じる
2. 30秒待機（MCPサーバーの接続を確実に切断）
3. Cursorを再起動

#### 4. 動作確認

```bash
# ローカル開発用
@n8n-local 利用可能なツールを表示して

# n8n Cloud実装用
@n8n-cloud 利用可能なツールを表示して
```

---

## 4. ワークフロー管理運用

### 標準フロー（Cursor → n8n Cloud）

#### ステップ1-3: Cursorの役割（自動実行）

**原則**: Cursorは以下の作業を自動的に実行します。

1. **Cursorでワークフロー編集**
2. **ローカル検証**
   - `npm run format`（自動整形）
   - `npm run format:check`（確認）
3. **GitHubへコミット・プッシュ（オプション・自動実行）**
   - Cursorが自動的にコミット・プッシュを実行
   - GitHubはバックアップ/バージョン管理として使用（必須ではない）

#### ステップ5-7: Cursorの役割（自動実行）

5. **環境変数ファイルの確認**（自動・Cursorの役割）
   - `.env`ファイルが存在するか確認
   - 存在しない場合は`.env.env`ファイルも確認（`.env.env`ファイルも対応）
   - `N8N_API_KEY`が設定されていることを確認

6. **n8n Cloudへインポート**（自動・Cursorの役割）
   - インポートスクリプトを使用: `python scripts/import-workflow-to-n8n.py workflows/workflow-name.json`
   - またはn8n-MCPパッケージを使用: `@n8n-local workflows/workflow-name.jsonをインポートして`
   - またはn8n APIを使用して直接インポート（GitHub経由不要）
   - ワークフローIDとURLを確認

7. **インポート後の検証**（自動・Cursorの役割）
   - ワークフローが正常にインポートされたことを確認（ワークフローIDとURLを確認）
   - テストスクリプトを作成して基本動作を確認
   - Webhook URLの基本動作確認

#### ステップ8-10: 人間の役割（手動）

8. **フォルダへの移動**（手動・人間の役割）
   - Personalフォルダ: `https://hadayalab.app.n8n.cloud/projects/fPT5foO8DCTDBr0k/workflows`
   - hadayalab-automation-platformフォルダ: `https://hadayalab.app.n8n.cloud/projects/9D29Es58GIo6IPkZ/workflows`
   - n8n Dashboardでドラッグ&ドロップで移動

9. **認証情報の設定**（手動・人間の役割）
   - 各ノードの認証情報を設定
   - Google Workspace、Chatwork等の認証情報を設定

10. **ワークフローの有効化**（手動・人間の役割）
    - 「Activate」ボタンをクリック
    - 「Available in MCP」を有効化（MCP経由でアクセスする場合）

**詳細**: [ワークフローインポートベストプラクティス](./n8n-complete-SSOT-workflow-import-best-practices.md) を参照

**重要**: ワークフローのインポート/エクスポートはGitHub経由でなくてもよい。n8n APIを直接使用してインポート/エクスポートできる。

### 例外フロー（Cloud → ローカル取り込み）

Cloud UIで編集した場合の手順：

1. **Cloud UIで編集実施**（手動・人間の役割）
2. **Export（JSONダウンロード）またはn8n APIで取得**（手動・人間の役割、またはCursorがn8n APIで取得）
3. **`workflows/`へ保存（命名規約準拠）**（Cursorの役割・自動実行）
4. **`npm run format`（自動整形）**（Cursorの役割・自動実行）
5. **GitHubへpush（オプション・バックアップとして）**（Cursorの役割・自動実行）

**注意**: GitHubはバックアップ/バージョン管理として使用するが、インポート/エクスポートはn8n APIで直接実行できる

---

## 5. ワークフロー開発ガイド

### n8n-MCPパッケージの活用（車輪の再発明禁止）

#### 原則

- ✅ **n8n-MCPパッケージのテンプレート（2,700+）を参照**
- ✅ **n8n-MCPパッケージのノード（543個）を参照**
- ✅ **既存の実装を活用**

#### ノード検索（543個）

```
@n8n-local Gmailノードを検索して
@n8n-local HTTP Requestノードを検索して
```

#### テンプレート検索（2,700+）

```
@n8n-local テンプレートを検索して、keyword=email automation
@n8n-local テンプレートを検索して、keyword=webhook trigger
```

### ファイル名規則

`<category>-<purpose>[-version].json`

#### カテゴリ

- `webhook`: Webhook トリガー
- `schedule`: スケジュール実行
- `manual`: 手動実行
- `email`: メールトリガー

#### 例

- `webhook-slack-notification.json`
- `schedule-daily-report-v2.json`
- `manual-hello-world-test.json`
- `email-support-automation.json`

### タグ運用（ワークフローJSON内）

```json
{
  "tags": ["production", "mcp", "slack"]
}
```

#### 推奨タグ

- `test`: テスト用
- `production`: 本番稼働
- `mcp`: MCP経由で作成
- `draft`: ドラフト

### ワークフロー構造

- **必須**: `name`, `nodes`, `connections`
- **推奨**: `tags`, `settings`, `pinData`

---

## 6. MCP機能比較

### クイックリファレンス

| 機能 | n8nネイティブMCP | n8n-mcpパッケージ | 備考 |
|------|-----------------|------------------|------|
| **ワークフロー検索** | ✅ | ✅ | 両方で利用可能 |
| **ワークフロー詳細取得** | ✅ | ✅ | 両方で利用可能 |
| **ワークフロー実行** | ✅ | ❌ | ネイティブMCPのみ |
| **ワークフロー作成** | ✅ 有料プラン | ✅ | 有料プランではネイティブMCPでも可能 |
| **ワークフロー更新** | ✅ 有料プラン | ✅ | 有料プランではネイティブMCPでも可能 |
| **ワークフロー削除** | ✅ 有料プラン | ✅ | 有料プランではネイティブMCPでも可能 |
| **ノード検索** | ❌ | ✅ | n8n-mcpパッケージのみ（543個） |
| **テンプレート検索** | ❌ | ✅ | n8n-mcpパッケージのみ（2,700+） |
| **ワークフロー検証** | ❌ | ✅ | n8n-mcpパッケージのみ |
| **実行履歴確認** | ✅ 詳細 | ⚠️ 基本のみ | ネイティブMCPが詳細 |
| **環境変数管理** | ✅ | ❌ | ネイティブMCPのみ |
| **Webhook実行** | ✅ | ❌ | ネイティブMCPのみ |

### 使い分けガイド

#### n8nネイティブMCPを使用する場合

**有料プラン**: n8nを有料プランにすると、ネイティブMCPでほとんどのオペレーションが可能になります。

- ✅ **ワークフローの作成・更新・削除**（有料プラン）
- ✅ **ワークフローの実行**
- ✅ **実行履歴の確認**
- ✅ **環境変数の管理**
- ✅ **ワークフローの検索・詳細取得**
- ✅ **その他ほとんどのn8n操作**（有料プラン）

#### n8n-mcpパッケージを使用する場合

- ✅ **ノード検索**（543個）
- ✅ **テンプレート検索**（2,700+）
- ✅ **ワークフロー検証**

**無料プランでの代替用途**（有料プランがない場合）:
- ✅ ワークフローの作成・編集・削除
- ✅ 実行履歴の基本確認

---

## 7. 認証情報

### n8nネイティブMCP認証情報

- **N8N_SERVER_URL**: `https://hadayalab.app.n8n.cloud/mcp-server/http`
- **N8N_ACCESS_TOKEN**: MCP Access Token（Settings → MCP Access → Access Tokenタブ）

### n8n-mcpパッケージ認証情報（Infisicalから取得）

- **N8N_API_URL**: `https://hadayalab.app.n8n.cloud`
- **N8N_API_KEY**: Infisicalから取得（`N8N_PERSONAL_ACCESS_TOKEN`として保存）
  - Infisicalプロジェクト: `hadayalab-automation-platform-c79-q`
  - 取得方法: `infisical secrets get N8N_PERSONAL_ACCESS_TOKEN`

**注意**: Personal Access Token取得には有料プラン（Starter以上、24€/mo）が必要

---

## 8. 環境変数・シークレット管理

### .envファイルのキー管理（重要）

**`.env`ファイルの位置**: `C:\Users\chiba\hadayalab-automation-platform\.env`

**重要事項**:
- ✅ **`.env`ファイルにAPIキーや認証情報が格納されている**
- ✅ ローカル開発環境で使用するすべてのシークレットは`.env`ファイルで管理
- ⚠️ `.env`ファイルは`.gitignore`に含まれており、Gitにコミットされない
- ⚠️ `.env`ファイルは共有しない（機密情報のため）
- ✅ 必要なキーが不足している場合は、Infisicalまたはn8n Cloud環境変数から取得

**`.env`ファイルに含まれる可能性があるキー**:
- `N8N_API_KEY` - n8n Cloud API認証キー
- `WHOP_API_KEY` - Whop API認証キー
- `TELEGRAM_BOT_TOKEN` - Telegram Bot認証トークン
- `GOOGLE_OAUTH_2.0_CLIENT_ID` - Google OAuth2 Client ID
- `GOOGLE_OAUTH_2.0_SECRET` - Google OAuth2 Client Secret
- `GOOGLE_OAUTH_2.0_REFRESH_TOKEN` - Google OAuth2 Refresh Token
- その他のAPIキーや認証情報

**運用ルール**:
1. `.env`ファイルはプロジェクトルートに配置
2. 新しいAPIキーを取得した場合は`.env`ファイルに追加
3. `.env`ファイルのバックアップは安全な場所に保管
4. チームメンバーには`.env`ファイルの直接共有ではなく、Infisicalなどのシークレット管理ツールを使用

### 本番環境（n8n Cloud）

- ✅ **n8n Cloud環境変数**: n8n Cloud Dashboardで管理
- ✅ **Infisical**: シークレット一元管理（推奨）

---

## 9. トラブルシューティング

### MCPサーバーが動作しない場合

1. **認証情報の確認**
   - `mcp.json`の認証情報が正しいか確認
   - n8n Cloud Dashboardでトークンが有効か確認

2. **Cursor再起動**
   - すべてのCursorウィンドウを閉じる
   - 30秒待機
   - Cursorを再起動

3. **ログの確認**
   - Cursor Settings → Tools & MCP → [MCP名] → "Show Output"
   - エラーメッセージを確認

### ワークフローがインポートできない場合（実証済みベストプラクティス）

**詳細**: [ワークフローインポートベストプラクティス](./n8n-complete-SSOT-workflow-import-best-practices.md) を参照

#### エラー: "Install this node to use it" / "Node is not currently installed"

- **原因**: 存在しないノードタイプがワークフローに含まれている
- **対策**: ワークフロー作成前に`@n8n-local [ノード名]ノードを検索して`で存在確認

#### エラー: "Cannot read properties of undefined (reading 'execute')"

- **原因**: 認証情報が設定されていない、またはノードがインストールされていない
- **対策**: 各ノードで認証情報を設定、ノードの存在確認

#### エラー: "request/body must NOT have additional properties"

- **原因**: n8n APIが受け付けないプロパティが含まれている
- **対策**: `name`, `nodes`, `connections`, `settings`のみを保持。`versionId`, `updatedAt`, `tags`等を削除
- **推奨**: `scripts/import-workflow-to-n8n.py`で自動クリーンアップ

#### エラー: "request/body/tags is read-only"

- **原因**: `tags`プロパティをワークフロー作成時に含めた
- **対策**: 作成時は`tags`を含めず、作成後にn8n Dashboardで設定

**ベストプラクティス**（実証済み）:
1. ノードの存在確認（`@n8n-local`で検索）
2. 環境変数ファイルの確認（`.env`または`.env.env`に`N8N_API_KEY`が設定されているか）
3. インポートスクリプト使用（`scripts/import-workflow-to-n8n.py`）
4. インポート後の検証（ワークフローIDとURLを確認）
5. フォルダへの移動（Personalまたはhadayalab-automation-platform）
6. 認証情報の設定（人間の役割）
7. ワークフローの有効化（人間の役割）
8. テストスクリプトの作成と基本動作確認（Cursor）

### ワークフローが実行できない場合

1. **ワークフローの公開状態確認**
   - ワークフローが公開済みか確認
   - 「Available in MCP」が有効になっているか確認

2. **認証情報の確認**
   - 各ノードの認証情報が正しく設定されているか確認

3. **実行履歴の確認**
   - `@n8n-cloud 実行履歴を確認して`でエラーログを確認

---

## 📚 参考リンク

### 公式ドキュメント

- [n8n MCP Server Documentation](https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/)
- [n8n-mcp npm package](https://www.npmjs.com/package/n8n-mcp)
- [n8n-mcp GitHub](https://github.com/n8n-io/n8n-mcp)

### 関連SSOTドキュメント

- [hadayalab-automation-platform SSOT](./hadayalab-automation-platform-SSOT.md) - プロジェクト全体SSOT
- [n8n + Whop 完全活用戦略 SSOT](./n8n-whop-full-strategy-SSOT.md) - n8n + Whop統合戦略

---

**最終更新**: 2025-12-26
**バージョン**: 1.1.0（ワークフローインポートベストプラクティス追加）
**メンテナー**: HadayaLab

## 🔄 更新履歴

### 2025-12-26 (v1.2.0)
- **ワークフローインポート標準フローを明確化**（実証済み）
  - 環境変数ファイルの確認手順（`.env`または`.env.env`）
  - インポート後の検証手順を追加
  - フォルダへの移動手順を追加（Personal、hadayalab-automation-platform）
  - テストスクリプトの作成と基本動作確認手順を追加
- **役割分担の明確化**
  - Cursorの役割：インポート、検証、テストスクリプト作成
  - 人間の役割：フォルダ移動、認証情報設定、ワークフロー有効化

### 2025-12-26 (v1.1.0)
- **ワークフローインポートベストプラクティスを追加**（実証済み）
  - ノードの存在確認手順
  - ワークフローJSONのクリーンアップ方法
  - n8n APIが受け付けるプロパティの明確化
  - インポートスクリプトの推奨使用方法
  - レスポンスステータスコードの扱い
  - エラーハンドリングの改善
- **トラブルシューティングセクションを大幅拡充**
  - "Install this node to use it"エラーの対処法
  - "Cannot read properties of undefined (reading 'execute')"エラーの対処法
  - n8n APIエラーの対処法（additional properties, read-only properties等）

### 2025-12-26 (v1.0.0)
- 初版作成
- n8n関連のすべてのナレッジをこのSSOTに統合

