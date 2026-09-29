# Claudeの設定メモ

## ステータスラインで作業状況を常時可視化

claudeに指示

```
/statusline モデル名、ブランチ、コンテキスト使用量を表示して


リポジトリ名とGitブランチ : my-project ⎇ main
コンテキスト使用量 : ゲージとパーセンテージ(●●●●○○○○○○ 40%)
レートリミット消費 : 5時間ウィンドウの使用率とリセット時刻(5h: 26% ↺17:00)、7日ウィンドウ(7d: 12%)
```


## 朝7時のpingで5時間制限を業務時間に揃える(ルーチン)


```
/schedule every day at 7am: pingメッセージを送る
```

## 原始人口調でトークンを約80%削減する「genshijin」

https://github.com/interfacex-co-jp/genshijin

```
claude plugin marketplace add InterfaceX-co-jp/genshijin
/plugin install genshijin@genshijin
```

コマンド

```
/genshijin          # 通常モード（デフォルト）で起動
/genshijin 丁寧     # ビジネス向け簡潔体
/genshijin 極限     # 最大圧縮
会話中に 原始人やめて または 通常モード で解除。
```


## 開発方法論をプラグイン化した「superpowers」

https://github.com/obra/superpowers

```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```


## claude design


インストール

```
claude mcp add --scope user --transport http claude-design https://api.anthropic.com/v1/design/mcp

/design-login
```