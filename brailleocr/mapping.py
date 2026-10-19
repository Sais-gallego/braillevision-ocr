from typing import Dict, Optional, Tuple

BRAILLE_UNICODE_OFFSET = 0x2800

# 6-dot bit representation: (dot1, dot2, dot3, dot4, dot5, dot6)
CHAR_TO_DOTS: Dict[str, Tuple[int, int, int, int, int, int]] = {
    # Alphabet
    "a": (1, 0, 0, 0, 0, 0),
    "b": (1, 1, 0, 0, 0, 0),
    "c": (1, 0, 0, 1, 0, 0),
    "d": (1, 0, 0, 1, 1, 0),
    "e": (1, 0, 0, 0, 1, 0),
    "f": (1, 1, 0, 1, 0, 0),
    "g": (1, 1, 0, 1, 1, 0),
    "h": (1, 1, 0, 0, 1, 0),
    "i": (0, 1, 0, 1, 0, 0),
    "j": (0, 1, 0, 1, 1, 0),
    "k": (1, 0, 1, 0, 0, 0),
    "l": (1, 1, 1, 0, 0, 0),
    "m": (1, 0, 1, 1, 0, 0),
    "n": (1, 0, 1, 1, 1, 0),
    "o": (1, 0, 1, 0, 1, 0),
    "p": (1, 1, 1, 1, 0, 0),
    "q": (1, 1, 1, 1, 1, 0),
    "r": (1, 1, 1, 0, 1, 0),
    "s": (0, 1, 1, 1, 0, 0),
    "t": (0, 1, 1, 1, 1, 0),
    "u": (1, 0, 1, 0, 0, 1),
    "v": (1, 1, 1, 0, 0, 1),
    "w": (0, 1, 0, 1, 1, 1),
    "x": (1, 0, 1, 1, 0, 1),
    "y": (1, 0, 1, 1, 1, 1),
    "z": (1, 0, 1, 0, 1, 1),
    # Space
    " ": (0, 0, 0, 0, 0, 0),
    # Punctuation
    ",": (0, 1, 0, 0, 0, 0),
    ";": (0, 1, 1, 0, 0, 0),
    ":": (0, 1, 0, 0, 1, 0),
    ".": (0, 1, 0, 0, 1, 1),
    "!": (0, 1, 1, 0, 1, 0),
    "?": (0, 1, 1, 0, 0, 1),
    "-": (0, 0, 1, 0, 0, 1),
}

# Special indicators
NUMBER_PREFIX = (0, 0, 1, 1, 1, 1)  # ⠼
CAPITAL_PREFIX = (0, 0, 0, 0, 0, 1)  # ⠠

# Mapping digits 1-9, 0 (using a-j dot patterns)
DIGIT_TO_LETTER = {
    "1": "a", "2": "b", "3": "c", "4": "d", "5": "e",
    "6": "f", "7": "g", "8": "h", "9": "i", "0": "j"
}
LETTER_TO_DIGIT = {v: k for k, v in DIGIT_TO_LETTER.items()}


def dots_to_unicode(dots: Tuple[int, int, int, int, int, int]) -> str:
    """Convert 6-dot tuple to Unicode Braille Pattern character."""
    mask = 0
    for i, val in enumerate(dots):
        if val:
            mask |= (1 << i)
    return chr(BRAILLE_UNICODE_OFFSET + mask)


def unicode_to_dots(char: str) -> Tuple[int, int, int, int, int, int]:
    """Convert Unicode Braille character to 6-dot tuple."""
    code = ord(char) - BRAILLE_UNICODE_OFFSET
    if code < 0 or code > 0xFF:
        return (0, 0, 0, 0, 0, 0)
    return (
        (code >> 0) & 1,
        (code >> 1) & 1,
        (code >> 2) & 1,
        (code >> 3) & 1,
        (code >> 4) & 1,
        (code >> 5) & 1,
    )


# Build reverse lookup tables
DOTS_TO_CHAR: Dict[Tuple[int, int, int, int, int, int], str] = {
    dots: ch for ch, dots in CHAR_TO_DOTS.items()
}

BRAILLE_TO_CHAR: Dict[str, str] = {
    dots_to_unicode(dots): ch for ch, dots in CHAR_TO_DOTS.items()
}

CHAR_TO_BRAILLE: Dict[str, str] = {
    ch: dots_to_unicode(dots) for ch, dots in CHAR_TO_DOTS.items()
}
