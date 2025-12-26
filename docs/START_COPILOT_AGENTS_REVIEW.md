# GitHub Copilot Agents レビュー開始手順

## ⚠️ 重要: GitHub Copilot Agentsは手動で起動する必要があります

GitHub Copilot Agentsは、GitHub.com上で手動で起動する必要があります。CLI経由では自動起動しません。

## 🚀 レビューを開始する手順

### ステップ1: GitHub.comにアクセス

1. **Issue #1を開く**
   - https://github.com/hadayalab-web/hadayalab-automation-platform/issues/1
   - または、ブラウザで直接アクセス

### ステップ2: GitHub Copilot Chatを開く

1. **サイドバーのCopilotアイコンをクリック**
   - または、`@` キーを押す
   - または、コメント欄で `@copilot` と入力

2. **GitHub Copilot Chatパネルが開く**

### ステップ3: レビュー依頼を入力

以下のコマンドをコピー＆ペースト：

```
@copilot Issue #1のレビュー依頼内容を確認して、以下のファイルをレビューしてください:

1. n8n-workflows-design.md - n8nワークフロー設計の妥当性を確認
2. workflow-1-trial-onboarding.json - JSON形式の正確性とn8nインポート可能性を確認
3. README-n8n-implementation.md - 実装ガイドの完全性を確認

特に以下の点を重点的にレビューしてください:
- Wait Nodeの長時間待機（6時間、12時間）の実装方法が適切か（n8n Cloudでの実行時間制限を考慮）
- Switch Nodeの6市場分岐（EN/AR/KO/JA/ES/PT-BR）の実装が効率的か
- 式（expressions）の記述が正しいか（例: {{ $json.body.user_email || $json.body.data?.user_email }}）
- エラーハンドリングが適切か（Try-Catch NodeまたはError Triggerの追加が必要か）
- セキュリティ設定が適切か（API Key管理、Webhook認証、データ暗号化の必要性）

既知の問題:
- Wait Nodeの長時間待機はn8nインスタンスが継続実行中である必要がある
- エラーハンドリングノードが未実装
- API Keyがプレースホルダー使用中

改善提案と具体的な修正方法を教えてください。レビュー結果はこのIssueにコメントしてください。
```

### ステップ4: 送信

1. **Enterキーを押す** または **送信ボタンをクリック**
2. **GitHub Copilot Agentsが自動でレビューを開始**

## 🔍 レビュー開始の確認方法

### 確認ポイント

1. **GitHub Copilot Chatで応答が表示される**
   - "Reviewing..." などのメッセージが表示される
   - レビューが進行中であることが確認できる

2. **Issue #1のコメント欄に新しいコメントが追加される**
   - GitHub Copilot Agentsからの回答がコメントとして追加される

3. **GitHub Copilot Agentsパネルでタスクが表示される**
   - ナビゲーションバーの「Agents」をクリック
   - 実行中のタスクが表示される

## ⚠️ レビューが開始されない場合の対処法

### 1. GitHub Copilot Proの確認

- GitHub Copilot Proのサブスクリプションが必要
- Settings → Copilot で確認
- https://github.com/settings/copilot

### 2. リポジトリへのアクセス権限確認

- 書き込み権限が必要
- リポジトリのSettings → Collaborators で確認

### 3. Issueの割り当て確認

- IssueにCopilotが割り当てられているか確認
- 割り当てられていない場合は手動で割り当て

### 4. コメントの形式確認

- `@copilot` を必ずメンション
- 明確な指示を含める
- レビュー対象ファイルを明記

## 📋 代替方法: Issueコメントで直接依頼

GitHub Copilot Chatが開けない場合は、Issue #1のコメント欄に直接以下を入力：

```markdown
@copilot このIssueのレビュー依頼内容を確認して、n8n-workflows-design.md、workflow-1-trial-onboarding.json、README-n8n-implementation.mdをレビューしてください。

特に以下の点を重点的にレビューしてください:
1. Wait Nodeの長時間待機（6時間、12時間）の実装方法
2. Switch Nodeの6市場分岐の効率性
3. 式（expressions）の記述が正しいか
4. エラーハンドリングが適切か
5. セキュリティ設定が適切か

改善提案と具体的な修正方法を教えてください。
```

## 🎯 現在の状況

- **Issue #1**: OPEN
- **URL**: https://github.com/hadayalab-web/hadayalab-automation-platform/issues/1
- **コメント**: レビュー依頼コメント追加済み（2件）
- **次のステップ**: GitHub.com上でGitHub Copilot Chatを開いてレビュー依頼を送信

---

**作成日**: 2025-12-23
**目的**: GitHub Copilot Agentsを手動で起動するための詳細ガイド





















