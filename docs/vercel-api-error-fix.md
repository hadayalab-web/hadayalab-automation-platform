# Vercel API エラー修正手順

## 修正内容

ワークフローの `Trigger Vercel Deployment` ノードのリクエスト形式を修正しました。

### 変更前（問題あり）
- `bodyParameters` を使用
- `projectSettings` を含む（不要なパラメータ）
- `gitSource` が文字列として送信される可能性

### 変更後（修正済み）
- `jsonBody` を使用（正しいJSON形式）
- `projectSettings` を削除
- `gitSource` を正しいオブジェクト形式で送信

## 修正後のワークフローを適用

1. **修正されたワークフローJSONをダウンロード**
   - `workflow-cursor-vercel-deploy.json` を確認

2. **n8n Dashboardでワークフローを更新**
   - ワークフローを開く
   - `Trigger Vercel Deployment` ノードを選択
   - Body設定を確認：
     - **Specify Body**: `JSON`
     - **JSON Body**: `={{ { name: $json.repository.name, gitSource: { type: 'github', repo: $json.repository.fullName, ref: $json.repository.branch } } }}`

3. **保存して再テスト**

## 確認事項

### 1. 環境変数
- [ ] `VERCEL_API_TOKEN` が設定されている
- [ ] 値が正しい（`vck_5JSPF6NEHGpepNcpYT0UVRxsitlYsqYEj7If6Kyo7FeYUgdYgb301t6P`）

### 2. 認証ヘッダー
- [ ] Authorization: `Bearer {{ $env.VERCEL_API_TOKEN }}`
- [ ] Content-Type: `application/json`

### 3. リクエストボディ
- [ ] `name`: リポジトリ名
- [ ] `gitSource.type`: `github`
- [ ] `gitSource.repo`: `owner/repo` 形式
- [ ] `gitSource.ref`: ブランチ名（`main`）

## エラーの確認方法

n8n Dashboard → Executions で以下を確認：

1. **最新の実行を開く**
2. **`Trigger Vercel Deployment` ノードを確認**
   - エラーメッセージ
   - ステータスコード
   - リクエストボディ
   - レスポンス

## よくあるエラー

### 401 Unauthorized
- 環境変数 `VERCEL_API_TOKEN` が設定されていない
- Tokenが無効

### 400 Bad Request
- リクエストボディの形式が間違っている
- 必須パラメータが不足している

### 404 Not Found
- リポジトリが見つからない
- プロジェクトが存在しない

## 次のステップ

1. ワークフローを更新
2. 再度テスト実行
3. エラーログを確認
4. 問題があれば修正















