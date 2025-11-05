# 📖 Hướng dẫn sử dụng chi tiết Screen Translator

## 📑 Mục lục

1. [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
2. [Cài đặt từng bước](#cài-đặt-từng-bước)
3. [Chạy ứng dụng lần đầu](#chạy-ứng-dụng-lần-đầu)
4. [Hướng dẫn sử dụng GUI](#hướng-dẫn-sử-dụng-gui)
5. [Hướng dẫn sử dụng CLI](#hướng-dẫn-sử-dụng-cli)
6. [Các tình huống sử dụng thực tế](#các-tình-huống-sử-dụng-thực-tế)
7. [Xử lý lỗi](#xử-lý-lỗi)
8. [Tips & Tricks](#tips--tricks)

---

## Yêu cầu hệ thống

### Phần cứng tối thiểu:
- CPU: Dual-core 2.0 GHz trở lên
- RAM: 4GB (khuyến nghị 8GB)
- Dung lượng đĩa trống: 2GB (cho dependencies và OCR models)
- Kết nối internet: Cần thiết cho translation và tải OCR models lần đầu

### Phần mềm:
- Python 3.8 hoặc mới hơn
- pip (Python package manager)
- tkinter (thường đi kèm Python, nhưng có thể cần cài riêng trên Linux)

### Hệ điều hành:
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Ubuntu 20.04+ / Debian 10+ / Fedora 30+
- ✅ Các distro Linux khác (có thể cần cài thêm packages)

---

## Cài đặt từng bước

### Bước 1: Kiểm tra Python

Mở Terminal (Linux/macOS) hoặc Command Prompt (Windows) và chạy:

```bash
python --version
# hoặc
python3 --version
```

Bạn sẽ thấy output như: `Python 3.10.5`

**Nếu chưa có Python:** Tải từ https://www.python.org/downloads/

### Bước 2: Clone repository

```bash
# Di chuyển đến thư mục bạn muốn lưu dự án
cd ~/Documents  # macOS/Linux
# hoặc
cd C:\Users\YourName\Documents  # Windows

# Clone repository
git clone https://github.com/Thanhho1909/screenyy.git
cd screenyy
```

**Nếu chưa có Git:** Tải từ https://git-scm.com/downloads

### Bước 3: Cài đặt Tkinter (chỉ Linux)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

### Bước 4: Cài đặt dependencies Python

```bash
# Tạo virtual environment (khuyến nghị)
python -m venv venv

# Kích hoạt virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt
```

**Lưu ý:** Quá trình này có thể mất 5-10 phút tùy vào tốc độ internet.

### Bước 5: Kiểm tra cài đặt

```bash
python -c "import mss, easyocr, cv2; print('✓ All dependencies installed!')"
```

Nếu không có lỗi, bạn đã sẵn sàng!

---

## Chạy ứng dụng lần đầu

### Chạy GUI version

```bash
python screen_translator.py
```

Cửa sổ ứng dụng sẽ mở ra:

```
┌─────────────────────────────────────────┐
│       🌍 Screen Translator              │
├─────────────────────────────────────────┤
│  Target Language:                       │
│   ● Vietnamese (Tiếng Việt)            │
│   ○ English                             │
│   ○ Japanese (日本語)                   │
│   ○ Korean (한국어)                     │
│   ○ Chinese (中文)                      │
│   ○ Thai (ไทย)                         │
├─────────────────────────────────────────┤
│  Capture Mode:                          │
│  ┌───────────────────────────────────┐ │
│  │ 📷 Capture Full Screen            │ │
│  └───────────────────────────────────┘ │
│  ┌───────────────────────────────────┐ │
│  │ ✂️ Select Region                  │ │
│  └───────────────────────────────────┘ │
│  ☐ 🔄 Auto Mode (every 2 seconds)     │
├─────────────────────────────────────────┤
│  Status:                                │
│  ┌───────────────────────────────────┐ │
│  │ [10:30:15] Ready! Click           │ │
│  │ 'Initialize OCR Engine' to start. │ │
│  └───────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  ┌───────────────────────────────────┐ │
│  │ 🔧 Initialize OCR Engine          │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

## Hướng dẫn sử dụng GUI

### 🔧 Bước 1: Khởi tạo OCR Engine (QUAN TRỌNG!)

**Lần đầu chạy app:**

1. Click nút **"🔧 Initialize OCR Engine"**

2. Bạn sẽ thấy trong Status:
   ```
   [10:30:20] Initializing OCR engine... This may take a minute...
   ```

3. **QUAN TRỌNG - Lần chạy đầu tiên:**
   - EasyOCR sẽ tự động tải các OCR models (~500MB - 1GB)
   - Quá trình này mất 3-10 phút tùy vào internet
   - Bạn sẽ thấy trong console:
     ```
     Downloading detection model, please wait...
     Downloading recognition model, please wait...
     ```

4. Khi hoàn tất:
   ```
   [10:32:45] ✓ OCR engine initialized successfully!
   ```

**Các lần sau:** OCR khởi động nhanh hơn (10-30 giây) vì models đã được tải sẵn.

### 🌐 Bước 2: Chọn ngôn ngữ đích

Click vào radio button của ngôn ngữ bạn muốn dịch sang:

- **Vietnamese (Tiếng Việt)** - Mặc định
- **English** - Tiếng Anh
- **Japanese (日本語)** - Tiếng Nhật
- **Korean (한국어)** - Tiếng Hàn
- **Chinese (中文)** - Tiếng Trung
- **Thai (ไทย)** - Tiếng Thái

Status sẽ hiển thị:
```
[10:33:00] Target language changed to: vi
```

### 📷 Bước 3: Chụp màn hình

#### **Option 1: Capture Full Screen**

1. Click nút **"📷 Capture Full Screen"**

2. Ứng dụng sẽ:
   - Chụp toàn bộ màn hình
   - Phát hiện text trong ảnh (OCR)
   - Dịch sang ngôn ngữ đích
   - Hiển thị kết quả

3. Status log:
   ```
   [10:33:05] Capturing full screen...
   [10:33:06] Performing OCR...
   [10:33:08] ✓ Detected text: Hello World...
   [10:33:09] Translating...
   [10:33:10] ✓ Translation complete [en → vi]
   [10:33:10] Translation: Xin chào thế giới...
   ```

#### **Option 2: Select Region**

1. Click nút **"✂️ Select Region"**

2. **Hiện tại:** Sẽ chụp vùng giữa màn hình (800x600)
   - *Tính năng select bằng chuột sẽ được thêm trong tương lai*

3. Quá trình tương tự như Full Screen

#### **Option 3: Auto Mode** 🔄

1. Tick vào checkbox **"🔄 Auto Mode (capture every 2 seconds)"**

2. Status:
   ```
   [10:35:00] Auto mode enabled
   ```

3. Ứng dụng sẽ **TỰ ĐỘNG**:
   - Chụp màn hình mỗi 2 giây
   - OCR và dịch
   - Cập nhật overlay

4. **Tắt Auto Mode:** Bỏ tick checkbox

   ```
   [10:37:30] Auto mode disabled
   ```

### 👀 Bước 4: Xem kết quả

Khi có kết quả dịch, một **Overlay Window** sẽ xuất hiện:

```
┌────────────────────────────────────────────┐
│ Translation                           [×]  │
├────────────────────────────────────────────┤
│ [Detected: EN]                             │
│                                            │
│ Original:                                  │
│ Hello World                                │
│ Welcome to Screen Translator               │
│                                            │
│ Translation:                               │
│ Xin chào thế giới                         │
│ Chào mừng đến với Screen Translator       │
│                                            │
└────────────────────────────────────────────┘
```

**Đặc điểm Overlay:**
- Trong suốt 90% (có thể nhìn xuyên qua)
- Luôn ở trên cùng (always on top)
- Có thể di chuyển
- Có scrollbar nếu text dài

---

## Hướng dẫn sử dụng CLI

CLI version phù hợp cho:
- Người dùng quen dòng lệnh
- Scripting/automation
- Chạy trên server không có GUI
- Xử lý batch/nhiều ảnh

### Cú pháp cơ bản

```bash
python translate_cli.py [options]
```

### Các options

| Option | Mô tả | Mặc định |
|--------|-------|----------|
| `--lang CODE` | Ngôn ngữ đích | `vi` |
| `--region X Y W H` | Vùng capture (x y width height) | Full screen |
| `--ocr-langs LANG1 LANG2` | Ngôn ngữ OCR | `en ja ko zh_sim` |
| `--save PATH` | Lưu screenshot | Không lưu |

### Ví dụ sử dụng CLI

#### 1. Dịch toàn màn hình sang tiếng Việt

```bash
python translate_cli.py
```

Output:
```
🌍 Screen Translator CLI
==================================================

📸 Initializing screen capture...
🔧 Initializing OCR engine for languages: en, ja, ko, zh_sim
   (This may take a minute on first run...)
🌐 Initializing translation engine (target: vi)

📷 Capturing screen...
   Full screen

🔍 Performing OCR...
   ✓ Text detected!

==================================================
📝 ORIGINAL TEXT:
==================================================
Hello World
Welcome to Screen Translator

🔄 Translating...
   ✓ Translation complete [en → vi]

==================================================
🌍 TRANSLATION:
==================================================
Xin chào thế giới
Chào mừng đến với Screen Translator

==================================================
```

#### 2. Dịch sang tiếng Anh

```bash
python translate_cli.py --lang en
```

#### 3. Chụp vùng cụ thể

```bash
# Chụp vùng: x=100, y=100, width=800, height=600
python translate_cli.py --region 100 100 800 600
```

#### 4. Lưu screenshot

```bash
python translate_cli.py --save screenshot.png
```

Output sẽ có thêm:
```
📷 Capturing screen...
   ✓ Screenshot saved to: screenshot.png
```

#### 5. Chỉ định ngôn ngữ OCR

```bash
# Chỉ nhận diện tiếng Nhật và Anh
python translate_cli.py --ocr-langs ja en --lang vi
```

#### 6. Kết hợp nhiều options

```bash
python translate_cli.py \
  --lang vi \
  --region 200 150 1000 700 \
  --ocr-langs ja en \
  --save my_screenshot.png
```

---

## Các tình huống sử dụng thực tế

### 🎬 Tình huống 1: Xem anime với phụ đề tiếng Nhật

**Mục tiêu:** Dịch phụ đề anime sang tiếng Việt real-time

**Các bước:**

1. Mở video anime (VLC, browser, etc.)

2. Chạy Screen Translator:
   ```bash
   python screen_translator.py
   ```

3. Initialize OCR Engine (lần đầu)

4. Chọn target language: **Vietnamese**

5. **Bật Auto Mode** ✓

6. Play anime

7. Overlay sẽ tự động cập nhật phụ đề đã dịch mỗi 2 giây

**Tips:**
- Đặt overlay window ở vị trí không che khuất phụ đề gốc
- Nếu phụ đề thay đổi nhanh, có thể giảm thời gian Auto Mode (sửa trong code)
- Sử dụng region capture để chỉ chụp vùng phụ đề → nhanh hơn

### 📚 Tình huống 2: Đọc manga/manhwa online

**Mục tiêu:** Dịch text trong truyện tranh

**Các bước:**

1. Mở trang web manga (ví dụ: manga tiếng Nhật)

2. Chạy Screen Translator

3. Initialize OCR

4. Chọn language: Vietnamese

5. Click **"✂️ Select Region"** hoặc **"📷 Capture Full Screen"**

6. Đọc bản dịch trong overlay

7. Khi chuyển trang, click lại để dịch trang mới

**Với CLI (nếu muốn lưu ảnh):**
```bash
python translate_cli.py --save page1.png
```

### 🎮 Tình huống 3: Chơi game nước ngoài

**Mục tiêu:** Dịch dialog/quest trong game

**Ví dụ:** Game Nhật không có tiếng Việt

1. Chạy game

2. Chạy Screen Translator với Auto Mode OFF (để không lag)

3. Khi có dialog/quest cần dịch:
   - **Pause game** (nếu được)
   - Click **"📷 Capture Full Screen"**
   - Đọc bản dịch
   - Resume game

**Tips:**
- Nếu game chạy fullscreen, chuyển sang Windowed mode để dễ thao tác
- Có thể dùng 2 màn hình: game ở màn 1, translator ở màn 2

### 📄 Tình huống 4: Đọc PDF/tài liệu nước ngoài

**Mục tiêu:** Dịch tài liệu học tập/nghiên cứu

**Các bước:**

1. Mở PDF bằng viewer (Adobe Reader, browser, etc.)

2. Zoom đến kích thước text rõ ràng

3. Chạy Screen Translator

4. Capture từng phần cần dịch

**CLI workflow:**
```bash
# Dịch và lưu kết quả
python translate_cli.py --region 100 100 1200 800 > translation.txt
```

### 🌐 Tình huống 5: Dịch website

**Mục tiêu:** Đọc blog/news tiếng nước ngoài

**Các bước:**

1. Mở website trong browser

2. **Select text cần dịch** và scroll đến vị trí cần

3. Chạy Screen Translator

4. Capture region/full screen

**Lưu ý:**
- Với website, có thể dùng Google Translate extension nhanh hơn
- Screen Translator hữu ích khi text là ảnh (không copy được)

---

## Xử lý lỗi

### ❌ Lỗi 1: "No module named 'tkinter'"

**Nguyên nhân:** Tkinter chưa được cài đặt

**Giải pháp:**

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (thường đã có sẵn, nếu không)
brew install python-tk

# Windows: Reinstall Python và check "tcl/tk" option
```

### ❌ Lỗi 2: "Cannot initialize OCR engine"

**Nguyên nhân:**
- Không có internet (cần tải models)
- Không đủ dung lượng đĩa
- Lỗi download

**Giải pháp:**

1. Kiểm tra internet: `ping google.com`

2. Kiểm tra dung lượng: `df -h` (Linux/macOS) hoặc check trong File Explorer (Windows)

3. Thử xóa cache và tải lại:
   ```bash
   rm -rf ~/.EasyOCR/model/
   python screen_translator.py
   ```

4. Kiểm tra log chi tiết trong console

### ❌ Lỗi 3: "Translation failed"

**Nguyên nhân:**
- Mất internet
- Google Translate rate limit
- Text rỗng/không hợp lệ

**Giải pháp:**

1. Kiểm tra internet

2. Đợi vài giây rồi thử lại (rate limit tự reset)

3. Kiểm tra text có được detect không (xem Status log)

### ❌ Lỗi 4: "No text detected in image"

**Nguyên nhân:**
- Ảnh quá mờ/nhỏ
- Font chữ không được OCR hỗ trợ
- Ảnh toàn màu/background phức tạp
- Ngôn ngữ không được config

**Giải pháp:**

1. **Tăng kích thước/zoom** nội dung cần dịch

2. **Capture vùng nhỏ hơn** tập trung vào text

3. **Kiểm tra ngôn ngữ OCR:**
   - Mở `screen_translator.py`
   - Tìm dòng `OCREngine(languages=['en', 'ja', ...])`
   - Thêm ngôn ngữ cần thiết

4. **Tăng độ tương phản:** Nếu text màu nhạt

### ❌ Lỗi 5: App chạy rất chậm

**Nguyên nhân:**
- OCR/Translation tốn thời gian
- Ảnh quá lớn (full 4K screen)
- Không có GPU

**Giải pháp:**

1. **Dùng region capture** thay vì full screen

2. **Tăng thời gian Auto Mode:**
   - Sửa `time.sleep(2)` thành `time.sleep(5)` trong code

3. **Giảm số ngôn ngữ OCR:**
   - Chỉ giữ ngôn ngữ cần thiết

4. **Sử dụng GPU cho OCR** (nếu có):
   ```bash
   # Cài PyTorch với CUDA
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

   # Sửa trong screen_translator.py:
   # self.reader = easyocr.Reader(languages, gpu=True)
   ```

### ❌ Lỗi 6: "Permission denied" khi chụp màn hình

**Nguyên nhân:** Hệ điều hành chặn screen capture

**Giải pháp:**

**macOS:**
```
System Preferences → Security & Privacy → Privacy → Screen Recording
→ Cho phép Terminal/Python
```

**Linux (Wayland):**
- Wayland có thể có vấn đề với screen capture
- Thử chuyển sang X11 hoặc dùng tool khác

---

## Tips & Tricks

### 💡 Tip 1: Tăng độ chính xác OCR

1. **Zoom/phóng to** text trước khi capture
2. **Capture vùng nhỏ** chứa text rõ ràng
3. **Tăng độ tương phản** màn hình
4. **Font rõ ràng** dễ nhận diện hơn font nghệ thuật

### 💡 Tip 2: Tăng tốc độ

1. **Giảm resolution** capture (dùng region thay vì full screen)
2. **Giảm số ngôn ngữ OCR** xuống còn cái cần thiết
3. **Tắt Auto Mode** khi không dùng
4. **Sử dụng GPU** nếu có

### 💡 Tip 3: Sử dụng hotkey (cần implement)

Hiện tại chưa có hotkey, nhưng bạn có thể:
- Sử dụng AutoHotkey (Windows) hoặc Hammerspoon (macOS) để gán phím tắt
- Script click vào button "Capture Full Screen"

### 💡 Tip 4: Dịch offline (không cần internet)

Hiện tại tool cần internet cho translation. Để offline:

1. Thay Google Translate bằng offline translation model
2. Cài đặt `translate` package (offline)
3. Hoặc dùng local LLM (llama.cpp, etc.)

**Sẽ update trong tương lai!**

### 💡 Tip 5: Lưu lịch sử dịch

Hiện chưa có feature này, nhưng bạn có thể:

**CLI:**
```bash
python translate_cli.py > translation_$(date +%Y%m%d_%H%M%S).txt
```

**GUI:** Tự copy từ overlay window

### 💡 Tip 6: Dịch nhiều ngôn ngữ cùng lúc

Chỉnh sửa code để hiển thị nhiều bản dịch:

```python
# Trong TranslationEngine.translate()
# Dịch sang nhiều ngôn ngữ:
for lang in ['vi', 'en', 'ja']:
    result = self.translator.translate(text, dest=lang)
    # Hiển thị tất cả
```

### 💡 Tip 7: Chạy trên 2 màn hình

- Màn 1: Content cần dịch (video/game/document)
- Màn 2: Screen Translator app + Overlay

Hoặc dùng monitor selection trong code:
```python
# Chụp màn hình thứ 2
img = self.screen_capture.capture_screen(monitor_number=2)
```

---

## 🎓 Workflow đề xuất

### Workflow 1: Xem video có phụ đề

```
1. Mở video
2. python screen_translator.py
3. Initialize OCR (lần đầu)
4. Select language
5. ✓ Enable Auto Mode
6. Enjoy video với phụ đề dịch!
```

### Workflow 2: Đọc tài liệu

```
1. Mở PDF/document
2. python screen_translator.py
3. Initialize OCR
4. Select language
5. Capture từng phần cần đọc
6. Copy bản dịch nếu cần lưu
```

### Workflow 3: Batch processing nhiều ảnh

```bash
# Tạo script
for img in screenshots/*.png; do
    # Xử lý từng ảnh
    # (Cần modify code để đọc từ file)
done
```

---

## 📞 Hỗ trợ

Nếu gặp vấn đề không có trong tài liệu:

1. Kiểm tra console output để xem lỗi chi tiết
2. Mở issue trên GitHub với thông tin:
   - OS và version
   - Python version
   - Lỗi message đầy đủ
   - Steps to reproduce

---

**Chúc bạn sử dụng Screen Translator hiệu quả!** 🎉
