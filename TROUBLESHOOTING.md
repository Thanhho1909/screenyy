# 🔧 Quick Fix for Installation Errors

## ❌ Error: "scikit-image" build failed

Nếu bạn thấy lỗi này khi chạy `setup.bat`:

```
ERROR: Unknown compiler(s): [['cl'], ['gcc'], ['clang']]
error: metadata-generation-failed
× Encountered error while generating package metadata.
╰─> scikit-image
```

### 💡 Giải pháp nhanh (Chọn 1 trong 3)

#### **Giải pháp 1: Dùng setup script mới (ĐỀ XUẤT)**

```cmd
# Dùng setup script đã fix lỗi
setup_windows.bat
```

Script này sẽ:
- Tự động bỏ qua scikit-image (không bắt buộc)
- Cài đặt từng package riêng lẻ
- Xử lý lỗi một cách graceful

#### **Giải pháp 2: Cài thủ công (nếu Solution 1 fail)**

```cmd
# 1. Kích hoạt venv
venv\Scripts\activate

# 2. Cài core packages (bỏ qua scikit-image)
pip install mss pillow numpy opencv-python googletrans==4.0.0rc1

# 3. Cài PyTorch (CPU version)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 4. Cài EasyOCR (bỏ qua dependencies đã cài)
pip install easyocr --no-deps
pip install python-bidi PyYAML opencv-python-headless scipy

# 5. Test
python -c "import easyocr; print('OK!')"
```

#### **Giải pháp 3: Dùng Python 3.10 hoặc 3.11**

Python 3.14 quá mới, nhiều package chưa có pre-built wheel.

```cmd
# 1. Gỡ Python 3.14
# 2. Tải và cài Python 3.11 từ: https://www.python.org/downloads/
# 3. Chạy lại setup.bat
```

### ✅ Kiểm tra cài đặt

Sau khi cài xong, test:

```cmd
venv\Scripts\activate
python test_installation.py
```

### 🚀 Chạy app ngay (nếu không muốn sửa lỗi)

Bạn có thể chạy version đơn giản không cần scikit-image:

```cmd
venv\Scripts\activate
python screen_translator.py
```

EasyOCR sẽ vẫn hoạt động, chỉ thiếu một vài tính năng preprocessing nâng cao (không ảnh hưởng nhiều).

### 📋 Packages bắt buộc vs tùy chọn

**Bắt buộc (MUST HAVE):**
- ✅ mss (screen capture)
- ✅ pillow (image processing)
- ✅ numpy (arrays)
- ✅ opencv-python (image ops)
- ✅ googletrans (translation)
- ✅ torch + torchvision (OCR backend)
- ✅ easyocr (OCR engine)

**Tùy chọn (NICE TO HAVE):**
- ⚠️ scikit-image (advanced preprocessing) - Có thể bỏ qua!

### 🆘 Vẫn không được?

Liên hệ qua GitHub issues hoặc thử:

**Option A: Dùng pre-built package (nếu có)**
```cmd
pip install scikit-image --only-binary :all:
```

**Option B: Cài Visual Studio Build Tools**
1. Tải từ: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Cài "Desktop development with C++"
3. Chạy lại setup.bat

**Option C: Dùng Docker (advanced)**
```cmd
docker pull python:3.11
# ... setup trong container
```

---

## ✨ Tóm tắt cho người bận

```cmd
# Cách nhanh nhất:
setup_windows.bat

# Nếu lỗi:
venv\Scripts\activate
pip install mss pillow numpy opencv-python googletrans==4.0.0rc1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install easyocr

# Chạy app:
python screen_translator.py
```

Done! 🎉
