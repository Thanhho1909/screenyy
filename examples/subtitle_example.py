#!/usr/bin/env python3
"""
Example: Subtitle Translation
Optimized for anime/movie subtitle translation
"""

import sys
sys.path.insert(0, '..')

from screen_translator_optimized import (
    ScreenCapture, OCREngine, TranslationEngine, OverlayWindow
)
import tkinter as tk
import time


def main():
    print("🎬 Subtitle Translation Example")
    print("=" * 50)
    print()

    # Setup
    print("📸 Initializing screen capture...")
    screen_capture = ScreenCapture()

    print("🔧 Initializing OCR (Japanese only for faster processing)...")
    print("   This may take 1-2 minutes on first run...")
    ocr_engine = OCREngine(languages=['ja'])

    print("🌐 Initializing translation to Vietnamese...")
    translation_engine = TranslationEngine(target_language='vi')

    # Get subtitle region (bottom 20% of screen)
    x, y, width, height = screen_capture.get_subtitle_region()
    print(f"✓ Subtitle region: ({x}, {y}) {width}x{height}")
    print()

    # Create overlay
    root = tk.Tk()
    root.withdraw()  # Hide main window
    overlay = OverlayWindow(root)

    print("🎥 Starting subtitle translation...")
    print("   Capturing subtitle region every 1.5 seconds")
    print("   Press Ctrl+C to stop")
    print()

    try:
        iteration = 0
        while True:
            iteration += 1
            start_time = time.time()

            # Capture subtitle region
            img = screen_capture.capture_region(x, y, width, height)

            if img is None:
                time.sleep(0.1)
                continue

            # OCR with preprocessing
            text = ocr_engine.extract_text_combined(
                img,
                preprocess=True,
                preset='subtitle'
            )

            if text:
                print(f"[{iteration}] Detected: {text[:50]}...")

                # Translate
                result = translation_engine.translate(text)

                if result:
                    elapsed = time.time() - start_time
                    print(f"     Translated in {elapsed:.2f}s")
                    print(f"     → {result.translated_text[:50]}...")
                    print()

                    # Update overlay
                    if not overlay.is_visible:
                        overlay.create_overlay(x, y, 550, 250)

                    overlay.update_text(
                        result.original_text,
                        result.translated_text,
                        result.language
                    )

            # Wait before next capture
            root.update()
            time.sleep(1.5)

    except KeyboardInterrupt:
        print()
        print("⏹️  Stopped by user")
        overlay.close()


if __name__ == "__main__":
    main()
