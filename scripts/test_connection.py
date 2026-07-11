#!/usr/bin/env python3
"""接続テスト: 認証確認 → テスト投稿 → メトリクス取得 → 削除

実行: python3 scripts/test_connection.py
消費クレジット: 投稿$0.015 + 読取数回分(合計 $0.02 前後)
"""
import json
import sys
import time

import x_api


def step(label, status, data, expect=200):
    ok = status == expect
    print(f"{'✅' if ok else '❌'} {label}: HTTP {status}")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    if not ok:
        print("テスト中断。上のエラー内容を確認してください。")
        sys.exit(1)


def main():
    status, data = x_api.me()
    step("認証確認 (/users/me)", status, data)
    username = data.get("data", {}).get("username", "?")
    print(f"→ 認証されたアカウント: @{username}\n")

    status, data = x_api.post(f"接続テスト投稿です(すぐ削除します) {int(time.time())}")
    step("テスト投稿", status, data, expect=201)
    tweet_id = data["data"]["id"]

    time.sleep(3)
    status, data = x_api.metrics([tweet_id])
    step("メトリクス取得", status, data)

    status, data = x_api.delete(tweet_id)
    step("テスト投稿の削除", status, data)

    print("\n🎉 全テスト成功。Phase 0 完了です。")


if __name__ == "__main__":
    main()
