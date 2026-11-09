"""Unit tests for CAU Design System & Token Extractor."""

import unittest
from pathlib import Path
import sys

# Ensure scripts directory is in sys.path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from extract_design_tokens import (
    parse_hex_color,
    calculate_luminance,
    categorize_color,
    clean_font_family,
    extract_tokens_from_css,
)


class TestDesignTokenExtractor(unittest.TestCase):
    def test_parse_hex_color_standard(self):
        self.assertEqual(parse_hex_color("#ffffff"), (255, 255, 255))
        self.assertEqual(parse_hex_color("#000000"), (0, 0, 0))
        self.assertEqual(parse_hex_color("#ff0000"), (255, 0, 0))
        self.assertEqual(parse_hex_color("#00ff00"), (0, 255, 0))
        self.assertEqual(parse_hex_color("#0000ff"), (0, 0, 255))

    def test_parse_hex_color_shorthand(self):
        self.assertEqual(parse_hex_color("#fff"), (255, 255, 255))
        self.assertEqual(parse_hex_color("#000"), (0, 0, 0))
        self.assertEqual(parse_hex_color("#f00"), (255, 0, 0))

    def test_calculate_luminance(self):
        white_lum = calculate_luminance(255, 255, 255)
        black_lum = calculate_luminance(0, 0, 0)
        self.assertAlmostEqual(white_lum, 1.0, places=2)
        self.assertAlmostEqual(black_lum, 0.0, places=2)

    def test_categorize_color(self):
        self.assertEqual(categorize_color("#ffffff"), "background-light")
        self.assertEqual(categorize_color("#000000"), "text-dark")
        self.assertEqual(categorize_color("#3b82f6"), "accent")
        self.assertEqual(categorize_color("#71717a"), "neutral")

    def test_clean_font_family(self):
        raw = "'Plus Jakarta Sans', \"Inter\", sans-serif"
        cleaned = clean_font_family(raw)
        self.assertEqual(cleaned, "Plus Jakarta Sans, Inter, sans-serif")

    def test_extract_tokens_from_css(self):
        sample_css = """
        :root {
            --primary: #3b82f6;
            --background: #09090b;
        }
        body {
            font-family: 'Inter', system-ui, sans-serif;
            color: #ffffff;
            background-color: #09090b;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        """
        tokens = extract_tokens_from_css(sample_css)
        self.assertIn("--primary", tokens.get("cssVariables", {}))
        self.assertEqual(tokens["cssVariables"]["--primary"], "#3b82f6")
        self.assertIn("Inter, system-ui, sans-serif", tokens.get("typography", {}).get("fontFamilies", []))
        self.assertIn("12px", tokens.get("shape", {}).get("borderRadii", []))


if __name__ == "__main__":
    unittest.main()
