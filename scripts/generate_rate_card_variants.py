import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
RATES_PATH = ROOT / "src" / "rates.json"
LOGO_PATH = ROOT / "public" / "logo.png"
COMPARISON_PATH = OUTPUT_DIR / "infamous-gaming-rate-card-variants-comparison.png"
ARCADE_V2_STEM = OUTPUT_DIR / "infamous-gaming-rate-card-arcade-circuit-v2"

VARIANTS = {
    "scoreboard": OUTPUT_DIR / "infamous-gaming-rate-card-scoreboard",
    "minimal-menu": OUTPUT_DIR / "infamous-gaming-rate-card-minimal-menu",
    "arcade-circuit": OUTPUT_DIR / "infamous-gaming-rate-card-arcade-circuit",
}

BLACK = Color(0, 0, 0)
INK = Color(10 / 255, 12 / 255, 10 / 255)
PANEL = Color(17 / 255, 20 / 255, 17 / 255)
WHITE = Color(241 / 255, 239 / 255, 231 / 255)
MUTED = Color(158 / 255, 164 / 255, 154 / 255)
GREEN = Color(5 / 255, 230 / 255, 4 / 255)
RED = Color(1, 23 / 255, 23 / 255)
LINE = Color(61 / 255, 67 / 255, 60 / 255)


def register_fonts():
    font_dir = Path("/System/Library/Fonts/Supplemental")
    font_files = {
        "ArenaDisplay": font_dir / "Arial Narrow Bold Italic.ttf",
        "ArenaBold": font_dir / "Arial Bold.ttf",
        "ArenaRegular": font_dir / "Arial.ttf",
        "ArenaCurrency": Path("/System/Library/Fonts/SFNS.ttf"),
    }
    for name, path in font_files.items():
        if not path.exists():
            raise FileNotFoundError(f"Required print font is unavailable: {path}")
        if name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name, str(path)))


def fit_font_size(text, font_name, max_size, max_width, min_size=6.5):
    size = max_size
    while size > min_size and pdfmetrics.stringWidth(text, font_name, size) > max_width:
        size -= 0.25
    return size


def draw_tracking_text(pdf, text, x, y, font_name, font_size, color, tracking=1.0):
    text_object = pdf.beginText(x, y)
    text_object.setFont(font_name, font_size)
    text_object.setFillColor(color)
    text_object.setCharSpace(tracking)
    text_object.textLine(text)
    pdf.drawText(text_object)


def start_card(path, title):
    width, height = A4
    pdf = canvas.Canvas(str(path), pagesize=A4, pageCompression=1)
    pdf.setTitle(f"inFAMOUS Gaming Cafe - {title} Rate Card")
    pdf.setAuthor("inFAMOUS Gaming Cafe")
    pdf.setSubject("Current gaming rates for inFAMOUS Gaming Cafe, Lucknow")
    pdf.setFillColor(BLACK)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)
    return pdf, width, height


def draw_logo(pdf, x, y, size):
    pdf.drawImage(
        ImageReader(str(LOGO_PATH)),
        x,
        y,
        width=size,
        height=size,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )


def draw_common_footer(pdf, width, label, band_color=GREEN):
    pdf.setFillColor(band_color)
    pdf.rect(28, 25, width - 56, 62, fill=1, stroke=0)
    pdf.setFillColor(BLACK)
    pdf.setFont("ArenaBold", 6.4)
    pdf.drawString(40, 64, "Additional charges apply for more than two players.")
    pdf.drawRightString(width - 40, 64, "CONTACT • +91 99183 32386")
    pdf.setFont("ArenaRegular", 6.1)
    pdf.drawString(40, 43, "A-1/114, Ratan Khand, Sharda Nagar, Lucknow 226012")
    pdf.drawRightString(width - 40, 43, "@infamousgaming_cafe")
    draw_tracking_text(pdf, label.upper(), 40, 30, "ArenaBold", 4.8, BLACK, 0.8)


def draw_compact_group(pdf, group, x, top, width, height, number, accent):
    bottom = top - height
    pdf.setFillColor(PANEL)
    pdf.setStrokeColor(accent)
    pdf.setLineWidth(1.2)
    pdf.rect(x, bottom, width, height, fill=1, stroke=1)

    pdf.setFillColor(accent)
    pdf.rect(x, top - 32, 42, 32, fill=1, stroke=0)
    pdf.setFillColor(BLACK)
    pdf.setFont("ArenaDisplay", 18)
    pdf.drawCentredString(x + 21, top - 23, f"0{number}")
    draw_tracking_text(
        pdf,
        group["category"].upper(),
        x + 53,
        top - 22,
        "ArenaDisplay",
        13.5,
        WHITE,
        0.25,
    )

    label_y = top - 48
    pdf.setFont("ArenaBold", 5.2)
    pdf.setFillColor(MUTED)
    pdf.drawRightString(x + width - 55, label_y, "HALF HOUR")
    pdf.drawRightString(x + width - 10, label_y, "FULL HOUR")

    row_height = (height - 59) / len(group["items"])
    for index, item in enumerate(group["items"]):
        row_top = top - 57 - (index * row_height)
        baseline = row_top - row_height * 0.62
        if index:
            pdf.setStrokeColor(LINE)
            pdf.setLineWidth(0.45)
            pdf.line(x + 12, row_top, x + width - 12, row_top)
        name_size = fit_font_size(item["name"], "ArenaBold", 9.1, width - 105)
        pdf.setFillColor(WHITE)
        pdf.setFont("ArenaBold", name_size)
        pdf.drawString(x + 12, baseline, item["name"])
        pdf.setFont("ArenaCurrency", 10.2)
        pdf.setFillColor(accent)
        pdf.drawRightString(x + width - 55, baseline - 1, f"₹{item['halfHour']}")
        pdf.setFillColor(WHITE)
        pdf.drawRightString(x + width - 10, baseline - 1, f"₹{item['fullHour']}")


def create_scoreboard(rates, path):
    pdf, width, height = start_card(path, "Tournament Scoreboard")

    pdf.setFillColor(RED)
    pdf.rect(0, height - 14, width, 14, fill=1, stroke=0)
    pdf.setFillColor(GREEN)
    pdf.rect(28, height - 125, 9, 91, fill=1, stroke=0)
    draw_tracking_text(pdf, "INFAMOUS", 53, 782, "ArenaDisplay", 29, WHITE, 0.2)
    draw_tracking_text(pdf, "TOURNAMENT SCOREBOARD", 53, 747, "ArenaDisplay", 22, GREEN, 0.15)
    draw_tracking_text(pdf, "RATE CARD • CURRENT PRICES", 54, 722, "ArenaBold", 7.2, MUTED, 1.0)
    draw_logo(pdf, width - 132, 711, 104)

    gutter = 14
    card_width = (width - 56 - gutter) / 2
    left_x = 28
    right_x = left_x + card_width + gutter
    draw_compact_group(pdf, rates[0], left_x, 680, card_width, 248, 1, GREEN)
    draw_compact_group(pdf, rates[2], left_x, 418, card_width, 202, 3, RED)
    draw_compact_group(pdf, rates[1], right_x, 680, card_width, 218, 2, RED)
    draw_compact_group(pdf, rates[3], right_x, 448, card_width, 202, 4, GREEN)

    draw_common_footer(pdf, width, "Tournament Scoreboard", band_color=RED)
    pdf.showPage()
    pdf.save()


def draw_menu_group(pdf, group, category_y, number):
    name_x = 82
    half_x = 423
    full_x = 510

    pdf.setFillColor(RED)
    pdf.circle(58, category_y + 3, 5.5, fill=1, stroke=0)
    draw_tracking_text(
        pdf,
        f"0{number}  {group['category'].upper()}",
        name_x,
        category_y,
        "ArenaDisplay",
        17,
        RED,
        0.3,
    )
    pdf.setStrokeColor(GREEN)
    pdf.setLineWidth(1)
    pdf.line(name_x, category_y - 9, 510, category_y - 9)

    baseline = category_y - 34
    for item in group["items"]:
        name_size = fit_font_size(item["name"], "ArenaBold", 11.5, 250)
        pdf.setFillColor(WHITE)
        pdf.setFont("ArenaBold", name_size)
        pdf.drawString(name_x, baseline, item["name"])
        pdf.setFont("ArenaCurrency", 12.8)
        pdf.setFillColor(GREEN)
        pdf.drawRightString(half_x, baseline - 1, f"₹{item['halfHour']}")
        pdf.setFillColor(WHITE)
        pdf.drawRightString(full_x, baseline - 1, f"₹{item['fullHour']}")
        baseline -= 24
    return baseline - 15


def create_minimal_menu(rates, path):
    pdf, width, height = start_card(path, "Minimal Cafe Menu")

    pdf.setFillColor(GREEN)
    pdf.rect(0, 0, 22, height, fill=1, stroke=0)
    pdf.setFillColor(RED)
    pdf.rect(22, 0, 6, height, fill=1, stroke=0)

    draw_logo(pdf, width - 151, 692, 122)
    draw_tracking_text(pdf, "INFAMOUS", 58, 786, "ArenaDisplay", 31, WHITE, 0.1)
    draw_tracking_text(pdf, "GAMING RATE CARD", 58, 746, "ArenaDisplay", 30, GREEN, 0.05)
    draw_tracking_text(pdf, "SIMPLE PRICES. MORE PLAY.", 60, 718, "ArenaBold", 7.3, MUTED, 1.0)

    draw_tracking_text(pdf, "HALF HOUR", 372, 672, "ArenaBold", 6.4, GREEN, 0.75)
    draw_tracking_text(pdf, "FULL HOUR", 459, 672, "ArenaBold", 6.4, GREEN, 0.75)

    category_y = 642
    for number, group in enumerate(rates, start=1):
        category_y = draw_menu_group(pdf, group, category_y, number)

    draw_common_footer(pdf, width, "Minimal Cafe Menu", band_color=GREEN)
    pdf.showPage()
    pdf.save()


def angled_panel_path(pdf, x, bottom, width, height, cut=16):
    path = pdf.beginPath()
    path.moveTo(x + cut, bottom)
    path.lineTo(x + width, bottom)
    path.lineTo(x + width, bottom + height - cut)
    path.lineTo(x + width - cut, bottom + height)
    path.lineTo(x, bottom + height)
    path.lineTo(x, bottom + cut)
    path.close()
    return path


def draw_circuit_group(pdf, group, x, top, width, height, number, accent):
    bottom = top - height
    panel = angled_panel_path(pdf, x, bottom, width, height)
    pdf.setFillColor(PANEL)
    pdf.setStrokeColor(accent)
    pdf.setLineWidth(1.2)
    pdf.drawPath(panel, fill=1, stroke=1)

    pdf.setFillColor(accent)
    pdf.circle(x + 18, top - 22, 8, fill=1, stroke=0)
    pdf.setFillColor(BLACK)
    pdf.setFont("ArenaBold", 7.5)
    pdf.drawCentredString(x + 18, top - 25, f"{number}")
    draw_tracking_text(
        pdf,
        group["category"].upper(),
        x + 36,
        top - 27,
        "ArenaDisplay",
        13.5,
        WHITE,
        0.25,
    )

    pdf.setFillColor(MUTED)
    pdf.setFont("ArenaBold", 5.1)
    pdf.drawRightString(x + width - 57, top - 49, "HALF HOUR")
    pdf.drawRightString(x + width - 13, top - 49, "FULL HOUR")

    row_height = (height - 62) / len(group["items"])
    for index, item in enumerate(group["items"]):
        baseline = top - 62 - index * row_height - row_height * 0.54
        name_size = fit_font_size(item["name"], "ArenaBold", 9.1, width - 108)
        pdf.setFillColor(WHITE)
        pdf.setFont("ArenaBold", name_size)
        pdf.drawString(x + 14, baseline, item["name"])
        pdf.setFont("ArenaCurrency", 10.1)
        pdf.setFillColor(accent)
        pdf.drawRightString(x + width - 57, baseline - 1, f"₹{item['halfHour']}")
        pdf.setFillColor(WHITE)
        pdf.drawRightString(x + width - 13, baseline - 1, f"₹{item['fullHour']}")

    pdf.setStrokeColor(accent)
    pdf.setLineWidth(1.2)
    pdf.line(x + width - 33, bottom + 7, x + width - 9, bottom + 7)
    pdf.line(x + width - 9, bottom + 7, x + width - 9, bottom + 26)


def create_arcade_circuit(rates, path):
    pdf, width, height = start_card(path, "Arcade Circuit")

    pdf.setStrokeColor(Color(5 / 255, 230 / 255, 4 / 255, alpha=0.09))
    pdf.setLineWidth(0.4)
    for grid_x in range(0, int(width) + 1, 24):
        pdf.line(grid_x, 0, grid_x, height)
    for grid_y in range(0, int(height) + 1, 24):
        pdf.line(0, grid_y, width, grid_y)

    pdf.setFillColor(RED)
    header_band = pdf.beginPath()
    header_band.moveTo(0, 842)
    header_band.lineTo(440, 842)
    header_band.lineTo(400, 706)
    header_band.lineTo(0, 706)
    header_band.close()
    pdf.drawPath(header_band, fill=1, stroke=0)
    draw_logo(pdf, 35, 720, 105)
    draw_tracking_text(pdf, "ARCADE CIRCUIT", 152, 786, "ArenaDisplay", 28, BLACK, 0.1)
    draw_tracking_text(pdf, "INFAMOUS RATE CARD", 152, 746, "ArenaDisplay", 23, BLACK, 0.15)
    draw_tracking_text(pdf, "CHOOSE MODE • CHECK PRICE • PLAY", 153, 721, "ArenaBold", 6.4, BLACK, 0.9)

    pdf.setFillColor(GREEN)
    pdf.circle(width - 76, 772, 20, fill=1, stroke=0)
    pdf.setFillColor(BLACK)
    pdf.setFont("ArenaDisplay", 16)
    pdf.drawCentredString(width - 76, 766, "ON")
    pdf.setStrokeColor(GREEN)
    pdf.setLineWidth(3)
    pdf.line(width - 76, 752, width - 76, 706)
    pdf.line(width - 76, 706, width - 116, 706)

    gutter = 14
    panel_width = (width - 56 - gutter) / 2
    left_x = 28
    right_x = left_x + panel_width + gutter
    draw_circuit_group(pdf, rates[0], left_x, 680, panel_width, 246, 1, GREEN)
    draw_circuit_group(pdf, rates[1], right_x, 680, panel_width, 214, 2, RED)
    draw_circuit_group(pdf, rates[2], left_x, 416, panel_width, 205, 3, RED)
    draw_circuit_group(pdf, rates[3], right_x, 448, panel_width, 205, 4, GREEN)

    draw_common_footer(pdf, width, "Arcade Circuit", band_color=RED)
    pdf.showPage()
    pdf.save()


def draw_circuit_route(pdf, width):
    """Draw a restrained route that visually connects the four pricing zones."""
    route = Color(5 / 255, 230 / 255, 4 / 255, alpha=0.22)
    junction_x = width / 2
    pdf.setStrokeColor(route)
    pdf.setLineWidth(1.2)
    pdf.line(junction_x, 642, junction_x, 160)
    pdf.line(junction_x - 24, 642, junction_x + 24, 642)
    pdf.line(junction_x - 24, 417, junction_x + 24, 417)
    pdf.line(junction_x - 24, 160, junction_x + 24, 160)

    for y, color in ((642, GREEN), (417, RED), (160, GREEN)):
        pdf.setFillColor(BLACK)
        pdf.setStrokeColor(color)
        pdf.setLineWidth(1.3)
        pdf.circle(junction_x, y, 4.2, fill=1, stroke=1)


def draw_arcade_v2_group(pdf, group, x, top, width, height, number, accent):
    bottom = top - height
    panel = angled_panel_path(pdf, x, bottom, width, height, cut=12)
    pdf.setFillColor(Color(14 / 255, 17 / 255, 14 / 255))
    pdf.setStrokeColor(accent)
    pdf.setLineWidth(1.05)
    pdf.drawPath(panel, fill=1, stroke=1)

    # Compact terminal-style category header.
    pdf.setFillColor(accent)
    pdf.rect(x + 12, top - 39, 36, 27, fill=1, stroke=0)
    pdf.setFillColor(BLACK)
    pdf.setFont("ArenaDisplay", 14)
    pdf.drawCentredString(x + 30, top - 32, f"0{number}")
    category_size = fit_font_size(
        group["category"].upper(),
        "ArenaDisplay",
        15.5,
        width - 67,
        min_size=11,
    )
    draw_tracking_text(
        pdf,
        group["category"].upper(),
        x + 58,
        top - 33,
        "ArenaDisplay",
        category_size,
        WHITE,
        0.18,
    )

    header_y = top - 58
    pdf.setStrokeColor(Color(1, 1, 1, alpha=0.12))
    pdf.setLineWidth(0.5)
    pdf.line(x + 12, header_y - 6, x + width - 12, header_y - 6)
    pdf.setFillColor(MUTED)
    pdf.setFont("ArenaBold", 5.7)
    pdf.drawRightString(x + width - 61, header_y, "HALF HOUR")
    pdf.drawRightString(x + width - 13, header_y, "FULL HOUR")

    row_area = height - 77
    row_height = row_area / len(group["items"])
    for index, item in enumerate(group["items"]):
        row_top = header_y - 9 - index * row_height
        baseline = row_top - row_height * 0.62
        if index:
            pdf.setStrokeColor(Color(1, 1, 1, alpha=0.08))
            pdf.setLineWidth(0.4)
            pdf.line(x + 13, row_top, x + width - 13, row_top)

        name_size = fit_font_size(item["name"], "ArenaBold", 10.1, width - 118, min_size=7.5)
        pdf.setFillColor(WHITE)
        pdf.setFont("ArenaBold", name_size)
        pdf.drawString(x + 14, baseline, item["name"])
        pdf.setFont("ArenaCurrency", 10.8)
        pdf.setFillColor(accent)
        pdf.drawRightString(x + width - 61, baseline - 1, f"₹{item['halfHour']}")
        pdf.setFillColor(WHITE)
        pdf.drawRightString(x + width - 13, baseline - 1, f"₹{item['fullHour']}")

    # Small route terminal makes each panel feel connected without adding clutter.
    pdf.setStrokeColor(accent)
    pdf.setLineWidth(1.15)
    pdf.line(x + width - 32, bottom + 8, x + width - 10, bottom + 8)
    pdf.line(x + width - 10, bottom + 8, x + width - 10, bottom + 23)
    pdf.setFillColor(accent)
    pdf.circle(x + width - 10, bottom + 23, 2.2, fill=1, stroke=0)


def draw_arcade_v2_footer(pdf, width):
    footer_x = 28
    footer_y = 25
    footer_width = width - 56
    footer_height = 103

    pdf.setFillColor(BLACK)
    pdf.setStrokeColor(RED)
    pdf.setLineWidth(1.2)
    pdf.rect(footer_x, footer_y, footer_width, footer_height, fill=1, stroke=1)
    pdf.setFillColor(RED)
    pdf.rect(footer_x, footer_y + footer_height - 6, footer_width, 6, fill=1, stroke=0)

    pdf.setFillColor(GREEN)
    pdf.rect(footer_x + footer_width - 188, footer_y, 188, footer_height - 6, fill=1, stroke=0)
    pdf.setFillColor(BLACK)
    draw_tracking_text(
        pdf,
        "BOOK YOUR SESSION",
        footer_x + footer_width - 170,
        footer_y + 66,
        "ArenaBold",
        7.1,
        BLACK,
        0.65,
    )
    pdf.setFont("ArenaCurrency", 17)
    pdf.drawString(footer_x + footer_width - 170, footer_y + 39, "+91 99183 32386")
    pdf.setFont("ArenaBold", 6.2)
    pdf.drawString(footer_x + footer_width - 170, footer_y + 18, "CALL OR WHATSAPP")

    left_x = footer_x + 15
    pdf.setFillColor(WHITE)
    pdf.setFont("ArenaBold", 7.2)
    pdf.drawString(left_x, footer_y + 77, "Additional charges apply for more than two players.")
    pdf.setFillColor(MUTED)
    pdf.setFont("ArenaRegular", 6.5)
    pdf.drawString(left_x, footer_y + 52, "A-1/114, Ratan Khand, Sharda Nagar")
    pdf.drawString(left_x, footer_y + 39, "Lucknow, Uttar Pradesh 226012")
    pdf.setFillColor(GREEN)
    pdf.setFont("ArenaBold", 6.8)
    pdf.drawString(left_x, footer_y + 17, "@infamousgaming_cafe")


def create_arcade_circuit_v2(rates, path):
    pdf, width, height = start_card(path, "Arcade Circuit V2")

    # Softer grid: atmosphere only, never competition for the rate table.
    pdf.setStrokeColor(Color(5 / 255, 230 / 255, 4 / 255, alpha=0.045))
    pdf.setLineWidth(0.35)
    for grid_x in range(0, int(width) + 1, 24):
        pdf.line(grid_x, 0, grid_x, height)
    for grid_y in range(0, int(height) + 1, 24):
        pdf.line(0, grid_y, width, grid_y)

    # The title wedge begins after the plate: red never sits behind the logo.
    header_band = pdf.beginPath()
    header_band.moveTo(184, height)
    header_band.lineTo(width, height)
    header_band.lineTo(width, 694)
    header_band.lineTo(215, 694)
    header_band.close()
    pdf.setFillColor(RED)
    pdf.drawPath(header_band, fill=1, stroke=0)
    pdf.setFillColor(GREEN)
    pdf.rect(215, 694, width - 215, 5, fill=1, stroke=0)

    # Dedicated pure-black plate guarantees consistent logo contrast in print.
    plate_x, plate_y, plate_width, plate_height = 28, 694, 145, 130
    pdf.setFillColor(BLACK)
    pdf.setStrokeColor(GREEN)
    pdf.setLineWidth(1.4)
    pdf.rect(plate_x, plate_y, plate_width, plate_height, fill=1, stroke=1)
    pdf.setStrokeColor(RED)
    pdf.setLineWidth(1)
    pdf.line(plate_x + 18, plate_y, plate_x + plate_width, plate_y)
    pdf.line(plate_x + plate_width, plate_y, plate_x + plate_width, plate_y + 42)
    draw_logo(pdf, plate_x + 15, plate_y + 8, 114)

    draw_tracking_text(pdf, "ARCADE CIRCUIT", 225, 788, "ArenaDisplay", 29, BLACK, 0.1)
    draw_tracking_text(pdf, "INFAMOUS RATE CARD", 225, 749, "ArenaDisplay", 23, BLACK, 0.12)
    draw_tracking_text(
        pdf,
        "SELECT YOUR ARENA  /  CHECK YOUR TIME  /  PLAY",
        226,
        720,
        "ArenaBold",
        6.1,
        BLACK,
        0.72,
    )
    pdf.setFillColor(GREEN)
    pdf.circle(width - 45, 720, 9, fill=1, stroke=0)
    pdf.setFillColor(BLACK)
    pdf.setFont("ArenaDisplay", 7.4)
    pdf.drawCentredString(width - 45, 717.3, "ON")

    draw_circuit_route(pdf, width)
    gutter = 18
    panel_width = (width - 56 - gutter) / 2
    left_x = 28
    right_x = left_x + panel_width + gutter
    panel_height = 250
    draw_arcade_v2_group(pdf, rates[0], left_x, 674, panel_width, panel_height, 1, GREEN)
    draw_arcade_v2_group(pdf, rates[1], right_x, 674, panel_width, panel_height, 2, RED)
    draw_arcade_v2_group(pdf, rates[2], left_x, 410, panel_width, panel_height, 3, RED)
    draw_arcade_v2_group(pdf, rates[3], right_x, 410, panel_width, panel_height, 4, GREEN)

    draw_arcade_v2_footer(pdf, width)
    pdf.showPage()
    pdf.save()


def render_png(pdf_path, png_path):
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        raise FileNotFoundError("pdftoppm is required to render rate-card PNGs")
    subprocess.run(
        [
            pdftoppm,
            "-singlefile",
            "-r",
            "300",
            "-png",
            str(pdf_path),
            str(png_path.with_suffix("")),
        ],
        check=True,
    )


def create_comparison_sheet():
    thumbnails = []
    target_height = 1100
    for label, stem in VARIANTS.items():
        image = Image.open(stem.with_suffix(".png")).convert("RGB")
        target_width = round(image.width * (target_height / image.height))
        thumbnails.append((label, image.resize((target_width, target_height), Image.Resampling.LANCZOS)))

    margin = 70
    gap = 65
    title_height = 150
    label_height = 90
    width = margin * 2 + sum(image.width for _, image in thumbnails) + gap * 2
    height = margin + title_height + target_height + label_height + margin
    sheet = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(sheet)
    title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 48)
    label_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
    small_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)

    draw.text((margin, margin), "INFAMOUS RATE CARD VARIANTS", font=title_font, fill=(5, 230, 4))
    draw.text(
        (margin, margin + 66),
        "Same confirmed rates • logo green #05E604 • stronger red card accents",
        font=small_font,
        fill=(220, 220, 214),
    )

    x = margin
    labels = {
        "scoreboard": "01  TOURNAMENT SCOREBOARD",
        "minimal-menu": "02  MINIMAL CAFE MENU",
        "arcade-circuit": "03  ARCADE CIRCUIT",
    }
    for index, (label, image) in enumerate(thumbnails):
        border = (255, 23, 23) if index != 1 else (5, 230, 4)
        y = margin + title_height
        draw.rectangle((x - 5, y - 5, x + image.width + 5, y + image.height + 5), outline=border, width=5)
        sheet.paste(image, (x, y))
        draw.text((x, y + image.height + 25), labels[label], font=label_font, fill=border)
        x += image.width + gap

    sheet.save(COMPARISON_PATH, quality=95)


def main():
    register_fonts()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not LOGO_PATH.exists():
        raise FileNotFoundError(f"Enhanced cafe logo is unavailable: {LOGO_PATH}")

    rates = json.loads(RATES_PATH.read_text(encoding="utf-8"))
    if len(rates) != 4:
        raise ValueError("Variant layouts expect exactly four pricing groups")

    creators = {
        "scoreboard": create_scoreboard,
        "minimal-menu": create_minimal_menu,
        "arcade-circuit": create_arcade_circuit,
    }
    for label, stem in VARIANTS.items():
        pdf_path = stem.with_suffix(".pdf")
        png_path = stem.with_suffix(".png")
        creators[label](rates, pdf_path)
        render_png(pdf_path, png_path)
        print(f"Created {pdf_path}")
        print(f"Created {png_path}")

    arcade_v2_pdf = ARCADE_V2_STEM.with_suffix(".pdf")
    arcade_v2_png = ARCADE_V2_STEM.with_suffix(".png")
    create_arcade_circuit_v2(rates, arcade_v2_pdf)
    render_png(arcade_v2_pdf, arcade_v2_png)
    print(f"Created {arcade_v2_pdf}")
    print(f"Created {arcade_v2_png}")

    create_comparison_sheet()
    print(f"Created {COMPARISON_PATH}")


if __name__ == "__main__":
    main()
