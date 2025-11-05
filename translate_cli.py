#!/usr/bin/env python3
"""
Simple CLI version of Screen Translator
Usage: python translate_cli.py [--lang vi] [--region x y width height]
"""

import argparse
import sys
from screen_translator import ScreenCapture, OCREngine, TranslationEngine


def main():
    parser = argparse.ArgumentParser(
        description='Screen Translator CLI - Translate text from screen'
    )
    parser.add_argument(
        '--lang',
        default='vi',
        help='Target language code (default: vi for Vietnamese)'
    )
    parser.add_argument(
        '--region',
        nargs=4,
        type=int,
        metavar=('X', 'Y', 'WIDTH', 'HEIGHT'),
        help='Capture specific region (x y width height)'
    )
    parser.add_argument(
        '--ocr-langs',
        nargs='+',
        default=['en', 'ja', 'ko', 'zh_sim'],
        help='OCR language codes (default: en ja ko zh_sim)'
    )
    parser.add_argument(
        '--save',
        help='Save screenshot to file'
    )

    args = parser.parse_args()

    print("🌍 Screen Translator CLI")
    print("=" * 50)

    # Initialize components
    print("\n📸 Initializing screen capture...")
    screen_capture = ScreenCapture()

    print(f"🔧 Initializing OCR engine for languages: {', '.join(args.ocr_langs)}")
    print("   (This may take a minute on first run...)")
    ocr_engine = OCREngine(languages=args.ocr_langs)

    print(f"🌐 Initializing translation engine (target: {args.lang})")
    translation_engine = TranslationEngine(target_language=args.lang)

    # Capture screen
    print("\n📷 Capturing screen...")
    if args.region:
        x, y, width, height = args.region
        print(f"   Region: ({x}, {y}) {width}x{height}")
        image = screen_capture.capture_region(x, y, width, height)
    else:
        print("   Full screen")
        image = screen_capture.capture_screen()

    # Save if requested
    if args.save:
        from PIL import Image
        Image.fromarray(image).save(args.save)
        print(f"   ✓ Screenshot saved to: {args.save}")

    # Perform OCR
    print("\n🔍 Performing OCR...")
    text = ocr_engine.extract_text_combined(image)

    if not text:
        print("   ✗ No text detected in image")
        sys.exit(1)

    print("   ✓ Text detected!")
    print("\n" + "=" * 50)
    print("📝 ORIGINAL TEXT:")
    print("=" * 50)
    print(text)

    # Translate
    print("\n🔄 Translating...")
    result = translation_engine.translate(text)

    if not result:
        print("   ✗ Translation failed")
        sys.exit(1)

    print(f"   ✓ Translation complete [{result.language} → {args.lang}]")
    print("\n" + "=" * 50)
    print("🌍 TRANSLATION:")
    print("=" * 50)
    print(result.translated_text)
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
