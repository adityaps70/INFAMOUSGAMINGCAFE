import hashlib
import json
import unittest
from pathlib import Path

import pdfplumber
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
RATES_PATH = ROOT / "src" / "rates.json"
VARIANTS = {
    "scoreboard": "infamous-gaming-rate-card-scoreboard",
    "minimal-menu": "infamous-gaming-rate-card-minimal-menu",
    "arcade-circuit": "infamous-gaming-rate-card-arcade-circuit",
}
COMPARISON_PATH = OUTPUT_DIR / "infamous-gaming-rate-card-variants-comparison.png"
ARCADE_V2_PDF = OUTPUT_DIR / "infamous-gaming-rate-card-arcade-circuit-v2.pdf"
ARCADE_V2_PNG = OUTPUT_DIR / "infamous-gaming-rate-card-arcade-circuit-v2.png"
LOGO_GREEN = (5 / 255, 230 / 255, 4 / 255)
ACCENT_RED = (1.0, 23 / 255, 23 / 255)


def color_is(actual, expected, tolerance=0.003):
    return (
        isinstance(actual, tuple)
        and len(actual) == len(expected)
        and all(abs(channel - target) <= tolerance for channel, target in zip(actual, expected))
    )


class RateCardVariantArtifactTests(unittest.TestCase):
    def test_arcade_circuit_v2_is_a_complete_print_ready_card(self):
        self.assertTrue(ARCADE_V2_PDF.exists(), "Arcade Circuit V2 PDF should exist")
        self.assertTrue(ARCADE_V2_PNG.exists(), "Arcade Circuit V2 PNG should exist")
        rates = json.loads(RATES_PATH.read_text(encoding="utf-8"))

        with pdfplumber.open(ARCADE_V2_PDF) as pdf:
            self.assertEqual(len(pdf.pages), 1)
            page = pdf.pages[0]
            self.assertGreaterEqual(len(page.images), 1)
            text = page.extract_text() or ""

        for required in [
            "INFAMOUS",
            "ARCADE CIRCUIT",
            "RATE CARD",
            "HALF HOUR",
            "FULL HOUR",
            "+91 99183 32386",
        ]:
            self.assertIn(required, text)

        for group in rates:
            self.assertIn(group["category"].upper(), text.upper())
            for item in group["items"]:
                self.assertIn(item["name"], text)
                self.assertIn(f"₹{item['halfHour']}", text)
                self.assertIn(f"₹{item['fullHour']}", text)

        with Image.open(ARCADE_V2_PNG) as image:
            width, height = image.size
        self.assertGreaterEqual(width, 2400)
        self.assertGreaterEqual(height, 3300)
        self.assertLess(abs((width / height) - (210 / 297)), 0.02)

    def test_arcade_circuit_v2_places_logo_on_a_dedicated_black_plate(self):
        self.assertTrue(ARCADE_V2_PDF.exists(), "Arcade Circuit V2 PDF should exist")
        with pdfplumber.open(ARCADE_V2_PDF) as pdf:
            page = pdf.pages[0]
            logo = page.images[0]
            logo_plates = [
                shape
                for shape in page.rects
                if color_is(shape.get("non_stroking_color"), (0, 0, 0))
                and 100 <= shape["width"] <= 180
                and 100 <= shape["height"] <= 180
                and shape["x0"] <= logo["x0"]
                and shape["x1"] >= logo["x1"]
                and shape["y0"] <= logo["y0"]
                and shape["y1"] >= logo["y1"]
            ]

        self.assertGreaterEqual(
            len(logo_plates),
            1,
            "the full logo should sit inside its own pure-black header plate",
        )

    def test_each_variant_is_a_complete_single_page_rate_card(self):
        rates = json.loads(RATES_PATH.read_text(encoding="utf-8"))

        for label, stem in VARIANTS.items():
            with self.subTest(variant=label):
                pdf_path = OUTPUT_DIR / f"{stem}.pdf"
                png_path = OUTPUT_DIR / f"{stem}.png"
                self.assertTrue(pdf_path.exists(), f"{label} PDF should exist")
                self.assertTrue(png_path.exists(), f"{label} PNG should exist")

                with pdfplumber.open(pdf_path) as pdf:
                    self.assertEqual(len(pdf.pages), 1)
                    page = pdf.pages[0]
                    self.assertGreaterEqual(len(page.images), 1)
                    text = page.extract_text() or ""
                    shapes = [*page.rects, *page.curves, *page.lines]

                for required in [
                    "INFAMOUS",
                    "RATE CARD",
                    "HALF HOUR",
                    "FULL HOUR",
                    "+91 99183 32386",
                    "Additional charges apply for more than two players.",
                ]:
                    self.assertIn(required, text)

                for group in rates:
                    self.assertIn(group["category"].upper(), text.upper())
                    for item in group["items"]:
                        self.assertIn(item["name"], text)
                        self.assertIn(f"₹{item['halfHour']}", text)
                        self.assertIn(f"₹{item['fullHour']}", text)

                self.assertTrue(
                    any(color_is(shape.get("non_stroking_color"), LOGO_GREEN) for shape in shapes),
                    f"{label} should use the green sampled from the original logo",
                )
                self.assertTrue(
                    any(
                        color_is(shape.get("non_stroking_color"), ACCENT_RED)
                        or color_is(shape.get("stroking_color"), ACCENT_RED)
                        for shape in shapes
                    ),
                    f"{label} should include visible red accents",
                )

                with Image.open(png_path) as image:
                    width, height = image.size
                self.assertGreaterEqual(width, 2400)
                self.assertGreaterEqual(height, 3300)
                self.assertLess(abs((width / height) - (210 / 297)), 0.02)

    def test_variants_are_visually_distinct(self):
        png_paths = [OUTPUT_DIR / f"{stem}.png" for stem in VARIANTS.values()]
        for png_path in png_paths:
            self.assertTrue(png_path.exists(), f"{png_path.name} should exist")

        digests = {
            hashlib.sha256(png_path.read_bytes()).hexdigest()
            for png_path in png_paths
        }
        self.assertEqual(len(digests), 3)

    def test_comparison_sheet_shows_all_three_variants_in_landscape(self):
        self.assertTrue(COMPARISON_PATH.exists(), "comparison sheet should exist")
        with Image.open(COMPARISON_PATH) as image:
            width, height = image.size
        self.assertGreater(width, height)
        self.assertGreaterEqual(width, 2400)
        self.assertGreaterEqual(height, 1000)


if __name__ == "__main__":
    unittest.main()
