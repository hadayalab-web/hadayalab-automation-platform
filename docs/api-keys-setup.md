# API Keys設定ガイド

このドキュメントは、MCPサーバーとGitHub Copilot Pro連携に必要な認証情報の取得・設定方法を説明します。

## ⚠️ 重要なセキュリティ注意事項

### .envファイルは共有しない

**❌ やってはいけないこと:**
- `.env`ファイルをGitにコミット
- `.env`ファイルを直接共有
- APIキーをチャットやメッセージで送信

**✅ 正しい方法:**
- `.env.example`をテンプレートとして使用
- 実際のAPIキーは`mcp.json`に直接設定（ローカルのみ）
- 環境変数として管理

---

## 📋 必要な認証情報一覧

### 必須（既に設定済み）

#### 1. n8n API Key
- **状況**: ✅ 既に設定済み
- **取得先**: https://hadayalab.app.n8n.cloud → Settings → API
- **設定場所**: `~/.cursor/mcp.json` の `N8N_API_KEY`

---

### 新規導入が必要な認証情報

#### 2. Vercel Access Token
- **必須理由**: Vercel運用中
- **取得方法**:
  1. Vercel Dashboard → Settings → Tokens
  2. "Create Token" をクリック
  3. トークン名を入力（例: "Cursor MCP"）
  4. スコープを選択（Full Access推奨）
  5. トークンをコピー（一度しか表示されません）
- **設定場所**: `~/.cursor/mcp.json` の `VERCEL_ACCESS_TOKEN`
- **形式**: `vercel_xxxxxxxxxxxxx`

#### 3. Google Workspace認証情報
- **必須理由**: Google Workspace利用中
- **取得方法**:
  1. Google Cloud Console → プロジェクト作成
  2. Google Workspace APIを有効化
  3. OAuth 2.0認証情報を作成
  4. Client ID, Client Secretを取得
  5. Refresh Tokenを取得（OAuth認証フロー実行）
- **設定場所**: `~/.cursor/mcp.json`
  - `GOOGLE_CLIENT_ID`
  - `GOOGLE_CLIENT_SECRET`
  - `GOOGLE_REFRESH_TOKEN`
- **形式**:
  - Client ID: `xxxxx.apps.googleusercontent.com`
  - Client Secret: `GOCSPX-xxxxxxxxxxxxx`
  - Refresh Token: `1//xxxxxxxxxxxxx`

#### 4. PostgreSQL/Supabase接続文字列
- **必須理由**: データベース操作の効率化
- **取得方法**:
  - **PostgreSQL**: `postgresql://user:password@host:port/database`
  - **Supabase**: Dashboard → Project Settings → Database → Connection String
- **設定場所**: `~/.cursor/mcp.json` の `POSTGRES_CONNECTION_STRING`
- **形式**: `postgresql://postgres:[PASSWORD]@[PROJECT-REF].supabase.co:5432/postgres`

#### 5. Context7 API Key（Perplexity代替）
- **必須理由**: 技術ドキュメントへのアクセス
- **取得方法**:
  1. Context7 Dashboard → API Keys
  2. "Create API Key" をクリック
  3. キーをコピー
- **設定場所**: `~/.cursor/mcp.json` の `CONTEXT7_API_KEY`
- **形式**: `ctx_xxxxxxxxxxxxx`

#### 6. Brave Search API Key（Perplexity代替）
- **必須理由**: リアルタイムWeb検索
- **取得方法**:
  1. Brave Search API → https://brave.com/search/api/
  2. "Get API Key" をクリック
  3. アカウント作成（無料プランあり）
  4. API Keyをコピー
- **設定場所**: `~/.cursor/mcp.json` の `BRAVE_API_KEY`
- **形式**: `BSA_xxxxxxxxxxxxx`

---

## 🔧 設定方法

### 方法1: mcp.jsonに直接設定（推奨）

**ファイル**: `C:\Users\chiba\.cursor\mcp.json`

```json
{
  "mcpServers": {
    "n8n": {
      "env": {
        "N8N_API_KEY": "実際のAPIキーをここに"
      }
    },
    "vercel": {
      "env": {
        "VERCEL_ACCESS_TOKEN": "実際のトークンをここに"
      }
    }
    // ... 他のMCPサーバーも同様
  }
}
```

**メリット:**
- シンプル
- 環境変数の管理が不要
- すぐに使用可能

**デメリット:**
- ファイルに平文で保存（セキュリティリスク）
- バックアップ時に注意が必要

### 方法2: 環境変数を使用（より安全）

**Windowsの場合:**
```powershell
# システム環境変数として設定
[System.Environment]::SetEnvironmentVariable("N8N_API_KEY", "your-key", "User")
[System.Environment]::SetEnvironmentVariable("VERCEL_ACCESS_TOKEN", "your-token", "User")
```

**mcp.jsonで参照:**
```json
{
  "mcpServers": {
    "n8n": {
      "env": {
        "N8N_API_KEY": "${N8N_API_KEY}"
      }
    }
  }
}
```

**メリット:**
- より安全（ファイルに平文保存しない）
- 環境ごとに異なる値を設定可能

**デメリット:**
- 設定がやや複雑
- 環境変数の管理が必要

---

## 📝 提供すべき情報（私への共有方法）

### 推奨方法: プレースホルダー付き設定ファイル

`.env.example`をベースに、以下の形式で情報を提供してください：

```markdown
## 認証情報（実際の値は直接共有しない）

以下のAPIキーを取得して、mcp.jsonに設定してください：

1. **Vercel Access Token**: [取得済み/未取得]
2. **Google Workspace**: [取得済み/未取得]
   - Client ID: [取得済み/未取得]
   - Client Secret: [取得済み/未取得]
   - Refresh Token: [取得済み/未取得]
3. **PostgreSQL接続文字列**: [取得済み/未取得]
4. **Context7 API Key**: [取得済み/未取得]
5. **Brave Search API Key**: [取得済み/未取得]
```

### 実際の値は共有しない

**❌ やってはいけないこと:**
```
N8N_API_KEY=eyJhb6ciOiJIUzI1NiIsInR5cCI6IkpXCJ9.eyJzdW...
VERCEL_ACCESS_TOKEN=vercel_xxxxxxxxxxxxx
```

**✅ 正しい方法:**
```
N8N_API_KEY=[設定済み]
VERCEL_ACCESS_TOKEN=[要設定]
```

---

## 🔐 セキュリティベストプラクティス

### 1. .gitignoreの確認

`.env`ファイルがGitにコミットされないことを確認：

```gitignore
# .gitignoreに以下が含まれているか確認
.env
.env.local
*.env
```

### 2. mcp.jsonのバックアップ

**重要**: `mcp.json`には実際のAPIキーが含まれるため：

- **Gitにコミットしない**（既に`.cursor/`は`.gitignore`に含まれている）
- **バックアップ時は暗号化**（Bitwarden、1Password等）
- **共有時はプレースホルダーを使用**

### 3. APIキーのローテーション

定期的にAPIキーを更新：
- **推奨頻度**: 3-6ヶ月ごと
- **更新手順**: 新しいキーを取得 → mcp.jsonを更新 → Cursor再起動

---

## 📋 チェックリスト

### 設定前の確認

- [ ] 必要なAPIキーをすべて取得
- [ ] `.env.example`を確認
- [ ] `.gitignore`に`.env`が含まれているか確認
- [ ] `mcp.json`のバックアップを作成

### 設定手順

- [ ] `mcp.json`を開く
- [ ] 各MCPサーバーの`<YOUR_XXX>`を実際の値に置き換え
- [ ] JSON構文を検証
- [ ] Cursorを再起動
- [ ] 各MCPサーバーの接続を確認

### 設定後の確認

- [ ] すべてのMCPサーバーが正常に接続
- [ ] エラーメッセージがない
- [ ] ツールが正常に動作

---

## 🆘 トラブルシューティング

### APIキーが無効

**症状:**
```
[error] Authentication failed
[error] Invalid API key
```

**対処:**
1. APIキーが正しくコピーされているか確認
2. 先頭・末尾の空白を削除
3. APIキーが有効期限内か確認
4. 新しいAPIキーを取得して再設定

### 環境変数が読み込まれない

**症状:**
```
[error] Environment variable not found
```

**対処:**
1. 環境変数が正しく設定されているか確認
2. Cursorを完全再起動
3. `mcp.json`で直接値を設定（一時的）

---

## 📚 参考リンク

- [Vercel API Tokens](https://vercel.com/docs/rest-api/authentication)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Supabase Connection String](https://supabase.com/docs/guides/database/connecting-to-postgres)
- [Context7 API](https://context7.com/)
- [Brave Search API](https://brave.com/search/api/)

---

**最終更新**: 2025-12-23
**バージョン**: 1.0.0

