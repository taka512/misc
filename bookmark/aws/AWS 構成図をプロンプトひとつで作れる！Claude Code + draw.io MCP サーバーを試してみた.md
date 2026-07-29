---
title: "AWS 構成図をプロンプトひとつで作れる！Claude Code + draw.io MCP サーバーを試してみた"
source: "https://dev.classmethod.jp/articles/aws-architecture-diagram-claude-code-drawio-mcp/"
author:
  - "[[M.Shimizu]]"
published: 2026-02-17
created: 2026-07-30
description: "draw.io MCP サーバーを利用して、簡単なプロンプトで AWS インフラ構成図を作成する手順を紹介します。"
tags:
  - "clippings"
image: "https://images.ctfassets.net/ct0aopd36mqt/3KBTm8tdpO9RJJuaVvVzod/a9964bb03097b448b2327edc6920bf9f/Claude.png"
---
## はじめに

クラスメソッドオペレーションズの Shimizu です。

ブログ執筆や社内資料のために AWS のインフラ構成図を作成する機会がよくあります。  
これまでは手動でコツコツ作っていましたが、draw.io MCP サーバーの登場により、複雑なシステム構成図もプロンプトの指示ひとつで簡単に作成できるようになりました。しかも自由に編集可能です。

![img-000](https://devio2024-media.developers.io/image/upload/v1771305045/2026/02/17/cjhngz6xjlov4q4v8ept.png)

今回は Claude Code と draw.io MCP サーバーを組み合わせて、管理している AWS アカウントのインフラ構成を読み取ってそのまま構成図にする、という手順を試してみました！

## draw.io とは

[draw.io](https://www.drawio.com/) はフローチャートやネットワーク図など、さまざまな図を直感的なマウス操作で作成できるwebサービスで、ユーザー登録不要で利用できます。（デスクトップアプリ版もあり）  
作成した図は自由に編集して画像や PDF に書き出したり、Google ドライブなどにも保存できます。

![img-001](https://devio2024-media.developers.io/image/upload/v1771305050/2026/02/17/wsc4ech6a4axpfxlcoos.png)

[AWS 公式のアイコンセット](https://aws.amazon.com/jp/architecture/icons/) も用意されているため、これまでも構成図の作成に大変重宝していましたが、今回 MCP サーバーの登場によってプロンプトだけで構成図を作成できるようになり、より便利になりました。

以下に、MCP 導入から構成図作成までの手順をご紹介します。

## やってみた

以下の作業環境を用意している前提で進めます。  
これから準備される方は、文末の資料を参考にしてください。

- 端末に Claude Code（または他のツール）を導入済みで MCP サーバーを利用できる
- node.js がインストールされており npx コマンドを実行できる
- 対象の AWS アカウントに AWS CLI で接続する設定ができている ※AWS 環境を読み取る場合に必要

上記前提で、まずは MCP サーバーへの接続を有効化します。

筆者は今回 Claude Code のデスクトップ版を使用するため、下記サイトを参考にして設定ファイル `claude_desktop_config.json` に以下の記述を追加しました。

<iframe src="https://embed.zenn.studio/card#zenn-embedded__252cb89a2ca0c" frameborder="0"></iframe>

設定ファイルに記述する内容

```json
{
  "mcpServers": {
    "drawio": {
      "command": "npx",
      "args": ["@drawio/mcp"]
    }
  }
}
```

これだけで MCP サーバーの用意は完了です。

Claude Code デスクトップアプリの「設定 > 開発者」から、drawio の MCP サーバーが有効になっていることを確認できます。（有効にならない場合は、アプリを再起動してみましょう）

![img-002](https://devio2024-media.developers.io/image/upload/v1771305055/2026/02/17/ljwhqbn51zz1mlsntyer.png)

有効化を確認できたら、まずは簡単な指示を出してみます。  
試しに以下のプロンプトを入れてみます。

```
draw.io を使用して以下の構成図を作成してください。
Route 53 > ALB > EC2
```

![img-003](https://devio2024-media.developers.io/image/upload/v1771305061/2026/02/17/dujb7jm6jz1wudpxtdx5.png)

しばらく待つと、指示した構成図が作成された状態で draw.io のWebブラウザ版アプリが立ち上がりました。図の見栄えはイマイチですが、マウス操作でアイコンや矢印を自由に編集して保存できます。

![img-004](https://devio2024-media.developers.io/image/upload/v1771305067/2026/02/17/jiu6wpuhfmaouvqll37m.png)

ひとまず MCP サーバーの動作を確認できたので、次はもっと複雑な構成図にチャレンジしてみます。  
実際に存在する AWS アカウントの環境構成を読み取り、その構成をそのまま図に落とし込んでみます。

対象 AWS アカウントに AWS CLI で接続できる前提で、適当なフォルダに `CLAUDE.md` ファイルを作成して、以下例のように記述します。  
構成図をきれいに作るため、公式アイコンを使用する指示も入れています。

```
## System Instructions
あなたは AWS クラウドの運用を担当するスペシャリストです。
指示に従って AWS CLI コマンドを操作し、AWS 環境の調査を行なってください。

## AWS CLI Rules
- 決してリソースの変更や削除はしないでください。
- 入力したプロンプトと実行した AWS CLI コマンド、出力結果は全てログファイル "YYYYMMDD_log.txt" に記録してください。

## dwaw.io Rules
- draw.io で構成図の作成を指示したら、下記URL上にある AWS の公式アイコンを用いて作成してください。
https://app.diagrams.net/?splash=0&libs=aws4
```

Claude Code アプリを再起動して、上記の `CLAUDE.md` ファイルを保存したフォルダを指定し、以下のように指示を与えます。（AWS アカウントの ID やリージョンは、実際の環境に合わせて置き換えてください。書き出すファイル名は適当で構いません）

```
AWS アカウント 0000 の ap-northeast-1 と us-east-1 のリソース構成を調べてください。
resource.md ファイルに書き出してください。
```

![img-005](https://devio2024-media.developers.io/image/upload/v1771305072/2026/02/17/xmjfginq1id9yzzexo21.png)

すると Claude が AWS CLI コマンドを駆使して対象アカウントに存在する AWS リソースを洗い出し、ファイルに一覧で書き出してくれました。

今回指定した AWS アカウントには弊社のコーポレートサイト環境があり、Route 53 ホストゾーンや CloudFront ディストリビューション、オリジンの S3 バケットなどが存在します。

![img-006](https://devio2024-media.developers.io/image/upload/v1771305077/2026/02/17/bzzxt1zjrkg4cau2q626.png)

上記で書き出された.md ファイルを元に、構成図を作成するように指示します。

```
draw.io を使用して resource.md ファイルの内容を構成図にしてください
```

しばらく待つと、対象 AWS アカウント上に存在するすべてのリソースを網羅した構成図が作成されました！

AWS 公式のカラフルなアイコンを使用して、各リソースの相互関係（ユーザー > Route 53 > CloudFront > オリジンS3 等）も的確に表現されており、もちろん手動で編集もできます。

![img-000](https://devio2024-media.developers.io/image/upload/v1771305045/2026/02/17/cjhngz6xjlov4q4v8ept.png)

今回試した内容は以上です。

## さいごに

いかがでしたでしょうか。

これまでは複雑な AWS インフラ構成図の作成に多くの時間を要しましたが、MCP サーバーでここまで簡単にできてしまうのと、想像以上の精度なのに驚きました。

AI で構成図の画像を生成するのは従来でも可能でしたが、draw.io の場合は何といっても自由に編集可能なファイル形式で保存できる、というところが大きいです。  
また draw.io はユーザー登録不要なので、API キーの発行も不要で簡単に MCP サーバーを使えるのも魅力です。

なお [draw.io のプライバシーポリシー](https://www.drawio.com/blog/policy-updates) によると、webアプリ上で作成した図はサーバー上には保存されないとのことです。  
従って作成した図をローカルに保存する分には問題ないと思いますが、もし Google ドライブなどに保存する場合は、社内の機密情報が含まれたシステム図を誤って公開フォルダに保存しないよう、十分に注意しましょう。

この記事がお役に立てば幸いです！

## 参考情報

<iframe src="https://embed.zenn.studio/card#zenn-embedded__37290478ce0248" frameborder="0" height="122"></iframe>

<iframe src="https://embed.zenn.studio/card#zenn-embedded__bf73bf5aec1568" frameborder="0" height="122"></iframe>

<iframe src="https://embed.zenn.studio/card#zenn-embedded__34d28b7910e8b" frameborder="0"></iframe>

<iframe src="https://embed.zenn.studio/card#zenn-embedded__7a5be1e3f52038" frameborder="0" height="122"></iframe>

<iframe src="https://embed.zenn.studio/card#zenn-embedded__886ce58dcb5098" frameborder="0"></iframe>

## クラスメソッドオペレーションズ株式会社について

クラスメソッドグループのオペレーション企業です。  
運用・保守開発・サポート・情シス・バックオフィスの専門チームが、IT・AIをフル活用した「しくみ」を通じて、お客様の業務代行から課題解決や高付加価値サービスまでを提供するエキスパート集団です。  
当社は様々な職種でメンバーを募集しています。  
「オペレーション・エクセレンス」と「らしく働く、らしく生きる」を共に実現するカルチャー・しくみ・働き方にご興味がある方は、 [クラスメソッドオペレーションズ株式会社 コーポレートサイト](https://classmethod-operations.jp/) をぜひご覧ください。  
※2026年1月 アノテーション㈱から社名変更しました