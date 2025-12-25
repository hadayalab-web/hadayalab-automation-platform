# Cursor APIとn8n連携 SSOT（Single Source of Truth）

**最終更新**: 2025-01-24
**最終検証**: 2025-01-24（公式ドキュメントと実機テスト）
**バージョン**: 1.0.0
**メンテナー**: HadayaLab

---

## ⚠️ 重要な注意事項

**Cursor APIとn8nを連携する際は、最初に必ず以下のリファレンスを参照してください。**

### 📚 公式リファレンス

#### Cursor API
- **MCP Extension API**: [Cursor MCP Extension API](https://docs.cursor.com/ja/context/mcp-extension-api/)
- **Background Agents API**: [Cursor Background Agents API](https://docs.cursor.com/ja/background-agent/api/overview/)
- **公式ドキュメント**: [Cursor Documentation](https://docs.cursor.com/)

#### n8n連携
- **n8nネイティブMCP**: [Accessing n8n MCP server](https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/)
- **n8n-mcpパッケージ**: [n8n-mcp on npm](https://www.npmjs.com/package/n8n-mcp)

---

## 📋 概要

このドキュメントは、Cursor APIとn8nを連携する方法と、Cursor APIで可能な操作をまとめた**唯一の信頼できる情報源（SSOT）**です。

### Cursor APIとは

Cursor APIは、Cursor IDEの機能をプログラムから制御するためのAPIです。主に2つのAPIが提供されています：

1. **MCP Extension API**: MCPサーバーの動的管理
2. **Background Agents API**: バックグラウンドエージェントの作成・管理

---

## 🎯 Cursor APIでできること

### 1. MCP Extension API

#### 概要
`mcp.json`を直接編集せずに、MCPサーバーの登録や管理をプログラムで行うことができます。

#### 主な機能

##### ✅ MCPサーバーの登録
- **メソッド**: `vscode.cursor.mcp.registerServer`
- **用途**: プログラムからMCPサーバーを動的に登録
- **利点**:
  - エンタープライズ環境での一括設定
  - オンボーディングツールでの自動設定
  - MDMシステムでの動的構成

##### ✅ MCPサーバーの削除
- **メソッド**: `vscode.cursor.mcp.unregisterServer`
- **用途**: 不要になったMCPサーバーを削除

##### ✅ 対応トランスポート
- **HTTP/SSE**: HTTP経由での接続
- **stdio**: 標準入出力経由での接続

#### 使用例

```typescript
// MCPサーバーを登録
await vscode.cursor.mcp.registerServer({
  name: "n8n-cloud",
  command: "npx",
  args: [
    "-y",
    "supergateway",
    "--streamableHttp",
    "https://hadayalab.app.n8n.cloud/mcp-server/http",
    "--header",
    "authorization:Bearer <YOUR_ACCESS_TOKEN_HERE>"
  ]
});

// MCPサーバーを削除
await vscode.cursor.mcp.unregisterServer("n8n-cloud");
```

#### 制限事項
- ⚠️ Cursor Extension APIを使用する必要がある
- ⚠️ 拡張機能の開発が必要（直接的なREST APIではない）

---

### 2. Background Agents API

#### 概要
リポジトリ上で自律的に動作するAI搭載のコーディングエージェントをプログラムから作成・管理できます。

#### 主な機能

##### ✅ エージェントの作成
- **用途**: バックグラウンドで動作するAIエージェントを作成
- **機能**:
  - プロンプトを理解してコードベースを変更
  - GitHubリポジトリと直接やり取り
  - ユーザーのフィードバックへの自動対応
  - バグ修正の自動化
  - ドキュメント更新の自動化

##### ✅ エージェントの管理
- エージェントの起動・停止
- エージェントの設定変更
- エージェントの実行履歴確認

#### 使用例

```typescript
// エージェントを作成
const agent = await vscode.cursor.backgroundAgent.create({
  name: "n8n-workflow-automation",
  prompt: "n8nワークフローを自動的に作成・更新・削除する",
  repository: "https://github.com/your-org/your-repo"
});

// エージェントを起動
await agent.start();

// エージェントを停止
await agent.stop();
```

#### 制限事項
- ⚠️ Cursor Extension APIを使用する必要がある
- ⚠️ 拡張機能の開発が必要

---

## 🔗 Cursor APIとn8nの連携方法

### 現在の連携方法（推奨）

現在、Cursorとn8nは**MCP（Model Context Protocol）**を通じて連携しています。

#### 方法1: n8nネイティブMCP（supergateway経由）

**設定ファイル**: `C:\Users\chiba\.cursor\mcp.json`

```json
{
  "mcpServers": {
    "n8n-cloud": {
      "command": "npx",
      "args": [
        "-y",
        "supergateway",
        "--streamableHttp",
        "https://hadayalab.app.n8n.cloud/mcp-server/http",
        "--header",
        "authorization:Bearer <YOUR_MCP_ACCESS_TOKEN>"
      ]
    }
  }
}
```

**できること**:
- ✅ ワークフローの実行
- ✅ 実行履歴の確認
- ✅ 環境変数の管理
- ✅ ワークフローの検索・詳細取得

#### 方法2: n8n-mcpパッケージ

**設定ファイル**: `C:\Users\chiba\.cursor\mcp.json`

```json
{
  "mcpServers": {
    "n8n-local": {
      "command": "npx",
      "args": ["-y", "n8n-mcp@latest"],
      "env": {
        "N8N_API_URL": "https://hadayalab.app.n8n.cloud",
        "N8N_API_KEY": "<YOUR_PERSONAL_ACCESS_TOKEN>",
        "LOG_LEVEL": "error",
        "NODE_NO_WARNINGS": "1"
      }
    }
  }
}
```

**できること**:
- ✅ ワークフローの作成・更新・削除
- ✅ ノード検索（543個）
- ✅ テンプレート検索（2,700+）
- ✅ ワークフロー検証

---

### Cursor APIを使用した連携（将来の可能性）

#### シナリオ1: MCP Extension APIでn8nサーバーを動的に登録

**用途**:
- エンタープライズ環境での一括設定
- オンボーディングツールでの自動設定
- MDMシステムでの動的構成

**実装例**:
```typescript
// Cursor Extension内で実行
import * as vscode from 'vscode';

async function setupN8nMCP() {
  await vscode.cursor.mcp.registerServer({
    name: "n8n-cloud",
    command: "npx",
    args: [
      "-y",
      "supergateway",
      "--streamableHttp",
      "https://hadayalab.app.n8n.cloud/mcp-server/http",
      "--header",
      `authorization:Bearer ${process.env.N8N_MCP_ACCESS_TOKEN}`
    ]
  });
}
```

#### シナリオ2: Background Agents APIでn8nワークフローを自動管理

**用途**:
- ワークフローの自動作成・更新
- バグ修正の自動化
- ドキュメント更新の自動化

**実装例**:
```typescript
// Cursor Extension内で実行
import * as vscode from 'vscode';

async function createN8nWorkflowAgent() {
  const agent = await vscode.cursor.backgroundAgent.create({
    name: "n8n-workflow-manager",
    prompt: `
      このリポジトリのn8nワークフローを自動管理する:
      - 新しいワークフローを作成
      - 既存のワークフローを更新
      - 不要なワークフローを削除
      - ワークフローの検証とテスト
    `,
    repository: "https://github.com/your-org/your-repo"
  });

  await agent.start();
}
```

---

## 🚀 実践的な連携ワークフロー

### ワークフロー1: Cursorからn8nワークフローを作成

```
【ステップ1: Cursor Chatで指示】
@n8n-local 新しいワークフローを作成して:
- Webhook Trigger
- HTTP Request ノードでVercel APIを呼び出し
- 結果をSlackに通知

【ステップ2: n8n-mcpパッケージが自動実行】
- ワークフローJSONを生成
- n8n Cloudに作成
- 検証とテスト

【ステップ3: 実行確認】
@n8n-cloud 作成したワークフローを実行して
```

### ワークフロー2: Cursor Extensionでn8n MCPを動的に設定

```
【ステップ1: Cursor Extensionを作成】
- MCP Extension APIを使用
- n8n MCPサーバーを動的に登録

【ステップ2: オンボーディング時に自動実行】
- 新規ユーザーのオンボーディング時に自動実行
- n8n MCPサーバーを自動設定

【ステップ3: 管理】
- MDMシステムから一括管理
- 設定の更新・削除を自動化
```

---

## ⚠️ 制限事項と注意点

### Cursor APIの制限

1. **Extension APIが必要**
   - MCP Extension APIとBackground Agents APIは、Cursor Extension内で使用する必要がある
   - 直接的なREST APIではない

2. **拡張機能の開発が必要**
   - Cursor Extensionを開発する必要がある
   - TypeScriptでの開発が必要

3. **認証の管理**
   - トークンやAPIキーの安全な管理が必要
   - 環境変数やシークレット管理ツールの使用を推奨

### n8n連携の制限

1. **MCP経由の連携が推奨**
   - 現在、Cursorとn8nの連携はMCP経由が最も確実
   - `mcp.json`での設定が最も簡単

2. **トークンの管理**
   - MCP Access Token（ネイティブMCP用）
   - Personal Access Token（n8n-mcpパッケージ用）
   - 適切なトークンを選択する必要がある

---

## 📊 比較表

| 機能 | MCP設定（現在） | Cursor API（将来） |
|------|---------------|-------------------|
| **n8n MCPサーバーの登録** | ✅ `mcp.json`で手動設定 | ✅ プログラムから動的登録 |
| **n8nワークフローの作成** | ✅ n8n-mcpパッケージ経由 | ⚠️ Background Agents APIで可能 |
| **n8nワークフローの実行** | ✅ ネイティブMCP経由 | ⚠️ Background Agents APIで可能 |
| **設定の一括管理** | ❌ 手動 | ✅ プログラムから可能 |
| **オンボーディング自動化** | ❌ 手動 | ✅ プログラムから可能 |
| **拡張機能の開発** | ❌ 不要 | ✅ 必要 |

---

## 🔄 更新履歴

### 2025-01-24 (v1.0.0)
- 初版作成
- Cursor APIの機能とn8n連携方法を追加
- 実践的なワークフローを追加
- 制限事項と注意点を追加

---

## 📚 参考リンク

### Cursor公式ドキュメント
- [Cursor MCP Extension API](https://docs.cursor.com/ja/context/mcp-extension-api/)
- [Cursor Background Agents API](https://docs.cursor.com/ja/background-agent/api/overview/)
- [Cursor Documentation](https://docs.cursor.com/)

### n8n公式ドキュメント
- [Accessing n8n MCP server](https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/)
- [n8n-mcp on npm](https://www.npmjs.com/package/n8n-mcp)

### プロジェクト内ドキュメント
- [n8n MCP機能比較 SSOT](./n8n-mcp-capabilities-comparison-SSOT.md)
- [MCPサーバー導入ガイド](./mcp-servers-setup.md)

---

**このドキュメントは、Cursor APIとn8n連携に関する唯一の信頼できる情報源（SSOT）です。**






