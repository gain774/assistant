---
type: research
topic: ツール・API・MCP・コネクタの調査(能力とコスト削減)
created: 2026-07-13
updated: 2026-07-13
tags: [assistant, research, ツール, コスト効率]
related: "[[next-run-kit]]"
status: 運用中(週次で更新)
---

# ツール・API・MCP・コネクタ調査

「便利/コスト削減になるツールを、Claude だけでなく X 一次リサーチでも探して先に見つける」ための
継続調査。**週次(日曜)に更新**。検証したら結果を残す(推測で終わらせない)。

## 導入済み・検証済み(使えるもの)
| 能力 | 状態 | メモ |
|---|---|---|
| X API 投稿/削除/メトリクス | ✅ | pay-per-use: 投稿$0.015、読取$0.005 |
| X API `user`/`tweets` | ✅ | 公式アカの投稿取得(話題便乗の元ネタ) |
| X API `search`(recent) | ✅ 2026-07-13 | **ニッチの実投稿を一次分析**。伸びてる型の抽出に使う |
| **X API 画像投稿**(`upload`/`post_image`) | ✅ 2026-07-13 検証 | v2 `/2/media/upload` マルチパート→media_id→投稿。**画像はエンゲージ増**。PIL で自前生成(追加コストほぼ0) |
| v1.1 profile/pin/icon 設定 | ✅ | bio・固定・アイコンを API で設定可 |
| Routine(Claude Code Remote) | ✅ | 定期実行・通知。メインセッション発火方式 |
| PIL(画像生成) | ✅ | アイコン・投稿画像をコードで生成 |

## 使えない/不採用(検証で判明)
- ブラウザ自動操作(Chromium): プロキシ不通で全滅 → reCAPTCHA系サイト登録は不可
- 引用ポスト(quote_tweet_id): 他人投稿は403 → 単独ポストで代替
- X 広告収益分配: 条件が重く不採用
- `upload.twitter.com`: ネット許可外(api.x.com の v2 upload を使えば回避)

## 未検証・今後試す候補(週次で1つずつ潰す)
- X API `/2/tweets/counts/recent`: トレンド語の投稿量を数値で取得 → ネタ選定の精度UP
- X API bookmarks/liked lookup: 自分の投稿の保存内訳の把握
- Google Drive/Calendar コネクタ: 資産保管・スケジュール(現状は不要と判断)
- 画像を使った「保存誘発型」投稿(リスト/Tier表を画像化)→ ブックマーク増を狙う(次に実運用でA/B)

## コスト(トークン)削減の観点
- 投稿は1日3本、予約トリガーも最小化(セッション発火数=コスト)
- リサーチは価値の高いものに集中。search は max_results を絞る
- ドキュメントはスクリプト追記で全文読み直しを避ける

## ネットワーク許可の全数実測(2026-07-13)
※重要: **リサーチは WebSearch ツールで可能**(直接 curl がブロックでも WebSearch は通る)。
下の「BLOCK」はプログラム直アクセスの可否であり、情報収集そのものは止まらない。

**現在OK(追加不要)**: api.x.com / api.twitter.com / github.com / api.github.com / pypi.org / googleapis.com / note.com

**開けてほしい(プラン上必要・優先順)**:
| ドメイン | 用途 | 優先 |
|---|---|---|
| `zenn.dev` | 収益の主軸(公開はgit経由で可だが、公開結果の確認・Zenn APIに必要) | 高 |
| `api.gumroad.com` | 自動化可能な有料販売(トークン認証・ブラウザ不要)。Zennの保険 | 高 |
| `af.moshimo.com` `www.a8.net` `www.valuecommerce.ne.jp` | アフィリエイトASP。※リンク取得はダッシュボード(人間ログイン)要 | 中 |
| `www.amazon.co.jp` `www.rakuten.co.jp` | アフィリエイト商品/リンク確認 | 中 |
| `api.x.ai` | Grok API(補助的な文章生成に使える可能性・要検証) | 低 |

**不要と確定**: `upload.twitter.com`(api.x.com の v2 upload で代替済み)/ トレンド・ニュース直サイト
(trends24 等は WebSearch で代替)

## 調査の進め方(継続ルール)
- 週次で「X で実運用者が使っているツール」を `x_api.py search` で拾い、有望なら**実際に叩いて検証**
- 使えたものは上表に追加し、投稿/収益に効くものは content-strategy / goals に反映
