---
title: "AWSに繋げなくてもテストできる？新サービス「AWS Blocks」を触ってみた"
source: "https://zenn.dev/aws_japan/articles/aws-blocks-ai-agent-intro"
author:
published: 2026-06-18
created: 2026-07-30
description:
tags:
  - "clippings"
image: "https://res.cloudinary.com/zenn/image/upload/s--YE_rz4EJ--/c_fit%2Cg_north_west%2Cl_text:notosansjp-medium.otf_55:AWS%25E3%2581%25AB%25E7%25B9%258B%25E3%2581%2592%25E3%2581%25AA%25E3%2581%258F%25E3%2581%25A6%25E3%2582%2582%25E3%2583%2586%25E3%2582%25B9%25E3%2583%2588%25E3%2581%25A7%25E3%2581%258D%25E3%2582%258B%25EF%25BC%259F%25E6%2596%25B0%25E3%2582%25B5%25E3%2583%25BC%25E3%2583%2593%25E3%2582%25B9%25E3%2580%258CAWS%2520Blocks%25E3%2580%258D%25E3%2582%2592%25E8%25A7%25A6%25E3%2581%25A3%25E3%2581%25A6%25E3%2581%25BF%25E3%2581%259F%2Cw_1010%2Cx_90%2Cy_100/g_south_west%2Cl_text:notosansjp-medium.otf_34:showish%2Cx_220%2Cy_108/bo_3px_solid_rgb:d6e3ed%2Cg_south_west%2Ch_90%2Cl_fetch:aHR0cHM6Ly9zdGF0aWMuemVubi5zdHVkaW8vdXNlci11cGxvYWQvYXZhdGFyLzZmZTY2NGI3N2IuanBlZw==%2Cr_20%2Cw_90%2Cx_92%2Cy_102/g_south_west%2Ch_34%2Cl_default:og-publication-pro-mark-xcosax%2Cw_34%2Cx_217%2Cy_158/co_rgb:6e7b85%2Cg_south_west%2Cl_text:notosansjp-medium.otf_30:%25E3%2582%25A2%25E3%2583%259E%25E3%2582%25BE%25E3%2583%25B3%2520%25E3%2582%25A6%25E3%2582%25A7%25E3%2583%2596%2520%25E3%2582%25B5%25E3%2583%25BC%25E3%2583%2593%25E3%2582%25B9%2520%25E3%2582%25B8%25E3%2583%25A3%25E3%2583%2591%25E3%2583%25B3%2520%2528%25E6%259C%2589%25E5%25BF%2597%2529%2Cx_255%2Cy_160/bo_4px_solid_white%2Cg_south_west%2Ch_50%2Cl_fetch:aHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSnRVNjBpSkV1OUV3R1NSdklLTE81eGhQLW50N0hYOGUwNWprNGFTVmd3NzBORHFBPXMyNTAtYw==%2Cr_max%2Cw_50%2Cx_139%2Cy_84/v1627283836/default/og-base-w1200-v2.png?_a=BACMTiAE"
---
[アマゾン ウェブ サービス ジャパン (有志)](https://zenn.dev/p/aws_japan) Publication Pro

154

91[AI](https://zenn.dev/topics/ai)

[

AWS

](https://zenn.dev/topics/aws)[

React

](https://zenn.dev/topics/react)[

TypeScript

](https://zenn.dev/topics/typescript)[

Bedrock

](https://zenn.dev/topics/bedrock)[

tech

](https://zenn.dev/tech-or-idea)

## はじめに

先日、AWSから [**AWS Blocks**](https://aws.amazon.com/products/developer-tools/blocks/) という新しい開発者向けツールがリリースされました。

ドキュメントをひと通り読んで実際にAIエージェントのデモアプリを作ってみたら、思っていた以上に「これは良いぞ」となったので紹介します。結論から言うと、 **「ローカルで即動く・AWS接続不要・そのままデプロイできる」** ツールです。

この記事では、

- AWS Blocks って結局なに？
- なにが嬉しいの？
- 実際にAIエージェントアプリを作って動かしてみる

という流れで、コード多めで紹介していきます。

## AWS Blocks とは？

ひとことで言うと、 **TypeScriptで書く「Infrastructure from Code（IFC）」スタイルのフルスタックフレームワーク** です。

「IaC（Infrastructure as Code）」はよく聞きますが、こちらは **from** です。インフラ定義を別ファイルに書くのではなく、アプリのコードを書くと **そこからインフラが導出される** という考え方です。

### IFCツールは他にもある。でも作ったのがAWS

実はIFCという考え方自体は新しいものではなく、すでにいくつかの有名なツールがあります。

- **[Encore](https://encore.dev/)** … Go / TypeScript対応。アプリコードからインフラを導出し、自分のAWS / GCPアカウントにデプロイする。独立系のスタートアップ製。
- **[Wing（Winglang）](https://www.winglang.io/)** … AWS CDKの作者が立ち上げた、クラウド向けの新言語。Terraformにコンパイルされ、AWS / Azure / GCPなどマルチクラウドに対応。
- **[SST](https://sst.dev/)** … TypeScriptでAWS上のフルスタックアプリを構築。こちらも独立系コミュニティ製。

これらに共通するのは、 **「アプリのコードからインフラを生やす」** という発想。AWS Blocksも基本は同じ路線です。

ではAWS Blocksの何が新しいのか。いちばん大きいのは、 **この手のツールを“クラウドベンダーであるAWS自身”が出してきた** という点です。上記のツールはどれもサードパーティ製で、「AWSを便利に使うための外部ツール」という立ち位置でした。AWS Blocksは、生成されるのが素のCDK / CloudFormationで、必要になればそのままCDKに降りられる - つまり **AWSのエコシステムにそのまま地続き** なのが効いてきます。

仕組みの肝は **Block** という単位。1つのBlockがnpmパッケージになっていて、その中に3つの顔が同居しています。

1. **ローカル実装** … メモリ／ファイルシステム上で動くモック
2. **CDKコンストラクト** … デプロイ時にCloudFormationになる
3. **ランタイム実装** … 本番のLambda上でAWS SDKを叩く

そして魔法のようなのが、 **同じ1行のコードが文脈に応じて中身を切り替える** こと。Node.jsの [Conditional Exports](https://nodejs.org/api/packages.html#conditional-exports) を使って実現しています。

```
const todos = new KVStore(scope, 'todos');
// ローカル開発 → インメモリのストア
// CDK synth   → DynamoDBテーブルの定義
// Lambda本番  → DynamoDBへのSDKコール
```

このコードを **1文字も変えずに** ローカルでも本番でも動かせる、というのが世界観です。

### Blockのラインナップ

用意されているBlockは約20種類。主要なものを挙げると：

| カテゴリ | Block | 対応するAWSサービス |
| --- | --- | --- |
| データ | `KVStore` / `DistributedTable` / `Database` | DynamoDB / Aurora |
| 認証 | `AuthBasic` / `AuthCognito` / `AuthOIDC` | Cognito ほか |
| 非同期処理 | `AsyncJob` / `CronJob` | SQS+Lambda / EventBridge |
| **AI** | **`Agent`** / **`KnowledgeBase`** | **Amazon Bedrock** |
| リアルタイム | `Realtime` | API Gateway WebSocket |
| 監視 | `Logger` / `Metrics` / `Tracer` / `Dashboard` | CloudWatch / X-Ray |

今回は太字の **AI系（ `Agent` と `KnowledgeBase` ）** を使ってデモを作ります。

## なにが嬉しいのか

触ってみて「お、いいな」と思ったポイントを4つ。

### 1\. とにかく起動が速い。AWSアカウントすら要らない

`npm run dev` で、認証もDBもリアルタイムも全部入りのアプリがローカルで立ち上がります。クラウドのエミュレータもDockerも不要。最初のうちはAWSアカウントすら開かなくていい。

「ちょっと試したいだけなのにIAMロールとVPCで日が暮れる」- そういった悩みから解放されます。

### 2\. フロントとバックエンドが型でつながる（コード生成なし）

バックエンド（ `aws-blocks/index.ts` ）で定義したAPIを、フロントが **そのままimportして呼ぶだけ** です。OpenAPIからのコード生成も、クライアントSDKの初期化もありません。

```
// フロント側。api.* はすべて型が効く
import { api } from 'aws-blocks';
const data = await api.sendMessage(convId, "hello", chId);
```

バックエンドのメソッドのシグネチャを変えたら、フロントが即コンパイルエラーになります。これだけで開発体験がぐっと上がります。

### 3\. AWSのサービス名やCloudFormationの作法を知らなくていい

これが個人的にいちばん効くと思ったポイント。普通にAWSでアプリを作ろうとすると、「チャット履歴はDynamoDB、ファイルはS3、非同期処理はSQS + Lambda……」とまずサービスを選び、それぞれのCloudFormation（やCDK）の書き方とベストプラクティスを調べることになります。

AWS Blocksでは、欲しいのは「データベース」「ファイル保存」「AIエージェント」といった **機能** であって、その裏でどのAWSサービスがどう構成されるかを覚える必要がありません。 `new KnowledgeBase(...)` と書けば、Bedrock Knowledge BaseもS3 Vectorsのベクトルストアも、AWS推奨の構成で勝手に組み上がります。 **AWSに詳しくなくてもAWSをちゃんと使える** 、という体験はなかなか新鮮でした。

### 4\. 抽象化の天井がない

Blockは内部的に素のAWSサービスを使っているだけなので、足りなくなったらCDKに降りて直接いじれます。「フレームワークに縛られて身動きが取れなくなる」がない、というのは大事なポイントです。

## 実際にAIエージェントを作ってみる

ここからが本番。 **「AcmeCloudというSaaSのサポートチャットボット」** を題材に、 `Agent` Blockと `KnowledgeBase` Blockでエージェントを組んでいきます。

作るものの仕様はこんな感じ：

- ユーザーとチャットできる（ストリーミング応答）
- ドキュメントを検索して答える（ **RAG** ）
- 注文ステータスを調べる（ツール呼び出し）
- 注文をキャンセルする（ **実行前に人間の承認が必要** = Human-in-the-Loop）

### プロジェクトを作る

```
npm create @aws-blocks/blocks-app@latest support-agent --template react
cd support-agent
```

テンプレートは `default` / `react` / `nextjs` / `bare` など複数。今回はReactを選びました。

### バックエンド：エージェントを定義する

`aws-blocks/index.ts` がこのフレームワークの心臓部、いわゆる「IFCレイヤー」です。ここにBlockを並べるだけで、APIもインフラも定義されます。

まずはRAG用の `KnowledgeBase` 。ローカルの `./knowledge` フォルダ（Markdownファイル群）を指すだけです。

```
import { Scope, ApiNamespace, AuthBasic, Agent, BedrockModels, KnowledgeBase } from '@aws-blocks/blocks';
import { z } from 'zod';

const scope = new Scope('support-agent');

// ./knowledge 配下のMarkdownを検索対象にする
const kb = new KnowledgeBase(scope, 'docs', {
  source: './knowledge',
  description: 'AcmeCloudの製品ドキュメントとFAQ',
  chunking: { strategy: 'semantic' },
});
```

次にエージェント本体。 `tools` にツールを3つ定義します。注目は3つ目の `cancelPurchase` で、 `needsApproval: true` を付けると **実行前に人間の承認待ちで一時停止** します。

（以下のツール定義は要点を絞った簡略版です。実際のリポジトリでは `folder` での絞り込みなど、もう少し作り込んでいます）

```
const agent = new Agent(scope, 'support', {
  model: {
    // デプロイ時: BedrockのClaude Sonnet 4
    deployed: BedrockModels.BALANCED,
    // ローカル: model.local を省略すると「canned（モック）」が自動で使われる
  },
  systemPrompt: 'あなたはAcmeCloudのサポート担当です。簡潔かつ親切に答えてください。',
  streamingMode: 'token', // 1トークンずつ流す（タイプライター風）
  toolContextSchema: z.object({ userId: z.string() }),
  tools: (tool) => ({
    // ① ナレッジベース検索（RAG）
    searchDocs: tool({
      description: '製品ドキュメントやFAQを検索する',
      parameters: z.object({ query: z.string() }),
      handler: async ({ input }) => kb.retrieve(input.query, { maxResults: 4 }),
    }),
    // ② 注文ステータス照会
    getOrderStatus: tool({
      description: '注文IDからステータスを取得する',
      parameters: z.object({ orderId: z.string() }),
      handler: async ({ input }) => ORDERS[input.orderId],
    }),
    // ③ 注文キャンセル（人間の承認が必要！）
    cancelPurchase: tool({
      description: '注文をキャンセルする。実行前に承認が必要。',
      parameters: z.object({ orderId: z.string(), reason: z.string() }),
      needsApproval: true,  // ← これだけでHITLになる
      trustable: true,      // 「今後は信頼」も選べる
      handler: async ({ input }) => {
        ORDERS[input.orderId].status = 'cancelled';
        return { success: true, orderId: input.orderId };
      },
    }),
  }),
});
```

`needsApproval: true` の1行だけでHITL（承認待ち→再開）が完結するの、シンプルながら強力だと思いませんか？

最後にAPIを公開します。 `ApiNamespace` がフロントとのRPCを型安全につないでくれます。

```
export const api = new ApiNamespace(scope, 'api', (context) => ({
  async createConversation() {
    const user = await auth.requireAuth(context);
    return { conversationId: await agent.createConversationId(user.userId) };
  },
  async sendMessage(conversationId: string, message: string, channelId: string) {
    const user = await auth.requireAuth(context);
    await agent.stream(message, {
      conversationId, channelId,
      userId: user.userId,
      context: { userId: user.userId },
    });
    return { ok: true };
  },
  // getConversation / getChannel / resume なども定義...
}));
```

ここで使っている `auth` （ `AuthBasic` Block）は、ユーザーごとに会話を分けるための軽量な認証です。

`Agent` Blockは内部で **S3 + DynamoDB×3 + API Gateway WebSocket + SQS+Lambda** を自動で構成してくれます（会話・メッセージ・WebSocket接続管理のテーブル）。会話の永続化もストリーミングも、開発者が意識する必要はありません。

### cdk synth で「実際に何が生成されるか」を見てみる

「自動で構成してくれる」と言われても、実際どれくらいのインフラになるのか気になりますよね。AWS BlocksはCDKアプリなので、 **デプロイせずに** `cdk synth` でCloudFormationテンプレートを生成して中身を確認できます（AWSアカウント不要）。

```
npx cdk synth --app "npx tsx -C cdk aws-blocks/index.cdk.ts" --context sandboxMode=true
```

今回の約250行のバックエンドから生成されたリソースを数えてみると……

```
TOTAL RESOURCES: 104
  5  AWS::DynamoDB::Table          # auth×2 + agent(convos/messages/connections)×3
 11  AWS::Lambda::Function
  3  AWS::S3::Bucket
  2  AWS::SQS::Queue               # AsyncJob 本体 + DLQ
  1  AWS::ApiGatewayV2::Api        # ストリーミング用 WebSocket
  1  AWS::ApiGateway::RestApi      # RPC エンドポイント
  1  AWS::Bedrock::KnowledgeBase   # KnowledgeBase Block
  1  AWS::S3Vectors::VectorBucket  # ベクトルストア（S3 Vectors）
  1  AWS::StepFunctions::StateMachine
 14  AWS::IAM::Role
  ...
```

**合計104リソース** 。 `new Agent(...)` と `new KnowledgeBase(...)` のたった2行から、Bedrock Knowledge Base、S3 Vectorsのベクトルストア、WebSocket API、SQS+Lambda、IAMロール一式までが展開されています。論理IDを見ると `support-convos` / `support-messages` / `support-connections` のように、どのBlockが何を作ったのかもちゃんと追えます。

ちなみにフロントエンドのホスティング（CloudFront + S3）も含めて本番デプロイ（ `npm run deploy` ）すると、リソース数はさらに増えて **120個** になりました。実際のCloudFormationコンソールがこちらです。

![CloudFormationコンソールのリソースタブ。120個のリソースがすべてCREATE_COMPLETEになっている](https://static.zenn.studio/user-upload/deployed-images/eff3c5c15e3bf4e0f8f54e11.png?sha=bdc56d72d276bf36161fb7affcf2952d18b44162)  
*`npm run deploy` で作られたスタック。120リソースがすべて `CREATE_COMPLETE`*

これを全部手で書くとどうなるかは、後半の [「いつものやり方だとどうなる？」](#%E3%81%84%E3%81%A4%E3%82%82%E3%81%AE%E3%82%84%E3%82%8A%E6%96%B9%E3%81%A0%E3%81%A8%E3%81%A9%E3%81%86%E3%81%AA%E3%82%8B%EF%BC%9F) で触れます。

### ナレッジベースのドキュメントを置く

`./knowledge` にMarkdownを置くだけ。サブフォルダ名は自動で `folder` というメタデータになり、検索時の絞り込みに使えます。

```
knowledge/
├── product-overview.md
├── faq/
│   ├── billing.md
│   └── getting-started.md
└── policies/
    ├── refunds.md
    └── support-sla.md
```

### フロントエンド：useChat でつなぐ

フロントは `@aws-blocks/bb-agent/client` の `useChat` を使うと、 **「subscribe してから send する」という面倒な順序制御** を全部やってくれます。

```
import { useRef } from 'react';
import { useChat } from '@aws-blocks/bb-agent/client';
import { api } from 'aws-blocks';

// useChat は一度だけ生成する（毎レンダリングで作り直さない）
const chatRef = useRef<ReturnType<typeof useChat> | null>(null);
if (!chatRef.current) {
  chatRef.current = useChat({
    api: {
      sendMessage: async (convId, msg, chId) => { await api.sendMessage(convId, msg, chId); },
      createConversation: () => api.createConversation(),
      getConversation: (id) => api.getConversation(id),
      resume: async (chId, res, convId) => { await api.resume(chId, res, convId ?? chId); },
    },
    subscribe: async (channelId, handler) => {
      const channel = await api.getChannel(channelId);
      return channel.subscribe(handler);
    },
    onMessagesChange: (msgs) => setMessages([...msgs]),
    onInterrupt: (interrupts) => setInterrupts(interrupts), // ← 承認待ちのUI表示
  });
}
const chat = chatRef.current;

await chat.sendMessage('返金ポリシーを教えて');
```

`onInterrupt` に承認待ちのコールバックを渡しておくと、 `cancelPurchase` が呼ばれたタイミングで「承認しますか？」のUIを出せます。承認したら `chat.respondToInterrupt([{ interruptId, approved: true }])` でエージェントが再開します。

### 動かす

```
npm run dev
```

`http://localhost:3000` を開いてサインアップ（ローカルはモック認証なので適当でOK）したら、チャットしてみましょう。

![サインイン後のチャット画面。3つの例文プロンプトが表示されている](https://static.zenn.studio/user-upload/deployed-images/a2b11c422a298b6062b27b10.png?sha=ffe3042b980d6af3d78cd3b97ae36cfdf0a5d169)  
*チャット画面。AWSアカウントなしでこの状態まで一発で立ち上がります*

| 入力してみる | 起きること |
| --- | --- |
| `返金ポリシーを教えて` | `searchDocs` が発火（RAG） |
| `注文のステータスは？` | `getOrderStatus` が発火 |
| `注文をキャンセルして` | `cancelPurchase` → **承認待ちで停止** |

ナレッジベース検索（RAG）を投げると、エージェントが `searchDocs` ツールを呼んで `./knowledge` の中から関連するチャンクを引っ張ってきます。

![RAG検索の結果。searchDocsツールがfaq/getting-started.mdからチャンクを取得している](https://static.zenn.studio/user-upload/deployed-images/8038d5a910fccd58672dd919.png?sha=2adfa5000367ed61e907ee1d56874351f1ef5b40)  
*`searchDocs` が発火し、ドキュメントの該当箇所（ `source` とスコア付き）が返ってきている*

そして本命のHITL。「注文をキャンセルして」と送ると、 `cancelPurchase` は `needsApproval: true` なので **実行されずに一時停止** し、承認カードが出ます。

![承認カード。cancelPurchaseの入力内容とApprove/Deny/Trustボタンが表示されている](https://static.zenn.studio/user-upload/deployed-images/f3a313f1a41c856f85de1005.png?sha=494899a7262607729776f9091f424da3f8b54518)  
*エージェントが一時停止し、ツールの入力内容とともに Approve / Deny / Trust ボタンが表示される*

**Approve** を押すとエージェントが再開し、ツールが実行されます。 `onInterrupt` → `respondToInterrupt` の往復が、UIとバックエンドのAsyncJobをまたいでちゃんとつながっているのがわかります。

![承認後の画面。Approvedと表示され、cancelPurchaseがsuccess:trueを返している](https://static.zenn.studio/user-upload/deployed-images/f9fad831d97464d6c34aeb9e.png?sha=4cb9118aa7263764d1ed0b18df4cfef42618a4b1)  
*承認後、エージェントが再開してツールが実行され、 `success: true` が返ってきた*

ローカルのモックモデルの挙動について（重要）

AWSの認証情報なしで動かすと、Agentは **canned（モック）プロバイダー** を使います。これは「メッセージにツール名に含まれる単語が出てきたらそのツールを呼ぶ」「ツールの入力はZodスキーマからダミー値を生成する」という挙動です。

つまり **ツール呼び出しやHITLの「配線」を確認するためのもの** で、本物のLLMの推論ではありません。本物の応答が見たいときは：

- `model.local` に [Ollama](https://ollama.com/) （ `OllamaModels.SMALL` など）を指定する
- もしくはAWSにデプロイしてBedrockを使う

のどちらかにしましょう。デモのツール名（ `searchDocs` / `getOrderStatus` / `cancelPurchase` ）は、それぞれ `search` / `status` / `cancel` という別々の単語で発火するように命名すると、ローカルでもキレイに動きます。

ちゃんと動いているか、E2Eテストでも確認できました。認証・ストリーミング・3つのツール・承認→再開フローまで、 **7/7 パス** しています。

## AWSへのデプロイ

ローカルで満足したら、 **同じコードのまま** AWSへ。今回はまず、CLIで自分のAWSアカウントに接続してから、サンドボックス環境にデプロイしてみました。

```
aws configure                # 自分のAWSアカウントにCLIで接続（SSOなら aws sso login）
npm run sandbox              # 自分専用のサンドボックスにデプロイ（バックエンドのみ、高速）
```

本番フルデプロイ（フロントのホスティング込み）はこちら。

```
npm run deploy
```

事前に必要なのは、

- AWS認証情報の設定（ `aws configure` など）と `npx cdk bootstrap` （アカウント/リージョンごとに1回）
- **Bedrockのモデルアクセス有効化** （ `BedrockModels.BALANCED` = Claude Sonnet 4 をリージョンで有効に）

くらい。料金はフレームワーク自体は無料で、 **使ったAWSリソース分だけ** の通常課金です。

### デプロイして本物のBedrockで動かしてみた

サンドボックスで手応えを掴んだあと、 `npm run deploy` で本番デプロイもしてみました。CloudFrontでホスティングされたフロントエンドが立ち上がり、バックエンドはBedrock（Claude Sonnet 4）につながります。 **コードはローカルのときから1行も変えていません。**

ローカルのモックと違って、ここからは本物のLLMの推論です。返金ポリシーを聞くと、ナレッジベースを検索したうえで、ちゃんと整形された回答が返ってきます。

![デプロイ後のRAG回答。Claude Sonnet 4が返金ポリシーを整形して回答している](https://static.zenn.studio/user-upload/deployed-images/70d9f4bd7d980c30563948c5.png?sha=b084d852c25e96c3ad3934028a16cac6b44c912c)  
*本物のBedrock（Claude Sonnet 4）の回答。 `searchDocs` でナレッジベースを引いたうえで回答を生成している*

注文ステータスの照会も、モックと違って **プロンプトから本物の注文ID（ `ORD-002` ）を抜き出して** ツールに渡してくれます。

![デプロイ後の注文照会。ORD-002のステータス・商品・金額が返ってきている](https://static.zenn.studio/user-upload/deployed-images/47eb85b6726f0f2493ffc2ca.png?sha=d6e87a022da4af6777f0e5f121547b0c90d98e5f)  
*`getOrderStatus` がプロンプト中の `ORD-002` を正しく抽出して呼ばれている*

そしてキャンセル。 `needsApproval: true` が効いて、エージェントは **実行前に必ず承認を求めて止まります** 。

![デプロイ後のHITL。注文詳細を示したうえで「承認しますか？」と確認している](https://static.zenn.studio/user-upload/deployed-images/683d451c98304f9623a642fb.png?sha=3e06fd31c4de9236e661f734f3a15e720bb717ec)  
*実行前に注文内容を提示して承認を求めるエージェント*

そして「 `KnowledgeBase` Blockの数行」が、本当にAmazon Bedrockのナレッジベースとして立ち上がっているのも確認できます。

![Bedrockコンソールのナレッジベース画面。ステータスが「利用可能」、データソースがS3でセマンティックチャンキング](https://static.zenn.studio/user-upload/deployed-images/00741b8d5271742192889d0e.png?sha=4f5181252f888ec63c46a2f496abc0dbbdba8050)  
*`./knowledge` を指していた数行が、Bedrock Knowledge Base（ステータス: 利用可能）として実体化している*

`./knowledge` に置いたMarkdownも、ちゃんとS3経由で取り込まれてインデックス済みになっています。

![ナレッジベースのデータソース画面。5つのドキュメントがすべてINDEXED、同期履歴が「完了」](https://static.zenn.studio/user-upload/deployed-images/d9e5954f642cb9a2e8700e34.png?sha=60c0ef2567353ebb6ba96dbc9f56518f7b72f019)  
*5つのドキュメントがすべて `INDEXED` 。同期も「完了」している*

DynamoDBを見れば、 `Agent` Blockと `AuthBasic` Blockが作った5つのテーブルが並んでいます。

![DynamoDBのテーブル一覧。support-agent-stack-prod- で始まる5つのテーブルがアクティブ](https://static.zenn.studio/user-upload/deployed-images/a6532bec00fa54db51983560.png?sha=94f70aca80a6ec9dc201435e4634ebd31e8d7d9b)  
*`Agent` （convos / messages / connections）+ `AuthBasic` （users / codes）= 5テーブル。論理IDのとおりの構成*

**ローカルで動いていたものが、文字どおり同じコードでクラウドに乗った** わけです。

## いつものやり方だとどうなる？

ここまでの「 `Agent` の数行 → 104リソース」を、もしフレームワークなしで自前で組むとどうなるか。同じ機能（ストリーミング + ツール呼び出し + HITL + 会話履歴の永続化）を素のAWSで作るなら、ざっくりこれだけの部品を **自分で配線する** ことになります。

| やりたいこと | 自前で組む場合 | AWS Blocks |
| --- | --- | --- |
| LLM呼び出し | Bedrock SDK（ `@aws-sdk/client-bedrock-runtime` ）を直接叩く | `model: BedrockModels.BALANCED` |
| ツール呼び出し | ツールスキーマ定義 → モデルの `toolUse` をパース → 実行 → 結果を再投入…のループを自作 | `tools: (tool) => ({ ... })` |
| ストリーミング | API Gatewayのタイムアウト対策で非同期化 → WebSocket APIを立てて配信 | `streamingMode: 'token'` （裏で自動） |
| HITL（承認待ち） | 「中断 → 状態を保存 → 再開」のステートマシンを設計 | `needsApproval: true` |
| 会話履歴 | DynamoDBのテーブル設計・読み書き | 自動（ `convos` / `messages` テーブル） |
| 型安全なAPI | OpenAPI定義 → クライアントコード生成 | `import { api } from 'aws-blocks'` |

LLMを呼ぶだけなら数行ですが、 **「ストリーミング」「ツールの実行ループ」「承認して再開」「履歴の永続化」を本番品質で揃える** となると、CDKスタックもLambdaのハンドラもそれなりの量になります。 `Agent` Blockはこの一式を「設定」に畳み込んでくれている、というわけです。

## つまずいたところ（v0.1.1）

正直に書いておくと、出たてなのでいくつか引っかかりました。後続の人のために共有します。

このあたりは早晩直ると思いますが、現時点では知っておくとスムーズです。

## まとめ

AWS Blocks、ファーストインプレッションはかなり良かったです。

- ✅ **AWSアカウントなしでローカル即起動** 。試行錯誤のサイクルが速い
- ✅ **フロント⇄バックが型でつながる** 。コード生成なしの気持ちよさ
- ✅ **`Agent` / `KnowledgeBase` でAIエージェントが一瞬で組める** 。HITLが1行
- ✅ **数行のコードが104リソースに展開される** 。それでいて中身は `cdk synth` で透けて見える
- ✅ **同じコードがそのままAWSにデプロイできる**

特にAI系のBlockは、「ツール呼び出し」「RAG」「Human-in-the-Loop」みたいな今どきのエージェントの要素が最初から型安全に揃っているのが強い。ツール実行ループやHITLの設計は、AWSが公開している [Strands Agents SDK](https://strandsagents.com/) がベースになっており、エージェントまわりの作りに一貫性があるのも納得です。

まだ `v0.1.x` で粗さはありますが、「ローカルファーストでサクッと作って、必要になったらAWSへ」という体験は、プロトタイピングからプロダクションまで一気通貫でカバーしてくれそうです。

`v0.1.x` の荒削りさはありますが、体験してみる価値は十分あります。気になった方はぜひ `npm create @aws-blocks/blocks-app@latest` で触ってみてください 🧱

---

### 参考リンク

- [AWS Blocks 製品ページ](https://aws.amazon.com/products/developer-tools/blocks/)
- [AWS Blocks Developer Guide](https://docs.aws.amazon.com/blocks/latest/devguide/)
- [AWS Blocks 公式リポジトリ（GitHub）](https://github.com/aws-devtools-labs/aws-blocks)
- [Strands Agents SDK](https://strandsagents.com/)
- [`FileBucket` （S3）を試した記事 by かわごえさん](https://zenn.dev/rrrraaaaa6/articles/aws-blocks-s3-presigned-url-local) — ストレージ系のBlockを使った別の切り口

91