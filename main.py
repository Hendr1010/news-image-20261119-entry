#!/usr/bin/env python3
"""The World in One Day - Thursday 19 November 2026.

Renders a one-page newspaper front page (1024x1024 PNG) summing up the
world news of 19 November 2026. Pure Pillow, no network, fully deterministic:
the same bytes on every run.

Stories (all reported on 19 Nov 2026):
  - GTA VI rolls out worldwide; ~1 in 5 US workers plan time off
  - Trump, Xi and Putin meet in Shenzhen - first three-way summit
  - Iran and the US trade strikes across the Gulf; tanker hit off Hormuz
  - NASA's Voyager 1 believed to have crossed one light-day from Earth
  - EU proposes a 45 billion euro loan for Ukraine
  - Australia, Canada, Italy and the UK call for aid access to flooded Gaza
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
INNER = W - 2 * MARGIN  # 968

PAPER = (247, 241, 227)
INK = (22, 21, 19)
RED = (200, 16, 46)
GRAY = (96, 91, 82)
FAINT = (210, 203, 188)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def serif(size, bold=True):
    name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def sans(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, box, stops):
    """Vertical gradient across box from a list of (pos, color) stops."""
    x0, y0, x1, y1 = box
    n = y1 - y0
    for y in range(n):
        t = y / max(1, n - 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                f = 0.0 if p1 == p0 else (t - p0) / (p1 - p0)
                col = lerp(c0, c1, f)
                break
        else:
            col = stops[-1][1]
        draw.line([(x0, y0 + y), (x1, y0 + y)], fill=col)


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        ang = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def draw_masthead(d):
    d.rectangle([MARGIN, 28, W - MARGIN, 32], fill=INK)
    title = "THE WORLD IN ONE DAY"
    f = serif(60)
    tw = d.textlength(title, font=f)
    d.text(((W - tw) / 2, 40), title, font=f, fill=INK)
    d.line([(MARGIN, 118), (W - MARGIN, 118)], fill=INK, width=1)
    left = "THURSDAY, 19 NOVEMBER 2026"
    right = "ONE DAY  ·  ONE PAGE  ·  THE WHOLE WORLD"
    fl = sans(19, bold=True)
    fr = sans(16)
    d.text((MARGIN, 126), left, font=fl, fill=INK)
    rw = d.textlength(right, font=fr)
    d.text((W - MARGIN - rw, 127), right, font=fr, fill=GRAY)
    d.rectangle([MARGIN, 152, W - MARGIN, 155], fill=INK)
    d.line([(MARGIN, 158), (W - MARGIN, 158)], fill=INK, width=1)


def draw_hero_visual(d, x0, y0, x1, y1):
    stops = [
        (0.00, (26, 11, 46)),
        (0.35, (91, 27, 110)),
        (0.62, (194, 39, 107)),
        (0.85, (255, 107, 74)),
        (1.00, (255, 179, 71)),
    ]
    vgrad(d, (x0, y0, x1, y1), stops)
    # sun with glow
    cx, cy = x0 + int((x1 - x0) * 0.68), y0 + int((y1 - y0) * 0.48)
    for r, col in ((78, (255, 140, 66)), (64, (255, 179, 71)), (51, (255, 224, 102))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    # skyline silhouettes (fixed heights, scaled to the visual height)
    base = y1 - 34
    max_h = (y1 - y0) - 42
    heights = [118, 74, 150, 92, 168, 108, 82, 142, 96, 124, 70, 158, 88, 132]
    bw = (x1 - x0) // len(heights)
    rng = random.Random(20261119)
    for i, hgt0 in enumerate(heights):
        hgt = int(hgt0 * max_h / 168)
        bx = x0 + i * bw
        d.rectangle([bx + 3, base - hgt, bx + bw - 3, y1], fill=(20, 8, 43))
        # lit windows, fixed pseudo-random pattern
        for wy in range(base - hgt + 10, base - 8, 16):
            for wx in range(bx + 8, bx + bw - 10, 14):
                if rng.random() < 0.30:
                    d.rectangle([wx, wy, wx + 5, wy + 7],
                                fill=(255, 209, 102) if rng.random() < 0.7
                                else (255, 94, 138))
    # water strip with light streaks
    d.rectangle([x0, y1 - 34, x1, y1], fill=(16, 7, 36))
    for i, (sx, sw, scol) in enumerate([
            (0.06, 0.20, (255, 107, 74)), (0.34, 0.12, (255, 224, 102)),
            (0.55, 0.26, (255, 140, 66)), (0.84, 0.10, (255, 209, 102))]):
        sx0 = x0 + int((x1 - x0) * sx)
        d.rectangle([sx0, y1 - 26 + (i % 3) * 7, sx0 + int((x1 - x0) * sw),
                     y1 - 22 + (i % 3) * 7], fill=scol)


def draw_hero(d):
    x0, x1 = MARGIN, W - MARGIN
    draw_hero_visual(d, x0, 170, x1, 352)
    d.text((x0, 362), "CULTURE  ·  VICE CITY", font=sans(18, bold=True), fill=RED)
    d.text((x0, 382), "VICE CITY OPENS", font=serif(62), fill=INK)
    deck = ("Grand Theft Auto VI rolls out worldwide — nearly 1 in 5 US workers "
            "plan time off. Consoles run at 30 fps; no 60 fps mode at launch.")
    lines = wrap(d, deck, sans(21), INNER)
    y = 452
    for line in lines:
        d.text((x0, y), line, font=sans(21), fill=INK)
        y += 27


def draw_flags_shenzhen(d, x0, y0, x1, y1):
    """Three simplified flags: US, China, Russia."""
    w = (x1 - x0) // 3
    # US flag
    ux, uy = x0, y0
    for i in range(7):
        col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([ux, uy + i * (y1 - y0) // 7, ux + w - 4,
                     uy + (i + 1) * (y1 - y0) // 7], fill=col)
    d.rectangle([ux, uy, ux + int(w * 0.42), uy + int((y1 - y0) * 0.55)],
                fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            d.ellipse([ux + 6 + c * 13, uy + 5 + r * 10,
                       ux + 10 + c * 13, uy + 9 + r * 10], fill=WHITE)
    # China flag
    cx = x0 + w
    d.rectangle([cx, y0, cx + w - 4, y1], fill=(222, 41, 16))
    d.polygon(star_points(cx + 22, y0 + 22, 13, 5), fill=(255, 222, 0))
    for sx, sy in ((cx + 48, y0 + 10), (cx + 58, y0 + 22),
                   (cx + 54, y0 + 38), (cx + 40, y0 + 44)):
        d.polygon(star_points(sx, sy, 5, 2), fill=(255, 222, 0))
    # Russia flag
    rx = x0 + 2 * w
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([rx, y0 + i * (y1 - y0) // 3, x1,
                     y0 + (i + 1) * (y1 - y0) // 3], fill=col)


def draw_gulf(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(11, 29, 51))
    rng = random.Random(77)
    for _ in range(26):
        sx = x0 + rng.randint(4, (x1 - x0) - 4)
        sy = y0 + rng.randint(3, int((y1 - y0) * 0.45))
        d.point((sx, sy), fill=(200, 214, 235))
    # sea
    d.rectangle([x0, y0 + int((y1 - y0) * 0.62), x1, y1], fill=(16, 48, 84))
    # tanker silhouette
    hx, hy = x0 + 22, y0 + int((y1 - y0) * 0.58)
    d.polygon([(hx, hy + 24), (hx + 168, hy + 24), (hx + 186, hy + 8),
               (hx + 196, hy + 8), (hx + 196, hy + 24)], fill=(8, 8, 10))
    d.rectangle([hx + 108, hy - 8, hx + 146, hy + 8], fill=(220, 224, 230))
    d.rectangle([hx + 118, hy - 20, hx + 128, hy - 8], fill=(220, 224, 230))
    # flame + smoke over the bow
    fx = hx + 214
    d.polygon([(fx, hy - 2), (fx + 12, hy - 30), (fx + 22, hy - 8),
               (fx + 32, hy - 34), (fx + 40, hy - 2)], fill=(255, 122, 26))
    d.polygon([(fx + 10, hy - 2), (fx + 18, hy - 18), (fx + 28, hy - 2)],
              fill=(255, 209, 102))
    for i, (sx, sy, sr) in enumerate([(fx + 16, hy - 44, 7), (fx + 30, hy - 56, 9),
                                      (fx + 44, hy - 48, 6)]):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 124, 130))


def draw_voyager(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(4, 6, 18))
    rng = random.Random(2026)
    for _ in range(42):
        sx = x0 + rng.randint(4, (x1 - x0) - 4)
        sy = y0 + rng.randint(3, (y1 - y0) - 3)
        r = rng.choice([1, 1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(235, 238, 250))
    # dotted trajectory
    for i in range(9):
        tx = x0 + 12 + i * 16
        ty = y0 + int((y1 - y0) * 0.72) - i * 5
        d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=(255, 209, 102))
    # probe: bus + dish + boom
    px, py = x0 + 168, y0 + 30
    d.rectangle([px, py, px + 34, py + 20], fill=(200, 204, 212))
    d.line([(px + 34, py + 10), (px + 62, py - 6)], fill=(200, 204, 212), width=3)
    d.polygon([(px + 62, py - 14), (px + 84, py - 2), (px + 62, py + 2)],
              fill=(235, 238, 250))
    d.line([(px + 8, py + 20), (px - 6, py + 44)], fill=(160, 164, 172), width=3)
    d.ellipse([px - 12, py + 40, px + 0, py + 52], fill=(255, 209, 102))


def draw_card(d, x, y, w, h, kicker, headline, deck, visual):
    visual(d, x, y, x + w, y + 72)
    d.text((x, y + 78), kicker, font=sans(15, bold=True), fill=RED)
    hl = wrap(d, headline, serif(26), w)
    hy = y + 98
    for line in hl[:2]:
        d.text((x, hy), line, font=serif(26), fill=INK)
        hy += 29
    dl = wrap(d, deck, sans(15), w)
    dy = y + 98 + 29 * len(hl[:2]) + 4
    for line in dl[:2]:
        d.text((x, dy), line, font=sans(15), fill=(52, 50, 46))
        dy += 19


def draw_eu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    cx, cy = x + w // 2, y + h // 2
    for i in range(12):
        ang = math.radians(-90 + i * 30)
        sx = cx + int(0.30 * h * math.cos(ang))
        sy = cy + int(0.30 * h * math.sin(ang))
        d.polygon(star_points(sx, sy, 7, 3), fill=(255, 204, 0))
    d.text((cx - 13, cy - 13), "€", font=sans(26, bold=True), fill=WHITE)


def draw_aid(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    # four mini flags: AU, CA, IT, UK
    fw, fh = 34, 22
    gap = (w - 4 * fw) // 5
    # Australia
    ax = x + gap
    d.rectangle([ax, y + 14, ax + fw, y + 14 + fh], fill=(0, 40, 104))
    d.polygon(star_points(ax + 9, y + 25, 6, 2), fill=WHITE)
    d.polygon(star_points(ax + 25, y + 20, 4, 2), fill=WHITE)
    d.polygon(star_points(ax + 25, y + 32, 4, 2), fill=WHITE)
    # Canada
    bx = ax + fw + gap
    d.rectangle([bx, y + 14, bx + 10, y + 14 + fh], fill=(255, 0, 0))
    d.rectangle([bx + 24, y + 14, bx + fw, y + 14 + fh], fill=(255, 0, 0))
    d.polygon(star_points(bx + 17, y + 25, 6, 2), fill=(255, 0, 0))
    # Italy
    cx = bx + fw + gap
    for i, col in enumerate([(0, 146, 70), (255, 255, 255), (206, 43, 55)]):
        d.rectangle([cx + i * fw // 3, y + 14, cx + (i + 1) * fw // 3,
                     y + 14 + fh], fill=col)
    # United Kingdom
    dx = cx + fw + gap
    d.rectangle([dx, y + 14, dx + fw, y + 14 + fh], fill=(1, 33, 105))
    d.line([(dx, y + 14), (dx + fw, y + 14 + fh)], fill=WHITE, width=4)
    d.line([(dx + fw, y + 14), (dx, y + 14 + fh)], fill=WHITE, width=4)
    d.line([(dx + fw // 2, y + 14), (dx + fw // 2, y + 14 + fh)],
           fill=(200, 16, 46), width=6)
    d.line([(dx, y + 14 + fh // 2), (dx + fw, y + 14 + fh // 2)],
           fill=(200, 16, 46), width=6)
    d.text((x + 8, y + 48), "AID ACCESS", font=sans(15, bold=True), fill=INK)


def draw_low_row(d):
    y = 748
    h = 132
    w = (INNER - 12) // 2
    # card 4: EU loan, visual left
    d.rectangle([MARGIN, y, MARGIN + w, y + h], fill=WHITE)
    d.rectangle([MARGIN, y, MARGIN + w, y + 3], fill=INK)
    draw_eu(d, MARGIN + 12, y + 16, 108, 108)
    tx = MARGIN + 134
    d.text((tx, y + 14), "EUROPE  ·  UKRAINE", font=sans(15, bold=True), fill=RED)
    d.text((tx, y + 34), "€45BN FOR UKRAINE", font=serif(24), fill=INK)
    deck = ("The EU proposes a €45 billion loan — to be repaid after "
            "Russia pays reparations.")
    dy = y + 70
    for line in wrap(d, deck, sans(16), w - 146):
        d.text((tx, dy), line, font=sans(16), fill=(52, 50, 46))
        dy += 21
    # card 5: Gaza aid, visual left
    x2 = MARGIN + w + 12
    d.rectangle([x2, y, x2 + w, y + h], fill=WHITE)
    d.rectangle([x2, y, x2 + w, y + 3], fill=INK)
    draw_aid(d, x2 + 12, y + 16, 108, 108)
    tx = x2 + 134
    d.text((tx, y + 14), "MIDDLE EAST  ·  GAZA", font=sans(15, bold=True), fill=RED)
    d.text((tx, y + 34), "AID FOR FLOODED GAZA", font=serif(24), fill=INK)
    deck = ("Australia, Canada, Italy and the UK jointly call on Israel to "
            "open humanitarian access.")
    dy = y + 70
    for line in wrap(d, deck, sans(16), w - 146):
        d.text((tx, dy), line, font=sans(16), fill=(52, 50, 46))
        dy += 21


def draw_ticker(d):
    y0, y1 = 892, 958
    d.rectangle([MARGIN, y0, W - MARGIN, y1], fill=INK)
    label = "ALSO TODAY  "
    f_lab = sans(17, bold=True)
    d.text((MARGIN + 12, y0 + 8), label, font=f_lab, fill=(255, 120, 120))
    lw = d.textlength(label, font=f_lab)
    items = ("France: 4th weekend of cost-of-living protests  ·  Cyclone Akvan "
             "nears India  ·  Cambridge word of 2026: “Human”  ·  Israel: Eisenkot "
             "tapped to form government  ·  Canada rethinks China ties")
    lines = wrap(d, items, sans(17), INNER - 24 - lw)
    ly = y0 + 8
    for line in lines[:2]:
        d.text((MARGIN + 12 + lw, ly), line, font=sans(17), fill=WHITE)
        ly += 24
    d.text((MARGIN, 966), "Compiled from the day's wire reports  ·  19 November 2026",
           font=sans(13), fill=GRAY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 10, H - 10], outline=INK, width=3)
    draw_masthead(d)
    draw_hero(d)
    d.line([(MARGIN, 516), (W - MARGIN, 516)], fill=INK, width=1)
    cw = (INNER - 24) // 3
    draw_card(d, MARGIN, 528, cw, 178, "DIPLOMACY  ·  SHENZHEN",
              "THREE POWERS, ONE TABLE",
              "Trump, Xi and Putin meet in Shenzhen — arms, Ukraine and "
              "Iran on the agenda.", draw_flags_shenzhen)
    draw_card(d, MARGIN + cw + 12, 528, cw, 178, "MIDDLE EAST  ·  THE GULF",
              "GULF ON EDGE",
              "Iran and the US trade strikes across the Gulf; a tanker is "
              "hit off Hormuz.", draw_gulf)
    draw_card(d, MARGIN + 2 * (cw + 12), 528, INNER - 2 * cw - 24, 178,
              "SPACE  ·  DEEP SPACE", "VOYAGER 1: ONE LIGHT-DAY OUT",
              "NASA's probe believed to have crossed a light-day — "
              "the farthest human object.", draw_voyager)
    d.line([(MARGIN, 736), (W - MARGIN, 736)], fill=INK, width=1)
    draw_low_row(d)
    draw_ticker(d)
    out = os.environ.get("OUTPUT_PATH", "/output/entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
