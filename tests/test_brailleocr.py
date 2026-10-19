import unittest
from brailleocr.engine import BrailleOCREngine
from brailleocr.mapping import dots_to_unicode, unicode_to_dots


class TestBrailleOCR(unittest.TestCase):
    def setUp(self):
        self.engine = BrailleOCREngine()

    def test_dots_and_unicode_roundtrip(self):
        dots = (1, 0, 1, 1, 0, 0)  # 'm'
        u_char = dots_to_unicode(dots)
        self.assertEqual(u_char, "⠍")
        recovered = unicode_to_dots(u_char)
        self.assertEqual(dots, recovered)

    def test_alphabet_translation(self):
        text = "hello world"
        braille_str = self.engine.text_to_braille(text)
        result = self.engine.braille_to_text(braille_str)
        self.assertEqual(result.translated_text, text)

    def test_capital_letters(self):
        text = "GitHub"
        braille_str = self.engine.text_to_braille(text)
        result = self.engine.braille_to_text(braille_str)
        self.assertEqual(result.translated_text, text)

    def test_numeric_encoding_and_decoding(self):
        text = "code 123"
        braille_str = self.engine.text_to_braille(text)
        result = self.engine.braille_to_text(braille_str)
        self.assertEqual(result.translated_text, text)

    def test_cell_ascii_art(self):
        res = self.engine.braille_to_text("⠁")
        self.assertEqual(len(res.cells), 1)
        ascii_art = res.cells[0].ascii_art()
        self.assertIn("●", ascii_art)
        self.assertIn("○", ascii_art)


if __name__ == "__main__":
    unittest.main()
