# Phase 1: ワークフロー1のテストとデプロイ - 実装ガイド

## 📋 概要

**目標**: Trial Onboarding Automationワークフローをn8nにインポートし、テストして本番環境にデプロイする

**所要時間**: 2-3時間

**対象ファイル**: `workflow-1-trial-onboarding.json`

---

## ✅ チェックリスト

### ステップ1: n8nインスタンス準備（30分）
- [ ] n8nインスタンスにアクセスできることを確認
- [ ] n8n Dashboardにログイン
- [ ] ワークフロー作成権限があることを確認
- [ ] Credentials設定画面にアクセスできることを確認

### ステップ2: 認証情報の設定（30-45分）
- [ ] Gmail OAuth2認証を設定
- [ ] Whop API Keyを取得・設定
- [ ] 認証情報のテスト（各ノードで認証情報が選択できることを確認）

### ステップ3: ワークフロー1のインポートとテスト（1-1.5時間）
- [ ] workflow-1-trial-onboarding.json をインポート
- [ ] 各ノードの設定を確認
- [ ] 認証情報を各ノードに割り当て
- [ ] Manual Triggerでテスト実行
- [ ] Webhook TriggerのURLを確認
- [ ] Gmail送信のテスト（テスト用メールアドレスで）
- [ ] Wait Nodeの動作確認（短時間でテスト）
- [ ] Switch Nodeの分岐確認
- [ ] エラーがないか確認

### ステップ4: 本番環境デプロイ（30分）
- [ ] ワークフローをActive化
- [ ] Webhook URLをWhopに設定
- [ ] 監視設定（エラー通知など）
- [ ] 最終確認（実際のTrial開始でテスト）

---

## 🚀 詳細手順

### ステップ1: n8nインスタンス準備

#### 1.1 n8nインスタンスへのアクセス確認

**あなたのタスク:**
1. n8nインスタンスのURLにアクセス
2. ログインしてDashboardを開く
3. ワークフロー作成権限があることを確認

**確認ポイント:**
- [ ] n8n Dashboardが表示される
- [ ] 「Workflows」メニューが表示される
- [ ] 「Credentials」メニューが表示される

---

### ステップ2: 認証情報の設定

#### 2.1 Gmail OAuth2認証の設定

**あなたのタスク:**
1. n8n Dashboard → **Credentials** → **Add Credential**
2. **Gmail OAuth2 API** を選択
3. Google Cloud ConsoleでOAuth2認証情報を作成（必要に応じて）
4. Client ID、Client Secret、Redirect URLを設定
5. 認証を完了

**必要な情報:**
- Google Cloud Console プロジェクト
- OAuth2認証情報（Client ID、Client Secret）
- Redirect URL（n8nが提供）

**参考**: [n8n Gmail Node Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.gmail/)

#### 2.2 Whop API Keyの取得・設定

**あなたのタスク:**
1. Whop Dashboard → API Settings
2. API Keyを生成
3. n8n Dashboard → **Credentials** → **Add Credential**
4. **HTTP Header Auth** または **HTTP Request** を選択
5. API Keyを設定（`Authorization: Bearer YOUR_API_KEY` 形式）

**必要な情報:**
- Whop API Key
- APIエンドポイント（`https://api.whop.com/api/v2/`）

**参考**: [Whop API Documentation](https://docs.whop.com/)

#### 2.3 認証情報のテスト

**あなたのタスク:**
1. 各認証情報が正しく設定されているか確認
2. 新しいワークフローを作成
3. Gmail Nodeを追加して、認証情報が選択できることを確認
4. HTTP Request Nodeを追加して、認証情報が選択できることを確認

---

### ステップ3: ワークフロー1のインポートとテスト

#### 3.1 ワークフローのインポート

**あなたのタスク:**
1. n8n Dashboard → **Workflows** → **Import from File**
2. `workflow-1-trial-onboarding.json` を選択
3. インポート完了を確認

**確認ポイント:**
- [ ] ワークフローが正しくインポートされた
- [ ] すべてのノードが表示されている
- [ ] ノード間の接続が正しい

#### 3.2 各ノードの設定確認

**あなたのタスク:**
1. 各ノードを開いて設定を確認
2. 認証情報を各ノードに割り当て

**確認すべきノード:**
- **Webhook Trigger**: Pathが `whop-trial-started` であることを確認
- **Gmail Node**: Gmail OAuth2認証を割り当て
- **HTTP Request Node**: Whop API Key認証を割り当て
- **Switch Node**: 6市場分岐（EN/AR/KO/JA/ES/PT-BR）を確認

#### 3.3 Manual Triggerでのテスト実行

**あなたのタスク:**
1. ワークフローを保存
2. **Execute Workflow** ボタンをクリック
3. Manual Triggerでテストデータを入力：
   ```json
   {
     "body": {
       "user_email": "test@example.com",
       "user_name": "Test User",
       "market": "EN",
       "trial_start_time": "2025-12-23T10:00:00Z",
       "membership_id": "test_membership_id"
     }
   }
   ```
4. 実行結果を確認
5. 各ノードが正しく実行されることを確認

**確認ポイント:**
- [ ] Webhook Triggerが正しく動作する
- [ ] Switch Nodeが正しく分岐する（EN市場）
- [ ] Gmail Nodeが正しく動作する（テスト用メールアドレスで確認）
- [ ] エラーがない

#### 3.4 Webhook Triggerのテスト

**あなたのタスク:**
1. ワークフローをActive化（一時的）
2. Webhook URLを確認（例: `https://your-n8n-instance.com/webhook/whop-trial-started`）
3. PostmanやcurlでWebhookをテスト：
   ```bash
   curl -X POST https://your-n8n-instance.com/webhook/whop-trial-started \
     -H "Content-Type: application/json" \
     -d '{
       "user_email": "test@example.com",
       "user_name": "Test User",
       "market": "EN",
       "trial_start_time": "2025-12-23T10:00:00Z",
       "membership_id": "test_membership_id"
     }'
   ```
4. ワークフローが実行されることを確認

#### 3.5 Wait Nodeの動作確認（短時間でテスト）

**あなたのタスク:**
1. Wait Nodeの設定を一時的に変更（テスト用）
   - 6時間 → 1分
   - 12時間 → 2分
2. ワークフローを実行
3. Wait Nodeが正しく動作することを確認
4. 元の設定に戻す（本番用）

**注意**: 本番環境では6時間、12時間に戻すことを忘れずに

#### 3.6 Switch Nodeの分岐確認

**あなたのタスク:**
1. 各市場（EN/AR/KO/JA/ES/PT-BR）でテスト実行
2. 正しい分岐に進むことを確認
3. 各市場用のGmail Nodeが正しく動作することを確認

---

### ステップ4: 本番環境デプロイ

#### 4.1 ワークフローをActive化

**あなたのタスク:**
1. ワークフローを保存
2. **Active** トグルをONにする
3. ワークフローがActive状態であることを確認

#### 4.2 Webhook URLをWhopに設定

**あなたのタスク:**
1. n8n DashboardでWebhook URLを確認
2. Whop Dashboard → Webhooks設定
3. Trial StartedイベントのWebhook URLを設定
4. テスト送信で動作確認

**Webhook URL例:**
```
https://your-n8n-instance.com/webhook/whop-trial-started
```

#### 4.3 監視設定

**あなたのタスク:**
1. n8n Dashboard → **Settings** → **Error Workflow** を設定（推奨）
2. エラー通知を設定（Email/Slackなど）
3. 実行ログを確認できるようにする

#### 4.4 最終確認

**あなたのタスク:**
1. 実際のTrial開始でテスト（可能であれば）
2. Welcome Emailが送信されることを確認
3. 6時間後にValue Emailが送信されることを確認（時間がかかるため、短時間テスト推奨）
4. エラーがないことを確認

---

## ⚠️ トラブルシューティング

### よくある問題

#### 1. ワークフローがインポートできない
- **原因**: JSON形式のエラー
- **解決**: `workflow-1-trial-onboarding.json` の形式を確認

#### 2. 認証情報が選択できない
- **原因**: 認証情報の設定が不完全
- **解決**: Credentials画面で認証情報を再設定

#### 3. Gmail送信が失敗する
- **原因**: OAuth2認証の問題
- **解決**: Gmail認証を再設定、スコープを確認

#### 4. Webhookが動作しない
- **原因**: Webhook URLが間違っている、またはワークフローがActiveでない
- **解決**: Webhook URLを確認、ワークフローをActive化

#### 5. Wait Nodeが動作しない
- **原因**: n8nインスタンスが継続実行中でない
- **解決**: n8n Cloudの場合は実行時間制限を確認、Self-hostedの場合はプロセスが実行中であることを確認

---

## 📞 サポートが必要な場合

以下の情報を準備して、GitHub Copilotに質問してください：

1. **エラーメッセージ**: n8n DashboardのExecutions画面からエラーメッセージをコピー
2. **実行ログ**: 失敗した実行のログを確認
3. **設定内容**: 問題が発生しているノードの設定を確認

**質問例:**
```
@copilot n8nワークフローのインポートでエラーが発生しています。
エラーメッセージ: [エラーメッセージを貼り付け]
どのように修正すればよいですか？
```

---

## ✅ 完了確認

Phase 1が完了したら、以下を確認：

- [ ] ワークフロー1がn8nにインポートされている
- [ ] 認証情報が正しく設定されている
- [ ] Manual Triggerでテスト実行が成功している
- [ ] Webhook Triggerでテスト実行が成功している
- [ ] ワークフローがActive化されている
- [ ] Webhook URLがWhopに設定されている
- [ ] 実際のTrial開始で動作確認ができている（可能であれば）

---

**次のステップ**: Phase 1完了後、Phase 2（ワークフロー2-5の実装）に進みます。

**作成日**: 2025-12-23
**ステータス**: 実装準備完了


