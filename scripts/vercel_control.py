#!/usr/bin/env python3
"""
Cursor-Vercel Control Script
CursorからVercel APIを直接制御するためのスクリプト
"""

import os
import sys
import json
import argparse
import requests
from typing import Dict, Any, Optional


class VercelController:
    """Vercel APIを制御するクラス"""

    def __init__(self, api_token: Optional[str] = None):
        """
        初期化

        Args:
            api_token: Vercel API Token（環境変数VERCEL_API_TOKENからも取得可能）
        """
        self.api_token = api_token or os.getenv('VERCEL_API_TOKEN')
        if not self.api_token:
            raise ValueError("Vercel API Tokenが必要です。環境変数VERCEL_API_TOKENを設定するか、--tokenオプションで指定してください。")

        self.base_url = "https://api.vercel.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Vercel APIにリクエストを送信

        Args:
            method: HTTPメソッド（GET, POST, PATCH, DELETE）
            endpoint: APIエンドポイント
            data: リクエストボディ（POST/PATCH用）

        Returns:
            APIレスポンス
        """
        url = f"{self.base_url}{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method == "PATCH":
                response = requests.patch(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"エラー: {e}", file=sys.stderr)
            if hasattr(e.response, 'text'):
                print(f"レスポンス: {e.response.text}", file=sys.stderr)
            sys.exit(1)

    def deploy(self, project_name: str, repository: str, branch: str = "main") -> Dict[str, Any]:
        """
        デプロイメントを作成

        Args:
            project_name: プロジェクト名
            repository: GitHubリポジトリ（例: owner/repo）
            branch: ブランチ名（デフォルト: main）

        Returns:
            デプロイメント情報
        """
        data = {
            "name": project_name,
            "gitSource": {
                "type": "github",
                "repo": repository,
                "ref": branch
            }
        }
        return self._request("POST", "/v13/deployments", data)

    def get_deployment_status(self, deployment_id: str) -> Dict[str, Any]:
        """
        デプロイメントステータスを取得

        Args:
            deployment_id: デプロイメントID

        Returns:
            デプロイメントステータス
        """
        return self._request("GET", f"/v13/deployments/{deployment_id}")

    def list_deployments(self, project_id: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """
        デプロイメント一覧を取得

        Args:
            project_id: プロジェクトID（オプション）
            limit: 取得件数（デフォルト: 10）

        Returns:
            デプロイメント一覧
        """
        endpoint = f"/v13/deployments?limit={limit}"
        if project_id:
            endpoint += f"&projectId={project_id}"
        return self._request("GET", endpoint)

    def get_deployment_logs(self, deployment_id: str) -> Dict[str, Any]:
        """
        デプロイメントログを取得

        Args:
            deployment_id: デプロイメントID

        Returns:
            デプロイメントログ
        """
        return self._request("GET", f"/v2/deployments/{deployment_id}/events")

    def get_project_info(self, project_id: str) -> Dict[str, Any]:
        """
        プロジェクト情報を取得

        Args:
            project_id: プロジェクトIDまたはプロジェクト名

        Returns:
            プロジェクト情報
        """
        return self._request("GET", f"/v9/projects/{project_id}")

    def list_projects(self) -> Dict[str, Any]:
        """
        プロジェクト一覧を取得

        Returns:
            プロジェクト一覧
        """
        return self._request("GET", "/v9/projects")

    def get_environment_variables(self, project_id: str) -> Dict[str, Any]:
        """
        環境変数一覧を取得

        Args:
            project_id: プロジェクトIDまたはプロジェクト名

        Returns:
            環境変数一覧
        """
        return self._request("GET", f"/v9/projects/{project_id}/env")

    def create_environment_variable(
        self,
        project_id: str,
        key: str,
        value: str,
        target: list = ["production", "preview", "development"]
    ) -> Dict[str, Any]:
        """
        環境変数を作成

        Args:
            project_id: プロジェクトIDまたはプロジェクト名
            key: 環境変数キー
            value: 環境変数値
            target: 適用環境（デフォルト: すべて）

        Returns:
            作成された環境変数情報
        """
        data = {
            "key": key,
            "value": value,
            "type": "encrypted",
            "target": target
        }
        return self._request("POST", f"/v9/projects/{project_id}/env", data)


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="CursorからVercel APIを制御するスクリプト",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # デプロイメント作成
  python vercel_control.py deploy --project my-project --repo owner/repo --branch main

  # デプロイメントステータス確認
  python vercel_control.py status --deployment-id dpl_xxxxx

  # デプロイメント一覧取得
  python vercel_control.py list --project-id prj_xxxxx --limit 10

  # デプロイメントログ取得
  python vercel_control.py logs --deployment-id dpl_xxxxx

  # プロジェクト情報取得
  python vercel_control.py project --project-id prj_xxxxx

  # 環境変数一覧取得
  python vercel_control.py env list --project-id prj_xxxxx

  # 環境変数作成
  python vercel_control.py env create --project-id prj_xxxxx --key API_KEY --value secret_value
        """
    )

    parser.add_argument(
        "--token",
        help="Vercel API Token（環境変数VERCEL_API_TOKENからも取得可能）"
    )

    subparsers = parser.add_subparsers(dest="command", help="実行するコマンド")

    # deploy コマンド
    deploy_parser = subparsers.add_parser("deploy", help="デプロイメントを作成")
    deploy_parser.add_argument("--project", required=True, help="プロジェクト名")
    deploy_parser.add_argument("--repo", required=True, help="GitHubリポジトリ（例: owner/repo）")
    deploy_parser.add_argument("--branch", default="main", help="ブランチ名（デフォルト: main）")

    # status コマンド
    status_parser = subparsers.add_parser("status", help="デプロイメントステータスを取得")
    status_parser.add_argument("--deployment-id", required=True, help="デプロイメントID")

    # list コマンド
    list_parser = subparsers.add_parser("list", help="デプロイメント一覧を取得")
    list_parser.add_argument("--project-id", help="プロジェクトID（オプション）")
    list_parser.add_argument("--limit", type=int, default=10, help="取得件数（デフォルト: 10）")

    # logs コマンド
    logs_parser = subparsers.add_parser("logs", help="デプロイメントログを取得")
    logs_parser.add_argument("--deployment-id", required=True, help="デプロイメントID")

    # project コマンド
    project_parser = subparsers.add_parser("project", help="プロジェクト情報を取得")
    project_parser.add_argument("--project-id", required=True, help="プロジェクトIDまたはプロジェクト名")

    # projects コマンド
    projects_parser = subparsers.add_parser("projects", help="プロジェクト一覧を取得")

    # env コマンド
    env_parser = subparsers.add_parser("env", help="環境変数管理")
    env_subparsers = env_parser.add_subparsers(dest="env_command", help="環境変数コマンド")

    env_list_parser = env_subparsers.add_parser("list", help="環境変数一覧を取得")
    env_list_parser.add_argument("--project-id", required=True, help="プロジェクトIDまたはプロジェクト名")

    env_create_parser = env_subparsers.add_parser("create", help="環境変数を作成")
    env_create_parser.add_argument("--project-id", required=True, help="プロジェクトIDまたはプロジェクト名")
    env_create_parser.add_argument("--key", required=True, help="環境変数キー")
    env_create_parser.add_argument("--value", required=True, help="環境変数値")
    env_create_parser.add_argument(
        "--target",
        nargs="+",
        default=["production", "preview", "development"],
        help="適用環境（デフォルト: production preview development）"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # VercelControllerを初期化
    controller = VercelController(api_token=args.token)

    # コマンド実行
    try:
        if args.command == "deploy":
            result = controller.deploy(args.project, args.repo, args.branch)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "status":
            result = controller.get_deployment_status(args.deployment_id)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "list":
            result = controller.list_deployments(args.project_id, args.limit)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "logs":
            result = controller.get_deployment_logs(args.deployment_id)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "project":
            result = controller.get_project_info(args.project_id)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "projects":
            result = controller.list_projects()
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "env":
            if args.env_command == "list":
                result = controller.get_environment_variables(args.project_id)
                print(json.dumps(result, indent=2, ensure_ascii=False))
            elif args.env_command == "create":
                result = controller.create_environment_variable(
                    args.project_id,
                    args.key,
                    args.value,
                    args.target
                )
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                env_parser.print_help()
                sys.exit(1)

        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
















