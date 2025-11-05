# 🌍 Screen Translator

Công cụ dịch trực tiếp mọi thứ đang hiển thị trên màn hình - phụ đề phim, truyện tranh, text trong game, và nhiều hơn nữa!

## ✨ Tính năng

- 📸 **Chụp màn hình**: Chụp toàn bộ màn hình hoặc vùng được chọn
- 🔍 **OCR đa ngôn ngữ**: Nhận diện text từ nhiều ngôn ngữ (Tiếng Anh, Nhật, Hàn, Trung, Thái, v.v.)
- 🌐 **Dịch tự động**: Dịch sang tiếng Việt hoặc ngôn ngữ khác
- 🎯 **Overlay trong suốt**: Hiển thị kết quả dịch ngay trên màn hình
- 🔄 **Chế độ tự động**: Tự động chụp và dịch liên tục
- 🎨 **Giao diện thân thiện**: GUI đơn giản, dễ sử dụng

## 📋 Yêu cầu hệ thống

- Python 3.8 trở lên
- Hệ điều hành: Windows, Linux, hoặc macOS
- RAM: Tối thiểu 4GB (khuyến nghị 8GB cho OCR)
- Kết nối internet (cho dịch thuật)

## 🚀 Cài đặt

### 1. Clone repository

```bash
git clone https://github.com/Thanhho1909/screenyy.git
cd screenyy
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

**Lưu ý**:
- Lần đầu chạy, EasyOCR sẽ tự động tải các model OCR (~500MB - 1GB)
- Quá trình này có thể mất vài phút tùy vào tốc độ internet

### 3. Cài đặt Tkinter (nếu chưa có)

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
```bash
brew install python-tk
```

**Windows:**
Tkinter thường đã được cài sẵn với Python

## 💻 Sử dụng

### Chạy ứng dụng GUI

```bash
python screen_translator.py
```

### Hướng dẫn sử dụng

1. **Khởi động OCR Engine**
   - Click nút "🔧 Initialize OCR Engine"
   - Đợi một chút để engine khởi tạo (chỉ làm 1 lần khi mở app)

2. **Chọn ngôn ngữ đích**
   - Chọn ngôn ngữ bạn muốn dịch sang (mặc định: Tiếng Việt)

3. **Chọn chế độ chụp**
   - **📷 Capture Full Screen**: Chụp toàn bộ màn hình
   - **✂️ Select Region**: Chọn vùng cụ thể trên màn hình
   - **🔄 Auto Mode**: Tự động chụp và dịch mỗi 2 giây

4. **Xem kết quả**
   - Kết quả dịch sẽ hiển thị trong cửa sổ overlay trong suốt
   - Cửa sổ luôn ở trên cùng để bạn có thể xem trong khi làm việc khác

## 🎯 Use Cases

### 1. Xem phim với phụ đề nước ngoài
```
- Mở video có phụ đề tiếng Anh/Nhật/Hàn
- Bật Auto Mode
- Phụ đề sẽ được dịch tự động sang tiếng Việt
```

### 2. Đọc truyện tranh/manga
```
- Mở trang truyện
- Click "Select Region" và chọn vùng có text
- Text sẽ được nhận diện và dịch
```

### 3. Chơi game nước ngoài
```
- Mở game
- Sử dụng Auto Mode hoặc Capture Full Screen khi cần
- Hiểu ngay lời thoại và hướng dẫn trong game
```

### 4. Đọc tài liệu/website
```
- Mở tài liệu PDF hoặc website
- Chụp vùng cần dịch
- Nhận bản dịch ngay lập tức
```

## ⚙️ Cấu hình

### Thay đổi ngôn ngữ OCR

Mở file `screen_translator.py` và tìm dòng:

```python
def __init__(self, languages: List[str] = ['en', 'ja', 'ko', 'zh_sim', 'th']):
```

Thêm hoặc bớt mã ngôn ngữ theo nhu cầu:
- `en`: Tiếng Anh
- `ja`: Tiếng Nhật
- `ko`: Tiếng Hàn
- `zh_sim`: Tiếng Trung giản thể
- `zh_tra`: Tiếng Trung phồn thể
- `th`: Tiếng Thái
- `vi`: Tiếng Việt
- ... [Xem danh sách đầy đủ tại EasyOCR docs]

### Tùy chỉnh thời gian Auto Mode

Tìm dòng trong hàm `auto_capture_loop`:

```python
time.sleep(2)  # Thay đổi số giây tại đây
```

## 🔧 Troubleshooting

### OCR không nhận diện được text

- Đảm bảo text trong ảnh đủ rõ nét và lớn
- Thử tăng kích thước vùng capture
- Kiểm tra ngôn ngữ OCR có được cấu hình đúng không

### Dịch thuật bị lỗi

- Kiểm tra kết nối internet
- Google Translate có thể giới hạn số request, đợi một chút rồi thử lại
- Xem xét sử dụng translation API khác nếu cần

### Ứng dụng chạy chậm

- OCR và dịch thuật cần thời gian xử lý
- Giảm tần suất chụp trong Auto Mode
- Giảm kích thước vùng capture
- Cân nhắc sử dụng GPU cho OCR (cài đặt PyTorch với CUDA)

### Lỗi import module

```bash
# Cài đặt lại dependencies
pip install -r requirements.txt --upgrade
```

## 🎨 Screenshots

```
+---------------------------+
|   🌍 Screen Translator    |
+---------------------------+
| Target Language:          |
|  ○ Vietnamese (Tiếng Việt)|
|  ○ English                |
|  ○ Japanese (日本語)       |
+---------------------------+
| Capture Mode:             |
| [📷 Capture Full Screen]  |
| [✂️ Select Region]        |
| ☑ 🔄 Auto Mode            |
+---------------------------+
| Status:                   |
| [2024-01-01 10:30:15]     |
| ✓ OCR initialized         |
| ✓ Detected text: こんにち...|
| ✓ Translation complete    |
+---------------------------+
```

## 🤝 Contributing

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📝 TODO

- [ ] Thêm region selection bằng cách kéo chuột
- [ ] Hỗ trợ hotkey toàn cục (ví dụ: Ctrl+Shift+T)
- [ ] Lưu lịch sử dịch
- [ ] Xuất kết quả ra file
- [ ] Hỗ trợ thêm translation engine (DeepL, Azure, v.v.)
- [ ] Tối ưu hóa performance với GPU
- [ ] Thêm chế độ "click to translate" tại vị trí con trỏ chuột

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết

## 🙏 Credits

- [EasyOCR](https://github.com/JaidedAI/EasyOCR) - OCR engine
- [googletrans](https://github.com/ssut/py-googletrans) - Translation API
- [mss](https://github.com/BoboTiG/python-mss) - Screen capture

## 📧 Contact

Nếu bạn có câu hỏi hoặc đề xuất, vui lòng mở issue trên GitHub!

---

Made with ❤️ for the community
