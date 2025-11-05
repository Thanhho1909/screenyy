# 🚀 Quick Start Guide

Hướng dẫn nhanh để bắt đầu sử dụng Screen Translator trong 5 phút!

## ⚡ Cài đặt nhanh

```bash
# 1. Clone repository
git clone https://github.com/Thanhho1909/screenyy.git
cd screenyy

# 2. Cài đặt dependencies
pip install -r requirements.txt

# 3. Chạy ứng dụng
python screen_translator.py
```

## 🎯 Sử dụng cơ bản

### GUI Mode (Đề xuất cho người mới)

1. Chạy ứng dụng:
   ```bash
   python screen_translator.py
   ```

2. Click "🔧 Initialize OCR Engine" (chỉ làm 1 lần khi mở app)

3. Chọn ngôn ngữ đích (mặc định: Tiếng Việt)

4. Click "📷 Capture Full Screen" để chụp và dịch toàn màn hình

5. Xem kết quả trong cửa sổ overlay!

### CLI Mode (Cho người dùng nâng cao)

```bash
# Dịch toàn màn hình
python translate_cli.py

# Dịch với ngôn ngữ đích cụ thể
python translate_cli.py --lang en

# Dịch vùng cụ thể (x, y, width, height)
python translate_cli.py --region 100 100 800 600

# Lưu screenshot
python translate_cli.py --save screenshot.png
```

## 💡 Ví dụ sử dụng

### 1. Xem anime với phụ đề Nhật

```bash
# Mở video anime
# Chạy Screen Translator
python screen_translator.py

# Bật Auto Mode để tự động dịch phụ đề
```

### 2. Đọc manga/manhwa

```bash
# Mở trang manga
# Chạy và click "Select Region"
# Chọn vùng có text cần dịch
```

### 3. Chơi game tiếng Anh

```bash
# Chơi game
# Nhấn "Capture Full Screen" khi có dialog/text cần dịch
# Hoặc bật Auto Mode để dịch liên tục
```

## 🔧 Tips & Tricks

### Tăng độ chính xác OCR

- Đảm bảo text rõ ràng, không bị mờ
- Tăng resolution/zoom của ứng dụng gốc
- Chọn vùng capture nhỏ hơn, tập trung vào text

### Tăng tốc độ

- Giảm số ngôn ngữ OCR (chỉ giữ những ngôn ngữ cần thiết)
- Sử dụng region capture thay vì full screen
- Tăng thời gian chờ trong Auto Mode (trong code)

### Sử dụng GPU cho OCR nhanh hơn

```bash
# Cài đặt PyTorch với CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Sửa trong screen_translator.py:
# self.reader = easyocr.Reader(languages, gpu=True)  # Đổi gpu=False thành gpu=True
```

## 🐛 Xử lý lỗi thường gặp

### "No module named 'tkinter'"

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### "Cannot initialize OCR engine"

- Kiểm tra kết nối internet (cần tải model lần đầu)
- Kiểm tra dung lượng đĩa (cần ~1GB cho OCR models)

### "Translation failed"

- Kiểm tra kết nối internet
- Thử lại sau vài giây (Google Translate có rate limit)

## 📚 Đọc thêm

- [README.md](README.md) - Tài liệu đầy đủ
- [Issues](https://github.com/Thanhho1909/screenyy/issues) - Báo cáo lỗi và đề xuất tính năng

## 🎉 Hoàn thành!

Bây giờ bạn đã sẵn sàng sử dụng Screen Translator! Chúc bạn có trải nghiệm tuyệt vời!

---

**Câu hỏi?** Mở issue trên GitHub hoặc xem README.md để biết thêm chi tiết.
