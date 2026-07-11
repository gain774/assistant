---
type: guide
topic: Phase 0 セットアップ手順書
created: 2026-07-09
updated: 2026-07-11
tags: [assistant, guide, AI自動化, X-API]
related: "[[ai-sns-automation]]"
status: 完了
---

# Phase 0 手順書: X 自動運用のセットアップ

本人がやるのは Step 1〜5(合計 40〜60 分、分割OK)。Step 6 以降はアシスタントの作業。

## Step 0: 決めておくこと(5分)
- [ ] アカウントのテーマ(推奨: 「AIにSNS運用させてみた」実験実況 × AI・自動化ネタ)
- [ ] アカウント名(例: 「AI運用実験室」系。後から変更可能なので仮でOK)
- [ ] 登録用メールアドレス(本垢と別のもの。Gmail なら新規エイリアスや別アドレス)

## Step 1: 実験用 X アカウント開設(スマホOK・10分)
1. X アプリまたは x.com で新規アカウント作成(**本垢からログアウトしてから**、または「アカウントを追加」)
2. 電話番号認証を済ませる(未認証アカウントは凍結されやすい)
3. プロフィール文・アイコンは仮でOK(後でアシスタントが案を作る)
4. **自動アカウントラベルの設定**(規約対応。Developer 登録後でも可):
   設定とプライバシー → アカウント → アカウント情報 → 自動化 → 管理者として本垢を指定

## Step 2: X Developer 登録(PC推奨、スマホブラウザでも可・15分)
1. **実験用アカウントでログインした状態**で https://developer.x.com へ
2. 「Sign up for Free Account」等のボタンから開発者登録
3. 利用目的を英語で聞かれたら(和訳: 自分のアカウントの自動投稿と分析の個人実験):
   `Automated posting and analytics for my own account as a personal learning experiment. No third-party data collection.`
4. 規約に同意して Developer Console(ダッシュボード)に入る

## Step 3: クレジットチャージ($5〜・5分)
- 2026年2月から**従量課金(pay-per-use)がデフォルト**。Console 内の Billing / Credits でカードを登録し **$5(約800円)** をチャージ
- 新規登録者には **$10 クーポン**が付与される場合あり → その場合はチャージ不要で始められる
- 参考単価: テキスト投稿 $0.015/件、自分の投稿のメトリクス取得 $0.001/リソース(月の運用コストは数百円)

## Step 4: アプリ設定と API キー発行(15分)⚠️ここが一番間違えやすい
1. Console に Project と App が自動作成される(なければ Create Project → Create App)
2. App の **User authentication settings** → Set up:
   - App permissions: **Read and write** ←最重要
   - Type of App: **Web App, Automated App or Bot**
   - Callback URI: `http://localhost`(ダミーでOK・必須項目)
   - Website URL: 自分の GitHub プロフィール URL などでOK
3. **Keys and tokens** タブで以下の4つを取得(メモ帳などに一時保存):
   - API Key(Consumer Key)
   - API Key Secret
   - Access Token
   - Access Token Secret
4. ⚠️ **Access Token / Secret は権限を Read and write にした「後」に Regenerate する**。
   トークンの下に「Created with Read and Write permissions」と表示されていることを確認。
   (Read only 時代のトークンのままだと投稿が 403 エラーになる)

## Step 5: 環境変数への登録(5分)
Claude Code(claude.ai/code)のこのリポジトリの**環境(Environment)設定 → 環境変数**に以下の4つを登録:

| 変数名 | 値 |
|---|---|
| `X_API_KEY` | API Key |
| `X_API_SECRET` | API Key Secret |
| `X_ACCESS_TOKEN` | Access Token |
| `X_ACCESS_TOKEN_SECRET` | Access Token Secret |

登録できたら、一時保存したメモは削除する。

### 🔒 セキュリティの鉄則
- キーは**チャットに直接貼らない**(会話ログに残るため)
- **リポジトリにコミットしない**(環境変数のみ)
- このキーはアカウントの投稿権限そのもの。パスワードと同じ扱いで

## Step 6: 動作確認(アシスタントの作業)
- [x] 認証テスト(自分のアカウント情報取得)— 2026-07-11 成功。アカウント @AISNS1st を確認
- [x] テスト投稿 → メトリクス取得 → テスト投稿の削除 — 2026-07-11 全ステップ成功(投稿は削除済み)
- [ ] 投稿/取得スクリプトと日次レポートの仕組みを構築
- [ ] 毎朝の Routine(定期実行)を設定

> 📝 メモ: 実行環境のネットワークポリシーで `api.x.com` の許可が必要(2026-07-11 に設定済み)。
> 新しい環境を作る場合は許可ドメインに `api.x.com` を追加すること。

## つまずいたら
- 各画面のUIは頻繁に変わる。表示が手順と違ったら、**画面のスクリーンショットを送ってもらえればその場で案内する**
- 403 エラー → Step 4-4(権限とトークン再生成)の確認が第一容疑者
