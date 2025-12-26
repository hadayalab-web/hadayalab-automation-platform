# Vercel CLI機能と制限 SSOT（Single Source of Truth）

**最終更新**: 2025-01-24
**バージョン**: 1.0.0
**参考**: [Vercel CLI Documentation](https://vercel.com/docs/cli)

---

## 📋 概要

このドキュメントは、Vercel CLIでできることとできないことを徹底的に調査し、整理した**唯一の信頼できる情報源（SSOT）**です。

---

## ✅ Vercel CLIでできること

### 1. プロジェクトのデプロイメント

#### 基本的なデプロイ
```bash
# プレビュー環境にデプロイ
vercel

# 本番環境にデプロイ
vercel --prod
```

#### デプロイオプション
- `--yes`: 確認プロンプトをスキップ
- `--force`: 既存のデプロイメントを上書き
- `--public`: 公開デプロイメントとして作成
- `--debug`: デバッグモードで実行

### 2. ローカル開発環境

```bash
# ローカル開発サーバーを起動
vercel dev

# 特定のポートで起動
vercel dev --listen 3000
```

**機能**:
- ローカル環境でVercelの機能を再現
- 変更を即座に確認
- 環境変数のローカル管理

### 3. 環境変数の管理

```bash
# 環境変数を追加
vercel env add <key>

# 環境変数一覧を表示
vercel env ls

# 環境変数を削除
vercel env rm <key>

# 環境変数を取得
vercel env pull
```

**対応環境**:
- `production`: 本番環境
- `preview`: プレビュー環境
- `development`: 開発環境

### 4. ログの取得

```bash
# デプロイメントログを取得
vercel logs <deployment-url|deployment-id>

# JSON形式で出力
vercel logs <deployment-id> --json

# JQでフィルタリング
vercel logs <deployment-id> --json | jq 'select(.level == "warning")'
```

**重要**: `vercel logs`コマンドの制限事項
- **Ready状態のデプロイメントのみ**: ログを取得できるのは、デプロイメントが`Ready`状態のもののみ
- **Runtime logsのみ**: 実行時（runtime）のログのみ取得可能
- **リアルタイムログ**: 現在から最大5分間のログを取得
- **ビルドログは取得不可**: ビルドログは取得できません（Vercel Dashboardから確認が必要）

### 5. デプロイメントの管理

```bash
# デプロイメント一覧を表示
vercel list [app] --yes

# デプロイメント情報を取得
vercel inspect <deployment-url|deployment-id>

# デプロイメントを削除
vercel remove <deployment-id>

# デプロイメントをロールバック
vercel rollback <deployment-id>
```

### 6. プロジェクトのリンク

```bash
# ローカルプロジェクトをVercelプロジェクトにリンク
vercel link

# 特定のプロジェクトにリンク
vercel link --project <project-name>
```

### 7. エイリアス（ドメイン）の管理

```bash
# エイリアスを追加
vercel alias <deployment-url> <alias-domain>

# エイリアス一覧を表示
vercel alias ls

# エイリアスを削除
vercel alias rm <alias-domain>
```

### 8. プロジェクトの管理

```bash
# プロジェクト一覧を表示
vercel projects ls

# プロジェクトを作成
vercel projects add <project-name>

# プロジェクトを削除
vercel projects rm <project-name>
```

### 9. ドメインの管理

```bash
# ドメイン一覧を表示
vercel domains ls

# ドメインを追加
vercel domains add <domain>

# ドメインを削除
vercel domains rm <domain>
```

### 10. 認証とアカウント管理

```bash
# ログイン
vercel login

# ログアウト
vercel logout

# 現在のユーザー情報を表示
vercel whoami

# チームを切り替え
vercel switch
```

---

## ❌ Vercel CLIでできないこと

### 1. ビルドログの取得

**制限**: `vercel logs`コマンドは**runtime logs（実行時ログ）のみ**を取得できます。

**取得できないログ**:
- ❌ ビルドログ（ビルドプロセスのログ）
- ❌ デプロイメント前のログ
- ❌ 過去のログ（最大5分間のみ）

**代替方法**:
- Vercel Dashboard → Deployments → デプロイメントを選択 → **「Build Logs」タブ**を確認

### 2. Ready状態以外のデプロイメントのログ

**制限**: `vercel logs`コマンドは、デプロイメントが**Ready状態**のもののみログを取得できます。

**取得できない状態**:
- ❌ `BUILDING`: ビルド中のデプロイメント
- ❌ `ERROR`: エラー状態のデプロイメント
- ❌ `CANCELED`: キャンセルされたデプロイメント

**代替方法**:
- Vercel Dashboardから確認
- `vercel inspect`コマンドでデプロイメント情報を確認

### 3. 高度な分析・モニタリング機能

**制限**: 以下の機能はCLIから利用できません：

- ❌ **Vercel Analytics**: Webダッシュボードから確認
- ❌ **Vercel Monitoring**: Webダッシュボードから確認
- ❌ **Real User Monitoring (RUM)**: Webダッシュボードから確認
- ❌ **Performance Insights**: Webダッシュボードから確認

### 4. 詳細なアクセス制御

**制限**: 以下の設定はCLIから行えません：

- ❌ **RBAC（Role-Based Access Control）**: Webダッシュボードから設定
- ❌ **Deployment Protection**: Webダッシュボードから設定
- ❌ **Password Protection**: Webダッシュボードから設定
- ❌ **IP Allowlist**: Webダッシュボードから設定

### 5. チーム管理

**制限**: 以下の操作はCLIから行えません：

- ❌ **チームメンバーの追加・削除**: Webダッシュボードから管理
- ❌ **チーム権限の設定**: Webダッシュボードから設定
- ❌ **チーム設定の変更**: Webダッシュボードから変更

### 6. 請求情報の管理

**制限**: 以下の操作はCLIから行えません：

- ❌ **請求情報の確認**: Webダッシュボードから確認
- ❌ **支払い方法の変更**: Webダッシュボードから変更
- ❌ **使用量の詳細確認**: Webダッシュボードから確認

### 7. カスタムドメインの詳細設定

**制限**: 基本的なドメイン管理は可能ですが、詳細な設定はCLIから行えません：

- ❌ **DNS設定の詳細管理**: Webダッシュボードから設定
- ❌ **SSL証明書の詳細設定**: Webダッシュボードから設定
- ❌ **ドメイン検証の詳細**: Webダッシュボードから確認

### 8. Webhookの管理

**制限**: Webhookの設定はCLIから行えません：

- ❌ **Webhookの作成**: Webダッシュボードから作成
- ❌ **Webhookの編集**: Webダッシュボードから編集
- ❌ **Webhookの削除**: Webダッシュボードから削除

### 9. インテグレーションの管理

**制限**: インテグレーションの設定はCLIから行えません：

- ❌ **GitHub連携の詳細設定**: Webダッシュボードから設定
- ❌ **その他のインテグレーション**: Webダッシュボードから設定

### 10. 過去のログの長期保存

**制限**: `vercel logs`コマンドは、**現在から最大5分間**のログのみ取得できます。

**取得できないログ**:
- ❌ 5分以上前のログ
- ❌ 過去のデプロイメントのログ（Ready状態でない場合）

**代替方法**:
- Vercel Dashboardから過去のログを確認
- ログを外部サービス（例: Logtail、Datadog）に転送

---

## 📊 機能比較表

| 機能 | CLI | Dashboard | API |
|------|-----|-----------|-----|
| **デプロイメント** | ✅ | ✅ | ✅ |
| **環境変数管理** | ✅ | ✅ | ✅ |
| **Runtime Logs** | ✅ | ✅ | ⚠️ 制限あり |
| **Build Logs** | ❌ | ✅ | ❌ |
| **デプロイメント一覧** | ✅ | ✅ | ✅ |
| **デプロイメント削除** | ✅ | ✅ | ✅ |
| **ロールバック** | ✅ | ✅ | ✅ |
| **Analytics** | ❌ | ✅ | ❌ |
| **Monitoring** | ❌ | ✅ | ❌ |
| **チーム管理** | ❌ | ✅ | ⚠️ 一部のみ |
| **請求情報** | ❌ | ✅ | ❌ |
| **Webhook管理** | ❌ | ✅ | ✅ |
| **アクセス制御** | ❌ | ✅ | ⚠️ 一部のみ |

---

## ⚠️ 重要な制限事項

### `vercel logs`コマンドの詳細制限

#### 1. Ready状態のデプロイメントのみ

```bash
# ✅ 動作する例
vercel logs dpl_6z4uk7ksfaX6T1fsDhcwizy3kCGP  # Ready状態のデプロイメント

# ❌ 動作しない例
vercel logs <BUILDING状態のデプロイメント>  # エラーが返される
```

#### 2. Runtime Logsのみ

- **取得可能**: アプリケーション実行時のログ（console.log、エラーログなど）
- **取得不可**: ビルドプロセスのログ（npm install、ビルドエラーなど）

#### 3. リアルタイムログのみ

- **取得可能**: 現在から最大5分間のログ
- **取得不可**: 5分以上前のログ

#### 4. URLからの直接取得の制限

```bash
# ⚠️ 動作しない場合がある
vercel logs https://example.vercel.app/

# ✅ 推奨: デプロイメントIDを使用
vercel logs dpl_xxxxx
```

**デプロイメントIDの取得方法**:
```bash
# inspectコマンドでデプロイメントIDを取得
vercel inspect https://example.vercel.app/
# 出力から id: dpl_xxxxx を取得
```

---

## 🔧 実用的な使用例

### ログ取得のワークフロー

```bash
# 1. デプロイメントIDを取得
vercel inspect https://cryptosignal-7l4999wfk-hadayalab-projects-projects.vercel.app/

# 2. デプロイメントIDでログを取得
vercel logs dpl_6z4uk7ksfaX6T1fsDhcwizy3kCGP

# 3. JSON形式で出力してフィルタリング
vercel logs dpl_6z4uk7ksfaX6T1fsDhcwizy3kCGP --json | jq 'select(.level == "error")'
```

### ビルドログが必要な場合

```bash
# ❌ CLIでは取得不可
# vercel logs <deployment-id>  # ビルドログは取得できない

# ✅ Dashboardから確認
# 1. Vercel Dashboard → Deployments
# 2. 対象のデプロイメントをクリック
# 3. 「Build Logs」タブを確認
```

---

## 📚 参考リンク

### 公式ドキュメント

- [Vercel CLI Documentation](https://vercel.com/docs/cli)
- [Vercel CLI Commands Reference](https://vercel.com/docs/cli/commands)
- [Vercel REST API Reference](https://vercel.com/docs/rest-api)
- [Vercel Limits](https://vercel.com/docs/limits)

### 関連ドキュメント

- [Vercelデプロイメントログ取得ガイド](./vercel-deployment-logs-guide.md)

---

## 🔄 更新履歴

### 2025-01-24
- 初版作成
- `vercel logs`コマンドの制限事項を詳細に記載
- 機能比較表を追加

---

**このドキュメントは、Vercel CLIの機能と制限に関する唯一の信頼できる情報源（SSOT）です。**















