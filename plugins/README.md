# taka512 プラグインマーケットプレイス

taka512 の開発用 Claude Code プラグイン（スキル）集です。マーケットプレイスのカタログはリポジトリ直下の `.claude-plugin/marketplace.json` にあります。

## クイックスタート

### 1. マーケットプレイスを追加

```bash
# GitHub経由で追加
/plugin marketplace add taka512/misc

# またはローカルパスで追加
/plugin marketplace add /path/to/misc
```

### 2. プラグインをインストール

```bash
/plugin install commit@taka512-marketplace
```

### 3. 使用

```bash
# スラッシュコマンド（名前空間付き）
/commit:commit

# スキルは自然言語でも自動起動
「変更をコミットして」
```

### マーケットプレイスの更新

```bash
/plugin marketplace update taka512-marketplace
```

---

## 利用可能なプラグイン一覧

| プラグイン名 | カテゴリ | 説明 |
|-------------|---------|------|
| `commit` | development | ローカルの変更を元にgit commitを行う |
| `instructional-video` | video | 台本・静止画・録画からナレーションと字幕を同期させた説明動画を制作（要 FFmpeg / Pillow / NumPy / edge-tts） |

---

## 新しいスキル（プラグイン）の追加手順

### 1. ディレクトリ構成

```
misc/
├── .claude-plugin/
│   └── marketplace.json          # マーケットプレイスのカタログ
└── plugins/
    └── <plugin-name>/
        ├── .claude-plugin/
        │   └── plugin.json       # プラグインのマニフェスト
        └── skills/
            └── <skill-name>/
                ├── SKILL.md      # スキル本体
                ├── references/   # (任意) 詳細資料。SKILL.md から参照
                └── scripts/      # (任意) スキルから実行するスクリプト
```

1 つのプラグインに複数のスキルを入れることもできます（`skills/` 配下にディレクトリを並べる）。

### 2. `plugin.json` を作成

`plugins/<plugin-name>/.claude-plugin/plugin.json`

```json
{
  "name": "<plugin-name>",
  "description": "プラグインの説明",
  "version": "1.0.0",
  "author": {
    "name": "taka512"
  },
  "repository": "https://github.com/taka512/misc",
  "keywords": ["development"]
}
```

### 3. `SKILL.md` を作成

`plugins/<plugin-name>/skills/<skill-name>/SKILL.md`

```markdown
---
name: <skill-name>
description: いつ・何のために使うスキルかを具体的に書く（自動起動の判定に使われる）
allowed-tools:
  - Bash(git status:*)
---

# <skill-name> スキル

## 手順
1. ...
```

### 4. `marketplace.json` に登録

`.claude-plugin/marketplace.json` の `plugins` 配列に追記します。

```json
{
  "name": "<plugin-name>",
  "source": "./plugins/<plugin-name>",
  "description": "プラグインの説明",
  "category": "development",
  "tags": ["development"]
}
```

### 5. 検証と反映

```bash
# マニフェストの検証
claude plugin validate .
claude plugin validate plugins/<plugin-name>

# 反映（push 後、またはローカル登録している場合はそのまま）
/plugin marketplace update taka512-marketplace
/plugin install <plugin-name>@taka512-marketplace
```

スキルを更新したら `plugin.json` の `version` を上げてください。
