# n8nワークフローインポートベストプラクティス（実証済み）

**作成日**: 2025-12-26
**最終更新**: 2025-12-26
**目的**: ワークフローインポート時のエラーと解決策をまとめたベストプラクティス

---

## 🔍 今回遭遇したエラーと解決策

### エラー1: "Install this node to use it" / "Node is not currently installed"

**エラーメッセージ**:
```
This node is not currently installed. It is either from a newer version of n8n, a custom node, or has an invalid structure.
```

**原因**: 存在しないノードタイプがワークフローに含まれている

**解決策**:
1. **ノードの存在確認**: ワークフロー作成前にn8n-MCPパッケージでノード検索を行い、存在確認
   ```
   @n8n-local Google Docsノードを検索して
   ```
2. **標準ノードか確認**: `n8n-nodes-base.*` が標準ノード
3. **存在しないノードは削除**: 今回は `n8n-nodes-base.googleDocs` が存在しないため削除

**ベストプラクティス**:
- ✅ ワークフロー作成前に使用するノードが存在するか確認
- ✅ 標準ノードリストを参照（543個のノード）
- ✅ 存在しないノードは削除するか、代替手段（HTTP Requestノード等）を使用

---

### エラー2: "Cannot read properties of undefined (reading 'execute')"

**エラーメッセージ**:
```
Cannot read properties of undefined (reading 'execute')
```

**原因**: 認証情報が設定されていない、またはノードがインストールされていない

**解決策**:
1. 各ノードで認証情報が選択されているか確認
2. ノードが正しくインストールされているか確認
3. 存在しないノードタイプを使用していないか確認

**ベストプラクティス**:
- ✅ インポート後、必ず各ノードの認証情報を設定
- ✅ ノードの存在確認を先に行う

---

### エラー3: "request/body must NOT have additional properties"

**エラーメッセージ**:
```
{"message":"request/body must NOT have additional properties"}
```

**原因**: n8n APIが受け付けないプロパティがワークフローJSONに含まれている

**解決策**: n8n APIが受け付けるプロパティのみを保持

**n8n APIが受け付けるプロパティ**:
- ✅ `name` - ワークフロー名（必須）
- ✅ `nodes` - ノード配列（必須）
- ✅ `connections` - 接続情報（必須）
- ✅ `settings` - 設定（オプション）

**削除すべきプロパティ**:
- ❌ `versionId` - APIが自動生成
- ❌ `updatedAt` - APIが自動生成
- ❌ `triggerCount` - APIが自動生成
- ❌ `tags` - 読み取り専用（作成時は含めない）
- ❌ `pinData` - 作成時は不要
- ❌ `staticData` - 作成時は不要
- ❌ `id` - 新規作成時は不要
- ❌ `createdAt` - APIが自動生成
- ❌ `isArchived` - APIが自動生成
- ❌ `versionCounter` - APIが自動生成

**ベストプラクティス**:
- ✅ インポートスクリプトで自動的にクリーンアップする（`scripts/import-workflow-to-n8n.py`参照）

---

### エラー4: "request/body/tags is read-only"

**エラーメッセージ**:
```
{"message":"request/body/tags is read-only"}
```

**原因**: `tags`プロパティをワークフロー作成時に含めようとした

**解決策**: ワークフロー作成時は`tags`を含めず、作成後にn8n Dashboardで手動設定するか、更新APIを使用

**ベストプラクティス**:
- ✅ ワークフロー作成時は`tags`を含めない
- ✅ 作成後にn8n Dashboardでタグを設定

---

## 🎯 ワークフローインポートベストプラクティス（実証済み）

### 1. ノードの存在確認

**推奨フロー**:
1. ワークフロー作成前に、使用するノードが存在するか確認
2. n8n-MCPパッケージでノード検索を実行

```
@n8n-local [ノード名]ノードを検索して
```

**例**:
- ❌ `n8n-nodes-base.googleDocs` - 標準ノードではない（存在しない）
- ✅ `n8n-nodes-base.gmail` - 標準ノード（存在する）
- ✅ `n8n-nodes-base.googleSheets` - 標準ノード（存在する）
- ✅ `n8n-nodes-base.googleDrive` - 標準ノード（存在する）
- ✅ `n8n-nodes-base.googleCalendar` - 標準ノード（存在する）

---

### 2. ワークフローJSONのクリーンアップ

**推奨**: インポートスクリプトを使用（`scripts/import-workflow-to-n8n.py`）

**手動クリーンアップ例**:

```python
# n8n APIが受け付けるプロパティのみを保持
workflow_data_clean = {
    'name': workflow_data.get('name'),
    'nodes': workflow_data.get('nodes', []),
    'connections': workflow_data.get('connections', {}),
}
if 'settings' in workflow_data:
    workflow_data_clean['settings'] = workflow_data['settings']
# tags は読み取り専用なので作成時は含めない
```

**削除すべきプロパティ一覧**:
- `versionId`
- `updatedAt`
- `triggerCount`
- `tags`（読み取り専用）
- `pinData`
- `staticData`（作成時は不要）
- `id`（新規作成時）
- `createdAt`
- `isArchived`
- `versionCounter`

---

### 3. インポートスクリプトの使用

**推奨**: `scripts/import-workflow-to-n8n.py`を使用

```bash
python scripts/import-workflow-to-n8n.py workflows/webhook-google-workspace-control.json
```

**メリット**:
- ✅ 自動的にプロパティをクリーンアップ
- ✅ .envファイルから認証情報を自動読み込み
- ✅ エラーハンドリングが適切
- ✅ ステータスコード200と201の両方を成功として処理

**重要な注意事項**: `.env`ファイルが存在しない場合、スクリプトは`.env.env`ファイルも自動的に確認します。環境変数ファイルの命名規則に注意してください。

---

### 4. レスポンスステータスコードの扱い

**n8n APIのレスポンスコード**:
- `200`: 成功（既存ワークフローの更新等）
- `201`: 成功（新規ワークフローの作成）

**ベストプラクティス**: 両方を成功として処理する

```python
if response.status_code in [200, 201]:
    # 成功処理
    workflow = response.json()
    print(f"[OK] ワークフローが正常にインポートされました")
```

---

### 5. 認証情報の扱い

**ワークフローJSON内の認証情報**:
- ✅ `credentials.name` のみを含める（`id`は含めない）
- ❌ インポート時に認証情報IDを指定しても無効

**インポート後の作業**:
1. n8n Dashboardでワークフローを開く
2. 各ノードの認証情報を手動で選択
3. 認証情報が正しく設定されているか確認

---

### 6. 標準フロー（実証済み）

1. **ワークフロー作成・編集**（Cursor）
2. **ノードの存在確認**（`@n8n-local`で検索）
3. **ローカル検証**（`npm run format`, `npm run format:check`）
4. **GitHubへコミット・プッシュ**（Cursor自動実行）
5. **環境変数ファイルの確認**
   - `.env`ファイルが存在するか確認
   - 存在しない場合は`.env.env`ファイルも確認
   - `N8N_API_KEY`が設定されていることを確認
6. **n8n Cloudへインポート**（`scripts/import-workflow-to-n8n.py`使用）
   ```bash
   python scripts/import-workflow-to-n8n.py workflows/workflow-name.json
   ```
7. **インポート結果の確認**
   - ワークフローIDとURLを確認
   - n8n Dashboardでワークフローが存在することを確認
8. **フォルダへの移動**（必要な場合）
   - Personalフォルダ: `https://hadayalab.app.n8n.cloud/projects/fPT5foO8DCTDBr0k/workflows`
   - hadayalab-automation-platformフォルダ: `https://hadayalab.app.n8n.cloud/projects/9D29Es58GIo6IPkZ/workflows`
   - n8n Dashboardでドラッグ&ドロップで移動
9. **認証情報設定**（n8n Dashboard・人間の役割）
   - 各ノードの認証情報を設定
   - Google Workspace、Chatwork等の認証情報を設定
10. **ワークフロー有効化**（n8n Dashboard・人間の役割）
    - 「Activate」ボタンをクリック
    - 「Available in MCP」を有効化（MCP経由でアクセスする場合）
11. **テストと検証**（Cursor）
    - テストスクリプトの作成
    - Webhook URLの基本動作確認
    - 各アクションのテスト（認証情報設定後）

---

## 📝 チェックリスト（実証済み）

ワークフローインポート前の確認事項:

- [ ] 使用するノードがすべて存在するか確認（`@n8n-local`で検索）
- [ ] ワークフローJSONの形式が正しいか確認（`npm run format:check`）
- [ ] 不要なプロパティが含まれていないか確認（`versionId`, `updatedAt`, `tags`等）
- [ ] 環境変数ファイルの確認（`.env`または`.env.env`に`N8N_API_KEY`が設定されているか）
- [ ] インポートスクリプトが最新か確認（`scripts/import-workflow-to-n8n.py`）

ワークフローインポート後の確認事項:

- [ ] インポートが成功したか確認（ワークフローIDとURLを確認）
- [ ] n8n Dashboardでワークフローが存在することを確認
- [ ] 適切なフォルダに移動されているか確認（Personalまたはhadayalab-automation-platform）
- [ ] 各ノードの認証情報を設定（人間の役割）
- [ ] ワークフローを有効化（人間の役割）
- [ ] Webhook URLが生成されているか確認
- [ ] テストスクリプトを作成して基本動作を確認（Cursor）

---

## 📝 今回のフローで得られた追加のベストプラクティス（2025-12-26）

### .envファイルの確認方法

**問題**: `.env`ファイルが存在しない場合、インポートスクリプトがエラーになる

**解決策**: インポートスクリプトは`.env`ファイルが見つからない場合、自動的に`.env.env`ファイルも確認します

**実装**:
```python
# .envファイルを読み込む（.env.envも確認）
env_path = Path(__file__).parent.parent / ".env"
if not env_path.exists():
    # .env.envも確認
    env_path = Path(__file__).parent.parent / ".env.env"
load_env_file(env_path)
```

### インポート後の検証手順

1. **インポート結果の確認**
   - ワークフローIDとURLを確認
   - 例: `ID: bELMAoceJ0vFNMaa`, `URL: https://hadayalab.app.n8n.cloud/workflow/bELMAoceJ0vFNMaa`

2. **n8n Dashboardでの確認**
   - ワークフローが存在することを確認
   - フォルダに移動されているか確認（必要な場合）

3. **テストスクリプトの作成**
   - Webhook URLの基本動作確認
   - 各アクションのテスト（認証情報設定後）

### フォルダへの移動手順

**Personalフォルダへの移動**:
1. n8n Dashboardでワークフローを開く
2. Personalフォルダ（プロジェクトID: `fPT5foO8DCTDBr0k`）にドラッグ&ドロップ
3. または、ワークフローメニュー（⋮）から「Move」を選択

**hadayalab-automation-platformフォルダへの移動**:
1. n8n Dashboardでワークフローを開く
2. hadayalab-automation-platformフォルダ（プロジェクトID: `9D29Es58GIo6IPkZ`）にドラッグ&ドロップ
3. または、ワークフローメニュー（⋮）から「Move」を選択

---

## 🔗 関連ドキュメント

- [n8n完全SSOT](./n8n-complete-SSOT.md) - n8n関連のすべてのナレッジ
- [インポートスクリプト](../../scripts/import-workflow-to-n8n.py) - 実装済みのインポートスクリプト
- [フォルダ整理ガイド](../setup/n8n-folder-organization-guide.md) - フォルダ管理ガイド

---

**最終更新**: 2025-12-26
**バージョン**: 1.1.0（.env.envファイル対応とインポート後検証手順を追加）

