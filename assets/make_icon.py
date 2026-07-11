#!/usr/bin/env python3
"""アイコン v4 最終: Claude配色ロボット(D1改)
- クリーム背景 × 墨色ヘッド × コーラルバイザー(Claude パレットのオマージュ)
- アンテナ先端は小さな4方向スパーク(ロゴ複製ではない控えめな引用)
- 口のバーグラフを低く・短く修正(ドクロ感の解消)
"""
import math

from PIL import Image, ImageDraw

S = 400
OUT = "/tmp/claude-0/-home-user-assistant/630a109f-8176-5850-bdb7-34e2b5c01edb/scratchpad"

CORAL = (217, 119, 87)
CORAL_DEEP = (193, 95, 60)
CORAL_LIGHT = (232, 150, 116)
CREAM = (240, 238, 229)
CREAM_HI = (248, 246, 239)
INK = (38, 38, 37)


def lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


img = Image.new("RGB", (S, S))
px = img.load()
for y in range(S):
    c = lerp(CREAM_HI, CREAM, y / (S - 1))
    for x in range(S):
        px[x, y] = c
d = ImageDraw.Draw(img)

x0, y0, x1, y1 = 84, 116, 316, 324
w = x1 - x0
cx = (x0 + x1) / 2

# アンテナ軸
d.line([(cx, y0 - 34), (cx, y0 + 4)], fill=INK, width=12)

# アンテナ先端: 小さな8方向スパーク(コーラル・長短交互)
scx, scy = cx, y0 - 54
for i in range(8):
    a = math.radians(i * 45)
    r = 26 if i % 2 == 0 else 15
    x_t, y_t = scx + r * math.cos(a), scy + r * math.sin(a)
    d.line([(scx, scy), (x_t, y_t)], fill=CORAL, width=9)
    d.ellipse([x_t - 4.5, y_t - 4.5, x_t + 4.5, y_t + 4.5], fill=CORAL)
d.ellipse([scx - 9, scy - 9, scx + 9, scy + 9], fill=CORAL)

# 耳
ear_w, ear_h = w * 0.11, w * 0.34
ey = y0 + (y1 - y0) * 0.30
d.rounded_rectangle([x0 - ear_w * 0.8, ey, x0 + ear_w * 0.2, ey + ear_h],
                    radius=int(ear_w * 0.4), fill=INK)
d.rounded_rectangle([x1 - ear_w * 0.2, ey, x1 + ear_w * 0.8, ey + ear_h],
                    radius=int(ear_w * 0.4), fill=INK)

# 頭
d.rounded_rectangle([x0, y0, x1, y1], radius=int(w * 0.27), fill=INK)

# バイザー(コーラル横グラデ)
vx0, vx1 = x0 + w * 0.14, x1 - w * 0.14
vy0 = y0 + (y1 - y0) * 0.28
vy1 = vy0 + (y1 - y0) * 0.27
vmask = Image.new("L", (S, S), 0)
ImageDraw.Draw(vmask).rounded_rectangle([vx0, vy0, vx1, vy1],
                                        radius=int((vy1 - vy0) / 2), fill=255)
vgrad = Image.new("RGB", (S, S))
vpx = vgrad.load()
for x in range(S):
    c = lerp(CORAL_LIGHT, CORAL_DEEP, x / (S - 1))
    for y in range(S):
        vpx[x, y] = c
img.paste(vgrad, (0, 0), vmask)

# 目(クリームの丸)
ew = (vy1 - vy0) * 0.60
ecy = (vy0 + vy1) / 2
for ecx in (cx - w * 0.17, cx + w * 0.17):
    d.ellipse([ecx - ew / 2, ecy - ew / 2, ecx + ew / 2, ecy + ew / 2], fill=CREAM_HI)

# 口: バーグラフ(低め・短め・上向き成長)
heights = [26, 40, 32, 52]
bw, gap = 24, 16
total = 4 * bw + 3 * gap
bx = cx - total / 2
by = y1 - (y1 - y0) * 0.13
for i, h in enumerate(heights):
    x = bx + i * (bw + gap)
    d.rounded_rectangle([x, by - h, x + bw, by], radius=7, fill=CORAL)

img.save(f"{OUT}/icon_v4_final.png")
img.resize((48, 48), Image.LANCZOS).save(f"{OUT}/icon_v4_final_48.png")

sheet = Image.new("RGB", (S + 40 + 96, S + 40), (18, 18, 24))
sheet.paste(img, (20, 20))
sheet.paste(img.resize((96, 96), Image.LANCZOS), (S + 30, 20))
sheet.paste(img.resize((48, 48), Image.LANCZOS), (S + 30, 140))
sheet.save(f"{OUT}/icon_v4_final_sheet.png")
print("done")
