import hashlib
import json
import unittest
from pathlib import Path

import pdfplumber
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
RATES_PATH = ROOT / "src" / "rates.json"

COLLECTION = {
    "luxe": OUTPUT_DIR / "infamous-gaming-rate-card-premium-luxe",
    "hud": OUTPUT_DIR / "infamous-gaming-rate-card-premium-hud",
    "lounge": OUTPUT_DIR / "infamous-gaming-rate-card-premium-lounge",
}
COMPARISON_PATH = OUTPUT_DIR / "infamous-gaming-premium-rate-card-collection.png"
LOGO_GREEN = (5 / 255, 230 / 255, 4 / 255)
ACCENT_RED = (1.0, 23 / 255, 23 / 255)
OPTION_LABELS = [
    "CONSOLE",
    "PC",
    "BILLIARDS",
    "RACING",
    "TABLE SPORTS",
    "BOARD GAMES",
]


def color_is(actual, expected, tolerance=0.003):
    return (
        isinstance(actual, tuple)
        and len(actual) == len(expected)
        and all(abs(channel - target) <= tolerance for channel, target in zip(actual, expected))
    )


class PremiumRateCardCollectionTests(unittest.TestCase):
    def test_each_card_is_a_complete_a4_rate_card(self):
        rates = json.loads(RATES_PATH.read_text(encoding="utf-8"))

        for label, stem in COLLECTION.items():
            with self.subTest(card=label):
                pdf_path = stem.with_suffix(".pdf")
                png_path = stem.with_suffix(".png")
                self.assertTrue(pdf_path.exists(), f"{label} PDF should exist")
                self.assertTrue(png_path.exists(), f"{label} PNG should exist")

                with pdfplumber.open(pdf_path) as pdf:
                    self.assertEqual(len(pdf.pages), 1)
                    page = pdf.pages[0]
                    text = page.extract_text() or ""
                    self.assertGreaterEqual(len(page.images), 1)

                for required in [
                    "INFAMOUS",
                    "RATE CARD",
                    "HALF HOUR",
                    "FULL HOUR",
                    "+91 99183 32386",
                    "Additional charges apply for more than two players.",
                    *OPTION_LABELS,
                ]:
                    self.assertIn(required, text)

                for group in rates:
                    self.assertIn(group["category"].upper(), text.upper())
                    for item in group["items"]:
                        self.assertIn(item["name"], text)
                        self.assertIn(f"₹{item['halfHour']}", text)
                        self.assertIn(f"₹{item['fullHour']}", text)

                with Image.open(png_path) as image:
                    width, height = image.size
                self.assertGreaterEqual(width, 2400)
                self.assertGreaterEqual(height, 3300)
                self.assertLess(abs((width / height) - (210 / 297)), 0.02)

    def test_each_logo_is_contained_by_a_pure_black_plate(self):
        for label, stem in COLLECTION.items():
            with self.subTest(card=label):
                pdf_path = stem.with_suffix(".pdf")
                self.assertTrue(pdf_path.exists(), f"{label} PDF should exist")
                pdf = pdfplumber.open(pdf_path)
                self.addCleanup(pdf.close)
                page = pdf.pages[0]
                logo = page.images[0]
                plates = [
                    rect
                    for rect in page.rects
                    if color_is(rect.get("non_stroking_color"), (0, 0, 0))
                    and 90 <= rect["width"] <= 200
                    and 70 <= rect["height"] <= 180
                    and rect["x0"] <= logo["x0"]
                    and rect["x1"] >= logo["x1"]
                    and rect["y0"] <= logo["y0"]
                    and rect["y1"] >= logo["y1"]
                ]
                self.assertGreaterEqual(len(plates), 1)

    def test_each_card_uses_the_logo_green_red_accents_and_vector_art(self):
        for label, stem in COLLECTION.items():
            with self.subTest(card=label):
                pdf_path = stem.with_suffix(".pdf")
                self.assertTrue(pdf_path.exists(), f"{label} PDF should exist")
                pdf = pdfplumber.open(pdf_path)
                self.addCleanup(pdf.close)
                page = pdf.pages[0]
                shapes = [*page.rects, *page.curves, *page.lines]
                self.assertTrue(
                    any(color_is(shape.get("non_stroking_color"), LOGO_GREEN) for shape in shapes)
                )
                self.assertTrue(
                    any(
                        color_is(shape.get("non_stroking_color"), ACCENT_RED)
                        or color_is(shape.get("stroking_color"), ACCENT_RED)
                        for shape in shapes
                    )
                )
                self.assertGreaterEqual(
                    len(page.curves) + len(page.lines),
                    25,
                    "each premium card should include substantial vector gaming artwork",
                )

    def test_three_cards_are_visually_distinct_and_compared_side_by_side(self):
        png_paths = [stem.with_suffix(".png") for stem in COLLECTION.values()]
        for path in png_paths:
            self.assertTrue(path.exists())

        digests = {hashlib.sha256(path.read_bytes()).hexdigest() for path in png_paths}
        self.assertEqual(len(digests), 3)

        self.assertTrue(COMPARISON_PATH.exists())
        with Image.open(COMPARISON_PATH) as image:
            width, height = image.size
        self.assertGreater(width, height)
        self.assertGreaterEqual(width, 2400)
        self.assertGreaterEqual(height, 1000)

    def test_lounge_billiards_watermark_does_not_inherit_bright_logo_green(self):
        lounge_pdf = COLLECTION["lounge"].with_suffix(".pdf")
        self.assertTrue(lounge_pdf.exists())

        with pdfplumber.open(lounge_pdf) as pdf:
            watermark_eights = [
                char
                for char in pdf.pages[0].chars
                if char["text"] == "8"
                and char["x0"] < 120
                and 270 < char["y0"] < 350
            ]

        self.assertGreaterEqual(len(watermark_eights), 1)
        self.assertTrue(
            all(
                not color_is(char.get("non_stroking_color"), LOGO_GREEN)
                for char in watermark_eights
            ),
            "the decorative 8-ball watermark should remain subtle",
        )


if __name__ == "__main__":
    unittest.main()
