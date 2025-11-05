#!/usr/bin/env python3
"""
Example: Manga Translation
Optimized for manga/comic page translation
"""

import sys
sys.path.insert(0, '..')

from screen_translator_optimized import (
    ScreenCapture, OCREngine, TranslationEngine
)
import time


def main():
    print("📖 Manga Translation Example")
    print("=" * 50)
    print()

    # Setup
    print("📸 Initializing screen capture...")
    screen_capture = ScreenCapture()

    print("🔧 Initializing OCR (Japanese + English for manga)...")
    print("   This may take 1-2 minutes on first run...")
    ocr_engine = OCREngine(languages=['ja', 'en'])

    print("🌐 Initializing translation to Vietnamese...")
    translation_engine = TranslationEngine(target_language='vi')
    print()

    # Get screen center for manga
    monitors = screen_capture.get_monitor_info()
    monitor = monitors[1]

    # Capture center region (typical manga page size)
    width, height = 800, 1200
    x = monitor['left'] + (monitor['width'] - width) // 2
    y = monitor['top'] + (monitor['height'] - height) // 2

    print(f"📐 Capture region set to: ({x}, {y}) {width}x{height}")
    print("   (Center of screen, portrait orientation)")
    print()

    print("📚 Manual Translation Mode")
    print("   Press Enter to capture and translate")
    print("   Press 'q' + Enter to quit")
    print()

    page_num = 0
    while True:
        user_input = input(f"[Page {page_num + 1}] Press Enter to translate (q to quit): ")

        if user_input.lower() == 'q':
            print("👋 Bye!")
            break

        page_num += 1
        print(f"📸 Capturing page {page_num}...")
        start_time = time.time()

        # Capture
        img = screen_capture.capture_region(x, y, width, height)

        if img is None:
            print("❌ Failed to capture")
            continue

        # OCR with manga preset
        print("🔍 Performing OCR...")
        text = ocr_engine.extract_text_combined(
            img,
            preprocess=True,
            preset='manga'
        )

        if not text:
            print("⚠️  No text detected")
            print()
            continue

        print("✓ Text detected:")
        print("-" * 50)
        print(text[:200] + ("..." if len(text) > 200 else ""))
        print("-" * 50)
        print()

        # Translate
        print("🔄 Translating...")
        result = translation_engine.translate(text)

        if result:
            elapsed = time.time() - start_time
            print(f"✅ Translation complete in {elapsed:.2f}s")
            print(f"   Language detected: {result.language.upper()}")
            print()
            print("=" * 50)
            print("📖 TRANSLATION:")
            print("=" * 50)
            print(result.translated_text)
            print("=" * 50)
        else:
            print("❌ Translation failed")

        print()


if __name__ == "__main__":
    main()
