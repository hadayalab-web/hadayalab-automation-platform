# hadayalab-automation-platform

HadayaLab Automation Platform - MCP統合型ワークフロー自動化プラットフォーム（SSOT）

## 🎯 概要

[hadayalab.app.n8n.cloud](https://hadayalab.app.n8n.cloud) の
ワークフローをGitHubで一元管理します。

- **実行環境**: n8n Cloud
- **開発**: Cursor + n8n-mcp
- **レビュー**: GitHub Copilot Pro
- **検証**: GitHub Actions（自動）
- **同期**: 手動Import（Phase 1） / 自動デプロイ（Phase 2計画中）

## 運用方針

このリポジトリはGitHubをSSOTとして運用します。
- **標準**: GitHub → n8n Cloud（一方向）
- **例外**: Cloud UI編集時は取り込み手順を実施
- **詳細**: [docs/n8n-cloud-sync.md](./docs/n8n-cloud-sync.md) 参照

## 📚 ドキュメント

- **[hadayalab-automation-platform SSOT](./docs/hadayalab-automation-platform-SSOT.md)** - プロジェクト全体の唯一の信頼できる情報源（**最初に参照**）
- **[n8n MCP機能比較 SSOT](./docs/n8n-mcp-capabilities-comparison-SSOT.md)** - n8nネイティブMCPとn8n-mcpパッケージの機能と制限の完全ガイド（**MCP機能確認時に参照**）
- [GitHub Copilot Proセットアップ](./docs/github-copilot-setup.md) - GitHub Copilot連携のセットアップ（**GitHub Copilot連携開始時に参照**）
- [GitHub Copilot タスク一覧](./docs/github-copilot-tasks.md) - GitHub Copilotに任せられる具体的なタスク（**GitHub Copilot活用時に参照**）
- [Cursor + GitHub Copilot連携](./docs/cursor-copilot-integration.md) - 連携ワークフロー
- [Cursor-Vercel連携](./docs/cursor-vercel-integration.md) - CursorからVercelを制御する方法（**新規追加**）
- [n8n Cloud同期運用](./docs/n8n-cloud-sync.md)
- [ワークフロー命名規約](./docs/workflow-conventions.md)
- [ドキュメント一覧](./docs/README.md)

## 🚀 クイックスタート

### 依存関係インストール
```bash
npm install
```

### JSON整形
```bash
npm run format
```

### JSON検証
```bash
npm run format:check
```


## 📁 ディレクトリ構成

```
hadayalab-automation-platform/
├── workflows/ # n8nワークフローJSON（SSOT）
├── docs/ # 運用ドキュメント
├── scripts/ # ユーティリティスクリプト
│   ├── vercel_control.py # Vercel API制御スクリプト
│   └── vercel_control_example.* # 使用例スクリプト
├── workflow-cursor-vercel-control.json # Cursor-Vercel連携ワークフロー
└── .github/workflows/ # CI/CD
```

## 🔗 リンク

- [n8n Cloud](https://hadayalab.app.n8n.cloud)
- [n8n-mcp](https://www.npmjs.com/package/n8n-mcp)
- [HadayaLab](https://github.com/hadayalab-web)

## トラブルシューティング

### MCP サーバー エラーハンドリング

#### JSON パース エラー

**症状：**
```
[error] Client error for command Unexpected token '',' in '"additi"...'
```

**対応：**

1. n8n-mcp バージョン確認：`npm list n8n-mcp`
2. v2.28.7 へアップグレード：`npm install n8n-mcp@2.28.7`
3. MCP サーバー再起動
4. Cursor 再起動

詳細は [docs/hadayalab-automation-platform-SSOT.md](./docs/hadayalab-automation-platform-SSOT.md) の「3. n8n-mcp の活用」を参照


