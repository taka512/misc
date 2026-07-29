## Claude.md

CLAUDE.mdの最適化
https://qiita.com/nogataka/items/d6c83ea50b82e1c2602c

ClaudeCodeの基礎
https://qiita.com/K5K/items/72cc4282819ace823524

## CLAUDEベストプラクティス

https://code.claude.com/docs/ja/best-practices

## 料金

https://claude.ai/upgrade

```
Free: $0
Pro: $20
Max: $100
Max: $200
```

## install

```
npm install -g @anthropic-ai/claude-code
```

認証

```
/login
```

[利用料のページ](https://claude.ai/settings/usage)


## 設定

プロジェクト共通の設定
```
.claude/settings.json
```

## MCP

**Claude Desktopでのmcpの設定**

「設定」→「開発者」→「設定」から編集可能

```
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json 
{
  "mcpServers": {
        "aws-knowledge-mcp-server": {
            "command": "uvx",
            "args": [
                "fastmcp",
                "run",
                "https://knowledge-mcp.global.api.aws"
            ]
        },
        "MCP_DOCKER": {
            "command": "docker",
            "args": ["mcp", "gateway", "run"]
        }
    }
}
```

**Claude Code での設定**

```
## aws knowledge
claude mcp add aws-knowledge-mcp-server -s user -- npx mcp-remote https://knowledge-mcp.global.api.aws

## MCP gateway
claude mcp add -s user mcp-docker docker mcp gateway run
```

mcpの設定がエラーの場合はログに出力

```
tail -n 20 -F ~/Library/Logs/Claude/mcp*.log
```
## command option

```
# Claude Codeの起動
claude

# 特定のディレクトリで起動
claude /path/to/project

# 最新版への更新
claude update

# 前回の会話を継続
claude -c

# 会話履歴を参照して起動
claude -r

# バージョン確認
claude --version

# 一回限りのタスクを実行
claude "fix the build error"

# 一回限りのクエリを実行して終了
claude -p "explain this function"

# Gitコミットを作成
claude commit

```
## slash command

```
コマンドで効率化
claudeコマンドを実行すると、Claude Codeが起動し、プロンプトを入力できるようになりますが、先頭に/をつけると、Claude Codeの便利ツールが使えます。

# ディレクトリ初期化
/init

# モデルの切り替え（Sonnet/Opus）
> /model

# コンテキストに別フォルダを追加
> /add-dir <path>

# 会話履歴をクリア
> /clear

# コマンド確認
/help

# 今読み込んでいるメモリーを確認
/memory

# 安全な作業を事前承認
/permissions
```

## hook

Hooksで例外なく実行する
Hooksは、Claude Codeのライフサイクルに合わせてコマンドを実行する仕組みです。
公式ドキュメントでは、`PreToolUse`、`PostToolUse`、`UserPromptSubmit`、`Stop`、`SessionStart` などのイベントが説明されています。

## Sub agents

- [Claude CodeのSub agentsでコンテキスト枯渇問題をサクッと解決できたはなし](https://zenn.dev/tacoms/articles/552140c84aaefa)
- [Claude Code Sub Agents 実践ガイド：自動委任機能の効果的な活用法！](https://zenn.dev/asuene/articles/d05c8b70da8365)
- [Claude Code でカスタムサブエージェントを作成する](https://azukiazusa.dev/blog/create-custom-sub-agent-in-claude-code/)

## SuperClaude

- [Claude Codeに専門家チームを追加！開発効率を向上させるSuperClaudeを試してみた](https://dev.classmethod.jp/articles/claude-code-superclaude/)

## link


- [Claude Code を初めて使う人向けの実践ガイド](https://zenn.dev/hokuto_tech/articles/86d1edb33da61a)
- [Claude Code ベストプラクティス](https://zenn.dev/farstep/articles/claude-code-best-practices)
- [Claude Codeを徹底解説してみた（前編）](https://dev.classmethod.jp/articles/get-started-claude-code-1/)
- [Claude Codeを徹底解説してみた（後編）](https://dev.classmethod.jp/articles/get-started-claude-code-2nd/)
- [Claude Codeに保守しやすいコードを書いてもらうための事前準備やガードレール](https://www.memory-lovers.blog/entry/2025/06/12/074355)
- [Claude Code Actions を試した！！ && Devin のようにSlackから話しかけたい！！！](https://www.ikkitang1211.site/entry/2025/05/27/232943)
- [Claude Codeをサンドボックス上で実行する(Mac編)](https://zenn.dev/todesking/articles/claude-code-with-sandbox-exec)
- [# Claude Code × HCP Terraformでセキュアなインフラ自動構築を実現する](https://dev.classmethod.jp/articles/claude-code-hcp-tf-authentication-information-management/)
