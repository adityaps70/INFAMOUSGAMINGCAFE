import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4

from generate_rate_card_variants import (
    BLACK,
    GREEN,
    MUTED,
    RED,
    WHITE,
    draw_logo,
    draw_tracking_text,
    fit_font_size,
    register_fonts,
    render_png,
    start_card,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
RATES_PATH = ROOT / "src" / "rates.json"
COMPARISON_PATH = OUTPUT_DIR / "infamous-gaming-premium-rate-card-collection.png"

COLLECTION = {
    "luxe": OUTPUT_DIR / "infamous-gaming-rate-card-premium-luxe",
    "hud": OUTPUT_DIR / "infamous-gaming-rate-card-premium-hud",
    "lounge": OUTPUT_DIR / "infamous-gaming-rate-card-premium-lounge",
}

CHARCOAL = Color(12 / 255, 14 / 255, 13 / 255)
GRAPHITE = Color(21 / 255, 24 / 255, 22 / 255)
SOFT_LINE = Color(1, 1, 1, alpha=0.12)
GREEN_GLOW = Color(5 / 255, 230 / 255, 4 / 255, alpha=0.22)
RED_GLOW = Color(1, 23 / 255, 23 / 255, alpha=0.22)

OPTIONS = [
    ("console", "CONSOLE"),
    ("pc", "PC"),
    ("billiards", "BILLIARDS"),
    ("racing", "RACING"),
    ("table", "TABLE SPORTS"),
    ("board", "BOARD GAMES"),
]


def draw_logo_plate(pdf, x, y, width=140, height=108, border=GREEN, logo_size=92):
    pdf.setFillColor(BLACK)
    pdf.setStrokeColor(border)
    pdf.setLineWidth(1.15)
    pdf.rect(x, y, width, height, fill=1, stroke=1)
    pdf.setStrokeColor(RED if border == GREEN else GREEN)
    pdf.setLineWidth(1)
    pdf.line(x, y + 12, x + 38, y + 12)
    pdf.line(x + width - 38, y + height - 12, x + width, y + height - 12)
    draw_logo(pdf, x + (width - logo_size) / 2, y + (height - logo_size) / 2, logo_size)


def draw_controller(pdf, cx, cy, size, color):
    path = pdf.beginPath()
    path.moveTo(cx - size * 0.42, cy - size * 0.13)
    path.curveTo(
        cx - size * 0.52,
        cy - size * 0.42,
        cx - size * 0.24,
        cy - size * 0.46,
        cx - size * 0.10,
        cy - size * 0.23,
    )
    path.lineTo(cx + size * 0.10, cy - size * 0.23)
    path.curveTo(
        cx + size * 0.24,
        cy - size * 0.46,
        cx + size * 0.52,
        cy - size * 0.42,
        cx + size * 0.42,
        cy - size * 0.13,
    )
    path.curveTo(cx + size * 0.34, cy + size * 0.12, cx + size * 0.24, cy + size * 0.22, cx, cy + size * 0.20)
    path.curveTo(cx - size * 0.24, cy + size * 0.22, cx - size * 0.34, cy + size * 0.12, cx - size * 0.42, cy - size * 0.13)
    path.close()
    pdf.setStrokeColor(color)
    pdf.setLineWidth(1.15)
    pdf.drawPath(path, fill=0, stroke=1)
    pdf.line(cx - size * 0.23, cy, cx - size * 0.05, cy)
    pdf.line(cx - size * 0.14, cy - size * 0.09, cx - size * 0.14, cy + size * 0.09)
    pdf.circle(cx + size * 0.18, cy + size * 0.04, size * 0.045, fill=0, stroke=1)
    pdf.circle(cx + size * 0.28, cy - size * 0.05, size * 0.045, fill=0, stroke=1)


def draw_pc(pdf, cx, cy, size, color):
    pdf.setStrokeColor(color)
    pdf.setLineWidth(1.15)
    pdf.roundRect(cx - size * 0.42, cy - size * 0.24, size * 0.64, size * 0.48, size * 0.04, fill=0, stroke=1)
    pdf.line(cx - size * 0.10, cy - size * 0.24, cx - size * 0.10, cy - size * 0.36)
    pdf.line(cx - size * 0.26, cy - size * 0.36, cx + size * 0.06, cy - size * 0.36)
    pdf.roundRect(cx + size * 0.27, cy - size * 0.30, size * 0.15, size * 0.58, size * 0.025, fill=0, stroke=1)
    pdf.circle(cx + size * 0.345, cy - size * 0.19, size * 0.025, fill=0, stroke=1)


def draw_billiards(pdf, cx, cy, size, color):
    pdf.setStrokeColor(color)
    pdf.setLineWidth(1.15)
    pdf.circle(cx - size * 0.16, cy, size * 0.18, fill=0, stroke=1)
    pdf.circle(cx + size * 0.15, cy + size * 0.07, size * 0.18, fill=0, stroke=1)
    pdf.circle(cx + size * 0.02, cy - size * 0.17, size * 0.18, fill=0, stroke=1)
    pdf.line(cx - size * 0.45, cy - size * 0.38, cx + size * 0.46, cy + size * 0.38)
    pdf.setFillColor(color)
    pdf.setFont("ArenaBold", max(4, size * 0.13))
    pdf.drawCentredString(cx - size * 0.16, cy - size * 0.045, "8")


def draw_racing(pdf, cx, cy, size, color):
    pdf.setStrokeColor(color)
    pdf.setLineWidth(1.15)
    pdf.circle(cx, cy, size * 0.36, fill=0, stroke=1)
    pdf.circle(cx, cy, size * 0.10, fill=0, stroke=1)
    for dx, dy in ((0, 0.26), (-0.24, -0.19), (0.24, -0.19)):
        pdf.line(cx, cy, cx + size * dx, cy + size * dy)


def draw_table_sports(pdf, cx, cy, size, color):
    pdf.setStrokeColor(color)
    pdf.setLineWidth(1.15)
    pdf.circle(cx - size * 0.12, cy + size * 0.07, size * 0.21, fill=0, stroke=1)
    pdf.line(cx - size * 0.26, cy - size * 0.08, cx - size * 0.42, cy - size * 0.31)
    pdf.circle(cx + size * 0.27, cy + size * 0.19, size * 0.07, fill=0, stroke=1)
    pdf.line(cx + size * 0.06, cy - size * 0.28, cx + size * 0.40, cy - size * 0.28)
    pdf.line(cx + size * 0.08, cy - size * 0.20, cx + size * 0.08, cy - size * 0.36)
    pdf.line(cx + size * 0.38, cy - size * 0.20, cx + size * 0.38, cy - size * 0.36)


def draw_board_games(pdf, cx, cy, size, color):
    pdf.setStrokeColor(color)
    pdf.setLineWidth(1.15)
    pdf.roundRect(cx - size * 0.40, cy - size * 0.28, size * 0.45, size * 0.58, size * 0.04, fill=0, stroke=1)
    pdf.roundRect(cx - size * 0.10, cy - size * 0.22, size * 0.46, size * 0.58, size * 0.04, fill=0, stroke=1)
    for dx, dy in ((0.02, 0.18), (0.22, 0.18), (0.02, -0.04), (0.22, -0.04)):
        pdf.circle(cx + size * dx, cy + size * dy, size * 0.035, fill=0, stroke=1)


ICON_DRAWERS = {
    "console": draw_controller,
    "pc": draw_pc,
    "billiards": draw_billiards,
    "racing": draw_racing,
    "table": draw_table_sports,
    "board": draw_board_games,
}


def draw_option_strip(pdf, x, y, width, height, style):
    tile_width = width / len(OPTIONS)
    for index, (kind, label) in enumerate(OPTIONS):
        tile_x = x + index * tile_width
        accent = GREEN if index % 2 == 0 else RED

        if style == "luxe":
            pdf.setFillColor(Color(1, 1, 1, alpha=0.025))
            pdf.setStrokeColor(Color(accent.red, accent.green, accent.blue, alpha=0.48))
            pdf.roundRect(tile_x + 3, y + 4, tile_width - 6, height - 8, 5, fill=1, stroke=1)
        elif style == "hud":
            pdf.setStrokeColor(accent)
            pdf.setLineWidth(0.65)
            pdf.line(tile_x + 5, y + 5, tile_x + 5, y + height - 5)
            pdf.line(tile_x + 5, y + height - 5, tile_x + 22, y + height - 5)
        else:
            pdf.setStrokeColor(Color(1, 1, 1, alpha=0.14))
            pdf.setLineWidth(0.45)
            if index:
                pdf.line(tile_x, y + 8, tile_x, y + height - 8)

        ICON_DRAWERS[kind](pdf, tile_x + tile_width / 2, y + height * 0.62, min(tile_width * 0.48, height * 0.48), accent)
        label_size = fit_font_size(label, "ArenaBold", 5.8, tile_width - 8, min_size=4.6)
        pdf.setFillColor(WHITE if style != "lounge" else MUTED)
        pdf.setFont("ArenaBold", label_size)
        pdf.drawCentredString(tile_x + tile_width / 2, y + 11, label)


def draw_rate_rows(pdf, group, x, top, width, available_height, accent, style):
    pdf.setFillColor(MUTED)
    pdf.setFont("ArenaBold", 5.2 if style != "lounge" else 5.5)
    pdf.drawRightString(x + width - 55, top, "HALF HOUR")
    pdf.drawRightString(x + width - 9, top, "FULL HOUR")

    row_height = (available_height - 12) / len(group["items"])
    for index, item in enumerate(group["items"]):
        row_top = top - 11 - index * row_height
        baseline = row_top - row_height * 0.62
        if index or style == "lounge":
            pdf.setStrokeColor(Color(1, 1, 1, alpha=0.08 if style != "lounge" else 0.12))
            pdf.setLineWidth(0.35)
            pdf.line(x + 7, row_top, x + width - 8, row_top)
        name_size = fit_font_size(item["name"], "ArenaBold", 8.8 if style != "lounge" else 9.6, width - 112)
        pdf.setFillColor(WHITE)
        pdf.setFont("ArenaBold", name_size)
        pdf.drawString(x + 8, baseline, item["name"])
        pdf.setFont("ArenaCurrency", 9.8 if style != "lounge" else 10.2)
        pdf.setFillColor(accent)
        pdf.drawRightString(x + width - 55, baseline - 1, f"₹{item['halfHour']}")
        pdf.setFillColor(WHITE)
        pdf.drawRightString(x + width - 9, baseline - 1, f"₹{item['fullHour']}")


def draw_luxe_group(pdf, group, x, top, width, height, number, accent):
    bottom = top - height
    pdf.setFillColor(GRAPHITE)
    pdf.setStrokeColor(Color(accent.red, accent.green, accent.blue, alpha=0.75))
    pdf.setLineWidth(0.9)
    pdf.roundRect(x, bottom, width, height, 8, fill=1, stroke=1)
    pdf.setFillColor(accent)
    pdf.roundRect(x + 11, top - 36, 33, 25, 4, fill=1, stroke=0)
    pdf.setFillColor(BLACK)
    pdf.setFont("ArenaDisplay", 12.5)
    pdf.drawCentredString(x + 27.5, top - 29, f"0{number}")
    draw_tracking_text(pdf, group["category"].upper(), x + 54, top - 30, "ArenaDisplay", 12.5, WHITE, 0.15)
    draw_rate_rows(pdf, group, x + 5, top - 49, width - 10, height - 53, accent, "luxe")


def draw_footer(pdf, width, mode):
    x, y, w, h = 28, 24, width - 56, 104
    if mode == "luxe":
        pdf.setFillColor(GRAPHITE)
        pdf.setStrokeColor(RED)
        pdf.roundRect(x, y, w, h, 8, fill=1, stroke=1)
        pdf.setFillColor(GREEN)
        pdf.roundRect(x + w - 184, y, 184, h, 8, fill=1, stroke=0)
    elif mode == "hud":
        pdf.setFillColor(BLACK)
        pdf.setStrokeColor(GREEN)
        pdf.rect(x, y, w, h, fill=1, stroke=1)
        pdf.setFillColor(RED)
        pdf.rect(x, y + h - 5, w, 5, fill=1, stroke=0)
        pdf.setFillColor(GREEN)
        pdf.rect(x + w - 184, y, 184, h - 5, fill=1, stroke=0)
    else:
        pdf.setFillColor(CHARCOAL)
        pdf.setStrokeColor(Color(1, 1, 1, alpha=0.18))
        pdf.roundRect(x, y, w, h, 5, fill=1, stroke=1)
        pdf.setFillColor(RED)
        pdf.rect(x, y + h - 3, w, 3, fill=1, stroke=0)
        pdf.setStrokeColor(GREEN)
        pdf.setLineWidth(1.2)
        pdf.line(x + w - 186, y + 12, x + w - 186, y + h - 12)

    left = x + 15
    pdf.setFillColor(WHITE)
    pdf.setFont("ArenaBold", 7.0)
    pdf.drawString(left, y + 76, "Additional charges apply for more than two players.")
    pdf.setFillColor(MUTED)
    pdf.setFont("ArenaRegular", 6.2)
    pdf.drawString(left, y + 51, "A-1/114, Ratan Khand, Sharda Nagar")
    pdf.drawString(left, y + 37, "Lucknow, Uttar Pradesh 226012")
    pdf.setFillColor(GREEN)
    pdf.setFont("ArenaBold", 6.6)
    pdf.drawString(left, y + 16, "@infamousgaming_cafe")

    contact_x = x + w - 169
    contact_color = BLACK if mode in {"luxe", "hud"} else WHITE
    pdf.setFillColor(contact_color)
    draw_tracking_text(pdf, "BOOK YOUR SESSION", contact_x, y + 72, "ArenaBold", 6.8, contact_color, 0.55)
    pdf.setFont("ArenaCurrency", 16.2)
    pdf.drawString(contact_x, y + 43, "+91 99183 32386")
    pdf.setFont("ArenaBold", 6.0)
    pdf.drawString(contact_x, y + 19, "CALL OR WHATSAPP")


def create_luxe(rates, path):
    pdf, width, height = start_card(path, "Premium Luxe Gaming Arena")

    # Carbon-like diagonal texture and a restrained red premium edge.
    pdf.setStrokeColor(Color(1, 1, 1, alpha=0.035))
    pdf.setLineWidth(0.35)
    for offset in range(-800, 700, 18):
        pdf.line(offset, 0, offset + 840, 840)
    pdf.setFillColor(RED)
    pdf.rect(0, 0, 7, height, fill=1, stroke=0)
    pdf.setFillColor(GREEN)
    pdf.rect(7, 0, 3, height, fill=1, stroke=0)

    draw_logo_plate(pdf, 28, 715, 140, 105, GREEN, 88)
    draw_tracking_text(pdf, "PREMIUM GAMING", 194, 789, "ArenaDisplay", 27, WHITE, 0.12)
    draw_tracking_text(pdf, "ARENA RATE CARD", 194, 751, "ArenaDisplay", 25, GREEN, 0.1)
    draw_tracking_text(pdf, "INFAMOUS  /  PLAY BEYOND ORDINARY", 195, 724, "ArenaBold", 6.2, MUTED, 0.75)
    pdf.setStrokeColor(RED)
    pdf.setLineWidth(1.1)
    pdf.line(194, 708, width - 28, 708)

    draw_option_strip(pdf, 28, 620, width - 56, 74, "luxe")

    gutter = 14
    panel_width = (width - 56 - gutter) / 2
    left, right = 28, 28 + panel_width + gutter
    draw_luxe_group(pdf, rates[0], left, 605, panel_width, 212, 1, GREEN)
    draw_luxe_group(pdf, rates[1], right, 605, panel_width, 190, 2, RED)
    draw_luxe_group(pdf, rates[2], left, 376, panel_width, 184, 3, RED)
    draw_luxe_group(pdf, rates[3], right, 398, panel_width, 184, 4, GREEN)

    draw_footer(pdf, width, "luxe")
    pdf.showPage()
    pdf.save()


def draw_hud_grid(pdf, width, height):
    pdf.setStrokeColor(Color(5 / 255, 230 / 255, 4 / 255, alpha=0.055))
    pdf.setLineWidth(0.35)
    for x in range(0, int(width) + 1, 20):
        pdf.line(x, 0, x, height)
    for y in range(0, int(height) + 1, 20):
        pdf.line(0, y, width, y)


def draw_hud_module(pdf, group, x, top, width, height, number, accent):
    bottom = top - height
    panel = pdf.beginPath()
    panel.moveTo(x + 10, bottom)
    panel.lineTo(x + width - 16, bottom)
    panel.lineTo(x + width, bottom + 16)
    panel.lineTo(x + width, top)
    panel.lineTo(x, top)
    panel.lineTo(x, bottom + 10)
    panel.close()
    pdf.setFillColor(Color(8 / 255, 12 / 255, 9 / 255))
    pdf.setStrokeColor(accent)
    pdf.setLineWidth(0.85)
    pdf.drawPath(panel, fill=1, stroke=1)

    pdf.setFillColor(accent)
    pdf.rect(x, top - 26, 70, 26, fill=1, stroke=0)
    pdf.setFillColor(BLACK)
    pdf.setFont("ArenaDisplay", 11.5)
    pdf.drawString(x + 10, top - 19, f"ZONE 0{number}")
    draw_tracking_text(pdf, group["category"].upper(), x + 82, top - 19, "ArenaDisplay", 12.5, WHITE, 0.18)
    pdf.setFillColor(MUTED)
    pdf.setFont("ArenaBold", 5.2)
    pdf.drawRightString(x + width - 58, top - 18, "HALF HOUR")
    pdf.drawRightString(x + width - 13, top - 18, "FULL HOUR")

    row_height = (height - 31) / len(group["items"])
    for index, item in enumerate(group["items"]):
        row_top = top - 30 - index * row_height
        baseline = row_top - row_height * 0.64
        if index:
            pdf.setStrokeColor(Color(1, 1, 1, alpha=0.08))
            pdf.line(x + 12, row_top, x + width - 12, row_top)
        pdf.setFillColor(WHITE)
        pdf.setFont("ArenaBold", fit_font_size(item["name"], "ArenaBold", 8.5, width - 126))
        pdf.drawString(x + 13, baseline, item["name"])
        pdf.setFont("ArenaCurrency", 9.5)
        pdf.setFillColor(accent)
        pdf.drawRightString(x + width - 58, baseline - 1, f"₹{item['halfHour']}")
        pdf.setFillColor(WHITE)
        pdf.drawRightString(x + width - 13, baseline - 1, f"₹{item['fullHour']}")

    pdf.setStrokeColor(accent)
    pdf.setLineWidth(1)
    pdf.line(x + width - 35, bottom + 7, x + width - 12, bottom + 7)
    pdf.circle(x + width - 9, bottom + 7, 2.5, fill=0, stroke=1)


def create_hud(rates, path):
    pdf, width, height = start_card(path, "Premium Esports HUD")
    draw_hud_grid(pdf, width, height)

    pdf.setFillColor(RED)
    header = pdf.beginPath()
    header.moveTo(182, height)
    header.lineTo(width, height)
    header.lineTo(width, 714)
    header.lineTo(214, 714)
    header.close()
    pdf.drawPath(header, fill=1, stroke=0)
    draw_logo_plate(pdf, 28, 724, 136, 96, GREEN, 80)
    draw_tracking_text(pdf, "ESPORTS HUD", 218, 790, "ArenaDisplay", 27, BLACK, 0.08)
    draw_tracking_text(pdf, "INFAMOUS RATE CARD", 218, 751, "ArenaDisplay", 22.5, BLACK, 0.12)
    draw_tracking_text(pdf, "LIVE ARENAS  /  CURRENT PRICES", 219, 726, "ArenaBold", 6.0, BLACK, 0.8)

    pdf.setFillColor(GREEN)
    pdf.rect(28, 696, width - 56, 4, fill=1, stroke=0)
    draw_option_strip(pdf, 28, 643, width - 56, 49, "hud")

    x, module_width = 28, width - 56
    draw_hud_module(pdf, rates[0], x, 630, module_width, 108, 1, GREEN)
    draw_hud_module(pdf, rates[1], x, 511, module_width, 98, 2, RED)
    draw_hud_module(pdf, rates[2], x, 402, module_width, 98, 3, RED)
    draw_hud_module(pdf, rates[3], x, 293, module_width, 98, 4, GREEN)

    pdf.setStrokeColor(GREEN)
    pdf.setLineWidth(1)
    pdf.line(17, 620, 17, 213)
    for y, accent in ((602, GREEN), (486, RED), (377, RED), (268, GREEN)):
        pdf.setStrokeColor(accent)
        pdf.circle(17, y, 3.2, fill=0, stroke=1)
        pdf.line(17, y, 28, y)

    draw_footer(pdf, width, "hud")
    pdf.showPage()
    pdf.save()


def draw_lounge_group(pdf, group, x, top, width, height, number, accent):
    pdf.setFillColor(accent)
    pdf.setFont("ArenaDisplay", 10)
    pdf.drawString(x, top - 9, f"0{number}")
    draw_tracking_text(pdf, group["category"].upper(), x + 30, top - 10, "ArenaDisplay", 14, WHITE, 0.12)
    pdf.setStrokeColor(accent)
    pdf.setLineWidth(0.8)
    pdf.line(x, top - 18, x + width, top - 18)
    draw_rate_rows(pdf, group, x, top - 32, width, height - 35, accent, "lounge")


def draw_lounge_watermarks(pdf, width):
    subtle_green = Color(5 / 255, 230 / 255, 4 / 255, alpha=0.05)
    subtle_red = Color(1, 23 / 255, 23 / 255, alpha=0.055)
    draw_controller(pdf, width - 78, 635, 132, subtle_green)
    draw_billiards(pdf, 85, 315, 116, subtle_red)
    draw_racing(pdf, width - 78, 292, 112, subtle_green)


def create_lounge(rates, path):
    pdf, width, height = start_card(path, "Premium Lounge Menu")

    pdf.setFillColor(RED)
    pdf.rect(0, 0, 8, height, fill=1, stroke=0)
    pdf.setFillColor(GREEN)
    pdf.rect(8, 0, 3, height, fill=1, stroke=0)
    draw_lounge_watermarks(pdf, width)

    draw_tracking_text(pdf, "INFAMOUS", 34, 792, "ArenaDisplay", 30, WHITE, 0.1)
    draw_tracking_text(pdf, "PREMIUM LOUNGE", 34, 753, "ArenaDisplay", 25, GREEN, 0.08)
    draw_tracking_text(pdf, "GAMING RATE CARD", 35, 719, "ArenaDisplay", 20, WHITE, 0.12)
    draw_logo_plate(pdf, width - 162, 719, 134, 101, RED, 84)
    pdf.setStrokeColor(Color(1, 1, 1, alpha=0.18))
    pdf.setLineWidth(0.7)
    pdf.line(34, 698, width - 28, 698)
    draw_tracking_text(pdf, "CURATED PLAY  /  TIME WELL SPENT", 35, 679, "ArenaBold", 6.2, MUTED, 0.7)

    column_width = (width - 84) / 2
    left, right = 34, 50 + column_width
    draw_lounge_group(pdf, rates[0], left, 650, column_width, 218, 1, GREEN)
    draw_lounge_group(pdf, rates[1], right, 650, column_width, 188, 2, RED)
    draw_lounge_group(pdf, rates[2], left, 414, column_width, 176, 3, RED)
    draw_lounge_group(pdf, rates[3], right, 444, column_width, 176, 4, GREEN)

    draw_tracking_text(pdf, "THE INFAMOUS EXPERIENCE", 34, 218, "ArenaDisplay", 11.5, WHITE, 0.25)
    pdf.setStrokeColor(RED)
    pdf.line(212, 221, width - 28, 221)
    draw_option_strip(pdf, 34, 145, width - 68, 63, "lounge")

    draw_footer(pdf, width, "lounge")
    pdf.showPage()
    pdf.save()


def create_comparison_sheet():
    target_height = 1180
    thumbnails = []
    labels = {
        "luxe": "01  LUXE GAMING ARENA",
        "hud": "02  ESPORTS HUD",
        "lounge": "03  PREMIUM LOUNGE",
    }
    for label, stem in COLLECTION.items():
        image = Image.open(stem.with_suffix(".png")).convert("RGB")
        target_width = round(image.width * target_height / image.height)
        image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        thumbnails.append((label, image))

    margin, gap, title_height, label_height = 72, 62, 150, 84
    width = margin * 2 + sum(image.width for _, image in thumbnails) + gap * 2
    height = margin + title_height + target_height + label_height + margin
    sheet = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(sheet)
    title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 47)
    label_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 27)
    body_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 21)

    draw.text((margin, margin), "INFAMOUS PREMIUM RATE CARD COLLECTION", font=title_font, fill=(5, 230, 4))
    draw.text(
        (margin, margin + 66),
        "Three original A4 concepts  /  confirmed rates  /  original logo  /  300 DPI",
        font=body_font,
        fill=(225, 225, 220),
    )

    x = margin
    for index, (label, image) in enumerate(thumbnails):
        y = margin + title_height
        border = (5, 230, 4) if index != 1 else (255, 23, 23)
        draw.rectangle((x - 5, y - 5, x + image.width + 5, y + image.height + 5), outline=border, width=5)
        sheet.paste(image, (x, y))
        draw.text((x, y + image.height + 24), labels[label], font=label_font, fill=border)
        x += image.width + gap

    sheet.save(COMPARISON_PATH, quality=95)


def main():
    register_fonts()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rates = json.loads(RATES_PATH.read_text(encoding="utf-8"))
    if len(rates) != 4:
        raise ValueError("Premium collection layouts expect exactly four rate groups")

    creators = {
        "luxe": create_luxe,
        "hud": create_hud,
        "lounge": create_lounge,
    }
    for label, stem in COLLECTION.items():
        pdf_path = stem.with_suffix(".pdf")
        png_path = stem.with_suffix(".png")
        creators[label](rates, pdf_path)
        render_png(pdf_path, png_path)
        print(f"Created {pdf_path}")
        print(f"Created {png_path}")

    create_comparison_sheet()
    print(f"Created {COMPARISON_PATH}")


if __name__ == "__main__":
    main()
