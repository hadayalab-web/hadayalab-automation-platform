# GitHub Copilot Agents/Copilot → n8nワークフロー実行 SSOT

**最終更新**: 2025-01-24
**最終検証**: 2025-01-24（設計）
**バージョン**: 1.0.0
**メンテナー**: HadayaLab

---

## 📚 公式リファレンス

- **GitHub Copilot Agents**: [GitHub Copilot Agents Documentation](https://docs.github.com/ja/copilot/responsible-use/copilot-coding-agent)
- **GitHub Actions**: [GitHub Actions Documentation](https://docs.github.com/ja/actions)
- **n8n API**: [n8n API Documentation](https://docs.n8n.io/api/)
- **n8n MCP**: [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)

---

## 🎯 設計方針

**GitHub Copilot Agents/Copilotがn8nワークフローを実行する仕組み**

このドキュメントは、GitHub Copilot Agents/Copilotが「Actions」機能を使用してn8nワークフローを実行する仕組みを設計した**唯一の信頼できる情報源（SSOT）**です。

### 核心理念

**「ユーザー → AI（私、司令塔） → GitHub Copilot Agents/Copilot → GitHub Actions → n8nワークフロー → 結果報告 → AI（私）検証 → ユーザー」**

GitHub Copilot Agents/Copilotを実行役として活用し、GitHub Actions経由でn8nワークフローを実行します。

---

## 🔄 完全自動化ワークフロー

### ワークフロー1: ユーザー → AI → GitHub Copilot Agents → Actions → n8nワークフロー

**目的**: ユーザーがCursor Chatで指示を出すと、AI（私）がGitHub Copilot Agentsに指示を出し、GitHub Actions経由でn8nワークフローを実行する

**実行フロー**:

```
1. ユーザーがCursor Chatで指示
   「このデータを処理するn8nワークフローを実行して」
   ↓
2. AI（私、司令塔）がGitHub Copilot Agents/Copilotへ指示
   - GitHub APIでIssue/PRを作成
   - @copilotメンション付きコメントを自動追加
   - 実行すべきn8nワークフローとパラメータを指定
   ↓
3. GitHub Copilot Agents/CopilotがActionsを実行
   - GitHub Actionsワークフローを起動
   - n8nワークフロー実行用のパラメータを渡す
   ↓
4. GitHub Actionsがn8nワークフローを実行
   - n8n APIを使用してワークフローを実行
   - 実行結果を取得
   ↓
5. GitHub Actionsが結果をGitHub Copilot Agents/Copilotへ報告
   - Issue/PRにコメントとして結果を追加
   ↓
6. GitHub Copilot Agents/CopilotがAI（私）へ報告
   - 実行結果をIssue/PRに記録
   ↓
7. AI（私）が結果を検証
   - 実行結果の品質を確認
   - エラーがないか確認
   - 追加指示が必要か判断
   ↓
8a. 追加指示が必要な場合
    - AI（私）がGitHub Copilot Agents/Copilotに追加指示
    - ステップ3に戻る（最大3回まで）
   ↓
8b. 完了した場合
    - AI（私）が結果を整理
    - ユーザーに完了報告
    - 実行結果をCursor Chatに表示
```

---

## 🔧 実装詳細

### GitHub Actionsワークフロー設計

#### ワークフロー1: n8nワークフロー実行（GitHub Copilot Agents/Copilot経由）

**ファイル**: `.github/workflows/n8n-workflow-executor.yml`

**トリガー**:
- Issueコメント（`@copilot`メンション + 特定のキーワード）
- PRコメント（`@copilot`メンション + 特定のキーワード）
- 手動実行（workflow_dispatch）

**ワークフロー構造**:

```yaml
name: Execute n8n Workflow (via Copilot)

on:
  issue_comment:
    types: [created]
  pull_request:
    types: [opened, synchronize]
  workflow_dispatch:
    inputs:
      workflow_name:
        description: 'n8nワークフロー名'
        required: true
      workflow_params:
        description: 'n8nワークフローパラメータ（JSON形式）'
        required: false

jobs:
  execute-n8n-workflow:
    runs-on: ubuntu-latest
    steps:
      - name: Check if Copilot triggered
        id: check-copilot
        uses: actions/github-script@v7
        with:
          script: |
            const comment = context.payload.comment?.body || '';
            const isCopilot = comment.includes('@copilot') ||
                            context.actor === 'github-actions[bot]';
            const hasN8nCommand = comment.includes('n8n') ||
                                 comment.includes('ワークフロー実行');
            return { isCopilot, hasN8nCommand };

      - name: Parse n8n workflow command
        id: parse-command
        if: steps.check-copilot.outputs.isCopilot == 'true'
        uses: actions/github-script@v7
        with:
          script: |
            const comment = context.payload.comment?.body || '';
            // n8nワークフロー名とパラメータを抽出
            const workflowMatch = comment.match(/n8nワークフロー[：:]\s*(\w+)/);
            const paramsMatch = comment.match(/パラメータ[：:]\s*({.*})/);

            const workflowName = workflowMatch ? workflowMatch[1] :
                                github.event.inputs?.workflow_name || 'default';
            const params = paramsMatch ? JSON.parse(paramsMatch[1]) :
                          github.event.inputs?.workflow_params ?
                          JSON.parse(github.event.inputs.workflow_params) : {};

            return { workflowName, params: JSON.stringify(params) };

      - name: Execute n8n workflow
        id: execute-n8n
        if: steps.check-copilot.outputs.isCopilot == 'true'
        env:
          N8N_API_URL: ${{ secrets.N8N_API_URL }}
          N8N_API_KEY: ${{ secrets.N8N_API_KEY }}
        run: |
          WORKFLOW_NAME="${{ steps.parse-command.outputs.workflowName }}"
          WORKFLOW_PARAMS="${{ steps.parse-command.outputs.params }}"

          # n8nワークフローIDを取得
          WORKFLOW_ID=$(curl -s -X GET \
            "$N8N_API_URL/api/v1/workflows" \
            -H "X-N8N-API-KEY: $N8N_API_KEY" \
            | jq -r ".data[] | select(.name == \"$WORKFLOW_NAME\") | .id")

          # n8nワークフローを実行
          EXECUTION_ID=$(curl -s -X POST \
            "$N8N_API_URL/api/v1/workflows/$WORKFLOW_ID/execute" \
            -H "X-N8N-API-KEY: $N8N_API_KEY" \
            -H "Content-Type: application/json" \
            -d "$WORKFLOW_PARAMS" \
            | jq -r ".data.executionId")

          echo "executionId=$EXECUTION_ID" >> $GITHUB_OUTPUT

          # 実行結果を待機
          sleep 10

          # 実行結果を取得
          RESULT=$(curl -s -X GET \
            "$N8N_API_URL/api/v1/executions/$EXECUTION_ID" \
            -H "X-N8N-API-KEY: $N8N_API_KEY")

          echo "result<<EOF" >> $GITHUB_OUTPUT
          echo "$RESULT" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Report result to Copilot
        if: steps.check-copilot.outputs.isCopilot == 'true'
        uses: actions/github-script@v7
        with:
          script: |
            const result = JSON.parse('${{ steps.execute-n8n.outputs.result }}');
            const executionId = '${{ steps.execute-n8n.outputs.executionId }}';

            const comment = `✅ n8nワークフロー実行が完了しました。

**実行結果**:
- ワークフロー名: ${{ steps.parse-command.outputs.workflowName }}
- 実行ID: ${executionId}
- ステータス: ${result.data.finished ? '成功' : '実行中'}
${result.data.data ? `- 結果: \`\`\`json\n${JSON.stringify(result.data.data, null, 2)}\n\`\`\`` : ''}

**詳細**: ${result.data.stoppedAt ? `実行完了時刻: ${result.data.stoppedAt}` : '実行中...'}`;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

---

## 📋 GitHub Copilot Agents/Copilotへの指示形式

### 基本形式

```markdown
@copilot 以下のn8nワークフローを実行してください:

**ワークフロー名**: github-copilot-ai-review-assistant
**パラメータ**:
{
  "file": "src/main.ts",
  "focus": "security,performance"
}
```

### 詳細形式

```markdown
@copilot n8nワークフローを実行してください。

**ワークフロー名**: github-copilot-ai-review-assistant
**実行パラメータ**:
- file: src/main.ts
- focus: security,performance
- questions: エラーハンドリングは適切か？

**実行条件**:
- エラーが発生した場合は再試行
- 実行結果をIssueにコメントとして記録
```

---

## 🚀 実装手順

### ステップ1: GitHub Actionsワークフローの作成

1. **`.github/workflows/n8n-workflow-executor.yml`を作成**
   - 上記のワークフロー定義を使用

2. **GitHub Secretsを設定**
   - `N8N_API_URL`: n8n CloudのAPI URL
   - `N8N_API_KEY`: n8n Personal Access Token

### ステップ2: n8nワークフローの準備

1. **実行可能なn8nワークフローを作成**
   - Webhook TriggerまたはManual Triggerを使用
   - パラメータを受け取れるように設計

2. **n8nワークフローをアクティブ化**

### ステップ3: GitHub Copilot Agents/Copilotへの指示

1. **Cursor Chatで指示**
   ```
   GitHub Copilot Agentsに、n8nワークフロー「github-copilot-ai-review-assistant」を実行するように指示して。パラメータはfile=src/main.ts, focus=security,performance
   ```

2. **AI（私）がGitHub APIでIssue/PRを作成**
   - `@copilot`メンション付きコメントを追加
   - 実行すべきn8nワークフローとパラメータを指定

3. **GitHub Copilot Agents/CopilotがActionsを実行**
   - GitHub Actionsワークフローが自動起動
   - n8nワークフローが実行される

---

## 📊 制御可能な操作一覧

| 操作 | GitHub Copilot Agents/Copilot指示 | GitHub Actions | n8nワークフロー | 実証状況 |
|------|--------------------------------|---------------|---------------|---------|
| **n8nワークフロー実行** | ✅ | ✅ | ✅ | ✅ 実装可能 |
| **実行結果取得** | ✅ | ✅ | ✅ | ✅ 実装可能 |
| **エラーハンドリング** | ✅ | ✅ | ✅ | ✅ 実装可能 |
| **結果報告** | ✅ | ✅ | ✅ | ✅ 実装可能 |

---

## 💡 使用例

### 例1: n8nワークフロー実行（GitHub Copilot Agents経由）

**ユーザーがCursor Chatで指示**:
```
GitHub Copilot Agentsに、n8nワークフロー「github-copilot-ai-review-assistant」を実行するように指示して。パラメータはfile=src/main.ts, focus=security,performance
```

**AI（私）の動作**:
1. GitHub APIでIssueを作成
2. `@copilot`メンション付きコメントを追加:
   ```markdown
   @copilot 以下のn8nワークフローを実行してください:

   **ワークフロー名**: github-copilot-ai-review-assistant
   **パラメータ**:
   {
     "file": "src/main.ts",
     "focus": "security,performance"
   }
   ```
3. GitHub Copilot Agents/CopilotがActionsを実行
4. GitHub Actionsがn8nワークフローを実行
5. 実行結果をIssueにコメントとして追加
6. AI（私）が結果を検証
7. ユーザーに完了報告

---

## ⚠️ 制限事項と回避策

### 制限1: GitHub Actionsの実行時間制限

**問題**: GitHub Actionsの無料プランでは実行時間に制限がある

**回避策**:
- 長時間実行が必要な場合は、n8nワークフロー側で非同期処理を実装
- 実行結果の取得をポーリング方式に変更

### 制限2: n8n APIのレート制限

**問題**: n8n APIにはレート制限がある

**回避策**:
- リクエスト間隔を調整
- エラーハンドリングを実装
- レート制限エラーを検出して再試行

### 制限3: GitHub Copilot Agents/Copilotの応答タイミング

**問題**: GitHub Copilot Agents/Copilotの応答タイミングが予測できない

**回避策**:
- Issue/PRコメントを監視
- 一定時間待機してから実行結果を確認

---

## 🔄 更新履歴

### 2025-01-24 (v1.0.0)
- 初版作成
- GitHub Copilot Agents/Copilot → GitHub Actions → n8nワークフロー実行フローを設計
- GitHub Actionsワークフロー定義を追加
- GitHub Copilot Agents/Copilotへの指示形式を追加

---

**このドキュメントは、GitHub Copilot Agents/Copilot → n8nワークフロー実行に関する唯一の信頼できる情報源（SSOT）です。**















