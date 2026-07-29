# CaludeCodeのスキルメモ

本文は呼ばれるまで読まれないので、「呼ばれるかどうか」はほぼ description で決まります。
公式ベストプラクティスは、description を三人称で書き、「何をするか」と「いつ使うか」の両方を入れることを推奨
https://platform.claude.com/docs/ja/agents-and-tools/agent-skills/best-practices

description に手順を要約して書いてはいけない

description 一覧に割り当てられる予算はコンテキストウィンドウの1%（デフォルト）で、1スキルあたりの説明文は 1,536 文字で切り詰められます。
https://code.claude.com/docs/en/skill

SKILL.md に全部を書かない
公式ベストプラクティスは、SKILL.md を500行以内に収め、参照は1階層までにするよう求めています。
https://platform.claude.com/docs/ja/agents-and-tools/agent-skills/best-practices
コンテキストの圧縮（compaction）が走ると、呼び出し済みの Skill は「各スキル先頭5,000トークン・全体25,000トークン」の枠内でしか引き継がれません（公式ドキュメント）。
https://code.claude.com/docs/en/skills


呼び出し制御（Claude Code の frontmatter）
disable-model-invocation: true   # Claude の自動呼び出しを止める（人間専用）
user-invocable: false            # / メニューから隠す（Claude 専用）
何も書かなければ両方から呼べる
コミットやデプロイのような副作用のある操作は、勝手に発火されると困るので disable-model-invocation で自動呼び出しを止めます。


context: forkを付けると、重めのSkillでも内部作業ログを親のメイン会話から切り離せます
fork付きSkillとSubagentはかなり似ています。どちらもメイン会話を汚さずに、別コンテキストで作業できます。
では、何を基準に使い分ければよいのでしょうか。個人的には、再利用したいものが手順(fork)なのか、担当者なのかで考える
https://code.claude.com/docs/ja/skills#%E3%82%B9%E3%82%AD%E3%83%AB%E3%82%92%E3%82%B5%E3%83%96%E3%82%A8%E3%83%BC%E3%82%B8%E3%82%A7%E3%83%B3%E3%83%88%E3%81%A7%E5%AE%9F%E8%A1%8C%E3%81%99%E3%82%8B

