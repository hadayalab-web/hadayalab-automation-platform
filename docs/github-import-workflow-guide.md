# GitHubからn8nワークフローをインポートする方法

## 現状の制限

n8nの標準機能では、**GitHubリポジトリから直接ワークフローをインポートする機能は実装されていません**。

ただし、以下の方法でGitHubからワークフローをインポートできます：

## 方法1: GitHub Raw URLからインポート（推奨）

### 手順

1. **ワークフローJSONをGitHubにプッシュ**
   ```bash
   git add workflow-cursor-vercel-deploy.json
   git commit -m "Add Cursor-Vercel workflow"
   git push origin main
   ```

2. **GitHub Raw URLを取得**
   - GitHubリポジトリでJSONファイルを開く
   - 「Raw」ボタンをクリック
   - URLをコピー（例: `https://raw.githubusercontent.com/hadayalab-web/hadayalab-automation-platform/main/workflow-cursor-vercel-deploy.json`）

3. **n8nでインポート**
   - n8n Dashboard → Workflows → Import from URL（もし機能があれば）
   - または、Raw URLからJSONをダウンロードして「Import from File」でインポート

### n8nのURLインポート機能の確認

n8nの最新バージョンでは、URLから直接インポートできる機能があるかもしれません。以下を確認してください：

1. n8n Dashboard → Workflows
2. 「Import」ボタンをクリック
3. 「Import from URL」オプションがあるか確認

## 方法2: GitHubからダウンロードしてインポート

### 手順

1. **GitHubリポジトリでJSONファイルを開く**
   - `https://github.com/hadayalab-web/hadayalab-automation-platform/blob/main/workflow-cursor-vercel-deploy.json`

2. **Rawボタンをクリック**
   - ブラウザでJSONが表示される

3. **JSONをコピー**
   - 全選択（Ctrl+A）→ コピー（Ctrl+C）

4. **n8nでインポート**
   - n8n Dashboard → Workflows → Import from File
   - または、JSONをテキストファイルとして保存してインポート

## 方法3: n8n Templates機能を使用

n8nには**Community Templates**機能があり、GitHub上のテンプレートを検索・インポートできる可能性があります：

1. n8n Dashboard → Templates
2. 「Community Templates」を検索
3. GitHubリポジトリのURLを入力して検索

## 方法4: n8n MCPツール経由（自動化）

MCPツールを使用して、GitHubから直接ワークフローを取得してインポートするスクリプトを作成：

```python
# scripts/import-from-github.py
import urllib.request
import json

# GitHub Raw URLからワークフローを取得
github_raw_url = "https://raw.githubusercontent.com/hadayalab-web/hadayalab-automation-platform/main/workflow-cursor-vercel-deploy.json"

with urllib.request.urlopen(github_raw_url) as response:
    workflow_data = json.loads(response.read().decode('utf-8'))

# n8nにインポート（REST API経由）
# ...
```

## 推奨ワークフロー

### GitHub → n8n 自動同期

1. **GitHubにワークフローJSONをプッシュ**
2. **GitHub Actionsで自動インポート**（カスタムワークフロー作成）
   - GitHub Actionsからn8n REST APIを呼び出し
   - ワークフローを自動インポート

3. **n8n WebhookでGitHubイベントを受信**
   - GitHub Webhook → n8n Webhook Trigger
   - ワークフローを自動更新

## 今すぐ試せる方法

### クイックインポート（現在のワークフロー）

```bash
# 1. GitHub Raw URLを生成
# https://raw.githubusercontent.com/hadayalab-web/hadayalab-automation-platform/main/workflow-cursor-vercel-deploy.json

# 2. ブラウザで開いてJSONをコピー

# 3. n8n Dashboardでインポート
# Workflows → Import from File → JSONを貼り付け
```

## 今後の改善案

### n8nにGitHubインポート機能を追加

n8nのカスタムノードまたはワークフローで、GitHubから自動インポートする機能を実装：

1. **GitHub Webhook受信**
2. **変更されたJSONファイルを検出**
3. **n8n REST APIでワークフローを更新**

## 参考リンク

- [n8n Documentation - Import/Export](https://docs.n8n.io/workflows/import-export/)
- [n8n GitHub Repository](https://github.com/n8n-io/n8n)
- [n8n Community Templates](https://n8n.io/workflows/)















