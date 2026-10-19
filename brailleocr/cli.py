import argparse
import asyncio
import json
import sys
from .engine import BrailleOCREngine


def display_ascii_preview(result):
    print("=" * 60)
    print("  BrailleVision-OCR: Translation & Visualizer")
    print("=" * 60)
    print(f" Braille Source : {result.braille_text}")
    print(f" Decoded Text   : {result.translated_text}")
    print(f" Cells Detected : {result.cell_count}")
    print("-" * 60)
    print(" 6-Dot Cell Visualizer:")
    for i, cell in enumerate(result.cells[:10]):
        dots_repr = "".join(str(d) for d in cell.dots)
        print(f"  Cell #{i+1} [{cell.unicode_char}] -> '{cell.latin_char}' (Dots: {dots_repr})")
        lines = cell.ascii_art().split("\n")
        for line in lines:
            print(f"    {line}")
        print()
    if len(result.cells) > 10:
        print(f"  ... and {len(result.cells) - 10} more cells")
    print("=" * 60)


async def synthesize_speech(text: str, output_file: str):
    try:
        import edge_tts  # type: ignore
        communicate = edge_tts.Communicate(text, "en-US-JennyNeural")
        await communicate.save(output_file)
        print(f"✔️ Spoken audio synthesized to: {output_file}")
    except ImportError:
        print("Note: 'edge-tts' package required for audio speech output.", file=sys.stderr)
    except Exception as e:
        print(f"Error synthesizing audio: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="BrailleVision-OCR Accessibility CLI")
    parser.add_argument("--encode", help="Convert standard text into Braille Unicode & dot representation")
    parser.add_argument("--decode", help="Decode Braille Unicode characters into English text")
    parser.add_argument("--tts", help="Generate spoken MP3 audio file of the decoded text")
    parser.add_argument("--json", action="store_true", help="Output JSON structure")
    args = parser.parse_args()

    engine = BrailleOCREngine()

    if args.encode:
        braille_str = engine.text_to_braille(args.encode)
        result = engine.braille_to_text(braille_str)
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            display_ascii_preview(result)
        sys.exit(0)

    if args.decode:
        result = engine.braille_to_text(args.decode)
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            display_ascii_preview(result)

        if args.tts:
            asyncio.run(synthesize_speech(result.translated_text, args.tts))
        sys.exit(0)

    # Default demo
    sample_text = "Hello 2026!"
    print(f"Running default demo with sample: '{sample_text}'\n")
    braille_str = engine.text_to_braille(sample_text)
    result = engine.braille_to_text(braille_str)
    display_ascii_preview(result)


if __name__ == "__main__":
    main()
