"""Draw the news-image-20261123 entry: one newspaper front page.

A 1024x1024 PNG, masthead "The World in One Day", summing up
Monday 23 November 2026 in six stories. Flat vector shapes drawn
with Pillow only -- no photos, no downloaded assets.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 230)
PANEL = (241, 235, 218)
INK = (26, 23, 18)
RED = (166, 38, 24)
NAVY = (31, 52, 84)
GREEN = (22, 92, 44)
GRAY = (97, 89, 75)
LINE = (198, 189, 165)
SKY = (198, 218, 230)
LAND = (96, 142, 92)

NOTO = "/usr/share/fonts/truetype/noto/"
_cache = {}


def F(name, size):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(NOTO + name, size)
    return _cache[key]


def serif(size):
    return F("NotoSerif-Bold.ttf", size)


def sans(size, bold=True):
    return F("NotoSans-Bold.ttf" if bold else "NotoSans-Regular.ttf", size)


def italic(size):
    return F("NotoSerif-Italic.ttf", size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def tw(text, font):
    return d.textlength(text, font=font)


def wrap(text, font, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if tw(trial, font) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(x, y, text, font, fill, maxw, lh):
    for line in wrap(text, font, maxw):
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def centered(text, y, font, fill):
    d.text(((W - tw(text, font)) / 2, y), text, font=font, fill=fill)


def rule(y, x0=36, x1=988, fill=INK, width=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# ------------------------------------------------------------------
# Page frame and masthead
# ------------------------------------------------------------------
d.rectangle([13, 13, 1011, 1011], outline=INK, width=3)
d.rectangle([21, 21, 1003, 1003], outline=INK, width=1)

centered("ONE PAGE · THE WHOLE DAY · EVERYWHERE ON EARTH", 38, sans(16), GRAY)
centered("THE WORLD IN ONE DAY", 62, serif(64), INK)
rule(148, width=3)

d.rectangle([36, 158, 988, 198], fill=INK)
d.text((52, 168), "No. 8", font=sans(16), fill=PAPER)
centered("MONDAY · 23 NOVEMBER 2026", 165, sans(24), PAPER)
rgt = "GLOBAL EDITION"
d.text((988 - tw(rgt, sans(16)), 168), rgt, font=sans(16), fill=PAPER)

# ------------------------------------------------------------------
# Lead story: COP31 ends with no deal
# ------------------------------------------------------------------
LX, LY = 36, 218
d.text((LX, LY), "CLIMATE — ANTALYA, TÜRKIYE", font=sans(17), fill=RED)
y = block(LX, LY + 26, "COP31 climate summit ends with no deal",
          serif(37), INK, 592, 46)
y = block(LX, y + 8,
          "After nearly 48 hours of overtime, nearly 200 nations left "
          "Antalya without a deal. The EU rejected a final text that "
          "dropped any mention of moving away from fossil fuels, and "
          "Pacific island nations voiced despair.",
          sans(19, bold=False), INK, 592, 26)
d.text((LX, 442), "Reuters · SCMP · Xinhua", font=italic(15), fill=GRAY)

# Lead illustration: globe, thermometer, NO DEAL stamp
IX0, IY0, IX1, IY1 = 652, 218, 988, 462
d.rectangle([IX0, IY0, IX1, IY1], fill=(238, 232, 214), outline=LINE, width=1)
cx, cy, r = 770, 322, 76
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY, outline=NAVY, width=3)
d.ellipse([cx - 62, cy - 48, cx - 8, cy - 6], fill=LAND)      # Americas top
d.polygon([(cx - 44, cy + 2), (cx - 12, cy + 4), (cx - 22, cy + 52),
           (cx - 40, cy + 34)], fill=LAND)                     # Americas low
d.ellipse([cx + 8, cy - 40, cx + 58, cy + 2], fill=LAND)      # Europe/Asia
d.ellipse([cx + 16, cy + 8, cx + 46, cy + 40], fill=LAND)     # Africa
d.ellipse([cx - r, cy - 30, cx + r, cy + 30], outline=NAVY, width=1)
d.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=1)
# thermometer
tx = 902
d.rounded_rectangle([tx, 252, tx + 22, 372], radius=11, outline=INK, width=3)
d.ellipse([tx - 13, 356, tx + 35, 404], outline=INK, width=3)
d.rectangle([tx + 6, 268, tx + 16, 372], fill=RED)
d.ellipse([tx - 6, 363, tx + 28, 397], fill=RED)
for i in range(4):
    d.line([(tx + 30, 272 + i * 26), (tx + 44, 272 + i * 26)], fill=INK, width=2)
# stamp
stamp = Image.new("RGBA", (224, 88), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([4, 4, 220, 84], radius=10, outline=RED + (255,), width=6)
t = "NO DEAL"
sd.text(((224 - sd.textlength(t, font=sans(42))) / 2, 18), t,
        font=sans(42), fill=RED + (255,))
tilted = stamp.rotate(9, expand=True)
img.paste(tilted, (650, 338), tilted)
d = ImageDraw.Draw(img)

rule(478, fill=LINE, width=1)

# ------------------------------------------------------------------
# Four panel stories
# ------------------------------------------------------------------
def panel(x0, y0, kicker, kcolor, head, body, source):
    x1, y1 = x0 + 464, y0 + 192
    d.rectangle([x0, y0, x1, y1], fill=PANEL, outline=LINE, width=1)
    d.rectangle([x0 + 14, y0 + 13, x0 + 26, y0 + 25], fill=kcolor)
    d.text((x0 + 34, y0 + 9), kicker, font=sans(15), fill=kcolor)
    y = block(x0 + 14, y0 + 34, head, serif(23), INK, 436, 28)
    block(x0 + 14, y + 4, body, sans(17, bold=False), INK, 436, 22)
    d.text((x0 + 14, y1 - 24), source, font=italic(14), fill=GRAY)


panel(36, 490, "UKRAINE — WAR", RED,
      "Russian attack kills 11 in Kyiv region",
      "Rescuers pulled another body from the rubble in Dymer on "
      "Monday, lifting the toll to 11, in the latest of a week of "
      "heavy strikes across Ukraine.",
      "Reuters · Arab News")
panel(524, 490, "INDONESIA — DISASTER", RED,
      "Factory fire toll rises to 24, dozens missing",
      "Rescuers picked through the burned-out Cikande candy factory "
      "in Banten for about 30 workers still missing, as police "
      "confirmed 24 dead.",
      "Reuters · The Straits Times · Xinhua")
panel(36, 694, "UNITED STATES — POLITICS", NAVY,
      "Democrats seal 258-seat House majority",
      "Democrats clinched at least 258 House seats — their largest "
      "majority since 1992 — as the last of the midterm races were "
      "called.",
      "SCMP · Economic Times · Arab News")
panel(524, 694, "MARKETS — AI SELL-OFF", NAVY,
      "AI sell-off deepens as Asia tumbles",
      "Seoul's Kospi fell as much as 5.8% as AI-boom fears spread "
      "through Asia; on Friday the S&P 500 slid 3.7% into correction "
      "and the Nasdaq lost 5.3%.",
      "Al Jazeera · AP · Reuters")

# ------------------------------------------------------------------
# Sport banner and footer
# ------------------------------------------------------------------
d.rectangle([36, 898, 988, 958], fill=GREEN)
d.ellipse([906, 906, 950, 950], outline=PAPER, width=3)
d.ellipse([922, 922, 934, 934], fill=PAPER)
d.text((56, 905), "SPORT — Liverpool 4–0 Man United: Pochettino's "
       "debut nightmare", font=sans(21), fill=PAPER)
d.text((56, 934), "Yoro sent off in the 8th minute · two down in 13 · "
       "United stay 19th · Reuters · Al Jazeera",
       font=sans(15, bold=False), fill=PAPER)

rule(970, fill=LINE, width=1)
centered("Drawn from reports published on Monday 23 November 2026 — "
         "Reuters · AP · Al Jazeera · SCMP · Xinhua · The Straits Times",
         978, italic(14), GRAY)

if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, optimize=True)
    print(out, os.path.getsize(out), "bytes")
