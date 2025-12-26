# n8n Workflows Index

このファイルは、Cursor Chatでワークフローをメンションするためのインデックスです。

## 📋 ワークフロー一覧

### @simple-time-check
- **ファイル**: `workflows/simple-time-check.json`
- **説明**: 簡単な実験用ワークフロー（現在時刻取得）
- **機能**: Webhook TriggerでHTTPリクエストを受け取り、World Time APIから東京の現在時刻を取得してJSONで返す
- **タグ**: test, experiment, simple
- **参照方法**: `@workflows/simple-time-check.json` または `@simple-time-check`

### @manual-hello-world-test
- **ファイル**: `workflows/manual-hello-world-test.json`
- **説明**: MCPテスト用ワークフロー
- **機能**: Manual Triggerで「Hello from n8n-mcp!」メッセージを返す
- **タグ**: test, mcp, validated
- **参照方法**: `@workflows/manual-hello-world-test.json` または `@manual-hello-world-test`

## 🔍 Cursor Chatでの使用方法

### ワークフローを参照する

```
@workflows/simple-time-check.json を検証して
@workflows/simple-time-check.json をn8n Cloudにインポートして
@simple-time-check ワークフローを実行して
```

### ワークフロー一覧を確認する

```
@workflows/workflow-index.md を参照して、利用可能なワークフローを表示して
```

### ワークフローを検索する

```
@workflows で「時刻」に関連するワークフローを検索して
```

## 📝 新しいワークフローの追加方法

1. `workflows/` ディレクトリにワークフローJSONファイルを作成
2. このファイル（`workflow-index.md`）に新しいワークフローを追加
3. ワークフロー名、説明、機能、タグを記載
4. 参照方法を記載

## 🎯 ワークフロー命名規則

- ファイル名: `kebab-case`（例: `simple-time-check.json`）
- ワークフロー名: ファイル名と同じ（JSON内の`name`フィールド）
- メンション名: `@` + ファイル名（拡張子なし）

---

**最終更新**: 2025-01-24















