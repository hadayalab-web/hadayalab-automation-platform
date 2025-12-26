# アフィリエイター候補抽出スクリプト 実行ガイド

**作成日**: 2025-12-26
**目的**: Cursorが固まらないようにスクリプトを実行する方法

---

## ⚠️ 問題

スクリプトを直接実行すると、多数のAPI呼び出しとログ出力によりCursorが固まってしまう可能性があります。

---

## ✅ 推奨実行方法

### 方法1: PowerShellスクリプトを使用（推奨）

**実行コマンド**:
```powershell
cd C:\Users\chiba\hadayalab-automation-platform
.\scripts\run-affiliate-extraction.ps1
```

**特徴**:
- ✅ 出力をログファイルに保存
- ✅ コンソールにも進捗を表示
- ✅ Cursorが固まりにくい

**出力先**:
- ログファイル: `affiliate_extraction_output_YYYYMMDD_HHMMSS.log`
- JSONファイル: `affiliate_candidates_YYYYMMDD_HHMMSS.json`

---

### 方法2: コマンドプロンプトで実行

**実行コマンド**:
```cmd
cd C:\Users\chiba\hadayalab-automation-platform
set XAI_API_KEY=xai-xxxxxxxxxxxxx
python scripts\grok-x-affiliate-extraction.py > extraction.log 2>&1
```

**出力確認**:
```cmd
type extraction.log
```

---

### 方法3: バックグラウンドで実行（Windows）

**実行コマンド**:
```powershell
$apiKey = (Get-Content "C:\Users\chiba\Downloads\XAI_API_KEY.txt" -Raw -Split "`n")[1].Trim()
$env:XAI_API_KEY = $apiKey
Start-Process python -ArgumentList "scripts\grok-x-affiliate-extraction.py" -NoNewWindow -RedirectStandardOutput "extraction.log" -RedirectStandardError "extraction_error.log"
```

---

## 🔧 スクリプトの改善内容

### 1. 出力の簡略化

**変更前**:
```python
print(f"[INFO] Calling Grok AI for query: {search_query} (Market: {market_code})")
```

**変更後**:
```python
print(f"[INFO] Query: {search_query[:40]}... (Market: {market_code})")
```

### 2. タイムアウト時間の短縮

**変更前**: `timeout=60`秒
**変更後**: `timeout=30`秒 + リトライ機能

### 3. エラーメッセージの簡略化

**変更前**: 詳細なエラーメッセージを出力
**変更後**: エラータイプのみを出力（デバッグ情報は最小限）

### 4. 進捗表示の改善

**追加**:
```python
print(f"  Progress: {processed_x_queries}/{total_x_queries} queries")
```

---

## ⏱️ 実行時間の目安

**総API呼び出し数**: 約50-70回
**各API呼び出し間隔**: 2秒
**タイムアウト時**: 30秒 + リトライ（最大2回）

**予想実行時間**:
- **正常時**: 約5-10分
- **タイムアウト多発時**: 約15-20分

---

## 📊 実行結果

### 正常終了時の出力

```
============================================================
抽出結果サマリー
============================================================
総候補数: 198

  X (Twitter): 121 候補
  Telegram: 77 候補

  EN: 58 候補 (X: 45, Telegram: 13)
  AR: 33 候補 (X: 20, Telegram: 13)
  ...
```

### 出力ファイル

1. **JSONファイル**: `affiliate_candidates_YYYYMMDD_HHMMSS.json`
   - 全候補データ（構造化）

2. **ログファイル**: `affiliate_extraction_output_YYYYMMDD_HHMMSS.log`（PowerShellスクリプト使用時）
   - 実行ログ全体

---

## 🔍 トラブルシューティング

### 問題1: タイムアウトが多い

**原因**: APIサーバーの負荷が高い

**対処**:
- 実行時間を変更（サーバー負荷が低い時間帯に実行）
- タイムアウト時間を延長（`timeout=30` → `timeout=60`）

### 問題2: Cursorが固まる

**対処**:
- PowerShellスクリプトを使用（方法1）
- コマンドプロンプトで実行（方法2）
- バックグラウンドで実行（方法3）

### 問題3: API Keyエラー

**対処**:
```powershell
# XAI_API_KEY.txtの内容を確認
Get-Content "C:\Users\chiba\Downloads\XAI_API_KEY.txt"

# 環境変数を確認
echo $env:XAI_API_KEY
```

---

## 📝 次のステップ

1. ✅ スクリプト実行完了後、JSONファイルを確認
2. ✅ Google Sheets API統合（データベース化）
3. ✅ n8nワークフロー実装（週次自動実行）
4. ✅ 重複排除ロジック実装

---

**最終更新**: 2025-12-26
**ステータス**: ✅ 改善完了

