#!/usr/bin/env python3
"""Render the editorial news poster for 17 November 2026."""

from PIL import Image, ImageDraw, ImageFont

W = H = 1000
OUT = "entry.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BG = "#0B1020"
HEADER = "#121B30"
GOLD = "#F0C04A"
WHITE = "#F7F7F5"
BODY = "#CDD7E6"
MUTED = "#8195B2"
CARD = "#161F33"
INK = "#0B1020"

STORIES = [
    (
        "US-IRAN ESCALATION",
        "Third drone strike on a US radar base in Bahrain intercepted; "
        "US retaliates. Gas tanker hit in Strait of Hormuz.",
        "#EF6A5A",
    ),
    (
        "UKRAINE HITS KERCH BRIDGE",
        "Largest drone strike of the war damages the Kerch Bridge to "
        "Crimea and oil refineries.",
        "#4DA3E3",
    ),
    (
        "TRUMP ARRIVES IN MANILA",
        "Asia trip begins ahead of a trilateral summit with Xi and "
        "Putin in Shenzhen.",
        "#F0C04A",
    ),
    (
        "ALASKA SENATE FLIP",
        "Peltola ousts Sullivan in a US Senate flip.",
        "#7BC47F",
    ),
    (
        "NVIDIA BREAKS SILENCE",
        "Founder's first public comments since stepping down amid a "
        "spy scandal.",
        "#5FD0C0",
    ),
    (
        "BANKING AND FLIGHT OUTAGES",
        "JPMorgan/Chase Zelle down for hours; United flights disrupted "
        "after an FAA ground stop.",
        "#B18CF0",
    ),
    (
        "ISRAEL AND ITALY",
        "Italy passes antisemitism law; a new Knesset speaker is elected "
        "in Israel.",
        "#EA8FB6",
    ),
    (
        "CLIMATE TALKS",
        "Small island nations demand stronger action at the UN climate "
        "summit.",
        "#A8C94F",
    ),
]


def wrap(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(BOLD, 66)
    date_font = ImageFont.truetype(BOLD, 38)
    small_font = ImageFont.truetype(BOLD, 20)
    tiny_font = ImageFont.truetype(REG, 19)
    head_font = ImageFont.truetype(BOLD, 23)
    detail_font = ImageFont.truetype(REG, 19)
    badge_font = ImageFont.truetype(BOLD, 20)

    # Masthead
    d.rectangle((0, 0, W, 168), fill=HEADER)
    d.rectangle((0, 168, W, 173), fill=GOLD)
    d.text((40, 24), "WORLD NEWS", font=title_font, fill=WHITE)
    d.text((42, 108), "17 NOVEMBER 2026", font=date_font, fill=GOLD)
    d.text((960, 52), "TUESDAY", font=small_font, fill=BODY, anchor="ra")
    d.text((960, 92), "08 STORIES / GLOBAL BRIEF", font=tiny_font,
           fill=MUTED, anchor="ra")

    # Story grid: 2 columns x 4 rows
    card_w, card_h, gap_x, gap_y = 450, 184, 20, 12
    top = 190
    for i, (headline, detail, accent) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = 40 + col * (card_w + gap_x)
        y = top + row * (card_h + gap_y)

        d.rounded_rectangle((x, y, x + card_w, y + card_h), radius=12,
                            fill=CARD, outline=accent, width=2)
        d.rounded_rectangle((x + 2, y + 14, x + 8, y + card_h - 14),
                            radius=3, fill=accent)

        d.rounded_rectangle((x + 18, y + 16, x + 54, y + 52), radius=7,
                            fill=accent)
        label = str(i + 1)
        bbox = d.textbbox((0, 0), label, font=badge_font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((x + 36 - tw / 2 - bbox[0], y + 34 - th / 2 - bbox[1]),
               label, font=badge_font, fill=INK)

        head_lines = wrap(d, headline, head_font, card_w - 80)
        assert len(head_lines) <= 2, (i, head_lines)
        for line_no, line in enumerate(head_lines):
            d.text((x + 66, y + 17 + line_no * 28), line,
                   font=head_font, fill=WHITE)

        detail_y = y + 22 + len(head_lines) * 29 + 6
        lines = wrap(d, detail, detail_font, card_w - 44)
        assert len(lines) <= 4, (i, lines)
        for line_no, line in enumerate(lines):
            d.text((x + 22, detail_y + line_no * 25), line,
                   font=detail_font, fill=BODY)
            assert detail_y + line_no * 25 + 23 <= y + card_h - 6, (
                "clipped detail", i)

    assert img.size == (W, H)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT}: {img.size}, color mode {img.mode}")


if __name__ == "__main__":
    main()
