# hadayalab-automation-platform SSOT（Single Source of Truth）

このドキュメントは、hadayalab-automation-platformプロジェクト全体の**唯一の信頼できる情報源**として機能します。

## 1. プロジェクト概要

- **プロジェクト名**: hadayalab-automation-platform
- **位置づけ**: 🏛️ **戦略本部** - 戦略立案・ワークフロー設計・自動化基盤の統合管理
- **目的**: MCP統合型ワークフロー自動化プラットフォーム
- **リポジトリ**: https://github.com/hadayalab-web/hadayalab-automation-platform
- **実行環境**: n8n Cloud (https://hadayalab.app.n8n.cloud)

### 3プロジェクト連携構造

```
🏛️ 戦略本部: hadayalab-automation-platform（このプロジェクト）
    ├── 📦 プロダクト: cryptosignal-ai
    └── 📚 ナレッジベース: hadayalab-knowledge-base
```

**役割分担**:
- **戦略本部**: 戦略立案・ワークフロー設計・自動化基盤の統合管理
- **プロダクト**: コアシステム実装・実行（Vercelデプロイ、Telegram配信）
- **ナレッジベース**: 理論文献・戦略文献の一元管理・提供

## 2. SSOT原則

### ドキュメント優先順位

本書（hadayalab-automation-platform-SSOT.md）がプロジェクト全体の最高位ドキュメントです。

矛盾がある場合の優先順位：

1. **本書（hadayalab-automation-platform-SSOT.md）** - プロジェクト全体方針
2. **n8n-cloud-sync.md** - 同期フロー詳細手順
3. **workflow-conventions.md** - 命名規約・コーディング規約

### GitHubがSSOT

- **GitHubが唯一の信頼できる情報源（Single Source of Truth）**
- すべての変更はGitHubを起点とする
- n8n Cloud UIは動作確認・モニタリング用途のみ

### SSOTの重要性

- ワークフローの真実の状態は常にGitHubリポジトリに存在
- n8n Cloudは実行環境であり、ソース管理ではない
- 変更の追跡・レビュー・ロールバックはすべてGitHubで実施

## 3. n8n MCP の活用（543個ノード × 2,700+テンプレート）

### 🎯 設計方針：すべてのn8nワークフローをCursor UIから制御

**重要な仕様**: **n8nのワークフローはすべてCursorのUIから制御できる仕様にする**

この設計方針により、以下のメリットが実現されます：

- ✅ **統一された開発環境**: n8n Dashboardへの切り替え不要
- ✅ **コンテキストの維持**: Cursor内で完結するワークフロー管理
- ✅ **効率的な開発**: Cursor Chatから直接n8nワークフローを操作
- ✅ **自動化の推進**: AIエージェントによるワークフロー自動生成・管理

#### 実装方法

**2つのMCP実装方法**を組み合わせて、すべてのn8nワークフロー操作をCursor UIから実行可能：

1. **n8nネイティブMCP**（supergateway経由）- **有料プランでほとんどのオペレーションが可能**
2. **n8n-mcpパッケージ** - ワークフロー作成・編集・削除・ノード検索・テンプレート検索に特化

**重要**: n8nを有料プランにすると、ネイティブのn8n-MCPでほとんどのオペレーションができるようになります。これにより、より統一的で強力な制御が可能になります。

**詳細**: [n8n完全統合SSOT](./n8n-complete-SSOT.md) を参照（**すべてのn8n関連情報を統合**）

**mcp.json 設定によって実装済み** となっており、以下の能力を持ちます：

#### Cursor UIから実行可能な操作

| 操作 | 使用するMCP | Cursor Chatコマンド例 |
|------|------------|---------------------|
| **ワークフロー作成** | n8n-mcpパッケージ | `@n8n-local 新しいワークフローを作成して` |
| **ワークフロー更新** | n8n-mcpパッケージ | `@n8n-local workflow.jsonを更新して` |
| **ワークフロー削除** | n8n-mcpパッケージ | `@n8n-local ワークフローIDを削除して` |
| **ワークフロー実行** | n8nネイティブMCP | `@n8n-cloud ワークフローを実行して` |
| **実行履歴確認** | n8nネイティブMCP | `@n8n-cloud 実行履歴を表示して` |
| **環境変数管理** | n8nネイティブMCP | `@n8n-cloud 環境変数を設定して` |
| **ノード検索** | n8n-mcpパッケージ | `@n8n-local HTTP Requestノードを検索して` |
| **テンプレート検索** | n8n-mcpパッケージ | `@n8n-local Slack通知テンプレートを検索して` |
| **ワークフロー検証** | n8n-mcpパッケージ | `@n8n-local workflow.jsonを検証して` |

#### 禁止事項

- ❌ **n8n Dashboardでの直接編集は原則禁止**（緊急時のみ例外）
- ❌ **n8n Dashboardでのワークフロー作成は原則禁止**（緊急時のみ例外）
- ⚠️ **緊急時は例外フロー（Cloud→GitHub取り込み）を実施**（[n8n Cloud同期運用](./n8n-cloud-sync.md)参照）

### 利用可能なリソース

#### 📊 543個の n8n ノード
- HTTP Request、Code、データ処理ノード
- Slack、Gmail、Google Drive、Salesforce、Stripe、HubSpot、Jira、GitHub 等
- PostgreSQL、MySQL、MongoDB、Snowflake、BigQuery
- OpenAI、Claude、Gemini、LangChain 等

#### 📚 2,700+ ワークフロー テンプレート
- CRM自動化、マーケティング自動化、営業支援
- HR・採用、財務・会計、カスタマーサポート
- データ分析、開発者向けツール

#### 🔧 42個の主要ツール
- list_node_templates: ノード検索
- search_templates: テンプレート検索
- validate_workflow: ワークフロー検証
- create_workflow: ワークフロー作成
- execute_workflow: オンデマンド実行

### 本プロジェクトでの活用

#### 標準フロー（GitHub → Cloud）での役割

```
GitHub に .json push
↓
GitHub Actions トリガー
↓
npm run format（Prettier 整形）
↓
n8n-mcp: validate_workflow（543個ノード検証）
↓
n8n Cloud 自動反映
↓
Slack 通知
```

#### 拡張機会

1. **ワークフロー テンプレート ライブラリ化**
   - workflows/templates/ 配下に 2,700+テンプレートから選別した
     ベストプラクティスを集約
   - 命名規約に従いカスタマイズして管理

2. **AI Agent 統合**
   - Claude Desktop → n8n-mcp → ワークフロー自動生成
   - 「このデータを処理して」→ ワークフロー自動実装
   - docs/n8n-cloud-sync.md の標準フロー自動実行

3. **ノード検索スクリプト自動化**
   - n8n-mcp の 543個ノードから最適な組み合わせを推奨
   - 2,700+テンプレートから参考実装を抽出
   - GitHub CLI 連携で自動提案

### 重要な注意事項

- mcp.json は ~/.cursor/mcp.json に配置（環境依存）
- N8N_API_URL と N8N_API_KEY は環境変数で管理（JSON 非含有）
- 同期検証は GitHub Actions 経由で自動実行（手動実行不要）
- 543個ノードのうち利用するものは docs/workflow-conventions.md で指定

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

#### n8n-mcp バージョン管理

**現在の推奨バージョン：v2.28.7（2025-12-23 リリース）**

##### バージョン情報（2025年12月23日時点）

- 最新安定版：v2.28.7
- ノード対応数：543個（前版比 +8）
- テンプレート：2,700+（最新版）
- パフォーマンス：~12ms 平均応答時間
- 新機能：Workflow Diff Operations（80-90% トークン削減）

##### n8n 本体との互換性

| n8n バージョン | 互換性 | 備考 |
|--------------|------|------|
| v2.0.3以上 | ✅ 完全対応 | 最新安定版推奨 |
| v1.120.0+ | ✅ 完全対応 | 推奨版 |
| v1.100.0+ | ✅ 対応 | OK |

##### 既知の問題と対策

**JSON パース エラー（2025年12月23日確認）**

症状：
```
[error] Client error for command Unexpected token '',' in '"additi"...'
[error] "additi"... is not valid JSON
```

原因：
- n8n-mcp のレスポンス形式と Cursor JSON パーサーの不一致
- 表示層のみの問題で実機能に支障なし

対策：
- ✅ v2.28.7 へのアップグレード推奨
- ✅ MCP サーバー再起動（`docker restart n8n-mcp`）
- ✅ Cursor 再起動

効果：
- JSON パースエラー の解消予定
- 543個ノード対応（前版535個 → 2.28.7で543個）
- Diff-based updates による効率化（80-90% トークン削減）

##### アップグレード手順

1. **npm パッケージ更新**
   ```bash
   npm install n8n-mcp@2.28.7
   ```

2. **Docker イメージ更新（Docker利用の場合）**
   ```bash
   docker pull ghcr.io/czlonkowski/n8n-mcp:latest
   docker-compose up -d
   ```

3. **MCP サーバー再起動**
   ```bash
   pkill -f n8n-mcp
   ```

4. **Cursor 再起動**
   - Cursor をいったん閉じて再起動

##### バージョン確認方法

**インストール済みバージョン確認**
```bash
npm list n8n-mcp
```

期待される出力：
```
n8n-mcp@2.28.7
```

##### 次回アップグレード計画

- **確認周期**：毎月第1週に最新版確認
- **アップグレード実施**：安定版リリース後1週間以内
- **本体アップグレード**：n8n 安定版リリース後1週間以内

### 次フェーズの検討事項

現在の実装で十分な運用は可能ですが、以下の拡張を検討可能：

- ワークフロー テンプレート ライブラリの体系化（優先度：中）
- Claude との完全統合（優先度：中）
- ワークフロー自動生成ツール（優先度：低）

詳細は本プロジェクトのマイルストーンを参照してください。

## 4. 開発環境

### 役割分担

#### 人間の役割: n8n Cloud UIでのインポート・エクスポート操作のみ

- ✅ n8n Cloud UIでのインポート・エクスポート操作

#### Cursorの役割: それ以外すべて（GitHubへのコミット・プッシュを含む）

- ✅ ワークフローの作成・編集
- ✅ コード生成・リファクタリング
- ✅ バグ修正
- ✅ テスト実行
- ✅ **GitHubへのコミット・プッシュ（CursorはGitHubにシームレスにつながっているため自動実行）**

**原則**: CursorはGitHubにシームレスにつながっているため、ワークフローの作成・編集後は自動的にGitHubにコミット・プッシュする

### 実装担当
- **Cursor**: ワークフロー作成・編集の実装ツール
  - コード生成・編集
  - リファクタリング
  - バグ修正
  - 新機能実装
  - GitHubへのコミット・プッシュ（自動実行）

### レビュー担当
- **GitHub Copilot Pro**: コードレビュー・品質保証
  - コードレビュー
  - プロジェクト全体分析
  - アーキテクチャ設計提案
  - Issue/PR管理

### ツール連携
- **n8n-mcp**: GitHub ⇔ n8n Cloud同期ツール
  - 設定: `~/.cursor/mcp.json`
  - 参考: `.env.example`
  - ⚠️ **重要**: APIキーは`.env`ファイル（`C:\Users\chiba\hadayalab-automation-platform\.env`）に格納されている
- **Cursor + GitHub Copilot連携**: 実装からレビューまで一貫したワークフロー
  - 詳細: [Cursor + GitHub Copilot連携ガイド](./cursor-copilot-integration.md)

### 環境変数とシークレット管理

**ローカル開発環境**:
- ✅ **`.env`ファイル**: `C:\Users\chiba\hadayalab-automation-platform\.env`
  - ローカル開発で使用するすべてのAPIキーと認証情報を格納
  - `.gitignore`に含まれており、Gitにコミットされない
  - 機密情報のため共有禁止

**本番環境（n8n Cloud）**:
- ✅ **n8n Cloud環境変数**: n8n Cloud Dashboardで管理
- ✅ **Infisical**: シークレット一元管理（推奨）

**重要な運用ルール**:
1. `.env`ファイルはプロジェクトルートに配置（`C:\Users\chiba\hadayalab-automation-platform\.env`）
2. 新しいAPIキー取得後は`.env`ファイルに追加
3. `.env`ファイルのバックアップは安全な場所に保管
4. チーム共有時は`.env`ファイルを直接共有せず、Infisicalなどを使用

## 5. ワークフロー管理運用

### 標準フロー（GitHub → n8n Cloud）

詳細は [n8n Cloud同期運用](./n8n-cloud-sync.md) を参照
※「標準フロー（GitHub→Cloud）」セクションを参照

1. Cursorでワークフロー編集
2. ローカル検証
   - `npm run format`（自動整形）
   - `npm run format:check`（確認）
3. GitHubへpush
4. GitHub Actions自動検証
   - ※push後、GitHub Actionsが自動実行されgreenになることを確認してから次のステップへ（推奨）
5. n8n-mcp経由でCloud反映
6. Cloud UIで動作確認

### 例外フロー（Cloud → GitHub取り込み）

詳細は [n8n Cloud同期運用](./n8n-cloud-sync.md) を参照
※「例外フロー（Cloud→GitHub取り込み）」セクションを参照

緊急時にCloud UIで編集した場合の手順:

1. **Cloud UIで編集実施**（手動・人間の役割）
2. **直後にExport（JSONダウンロード）**（手動・人間の役割）
3. **`workflows/`へ保存（命名規約準拠）**（Cursorの役割・自動実行）
4. **`npm run format`（自動整形）**（Cursorの役割・自動実行）
5. **GitHubへpush（取り込み・自動実行）**（Cursorの役割・自動実行、CursorはGitHubにシームレスにつながっているため）
6. **以降GitHubを正とする**

### 命名規約

詳細は [ワークフロー命名規約](./workflow-conventions.md) を参照

- ファイル名規則: `<category>-<purpose>[-version].json`
- カテゴリ: `webhook`, `schedule`, `manual`, `email`
- タグ運用: `test`, `production`, `mcp`, `draft`

## 6. 品質保証

### GitHub Actions

- **ワークフローJSON検証**: Prettierフォーマットチェック
- **JSON構文検証**: jqによる構文検証
- **自動実行**: `workflows/**/*.json` 変更時に自動実行

### Prettier

- **差分可読性向上**: 一貫したフォーマットで差分を読みやすく
- **自動整形**: `npm run format` で自動整形
- **CI検証**: `npm run format:check` でCI検証

### レビュープロセス

1. **Cursor実装**: ワークフロー作成・編集
2. **Copilot先生レビュー**: コードレビュー・品質保証
3. **GitHub Actions**: 自動検証
4. **マージ**: レビュー通過後マージ

## 7. 重要な運用原則

### 同時編集禁止

- **同じワークフローをCloudとGitHub両方で同時編集禁止**
- 編集前に必ずGitHubの最新状態を確認
- 競合を防ぐため、編集権限を明確化

### UI編集後の取り込み

- **UI編集後は必ず取り込みコミット作成**
- Export → 整形 → push の手順を厳守
- 取り込みコミットメッセージに `"Import from Cloud:"` プレフィックス

### Credentials/Secrets管理

- **Credentials/Secretsは環境依存（JSON非含有）**
- JSONファイルには含まれない
- Import後、手動で設定が必要

#### ローカル開発環境でのシークレット管理

**`.env`ファイルによるキー管理**:
- ✅ ローカル開発環境では`.env`ファイル（`C:\Users\chiba\hadayalab-automation-platform\.env`）にAPIキーを格納
- ✅ `.env`ファイルは`.gitignore`に含まれており、Gitにコミットされない
- ✅ スクリプトやMCPサーバーは`.env`ファイルから環境変数を読み込む

**`.env`ファイルの役割**:
- ローカル開発時のAPIキー管理
- MCPサーバー設定時の認証情報提供
- スクリプト実行時の環境変数設定

**注意事項**:
- `.env`ファイルは機密情報を含むため、共有禁止
- 新しい環境でのセットアップ時は、Infisicalまたはn8n Cloud環境変数から必要なキーを取得して`.env`ファイルに設定
- `.env`ファイルのバックアップは安全な場所に保管

### Import/Deployの違い

- **Import（UI）＝デプロイ**: n8n Cloud UIでの「Import」は上書き（デプロイ）
- **取り込み＝Export→GitHub push**: Cloud変更のGitHub反映は必ずExport→取り込み手順を実施

### Export JSONの特性

- Export時にメタデータ（updatedAt等）含有
- 差分が荒れるのは仕様
- Prettierで整形されるが、重要な変更のみに注目

## 8. ドキュメント構造

### 主要ドキュメント

- **README.md**: プロジェクト概要と運用方針
- **docs/SSOT/hadayalab-automation-platform-SSOT.md**: プロジェクト全体SSOT（このファイル）
- **docs/setup/n8n-cloud-sync.md**: GitHub⇔n8n Cloud同期詳細
- **docs/workflows/workflow-conventions.md**: ワークフロー命名規約
- **docs/README.md**: ドキュメント一覧

### ドキュメントの役割

| ドキュメント | 役割 |
|------------|------|
| README.md | プロジェクトの入り口、概要とクイックスタート |
| hadayalab-automation-platform-SSOT.md | プロジェクト全体の真実の唯一の情報源 |
| n8n-whop-full-strategy-SSOT.md | n8n + Whop完全活用戦略（SSOT） ⭐ 新規追加 |
| n8n-cloud-sync.md | 同期運用の詳細手順 |
| workflow-conventions.md | 命名規約と構造ルール |

### ドキュメント構造（2025-12-26更新）

```
docs/
├── SSOT/                          # SSOTドキュメント（最優先参照）
│   ├── hadayalab-automation-platform-SSOT.md
│   ├── n8n-mcp-capabilities-comparison-SSOT.md
│   ├── n8n-whop-full-strategy-SSOT.md
│   ├── n8n-workflow-full-control-SSOT.md
│   ├── workflow-sync-status-SSOT.md
│   └── whop-control-workflow-SSOT.md
│
├── workflows/                     # ワークフロー設計・実装
│   ├── n8n-workflows-design.md
│   ├── workflow-conventions.md
│   └── workflow-test-guide.md
│
├── setup/                         # セットアップガイド
│   ├── n8n-cloud-sync.md
│   ├── n8n-mcp-setup-complete.md
│   └── api-keys-setup.md
│
├── api-integration/               # API統合関連
│   ├── api-integration-implementation-plan.md
│   ├── api-integration-progress.md
│   └── WHOP_API_CAPABILITIES_COMPLETE.md
│
├── troubleshooting/               # トラブルシューティング
│   └── n8n-workflow-deletion-guide.md（統合版）
│
└── archive/                       # アーカイブ（古い・重複ドキュメント）
    └── n8n-workflow-deletion-*.md（統合済み）
```

## 9. 参照リンク

### 内部ドキュメント

#### SSOTドキュメント（最優先参照）

- **[n8n + Whop 完全活用戦略 SSOT](./n8n-whop-full-strategy-SSOT.md)** - **n8n + Whop完全統合戦略（SSOT）** ⭐ 新規追加
- [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md) - **n8n MCP機能の完全ガイド（SSOT）**
- [whop-control-workflow SSOT](./whop-control-workflow-SSOT.md) - Whop制御ワークフローのSSOT
- [n8nワークフロー完全制御 SSOT](./n8n-workflow-full-control-SSOT.md) - ワークフロー制御のSSOT
- [ワークフロー同期状況 SSOT](./workflow-sync-status-SSOT.md) - 同期状況のSSOT

#### 実装ガイド

- [n8n Cloud同期運用](../setup/n8n-cloud-sync.md)
- [ワークフロー命名規約](../workflows/workflow-conventions.md)
- [ワークフロー設計](../workflows/n8n-workflows-design.md)
- [API統合実装計画](../api-integration/api-integration-implementation-plan.md)
- [トラブルシューティング](../troubleshooting/n8n-workflow-deletion-guide.md)
- [ドキュメント一覧](../README.md)

### 外部リソース

- [n8n Cloud](https://hadayalab.app.n8n.cloud)
- [n8n-mcp](https://www.npmjs.com/package/n8n-mcp)
- [HadayaLab](https://github.com/hadayalab-web)

### 関連SSOT

- [汎用開発環境SSOT](../Cursor-Pro-GitHub-Copilot-Pro-最強開発環境-SSOT-v3.1.md)（参照先が存在する場合）

## 10. トラブルシューティング

### よくある問題

#### GitHub Actionsが失敗する

1. Prettierフォーマットエラー: `npm run format` で自動整形
2. JSON構文エラー: jqで構文検証
3. パス指定エラー: `workflows/**/*.json` パターンを確認

#### CloudとGitHubで不整合

1. GitHubの最新状態を確認
2. Cloud UIでExportして取り込み
3. 以降GitHubを正とする

#### ワークフローが動作しない

1. Cloud UIで有効化（Activate）確認
2. Credentials設定確認
3. Webhook URL確認

#### Activate状態の確認

- **症状**: ワークフローが実行されない
- **原因**: Import後にInactiveになっている
- **対処**: n8n Cloud UIでワークフローを開き、Activateボタンをクリック

#### Webhook URLの環境依存

- **注意**: Cloud固有のWebhook URLは再生成される
- **対応**: Import後にWebhook URLを確認・更新

## 11. 今後の運用

### 迷ったときは

1. **このSSOTドキュメントを最初に参照**
2. 関連ドキュメントを確認
3. GitHub Copilot先生にレビュー依頼

### 最短判断ツリー

#### Cloud UIで編集してしまった？

- **Yes** → 例外フロー実施（Export→整形→コミット）
- **No** → 標準フロー継続

#### GitHub Actions が red？

- **Fix first（修正が最優先）**
- **redのままCloudへ反映禁止**

#### Credentials関連？

- JSONには含まれない（環境依存）
- `.env` と Cloud UI で個別設定

#### 例外フローを常態化させない

- 緊急時のみ許可（P1障害、期限対応など）
- **原則は標準フロー**

### ドキュメント更新

- SSOT原則に基づき、このドキュメントを最新に保つ
- 運用方針変更時は必ずこのドキュメントを更新
- 更新後はGitHub Copilot先生にレビュー依頼

---

**最終更新**: 2025-12-26
**バージョン**: 1.2.0（.envファイルキー管理情報追加）
**メンテナー**: HadayaLab

## 🔄 更新履歴

### v1.4.0 (2025-12-26)
- **n8n有料プランでのネイティブMCP機能拡張情報を追加**: n8nを有料プランにすると、ネイティブのn8n-MCPでほとんどのオペレーションができるようになることをSSOTに追加

### v1.3.0 (2025-12-26)
- **役割分担の明確化**: CursorはGitHubにシームレスにつながっているため、ワークフローの作成・編集後は自動的にGitHubにコミット・プッシュすることをSSOTに追加
- **人間の役割を最小化**: n8n Cloud UIでのインポート・エクスポート操作のみが人間の役割であることを明確化
- **開発環境セクション更新**: 役割分担セクションを追加し、Cursorの役割にGitHubへのコミット・プッシュを含める

### v1.2.0 (2025-12-26)
- **.envファイルキー管理情報追加**: `.env`ファイル（`C:\Users\chiba\hadayalab-automation-platform\.env`）にAPIキーが格納されていることを重要事項として明記
- **環境変数とシークレット管理セクション追加**: ローカル開発環境と本番環境でのシークレット管理方法を明確化
- **Credentials/Secrets管理セクション拡張**: `.env`ファイルの役割と運用ルールを追加

### v1.1.0 (2025-12-26)
- **ドキュメント整理完了**: カテゴリ別フォルダ構成に再編成
- **SSOTドキュメント移動**: `docs/SSOT/` フォルダに集約
- **重複ドキュメント統合**: ワークフロー削除ガイドを1つに統合
- **参照リンク更新**: 新しいフォルダ構造を反映

### v1.0.0 (2025-12-23)
- 初版作成

