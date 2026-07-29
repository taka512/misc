---
title: "CLAUDE.mdに本当は何を書くべきなのか"
source: "https://zenn.dev/cureapp/articles/65b9a99d22ce2b"
author:
  - "[[Zenn]]"
published: 2026-03-03
created: 2026-03-05
description:
tags:
  - "clippings"
image: "https://res.cloudinary.com/zenn/image/upload/s--p8Uhvh6Y--/c_fit%2Cg_north_west%2Cl_text:notosansjp-medium.otf_55:CLAUDE.md%25E3%2581%25AB%25E6%259C%25AC%25E5%25BD%2593%25E3%2581%25AF%25E4%25BD%2595%25E3%2582%2592%25E6%259B%25B8%25E3%2581%258F%25E3%2581%25B9%25E3%2581%258D%25E3%2581%25AA%25E3%2581%25AE%25E3%2581%258B%2Cw_1010%2Cx_90%2Cy_100/g_south_west%2Cl_text:notosansjp-medium.otf_34:7tsuno%2Cx_220%2Cy_108/bo_3px_solid_rgb:d6e3ed%2Cg_south_west%2Ch_90%2Cl_fetch:aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3plbm4tdXNlci11cGxvYWQvYXZhdGFyL2M1MThkMWZlMzkuanBlZw==%2Cr_20%2Cw_90%2Cx_92%2Cy_102/co_rgb:6e7b85%2Cg_south_west%2Cl_text:notosansjp-medium.otf_30:CureApp%2520%25E3%2583%2586%25E3%2583%2583%25E3%2582%25AF%25E3%2583%2596%25E3%2583%25AD%25E3%2582%25B0%2Cx_220%2Cy_160/bo_4px_solid_white%2Cg_south_west%2Ch_50%2Cl_fetch:aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3plbm4tdXNlci11cGxvYWQvYXZhdGFyL2NlNDY1N2YxMjAuanBlZw==%2Cr_max%2Cw_50%2Cx_139%2Cy_84/v1627283836/default/og-base-w1200-v2.png?_a=BACAGSGT"
---
[CureApp テックブログ](https://zenn.dev/p/cureapp) [Publicationへの投稿](https://zenn.dev/faq/what-is-publication)

98

52[tech](https://zenn.dev/tech-or-idea)

## TL;DR

- CLAUDE.mdはSystem Promptではなく、User Messageとして注入される
- セッション後半になると影響力が薄れるため、セッションを通して守らせたいルールの置き場所には向かない
- CLAUDE.mdにはセッション開始時の作業を助ける情報だけを書き、ルールは `.claude/rules/` に置く

## はじめに

Claude Codeを使っている人なら、CLAUDE.mdに何を書くかで一度は悩んだことがあるのではないでしょうか。

コーディングルール、命名規則、テストの方針、コミットメッセージのフォーマット。色々なことを書いている人が多いと思います。自分もそうでした。

ただ、CLAUDE.mdの **内部的な扱われ方** を知ると、そこに書くべきものの考え方が結構変わります。結論から言うと、CLAUDE.mdにはセッション開始時の作業を助ける情報だけを書いて、ルールは `.claude/rules/` に移そう、という話です。

## CLAUDE.mdはSystem Promptではない

多くの人がCLAUDE.mdをSystem Promptのようなものだと思っています。「ここに書いたことはClaudeの振る舞いのベースになる」と。

ただ、公式ドキュメントにはこう書かれています。

> CLAUDE.md adds the contents as a user message following Claude Code's default system prompt.  
> \--append-system-prompt appends the content to the system prompt.
> 
> （CLAUDE.md は内容をUser Messageとして Claude Code のデフォルトSystem Promptの「後に」追加します。--append-system-prompt は内容をSystem Promptに追記します。）

出典: [Output styles - Claude Code Docs](https://code.claude.com/docs/en/output-styles)

また、Memory managementのページにはこうあります。

> Claude treats them as context, not enforced configuration.  
> CLAUDE.md files are loaded into the context window at the start of every session, consuming tokens alongside your conversation.
> 
> （Claudeはこれらを強制的な設定ではなく、コンテキストとして扱います。CLAUDE.mdファイルはセッション開始時にコンテキストウィンドウに読み込まれ、会話と一緒にトークンを消費します。）

出典: [Memory management - Claude Code Docs](https://code.claude.com/docs/en/memory)

CLAUDE.mdの内容は **System Promptではなく、セッションの最初のUser Message** として注入されます。enforced configuration（強制的な設定）ではなくcontext（文脈）として扱われる、自分がClaude Codeに投げるプロンプトと同じ扱いで、会話の中の一つのメッセージにすぎません。

整理するとこうなります。

| 手段 | 注入先 | 性質 |
| --- | --- | --- |
| CLAUDE.md | User Message（最初のメッセージ） | 会話の中の一つのメッセージ |
| `--append-system-prompt` | System Prompt（末尾に追記） | Claudeの振る舞いの基盤 |

この違いは結構大きいです。

## なぜこの違いが重要なのか

System Promptは会話のメッセージとは別の領域で管理されています。どれだけ会話が長くなっても、Claudeにとっての重要度は変わりません。

一方、User Messageとして注入されたCLAUDE.mdの内容は、会話が進むにつれて **どんどん古いメッセージになっていきます** 。10ターン、20ターンと会話が続けば、CLAUDE.mdに書いたことの影響力は薄れていきます。

つまり:

- **セッション開始直後** → 直前に伝えたことなのでよく効く
- **セッション後半** → だいぶ前に伝えたことなので、忘れられがち

「テストは必ず書け」「コミット前にlintを通せ」といったルールをCLAUDE.mdに書いても、セッションが長くなるにつれて守られなくなる可能性があります。これはClaudeがルールを無視しているのではなく、User Messageとしてのルールが会話の中に埋もれているだけです。

## CLAUDE.mdはSession Start Hookである

ここまでの事実を踏まえると、CLAUDE.mdの本質は「Session Start Hook」だと考えるとわかりやすいです。

Session Start Hookとは、セッションが開始されるたびに実行される処理のことです。

CLAUDE.mdも同じです。セッションが始まるたびに、最初のUser Messageとして内容が注入されます。Compactが発生してセッションが圧縮された後も、再度読み込まれます。

Hookの役割は「起動時に必要な初期化処理を行うこと」であって、「アプリケーション全体を通じて守るべきルールを定義すること」ではありません。ルールを定義したいなら、後述する `.claude/rules/` に書くか、 `--append-system-prompt` を利用する方が適切です。

## CLAUDE.mdに書くべきもの

では、Session Start Hookとして何を書くべきか。

基準は **「セッション開始時の作業を助ける情報か？」** です。

Claude Codeでの作業は多岐にわたります。開発、調査、設計、レビュー、ドキュメント作成。これらすべての用途において、セッションの最初に知っておくべき情報は何でしょうか。

例えば:

- **プロジェクトの概要**: 何のためのプロジェクトで、何をしているのか
- **モジュール構成**: モノレポで、ディレクトリ名だけでは各モジュールの役割が分かりにくい場合など

これらはどの用途でも、セッションの最初にClaudeが把握しておくべき情報です。Claude Codeはどんな作業でもまずディレクトリ構造を探索するところから始まるので、名前から推測しにくいモジュールの説明などがあれば、その探索を助けられます。

また、情報だけでなく「セッション開始時にやるべき手順」も書く価値があります。例えば「Issueベースの作業時はworktreeを作成し、命名は `feat/{issue番号}-{kebab-case}` にする」のような手順は、セッション開始時に実行されるので、後半に埋もれても問題ありません（もう実行済みなので）。厳密には全セッションで使うわけではありませんが、ほぼ毎回のセッションで行う手順であれば、CLAUDE.mdに書いておく実用的な価値はあると思います。このあたりはプロジェクトの運用に合わせて判断すればいいでしょう。

他にもセッション開始時の作業を助けるものがあれば書く価値はありますが、そもそも常にすべてのセッションで渡すべき情報はそう多くありません。必要な情報は必要なタイミングで渡す方が効果的で、それ以外は後述する `.claude/rules/` やSkillsで都度渡すのが適切です。

## CLAUDE.mdに書くべきでないもの

逆に、以下のようなものはCLAUDE.mdには向きません。

**セッション全体を通じて守らせたいルール**

「テストは必ず書くこと」「コミットメッセージはConventional Commitsに従うこと」など。前述の通り、User Messageとして注入される以上、セッション後半では埋もれていきます。特にコミットメッセージのルールは、コミットするにしても大抵セッションの終盤なので、最もメッセージが古くなったタイミングで必要になります。

**特定の用途でしか使わない情報**

「開発時はfeatureブランチを切ること」「レビュー時はセキュリティ観点を重視すること」など。開発の情報を書けば調査時にはノイズになりますし、レビューの情報を書けば開発時には邪魔になります。用途固有の指示はSkillsやプロンプトで都度渡す方が適切です。

**量の多い情報**

例えば50行のルールをCLAUDE.mdに書くということは、毎回のセッションで50行分のコンテキストを無条件に消費するということです。常に渡す情報は最小限にすべきです。

### Before / After

よくあるCLAUDE.mdと、整理後のCLAUDE.mdを比較してみます。

**Before（よくあるCLAUDE.md）**

```
# プロジェクト概要
ECサイトのバックエンドAPI。NestJS + TypeScript + PostgreSQL。

# モジュール構成
- packages/core - 注文・在庫・顧客のドメインロジック
- packages/gateway - 外部決済サービスとの連携
- packages/bridge - レガシーシステムとのデータ同期

# コーディングルール
- TypeScriptではinterfaceを優先すること
- 関数名はcamelCase、クラス名はPascalCase
- マジックナンバーは定数化すること

# テスト方針
- すべてのAPIエンドポイントにはE2Eテストを書くこと
- ユニットテストのカバレッジは80%以上を維持すること
- テストファイルは対象ファイルと同じディレクトリに配置すること

# コミットルール
- Conventional Commitsに従うこと (feat:, fix:, chore: など)
- コミットメッセージは日本語で書くこと

# レビュー観点
- セキュリティ: SQLインジェクション、XSSに注意
- パフォーマンス: N+1クエリがないか確認
```

**After（整理後のCLAUDE.md）**

```
# プロジェクト概要
ECサイトのバックエンドAPI。

# モジュール構成
- packages/core - 注文・在庫・顧客のドメインロジック
- packages/gateway - 外部決済サービスとの連携
- packages/bridge - レガシーシステムとのデータ同期

# セッション開始時の手順
- Issueベースの作業時はworktreeを作成する
- 命名は feat/{issue番号}-{kebab-case英語max3語} 形式にする
```

Beforeにあったコーディングルール、テスト方針、コミットルール、レビュー観点は、すべて `.claude/rules/` に移動させます。

## ルールを書きたいなら.claude/rules/ に書く

ここまでの話を聞いて、「じゃあルールはどこに書けばいいの？」と思うかもしれません。

答えは `.claude/rules/` です。

`.claude/rules/` に置いたMarkdownファイルはconditional rulesとして機能します。YAML frontmatterの `paths` フィールドを使えば、特定のファイルを扱う時だけ読み込ませることができます。

```
---
paths:
  - "src/api/**/*.ts"
---
# API開発ルール
- すべてのAPIエンドポイントには入力バリデーションを含めること
- 標準のエラーレスポンスフォーマットを使用すること
- OpenAPIのドキュメントコメントを付けること
```

出典: [Memory management - Claude Code Docs](https://code.claude.com/docs/en/memory)

`.claude/rules/` の強みは **注入されるタイミング** です。

CLAUDE.mdはセッション開始時にすべての情報を一括で渡します。一方、conditional rulesは該当するファイルを初めて扱ったタイミングで注入されます。これはProgressive Disclosure（段階的開示）の考え方に近く、必要な情報を必要なタイミングで渡すことで、ルールがより新しいメッセージとして届きます。

セッションの30ターン目で初めてTypeScriptファイルを編集した時、そのタイミングで注入されたルールは、セッション開幕に注入されたCLAUDE.mdよりも新しいメッセージなのでよく効きます。

同じUser Messageだとしても、 **いつ注入されるか** でルールとしての実効性は大きく変わります。

| 手段 | 注入タイミング | ルールとしての効き |
| --- | --- | --- |
| CLAUDE.md | セッション開始時（一度だけ） | セッション後半に弱くなる |
| `.claude/rules/` | 該当ファイルを初めて扱う時 | 作業に近い位置で効く |
| `--append-system-prompt` | System Promptに追記 | 常に一定の強さで効く |

なお、 `--append-system-prompt` はSystem Promptに追記されるため常に一定の強さで効きますが、CLI起動時に毎回指定する必要があり、チームで共有しにくいという制約があります。

「テストは必ず書け」「命名規則を守れ」といったルールは、CLAUDE.mdではなく `.claude/rules/` に、必要であれば `paths` でスコープを絞って書く方がいいのではないかと思っています。

### .claude/rules/ の注意点

`.claude/rules/` も万能ではありません。

- **注入は初回のみ**: conditional rulesが注入されるのは、該当ファイルをセッション内で初めて扱ったタイミングだけです。同じ条件に当てはまるファイルを2回目以降に触っても再注入はされません。また、注入もUser Messageとして行われるため、その後さらに会話が続けば古いメッセージになっていきます。それでも、セッション開幕に注入されるCLAUDE.mdよりは新しいメッセージになるので有利です。

## まとめ

| 観点 | 内容 |
| --- | --- |
| CLAUDE.mdの実態 | System Promptではなく、最初のUser Message |
| 書くべきもの | セッション開始時の作業を助ける情報（プロジェクト概要、モジュール構成） |
| 効きにくいもの | セッション全体を通じて守らせたいルール |
| 考え方 | Session Start Hook。セッション開始時の作業を助ける情報だけを書く |
| ルールを書きたい場合 | `.claude/rules/` にconditional rulesとして書く |

CLAUDE.mdに何を書くかを考えることは、「Claudeとの毎回の会話で、最初に何を伝えるべきか？」を考えることと同じです。その問いに対して、本当に必要な答えだけを書けばいいのかなと思っています。

## 参考リンク

- [Output styles - Claude Code Docs](https://code.claude.com/docs/en/output-styles) - CLAUDE.mdの注入先についての公式ドキュメント
- [Memory management - Claude Code Docs](https://code.claude.com/docs/en/memory) - `.claude/rules/` やconditional rulesについての公式ドキュメント
- [Claude Code Overview](https://code.claude.com/docs/en/overview) - Claude Code全体の公式ドキュメント

98

52