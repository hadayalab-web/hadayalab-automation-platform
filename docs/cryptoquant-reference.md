# CryptoQuant API リファレンス

このドキュメントは、CryptoQuant APIの公式ドキュメントとカタログへのクイックアクセスを提供します。

## 📚 公式リファレンス

### API ドキュメント
- **URL**: https://cryptoquant.com/docs
- **説明**: CryptoQuant APIの完全なドキュメント
- **用途**: APIエンドポイント、認証方法、リクエスト/レスポンス形式の確認

### API カタログ
- **URL**: https://cryptoquant.com/catalog
- **説明**: 利用可能なすべてのAPIエンドポイントとデータセットのカタログ
- **用途**: 利用可能なデータセットの検索、エンドポイントの一覧確認

---

## 📂 ローカルドキュメントの場所

### 既存のドキュメント（cryptosignal-aiプロジェクト）

既に保存されているドキュメントが以下の場所にあります：

```
C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs\
├── API Docs _ CryptoQuant.html      # APIドキュメント
├── Catalog _ CryptoQuant.html       # APIカタログ
└── [関連ファイル]
```

**Cursorはこのディレクトリ内のファイルを自動的に参照できます。**

### 現在のプロジェクトでの参照

現在のプロジェクト（hadayalab-automation-platform）からも、上記のディレクトリを参照できます。

Cursor Chatで以下のように参照できます：

```
「C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs のドキュメントを確認して」
「CryptoQuantのAPIドキュメントを参照して」
「CryptoQuantのカタログからエンドポイントを探して」
```

---

## 🔄 Cursorが参照できるようにする方法

### 既存のドキュメントを使用（推奨）

既に `C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs\` にドキュメントが保存されているため、追加の作業は不要です。

Cursorは以下の方法で自動的に参照できます：

1. **直接パス指定**
   ```
   「C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs\API Docs _ CryptoQuant.html を確認して」
   ```

2. **ディレクトリ指定**
   ```
   「C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs の内容を確認して」
   ```

3. **自然な質問**
   ```
   「CryptoQuantのAPIドキュメントを参照して」
   「CryptoQuantのカタログからエンドポイントを探して」
   ```

### 現在のプロジェクトにコピーする場合（オプション）

現在のプロジェクト内にもドキュメントを保存したい場合：

1. **シンボリックリンクを作成**（推奨）
   ```powershell
   # プロジェクトルートから実行
   New-Item -ItemType SymbolicLink -Path "docs\cryptoquant-docs" -Target "C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs"
   ```

2. **または、ファイルをコピー**
   ```powershell
   Copy-Item -Path "C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs\*" -Destination "docs\cryptoquant-docs\" -Recurse
   ```

---

## 🔗 クイックアクセス

### ブラウザブックマーク
以下のURLをブラウザのブックマークに追加することを推奨します：

```
📖 CryptoQuant Docs: https://cryptoquant.com/docs
📦 CryptoQuant Catalog: https://cryptoquant.com/catalog
```

### VS Code / Cursor クイックオープン
このファイルを開くには：
- `Ctrl+P` (Windows) / `Cmd+P` (Mac) を押す
- `cryptoquant-reference` と入力

---

## 📝 使用例

### API認証
```bash
# API Keyを使用した認証例
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.cryptoquant.com/v1/...
```

### よく使用するエンドポイント
（実際の使用時にカタログから確認してください）

---

## 🔄 更新方法

ドキュメントを更新する場合：

1. ブラウザで最新のドキュメントにアクセス
2. Cloudflareチャレンジを通過
3. ページを保存して `C:\Users\chiba\cryptosignal-ai\docs\cryptoquant-docs\` に上書き保存
4. Cursorが自動的に最新版を参照します

---

## 💡 ヒント

1. **既存のドキュメントを活用**: 既に保存されているドキュメントがあるため、追加の作業は不要です
2. **定期的な更新**: APIの更新があるため、定期的にドキュメントを更新することを推奨します
3. **検索しやすく**: CursorはHTMLファイルも検索できるため、そのまま使用できます

---

## 📞 サポート

- **公式ドキュメント**: https://cryptoquant.com/docs
- **サポート**: CryptoQuant公式サイトのサポートページを参照

---

## 🔄 更新履歴

- 2024-XX-XX: 既存のドキュメントディレクトリへの参照を追加
