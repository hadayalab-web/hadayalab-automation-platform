# n8n Cloud vs Self-hosted 比較 SSOT（Single Source of Truth）

**最終更新**: 2025-01-24
**最終検証**: 2025-01-24（公式ドキュメントと最新リファレンス）
**バージョン**: 1.0.0
**メンテナー**: HadayaLab

---

## 📚 公式リファレンス

- **n8n公式ドキュメント**: [n8n Documentation](https://docs.n8n.io/)
- **n8n Hosting**: [n8n Hosting Documentation](https://docs.n8n.io/hosting/)
- **n8n Installation**: [n8n Installation Documentation](https://docs.n8n.io/installation-setup/)
- **n8n Docker**: [n8n Docker Documentation](https://docs.n8n.io/hosting/installation/docker/)

---

## 🎯 概要

n8nには**2つの主要なデプロイメントオプション**があります：

1. **n8n Cloud**（マネージドサービス）
2. **n8n Self-hosted**（セルフホスティング版）

---

## ☁️ n8n Cloud

### 📝 概要

n8nが提供するマネージドサービスで、ユーザーはサーバーの管理やメンテナンスを行う必要がありません。

### ✅ 特徴

#### メリット

- ✅ **すぐに利用開始**: サーバーセットアップ不要
- ✅ **メンテナンス不要**: n8nがサーバー管理を担当
- ✅ **自動アップデート**: 最新バージョンに自動更新
- ✅ **スケーラビリティ**: 自動スケーリング
- ✅ **セキュリティ**: n8nがセキュリティ対策を実施
- ✅ **サポート**: 公式サポートが利用可能

#### デメリット

- ❌ **月額料金**: 有料プランが必要（無料プランは制限あり）
- ❌ **カスタマイズ制限**: 環境や設定のカスタマイズが制限される
- ❌ **データの場所**: データがn8nのサーバーに保存される

### 💰 料金

- **無料プラン**: 制限あり（実行時間、ワークフロー数など）
- **有料プラン**: 月額料金が発生（プランによって異なる）

### 🔧 現在の使用状況

- **URL**: https://hadayalab.app.n8n.cloud
- **認証**: MCP Access Token（`N8N_ACCESS_TOKEN`）
- **MCP Server URL**: `https://hadayalab.app.n8n.cloud/mcp-server/http`

---

## 🖥️ n8n Self-hosted（セルフホスティング版）

### 📝 概要

ユーザー自身がサーバーにn8nをインストールして運用する形式です。**無料で利用可能**です。

### ✅ 特徴

#### メリット

- ✅ **無料**: n8nのソフトウェア自体は無料
- ✅ **完全な制御**: サーバー、データ、設定を完全に制御
- ✅ **カスタマイズ性**: 環境や設定を自由にカスタマイズ可能
- ✅ **データの管理**: データを自分のサーバーで管理
- ✅ **プライバシー**: データが外部に送信されない
- ✅ **制限なし**: 実行時間、ワークフロー数などの制限なし（サーバーリソース次第）

#### デメリット

- ❌ **セットアップが必要**: サーバーのセットアップとメンテナンスが必要
- ❌ **技術的知識が必要**: Docker、サーバー管理の知識が必要
- ❌ **メンテナンス負担**: アップデート、セキュリティ対策を自分で実施
- ❌ **サーバーコスト**: サーバーの運用費用が発生
- ❌ **サポート**: コミュニティサポートのみ（公式サポートは有料）

### 🔧 インストール方法

#### 方法1: Docker（推奨）

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

#### 方法2: npm

```bash
npm install n8n -g
n8n start
```

#### 方法3: Docker Compose

```yaml
version: '3.8'
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
    volumes:
      - ~/.n8n:/home/node/.n8n
```

### 📋 システム要件

- **OS**: Linux、macOS、Windows（Docker推奨）
- **メモリ**: 最低2GB（推奨4GB以上）
- **ストレージ**: 最低10GB（推奨20GB以上）
- **CPU**: 最低2コア（推奨4コア以上）

### 🔐 認証

Self-hosted版では、以下の認証方法が利用可能です：

- **Basic Auth**: ユーザー名とパスワード
- **OAuth2**: 外部認証プロバイダー
- **API Key**: REST API用のAPI Keyを生成可能

### ⚙️ 設定

Self-hosted版では、環境変数や設定ファイルで詳細なカスタマイズが可能です：

- データベース設定（PostgreSQL、MySQL、SQLite）
- メール設定
- 外部認証設定
- カスタムノードの追加
- 実行環境のカスタマイズ

---

## 📊 比較表

| 項目 | n8n Cloud | n8n Self-hosted |
|------|-----------|----------------|
| **費用** | 月額料金（無料プランは制限あり） | 無料（サーバー費用は別途） |
| **セットアップ** | 不要（すぐに利用開始） | 必要（サーバーセットアップ） |
| **メンテナンス** | n8nが実施 | ユーザーが実施 |
| **アップデート** | 自動 | 手動 |
| **カスタマイズ** | 制限あり | 完全にカスタマイズ可能 |
| **データの場所** | n8nのサーバー | ユーザーのサーバー |
| **スケーラビリティ** | 自動スケーリング | 手動スケーリング |
| **セキュリティ** | n8nが実施 | ユーザーが実施 |
| **サポート** | 公式サポート | コミュニティサポート（公式サポートは有料） |
| **実行時間制限** | プランによる | なし（サーバーリソース次第） |
| **ワークフロー数制限** | プランによる | なし（サーバーリソース次第） |
| **Personal Access Token** | 条件による（バージョン・プラン） | ✅ 取得可能 |
| **MCP Access Token** | ✅ 取得可能 | ✅ 取得可能 |

---

## 🎯 選択ガイド

### n8n Cloudを選択する場合

- ✅ **すぐに利用開始したい**
- ✅ **サーバー管理をしたくない**
- ✅ **メンテナンスをしたくない**
- ✅ **公式サポートが必要**
- ✅ **自動スケーリングが必要**
- ✅ **予算がある**

### n8n Self-hostedを選択する場合

- ✅ **コストを抑えたい**
- ✅ **完全な制御が必要**
- ✅ **カスタマイズが必要**
- ✅ **データを自分のサーバーで管理したい**
- ✅ **プライバシーを重視**
- ✅ **技術的知識がある**
- ✅ **サーバー管理が可能**

---

## 🔄 移行可能性

### Cloud → Self-hosted

- ✅ **可能**: ワークフローをエクスポートしてSelf-hosted版にインポート
- ⚠️ **注意**: 認証情報（Credentials）は再設定が必要

### Self-hosted → Cloud

- ✅ **可能**: ワークフローをエクスポートしてCloud版にインポート
- ⚠️ **注意**: 認証情報（Credentials）は再設定が必要

---

## 📝 現在のプロジェクトでの使用状況

### 現在の構成

- **使用環境**: n8n Cloud
- **URL**: https://hadayalab.app.n8n.cloud
- **認証**: MCP Access Token（`N8N_ACCESS_TOKEN`）
- **MCP Server URL**: `https://hadayalab.app.n8n.cloud/mcp-server/http`

### Self-hosted版への移行を検討する場合

#### メリット

- ✅ Personal Access Tokenが確実に取得可能（無料）
- ✅ カスタマイズが可能
- ✅ コスト削減（サーバー費用のみ）
- ✅ **n8n-mcpパッケージを無料で使用可能**

#### デメリット

- ❌ サーバーのセットアップとメンテナンスが必要
- ❌ 現在のワークフローの移行が必要
- ❌ 認証情報の再設定が必要

### 重要な結論

**n8n-mcpパッケージは無料でセルフホスト版で利用したい人向け**

- **n8n Cloud**: Personal Access Token取得には有料プラン（Starter以上、24€/mo）が必要
- **n8n Self-hosted**: Personal Access Tokenを無料で取得可能
- **推奨**: 無料でn8n-mcpパッケージを使用したい場合は、**n8n Self-hosted版**を使用

---

## 🔐 認証の違い

### n8n Cloud

- **MCP Access Token**: ✅ 取得可能（Settings → MCP Access → Access Tokenタブ）
- **Personal Access Token**: 条件による（バージョン・プラン）

### n8n Self-hosted

- **MCP Access Token**: ✅ 取得可能（Settings → MCP Access → Access Tokenタブ）
- **Personal Access Token**: ✅ 取得可能（Settings → API → Personal Access Tokens）
- **API Key**: ✅ 生成可能（REST API用）

---

## 📚 参考リンク

### 公式ドキュメント

- [n8n Hosting Documentation](https://docs.n8n.io/hosting/)
- [n8n Installation Documentation](https://docs.n8n.io/installation-setup/)
- [n8n Docker Documentation](https://docs.n8n.io/hosting/installation/docker/)
- [n8n Docker Compose Documentation](https://docs.n8n.io/hosting/installation/server-setups/docker-compose/)

### コミュニティ

- [n8n Community Forum](https://community.n8n.io/)
- [n8n GitHub](https://github.com/n8n-io/n8n)

---

## 🔄 更新履歴

### 2025-01-24 (v1.0.0)
- 初版作成
- n8n CloudとSelf-hosted版の徹底比較
- 公式ドキュメントと最新リファレンスを基に、特徴、メリット・デメリット、インストール方法をまとめ
- 認証の違いを明確化

---

**このドキュメントは、n8n CloudとSelf-hosted版の比較に関する唯一の信頼できる情報源（SSOT）です。**

