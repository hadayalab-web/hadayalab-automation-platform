# 🔐 Google OAuth設定完全ガイド（2つの設定を区別）

## 📋 概要

Google OAuth設定には**2つの異なる設定画面**があり、それぞれ入力形式が違います。混同しやすいので、明確に区別して設定する必要があります。

---

## ⚠️ 2つの設定の違い

### 設定1: OAuth同意画面 → 承認済みドメイン

**場所**: Google Cloud Console → APIs & Services → **OAuth同意画面**

**入力形式**: **ドメイン名のみ**（スキームなし、パスなし）

```yaml
✅ 正しい入力:
  oauth.n8n.cloud

❌ 間違った入力:
  https://oauth.n8n.cloud/oauth2/callback
  → エラー: "無効なドメイン: スキーム (http:// または https://) を指定することはできません"
```

**目的**: アプリが使用するドメインを事前登録

---

### 設定2: Credentials → OAuth 2.0 クライアントID → 承認済みのリダイレクトURI

**場所**: Google Cloud Console → APIs & Services → **Credentials** → OAuth 2.0 クライアントID

**入力形式**: **完全なURL**（スキーム含む、パス含む）

```yaml
✅ 正しい入力:
  https://oauth.n8n.cloud/oauth2/callback

❌ 間違った入力:
  oauth.n8n.cloud
  → エラー: redirect_uri_mismatch
```

**目的**: OAuth認証後のリダイレクト先URLを指定

---

## ✅ 完全な設定手順

### Part 1: OAuth同意画面の設定

#### Step 1-1: OAuth同意画面を開く

1. https://console.cloud.google.com/ にアクセス
2. プロジェクトを選択
3. 左メニュー → **APIs & Services** → **OAuth同意画面**

#### Step 1-2: 承認済みドメインを設定

1. 「**承認済みドメイン**」セクションを探す
2. 既存のエラーが出ているドメインを削除（`https://oauth.n8n.cloud/oauth2/callback`など）
3. 「**+ ドメインの追加**」をクリック
4. 以下を入力（**スキームなし、パスなし**）：
   ```
   oauth.n8n.cloud
   ```
5. 「**保存**」をクリック

**確認ポイント**:
- ✅ エラーメッセージが消えている
- ✅ ドメイン名のみが表示されている

#### Step 1-3: その他の設定（オプション）

```yaml
アプリ名: n8n
ユーザーサポートメール: admin@cryptotradeacademy.io
デベロッパーの連絡先情報: hadayalab@gmail.com

推奨設定（オプション）:
  - アプリケーションのホームページ: （設定推奨）
  - プライバシーポリシーリンク: （設定推奨）
  - 利用規約リンク: （設定推奨）
```

---

### Part 2: OAuth 2.0 クライアントIDの設定

#### Step 2-1: Credentials画面を開く

1. 左メニュー → **APIs & Services** → **Credentials**
2. 「**OAuth 2.0 Client IDs**」セクションを探す
3. 既存のクライアントIDをクリック（または新規作成）

#### Step 2-2: 承認済みのリダイレクトURIを設定

1. 編集画面で「**承認済みのリダイレクト URI**」セクションを探す
2. 「**+ URI を追加**」ボタンをクリック
3. 以下のURLを**正確に**入力（**完全なURL**）：
   ```
   https://oauth.n8n.cloud/oauth2/callback
   ```
4. 「**保存**」をクリック

**確認ポイント**:
- ✅ `https://`が含まれている
- ✅ パス（`/oauth2/callback`）が含まれている
- ✅ 完全一致している

---

### Part 3: n8n側の設定

#### Step 3-1: n8n Credentials設定

1. n8n Dashboard → **Credentials** → **Google account**
2. 以下を設定：

```yaml
Client ID:
  135718974606-htnvh8mlcfmofnh8reqk81b734j6fk8b.apps.googleusercontent.com

Client Secret:
  （Google Cloud Consoleから取得したSecret）

Scope:
  https://www.googleapis.com/auth/drive
  https://www.googleapis.com/auth/calendar
  https://www.googleapis.com/auth/gmail.send
  https://www.googleapis.com/auth/gmail.readonly
  https://www.googleapis.com/auth/spreadsheets
  https://www.googleapis.com/auth/youtube.readonly
```

#### Step 3-2: 認証実行

1. 「**Sign in with Google**」ボタンをクリック
2. Googleアカウントでログイン
3. 権限を承認
4. 認証が完了することを確認

---

## 🔍 トラブルシューティング

### エラー1: "無効なドメイン: スキーム (http:// または https://) を指定することはできません"

**原因**: OAuth同意画面の「承認済みドメイン」に`https://`を含めている

**解決方法**:
- `https://oauth.n8n.cloud/oauth2/callback` → `oauth.n8n.cloud`に変更
- スキーム（`https://`）とパス（`/oauth2/callback`）を削除

---

### エラー2: "redirect_uri_mismatch"

**原因**: Credentials側の「承認済みのリダイレクトURI」が設定されていない、または不一致

**解決方法**:
1. Credentials → OAuth 2.0 クライアントIDを開く
2. 「承認済みのリダイレクトURI」に`https://oauth.n8n.cloud/oauth2/callback`を追加
3. 完全一致していることを確認（大文字小文字、末尾のスラッシュなど）

---

### エラー3: 両方の設定が混在している

**症状**: OAuth同意画面に完全なURLを入力してしまった

**解決方法**:
1. OAuth同意画面の「承認済みドメイン」を確認
2. `https://`やパスが含まれている場合は削除
3. ドメイン名のみ（`oauth.n8n.cloud`）に修正

---

## 📊 設定チェックリスト

### OAuth同意画面

- [ ] 承認済みドメインに`oauth.n8n.cloud`が設定されている（スキームなし）
- [ ] エラーメッセージが表示されていない
- [ ] アプリ名、サポートメールが設定されている

### Credentials → OAuth 2.0 クライアントID

- [ ] 承認済みのリダイレクトURIに`https://oauth.n8n.cloud/oauth2/callback`が設定されている（完全なURL）
- [ ] Client IDとClient Secretが正しく設定されている

### n8n側

- [ ] Client IDが正しく入力されている
- [ ] Client Secretが正しく入力されている
- [ ] Scopeが正しく入力されている
- [ ] 「Sign in with Google」で認証が成功する

---

## 🎯 まとめ

```yaml
OAuth同意画面 → 承認済みドメイン:
  入力: oauth.n8n.cloud
  形式: ドメイン名のみ（スキームなし、パスなし）

Credentials → 承認済みのリダイレクトURI:
  入力: https://oauth.n8n.cloud/oauth2/callback
  形式: 完全なURL（スキーム含む、パス含む）
```

**この2つを区別して設定すれば、エラーは解消されます！**

---

**作成日**: 2025-12-26
**バージョン**: 1.0
**ステータス**: 完全ガイド完了




