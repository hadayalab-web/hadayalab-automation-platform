# Cursor Chatでワークフローが表示されない場合のトラブルシューティング

## 🔍 問題: `@workflows/` でファイルが表示されない

### 原因1: ファイルがGitに追加されていない

**症状**: `@workflows/` と入力しても、ファイルが補完候補に表示されない

**解決方法**:

1. **ファイルをGitに追加**:
   ```bash
   git add workflows/simple-time-check.json
   ```

2. **Cursorを再起動**:
   - Cursorを完全に終了して再起動
   - または、`Cmd+Shift+P` (Mac) / `Ctrl+Shift+P` (Windows) → "Reload Window"

3. **ファイルを直接開く**:
   - `workflows/simple-time-check.json` を一度開いて、Cursorに認識させる

### 原因2: Cursorのインデックスが更新されていない

**症状**: ファイルは存在するが、補完候補に表示されない

**解決方法**:

1. **ファイルを直接開く**:
   ```
   workflows/simple-time-check.json を開いて
   ```

2. **ファイルエクスプローラーで確認**:
   - 左パネルのファイルエクスプローラーで `workflows/` ディレクトリを確認
   - ファイルが表示されているか確認

3. **Cursorを再起動**:
   - Cursorを完全に終了して再起動

### 原因3: ファイルパスが正しく認識されていない

**症状**: `@workflows/` と入力しても、何も表示されない

**解決方法**:

1. **完全なパスで指定**:
   ```
   @workflows/simple-time-check.json
   ```

2. **相対パスで指定**:
   ```
   workflows/simple-time-check.json を参照して
   ```

3. **ワークフローインデックスを参照**:
   ```
   @workflows/workflow-index.md を参照して
   ```

## ✅ 推奨される使用方法

### 方法1: ファイルパスを直接指定（最も確実）

```
@workflows/simple-time-check.json を検証して
```

### 方法2: ワークフローインデックスを参照

```
@workflows/workflow-index.md を参照して、simple-time-checkワークフローの情報を表示して
```

### 方法3: n8n-mcpパッケージで検索

```
@n8n-local simple-time-checkワークフローを検索して
```

## 🔧 確認手順

### ステップ1: ファイルの存在確認

```bash
ls workflows/simple-time-check.json
# または
Get-ChildItem workflows/simple-time-check.json
```

### ステップ2: Gitの状態確認

```bash
git status workflows/simple-time-check.json
```

### ステップ3: ファイルを開いて確認

Cursorで `workflows/simple-time-check.json` を直接開いて、内容が表示されるか確認

### ステップ4: Cursor Chatで試す

```
@workflows/simple-time-check.json を検証して
```

## 📝 新しいワークフローを追加した場合

新しいワークフローを追加したら、以下を実行してください：

1. **ファイルをGitに追加**:
   ```bash
   git add workflows/新しいワークフロー名.json
   ```

2. **ワークフローインデックスを更新**:
   - `workflows/workflow-index.md` に新しいワークフローを追加
   - `workflows/README.md` を更新

3. **Cursorを再起動**（必要に応じて）

## 🎯 ベストプラクティス

### 1. ファイルをGitに追加する

新しいワークフローを作成したら、必ずGitに追加してください：

```bash
git add workflows/新しいワークフロー名.json
```

### 2. ワークフローインデックスを活用

`@workflows/workflow-index.md` を参照することで、すべてのワークフローを確認できます。

### 3. 完全なファイルパスを使用

補完が機能しない場合は、完全なファイルパス（`@workflows/xxx.json`）を直接指定してください。

## 🔗 関連ドキュメント

- [Cursor Chatでワークフローをメンションする方法](./cursor-workflow-mention-guide.md)
- [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)

---

**最終更新**: 2025-01-24















