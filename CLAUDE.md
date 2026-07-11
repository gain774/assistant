# assistant リポジトリについて

これはユーザーの個人アシスタント用リポジトリ。コードベースではなく「記憶と作業場」。
**ユーザーとのやり取りはすべて日本語で行うこと。**

## まず読むもの
- `profile.md` — ユーザーのプロフィール(20代・製造/技術系会社員・開発初心者。行動前に確認を好む)
- `plans/side-income.md` — 副業戦略(月3〜5万円目標)
- `plans/ai-sns-automation.md` — 進行中のメインプロジェクト: Claude による X アカウント自動運用実験
- `plans/phase0-setup.md` — セットアップ手順書と進捗

## 現在の状態(2026-07-11 時点)
- Phase 0 進行中: X Developer 登録・$5チャージ・APIキー発行・環境変数登録まで完了
- 次のタスク: **接続テスト** — `python3 scripts/test_connection.py` を実行する
  (環境変数 X_API_KEY / X_API_SECRET / X_ACCESS_TOKEN / X_ACCESS_TOKEN_SECRET が必要)
- 接続テスト成功後: 日次運用の仕組み(投稿生成→承認→投稿、日次レポート、Routine)の構築へ

## ツール
- `scripts/x_api.py` — X API v2 クライアント(OAuth 1.0a、標準ライブラリのみ)
  - `python3 scripts/x_api.py me | post "text" | delete <id> | metrics <id,...>`
- `scripts/test_connection.py` — 接続テスト一式(認証→投稿→計測→削除)

## 鉄則
- APIキーの値を**チャット・ログ・コミットに絶対に出さない**(環境変数のみ。過去に一度チャットに貼られ再生成済み)
- X の自動化ルール順守: 低頻度投稿(1日2〜3件)、自動フォロー/いいね/DMはしない、bot であることを bio で開示
- 投稿など外部に見える操作は、事前にユーザーの承認を得る(Phase A の間)
- レポート類は Obsidian 互換の Markdown(YAML frontmatter 付き)で書く。正式保存先は将来的にユーザーの Obsidian
