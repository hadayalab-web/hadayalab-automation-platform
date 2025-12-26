# Vercel API でできること

## 概要

Vercel APIキー（`vck_` で始まるトークン）を使用すると、Vercelのほぼすべての機能をプログラムから操作できます。

## 主要な機能

### 1. デプロイメント管理

#### デプロイメントの作成
```bash
POST https://api.vercel.com/v13/deployments
```
- GitHubリポジトリからデプロイを開始
- プロジェクトのビルドとデプロイを実行
- 環境変数を指定してデプロイ

#### デプロイメントの取得
```bash
GET https://api.vercel.com/v13/deployments/{id}
```
- デプロイメントの詳細情報を取得
- ステータス（BUILDING, READY, ERROR）を確認
- デプロイメントURLを取得

#### デプロイメントの一覧取得
```bash
GET https://api.vercel.com/v13/deployments
```
- プロジェクトのデプロイメント履歴を取得
- フィルタリング（プロジェクト、ステータス、期間など）

#### デプロイメントの削除
```bash
DELETE https://api.vercel.com/v13/deployments/{id}
```
- 古いデプロイメントを削除
- ストレージの節約

### 2. ログとイベント

#### デプロイメントログの取得
```bash
GET https://api.vercel.com/v2/deployments/{id}/events
```
- ビルドログを取得
- エラーログを確認
- リアルタイムでログをストリーミング

#### 関数ログの取得
```bash
GET https://api.vercel.com/v1/deployments/{id}/functions/{name}/logs
```
- サーバーレス関数の実行ログ
- エラーとトレース情報

### 3. プロジェクト管理

#### プロジェクトの作成
```bash
POST https://api.vercel.com/v9/projects
```
- 新しいプロジェクトを作成
- GitHubリポジトリを接続
- 設定を指定

#### プロジェクトの取得
```bash
GET https://api.vercel.com/v9/projects/{id}
```
- プロジェクトの詳細情報
- 設定、環境変数、ドメインなど

#### プロジェクトの一覧取得
```bash
GET https://api.vercel.com/v9/projects
```
- アカウント内の全プロジェクト
- チームのプロジェクトも取得可能

#### プロジェクトの更新
```bash
PATCH https://api.vercel.com/v9/projects/{id}
```
- プロジェクト設定を更新
- ビルドコマンド、環境変数などを変更

#### プロジェクトの削除
```bash
DELETE https://api.vercel.com/v9/projects/{id}
```
- プロジェクトを削除

### 4. 環境変数管理

#### 環境変数の作成
```bash
POST https://api.vercel.com/v9/projects/{id}/env
```
- 環境変数を追加
- 環境（production, preview, development）を指定

#### 環境変数の取得
```bash
GET https://api.vercel.com/v9/projects/{id}/env
```
- プロジェクトの環境変数一覧

#### 環境変数の更新
```bash
PATCH https://api.vercel.com/v9/projects/{id}/env/{id}
```
- 環境変数の値を更新

#### 環境変数の削除
```bash
DELETE https://api.vercel.com/v9/projects/{id}/env/{id}
```
- 環境変数を削除

### 5. ドメイン管理

#### ドメインの追加
```bash
POST https://api.vercel.com/v9/projects/{id}/domains
```
- カスタムドメインを追加
- DNS設定を確認

#### ドメインの取得
```bash
GET https://api.vercel.com/v9/projects/{id}/domains
```
- プロジェクトのドメイン一覧

#### ドメインの削除
```bash
DELETE https://api.vercel.com/v9/projects/{id}/domains/{domain}
```
- ドメインを削除

### 6. チーム管理

#### チームの取得
```bash
GET https://api.vercel.com/v2/teams
```
- 所属チームの一覧

#### チームメンバーの取得
```bash
GET https://api.vercel.com/v2/teams/{id}/members
```
- チームメンバー一覧

### 7. Webhook管理

#### Webhookの作成
```bash
POST https://api.vercel.com/v1/integrations/webhooks
```
- デプロイメントイベントのWebhookを設定
- デプロイ完了時に通知

#### Webhookの取得
```bash
GET https://api.vercel.com/v1/integrations/webhooks
```
- 設定済みWebhookの一覧

### 8. 分析とメトリクス

#### デプロイメント分析
```bash
GET https://api.vercel.com/v1/deployments/{id}/analytics
```
- デプロイメントのパフォーマンスデータ
- ビルド時間、サイズなど

#### プロジェクト分析
```bash
GET https://api.vercel.com/v1/projects/{id}/analytics
```
- プロジェクト全体の分析データ

## 実用的な使用例

### 1. CI/CDパイプライン
- GitHub Actionsから自動デプロイ
- プルリクエストごとにプレビューデプロイ
- マージ時に本番デプロイ

### 2. モニタリングとアラート
- デプロイメントのステータスを監視
- エラーが発生したら通知
- ログを自動収集・分析

### 3. 環境管理
- 環境変数を一括管理
- 複数プロジェクトの設定を同期
- シークレットのローテーション

### 4. レポート生成
- デプロイメント履歴のレポート
- チームの活動状況を追跡
- コスト分析

### 5. 自動化
- 定期的なデプロイメント
- 古いデプロイメントの自動削除
- プロジェクトの自動セットアップ

## 現在のワークフローで使用している機能

### 使用中のエンドポイント

1. **デプロイメント作成**
   - `POST /v13/deployments`
   - GitHubリポジトリからデプロイを開始

2. **デプロイメントステータス確認**
   - `GET /v13/deployments/{id}`
   - デプロイメントの完了を待機

3. **ログ取得**（新規ワークフロー）
   - `GET /v2/deployments/{id}/events`
   - エラーログを確認

## 制限事項

### レート制限
- 通常: 100リクエスト/分
- バースト: 一時的に200リクエスト/分

### 権限
- APIキーは作成したユーザーの権限を継承
- チームのプロジェクトにアクセスするにはチームメンバーである必要がある

### 認証
- Bearer Token形式で認証
- `Authorization: Bearer {token}`

## 参考リンク

- [Vercel API Documentation](https://vercel.com/docs/rest-api)
- [Vercel API Reference](https://vercel.com/docs/rest-api/endpoints)
- [Vercel API Examples](https://vercel.com/docs/rest-api/examples)
















