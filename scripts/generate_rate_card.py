import json
import shutil
import subprocess
from pathlib import Path

from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
RATES_PATH = ROOT / "src" / "rates.json"
OUTPUT_DIR = ROOT / "outputs"
PDF_PATH = OUTPUT_DIR / "infamous-gaming-rate-card.pdf"
PNG_PATH = OUTPUT_DIR / "infamous-gaming-rate-card.png"
LOGO_PATH = ROOT / "public" / "logo.png"

BLACK = Color(0, 0, 0)
INK = Color(11 / 255, 13 / 255, 12 / 255)
PAPER = Color(241 / 255, 239 / 255, 231 / 255)
MUTED = Color(166 / 255, 171 / 255, 159 / 255)
LIME = Color(200 / 255, 255 / 255, 46 / 255)
RED = Color(255 / 255, 23 / 255, 23 / 255)
LINE = Color(63 / 255, 68 / 255, 62 / 255)


def register_fonts():
    font_dir = Path("/System/Library/Fonts/Supplemental")
    font_files = {
        "ArenaDisplay": font_dir / "Arial Narrow Bold Italic.ttf",
        "ArenaBold": font_dir / "Arial Bold.ttf",
        "ArenaRegular": font_dir / "Arial.ttf",
        "ArenaUnicode": font_dir / "Arial Unicode.ttf",
        "ArenaCurrency": Path("/System/Library/Fonts/SFNS.ttf"),
    }

    missing = [str(path) for path in font_files.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Required print fonts are unavailable: {missing}")

    for name, path in font_files.items():
        pdfmetrics.registerFont(TTFont(name, str(path)))


def fit_font_size(text, font_name, max_size, max_width, min_size=8):
    size = max_size
    while size > min_size and pdfmetrics.stringWidth(text, font_name, size) > max_width:
        size -= 0.25
    return size


def draw_tracking_text(pdf, text, x, y, font_name, font_size, color, tracking=1.2):
    text_object = pdf.beginText(x, y)
    text_object.setFont(font_name, font_size)
    text_object.setFillColor(color)
    text_object.setCharSpace(tracking)
    text_object.textLine(text)
    pdf.drawText(text_object)


def draw_rate_list_group(pdf, group, category_y):
    name_x = 68
    half_price_x = 416
    slash_x = 438
    full_price_x = 500

    draw_tracking_text(
        pdf,
        group["category"].upper(),
        name_x,
        category_y,
        "ArenaDisplay",
        18,
        LIME,
        tracking=0.35,
    )

    pdf.setStrokeColor(RED)
    pdf.setLineWidth(2)
    pdf.line(name_x, category_y - 7, name_x + 24, category_y - 7)

    baseline = category_y - 31
    for item in group["items"]:
        name_size = fit_font_size(item["name"], "ArenaBold", 11.2, 250)
        pdf.setFillColor(PAPER)
        pdf.setFont("ArenaBold", name_size)
        pdf.drawString(name_x, baseline, item["name"])

        pdf.setFont("ArenaCurrency", 12.6)
        pdf.drawRightString(half_price_x, baseline - 1, f"₹{item['halfHour']}")
        pdf.setFillColor(RED)
        pdf.setFont("ArenaBold", 10)
        pdf.drawCentredString(slash_x, baseline, "/")
        pdf.setFillColor(PAPER)
        pdf.setFont("ArenaCurrency", 12.6)
        pdf.drawRightString(full_price_x, baseline - 1, f"₹{item['fullHour']}")
        baseline -= 24

    return baseline - 14


def draw_route_marks(pdf):
    pdf.setStrokeColor(PAPER)
    pdf.setLineWidth(6)
    pdf.setLineCap(1)

    upper = pdf.beginPath()
    upper.moveTo(552, 515)
    upper.curveTo(513, 493, 506, 448, 531, 414)
    pdf.drawPath(upper, fill=0, stroke=1)
    pdf.line(531, 414, 514, 423)
    pdf.line(531, 414, 529, 434)

    pdf.circle(528, 345, 16, fill=0, stroke=1)

    lower = pdf.beginPath()
    lower.moveTo(552, 296)
    lower.curveTo(510, 287, 504, 254, 526, 226)
    pdf.drawPath(lower, fill=0, stroke=1)
    pdf.line(526, 226, 508, 234)
    pdf.line(526, 226, 524, 246)

    pdf.setLineCap(0)


def create_pdf(rates):
    register_fonts()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not LOGO_PATH.exists():
        raise FileNotFoundError(f"Enhanced cafe logo is unavailable: {LOGO_PATH}")

    width, height = A4
    pdf = canvas.Canvas(str(PDF_PATH), pagesize=A4, pageCompression=1)
    pdf.setTitle("inFAMOUS Gaming Cafe - Current Rate Card")
    pdf.setAuthor("inFAMOUS Gaming Cafe")
    pdf.setSubject("Current gaming rates for inFAMOUS Gaming Cafe, Lucknow")

    pdf.setFillColor(BLACK)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)

    margin = 36

    # The original cafe card used one oversized neon title block rather than
    # a conventional document header. Keep that silhouette, but render it
    # precisely for A4 printing.
    title_banner = pdf.beginPath()
    title_banner.moveTo(margin, 812)
    title_banner.lineTo(394, 812)
    title_banner.lineTo(350, 657)
    title_banner.lineTo(margin, 657)
    title_banner.close()
    pdf.setFillColor(LIME)
    pdf.drawPath(title_banner, fill=1, stroke=0)

    draw_tracking_text(pdf, "INFAMOUS", 58, 762, "ArenaDisplay", 35, BLACK, 0.1)
    draw_tracking_text(pdf, "GAMING", 58, 716, "ArenaDisplay", 35, BLACK, 0.1)
    draw_tracking_text(pdf, "RATE CARD", 58, 670, "ArenaDisplay", 35, BLACK, 0.1)

    logo_size = 150
    pdf.drawImage(
        ImageReader(str(LOGO_PATH)),
        width - margin - logo_size,
        676,
        width=logo_size,
        height=logo_size,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )

    pdf.setFillColor(RED)
    pdf.rect(margin, 635, 7, 7, fill=1, stroke=0)
    draw_tracking_text(
        pdf,
        "CURRENT RATES • GAMING RATE CARD • LUCKNOW",
        margin + 15,
        635,
        "ArenaBold",
        6.6,
        MUTED,
        0.7,
    )

    draw_tracking_text(pdf, "HALF HOUR", 363, 615, "ArenaBold", 6.3, LIME, 0.7)
    draw_tracking_text(pdf, "FULL HOUR", 447, 615, "ArenaBold", 6.3, LIME, 0.7)

    category_y = 588
    for group in rates:
        category_y = draw_rate_list_group(pdf, group, category_y)

    # Tall neon rail and hand-drawn play-route marks echo the laminated cafe
    # card without copying its rough print artifacts.
    pdf.setFillColor(LIME)
    pdf.rect(538, 106, 27, 468, fill=1, stroke=0)
    draw_route_marks(pdf)

    footer_y = 27
    footer_height = 64
    pdf.setFillColor(LIME)
    pdf.rect(28, footer_y, width - 56, footer_height, fill=1, stroke=0)

    pdf.setFillColor(BLACK)
    pdf.setFont("ArenaBold", 6.5)
    pdf.drawString(40, footer_y + 40, "Additional charges apply for more than two players.")
    pdf.drawRightString(width - 40, footer_y + 40, "CONTACT • +91 99183 32386")

    pdf.setFont("ArenaRegular", 6.2)
    pdf.drawString(40, footer_y + 19, "A-1/114, Ratan Khand, Sharda Nagar, Lucknow 226012")
    pdf.drawRightString(width - 40, footer_y + 19, "@infamousgaming_cafe")

    pdf.setStrokeColor(RED)
    pdf.setLineWidth(2)
    pdf.line(28, footer_y + footer_height, 88, footer_y + footer_height)
    pdf.line(width - 88, 826, width - 28, 826)

    pdf.showPage()
    pdf.save()


def render_png():
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        raise FileNotFoundError("pdftoppm is required to create the print-resolution PNG")

    output_prefix = PNG_PATH.with_suffix("")
    subprocess.run(
        [
            pdftoppm,
            "-singlefile",
            "-r",
            "300",
            "-png",
            str(PDF_PATH),
            str(output_prefix),
        ],
        check=True,
    )


def main():
    rates = json.loads(RATES_PATH.read_text(encoding="utf-8"))
    if len(rates) != 4:
        raise ValueError("The rate card layout expects exactly four pricing groups")

    create_pdf(rates)
    render_png()
    print(f"Created {PDF_PATH}")
    print(f"Created {PNG_PATH}")


if __name__ == "__main__":
    main()
