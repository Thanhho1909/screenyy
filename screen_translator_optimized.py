#!/usr/bin/env python3
"""
Screen Translator - Optimized version for Windows 11
Real-time translation tool with performance improvements for subtitle and manga translation
"""

import sys
import time
import threading
from dataclasses import dataclass
from typing import Optional, Tuple, List
from collections import deque
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
    timestamp: float = 0.0


@dataclass
class CapturePreset:
    """Predefined capture presets for different use cases"""
    name: str
    description: str
    region: Optional[Tuple[int, int, int, int]]  # x, y, width, height
    refresh_rate: float  # seconds
    ocr_langs: List[str]
    image_preprocessing: bool


# Predefined presets
PRESETS = {
    'subtitle': CapturePreset(
        name='Subtitle Mode',
        description='Optimized for movie/anime subtitles (bottom of screen)',
        region=None,  # Will be calculated based on screen size
        refresh_rate=1.5,
        ocr_langs=['en', 'ja', 'ko', 'zh_sim'],
        image_preprocessing=True
    ),
    'manga': CapturePreset(
        name='Manga Mode',
        description='Optimized for manga/comic text bubbles',
        region=None,
        refresh_rate=0,  # Manual capture
        ocr_langs=['ja', 'en'],
        image_preprocessing=True
    ),
    'game': CapturePreset(
        name='Game Mode',
        description='For game dialogs and UI',
        region=None,
        refresh_rate=2.0,
        ocr_langs=['en', 'ja', 'ko', 'zh_sim'],
        image_preprocessing=False
    ),
}


class ScreenCapture:
    """Handle screen capturing functionality - Windows optimized"""

    def __init__(self):
        self.sct = mss.mss()
        self.last_capture_time = 0
        self.min_capture_interval = 0.1  # Minimum 100ms between captures

    def capture_screen(self, monitor_number: int = 1) -> Optional[np.ndarray]:
        """
        Capture entire screen with rate limiting

        Args:
            monitor_number: Monitor index (1 for primary, 0 for all monitors)

        Returns:
            numpy array of the screenshot or None if rate limited
        """
        current_time = time.time()
        if current_time - self.last_capture_time < self.min_capture_interval:
            return None

        try:
            monitor = self.sct.monitors[monitor_number]
            screenshot = self.sct.grab(monitor)
            self.last_capture_time = current_time

            # Convert to numpy array
            img = np.array(screenshot)
            # Convert BGRA to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
            return img
        except Exception as e:
            print(f"Capture error: {e}")
            return None

    def capture_region(self, x: int, y: int, width: int, height: int) -> Optional[np.ndarray]:
        """
        Capture specific screen region with rate limiting

        Args:
            x, y: Top-left corner coordinates
            width, height: Region dimensions

        Returns:
            numpy array of the screenshot or None if rate limited
        """
        current_time = time.time()
        if current_time - self.last_capture_time < self.min_capture_interval:
            return None

        try:
            region = {"top": y, "left": x, "width": width, "height": height}
            screenshot = self.sct.grab(region)
            self.last_capture_time = current_time

            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
            return img
        except Exception as e:
            print(f"Capture error: {e}")
            return None

    def get_monitor_info(self) -> List[dict]:
        """Get information about all available monitors"""
        return self.sct.monitors

    def get_subtitle_region(self, monitor_number: int = 1) -> Tuple[int, int, int, int]:
        """Calculate subtitle region (bottom 20% of screen)"""
        monitor = self.sct.monitors[monitor_number]
        width = monitor['width']
        height = monitor['height']
        left = monitor['left']
        top = monitor['top']

        # Bottom 20% of screen, centered 80% width
        subtitle_height = int(height * 0.2)
        subtitle_width = int(width * 0.8)
        subtitle_x = left + int(width * 0.1)
        subtitle_y = top + height - subtitle_height

        return (subtitle_x, subtitle_y, subtitle_width, subtitle_height)


class OCREngine:
    """Handle OCR operations using EasyOCR - Performance optimized"""

    def __init__(self, languages: List[str] = ['en', 'ja', 'ko', 'zh_sim']):
        """
        Initialize OCR engine

        Args:
            languages: List of language codes to recognize
        """
        print(f"Initializing OCR engine for languages: {languages}")
        self.reader = easyocr.Reader(languages, gpu=False)
        self.last_text_hash = None
        print("OCR engine ready!")

    def preprocess_image(self, image: np.ndarray, preset: str = 'subtitle') -> np.ndarray:
        """
        Preprocess image for better OCR accuracy

        Args:
            image: Input image
            preset: Preprocessing preset (subtitle, manga, game)

        Returns:
            Preprocessed image
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        if preset == 'subtitle':
            # High contrast for subtitles
            # Apply adaptive thresholding
            processed = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
        elif preset == 'manga':
            # Manga pages often have good contrast already
            # Just denoise and sharpen
            denoised = cv2.fastNlMeansDenoising(gray)
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            processed = cv2.filter2D(denoised, -1, kernel)
        else:
            # Generic preprocessing
            processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Convert back to RGB for EasyOCR
        processed_rgb = cv2.cvtColor(processed, cv2.COLOR_GRAY2RGB)
        return processed_rgb

    def extract_text(self, image: np.ndarray, detail: int = 0,
                    preprocess: bool = True, preset: str = 'subtitle') -> List[Tuple[str, float]]:
        """
        Extract text from image

        Args:
            image: numpy array of the image
            detail: 0 for simple text+confidence, 1 for detailed bbox info
            preprocess: Apply image preprocessing
            preset: Preprocessing preset

        Returns:
            List of (text, confidence) tuples
        """
        if preprocess:
            image = self.preprocess_image(image, preset)

        results = self.reader.readtext(image, detail=detail)

        if detail == 0:
            return results
        else:
            # Extract only text and confidence from detailed results
            return [(text, conf) for (bbox, text, conf) in results]

    def extract_text_combined(self, image: np.ndarray,
                             preprocess: bool = True,
                             preset: str = 'subtitle',
                             min_confidence: float = 0.3) -> str:
        """
        Extract all text from image and combine into single string

        Args:
            image: numpy array of the image
            preprocess: Apply preprocessing
            preset: Preprocessing preset
            min_confidence: Minimum confidence threshold

        Returns:
            Combined text string
        """
        results = self.extract_text(image, preprocess=preprocess, preset=preset)
        if not results:
            return ""

        # Filter by confidence and combine
        texts = [text for text, conf in results if conf > min_confidence]
        combined = "\n".join(texts)

        # Check if text is duplicate (for auto mode optimization)
        text_hash = hash(combined)
        if text_hash == self.last_text_hash:
            return ""  # Return empty if same as last

        self.last_text_hash = text_hash
        return combined


class TranslationEngine:
    """Handle translation operations with caching"""

    def __init__(self, target_language: str = 'vi'):
        """
        Initialize translation engine

        Args:
            target_language: Target language code (default: 'vi' for Vietnamese)
        """
        self.translator = Translator()
        self.target_language = target_language
        self.translation_cache = {}  # Simple cache
        self.cache_max_size = 100

    def translate(self, text: str, src_lang: str = 'auto') -> Optional[TranslationResult]:
        """
        Translate text to target language with caching

        Args:
            text: Text to translate
            src_lang: Source language (auto-detect if 'auto')

        Returns:
            TranslationResult object or None if translation fails
        """
        if not text or not text.strip():
            return None

        # Check cache
        cache_key = f"{text}:{src_lang}:{self.target_language}"
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]

        try:
            result = self.translator.translate(
                text,
                src=src_lang,
                dest=self.target_language
            )

            translation_result = TranslationResult(
                original_text=text,
                translated_text=result.text,
                language=result.src,
                confidence=1.0,
                timestamp=time.time()
            )

            # Cache result
            if len(self.translation_cache) >= self.cache_max_size:
                # Remove oldest entry
                oldest_key = min(self.translation_cache.keys(),
                               key=lambda k: self.translation_cache[k].timestamp)
                del self.translation_cache[oldest_key]

            self.translation_cache[cache_key] = translation_result
            return translation_result

        except Exception as e:
            print(f"Translation error: {e}")
            return None

    def set_target_language(self, lang_code: str):
        """Change target language and clear cache"""
        self.target_language = lang_code
        self.translation_cache.clear()


class OverlayWindow:
    """Transparent overlay window to display translations - Windows optimized"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.window = None
        self.text_widget = None
        self.is_visible = False

    def create_overlay(self, x: int = 100, y: int = 100, width: int = 500, height: int = 250):
        """Create semi-transparent overlay window optimized for Windows 11"""
        if self.window:
            self.window.destroy()

        self.window = tk.Toplevel(self.root)
        self.window.title("Translation Overlay")

        # Windows 11 optimized positioning
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        # Transparency and always on top
        self.window.attributes('-alpha', 0.92)
        self.window.attributes('-topmost', True)

        # Remove window decorations for cleaner look (optional)
        # self.window.overrideredirect(True)

        # Modern dark theme
        frame = ttk.Frame(self.window, style='Dark.TFrame')
        frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Text widget with modern styling
        self.text_widget = tk.Text(
            frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            font=('Segoe UI', 11),  # Windows 11 default font
            bg='#1e1e1e',  # Dark background
            fg='#ffffff',
            insertbackground='white',
            borderwidth=0,
            highlightthickness=0,
            padx=10,
            pady=10
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_widget.yview)

        self.is_visible = True

    def update_text(self, original: str, translated: str, lang: str = ""):
        """Update overlay text with translation"""
        if not self.text_widget:
            return

        self.text_widget.delete(1.0, tk.END)

        if lang:
            self.text_widget.insert(tk.END, f"[{lang.upper()} → VI]\n\n", 'header')

        self.text_widget.insert(tk.END, "原文 Original:\n", 'label')
        self.text_widget.insert(tk.END, f"{original}\n\n", 'original')

        self.text_widget.insert(tk.END, "翻訳 Translation:\n", 'label')
        self.text_widget.insert(tk.END, translated, 'translated')

        # Configure tags for styling
        self.text_widget.tag_config('header', foreground='#888888', font=('Segoe UI', 9))
        self.text_widget.tag_config('label', foreground='#4CAF50', font=('Segoe UI', 10, 'bold'))
        self.text_widget.tag_config('original', foreground='#E0E0E0', font=('Segoe UI', 10))
        self.text_widget.tag_config('translated', foreground='#FFD700', font=('Segoe UI', 12, 'bold'))

    def close(self):
        """Close overlay window"""
        if self.window:
            self.window.destroy()
            self.window = None
            self.text_widget = None
            self.is_visible = False


class ScreenTranslatorGUI:
    """Main GUI application - Windows 11 optimized"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Screen Translator - Windows 11 Optimized")
        self.root.geometry("600x700")

        # Initialize components
        self.screen_capture = ScreenCapture()
        self.ocr_engine = None  # Lazy initialization
        self.translation_engine = TranslationEngine()
        self.overlay = OverlayWindow(root)

        # State
        self.auto_mode = False
        self.auto_thread = None
        self.current_preset = 'subtitle'
        self.custom_region = None

        # Performance tracking
        self.last_process_time = 0
        self.fps_history = deque(maxlen=10)

        self.setup_ui()

    def setup_ui(self):
        """Setup GUI components with Windows 11 style"""
        # Configure style
        style = ttk.Style()
        style.theme_use('vista')  # Windows native theme

        # Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title with emoji
        title = ttk.Label(
            main_frame,
            text="🌍 Screen Translator - Optimized",
            font=('Segoe UI', 18, 'bold')
        )
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Preset selection
        preset_frame = ttk.LabelFrame(main_frame, text="📋 Quick Presets", padding="10")
        preset_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.preset_var = tk.StringVar(value='subtitle')
        presets_list = [
            ('🎬 Subtitle Mode (Phụ đề phim)', 'subtitle'),
            ('📖 Manga Mode (Truyện tranh)', 'manga'),
            ('🎮 Game Mode (Game dialog)', 'game'),
            ('🖥️  Custom (Tùy chỉnh)', 'custom'),
        ]

        for i, (name, code) in enumerate(presets_list):
            ttk.Radiobutton(
                preset_frame,
                text=name,
                variable=self.preset_var,
                value=code,
                command=self.on_preset_change
            ).grid(row=i, column=0, sticky=tk.W, pady=3)

        # Language selection
        lang_frame = ttk.LabelFrame(main_frame, text="🌐 Target Language", padding="10")
        lang_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.lang_var = tk.StringVar(value='vi')
        languages = [
            ('🇻🇳 Tiếng Việt', 'vi'),
            ('🇬🇧 English', 'en'),
            ('🇯🇵 日本語', 'ja'),
            ('🇰🇷 한국어', 'ko'),
            ('🇨🇳 中文', 'zh-cn'),
        ]

        for i, (name, code) in enumerate(languages):
            col = i % 2
            row = i // 2
            ttk.Radiobutton(
                lang_frame,
                text=name,
                variable=self.lang_var,
                value=code,
                command=self.on_language_change
            ).grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)

        # Control buttons
        control_frame = ttk.LabelFrame(main_frame, text="🎯 Controls", padding="10")
        control_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(
            control_frame,
            text="🔧 Initialize OCR Engine",
            command=self.initialize_ocr
        ).grid(row=0, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

        ttk.Button(
            control_frame,
            text="📷 Capture & Translate",
            command=self.capture_and_translate
        ).grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E), padx=(0, 5))

        ttk.Button(
            control_frame,
            text="🔧 Set Custom Region",
            command=self.set_custom_region
        ).grid(row=1, column=1, pady=5, sticky=(tk.W, tk.E), padx=(5, 0))

        # Auto mode
        self.auto_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            control_frame,
            text="🔄 Auto Mode (Continuous Translation)",
            variable=self.auto_var,
            command=self.toggle_auto_mode
        ).grid(row=2, column=0, columnspan=2, pady=5, sticky=tk.W)

        # Performance info
        perf_frame = ttk.LabelFrame(main_frame, text="⚡ Performance", padding="10")
        perf_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.perf_label = ttk.Label(perf_frame, text="Ready", font=('Consolas', 9))
        self.perf_label.pack()

        # Status log
        status_frame = ttk.LabelFrame(main_frame, text="📊 Status Log", padding="10")
        status_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        self.status_text = tk.Text(status_frame, height=12, wrap=tk.WORD, font=('Consolas', 9))
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.status_text.config(yscrollcommand=scrollbar.set)

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)

        self.log("✅ Ready! Select preset and initialize OCR to start.")
        self.log("💡 Tip: Use Subtitle Mode for movies, Manga Mode for comics!")

    def log(self, message: str):
        """Add message to status log"""
        timestamp = time.strftime('%H:%M:%S')
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()

    def update_performance_info(self, process_time: float):
        """Update performance metrics"""
        fps = 1.0 / process_time if process_time > 0 else 0
        self.fps_history.append(fps)
        avg_fps = sum(self.fps_history) / len(self.fps_history)

        self.perf_label.config(
            text=f"⚡ Last: {process_time:.2f}s | Avg FPS: {avg_fps:.2f} | "
                 f"Mode: {self.current_preset.upper()}"
        )

    def initialize_ocr(self):
        """Initialize OCR engine based on preset"""
        if self.ocr_engine:
            self.log("✓ OCR engine already initialized!")
            return

        preset = PRESETS.get(self.preset_var.get(), PRESETS['subtitle'])
        self.log(f"🔧 Initializing OCR for {preset.name}...")
        self.log("⏳ This may take 1-2 minutes on first run...")
        self.root.update()

        try:
            self.ocr_engine = OCREngine(languages=preset.ocr_langs)
            self.log("✅ OCR engine initialized successfully!")
            self.log(f"📋 Languages: {', '.join(preset.ocr_langs)}")
        except Exception as e:
            self.log(f"❌ Error initializing OCR: {e}")
            messagebox.showerror("Error", f"Failed to initialize OCR: {e}")

    def on_preset_change(self):
        """Handle preset change"""
        self.current_preset = self.preset_var.get()
        preset = PRESETS.get(self.current_preset)

        if preset:
            self.log(f"📋 Preset changed: {preset.name}")
            self.log(f"   {preset.description}")
        else:
            self.log("📋 Custom mode selected")

    def on_language_change(self):
        """Handle language change"""
        lang = self.lang_var.get()
        self.translation_engine.set_target_language(lang)
        self.log(f"🌐 Target language: {lang}")

    def set_custom_region(self):
        """Set custom capture region"""
        self.log("🔧 Custom region: Capturing center 1000x600 area")
        monitors = self.screen_capture.get_monitor_info()
        monitor = monitors[1]

        x = monitor['left'] + (monitor['width'] - 1000) // 2
        y = monitor['top'] + (monitor['height'] - 600) // 2

        self.custom_region = (x, y, 1000, 600)
        self.log(f"✓ Region set: ({x}, {y}) 1000x600")

    def capture_and_translate(self):
        """Capture screen and translate"""
        if not self.ocr_engine:
            messagebox.showwarning("Warning", "Please initialize OCR engine first!")
            return

        start_time = time.time()

        # Determine capture region based on preset
        preset_name = self.preset_var.get()

        if preset_name == 'custom' and self.custom_region:
            x, y, w, h = self.custom_region
            self.log(f"📷 Capturing custom region...")
            img = self.screen_capture.capture_region(x, y, w, h)
            overlay_pos = (x, y)
        elif preset_name == 'subtitle':
            x, y, w, h = self.screen_capture.get_subtitle_region()
            self.log(f"📷 Capturing subtitle region (bottom 20%)...")
            img = self.screen_capture.capture_region(x, y, w, h)
            overlay_pos = (x, y)
        else:
            self.log("📷 Capturing full screen...")
            img = self.screen_capture.capture_screen()
            overlay_pos = (100, 100)

        if img is None:
            self.log("⏭️  Skipped (rate limited)")
            return

        self.process_image(img, overlay_pos, start_time)

    def toggle_auto_mode(self):
        """Toggle automatic capture mode"""
        if self.auto_var.get():
            if not self.ocr_engine:
                self.auto_var.set(False)
                messagebox.showwarning("Warning", "Initialize OCR engine first!")
                return

            preset = PRESETS.get(self.preset_var.get(), PRESETS['subtitle'])
            self.log(f"🔄 Auto mode enabled (refresh: {preset.refresh_rate}s)")
            self.auto_mode = True
            self.auto_thread = threading.Thread(target=self.auto_capture_loop, daemon=True)
            self.auto_thread.start()
        else:
            self.log("⏸️  Auto mode disabled")
            self.auto_mode = False

    def auto_capture_loop(self):
        """Auto capture loop"""
        preset = PRESETS.get(self.preset_var.get(), PRESETS['subtitle'])

        while self.auto_mode:
            try:
                self.capture_and_translate()
                time.sleep(preset.refresh_rate)
            except Exception as e:
                print(f"Auto capture error: {e}")
                time.sleep(2)

    def process_image(self, image: np.ndarray, overlay_pos: Tuple[int, int], start_time: float):
        """Process captured image: OCR + Translation"""
        try:
            preset_name = self.preset_var.get()
            preset = PRESETS.get(preset_name, PRESETS['subtitle'])

            # OCR
            self.log("🔍 Performing OCR...")
            text = self.ocr_engine.extract_text_combined(
                image,
                preprocess=preset.image_preprocessing,
                preset=preset_name
            )

            if not text:
                self.log("⚠️  No new text detected")
                return

            self.log(f"✓ Text: {text[:50]}{'...' if len(text) > 50 else ''}")

            # Translate
            self.log("🔄 Translating...")
            result = self.translation_engine.translate(text)

            if result:
                process_time = time.time() - start_time
                self.update_performance_info(process_time)

                self.log(f"✅ Done [{result.language} → {self.lang_var.get()}] in {process_time:.2f}s")

                # Show overlay
                x, y = overlay_pos
                self.overlay.create_overlay(x, y, 550, 280)
                self.overlay.update_text(
                    result.original_text,
                    result.translated_text,
                    result.language
                )
            else:
                self.log("❌ Translation failed")

        except Exception as e:
            self.log(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Main entry point"""
    root = tk.Tk()

    # Windows 11 DPI awareness
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    app = ScreenTranslatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
