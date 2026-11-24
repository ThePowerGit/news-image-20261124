#!/usr/bin/env python3
"""Draw one image summing up Tuesday 24 November 2026's world news.

Six stories across regions and fields, drawn as flat vector shapes at 4x and
downsampled, so every edge lands clean at 1024px and stays legible at 300px.
"""

from PIL import Image, ImageDraw, ImageFont

S = 4                       # supersample factor
W = H = 1024
C = W * S

INK = (18, 22, 30)
PAPER = (247, 244, 238)
CARD = (255, 253, 249)
EDGE = (222, 217, 208)
MUTED = (122, 118, 110)

RED = (176, 42, 44)
BLUE = (26, 76, 138)
TEAL = (16, 100, 98)
AMBER = (168, 100, 14)
PLUM = (94, 42, 110)
GREEN = (36, 100, 56)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

img = Image.new("RGB", (C, C), PAPER)
d = ImageDraw.Draw(img)


def sc(*v):
    return tuple(int(round(x * S)) for x in v)


def text(xy, s, font, fill=INK, anchor="la"):
    d.text((xy[0] * S, xy[1] * S), s, font=font, fill=fill, anchor=anchor)


def font(path, px):
    return ImageFont.truetype(path, int(round(px * S)))


def wrap(s, font, maxw):
    """Greedy wrap; maxw is in design units."""
    out, cur = [], ""
    for wd in s.split():
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=font) <= maxw * S or not cur:
            cur = trial
        else:
            out.append(cur)
            cur = wd
    if cur:
        out.append(cur)
    return out


# ================================================================== masthead
text((60, 50), "THE WORLD IN ONE DAY", font(BOLD, 25), MUTED)
text((964, 50), "6 STORIES  \u00b7  4 REGIONS", font(BOLD, 22), MUTED, anchor="ra")

text((60, 84), "TUESDAY", font(BOLD, 38), RED)
text((60, 126), "24 NOVEMBER 2026", font(BOLD, 70), INK)

d.line(sc(60, 226, 964, 226), fill=INK, width=int(3 * S))
d.line(sc(60, 234, 964, 234), fill=INK, width=int(1 * S))

# ================================================================== cards
CARD_TOP = 264
CARD_H = 212
GAP = 18
LEFT = 60
RIGHT = 964
COLW = (RIGHT - LEFT - GAP) // 2

cards = [
    (0, 0, BLUE, "TECHNOLOGY", "Nvidia's Huang back as CEO",
     "Shares jump 30%; Asian markets rally", "chip"),
    (1, 0, RED, "MIDDLE EAST", "Gaza strike kills three",
     "Drone hits a police post in Khan Younis", "rubble"),
    (0, 1, AMBER, "EUROPE", "Ukraine, Russia clash at UN",
     "Black Sea attacks; 850,000 lose power", "bolt"),
    (1, 1, TEAL, "ASIA", "China's submarines pressure Japan",
     "ASEAN+3 finance talks open in Kyoto", "sub"),
    (0, 2, GREEN, "AFRICA", "Angola and Ghana cut rates",
     "To 14% and 11%; South Africa holds", "chart"),
    (1, 2, PLUM, "HUMANITARIAN", "WFP: 7.3 million face food cuts",
     "$727m more in shipping costs by 2027", "aid"),
]


def tint(col, k=0.88):
    return tuple(int(c + (255 - c) * k) for c in col)


def ic_chip(dr, x, y, w, h, col):
    r = lambda *v: sc(*v)
    dr.rounded_rectangle(r(x + w * .16, y + h * .16, x + w * .84, y + h * .84),
                         radius=int(w * .08 * S), outline=col, width=int(w * .055 * S))
    dr.rounded_rectangle(r(x + w * .36, y + h * .36, x + w * .64, y + h * .64),
                         radius=int(w * .04 * S), fill=col)
    for i in range(3):
        o = .28 + i * .22
        dr.line(r(x + w * o, y + h * .04, x + w * o, y + h * .16), fill=col, width=int(w * .05 * S))
        dr.line(r(x + w * o, y + h * .84, x + w * o, y + h * .96), fill=col, width=int(w * .05 * S))
        dr.line(r(x + w * .04, y + h * o, x + w * .16, y + h * o), fill=col, width=int(w * .05 * S))
        dr.line(r(x + w * .84, y + h * o, x + w * .96, y + h * o), fill=col, width=int(w * .05 * S))


def ic_rubble(dr, x, y, w, h, col):
    r = lambda *v: sc(*v)
    base = y + h * .90
    specs = [(.06, .40), (.28, .58), (.50, .30), (.72, .50)]
    for xo, hh in specs:
        bw = w * .19
        bh = h * hh
        dr.rectangle(r(x + w * xo, base - bh, x + w * xo + bw, base), fill=col)
        for row in range(2):
            for cix in range(2):
                wx = x + w * xo + bw * (.22 + cix * .34)
                wy = base - bh + bh * (.18 + row * .30)
                dr.rectangle(r(wx, wy, wx + bw * .24, wy + bh * .14), fill=PAPER)
    dr.polygon([r(x + w * .28, base - h * .58), r(x + w * .35, base - h * .70),
                r(x + w * .42, base - h * .60), r(x + w * .47, base - h * .58)], fill=col)
    dr.line(r(x + w * .02, base, x + w * .98, base), fill=col, width=int(w * .055 * S))
    dx, dy = x + w * .62, y + h * .14
    dr.line(r(dx - w * .11, dy, dx + w * .11, dy), fill=col, width=int(w * .035 * S))
    dr.ellipse(r(dx - w * .04, dy - h * .05, dx + w * .04, dy + h * .05), fill=col)
    for sgn in (-1, 1):
        dr.ellipse(r(dx + sgn * w * .11 - w * .045, dy - h * .05,
                     dx + sgn * w * .11 + w * .045, dy + h * .05),
                   outline=col, width=int(w * .03 * S))


def ic_bolt(dr, x, y, w, h, col):
    r = lambda *v: sc(*v)
    base = y + h * .92
    for xo, hh in [(.08, .24), (.28, .36), (.50, .20), (.70, .30)]:
        dr.rectangle(r(x + w * xo, base - h * hh, x + w * xo + w * .15, base), fill=col)
    dr.line(r(x + w * .02, base, x + w * .98, base), fill=col, width=int(w * .055 * S))
    dr.polygon([r(x + w * .56, y + h * .04), r(x + w * .36, y + h * .46),
                r(x + w * .50, y + h * .46), r(x + w * .40, y + h * .78),
                r(x + w * .70, y + h * .34), r(x + w * .55, y + h * .34)], fill=col)


def ic_sub(dr, x, y, w, h, col):
    r = lambda *v: sc(*v)
    cy = y + h * .62
    dr.ellipse(r(x + w * .04, cy - h * .15, x + w * .96, cy + h * .15), fill=col)
    dr.rounded_rectangle(r(x + w * .32, cy - h * .29, x + w * .54, cy - h * .11),
                         radius=int(w * .03 * S), fill=col)
    dr.line(r(x + w * .43, cy - h * .29, x + w * .43, cy - h * .44), fill=col, width=int(w * .035 * S))
    dr.line(r(x + w * .43, cy - h * .44, x + w * .52, cy - h * .44), fill=col, width=int(w * .035 * S))
    for i in range(3):
        wx = x + w * (.08 + i * .13)
        dr.arc(r(wx, cy - h * .04, wx + w * .09, cy + h * .09), 200, 340,
               fill=PAPER, width=int(w * .03 * S))


def ic_chart(dr, x, y, w, h, col):
    r = lambda *v: sc(*v)
    base = y + h * .90
    dr.line(r(x + w * .08, base, x + w * .94, base), fill=col, width=int(w * .045 * S))
    dr.line(r(x + w * .08, y + h * .08, x + w * .08, base), fill=col, width=int(w * .045 * S))
    pts = [(.14, .20), (.32, .32), (.50, .28), (.68, .54), (.86, .72)]
    xy = [r(x + w * p, y + h * q) for p, q in pts]
    dr.line(xy, fill=col, width=int(w * .055 * S), joint="curve")
    ax, ay = x + w * .86, y + h * .72
    dr.polygon([r(ax, ay + h * .14), r(ax - w * .08, ay + h * .01),
                r(ax + w * .08, ay + h * .01)], fill=col)


def ic_aid(dr, x, y, w, h, col):
    r = lambda *v: sc(*v)
    bx0, by0, bx1, by1 = x + w * .12, y + h * .34, x + w * .88, y + h * .92
    dr.rectangle(r(bx0, by0, bx1, by1), outline=col, width=int(w * .05 * S))
    dr.line(r(bx0, y + h * .50, bx1, y + h * .50), fill=col, width=int(w * .04 * S))
    dr.line(r(x + w * .50, by0, x + w * .50, by1), fill=col, width=int(w * .04 * S))
    sx, sy = x + w * .50, y + h * .06
    dr.line(r(sx, sy, sx, y + h * .34), fill=col, width=int(w * .035 * S))
    for i in range(3):
        yy = sy + h * (.02 + i * .055)
        for sgn in (-1, 1):
            dr.ellipse(r(sx + sgn * w * .032 - w * .034, yy - h * .026,
                         sx + sgn * w * .032 + w * .034, yy + h * .026), fill=col)


ICONS = {"chip": ic_chip, "rubble": ic_rubble, "bolt": ic_bolt,
         "sub": ic_sub, "chart": ic_chart, "aid": ic_aid}

FH = font(BOLD, 28)
FD = font(REG, 19)
FK = font(BOLD, 19)

for col, row, accent, kicker, head, detail, ic in cards:
    x = LEFT + col * (COLW + GAP)
    y = CARD_TOP + row * (CARD_H + GAP)

    d.rounded_rectangle(sc(x, y, x + COLW, y + CARD_H), radius=10 * S,
                        fill=CARD, outline=EDGE, width=int(1.5 * S))
    d.rounded_rectangle(sc(x, y, x + 8, y + CARD_H), radius=4 * S, fill=accent)

    # icon plate
    iw = ih = 92
    ix, iy = x + 20, y + 22
    d.rounded_rectangle(sc(ix, iy, ix + iw, iy + ih), radius=8 * S, fill=tint(accent))
    ICONS[ic](d, ix + 11, iy + 11, iw - 22, ih - 22, accent)

    tx = ix + iw + 18
    tw = x + COLW - tx - 16

    text((tx, y + 24), kicker, FK, accent)

    lines = wrap(head, FH, tw)[:3]
    ly = y + 52
    for ln in lines:
        text((tx, ly), ln, FH, INK)
        ly += 33

    dy = max(ly + 4, y + 150)
    for ln in wrap(detail, FD, tw)[:2]:
        text((tx, dy), ln, FD, (88, 85, 79))
        dy += 24

# ================================================================== footer
FY = CARD_TOP + 3 * CARD_H + 2 * GAP + 12
d.line(sc(60, FY, 964, FY), fill=(206, 201, 192), width=int(1.5 * S))
text((60, FY + 9), "Compiled from wire reports of 24 November 2026", font(REG, 17), MUTED)
text((964, FY + 9), "make.fun", font(BOLD, 17), (190, 185, 176), anchor="ra")

# ================================================================== output
out = img.resize((W, H), Image.LANCZOS)
out.save("/home/administrator/.hermes/cache/scratch/mkimg/entry.png", "PNG", optimize=True)
print("wrote entry.png", out.size, out.mode)
