import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from .mapping import (
    CAPITAL_PREFIX,
    CHAR_TO_DOTS,
    DIGIT_TO_LETTER,
    DOTS_TO_CHAR,
    LETTER_TO_DIGIT,
    NUMBER_PREFIX,
    dots_to_unicode,
    unicode_to_dots,
)


@dataclass
class BrailleCell:
    dots: Tuple[int, int, int, int, int, int]
    unicode_char: str
    latin_char: str
    confidence: float = 1.0
    bounding_box: Optional[Tuple[int, int, int, int]] = None

    def ascii_art(self) -> str:
        d = self.dots
        dot_symbols = [("●" if v else "○") for v in d]
        return f"{dot_symbols[0]} {dot_symbols[3]}\n{dot_symbols[1]} {dot_symbols[4]}\n{dot_symbols[2]} {dot_symbols[5]}"


@dataclass
class RecognitionResult:
    braille_text: str
    translated_text: str
    cell_count: int
    cells: List[BrailleCell] = field(default_factory=list)
    confidence: float = 1.0

    def to_dict(self) -> Dict:
        return {
            "braille_text": self.braille_text,
            "translated_text": self.translated_text,
            "cell_count": self.cell_count,
            "confidence": round(self.confidence, 4),
            "cells": [
                {
                    "dots": c.dots,
                    "unicode": c.unicode_char,
                    "latin": c.latin_char,
                    "confidence": c.confidence,
                }
                for c in self.cells
            ],
        }


class BrailleOCREngine:
    """
    Core Braille recognition, decoding, and translation engine.
    """

    def text_to_braille(self, text: str) -> str:
        """Convert standard Latin text to Braille Unicode."""
        result = []
        is_number_mode = False

        for ch in text:
            if ch.isupper():
                result.append(dots_to_unicode(CAPITAL_PREFIX))
                ch = ch.lower()

            if ch.isdigit():
                if not is_number_mode:
                    result.append(dots_to_unicode(NUMBER_PREFIX))
                    is_number_mode = True
                mapped_letter = DIGIT_TO_LETTER.get(ch, "a")
                dots = CHAR_TO_DOTS.get(mapped_letter, (0, 0, 0, 0, 0, 0))
                result.append(dots_to_unicode(dots))
            else:
                is_number_mode = False
                dots = CHAR_TO_DOTS.get(ch, (0, 0, 0, 0, 0, 0))
                result.append(dots_to_unicode(dots))

        return "".join(result)

    def braille_to_text(self, braille_str: str) -> RecognitionResult:
        """Decode a sequence of Braille Unicode characters into standard Latin text."""
        cells: List[BrailleCell] = []
        chars: List[str] = []

        is_capital = False
        is_number_mode = False

        for char in braille_str:
            dots = unicode_to_dots(char)

            # Check special prefixes
            if dots == CAPITAL_PREFIX:
                is_capital = True
                cells.append(BrailleCell(dots=dots, unicode_char=char, latin_char="[CAP]"))
                continue

            if dots == NUMBER_PREFIX:
                is_number_mode = True
                cells.append(BrailleCell(dots=dots, unicode_char=char, latin_char="[NUM]"))
                continue

            # Space resets number mode
            if dots == (0, 0, 0, 0, 0, 0):
                is_number_mode = False
                chars.append(" ")
                cells.append(BrailleCell(dots=dots, unicode_char=char, latin_char=" "))
                continue

            base_char = DOTS_TO_CHAR.get(dots, "?")

            if is_number_mode and base_char in LETTER_TO_DIGIT:
                resolved_char = LETTER_TO_DIGIT[base_char]
            else:
                resolved_char = base_char.upper() if is_capital else base_char
                is_capital = False

            chars.append(resolved_char)
            cells.append(BrailleCell(dots=dots, unicode_char=char, latin_char=resolved_char))

        translated_text = "".join(chars)
        return RecognitionResult(
            braille_text=braille_str,
            translated_text=translated_text,
            cell_count=len(cells),
            cells=cells,
            confidence=1.0,
        )

    def decode_dot_matrix(self, dot_matrix: List[Tuple[int, int, int, int, int, int]]) -> RecognitionResult:
        """Decode a list of raw 6-dot tuples."""
        braille_str = "".join(dots_to_unicode(d) for d in dot_matrix)
        return self.braille_to_text(braille_str)
