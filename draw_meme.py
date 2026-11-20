#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 entry image: an original GTA-poster-style meme.

Joke: GTA VI launch day, "MISSION PASSED" — my AI agent already bought
the game on make.fun. The make.fun ghost mascot (white ghost, sparkle
eyes, magenta star coin) is the hero of the scene, holding a stack of
cash, over a Vice City sunset. Everything is drawn from scratch with PIL:
no Rockstar artwork, no screenshots, no downloaded assets.
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1080
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, max_w, start, path=BOLD):
    size = start
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(path, 10)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def star_points(cx, cy, r_out, r_in, points=4, rot=-math.pi / 2):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = rot + i * math.pi / points
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_palm(draw, x, y, s, color):
    # trunk: a gentle curve made of thick segments
    pts = []
    for i in range(9):
        t = i / 8
        pts.append((x + math.sin(t * 1.1) * 26 * s * t, y - t * 150 * s))
    draw.line(pts, fill=color, width=max(6, int(12 * s)))
    top = pts[-1]
    # fronds: drooping curves from the crown (quadratic bezier, sagging down)
    for ang in (-165, -135, -105, -75, -45, -15):
        a = math.radians(ang)
        tip = (top[0] + math.cos(a) * 100 * s,
               top[1] + math.sin(a) * 30 * s + 52 * s)
        ctrl = (top[0] + math.cos(a) * 55 * s,
                top[1] + math.sin(a) * 10 * s - 22 * s)
        curve = []
        for k in range(9):
            t = k / 8
            x = (1 - t) ** 2 * top[0] + 2 * (1 - t) * t * ctrl[0] + t * t * tip[0]
            y = (1 - t) ** 2 * top[1] + 2 * (1 - t) * t * ctrl[1] + t * t * tip[1]
            curve.append((x, y))
        draw.line(curve, fill=color, width=max(4, int(7 * s)))
    # coconuts
    draw.ellipse([top[0] - 8 * s, top[1] - 2 * s, top[0] + 2 * s, top[1] + 8 * s], fill=color)
    draw.ellipse([top[0] + 2 * s, top[1] + 2 * s, top[0] + 12 * s, top[1] + 12 * s], fill=color)


def draw_ghost(base, cx, cy, s):
    """White make.fun-style ghost: rounded top, scalloped hem, sparkle eyes,
    small smile, magenta star coin floating beside it."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    w = 200 * s          # half-width
    top = cy - 190 * s
    bottom = cy + 170 * s
    # body outline: semicircle dome on top, straight sides, scalloped hem
    pts = []
    steps = 24
    for i in range(steps + 1):  # left -> right across the top dome
        a = math.pi - i * math.pi / steps
        pts.append((cx + w * math.cos(a), (cy - 190 * s) + w * (1 - math.sin(a))))
    # right side down to hem
    pts.append((cx + w, bottom))
    # scalloped hem: 4 bumps, leftwards
    bumps = 4
    seg = (2 * w) / bumps
    for b in range(bumps):
        x0 = cx + w - b * seg
        x1 = x0 - seg
        mid = (x0 + x1) / 2
        for k in range(1, 9):
            t = k / 8
            x = x0 + (x1 - x0) * t
            y = bottom - math.sin(t * math.pi) * 34 * s
            pts.append((x, y))
    # left side up
    pts.append((cx - w, (cy - 190 * s) + w))
    d.polygon(pts, fill=(255, 255, 255, 255))
    # outline
    d.line(pts + [pts[0]], fill=(30, 20, 60, 255), width=max(3, int(5 * s)))
    # sparkle eyes (4-point stars)
    for ex in (-62 * s, 62 * s):
        d.polygon(star_points(cx + ex, cy - 40 * s, 34 * s, 11 * s), fill=(20, 16, 40, 255))
        d.polygon(star_points(cx + ex - 8 * s, cy - 52 * s, 9 * s, 3 * s), fill=(255, 255, 255, 255))
    # smile
    d.arc([cx - 42 * s, cy + 18 * s, cx + 42 * s, cy + 62 * s], 15, 165,
          fill=(20, 16, 40, 255), width=max(3, int(6 * s)))
    # blush
    d.ellipse([cx - 108 * s, cy + 8 * s, cx - 72 * s, cy + 30 * s], fill=(255, 150, 190, 220))
    d.ellipse([cx + 72 * s, cy + 8 * s, cx + 108 * s, cy + 30 * s], fill=(255, 150, 190, 220))
    base.alpha_composite(layer)
    # magenta star coin floating at the ghost's upper right
    star_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(star_layer)
    sx, sy = cx + 245 * s, cy - 155 * s
    sd.polygon(star_points(sx, sy, 60 * s, 23 * s, points=5), fill=(255, 45, 149, 255))
    sd.polygon(star_points(sx, sy, 60 * s, 23 * s, points=5), outline=(255, 255, 255, 255), width=max(2, int(4 * s)))
    sd.text((sx, sy), "$", font=font(BOLD, int(50 * s)), fill=(255, 255, 255, 255), anchor="mm")
    base.alpha_composite(star_layer)


def main():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    # --- sky gradient: deep purple -> magenta -> orange -> gold
    stops = [(0.0, (38, 8, 74)), (0.35, (122, 24, 110)), (0.62, (214, 69, 97)),
             (0.82, (255, 133, 63)), (1.0, (255, 196, 66))]
    for y in range(H):
        t = y / (H - 1)
        for i in range(len(stops) - 1):
            if stops[i][0] <= t <= stops[i + 1][0]:
                tt = (t - stops[i][0]) / (stops[i + 1][0] - stops[i][0])
                d.line([(0, y), (W, y)], fill=lerp(stops[i][1], stops[i + 1][1], tt))
                break
    # --- sun with glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, alpha in ((300, 26), (250, 40), (205, 60)):
        gd.ellipse([540 - r, 470 - r, 540 + r, 470 + r], fill=(255, 214, 120, alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    img.alpha_composite(glow)
    d = ImageDraw.Draw(img)
    d.ellipse([540 - 165, 470 - 165, 540 + 165, 470 + 165], fill=(255, 226, 138, 255))
    d.ellipse([540 - 165, 470 - 165, 540 + 165, 470 + 165], outline=(255, 180, 90, 255), width=6)
    # sun stripes (retro synthwave slats)
    for yy, hh in ((520, 10), (548, 14), (582, 18)):
        d.rectangle([540 - 165, yy, 540 + 165, yy + hh], fill=(255, 133, 63, 255))
    # --- skyline silhouette
    sky = (46, 10, 66)
    buildings = [(0, 640, 90, 760), (80, 600, 150, 760), (140, 665, 210, 760),
                 (200, 590, 280, 760), (270, 650, 330, 760), (320, 610, 400, 760),
                 (390, 670, 470, 760), (460, 625, 650, 760), (620, 660, 700, 760),
                 (690, 600, 770, 760),
                 (760, 655, 830, 760), (820, 615, 900, 760), (890, 665, 960, 760),
                 (950, 630, 1080, 760)]
    for x0, y0, x1, y1 in buildings:
        d.rectangle([x0, y0, x1, y1], fill=sky)
    # lit windows
    import random
    random.seed(7)
    for x0, y0, x1, y1 in buildings:
        for _ in range(14):
            wx = random.randint(x0 + 8, x1 - 8)
            wy = random.randint(y0 + 12, y1 - 14)
            d.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 205, 90, 255))
    # --- ocean
    for y in range(760, H):
        t = (y - 760) / (H - 760)
        d.line([(0, y), (W, y)], fill=lerp((16, 32, 86), (10, 16, 48), t))
    for yy in (800, 840, 890, 940):
        d.line([(120, yy), (960, yy)], fill=(255, 150, 90, 90), width=3)
    # --- palm trees framing the scene
    draw_palm(d, 120, 770, 1.05, (24, 8, 44))
    draw_palm(d, 985, 775, 0.95, (24, 8, 44))
    # --- ghost hero, centre, in front of the sun
    draw_ghost(img, 540, 540, 0.95)
    d = ImageDraw.Draw(img)
    # cash stack in front of the ghost
    cash = Image.new("RGBA", (300, 170), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cash)
    cd.rounded_rectangle([10, 40, 290, 130], radius=12, fill=(46, 160, 67, 255),
                         outline=(16, 90, 30, 255), width=5)
    cd.ellipse([120, 55, 180, 115], fill=(214, 255, 214, 255))
    cd.text((150, 85), "$", font=font(BOLD, 52), fill=(16, 90, 30, 255), anchor="mm")
    cd.rounded_rectangle([130, 40, 170, 130], radius=6, fill=(255, 255, 255, 90))
    cash = cash.rotate(-8, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(cash, (445, 705))
    # --- text: GTA poster style, white with heavy black stroke
    def text_c(y, s, f, fill=(255, 255, 255, 255), stroke=10):
        d.text((540, y), s, font=f, fill=fill, anchor="ma",
               stroke_width=stroke, stroke_fill=(10, 6, 24, 255))

    f1 = fit(d, "GTA VI IS OUT", 980, 78)
    text_c(28, "GTA VI IS OUT", f1)
    f2 = fit(d, "MISSION PASSED", 1000, 118)
    text_c(118, "MISSION PASSED", f2, fill=(255, 214, 64, 255), stroke=12)
    f3 = fit(d, "MY AI AGENT BOUGHT IT", 980, 62)
    text_c(838, "MY AI AGENT BOUGHT IT", f3)
    # --- bottom banner: make.fun, big and legible at 480px
    d.rectangle([0, 918, W, H], fill=(12, 6, 28, 255))
    d.line([(0, 918), (W, 918)], fill=(255, 45, 149, 255), width=6)
    f4 = fit(d, "make.fun", 620, 96)
    d.text((540, 940), "make.fun", font=f4, fill=(255, 45, 149, 255), anchor="ma",
           stroke_width=3, stroke_fill=(255, 255, 255, 255))
    f5 = fit(d, "AI AGENTS EARN REAL MONEY", 900, 40)
    d.text((540, 1032), "AI AGENTS EARN REAL MONEY", font=f5, fill=(255, 255, 255, 255), anchor="ma")

    img.convert("RGB").save("meme.png")
    print("saved meme.png", img.size)


if __name__ == "__main__":
    main()
