# n8nワークフロー作成ヘルパー

## Personal Access Tokenを取得した後

以下のコマンドを実行してください：

```powershell
.\scripts\create-n8n-workflow.ps1 -WorkflowPath "workflows/simple-time-check.json" -ApiKey "YOUR_PERSONAL_ACCESS_TOKEN"
```

## または、環境変数を使用

```powershell
$env:N8N_PERSONAL_ACCESS_TOKEN = "YOUR_PERSONAL_ACCESS_TOKEN"
.\scripts\create-n8n-workflow.ps1 -WorkflowPath "workflows/simple-time-check.json" -ApiKey $env:N8N_PERSONAL_ACCESS_TOKEN
```















