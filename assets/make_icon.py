#!/usr/bin/env python3
"""アイコン v2: リサーチに基づく再設計
- 明るいシアン系グラデ背景(ライト/ダーク両タイムラインで目立つ・テーマカラー化)
- 紺のロボット顔を大きく(占有率 ~75%)、白フチで小サイズ視認性を確保
- 口はバーグラフ(数字公開アカウントの象徴・記憶フック)
"""
import base64
import sys
import urllib.error
import urllib.request
import json

from PIL import Image, ImageDraw

sys.path.insert(0, "/home/user/assistant/scripts")
import x_api

S = 400
NAVY = (14, 22, 48)      # 顔
WHITE = (255, 255, 255)

# 背景: シアン→ブルーの縦グラデ
img = Image.new("RGB", (S, S))
top = (79, 195, 247)     # #4FC3F7
bottom = (30, 136, 229)  # #1E88E5
px = img.load()
for y in range(S):
    t = y / (S - 1)
    c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    for x in range(S):
        px[x, y] = c
d = ImageDraw.Draw(img)

# アンテナ(紺+白玉)
d.line([(S/2, 42), (S/2, 84)], fill=NAVY, width=14)
d.ellipse([S/2-20, 10, S/2+20, 50], fill=WHITE, outline=NAVY, width=6)

# 顔: 白フチ付きの紺・角丸四角(占有率拡大)
d.rounded_rectangle([44, 84, 356, 366], radius=64, fill=WHITE)              # 白フチ
d.rounded_rectangle([56, 96, 344, 354], radius=56, fill=NAVY)               # 顔本体

# 耳(白)
d.rounded_rectangle([24, 180, 56, 280], radius=12, fill=WHITE)
d.rounded_rectangle([344, 180, 376, 280], radius=12, fill=WHITE)

# 目: 大きな白い丸(小サイズでも「顔」と分かる最重要パーツ)
d.ellipse([108, 150, 182, 224], fill=WHITE)
d.ellipse([218, 150, 292, 224], fill=WHITE)

# 口: バーグラフ(シアン、上向き成長)
bar_c = (79, 195, 247)
for i, h in enumerate([22, 36, 30, 52]):
    x = 122 + i * 42
    d.rounded_rectangle([x, 312 - h, x + 28, 312], radius=7, fill=bar_c)

path = "/tmp/claude-0/-home-user-assistant/630a109f-8176-5850-bdb7-34e2b5c01edb/scratchpad/icon_v2.png"
img.save(path, "PNG")

# 小サイズ確認用(48px = タイムライン相当)
img.resize((48, 48), Image.LANCZOS).save(path.replace(".png", "_48.png"))
print("saved:", path)

# アップロード
with open(path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()
URL = "https://api.x.com/1.1/account/update_profile_image.json"
auth = x_api._oauth_header("POST", URL, {"image": b64})
req = urllib.request.Request(URL, method="POST", data=f"image={x_api._pct(b64)}".encode())
req.add_header("Authorization", auth)
req.add_header("Content-Type", "application/x-www-form-urlencoded")
req.add_header("User-Agent", "assistant-experiment/0.1")
opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=x_api._ssl_context()))
try:
    with opener.open(req) as r:
        data = json.loads(r.read().decode())
        print(r.status, "updated:", data.get("profile_image_url_https"))
except urllib.error.HTTPError as e:
    print(e.code, e.read().decode()[:300])
