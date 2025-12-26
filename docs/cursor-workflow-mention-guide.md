# Cursor Chatでワークフローをメンションする方法

## 📋 概要

このガイドでは、Cursor Chatでワークフローをメンションして参照・操作する方法を説明します。

## 🎯 ワークフローのメンション方法

### 方法1: ファイルパスで直接参照（推奨）

```
@workflows/simple-time-check.json を検証して
@workflows/simple-time-check.json をn8n Cloudにインポートして
```

**メリット**:
- ✅ 正確なファイルを指定できる
- ✅ Cursorが自動的にファイルを読み込む
- ✅ ファイル内容を直接参照できる

### 方法2: ワークフロー名で参照

```
@simple-time-check ワークフローを検索して
@simple-time-check ワークフローを実行して
```

**メリット**:
- ✅ 短い名前で参照できる
- ✅ 覚えやすい

**注意**: この方法は、n8n-mcpパッケージの検索機能を使用します。

### 方法3: ワークフローインデックスを参照

```
@workflows/workflow-index.md を参照して、利用可能なワークフローを表示して
```

**メリット**:
- ✅ すべてのワークフローを一覧で確認できる
- ✅ ワークフローの説明と機能を確認できる

## 📚 実践例

### 例1: ワークフローの検証

```
@workflows/simple-time-check.json を検証して、エラーがないか確認して
```

### 例2: ワークフローの作成

```
@workflows/simple-time-check.json をn8n Cloudにインポートして作成して
```

### 例3: ワークフローの実行

```
@n8n-cloud simple-time-checkワークフローを実行して
```

### 例4: ワークフローの更新

```
@workflows/simple-time-check.json を参照して、HTTP RequestノードのURLを変更して、n8n Cloudに更新して
```

### 例5: ワークフロー一覧の確認

```
@workflows/workflow-index.md を参照して、現在利用可能なワークフローを一覧表示して
```

## 🔍 ワークフローの検索

### ファイル名で検索

```
@workflows で「time」を含むワークフローを検索して
```

### 機能で検索

```
@workflows で「時刻取得」に関連するワークフローを検索して
```

### タグで検索

```
@workflows で「test」タグが付いているワークフローを検索して
```

## 🎯 ベストプラクティス

### 1. ファイルパスでの参照を優先

ワークフローを操作する際は、ファイルパス（`@workflows/xxx.json`）で直接参照することを推奨します。

**理由**:
- Cursorが自動的にファイルを読み込む
- ファイル内容を直接参照できる
- より正確な操作が可能

### 2. ワークフロー名は一意にする

ワークフロー名は、他のワークフローと重複しないようにします。

**推奨命名規則**:
- `kebab-case`を使用（例: `simple-time-check`）
- 機能を表す名前を使用（例: `slack-notification`, `data-processing`）

### 3. ワークフローインデックスを更新

新しいワークフローを追加したら、必ず `workflows/workflow-index.md` を更新します。

### 4. タグを活用

ワークフローに適切なタグを付けることで、検索しやすくなります。

**推奨タグ**:
- `test`: テスト用ワークフロー
- `production`: 本番環境用ワークフロー
- `experiment`: 実験用ワークフロー
- `mcp`: MCP関連ワークフロー

## 📝 ワークフローインデックスの更新方法

新しいワークフローを追加したら、`workflows/workflow-index.md` に以下を追加：

```markdown
### @新しいワークフロー名
- **ファイル**: `workflows/新しいワークフロー名.json`
- **説明**: ワークフローの説明
- **機能**: ワークフローの機能
- **タグ**: tag1, tag2
- **参照方法**: `@workflows/新しいワークフロー名.json` または `@新しいワークフロー名`
```

## 🔗 関連ドキュメント

- [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)
- [n8n Cloud同期運用](./n8n-cloud-sync.md)
- [ワークフロー命名規約](./workflow-conventions.md)
- [簡単なワークフロー実験ガイド](./simple-workflow-experiment-guide.md)

---

**最終更新**: 2025-01-24
















