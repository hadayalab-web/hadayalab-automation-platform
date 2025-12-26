# 🔧 Google OAuth `redirect_uri_mismatch` エラー解決ガイド

## 📋 エラー内容

```
エラー 400: redirect_uri_mismatch
アクセスをブロック: このアプリのリクエストは無効です
```

## 🎯 原因

Google Cloud Console側で、**承認済みのリダイレクトURI**に`https://oauth.n8n.cloud/oauth2/callback`が設定されていないことが原因です。

**重要**: 「承認済みドメイン」と「承認済みのリダイレクトURI」は**別々の設定**です。

---

## ✅ 解決手順（ステップバイステップ）

### ⚠️ 重要な区別

Google Cloud Consoleには**2つの異なる設定**があります：

1. **OAuth同意画面 → 承認済みドメイン**
   - ドメイン名のみ（`oauth.n8n.cloud`）
   - `https://`や`http://`は**含めない**

2. **Credentials → OAuth 2.0 クライアントID → 承認済みのリダイレクトURI**
   - 完全なURL（`https://oauth.n8n.cloud/oauth2/callback`）
   - `https://`を含める

---

### Step 1: OAuth同意画面の設定（承認済みドメイン）

1. Google Cloud Console → **APIs & Services** → **OAuth同意画面**
2. 「**承認済みドメイン**」セクションを探す
3. 現在の設定を確認：
   - ❌ `https://oauth.n8n.cloud/oauth2/callback`（エラー）
   - ✅ `oauth.n8n.cloud`（正しい）

4. **修正方法**:
   - エラーが出ているドメインを削除
   - 「**+ ドメインの追加**」をクリック
   - 以下を入力（**スキームなし**）：
     ```
     oauth.n8n.cloud
     ```
   - 「**保存**」をクリック

**重要**:
- `https://`や`http://`は**含めない**
- パス（`/oauth2/callback`）も**含めない**
- ドメイン名のみ

---

### Step 2: OAuth 2.0 クライアントIDの設定（承認済みのリダイレクトURI）

1. Google Cloud Console → **APIs & Services** → **Credentials**
2. 「**OAuth 2.0 Client IDs**」セクションで、既存のクライアントIDを探す
   - クライアントID: `135718974606-htnvh8mlcfmofnh8reqk81b734j6fk8b.apps.googleusercontent.com`
3. 該当するOAuth 2.0 クライアントIDを**クリック**して編集画面を開く

4. 「**承認済みのリダイレクト URI**」セクションを探す
5. 「**+ URI を追加**」ボタンをクリック
6. 以下のURLを**正確に**入力：
   ```
   https://oauth.n8n.cloud/oauth2/callback
   ```
7. 「**保存**」をクリック

**重要**:
- こちらは**完全なURL**を入力
- `https://`を含める
- パス（`/oauth2/callback`）も含める
- URLは完全一致する必要があります

### Step 5: 設定確認

編集画面で以下が表示されていることを確認：

```yaml
承認済みのリダイレクト URI:
  ✅ https://oauth.n8n.cloud/oauth2/callback
```

### Step 6: n8n側で再認証

1. n8n Dashboardに戻る
2. 「**Credentials**」→「**Google account**」を開く
3. 「**Sign in with Google**」ボタンを再度クリック
4. 今度は正常に認証が完了するはずです

---

## 📸 設定画面の見つけ方

### Google Cloud Consoleでの確認方法

```
Google Cloud Console
  └─ APIs & Services
      └─ Credentials
          └─ OAuth 2.0 Client IDs
              └─ [あなたのクライアントID] ← ここをクリック
                  └─ 承認済みのリダイレクト URI ← ここに追加
```

---

## ⚠️ よくある間違い

### ❌ 間違った設定例

```yaml
❌ http://oauth.n8n.cloud/oauth2/callback
   → httpではなくhttpsを使用

❌ https://oauth.n8n.cloud/oauth2/callback/
   → 末尾にスラッシュ（/）を追加しない

❌ https://oauth.n8n.cloud/OAuth2/callback
   → 大文字小文字が間違っている

❌ https://oauth.n8n.cloud/oauth2/callback?param=value
   → クエリパラメータを追加しない
```

### ✅ 正しい設定

```yaml
✅ https://oauth.n8n.cloud/oauth2/callback
   → 完全一致
```

---

## 🔍 トラブルシューティング

### 問題1: クライアントIDが見つからない

**解決方法**:
1. 新規にOAuth 2.0 クライアントIDを作成
2. アプリケーションの種類: 「**ウェブアプリケーション**」を選択
3. 承認済みのリダイレクトURIに`https://oauth.n8n.cloud/oauth2/callback`を追加
4. Client IDとClient Secretをコピー
5. n8n側で新しい認証情報を作成

### 問題2: 保存しても反映されない

**解決方法**:
1. ブラウザのキャッシュをクリア
2. Google Cloud Consoleを再読み込み
3. 数分待ってから再度試す（反映に時間がかかる場合がある）

### 問題3: 複数のリダイレクトURIが必要な場合

**解決方法**:
- 複数のリダイレクトURIを設定する場合は、1行ずつ追加
- 例：
  ```
  https://oauth.n8n.cloud/oauth2/callback
  https://your-custom-domain.com/oauth2/callback
  ```

---

## ✅ 設定チェックリスト

### Google Cloud Console側

- [ ] OAuth 2.0 クライアントIDが作成されている
- [ ] 承認済みのリダイレクトURIに`https://oauth.n8n.cloud/oauth2/callback`が追加されている
- [ ] URLが完全一致している（大文字小文字、末尾のスラッシュなど）
- [ ] 保存が完了している

### n8n側

- [ ] Client IDが正しく入力されている
- [ ] Client Secretが正しく入力されている
- [ ] Scopeが正しく入力されている
- [ ] 「Sign in with Google」を再度実行

---

## 📚 参考資料

### Google公式ドキュメント

- [OAuth 2.0 リダイレクトURIの設定](https://developers.google.com/identity/protocols/oauth2/web-server#uri-validation)
- [OAuth 2.0 クライアントIDの作成](https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred)

### n8n公式ドキュメント

- [Google OAuth2 API認証](https://docs.n8n.io/integrations/builtin/credentials/google/oauth2-api/)

---

**作成日**: 2025-12-26
**バージョン**: 1.0
**ステータス**: エラー解決ガイド完了

