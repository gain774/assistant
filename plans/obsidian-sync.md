---
type: guide
topic: Obsidian への自動同期セットアップ(1回だけ・約5分)
created: 2026-07-12
updated: 2026-07-12
tags: [assistant, guide, Obsidian]
status: 本人作業待ち
---

# Obsidian 自動同期のセットアップ(デスクトップ・1回だけ)

このリポジトリの全ドキュメント(レポート・計画・判断記録)は Obsidian 互換で書いてある。
以下を1回設定すれば、**AI が push した内容がすべて自動で Obsidian に現れる**(以後の操作ゼロ)。

## 手順(約5分)

1. デスクトップの Obsidian で保管庫(Vault)を開く(新規でも既存でもOK)
2. 設定 → コミュニティプラグイン → 閲覧 → **「Git」**(obsidian-git)を検索してインストール→有効化
3. PC のターミナルで、Vault のフォルダ内にこのリポジトリをクローン:
   `git clone https://github.com/gain774/assistant.git`
   (Vault の中に `assistant` フォルダができる)
4. Obsidian の Git プラグイン設定で **「Auto pull interval」を 10(分)** に設定
5. 完了。以後、AI の全成果物が10分以内に Obsidian に自動反映される

## 補足

- スマホの Obsidian でも見たい場合: Obsidian 公式の Sync(有料)か、iOS なら a-Shell + git 等で可能。
  まずはデスクトップだけで十分
- このリポジトリ側の作業(frontmatter 付与・リンク互換)は AI が保証する。ドキュメントの置き場所や
  形式の希望があれば言ってもらえれば AI 側で直す
