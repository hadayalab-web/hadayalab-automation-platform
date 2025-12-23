# hadayalab-automation-platform SSOT（Single Source of Truth）

このドキュメントは、hadayalab-automation-platformプロジェクト全体の**唯一の信頼できる情報源**として機能します。

## 1. プロジェクト概要

- **プロジェクト名**: hadayalab-automation-platform
- **目的**: MCP統合型ワークフロー自動化プラットフォーム
- **リポジトリ**: https://github.com/hadayalab-web/hadayalab-automation-platform
- **実行環境**: n8n Cloud (https://hadayalab.app.n8n.cloud)

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

## 3. n8n-mcp の活用（543個ノード × 2,700+テンプレート）

### n8n-mcp とは

n8n-mcp（Model Context Protocol）は、n8nが提供する強力なツールであり、
本プロジェクトの自動化基盤の核となるコンポーネントです。

**mcp.json 設定によって実装済み** となっており、以下の能力を持ちます：

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

### 実装担当
- **Cursor**: ワークフロー作成・編集の実装ツール
  - コード生成・編集
  - リファクタリング
  - バグ修正
  - 新機能実装

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
- **Cursor + GitHub Copilot連携**: 実装からレビューまで一貫したワークフロー
  - 詳細: [Cursor + GitHub Copilot連携ガイド](./cursor-copilot-integration.md)

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

1. Cloud UIで編集実施
2. 直後にExport（JSONダウンロード）
3. `workflows/`へ保存（命名規約準拠）
4. `npm run format`（自動整形）
5. GitHubへpush（取り込み）
6. 以降GitHubを正とする

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
- **docs/hadayalab-automation-platform-SSOT.md**: プロジェクト全体SSOT（このファイル）
- **docs/n8n-cloud-sync.md**: GitHub⇔n8n Cloud同期詳細
- **docs/workflow-conventions.md**: ワークフロー命名規約
- **docs/README.md**: ドキュメント一覧

### ドキュメントの役割

| ドキュメント | 役割 |
|------------|------|
| README.md | プロジェクトの入り口、概要とクイックスタート |
| hadayalab-automation-platform-SSOT.md | プロジェクト全体の真実の唯一の情報源 |
| n8n-cloud-sync.md | 同期運用の詳細手順 |
| workflow-conventions.md | 命名規約と構造ルール |

## 9. 参照リンク

### 内部ドキュメント

- [n8n Cloud同期運用](./n8n-cloud-sync.md)
- [ワークフロー命名規約](./workflow-conventions.md)
- [ドキュメント一覧](./README.md)

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

**最終更新**: 2025-12-23
**バージョン**: 1.0.0
**メンテナー**: HadayaLab

