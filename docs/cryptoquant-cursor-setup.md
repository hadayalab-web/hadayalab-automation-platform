# CryptoQuant ドキュメント - Cursor参照設定ガイド

このガイドでは、CryptoQuantのAPIドキュメントとカタログをCursorが参照できるように設定する方法を説明します。

## 🎯 目的

Cloudflareのセキュリティチャレンジにより、Cursorが直接Webサイトにアクセスできないため、ドキュメントをローカルに保存してCursorが参照できるようにします。

---

## ✅ 既存のドキュメント

**良いニュース**: 既にドキュメントが保存されています！

以下のディレクトリにCryptoQuantのドキュメントが保存されています：

```
C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs\
├── API Docs _ CryptoQuant.html      # APIドキュメント
├── Catalog _ CryptoQuant.html       # APIカタログ
└── [関連ファイル]
```

**Cursorはこのディレクトリ内のファイルを自動的に参照できます。**

---

## 🔍 Cursorでの参照方法

### 方法1: 直接パス指定

```
「C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs\API Docs _ CryptoQuant.html を確認して」
「C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs\Catalog _ CryptoQuant.html を確認して」
```

### 方法2: ディレクトリ指定

```
「C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs の内容を確認して」
「C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs からCryptoQuantのAPI情報を探して」
```

### 方法3: 自然な質問（推奨）

```
「CryptoQuantのAPIドキュメントを参照して」
「CryptoQuantのカタログからエンドポイントを探して」
「CryptoQuantのAPIで認証方法を教えて」
「CryptoQuantのAPIでBitcoinのデータを取得する方法を教えて」
```

Cursorは自動的に該当するファイルを検索・参照します。

---

## 🔄 現在のプロジェクトに統合する方法（オプション）

現在のプロジェクト（hadayalab-automation-platform）内からも簡単に参照できるようにする場合：

### 方法A: シンボリックリンクを作成（推奨）

```powershell
# プロジェクトルートから実行
New-Item -ItemType SymbolicLink `
  -Path "docs\cryptoquant-docs" `
  -Target "C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs"
```

これにより、`docs\cryptoquant-docs` から既存のドキュメントにアクセスできます。

### 方法B: ファイルをコピー

```powershell
# プロジェクトルートから実行
# ディレクトリを作成
New-Item -ItemType Directory -Path "docs\cryptoquant-docs" -Force

# ファイルをコピー
Copy-Item -Path "C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs\*" `
  -Destination "docs\cryptoquant-docs\" -Recurse -Force
```

**注意**: この方法では、元のファイルとコピーが別々になるため、更新時に両方を更新する必要があります。

---

## 🔄 更新方法

ドキュメントを更新する場合：

1. ブラウザで https://cryptoquant.com/docs にアクセス
2. Cloudflareチャレンジを通過
3. ページを保存して `C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs\` に上書き保存
4. Cursorが自動的に最新版を参照します

---

## 💡 ヒント

### Cursorでの検索を最適化

1. **具体的な質問**: 「CryptoQuantのAPIで」という接頭辞を使うと、Cursorが適切なファイルを検索しやすくなります

2. **エンドポイント名を指定**: 特定のエンドポイントについて質問する場合、名前を明示すると検索精度が上がります

3. **カテゴリを指定**: 「Bitcoin」「Ethereum」などのカテゴリを指定すると、カタログから適切な情報を見つけやすくなります

### トラブルシューティング

**Cursorがドキュメントを参照できない場合:**

1. **パスを確認**: ファイルが正しい場所にあるか確認
   ```
   C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs\API Docs _ CryptoQuant.html
   ```

2. **明示的にパスを指定**: 直接パスを指定して参照
   ```
   「C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs\API Docs _ CryptoQuant.html を確認して」
   ```

3. **ファイル名を確認**: ファイル名にスペースが含まれているため、必要に応じて引用符で囲む

---

## ✅ 完了チェックリスト

- [x] 既存のドキュメントを確認（`C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs\`）
- [ ] Cursorで動作確認（任意の質問でテスト）
- [ ] 必要に応じてシンボリックリンクを作成（オプション）

---

## 🔗 関連ドキュメント

- [CryptoQuant API リファレンス](./cryptoquant-reference.md) - クイックリファレンス
- [CryptoQuant ドキュメント保存ディレクトリ](./cryptoquant-docs/README.md) - ディレクトリの説明（新規保存用）

---

**最終更新**: 2024-XX-XX
