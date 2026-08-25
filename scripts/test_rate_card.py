import json
import unittest
from pathlib import Path

import pdfplumber
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "outputs" / "infamous-gaming-rate-card.pdf"
PNG_PATH = ROOT / "outputs" / "infamous-gaming-rate-card.png"
RATES_PATH = ROOT / "src" / "rates.json"


def color_is(actual, expected, tolerance=0.002):
    return (
        isinstance(actual, tuple)
        and len(actual) == len(expected)
        and all(abs(channel - target) <= tolerance for channel, target in zip(actual, expected))
    )


class RateCardArtifactTests(unittest.TestCase):
    def test_reference_style_uses_a_large_neon_title_banner(self):
        with pdfplumber.open(PDF_PATH) as pdf:
            page = pdf.pages[0]
            large_lime_shapes = [
                shape
                for shape in page.curves
                if color_is(shape.get("non_stroking_color"), (200 / 255, 1.0, 46 / 255))
                and shape["width"] >= 300
                and shape["height"] >= 120
            ]

        self.assertGreaterEqual(
            len(large_lime_shapes),
            1,
            "the earlier cafe design uses a large angled neon-green title banner",
        )

    def test_reference_style_keeps_rates_in_one_open_list_not_four_tiles(self):
        with pdfplumber.open(PDF_PATH) as pdf:
            page = pdf.pages[0]
            large_dark_panels = [
                shape
                for shape in page.curves
                if color_is(shape.get("non_stroking_color"), (20 / 255, 23 / 255, 20 / 255))
                and shape["width"] >= 200
                and shape["height"] >= 150
            ]

        self.assertEqual(
            large_dark_panels,
            [],
            "pricing should read as one continuous poster list rather than four boxed cards",
        )

    def test_pdf_is_single_page_and_contains_all_confirmed_copy(self):
        self.assertTrue(PDF_PATH.exists(), "print-ready PDF should exist")

        with pdfplumber.open(PDF_PATH) as pdf:
            self.assertEqual(len(pdf.pages), 1)
            self.assertGreaterEqual(
                len(pdf.pages[0].images),
                1,
                "the original cafe logo should be embedded in the print rate card",
            )
            text = pdf.pages[0].extract_text() or ""

        for required in [
            "INFAMOUS",
            "GAMING RATE CARD",
            "CURRENT RATES",
            "HALF HOUR",
            "FULL HOUR",
            "+91 99183 32386",
            "@infamousgaming_cafe",
            "Additional charges apply for more than two players.",
        ]:
            self.assertIn(required, text)

        rates = json.loads(RATES_PATH.read_text(encoding="utf-8"))
        for group in rates:
            self.assertIn(group["category"].upper(), text.upper())
            for item in group["items"]:
                self.assertIn(item["name"], text)
                self.assertIn(f"₹{item['halfHour']}", text)
                self.assertIn(f"₹{item['fullHour']}", text)

    def test_png_is_print_resolution_a4_portrait(self):
        self.assertTrue(PNG_PATH.exists(), "high-resolution PNG should exist")

        with Image.open(PNG_PATH) as image:
            width, height = image.size

        self.assertGreaterEqual(width, 2400)
        self.assertGreaterEqual(height, 3300)
        self.assertLess(abs((width / height) - (210 / 297)), 0.02)


if __name__ == "__main__":
    unittest.main()
