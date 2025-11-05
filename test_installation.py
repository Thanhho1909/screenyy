#!/usr/bin/env python3
"""
Test installation of Screen Translator dependencies
"""

import sys

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    if package_name is None:
        package_name = module_name

    try:
        __import__(module_name)
        print(f"✅ {package_name:25s} - OK")
        return True
    except ImportError as e:
        print(f"❌ {package_name:25s} - FAILED: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {package_name:25s} - WARNING: {e}")
        return False


def main():
    print("=" * 60)
    print("Screen Translator - Installation Test")
    print("=" * 60)
    print()

    results = {}

    print("Core Dependencies (REQUIRED):")
    print("-" * 60)
    results['mss'] = test_import('mss', 'mss (screen capture)')
    results['PIL'] = test_import('PIL', 'Pillow (image processing)')
    results['numpy'] = test_import('numpy', 'numpy (arrays)')
    results['cv2'] = test_import('cv2', 'opencv-python (image ops)')
    results['googletrans'] = test_import('googletrans', 'googletrans (translation)')
    print()

    print("OCR Dependencies (REQUIRED):")
    print("-" * 60)
    results['torch'] = test_import('torch', 'PyTorch (OCR backend)')
    results['torchvision'] = test_import('torchvision', 'torchvision')
    results['easyocr'] = test_import('easyocr', 'EasyOCR (OCR engine)')
    print()

    print("Optional Dependencies:")
    print("-" * 60)
    results['scipy'] = test_import('scipy', 'scipy (optimization)')
    results['skimage'] = test_import('skimage', 'scikit-image (preprocessing)')
    print()

    print("GUI Dependencies:")
    print("-" * 60)
    try:
        import tkinter as tk
        print(f"✅ {'Tkinter (GUI)':25s} - OK (version {tk.TkVersion})")
        results['tkinter'] = True
    except:
        print(f"❌ {'Tkinter (GUI)':25s} - FAILED")
        results['tkinter'] = False
    print()

    # Summary
    print("=" * 60)
    print("Summary:")
    print("=" * 60)

    required = ['mss', 'PIL', 'numpy', 'cv2', 'googletrans', 'torch', 'torchvision', 'easyocr', 'tkinter']
    optional = ['scipy', 'skimage']

    required_ok = sum(1 for k in required if results.get(k, False))
    optional_ok = sum(1 for k in optional if results.get(k, False))

    print(f"Required packages: {required_ok}/{len(required)} installed")
    print(f"Optional packages: {optional_ok}/{len(optional)} installed")
    print()

    if required_ok == len(required):
        print("✅ SUCCESS! All required packages are installed.")
        print()
        print("You can now run:")
        print("  python screen_translator.py")
        print("  or")
        print("  python screen_translator_optimized.py")
        print()
        return 0
    else:
        print("❌ INCOMPLETE! Some required packages are missing.")
        print()
        print("Please install missing packages:")

        missing = [k for k in required if not results.get(k, False)]
        for pkg in missing:
            if pkg == 'PIL':
                print(f"  pip install pillow")
            elif pkg == 'cv2':
                print(f"  pip install opencv-python")
            else:
                print(f"  pip install {pkg}")
        print()
        print("Or run: setup_windows.bat")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
