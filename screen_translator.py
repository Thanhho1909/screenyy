#!/usr/bin/env python3
"""
Screen Translator - Real-time translation tool for on-screen text
Captures screen content, performs OCR, and translates to target language
"""

import sys
import time
import threading
from dataclasses import dataclass
from typing import Optional, Tuple, List
import mss
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox
import easyocr
from googletrans import Translator
import cv2


@dataclass
class TranslationResult:
    """Result of OCR and translation"""
    original_text: str
    translated_text: str
    language: str
    confidence: float


class ScreenCapture:
    """Handle screen capturing functionality"""

    def __init__(self):
        self.sct = mss.mss()

    def capture_screen(self, monitor_number: int = 1) -> np.ndarray:
        """
        Capture entire screen

        Args:
            monitor_number: Monitor index (1 for primary, 0 for all monitors)

        Returns:
            numpy array of the screenshot
        """
        monitor = self.sct.monitors[monitor_number]
        screenshot = self.sct.grab(monitor)
        # Convert to numpy array
        img = np.array(screenshot)
        # Convert BGRA to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        return img

    def capture_region(self, x: int, y: int, width: int, height: int) -> np.ndarray:
        """
        Capture specific screen region

        Args:
            x, y: Top-left corner coordinates
            width, height: Region dimensions

        Returns:
            numpy array of the screenshot
        """
        region = {"top": y, "left": x, "width": width, "height": height}
        screenshot = self.sct.grab(region)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        return img

    def get_monitor_info(self) -> List[dict]:
        """Get information about all available monitors"""
        return self.sct.monitors


class OCREngine:
    """Handle OCR operations using EasyOCR"""

    def __init__(self, languages: List[str] = ['en', 'ja', 'ko', 'zh_sim', 'th']):
        """
        Initialize OCR engine

        Args:
            languages: List of language codes to recognize
        """
        print(f"Initializing OCR engine for languages: {languages}")
        self.reader = easyocr.Reader(languages, gpu=False)
        print("OCR engine ready!")

    def extract_text(self, image: np.ndarray, detail: int = 0) -> List[Tuple[str, float]]:
        """
        Extract text from image

        Args:
            image: numpy array of the image
            detail: 0 for simple text+confidence, 1 for detailed bbox info

        Returns:
            List of (text, confidence) tuples
        """
        results = self.reader.readtext(image, detail=detail)

        if detail == 0:
            return results
        else:
            # Extract only text and confidence from detailed results
            return [(text, conf) for (bbox, text, conf) in results]

    def extract_text_combined(self, image: np.ndarray) -> str:
        """
        Extract all text from image and combine into single string

        Args:
            image: numpy array of the image

        Returns:
            Combined text string
        """
        results = self.extract_text(image)
        if not results:
            return ""
        return "\n".join([text for text, conf in results if conf > 0.3])


class TranslationEngine:
    """Handle translation operations"""

    def __init__(self, target_language: str = 'vi'):
        """
        Initialize translation engine

        Args:
            target_language: Target language code (default: 'vi' for Vietnamese)
        """
        self.translator = Translator()
        self.target_language = target_language

    def translate(self, text: str, src_lang: str = 'auto') -> Optional[TranslationResult]:
        """
        Translate text to target language

        Args:
            text: Text to translate
            src_lang: Source language (auto-detect if 'auto')

        Returns:
            TranslationResult object or None if translation fails
        """
        if not text or not text.strip():
            return None

        try:
            result = self.translator.translate(
                text,
                src=src_lang,
                dest=self.target_language
            )

            return TranslationResult(
                original_text=text,
                translated_text=result.text,
                language=result.src,
                confidence=1.0
            )
        except Exception as e:
            print(f"Translation error: {e}")
            return None

    def set_target_language(self, lang_code: str):
        """Change target language"""
        self.target_language = lang_code


class OverlayWindow:
    """Transparent overlay window to display translations"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.window = None
        self.text_widget = None

    def create_overlay(self, x: int, y: int, width: int = 400, height: int = 200):
        """Create semi-transparent overlay window"""
        if self.window:
            self.window.destroy()

        self.window = tk.Toplevel(self.root)
        self.window.title("Translation")
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        # Make window semi-transparent and always on top
        self.window.attributes('-alpha', 0.9)
        self.window.attributes('-topmost', True)

        # Create text widget with scrollbar
        frame = ttk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_widget = tk.Text(
            frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            font=('Arial', 11),
            bg='#2b2b2b',
            fg='#ffffff',
            insertbackground='white'
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_widget.yview)

    def update_text(self, original: str, translated: str, lang: str = ""):
        """Update overlay text with translation"""
        if not self.text_widget:
            return

        self.text_widget.delete(1.0, tk.END)

        if lang:
            self.text_widget.insert(tk.END, f"[Detected: {lang.upper()}]\n\n", 'header')

        self.text_widget.insert(tk.END, "Original:\n", 'label')
        self.text_widget.insert(tk.END, f"{original}\n\n", 'original')

        self.text_widget.insert(tk.END, "Translation:\n", 'label')
        self.text_widget.insert(tk.END, translated, 'translated')

        # Configure tags for styling
        self.text_widget.tag_config('header', foreground='#888888', font=('Arial', 9))
        self.text_widget.tag_config('label', foreground='#4CAF50', font=('Arial', 10, 'bold'))
        self.text_widget.tag_config('original', foreground='#E0E0E0')
        self.text_widget.tag_config('translated', foreground='#FFD700', font=('Arial', 11, 'bold'))

    def close(self):
        """Close overlay window"""
        if self.window:
            self.window.destroy()
            self.window = None
            self.text_widget = None


class ScreenTranslatorGUI:
    """Main GUI application"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Screen Translator")
        self.root.geometry("500x600")

        # Initialize components
        self.screen_capture = ScreenCapture()
        self.ocr_engine = None  # Lazy initialization
        self.translation_engine = TranslationEngine()
        self.overlay = OverlayWindow(root)

        # State
        self.is_selecting = False
        self.selection_rect = None
        self.auto_mode = False
        self.auto_thread = None

        self.setup_ui()

    def setup_ui(self):
        """Setup GUI components"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title = ttk.Label(
            main_frame,
            text="🌍 Screen Translator",
            font=('Arial', 16, 'bold')
        )
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Language selection
        lang_frame = ttk.LabelFrame(main_frame, text="Target Language", padding="10")
        lang_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.lang_var = tk.StringVar(value='vi')
        languages = [
            ('Vietnamese (Tiếng Việt)', 'vi'),
            ('English', 'en'),
            ('Japanese (日本語)', 'ja'),
            ('Korean (한국어)', 'ko'),
            ('Chinese (中文)', 'zh-cn'),
            ('Thai (ไทย)', 'th'),
        ]

        for i, (name, code) in enumerate(languages):
            ttk.Radiobutton(
                lang_frame,
                text=name,
                variable=self.lang_var,
                value=code,
                command=self.on_language_change
            ).grid(row=i, column=0, sticky=tk.W, pady=2)

        # Capture mode
        mode_frame = ttk.LabelFrame(main_frame, text="Capture Mode", padding="10")
        mode_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(
            mode_frame,
            text="📷 Capture Full Screen",
            command=self.capture_full_screen
        ).grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))

        ttk.Button(
            mode_frame,
            text="✂️ Select Region",
            command=self.start_region_selection
        ).grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))

        # Auto mode
        self.auto_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            mode_frame,
            text="🔄 Auto Mode (capture every 2 seconds)",
            variable=self.auto_var,
            command=self.toggle_auto_mode
        ).grid(row=2, column=0, pady=5, sticky=tk.W)

        # Status
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.status_text = tk.Text(status_frame, height=10, wrap=tk.WORD)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.status_text.config(yscrollcommand=scrollbar.set)

        # Initialize OCR button
        ttk.Button(
            main_frame,
            text="🔧 Initialize OCR Engine",
            command=self.initialize_ocr
        ).grid(row=4, column=0, columnspan=2, pady=10)

        self.log("Ready! Click 'Initialize OCR Engine' to start.")

    def log(self, message: str):
        """Add message to status log"""
        self.status_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update()

    def initialize_ocr(self):
        """Initialize OCR engine (can take some time)"""
        if self.ocr_engine:
            self.log("OCR engine already initialized!")
            return

        self.log("Initializing OCR engine... This may take a minute...")
        self.root.update()

        try:
            self.ocr_engine = OCREngine()
            self.log("✓ OCR engine initialized successfully!")
        except Exception as e:
            self.log(f"✗ Error initializing OCR: {e}")
            messagebox.showerror("Error", f"Failed to initialize OCR: {e}")

    def on_language_change(self):
        """Handle language change"""
        lang = self.lang_var.get()
        self.translation_engine.set_target_language(lang)
        self.log(f"Target language changed to: {lang}")

    def capture_full_screen(self):
        """Capture and translate full screen"""
        if not self.ocr_engine:
            messagebox.showwarning("Warning", "Please initialize OCR engine first!")
            return

        self.log("Capturing full screen...")
        try:
            img = self.screen_capture.capture_screen()
            self.process_image(img)
        except Exception as e:
            self.log(f"✗ Error: {e}")
            messagebox.showerror("Error", str(e))

    def start_region_selection(self):
        """Start region selection mode"""
        if not self.ocr_engine:
            messagebox.showwarning("Warning", "Please initialize OCR engine first!")
            return

        self.log("Select region on screen...")
        messagebox.showinfo(
            "Region Selection",
            "Region selection will be implemented.\nFor now, capturing center 800x600 region."
        )

        # For now, capture center region
        monitors = self.screen_capture.get_monitor_info()
        monitor = monitors[1]  # Primary monitor
        x = monitor['left'] + (monitor['width'] - 800) // 2
        y = monitor['top'] + (monitor['height'] - 600) // 2

        img = self.screen_capture.capture_region(x, y, 800, 600)
        self.process_image(img, x, y)

    def toggle_auto_mode(self):
        """Toggle automatic capture mode"""
        if self.auto_var.get():
            if not self.ocr_engine:
                self.auto_var.set(False)
                messagebox.showwarning("Warning", "Please initialize OCR engine first!")
                return

            self.log("Auto mode enabled")
            self.auto_mode = True
            self.auto_thread = threading.Thread(target=self.auto_capture_loop, daemon=True)
            self.auto_thread.start()
        else:
            self.log("Auto mode disabled")
            self.auto_mode = False

    def auto_capture_loop(self):
        """Auto capture loop for continuous translation"""
        while self.auto_mode:
            try:
                img = self.screen_capture.capture_screen()
                self.process_image(img)
                time.sleep(2)
            except Exception as e:
                print(f"Auto capture error: {e}")
                time.sleep(2)

    def process_image(self, image: np.ndarray, overlay_x: int = 100, overlay_y: int = 100):
        """Process captured image: OCR + Translation"""
        try:
            # OCR
            self.log("Performing OCR...")
            text = self.ocr_engine.extract_text_combined(image)

            if not text:
                self.log("✗ No text detected in image")
                return

            self.log(f"✓ Detected text: {text[:100]}...")

            # Translate
            self.log("Translating...")
            result = self.translation_engine.translate(text)

            if result:
                self.log(f"✓ Translation complete [{result.language} → {self.lang_var.get()}]")
                self.log(f"Translation: {result.translated_text[:100]}...")

                # Show overlay
                self.overlay.create_overlay(overlay_x, overlay_y)
                self.overlay.update_text(
                    result.original_text,
                    result.translated_text,
                    result.language
                )
            else:
                self.log("✗ Translation failed")

        except Exception as e:
            self.log(f"✗ Processing error: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ScreenTranslatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
