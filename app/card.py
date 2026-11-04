"""Shareable result cards (PNG) drawn with Pillow: a household card with the
four headline numbers and the sentence, and a reform card with the cost and
who gains. Used by the download buttons in the app.

    import card
    png = card.household_card(title, subtitle, tiles, sentence, footer)
    st.download_button("PNG", png, "mi_hogar.png", "image/png")
"""

import io
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_PATH = Path(__file__).resolve().parent / "static" / "fonts" / "Inter.ttf"
NAVY = (31, 59, 87)
INK = (28, 39, 51)
MUTED = (91, 107, 122)
SOFT = (245, 248, 251)
LINE = (227, 232, 238)
RED = (196, 78, 82)
GREEN = (30, 132, 73)
WHITE = (255, 255, 255)
W = 1200  # px; 2:1 social-card ratio with H = 600 plus room for the sentence


def _font(size, weight=400):
    try:
        f = ImageFont.truetype(str(FONT_PATH), size)
        try:
            f.set_variation_by_axes([14, weight])
        except Exception:
            pass
        return f
    except Exception:
        return ImageFont.load_default(size)


def _wrap(draw, text, font, width):
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def household_card(title, subtitle, tiles, sentence, footer):
    """tiles: list of (label, value, colour) with colour in {'pays','gets','net','rate'}."""
    colours = {"pays": RED, "gets": GREEN, "net": NAVY, "rate": MUTED}
    img = Image.new("RGB", (W, 640), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=NAVY)
    d.text((56, 44), title, font=_font(40, 700), fill=NAVY)
    y = 100
    for line in _wrap(d, subtitle, _font(22), W - 112)[:2]:
        d.text((56, y), line, font=_font(22), fill=MUTED)
        y += 30
    # tiles
    y0 = y + 20
    gap, tw, th = 20, (W - 112 - 3 * 20) // 4, 150
    for i, (label, value, kind) in enumerate(tiles[:4]):
        x = 56 + i * (tw + gap)
        d.rounded_rectangle(
            [x, y0, x + tw, y0 + th], radius=14, fill=SOFT, outline=LINE
        )
        d.rectangle([x, y0 + 14, x + 5, y0 + th - 14], fill=colours[kind])
        for j, l in enumerate(_wrap(d, label, _font(18), tw - 40)[:2]):
            d.text((x + 22, y0 + 18 + j * 22), l, font=_font(18), fill=MUTED)
        d.text(
            (x + 22, y0 + 78),
            value,
            font=_font(44, 700),
            fill=colours[kind] if kind in ("pays", "gets") else NAVY,
        )
    y = y0 + th + 28
    for line in _wrap(d, sentence, _font(24), W - 112)[:4]:
        d.text((56, y), line, font=_font(24), fill=INK)
        y += 34
    d.line([56, 640 - 60, W - 56, 640 - 60], fill=LINE, width=1)
    d.text((56, 640 - 46), footer, font=_font(17), fill=MUTED)
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def reform_card(title, subtitle, headline, bullets, footer):
    img = Image.new("RGB", (W, 640), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=(235, 104, 52))
    y = 44
    for line in _wrap(d, title, _font(38, 700), W - 112)[:2]:
        d.text((56, y), line, font=_font(38, 700), fill=NAVY)
        y += 48
    for line in _wrap(d, subtitle, _font(22), W - 112)[:2]:
        d.text((56, y), line, font=_font(22), fill=MUTED)
        y += 30
    y += 16
    d.text((56, y), headline, font=_font(64, 700), fill=NAVY)
    y += 90
    for b in bullets[:4]:
        for line in _wrap(d, "•  " + b, _font(24), W - 112)[:2]:
            d.text((56, y), line, font=_font(24), fill=INK)
            y += 34
        y += 6
    d.line([56, 640 - 60, W - 56, 640 - 60], fill=LINE, width=1)
    d.text((56, 640 - 46), footer, font=_font(17), fill=MUTED)
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()
