---
name: commit
description: gitコミットを作成
allowed-tools:
  - Bash(git add:*)
  - Bash(git commit:*)
  - Bash(git status:*)
  - Bash(git diff:*)
  - Bash(git log:*)
---

# Commit スキル

gitコミットを作成します。

## 使い方

```
/commit
```

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## タスク

上記の変更内容に基づいて、単一のgitコミットを作成してください。

複数のツールを1つのレスポンスで呼び出すことができます。ステージングとコミットの作成を1つのメッセージで行ってください。他のツールを使用したり、他の操作を行ったりしないでください。これらのツール呼び出し以外のテキストやメッセージを送信しないでください。
