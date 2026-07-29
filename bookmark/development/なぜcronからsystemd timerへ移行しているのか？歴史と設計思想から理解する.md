---
title: "なぜcronからsystemd timerへ移行しているのか？歴史と設計思想から理解する"
source: "https://zenn.dev/hcompany/articles/20260119_systemd_timer"
author:
published: 2026-01-30
created: 2026-07-30
description:
tags:
  - "clippings"
image: "https://res.cloudinary.com/zenn/image/upload/s--8axmbqDy--/c_fit%2Cg_north_west%2Cl_text:notosansjp-medium.otf_55:%25E3%2581%25AA%25E3%2581%259Ccron%25E3%2581%258B%25E3%2582%2589systemd%2520timer%25E3%2581%25B8%25E7%25A7%25BB%25E8%25A1%258C%25E3%2581%2597%25E3%2581%25A6%25E3%2581%2584%25E3%2582%258B%25E3%2581%25AE%25E3%2581%258B%25EF%25BC%259F%25E6%25AD%25B4%25E5%258F%25B2%25E3%2581%25A8%25E8%25A8%25AD%25E8%25A8%2588%25E6%2580%259D%25E6%2583%25B3%25E3%2581%258B%25E3%2582%2589%25E7%2590%2586%25E8%25A7%25A3%25E3%2581%2599%25E3%2582%258B%2Cw_1010%2Cx_90%2Cy_100/g_south_west%2Cl_text:notosansjp-medium.otf_34:tdera1215%2Cx_220%2Cy_108/bo_3px_solid_rgb:d6e3ed%2Cg_south_west%2Ch_90%2Cl_fetch:aHR0cHM6Ly9zdGF0aWMuemVubi5zdHVkaW8vdXNlci11cGxvYWQvYXZhdGFyLzhlNDc2OGQyNDkuanBlZw==%2Cr_20%2Cw_90%2Cx_92%2Cy_102/co_rgb:6e7b85%2Cg_south_west%2Cl_text:notosansjp-medium.otf_30:H%2526Company%25E3%2583%2586%25E3%2583%2583%25E3%2582%25AF%25E3%2583%2596%25E3%2583%25AD%25E3%2582%25B0%2Cx_220%2Cy_160/bo_4px_solid_white%2Cg_south_west%2Ch_50%2Cl_fetch:aHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSnRfclhQU3RCM2NHVWFrMlZ6d0hvdThEZ2RSajhieFFrdndvRUhtQ1RBLTdKUGJBPXM5Ni1j%2Cr_max%2Cw_50%2Cx_139%2Cy_84/v1627283836/default/og-base-w1200-v2.png?_a=BACMTiAE"
---
224

96

Linux で定期実行といえば、長らく **crontab** が使われてきました。

しかし近年では、

- 新規サーバ構築では cron を使わない
- systemd timer が推奨される
- cron は「保守対象」になりつつある

という流れが明確になっています。

本記事では、

- cron は何者なのか
- 何が問題だったのか
- なぜ systemd に統合されていったのか
- systemd timer はどう使うのか

を **歴史的背景と設計思想** から整理して解説します。

---

## 1\. そもそも crontab とは？

## cron とは

**cron** は Unix 系 OS における「時間ベースのジョブスケジューラ」です。

```
0 2 * * * /path/to/backup.sh
```

このように、

```
分 時 日 月 曜日
```

の5要素でスケジュールを指定し、

> 「指定時刻になったらコマンドを実行する」

という非常に単純な仕組みを持っています。

---

## cron の歴史（1970年代の最適解）

cron が登場したのは **1970年代（Unix V6〜V7）** 。当時の環境は次のようなものでした。

| 項目 | 当時 |
| --- | --- |
| ディスク容量 | 数MB〜数十MB |
| メモリ | 数百KB |
| CPU | 単一コア |
| 常時接続 | なし |
| 管理方法 | 端末＋メール |

この時代において cron は、軽量・シンプル・依存関係なしという **非常に優れた設計** でした。

### cron の「通知」はログではなくメール

cron は「ログを溜める」より「異常を通知する」発想でした。典型的には **stdout/stderr をメールで送る** のが当時の設計です。

<iframe src="https://embed.zenn.studio/mermaid#zenn-embedded__aab0cb93567c5" frameborder="0"></iframe>

---

## 2\. crontab の何が問題だったか？

cron は長年使われてきましたが、現代のサーバ運用では次の問題が顕在化しました。

---

## 問題① 実行されたか分からない（状態がない）

cron には「実行履歴」という概念がありません。

- 成功したか？
- 実行されたか？
- 何秒かかったか？

これらを OS 側で追跡しません。

<iframe src="https://embed.zenn.studio/mermaid#zenn-embedded__242384e1ad73c" frameborder="0"></iframe>

---

## 問題② ログが自動で残らない（可観測性が低い）

cron は標準でログを「保存」しません。  
そのため実務ではよく次のようになります。

```
* * * * * script.sh >> /var/log/script.log 2>&1
```

- 出力先は人力
- ローテーションも自前
- 失敗検知も自作

**運用が属人化しやすい** のが問題でした。

---

## 問題③ サーバ再起動に弱い（取りこぼし）

cron は「時刻」にしか反応しません。

- サーバ停止中に実行時刻を過ぎる
- → そのジョブは永久に失われる
<iframe src="https://embed.zenn.studio/mermaid#zenn-embedded__c4e6f7272ad73" frameborder="0" height="354.796875"></iframe>

---

## 問題④ 依存関係を書けない（起動順が曖昧）

cron では以下のような依存関係を宣言できません。

- ネットワーク起動後に実行
- DB 起動後に実行
- 他プロセス完了後に実行

結果として `sleep 30` のような回避策が増えがちです。

<iframe src="https://embed.zenn.studio/mermaid#zenn-embedded__ad0c9c357406" frameborder="0" height="150.828125"></iframe>

---

## 3\. なぜ systemd でコントロールされるようになったか？

## systemd とは何か

systemd は単なる init システムではありません。

> **Linux 全体を「状態管理する制御基盤」**

として設計されています。

---

## 以前の Linux は機能が分断されていた

以前の Linux は次のように役割が分かれていました。

- init：起動
- cron：定期実行
- syslog：ログ
- udev：デバイス

それぞれ独立しており、OS として一貫した「状態管理」が難しかった、という背景があります。

<iframe src="https://embed.zenn.studio/mermaid#zenn-embedded__873c97ddad902" frameborder="0" height="606.09375"></iframe>

---

## systemd の思想：すべてを unit として状態管理する

systemd は「unit」という単位で、さまざまな対象を管理します。

| Unit | 役割 |
| --- | --- |
| service | プロセス |
| timer | スケジュール |
| socket | ソケット |
| mount | マウント |
| target | グルーピング |

そして各 unit は状態を持ちます。

<iframe src="https://embed.zenn.studio/mermaid#zenn-embedded__9545f37eebdb5" frameborder="0" height="348.484375"></iframe>

---

## timer は cron の単純互換ではない（責務分離）

重要なのはここです。

systemd timer は、

> **「service を起動するトリガー」**

です。実行主体は service で、timer は「いつ」を担当します。

<iframe src="https://embed.zenn.studio/mermaid#zenn-embedded__73cc98c36beaf" frameborder="0" height="65.453125"></iframe>

この責務分離により、

- ログ
- exit code
- 実行履歴
- 再実行制御
- 依存関係

を OS として自然に扱えるようになります。

---

## 4\. systemd-timer の設定方法

systemd timer は **2ファイル1セット** です。

```
my-batch.service
my-batch.timer
```

---

## service ファイル（何を実行するか）

```
[Unit]
Description=My Batch Job
After=network-online.target      # ネットワーク起動後に実行
Requires=network-online.target   # ネットワークが必須

[Service]
Type=oneshot                     # 一度だけ実行して終了するタイプ
ExecStart=/usr/local/bin/batch.sh  # ← 実際に実行されるファイル
```

---

## timer ファイル（いつ実行するか）

```
# /etc/systemd/system/my-batch.timer
[Unit]
Description=Run my batch every day

[Timer]
OnCalendar=*-*-* 02:00:00    # 毎日午前2時に実行
Persistent=true              # 実行時刻を逃しても後で実行

[Install]
WantedBy=timers.target       # systemd起動時にこのtimerも有効化されるよう紐づける
```

---

## 有効化

```
sudo systemctl daemon-reload
sudo systemctl enable --now my-batch.timer
```

---

## 動作確認

次回実行予定を確認：

```
systemctl list-timers
```

ログ確認：

```
journalctl -u my-batch.service
```

---

## Persistent=true の重要性（取りこぼし防止）

```
Persistent=true
```

を指定すると、

> サーバ停止中に実行できなかったジョブを起動後に補完実行

してくれます。

<iframe src="https://embed.zenn.studio/mermaid#zenn-embedded__75aebca46726b" frameborder="0" height="297.234375"></iframe>

---

## 5\. まとめ

## cron は悪ではない

cron は

- 1970年代の制約下での最適解
- 極限までシンプル
- 互換性と堅牢性が高い

という意味で **非常に優秀** でした。今も多くの環境で現役です。

---

## ただし運用要件が変わった

現代では、

- 無人サーバ運用
- 自動復旧
- 可観測性
- 障害の再現性

が強く求められます。

---

## systemd timer は「現代の正解」

systemd timer は、

- スケジューリング
- プロセス管理
- ログ
- 依存関係
- 再実行制御

を統合した仕組みです。

### 一言でまとめると

> cron は「時間を知らせるだけ」  
> systemd timer は「ジョブを管理する」

## 参考資料

- cron – Wikipedia  
	[https://en.wikipedia.org/wiki/Cron](https://en.wikipedia.org/wiki/Cron)
- crontab(5) – Linux manual  
	[https://man7.org/linux/man-pages/man5/crontab.5.html](https://man7.org/linux/man-pages/man5/crontab.5.html)
- Why cron is bad  
	[https://blog.sorryapp.com/blog/2015/02/06/why-cron-is-bad/](https://blog.sorryapp.com/blog/2015/02/06/why-cron-is-bad/)
- systemd Official Documentation  
	[https://www.freedesktop.org/wiki/Software/systemd/](https://www.freedesktop.org/wiki/Software/systemd/)
- systemd.unit(5)  
	[https://man7.org/linux/man-pages/man5/systemd.unit.5.html](https://man7.org/linux/man-pages/man5/systemd.unit.5.html)
- systemd.timer(5)  
	[https://man7.org/linux/man-pages/man5/systemd.timer.5.html](https://man7.org/linux/man-pages/man5/systemd.timer.5.html)
- systemd.service(5)  
	[https://man7.org/linux/man-pages/man5/systemd.service.5.html](https://man7.org/linux/man-pages/man5/systemd.service.5.html)
- Red Hat Enterprise Linux – systemd Guide  
	[https://access.redhat.com/documentation/en-us/red\_hat\_enterprise\_linux/7/html/system\_administrators\_guide/chap-managing\_services\_with\_systemd](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/chap-managing_services_with_systemd)

96