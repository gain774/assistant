#!/usr/bin/env python3
"""アイコン v5: ロボット以外のモチーフ3案(コーラル×クリーム×墨は継続)
E1: 実験フラスコ(実験実況の本質)
E2: 吹き出し+スパーク(AIが発信する、の直喩)
E3: 上昇グラフ+スパーク(数字を公開して伸ばす)
"""
import math

from PIL import Image, ImageDraw

S = 400
OUT = "/tmp/claude-0/-home-user-assistant/630a109f-8176-5850-bdb7-34e2b5c01edb/scratchpad"

CORAL = (217, 119, 87)
CORAL_DEEP = (193, 95, 60)
CREAM = (240, 238, 229)
CREAM_HI = (248, 246, 239)
INK = (38, 38, 37)


def lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def cream_bg():
    img = Image.new("RGB", (S, S))
    px = img.load()
    for y in range(S):
        c = lerp(CREAM_HI, CREAM, y / (S - 1))
        for x in range(S):
            px[x, y] = c
    return img


def spark(d, cx, cy, r_long, r_short, w, color, dot=True):
    for i in range(8):
        a = math.radians(i * 45)
        r = r_long if i % 2 == 0 else r_short
        xt, yt = cx + r * math.cos(a), cy + r * math.sin(a)
        d.line([(cx, cy), (xt, yt)], fill=color, width=w)
        hw = w / 2
        d.ellipse([xt - hw, yt - hw, xt + hw, yt + hw], fill=color)
    if dot:
        d.ellipse([cx - w, cy - w, cx + w, cy + w], fill=color)


# E1: 実験フラスコ(三角フラスコ+コーラルの液体+スパークの泡)
def make_e1():
    img = cream_bg()
    d = ImageDraw.Draw(img)
    # フラスコ本体(墨のシルエット): 首+三角ボディ
    neck_w = 64
    d.polygon([(200 - neck_w/2, 92), (200 + neck_w/2, 92),
               (200 + neck_w/2, 168),
               (312, 318), (300, 344), (100, 344), (88, 318),
               (200 - neck_w/2, 168)], fill=INK)
    d.rounded_rectangle([200 - neck_w/2 - 14, 76, 200 + neck_w/2 + 14, 104], radius=14, fill=INK)
    # 液体(コーラル): ボディ下部
    d.polygon([(147, 238), (253, 238), (296, 296), (290, 326), (110, 326), (104, 296)],
              fill=CORAL)
    # 泡 = 小スパーク(クリーム)
    spark(d, 200, 280, 16, 9, 6, CREAM_HI)
    spark(d, 156, 300, 11, 6, 5, CREAM_HI)
    spark(d, 244, 305, 9, 5, 4, CREAM_HI)
    # 上昇する泡(液面の上)
    spark(d, 205, 210, 10, 6, 5, CORAL)
    spark(d, 190, 140, 7, 4, 4, CORAL)
    return img


# E2: 吹き出し+スパーク(AIが発信する)
def make_e2():
    img = cream_bg()
    d = ImageDraw.Draw(img)
    # 吹き出し(墨)
    d.rounded_rectangle([56, 84, 344, 296], radius=72, fill=INK)
    d.polygon([(118, 270), (108, 352), (196, 292)], fill=INK)
    # 中央にコーラルの大スパーク
    spark(d, 200, 190, 74, 42, 22, CORAL)
    return img


# E3: 上昇グラフ+スパーク(数字を伸ばす)
def make_e3():
    img = cream_bg()
    d = ImageDraw.Draw(img)
    # バー(墨→コーラルへ、上昇)
    bars = [(96, 96, INK), (156, 148, INK), (216, 204, CORAL_DEEP), (276, 268, CORAL)]
    bw = 44
    base = 330
    for x, h, c in bars:
        d.rounded_rectangle([x, base - h, x + bw, base], radius=14, fill=c)
    # 最高点にスパーク
    spark(d, 298, 96, 46, 26, 14, CORAL)
    return img


cands = {"E1": make_e1(), "E2": make_e2(), "E3": make_e3()}
for k, im in cands.items():
    im.save(f"{OUT}/icon_v5_{k}.png")

sheet = Image.new("RGB", (S * 3 + 80, S + 140), (18, 18, 24))
for i, (k, im) in enumerate(cands.items()):
    x = 20 + i * (S + 20)
    sheet.paste(im, (x, 20))
    small = im.resize((48, 48), Image.LANCZOS)
    sheet.paste(small, (x + S // 2 - 24, S + 60))
sheet.save(f"{OUT}/icon_v5_sheet.png")
print("done")
