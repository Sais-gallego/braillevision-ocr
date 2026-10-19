# ⠃⠗⠁⠊⠇⠇⠑ BrailleVision-OCR

[![CI Pipeline](https://github.com/Sais-gallego/braillevision-ocr/actions/workflows/ci.yml/badge.svg)](https://github.com/Sais-gallego/braillevision-ocr/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Accessibility: A11y](https://img.shields.io/badge/Accessibility-Braille%20%26%20TTS-green.svg)](https://www.w3.org/WAI/)

> **Computer Vision Braille Recognition & Text-to-Speech Accessibility Engine.**  
> Decodes embossed and printed 6-dot Braille cells into English text, renders ASCII tactile matrices, and converts reading material into synthetic speech for the visually impaired.

---

## ⚡ Key Capabilities

- **Full Grade-1 Braille Standard**: Complete support for the English 26-letter alphabet, numeric prefixes (⠼), capital letter indicators (⠠), spaces, and punctuation (`.`, `,`, `?`, `!`, `-`, `;`, `:`).
- **Unicode Braille Patterns (U+2800 - U+28FF)**: Bidirectional encoding and decoding between standard Latin text and Unicode Braille glyphs.
- **ASCII Dot Matrix Visualizer**: Renders 3x2 dot representations (`●` / `○`) in terminal reports for verification and tactile proofing.
- **Neural Text-to-Speech**: Built-in speech synthesis pipeline using neural TTS models to speak decoded books and documents aloud.
- **Zero-Dependency Core**: Algorithmic translation engine runs on standard Python with zero external libraries; optional vision and TTS modules provide extended pipeline functionality.

---

## 📐 Architecture Overview

```
 ┌──────────────────────┐         ┌──────────────────────┐
 │ Raw Text Input       │         │ Embossed Braille     │
 └──────────┬───────────┘         └──────────┬───────────┘
            │                                │
            ▼                                ▼
 ┌──────────────────────┐         ┌──────────────────────┐
 │ Prefix & Mode Parser │         │ 3x2 Dot Grid Matrix  │
 │ (Capital, Number)    │         │  - (d1, d2, d3)      │
 └──────────┬───────────┘         │  - (d4, d5, d6)      │
            │                     └──────────┬───────────┘
            ▼                                │
 ┌──────────────────────┐                    │
 │ Unicode Encoder      │                    │
 │ (U+2800 - U+28FF)    │                    │
 └──────────┬───────────┘                    │
            │                                │
            └───────────────┬────────────────┘
                            ▼
               ┌──────────────────────────┐
               │    BrailleOCR Engine     │
               │  - Dot State Validation  │
               │  - Cell Bounding Box     │
               └────────────┬─────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
      English Text     ASCII Visualizer  Neural Audio (TTS)
      "Hello 2026"         ● ○ / ● ●       audio_speech.mp3
```

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/Sais-gallego/braillevision-ocr.git
cd braillevision-ocr
pip install -r requirements.txt
pip install .
```

### CLI Usage

**Encode English Text to Braille:**
```bash
brailleocr --encode "Hello World"
```

**Output:**
```
============================================================
  BrailleVision-OCR: Translation & Visualizer
============================================================
 Braille Source : ⠠⠓⠑⠇⠇⠕ ⠺⠕⠗⠇⠙
 Decoded Text   : Hello world
 Cells Detected : 12
------------------------------------------------------------
 6-Dot Cell Visualizer:
  Cell #1 [⠠] -> '[CAP]' (Dots: 000001)
    ○ ○
    ○ ○
    ○ ●

  Cell #2 [⠓] -> 'H' (Dots: 110010)
    ● ○
    ● ●
    ○ ○
============================================================
```

**Decode Braille Unicode and Speak Aloud:**
```bash
brailleocr --decode "⠠⠓⠑⠇⠇⠕" --tts speech.mp3
```

---

## 🐍 Python SDK Integration

```python
from brailleocr import BrailleOCREngine

engine = BrailleOCREngine()

# Encode to Braille
braille_code = engine.text_to_braille("Access 2026")
print(f"Braille: {braille_code}")

# Decode from Braille
result = engine.braille_to_text(braille_code)
print(f"Decoded: {result.translated_text}")
```

---

## 🧪 Testing

```bash
python -m unittest discover tests -v
```

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for details.
