---
type: runbook
topic: 毎朝の日次運用 実行手順書(Routine 用)
created: 2026-07-11
updated: 2026-07-11
tags: [assistant, runbook, AI自動化, X-API]
related: "[[daily-operations]]"
status: 運用中
---

# 日次運用 実行手順書(毎朝 7:00 JST に Routine が実行)

このファイルは毎朝の Routine で実行する指示書。設計の背景は `plans/daily-operations.md`。
**日付・時刻はすべて JST 基準で判断すること**(実行環境の時計が UTC の場合は +9 時間)。

⚠️ **Routine はメインセッション(リポジトリ接続済み)に発火させること**。新規セッション方式は
リポジトリも GitHub アクセスも無く実行不能(2026-07-12 の障害で確認)。実行開始時は
`git pull origin main` で最新化してから手順に入る。

## 大原則(毎回最初に確認)
1. **ユーザーの承認がない投稿は絶対に出さない**。承認の返信がなければ投稿ゼロで終了(それが正常系)
2. APIキーの値をチャット・ログ・コミットに出さない
3. `log/sns/state.json` の `mistakes_checklist` を読み、投稿案作成時に毎項目照合する
4. 投稿数の上限は state.json の `posting.daily_range`(現在のランプアップ段階)に従う
5. **自律運用モード**(CLAUDE.md 参照): 承認・画面操作・課金以外は AI が判断して実行する。
   運用上の判断・改善を行ったら `log/decisions.md` に記録する(記録してから動く)
6. **日曜は週次見直し**: 週報作成に加え、runbook / content-strategy / daily-operations を
   数字に基づいて見直し、改善は自分で反映する(decisions.md に記録)。月初はさらに CLAUDE.md 含む全体棚卸し

## 手順

### 1. 状態の読み込み
- `log/sns/state.json` を読む(投稿履歴・前日のリサーチ・チェックリスト・コスト)
- `plans/content-strategy.md` のネタ帳と型カタログを読む

### 2. メトリクス取得
- state.json の `posts` から直近7日の投稿IDを集め、
  `python3 scripts/x_api.py metrics <id,id,...>` で取得(1コールでまとめる)
- `python3 scripts/x_api.py me` でフォロワー数を取得
- 取得結果を state.json の該当投稿の `metrics` に書き込む。コストを概算加算

### 3. トレンドリサーチと差分比較
- WebSearch で当日の話題をリサーチ(AI・自動化・SNS運用まわり+一般トレンド)
- state.json の `research_cache`(前日分)と比較し、daily-operations.md 3-2 の表に従い判断:
  持続トレンド=解説系に / 当日のみ=鮮度勝負 / 消えた=原則破棄 / 両方有望=両方使う
- 当日のリサーチ結果を `research_cache` に上書き保存

### 4. 日次レポート生成
- `log/sns/templates/daily.md` の形式で `log/sns/daily/YYYY-MM-DD.md` を作成
- **`plans/goals.md` の日次・週次・月次目標との対比を必ず記載する**(フォロワー進捗、インプ前日比、
  収益アクションの進捗。未達なら「次の一手」を書く)
- 振り返り(仮説→結果→学び)を書く。ミスがあれば `mistakes_checklist` に追加
- **日曜日は週報も作成**(`log/sns/templates/weekly.md` → `log/sns/weekly/YYYY-Www.md`)。
  週報ではランプアップ判断(頻度の維持/増/減)を行い、変更時は state.json の
  `posting` と `ramp_history` を更新する

### 5. 投稿案の生成
- **5本**(第1段階の上限に固定。2026-07-12 の自己監査による)。型カタログから配分し、
  **問いかけ型を1本以上、引用ポスト型を1〜2本**入れる
- 引用対象の探し方: リサーチで見つけたニュースの公式アカウント(例: LINEヤフー、OpenAI、
  AnthropicAI 等)の直近ポストを `python3 scripts/x_api.py user <username>` → `tweets <user_id>` で
  取得し、該当発表のポストIDを引用する(`post "本文" <quote_tweet_id>`)
- 各案に投稿予定時刻を割り当てる(`best_slots_jst` に分散。連投しない)
- A/B実験: 前週の週報で決めた「変える変数1つ」を反映
- 各案を `mistakes_checklist` と炎上リスク基準(政治・宗教・特定個人/企業・医療/投資断言)で検査
- URLは入れない。ハッシュタグ0〜1個

### 6. コミット(承認前)
- レポート・state.json を **main に直接コミット&プッシュ**(承認済みの運用ルール)
- コミットメッセージ例: `sns: 日次レポート 2026-07-14`

### 7. 承認依頼と待機
- ユーザーに投稿案を番号付きで提示し、承認を依頼(このセッションへの返信で承認してもらう)
- **PushNotification ツールでスマホに承認依頼を通知する**(ツールが無ければ ToolSearch で読み込む)
- 返信例への対応: 「全部OK」= 全部 / 「1と3」= その番号のみ / 「2はこう直して…」= 修正して再提示
- **返信がないまま終了した場合は投稿しない**。レポートに「未承認・投稿スキップ」と記録

### 8. 投稿の実行(承認後)
- 現在時刻が予定時刻を過ぎている案は即時投稿: `python3 scripts/x_api.py post "本文"`
- まだ先の案は `send_later` で予定時刻に自分を起こし、その時に投稿する
- 投稿したら ID・本文・型・時刻を state.json の `posts` に追記し、コスト加算、main にコミット&プッシュ

### 9. 終了時
- その日の要約(投稿数・特記事項)を短くユーザーに報告して終了

## 障害時の対応
- `api.x.com` に 403 (proxy) → 実行環境のネットワーク許可が外れている。ユーザーに設定変更を依頼して終了
- X API がエラー → 3回までリトライ(投稿の重複に注意: 成功レスポンスを受けた投稿は再送しない)
- リポジトリの push が競合 → pull してリトライ
- 判断に迷う内容 → 投稿せず、レポートに疑問点を書いてユーザーに確認
