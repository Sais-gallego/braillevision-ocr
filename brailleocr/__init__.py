"""
BrailleVision-OCR: Computer Vision Braille Recognition & Text-to-Speech Engine.
"""

__version__ = "1.0.0"
__author__ = "Sais-gallego"

from .mapping import BRAILLE_TO_CHAR, CHAR_TO_BRAILLE, BRAILLE_UNICODE_OFFSET
from .engine import BrailleCell, BrailleOCREngine, RecognitionResult

__all__ = [
    "BRAILLE_TO_CHAR",
    "CHAR_TO_BRAILLE",
    "BRAILLE_UNICODE_OFFSET",
    "BrailleCell",
    "BrailleOCREngine",
    "RecognitionResult",
]
