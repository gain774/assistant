#!/usr/bin/env python3
"""アイコン v3 候補生成: ネオン/グロー系の「AI感」デザイン3案"""
import math

from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 400
OUT = "/tmp/claude-0/-home-user-assistant/630a109f-8176-5850-bdb7-34e2b5c01edb/scratchpad"

CYAN = (34, 211, 238)
VIOLET = (192, 132, 252)
BLUE = (59, 130, 246)


def radial_bg(inner=(19, 28, 58), outer=(6, 9, 26), cx=200, cy=180):
    img = Image.new("RGB", (S, S))
    px = img.load()
    maxd = math.hypot(max(cx, S - cx), max(cy, S - cy))
    for y in range(S):
        for x in range(S):
            t = min(1.0, math.hypot(x - cx, y - cy) / maxd)
            px[x, y] = tuple(int(inner[i] + (outer[i] - inner[i]) * t) for i in range(3))
    return img


def lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def grad_x(c1, c2):
    """横方向グラデーション画像"""
    img = Image.new("RGB", (S, S))
    px = img.load()
    for x in range(S):
        c = lerp(c1, c2, x / (S - 1))
        for y in range(S):
            px[x, y] = c
    return img


def glow(base, draw_fn, blur, alpha=255):
    """透明レイヤーに draw_fn で描き、ぼかして重ねる"""
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    if alpha < 255:
        a = layer.getchannel("A").point(lambda v: v * alpha // 255)
        layer.putalpha(a)
    base.alpha_composite(layer)


def crisp(base, draw_fn):
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    base.alpha_composite(layer)


# ---------- 案A: ニューラルネットワーク ----------
def make_a():
    img = radial_bg().convert("RGBA")
    nodes = [(200, 84), (116, 138), (284, 138), (76, 224), (200, 196),
             (324, 224), (136, 296), (264, 296), (200, 352)]
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 4), (2, 5),
             (3, 4), (3, 6), (4, 6), (4, 7), (5, 7), (6, 8), (7, 8), (4, 5) ]

    def col(x):
        return lerp(CYAN, VIOLET, x / S)

    def draw_edges(d, w):
        for a, b in edges:
            ax, ay = nodes[a]; bx, by = nodes[b]
            c = col((ax + bx) / 2)
            d.line([(ax, ay), (bx, by)], fill=c + (255,), width=w)

    glow(img, lambda d: draw_edges(d, 9), blur=10, alpha=170)
    crisp(img, lambda d: draw_edges(d, 4))

    def draw_nodes_glow(d):
        for x, y in nodes:
            c = col(x)
            d.ellipse([x - 17, y - 17, x + 17, y + 17], fill=c + (255,))

    def draw_nodes_core(d):
        for x, y in nodes:
            c = col(x)
            d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=c + (255,))
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(240, 250, 255, 255))

    glow(img, draw_nodes_glow, blur=12, alpha=200)
    crisp(img, draw_nodes_core)
    return img.convert("RGB")


# ---------- 案B: バイザー型ロボット ----------
def make_b():
    img = Image.new("RGB", (S, S))
    px = img.load()
    for y in range(S):
        c = lerp((13, 18, 44), (22, 30, 68), y / (S - 1))
        for x in range(S):
            px[x, y] = c
    img = img.convert("RGBA")

    # アンテナ
    glow(img, lambda d: d.ellipse([182, 30, 218, 66], fill=CYAN + (255,)), blur=14, alpha=200)
    crisp(img, lambda d: (
        d.line([(200, 66), (200, 104)], fill=(90, 104, 150, 255), width=12),
        d.ellipse([188, 36, 212, 60], fill=(235, 250, 255, 255))))

    # 頭部(グラデ+マスク)
    head_grad = grad_x((46, 56, 100), (28, 35, 70)).rotate(90).convert("RGBA")
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([84, 104, 316, 312], radius=64, fill=255)
    img.paste(head_grad, (0, 0), mask)
    crisp(img, lambda d: d.rounded_rectangle([84, 104, 316, 312], radius=64,
                                             outline=(96, 112, 168, 255), width=4))
    # 耳
    crisp(img, lambda d: (
        d.rounded_rectangle([56, 172, 84, 258], radius=12, fill=(52, 62, 108, 255)),
        d.rounded_rectangle([316, 172, 344, 258], radius=12, fill=(52, 62, 108, 255))))

    # バイザー(発光する一本ライン)
    def visor_glow(d):
        d.rounded_rectangle([116, 180, 284, 232], radius=26, fill=CYAN + (255,))
    glow(img, visor_glow, blur=18, alpha=230)
    # バイザー本体: シアン→ブルーのグラデ
    visor_grad = grad_x(CYAN, BLUE).convert("RGBA")
    vmask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(vmask).rounded_rectangle([120, 184, 280, 228], radius=22, fill=255)
    img.paste(visor_grad, (0, 0), vmask)
    # バイザー内の目(明るいコア2つ)
    glow(img, lambda d: (
        d.ellipse([150, 194, 178, 218], fill=(255, 255, 255, 255)),
        d.ellipse([222, 194, 250, 218], fill=(255, 255, 255, 255))), blur=4)

    # 口: 小さな発光バーグラフ(数字公開の象徴を継承)
    def bars(d):
        for i, h in enumerate([12, 22, 16, 30]):
            x = 152 + i * 28
            d.rounded_rectangle([x, 282 - h, x + 16, 282], radius=5, fill=CYAN + (255,))
    glow(img, bars, blur=6, alpha=160)
    crisp(img, bars)
    return img.convert("RGB")


# ---------- 案C: AI モノグラム ----------
def make_c():
    img = radial_bg().convert("RGBA")
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 190)

    tmask = Image.new("L", (S, S), 0)
    td = ImageDraw.Draw(tmask)
    bbox = td.textbbox((0, 0), "AI", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pos = ((S - tw) / 2 - bbox[0], (S - th) / 2 - bbox[1] - 6)
    td.text(pos, "AI", font=font, fill=255)

    # グロー
    gl = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gl.paste(grad_x(CYAN, VIOLET).convert("RGBA"), (0, 0), tmask)
    img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(14)))
    # 本体
    body = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    body.paste(grad_x((190, 245, 255), (225, 200, 255)).convert("RGBA"), (0, 0), tmask)
    img.alpha_composite(body)

    # 外周リング(グラデ+グロー)
    ring_mask = Image.new("L", (S, S), 0)
    rd = ImageDraw.Draw(ring_mask)
    rd.ellipse([14, 14, 386, 386], outline=255, width=10)
    ring = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ring.paste(grad_x(CYAN, VIOLET).convert("RGBA"), (0, 0), ring_mask)
    img.alpha_composite(ring.filter(ImageFilter.GaussianBlur(6)))
    img.alpha_composite(ring)
    return img.convert("RGB")


cands = {"A": make_a(), "B": make_b(), "C": make_c()}
for k, im in cands.items():
    im.save(f"{OUT}/icon_v3_{k}.png")
    im.resize((48, 48), Image.LANCZOS).save(f"{OUT}/icon_v3_{k}_48.png")

# 比較シート(原寸+48px)
sheet = Image.new("RGB", (S * 3 + 80, S + 140), (18, 18, 24))
for i, (k, im) in enumerate(cands.items()):
    x = 20 + i * (S + 20)
    sheet.paste(im, (x, 20))
    small = im.resize((48, 48), Image.LANCZOS)
    sheet.paste(small, (x + S // 2 - 24, S + 60))
sheet.save(f"{OUT}/icon_v3_sheet.png")
print("done")
