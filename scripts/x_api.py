#!/usr/bin/env python3
"""X API v2 クライアント(OAuth 1.0a・標準ライブラリのみ)

環境変数 X_API_KEY / X_API_SECRET / X_ACCESS_TOKEN / X_ACCESS_TOKEN_SECRET を使う。
使い方: python3 scripts/x_api.py me | post "テキスト" | delete <id> | metrics <id,id,...>
"""
import base64
import hashlib
import hmac
import json
import os
import secrets
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.x.com/2"


def _env(name: str) -> str:
    v = os.environ.get(name, "").strip()
    if not v:
        raise SystemExit(f"環境変数 {name} が設定されていません")
    return v


def _pct(s) -> str:
    # OAuth 1.0a はRFC3986のパーセントエンコード(unreserved以外全て)を要求する
    return urllib.parse.quote(str(s), safe="-._~")


def _oauth_header(method: str, url: str, query: dict | None) -> str:
    oauth = {
        "oauth_consumer_key": _env("X_API_KEY"),
        "oauth_nonce": secrets.token_hex(16),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": _env("X_ACCESS_TOKEN"),
        "oauth_version": "1.0",
    }
    params = {**oauth, **(query or {})}
    # 署名はエンコード後のキーでソートしたパラメータ文字列に対して行う
    pairs = sorted((_pct(k), _pct(v)) for k, v in params.items())
    param_str = "&".join(f"{k}={v}" for k, v in pairs)
    base = "&".join([method.upper(), _pct(url), _pct(param_str)])
    key = f"{_pct(_env('X_API_SECRET'))}&{_pct(_env('X_ACCESS_TOKEN_SECRET'))}".encode()
    sig = base64.b64encode(hmac.new(key, base.encode(), hashlib.sha1).digest()).decode()
    oauth["oauth_signature"] = sig
    return "OAuth " + ", ".join(f'{_pct(k)}="{_pct(v)}"' for k, v in sorted(oauth.items()))


def _ssl_context() -> ssl.SSLContext:
    cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if not cafile and os.path.exists("/root/.ccr/ca-bundle.crt"):
        cafile = "/root/.ccr/ca-bundle.crt"
    return ssl.create_default_context(cafile=cafile)


def request(method: str, path: str, query: dict | None = None, body: dict | None = None):
    url = API_BASE + path
    full = url
    if query:
        full += "?" + "&".join(f"{_pct(k)}={_pct(v)}" for k, v in sorted(query.items()))
    req = urllib.request.Request(full, method=method)
    req.add_header("Authorization", _oauth_header(method, url, query))
    req.add_header("User-Agent", "assistant-experiment/0.1")
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode()
        req.add_header("Content-Type", "application/json")
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=_ssl_context()))
    try:
        with opener.open(req, data) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            detail = json.loads(e.read().decode() or "{}")
        except Exception:
            detail = {}
        return e.code, detail


def me():
    return request("GET", "/users/me", {"user.fields": "public_metrics,created_at"})


def post(text: str, quote_tweet_id: str | None = None):
    body = {"text": text}
    if quote_tweet_id:
        body["quote_tweet_id"] = quote_tweet_id
    return request("POST", "/tweets", body=body)


def delete(tweet_id: str):
    return request("DELETE", f"/tweets/{tweet_id}")


def metrics(ids: list[str]):
    return request("GET", "/tweets", {"ids": ",".join(ids), "tweet.fields": "public_metrics,created_at"})


def user_by_username(username: str):
    return request("GET", f"/users/by/username/{username}", {"user.fields": "public_metrics"})


def search(query: str, max_results: int = 25):
    # 直近の投稿を検索(ニッチ調査・伸びてる投稿の分析に使う)。lang:ja -is:retweet 等が使える
    return request("GET", "/tweets/search/recent",
                   {"query": query, "max_results": str(max_results),
                    "tweet.fields": "public_metrics,created_at"})


def user_tweets(user_id: str, max_results: int = 5):
    # 引用ポストの対象探しに使う(公式・ニュース系アカウントの直近ポスト取得)
    return request("GET", f"/users/{user_id}/tweets",
                   {"max_results": str(max_results), "tweet.fields": "public_metrics,created_at",
                    "exclude": "replies,retweets"})


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "me"
    if cmd == "me":
        status, data = me()
    elif cmd == "post":
        status, data = post(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif cmd == "delete":
        status, data = delete(sys.argv[2])
    elif cmd == "metrics":
        status, data = metrics(sys.argv[2].split(","))
    elif cmd == "user":
        status, data = user_by_username(sys.argv[2])
    elif cmd == "tweets":
        status, data = user_tweets(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 5)
    elif cmd == "search":
        status, data = search(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 25)
    else:
        raise SystemExit(f"不明なコマンド: {cmd}")
    print(status)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    sys.exit(0 if 200 <= status < 300 else 1)
