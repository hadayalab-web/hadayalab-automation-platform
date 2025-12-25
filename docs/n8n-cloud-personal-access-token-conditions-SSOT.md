# n8n Cloud Personal Access Token 取得条件 徹底調査 SSOT

**最終更新**: 2025-01-24
**最終検証**: 2025-01-24（公式ドキュメント、コミュニティフォーラム、SNS、YouTube）
**バージョン**: 1.0.0
**メンテナー**: HadayaLab

---

## 📚 公式リファレンス

- **n8n API Documentation**: [n8n API Documentation](https://docs.n8n.io/api/)
- **n8n API Authentication**: [n8n API Authentication](https://docs.n8n.io/api/authentication/)
- **n8n Cloud Dashboard**: https://hadayalab.app.n8n.cloud
- **n8n Community Forum**: https://community.n8n.io/

---

## 🔍 調査結果サマリー

### Personal Access Token（API Key）の取得条件

**結論**: **プラン、バージョン、アカウント状態によって取得可能性が異なる**

---

## ✅ 取得可能な条件

### 1. プラン要件

#### ✅ 有料プランが必要（Starterプラン以上）

- **無料トライアル期間中**: ❌ API機能が利用できない
- **Starterプラン（24€/mo）**: ✅ API機能が利用可能
- **Proプラン（60€/mo）**: ✅ API機能が利用可能
- **Enterpriseプラン（Custom）**: ✅ API機能 + スコープ設定が可能

**重要**:
- n8n Cloudの無料トライアル期間中は、API機能（Personal Access Token/API Key）が利用できません
- **Starterプラン以上**（有料プラン）にアップグレードすると、API機能が利用可能になります
- スコープ設定は**Enterpriseプランのみ**で利用可能です

### 2. バージョン要件

#### ✅ 最新バージョンが必要

- **古いバージョン**: ❌ Personal Access Token機能がまだ実装されていない可能性
- **最新バージョン**: ✅ Personal Access Token機能が利用可能

**確認方法**:
- Settings → Personal → バージョン情報を確認
- n8n Cloudは自動アップデートされるため、通常は最新バージョン

### 3. 権限要件

#### ✅ 管理者権限が必要

- **一般ユーザー**: ⚠️ 権限が不足している可能性
- **管理者**: ✅ Personal Access Tokenを作成可能

**確認方法**:
- Settings → API → Personal Access Tokens メニューにアクセスできるか確認
- アクセスできない場合は、管理者に権限の確認を依頼

### 4. アカウント状態

#### ✅ アクティブなアカウント

- **アクティブ**: ✅ Personal Access Tokenを作成可能
- **一時停止**: ❌ Personal Access Tokenを作成できない可能性
- **制限中**: ❌ Personal Access Tokenを作成できない可能性

---

## ❌ 取得できない条件

### 1. 無料トライアル期間中

**制限**: n8n Cloudの無料トライアル期間中は、API機能が利用できません。

**対応**:
- プランをアップグレードする必要があります
- 有料プランに移行すると、API機能が利用可能になります

### 2. 無料プラン

**制限**: 無料プランでは、Personal Access Token機能が制限されている可能性があります。

**対応**:
- 有料プランにアップグレード
- または、n8n Self-hosted版を使用（無料でPersonal Access Tokenが取得可能）

### 3. 古いバージョン

**制限**: 古いバージョンでは、Personal Access Token機能がまだ実装されていない可能性があります。

**対応**:
- n8n Cloudは自動アップデートされるため、通常は最新バージョン
- 問題がある場合は、n8n Cloudサポートに問い合わせ

### 4. 権限不足

**制限**: 一般ユーザーでは、Personal Access Tokenを作成できない可能性があります。

**対応**:
- 管理者に権限の確認を依頼
- 管理者権限を付与してもらう

### 5. 機能の段階的ロールアウト

**制限**: Personal Access Tokenがベータ機能として段階的にロールアウトされている可能性があります。

**対応**:
- 時間が経てば利用可能になる可能性
- n8n Cloudサポートに問い合わせて、機能の利用可能性を確認

---

## 📊 プラン別の機能比較

| プラン | Personal Access Token | API機能 | スコープ設定 | 料金 | 備考 |
|--------|---------------------|---------|------------|------|------|
| **無料トライアル** | ❌ 利用不可 | ❌ 利用不可 | ❌ | 無料 | プランアップグレードが必要 |
| **Starter** | ✅ 利用可能 | ✅ 利用可能 | ❌ | 24€/mo | 有料プラン、API機能利用可能 |
| **Pro** | ✅ 利用可能 | ✅ 利用可能 | ⚠️ 基本のみ | 60€/mo | より多くの機能 |
| **Enterprise** | ✅ 利用可能 | ✅ 利用可能 | ✅ 完全対応 | Custom | スコープ設定が可能 |

### プラン詳細（2025-01-24時点）

#### Starterプラン（24€/mo）

- ✅ **Personal Access Token（API Key）**: 利用可能
- ✅ **API機能**: 利用可能
- ❌ **スコープ設定**: 利用不可（エンタープライズプランのみ）
- **含まれる機能**:
  - 2.5k Workflow executions with unlimited steps
  - Active workflows and unlimited test ones
  - 1 shared project
  - 5 concurrent executions
  - Unlimited users
  - 50 AI Workflow Builder credits / month
  - Forum support
  - 1 day workflow history

#### Proプラン（60€/mo）

- ✅ **Personal Access Token（API Key）**: 利用可能
- ✅ **API機能**: 利用可能
- ⚠️ **スコープ設定**: 基本のみ（エンタープライズプランで完全対応）
- **含まれる機能**:
  - 10k Workflow executions with unlimited steps
  - Active workflows and unlimited test ones
  - 3 shared projects
  - 20 concurrent executions
  - 7 days of insights
  - 150 AI Workflow Builder credits / month
  - Admin roles
  - Global variables
  - 5 day workflow history
  - Execution search

#### Enterpriseプラン（Custom）

- ✅ **Personal Access Token（API Key）**: 利用可能
- ✅ **API機能**: 利用可能
- ✅ **スコープ設定**: 完全対応
- **含まれる機能**:
  - Unlimited workflow executions with unlimited steps
  - Up to unlimited active workflows and unlimited test ones
  - Unlimited shared projects
  - 200+ concurrent executions
  - 365 days of insights
  - 1000 AI Workflow Builder credits / month
  - SSO SAML and LDAP
  - Different environments
  - External secret store integration
  - Log streaming
  - Version control using Git
  - Scaling options
  - Extended data retention
  - Dedicated support with SLA
  - Invoice billing

---

## 🔍 実際の確認手順

### ステップ1: プラン情報の確認

1. **n8n Cloud Dashboardにログイン**
   ```
   https://hadayalab.app.n8n.cloud
   ```

2. **Settings → Subscription または Billing を確認**
   - 現在のプランを確認
   - 無料トライアル期間中かどうか確認
   - 有料プランかどうか確認

### ステップ2: APIメニューの確認

1. **Settings → API セクションを確認**
   - 「Personal Access Tokens」または「API Keys」メニューが存在するか確認
   - メニューが存在しない場合、プランが原因の可能性

### ステップ3: バージョン情報の確認

1. **Settings → Personal をクリック**
   - バージョン情報を確認
   - 最新バージョンかどうか確認

### ステップ4: 権限の確認

1. **Settings → API → Personal Access Tokens にアクセス**
   - アクセスできるか確認
   - 「Create Token」ボタンが表示されるか確認

---

## 🔄 API KeyとPersonal Access Tokenの関係

### 用語の整理

n8nの公式ドキュメントでは、以下の用語が使用されています：

- **API Key**: REST API認証用のキー（`X-N8N-API-KEY`ヘッダーで使用）
- **Personal Access Token**: より一般的な用語（GitHubなどで使用される用語）

**実際には、n8nでは「API Key」という用語が使用されており、「Personal Access Token」は同じものを指す場合があります。**

### 取得方法

#### n8n Cloud

1. Settings → **API** → **API Keys** または **Personal Access Tokens**
2. 「**Create API Key**」または「**Create Token**」をクリック
3. キーにラベルを付け、有効期限を設定
4. （エンタープライズプランの場合）スコープを選択
5. API Keyをコピーして保存

#### n8n Self-hosted

1. Settings → **API** → **API Keys**
2. 「**Create API Key**」をクリック
3. キーにラベルを付け、有効期限を設定
4. API Keyをコピーして保存

### 使用方法

#### REST APIでの使用

```bash
# X-N8N-API-KEYヘッダーとして使用
curl -X 'GET' \
  'https://hadayalab.app.n8n.cloud/api/v1/workflows?active=true' \
  -H 'accept: application/json' \
  -H 'X-N8N-API-KEY: <your-api-key>'
```

#### n8n-mcpパッケージでの使用

```json
{
  "mcpServers": {
    "n8n-local": {
      "command": "npx",
      "args": ["-y", "n8n-mcp@latest"],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
        "N8N_API_KEY": "<YOUR_API_KEY>",
        "LOG_LEVEL": "error",
        "NODE_NO_WARNINGS": "1"
      }
    }
  }
}
```

---

## 📝 エンタープライズプランのスコープ機能

### スコープとは

エンタープライズプランでは、API Keyに**スコープ**を設定することで、キーがアクセスできるリソースや操作を制限できます。

### スコープの例

- **workflow:read**: ワークフローの読み取りのみ
- **workflow:write**: ワークフローの作成・更新・削除
- **execution:read**: 実行履歴の読み取りのみ
- **variable:read**: 環境変数の読み取りのみ
- **variable:write**: 環境変数の作成・更新・削除

### スコープの設定方法

1. Settings → API → API Keys
2. 「Create API Key」をクリック
3. キーにラベルを付け、有効期限を設定
4. **スコープを選択**（エンタープライズプランの場合）
5. API Keyをコピーして保存

---

## 🎯 取得条件の判断フロー

```
Personal Access Token（API Key）を取得したい
  ↓
n8n Cloud Dashboardにログイン
  ↓
Settings → Subscription または Billing を確認
  ↓
┌─────────────────────────────────────┐
│ 無料トライアル期間中？              │
└─────────────────────────────────────┘
  ↓ YES
❌ 取得不可（プランアップグレードが必要）
  ↓
┌─────────────────────────────────────┐
│ 無料プラン？                        │
└─────────────────────────────────────┘
  ↓ YES
⚠️ 制限あり（有料プランへのアップグレードを検討）
  ↓
┌─────────────────────────────────────┐
│ 有料プラン？                        │
└─────────────────────────────────────┘
  ↓ YES
Settings → API → API Keys を確認
  ↓
┌─────────────────────────────────────┐
│ メニューが存在する？                │
└─────────────────────────────────────┘
  ↓ YES
✅ Personal Access Token（API Key）を作成
  ↓
┌─────────────────────────────────────┐
│ メニューが存在しない？              │
└─────────────────────────────────────┘
  ↓ YES
原因を確認:
1. バージョンが古い？
2. 権限が不足している？
3. 機能が段階的ロールアウト中？
  ↓
代替方法を検討:
1. MCP Access Tokenを使用（MCPプロトコル経由）
2. n8n Dashboardから手動操作
3. n8n Self-hosted版を使用
4. n8n Cloudサポートに問い合わせ
```

---

## 📚 情報源

### 公式ドキュメント

- [n8n API Documentation](https://docs.n8n.io/api/)
- [n8n API Authentication](https://docs.n8n.io/api/authentication/)

### コミュニティ

- [n8n Community Forum](https://community.n8n.io/)
- [n8n GitHub](https://github.com/n8n-io/n8n)

### SNS

- [n8n Twitter/X](https://twitter.com/n8n_io)
- [n8n LinkedIn](https://www.linkedin.com/company/n8n-io)

### YouTube

- [n8n YouTube Channel](https://www.youtube.com/@n8n_io)

---

## ⚠️ 重要な注意事項

### 1. 無料トライアル期間中の制限

**重要**: n8n Cloudの無料トライアル期間中は、**API機能（Personal Access Token/API Key）が利用できません**。

**対応**:
- プランをアップグレードする必要があります
- 有料プランに移行すると、API機能が利用可能になります

### 2. プランによる機能制限

- **無料プラン**: API機能が制限されている可能性
- **有料プラン**: API機能が利用可能
- **エンタープライズプラン**: API機能 + スコープ設定が可能

### 3. 用語の違い

- **API Key**: n8n公式ドキュメントで使用される用語
- **Personal Access Token**: より一般的な用語（GitHubなど）
- **実際には同じものを指す場合が多い**

---

## 🎯 結論

### Personal Access Token（API Key）の取得条件

1. **必須条件**:
   - ✅ **有料プラン**（無料トライアル期間中は不可）
   - ✅ **最新バージョン**（通常は自動アップデート）
   - ✅ **管理者権限**（一般ユーザーでは制限あり）

2. **推奨条件**:
   - ✅ **エンタープライズプラン**（スコープ設定が可能）

3. **取得できない場合**:
   - ❌ 無料トライアル期間中
   - ❌ 無料プラン（機能が制限されている）
   - ❌ 権限不足
   - ❌ 機能がまだロールアウトされていない

### 推奨事項

1. **まず確認**: n8n Cloud DashboardでSettings → Subscription または Billing を確認
2. **プラン確認**:
   - 無料トライアル期間中でないか確認
   - **Starterプラン以上**（有料プラン）かどうか確認
3. **APIメニュー確認**: Settings → API → API Keys または Personal Access Tokens メニューが存在するか確認
4. **存在する場合**: Personal Access Token（API Key）を作成して使用
5. **存在しない場合**:
   - **Starterプラン以上にアップグレード**（24€/moから）
   - MCP Access Tokenを使用（MCPプロトコル経由）
   - n8n Dashboardから手動操作
   - n8n Self-hosted版を使用
   - n8n Cloudサポートに問い合わせ

### Starterプランで十分か？

**結論**: ✅ **StarterプランでPersonal Access Token（API Key）は取得可能です**

**理由**:
- Starterプランは有料プラン（24€/mo）
- 有料プランではAPI機能が利用可能
- Personal Access Token（API Key）の作成・使用が可能

**制限事項**:
- ❌ スコープ設定は利用不可（Enterpriseプランのみ）
- ⚠️ 実行数制限: 2.5k Workflow executions / month
- ⚠️ 同時実行数制限: 5 concurrent executions

**推奨**:
- Personal Access Token（API Key）の取得のみが必要な場合: ✅ **Starterプランで十分**
- スコープ設定が必要な場合: ❌ Enterpriseプランが必要
- より多くの実行数が必要な場合: Proプラン（60€/mo）を検討

---

## 🔄 更新履歴

### 2025-01-24 (v1.0.0)
- 初版作成
- n8n CloudのPersonal Access Token取得条件を徹底調査
- 公式ドキュメント、コミュニティフォーラム、SNS、YouTubeなどの情報源を基に、プラン、バージョン、権限などの条件をまとめ
- 無料トライアル期間中の制限を明確化
- API KeyとPersonal Access Tokenの関係を明確化

---

**このドキュメントは、n8n Cloud Personal Access Tokenの取得条件に関する唯一の信頼できる情報源（SSOT）です。**

