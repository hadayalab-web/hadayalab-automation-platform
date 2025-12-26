# Vercelデプロイメントログ取得ガイド

## 📋 概要

Vercelのデプロイメントログを取得する方法を説明します。

## 🔍 重要な発見

### AI Gatewayとデプロイメントログの違い

- **AI Gateway**: AIモデルへのアクセスを統一するAPI（[Vercel AI Gateway Documentation](https://vercel.com/docs/ai-gateway)）
- **デプロイメントログ**: ビルド・デプロイメントの実行ログ

これらは**別の機能**です。

## 🚀 ログ取得方法

### 方法1: Vercel CLIを使用（推奨）

```bash
# Vercel CLIをインストール
npm install -g vercel

# ログイン
vercel login

# デプロイメントログを取得
vercel logs <deployment-url>
# 例: vercel logs https://cryptosignal-7l4999wfk-hadayalab-projects-projects.vercel.app/
```

### 方法2: Vercel Dashboardから確認

1. Vercel Dashboard → **Deployments**
2. 対象のデプロイメントをクリック
3. **「Logs」タブ**をクリック
4. ログを確認

### 方法3: Vercel REST APIを使用

#### デプロイメントIDの取得

まず、デプロイメントIDを取得する必要があります：

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_VERCEL_API_TOKEN"
}

# デプロイメント一覧を取得
$deployments = Invoke-RestMethod -Uri "https://api.vercel.com/v13/deployments?limit=20" -Headers $headers
$deployments.deployments | Where-Object { $_.url -like "*cryptosignal*" } | Select-Object id, url
```

#### ログの取得

デプロイメントIDが取得できたら、ログを取得：

```powershell
$deploymentId = "dpl_xxxxx"  # 実際のデプロイメントID
$headers = @{
    "Authorization" = "Bearer YOUR_VERCEL_API_TOKEN"
}

# ログを取得
$logs = Invoke-RestMethod -Uri "https://api.vercel.com/v2/deployments/$deploymentId/events" -Headers $headers
$logs | ConvertTo-Json -Depth 10
```

## ⚠️ 注意事項

### APIバージョンの問題

Vercel APIのバージョンによっては、エンドポイントが異なる可能性があります：

- `/v13/deployments` - デプロイメント一覧
- `/v2/deployments/{id}/events` - デプロイメントログ

### デプロイメントIDの形式

- デプロイメントIDは `dpl_` で始まる形式
- URLの一部（例: `7l4999wfk`）はデプロイメントIDの一部ですが、完全なIDではありません

### API Tokenの権限

- Vercel API Tokenには適切な権限が必要です
- プロジェクトへのアクセス権限を確認してください

## 📚 参考リンク

- [Vercel CLI Documentation](https://vercel.com/docs/cli)
- [Vercel REST API Reference](https://vercel.com/docs/rest-api)
- [Vercel AI Gateway Documentation](https://vercel.com/docs/ai-gateway)

---

**最終更新**: 2025-01-24















