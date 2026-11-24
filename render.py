#!/usr/bin/env python3
"""Render the entry image for make.fun news-image-20261124.

Draws a 1024x1024 newspaper front page summing up Tuesday 24 November
2026's world news, researched from reports published on 24 Nov 2026:

  Lead: Ukraine's sea drones sink the Russian corvette Merkury in Benghazi,
        Libya (attack Sun 22 Nov, confirmed by Zelenskyy Mon 23 Nov; cargo
        ship MV Angara also hit).
  Also: COP31 climate talks collapse in Antalya with no deal on fossil
        fuels; factory fire in Indonesia kills 24; Russian cargo ship
        Sparta II hit by drones in the Baltic; World Chess Championship
        opens in Geneva (Gukesh defends vs Sindarov); Alcaraz wins his
        first ATP Finals title in Turin; Iran vows to counter a US
        blockade threat in the Strait of Hormuz.

Run:  python3 render.py   -> writes entry.png beside this file.
Only Pillow + the DejaVu fonts shipped with the OS are used, locally.
The submitted entry program (main.py) only copies entry.png.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 242, 231)
PAPER = (252, 249, 240)
INK = (20, 20, 22)
RED = (178, 34, 34)
NAVY = (26, 42, 74)
TEAL = (18, 74, 88)
GOLD = (198, 138, 32)
GREY = (90, 90, 96)
LIGHT_LINE = (120, 110, 95)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.25)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.25)


# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# Top red rule + thin black rule
d.rectangle([0, 0, W, 10], fill=RED)
d.rectangle([0, 14, W, 16], fill=INK)

# ------------------------------------------------------------- masthead
_ms = 72
while d.textlength("THE WORLD IN ONE DAY", font=font(SERIF, _ms)) > 960 and _ms > 20:
    _ms -= 2
centred(d, W // 2, 26, "THE WORLD IN ONE DAY", font(SERIF, _ms), INK)
centred(d, W // 2, 106, "SIX STORIES  ·  ONE PLANET  ·  AS REPORTED AROUND THE WORLD",
        font(SANS_B, 17), GREY)

# Date bar
d.rectangle([28, 146, W - 28, 186], fill=INK)
centred(d, W // 2, 153, "TUESDAY  —  24 NOVEMBER 2026", font(SERIF, 26), (255, 255, 255))

# ---------------------------------------------------------- lead picture
# Flat dusk scene: the corvette Merkury burning at the Benghazi dock.
LX, LY, LW, LH = 28, 202, 560, 338
# sky gradient: deep orange horizon -> dark navy top
for i in range(LH):
    t = i / LH
    r = int(38 + (214 - 38) * (1 - t) ** 2)
    g = int(32 + (110 - 32) * (1 - t) ** 2)
    b = int(64 + (58 - 64) * (1 - t) ** 2)
    d.line([(LX, LY + i), (LX + LW, LY + i)], fill=(r, g, b))
# low sun
d.ellipse([LX + 470, LY + 210, LX + 540, LY + 280], fill=(232, 150, 60))
# sea
d.rectangle([LX, LY + 292, LX + LW, LY + LH], fill=(16, 58, 74))
for wx in range(0, LW, 46):
    d.arc([LX + wx, LY + 296, LX + wx + 40, LY + 312], 200, 340, fill=(90, 160, 175), width=3)
# pier
d.rectangle([LX, LY + 268, LX + LW, LY + 296], fill=(52, 44, 40))
for px in range(LX + 20, LX + LW, 64):
    d.rectangle([px, LY + 268, px + 10, LY + 296], fill=(40, 34, 30))
# listing corvette hull (tilted, half-submerged at the bow)
hull = [(LX + 120, LY + 252), (LX + 470, LY + 236), (LX + 505, LY + 258),
        (LX + 500, LY + 292), (LX + 140, LY + 296), (LX + 108, LY + 272)]
d.polygon(hull, fill=(138, 143, 152))
d.polygon([(LX + 120, LY + 252), (LX + 470, LY + 236), (LX + 505, LY + 258),
           (LX + 500, LY + 268), (LX + 130, LY + 272)], fill=(70, 74, 82))
# superstructure + mast, listing
d.polygon([(LX + 250, LY + 236), (LX + 330, LY + 232), (LX + 336, LY + 196),
           (LX + 268, LY + 200)], fill=(120, 124, 132))
d.line([(LX + 300, LY + 200), (LX + 292, LY + 158)], fill=(120, 124, 132), width=6)
d.polygon([(LX + 292, LY + 158), (LX + 312, LY + 164), (LX + 296, LY + 172)], fill=RED)
# flames licking from the deck
for fx, fh, fw in [(LX + 180, 64, 34), (LX + 240, 88, 40), (LX + 320, 76, 36),
                   (LX + 400, 60, 30), (LX + 452, 44, 26)]:
    d.polygon([(fx, LY + 244), (fx + fw // 2, LY + 244 - fh),
               (fx + fw, LY + 244)], fill=(232, 120, 30))
    d.polygon([(fx + 6, LY + 244), (fx + fw // 2, LY + 244 - fh + 26),
               (fx + fw - 6, LY + 244)], fill=(245, 196, 66))
# smoke column
for sx, sy, sr in [(LX + 300, LY + 140, 44), (LX + 330, LY + 100, 52),
                   (LX + 372, LY + 62, 58), (LX + 420, LY + 30, 54)]:
    d.ellipse([sx - sr, sy - sr // 2, sx + sr, sy + sr // 2], fill=(58, 56, 60))
# sea drone silhouette heading in
d.ellipse([LX + 60, LY + 316, LX + 108, LY + 328], fill=(12, 12, 14))
d.line([(LX + 108, LY + 322), (LX + 128, LY + 318)], fill=(12, 12, 14), width=3)
# caption strip on the picture
d.rectangle([LX, LY + LH - 30, LX + LW, LY + LH], fill=(0, 0, 0))
d.text((LX + 12, LY + LH - 25), "THE CORVETTE MERKURY BURNS AT BENGHAZI",
       font=font(SANS_B, 15), fill=(255, 255, 255))
d.rectangle([LX, LY, LX + LW, LY + LH], outline=INK, width=3)

# ----------------------------------------------------------- lead story
RX = 612
d.text((RX, 206), "THE WAR AT SEA", font=font(SANS_B, 20), fill=RED)
d.line([(RX, 232), (RX + 356, 232)], fill=RED, width=3)
y = 246
y = text_block(d, RX, y, wrap(d, "UKRAINE SINKS", font(SERIF, 32), 360), font(SERIF, 32), INK, 38)
y = text_block(d, RX, y, wrap(d, "RUSSIAN WARSHIP", font(SERIF, 32), 360), font(SERIF, 32), INK, 38)
y = text_block(d, RX, y, wrap(d, "OFF LIBYA", font(SERIF, 32), 360), font(SERIF, 32), INK, 38)
y += 6
y = text_block(d, RX, y,
               wrap(d, "Sea drones sink the corvette Merkury at Benghazi and hit the cargo ship Angara — the war reaches a new shore.",
                    font(SERIF_IT, 20), 360), font(SERIF_IT, 20), (52, 52, 56), 25)
y += 12
d.line([(RX, y), (RX + 356, y)], fill=LIGHT_LINE, width=2)
y += 10
y = text_block(d, RX, y, wrap(d, "ATTACK SUNDAY · CONFIRMED MONDAY",
               font(SANS_B, 15), 360), font(SANS_B, 15), RED, 20)

# ------------------------------------------------------------ also today
AY = 556
d.line([(28, AY), (W - 28, AY)], fill=INK, width=3)
d.text((28, AY + 10), "ALSO TODAY", font=font(SANS_B, 22), fill=INK)
d.text((W - 28 - d.textlength("24 NOVEMBER 2026", font(SANS_B, 18)), AY + 14),
       "24 NOVEMBER 2026", font=font(SANS_B, 18), fill=GREY)

# ------------------------------------------------------------- six panels
panels = [
    ("COP31", "CLIMATE TALKS COLLAPSE",
     "The Antalya summit ends with no deal on fossil fuels.",
     "globe"),
    ("INDONESIA", "FACTORY FIRE KILLS 24",
     "A blaze at a candy factory; rescuers search for missing workers.",
     "factory"),
    ("THE BALTIC", "SECOND SHIP HIT AT SEA",
     "Russian cargo ship Sparta II ablaze after a drone strike off Finland.",
     "ship"),
    ("CHESS", "GUKESH DEFENDS CROWN",
     "The World Championship opens in Geneva vs Sindarov.",
     "chess"),
    ("TENNIS", "ALCARAZ WINS ATP FINALS",
     "A first title in Turin, beating Zverev in the final.",
     "tennis"),
    ("THE GULF", "IRAN–US STANDOFF",
     "Tehran vows to counter a US blockade threat in the Strait of Hormuz.",
     "tanker"),
]

PX0, PY0, PW, PH, GX, GY = 28, 596, 312, 168, 20, 16


def draw_icon(dd, kind, cx, cy):
    """Small flat pictogram, centred on (cx, cy), ~64px across."""
    if kind == "globe":
        dd.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], outline=TEAL, width=5)
        dd.arc([cx - 30, cy - 30, cx + 30, cy + 30], 300, 60, fill=TEAL, width=4)
        dd.line([(cx - 30, cy), (cx + 30, cy)], fill=TEAL, width=4)
        dd.line([(cx, cy - 30), (cx, cy + 30)], fill=TEAL, width=4)
        dd.line([(cx - 22, cy - 18), (cx - 2, cy + 4), (cx + 12, cy - 12),
                 (cx + 24, cy + 8)], fill=RED, width=5)
    elif kind == "factory":
        dd.rectangle([cx - 30, cy - 6, cx + 30, cy + 28], fill=NAVY)
        dd.polygon([(cx - 30, cy - 6), (cx - 18, cy - 6), (cx - 18, cy - 28),
                    (cx - 8, cy - 28), (cx - 8, cy - 6)], fill=NAVY)
        dd.polygon([(cx - 2, cy - 26), (cx + 8, cy - 6), (cx + 18, cy - 26),
                    (cx + 26, cy - 6)], fill=(232, 120, 30))
        dd.polygon([(cx + 2, cy - 14), (cx + 9, cy - 2), (cx + 16, cy - 14)],
                   fill=(245, 196, 66))
        for wx in (-20, 0, 20):
            dd.rectangle([cx + wx - 5, cy + 6, cx + wx + 5, cy + 16], fill=CREAM)
    elif kind == "ship":
        dd.polygon([(cx - 30, cy + 4), (cx + 30, cy + 4), (cx + 22, cy + 26),
                    (cx - 22, cy + 26)], fill=NAVY)
        dd.rectangle([cx - 12, cy - 16, cx + 12, cy + 4], fill=NAVY)
        dd.line([(cx, cy - 16), (cx, cy - 30)], fill=NAVY, width=4)
        dd.polygon([(cx, cy - 30), (cx + 16, cy - 22), (cx, cy - 18)], fill=RED)
        dd.arc([cx - 34, cy + 28, cx - 6, cy + 40], 180, 360, fill=TEAL, width=3)
        dd.arc([cx + 6, cy + 28, cx + 34, cy + 40], 180, 360, fill=TEAL, width=3)
    elif kind == "chess":
        dd.ellipse([cx - 22, cy + 18, cx + 22, cy + 30], fill=INK)
        dd.rectangle([cx - 16, cy - 2, cx + 16, cy + 20], fill=INK)
        dd.ellipse([cx - 12, cy - 16, cx + 12, cy + 2], fill=INK)
        dd.line([(cx - 14, cy - 24), (cx + 14, cy - 24)], fill=INK, width=5)
        dd.line([(cx, cy - 30), (cx, cy - 18)], fill=INK, width=5)
        dd.ellipse([cx - 4, cy - 34, cx + 4, cy - 26], fill=INK)
    elif kind == "tennis":
        dd.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], outline=(120, 160, 40), width=6)
        dd.arc([cx - 28, cy - 28, cx + 28, cy + 28], 250, 110, fill=(120, 160, 40), width=5)
        dd.arc([cx - 28, cy - 28, cx + 28, cy + 28], 70, 290, fill=(120, 160, 40), width=5)
    elif kind == "tanker":
        dd.rectangle([cx - 32, cy - 2, cx + 32, cy + 20], fill=NAVY)
        dd.rectangle([cx + 12, cy - 16, cx + 30, cy - 2], fill=NAVY)
        dd.polygon([(cx - 32, cy - 2), (cx - 22, cy - 2), (cx - 22, cy - 14),
                    (cx - 14, cy - 14), (cx - 14, cy - 2)], fill=NAVY)
        dd.arc([cx - 34, cy + 22, cx - 6, cy + 34], 180, 360, fill=TEAL, width=3)
        dd.arc([cx + 6, cy + 22, cx + 34, cy + 34], 180, 360, fill=TEAL, width=3)


for i, (kicker, head, body, icon) in enumerate(panels):
    col, row = i % 3, i // 3
    x = PX0 + col * (PW + GX)
    y = PY0 + row * (PH + GY)
    d.rectangle([x, y, x + PW, y + PH], fill=PAPER, outline=LIGHT_LINE, width=2)
    d.rectangle([x, y, x + PW, y + 5], fill=RED)
    draw_icon(d, icon, x + 48, y + 52)
    d.text((x + 92, y + 14), kicker, font=font(SANS_B, 15), fill=RED)
    tx = x + 92
    ty = y + 36
    for ln in wrap(d, head, font(SANS_B, 21), PW - 108):
        d.text((tx, ty), ln, font=font(SANS_B, 21), fill=INK)
        ty += 25
    ty += 2
    text_block(d, tx, ty, wrap(d, body, font(SANS, 15), PW - 108),
               font(SANS, 15), (52, 52, 56), 19)

# ---------------------------------------------------------------- footer
FY = 986
d.line([(28, FY - 14), (W - 28, FY - 14)], fill=INK, width=2)
centred(d, W // 2, FY - 8,
        "24 NOVEMBER 2026  ·  THE DAY'S NEWS, DRAWN FROM REPORTS AROUND THE WORLD",
        font(SANS_B, 15), GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
