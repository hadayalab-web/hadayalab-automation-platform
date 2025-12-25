# Vercel API エラー修正ガイド

## 考えられるエラー原因

### 1. 環境変数の問題
- `VERCEL_API_TOKEN` が正しく設定されていない
- 環境変数名が間違っている（`VERCEL_API_KEY` ではなく `VERCEL_API_TOKEN`）

### 2. Vercel APIリクエスト形式の問題
現在のワークフローでは、以下の形式でリクエストを送信しています：

```json
{
  "name": "{{ $json.repository.name }}",
  "gitSource": {
    "type": "github",
    "repo": "{{ $json.repository.fullName }}",
    "ref": "{{ $json.repository.branch }}"
  },
  "projectSettings": {
    "framework": null,
    "buildCommand": null,
    "devCommand": null,
    "installCommand": null,
    "outputDirectory": null
  }
}
```

## 修正方法

### 方法1: Vercel APIの正しい形式に修正

Vercel API v13では、デプロイを作成する際に以下の形式が必要です：

```json
{
  "name": "project-name",
  "gitSource": {
    "type": "github",
    "repo": "owner/repo",
    "ref": "main"
  }
}
```

または、プロジェクトIDを指定する場合：

```json
{
  "projectId": "prj_xxxxx",
  "gitSource": {
    "type": "github",
    "repo": "owner/repo",
    "ref": "main"
  }
}
```

### 方法2: 環境変数の確認

n8n Dashboardで以下を確認：

1. **Settings → Environment Variables**
   - 変数名: `VERCEL_API_TOKEN`
   - 値: `vck_5JSPF6NEHGpepNcpYT0UVRxsitlYsqYEj7If6Kyo7FeYUgdYgb301t6P`

2. **ワークフローのノードを確認**
   - `Trigger Vercel Deployment` ノード
   - Authorization Header: `Bearer {{ $env.VERCEL_API_TOKEN }}`
   - 正しく設定されているか確認

### 方法3: エラーログの確認

n8n Dashboard → Executions で以下を確認：

1. **最新の実行を開く**
2. **エラーが発生したノードを確認**
   - `Trigger Vercel Deployment` ノード
   - エラーメッセージを確認
   - ステータスコード（401, 400, 404など）を確認

## よくあるエラーと対処法

### エラー: 401 Unauthorized
**原因**: Vercel API Tokenが無効または設定されていない
**対処法**:
1. 環境変数 `VERCEL_API_TOKEN` が正しく設定されているか確認
2. Tokenが有効か確認（Vercel Dashboard → Settings → Tokens）
3. Tokenに適切な権限があるか確認

### エラー: 400 Bad Request
**原因**: リクエストボディの形式が間違っている
**対処法**:
1. `gitSource` の形式を確認
2. `projectSettings` を削除または正しい形式に修正
3. 必須パラメータが含まれているか確認

### エラー: 404 Not Found
**原因**: リポジトリが見つからない、またはプロジェクトが存在しない
**対処法**:
1. リポジトリ名が正しいか確認（`owner/repo` 形式）
2. Vercelプロジェクトが存在するか確認
3. プロジェクトIDを指定する必要があるか確認

## 推奨される修正

### 修正1: プロジェクトIDを指定

Vercelプロジェクトが既に存在する場合、プロジェクトIDを指定する方が確実です：

```json
{
  "projectId": "prj_xxxxx",
  "gitSource": {
    "type": "github",
    "repo": "{{ $json.repository.fullName }}",
    "ref": "{{ $json.repository.branch }}"
  }
}
```

### 修正2: シンプルなリクエスト形式

`projectSettings` を削除して、最小限のパラメータのみ送信：

```json
{
  "name": "{{ $json.repository.name }}",
  "gitSource": {
    "type": "github",
    "repo": "{{ $json.repository.fullName }}",
    "ref": "{{ $json.repository.branch }}"
  }
}
```

## 次のステップ

1. n8n Dashboardでエラーログを確認
2. エラーメッセージに基づいて修正
3. 修正後、再度テスト実行






