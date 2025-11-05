# 🔧 Hướng dẫn cài đặt chi tiết theo từng hệ điều hành

## 📑 Mục lục
- [Windows 10/11](#windows-1011)
- [macOS](#macos)
- [Ubuntu/Debian](#ubuntudebian)
- [Fedora/RHEL](#fedorarhel)
- [Arch Linux](#arch-linux)
- [Xử lý lỗi cài đặt](#xử-lý-lỗi-cài-đặt)

---

## Windows 10/11

### Bước 1: Cài đặt Python

1. Truy cập https://www.python.org/downloads/

2. Tải **Python 3.10** hoặc mới hơn (khuyến nghị 3.10.x hoặc 3.11.x)

3. Chạy installer:
   - ✅ **QUAN TRỌNG:** Check "Add Python to PATH"
   - ✅ Check "Install pip"
   - Click "Install Now"

4. Kiểm tra cài đặt:
   ```cmd
   python --version
   pip --version
   ```

### Bước 2: Cài đặt Git (nếu chưa có)

1. Tải từ https://git-scm.com/download/win

2. Chạy installer với cài đặt mặc định

3. Kiểm tra:
   ```cmd
   git --version
   ```

### Bước 3: Clone repository

```cmd
# Mở Command Prompt hoặc PowerShell

# Di chuyển đến thư mục muốn lưu
cd C:\Users\YourName\Documents

# Clone
git clone https://github.com/Thanhho1909/screenyy.git
cd screenyy
```

### Bước 4: Tạo Virtual Environment (khuyến nghị)

```cmd
# Tạo venv
python -m venv venv

# Kích hoạt
venv\Scripts\activate

# Prompt sẽ có (venv) ở đầu
```

### Bước 5: Cài đặt dependencies

```cmd
# Upgrade pip
python -m pip install --upgrade pip

# Cài đặt requirements
pip install -r requirements.txt
```

**Lưu ý:** Quá trình này mất 5-10 phút. Bạn sẽ thấy nhiều packages đang được download.

### Bước 6: Chạy ứng dụng

```cmd
# Chạy GUI
python screen_translator.py

# Hoặc CLI
python translate_cli.py
```

### Xử lý lỗi Windows

#### Lỗi: "python is not recognized"

**Giải pháp:** Thêm Python vào PATH

1. Search "Environment Variables" trong Start Menu
2. Click "Environment Variables"
3. Trong "System Variables", tìm "Path"
4. Click "Edit" → "New"
5. Thêm:
   ```
   C:\Users\YourName\AppData\Local\Programs\Python\Python310\
   C:\Users\YourName\AppData\Local\Programs\Python\Python310\Scripts\
   ```
6. OK → Khởi động lại Command Prompt

#### Lỗi: "Microsoft Visual C++ 14.0 is required"

**Giải pháp:**

1. Tải "Microsoft C++ Build Tools" từ: https://visualstudio.microsoft.com/visual-cpp-build-tools/

2. Cài đặt "Desktop development with C++"

3. Chạy lại `pip install -r requirements.txt`

#### Lỗi: "Access denied" khi cài package

**Giải pháp:**

```cmd
# Chạy Command Prompt as Administrator
# Hoặc thêm --user
pip install -r requirements.txt --user
```

---

## macOS

### Bước 1: Cài đặt Homebrew (nếu chưa có)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Bước 2: Cài đặt Python

```bash
# Cài Python 3.10 hoặc 3.11
brew install python@3.10

# Kiểm tra
python3 --version
pip3 --version
```

### Bước 3: Cài đặt Git (thường đã có sẵn)

```bash
# Kiểm tra
git --version

# Nếu chưa có, cài qua Homebrew
brew install git
```

### Bước 4: Clone repository

```bash
# Mở Terminal

# Di chuyển đến thư mục
cd ~/Documents

# Clone
git clone https://github.com/Thanhho1909/screenyy.git
cd screenyy
```

### Bước 5: Tạo Virtual Environment

```bash
# Tạo venv
python3 -m venv venv

# Kích hoạt
source venv/bin/activate

# Prompt sẽ có (venv) ở đầu
```

### Bước 6: Cài đặt dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Cài đặt requirements
pip install -r requirements.txt
```

### Bước 7: Cấp quyền Screen Recording

**QUAN TRỌNG cho macOS:**

1. Chạy app lần đầu:
   ```bash
   python screen_translator.py
   ```

2. macOS sẽ hiện popup xin quyền Screen Recording

3. Hoặc cấu hình thủ công:
   ```
   System Preferences
   → Security & Privacy
   → Privacy
   → Screen Recording
   → ✓ Terminal (hoặc iTerm)
   ```

4. **Restart Terminal** sau khi cấp quyền

### Bước 8: Chạy ứng dụng

```bash
# GUI
python screen_translator.py

# CLI
python translate_cli.py
```

### Xử lý lỗi macOS

#### Lỗi: "command not found: python"

**Giải pháp:** Dùng `python3` thay vì `python`

```bash
# Tạo alias (thêm vào ~/.zshrc hoặc ~/.bash_profile)
alias python=python3
alias pip=pip3
```

#### Lỗi: "xcrun: error: invalid active developer path"

**Giải pháp:**

```bash
xcode-select --install
```

#### Lỗi: Tkinter không hoạt động

**Giải pháp:**

```bash
# Cài lại Python với tkinter support
brew reinstall python-tk@3.10
```

#### Lỗi: "Permission denied" khi capture screen

Xem Bước 7 phía trên để cấp quyền Screen Recording

---

## Ubuntu/Debian

### Bước 1: Update system

```bash
sudo apt-get update
sudo apt-get upgrade
```

### Bước 2: Cài đặt Python và dependencies

```bash
# Cài Python 3.10+ (Ubuntu 22.04+ đã có sẵn)
sudo apt-get install python3 python3-pip python3-venv

# Cài Tkinter
sudo apt-get install python3-tk

# Cài các dependencies cho OpenCV
sudo apt-get install python3-dev
sudo apt-get install libgl1-mesa-glx
sudo apt-get install libglib2.0-0
```

### Bước 3: Cài đặt Git

```bash
sudo apt-get install git
```

### Bước 4: Clone repository

```bash
cd ~/Documents  # hoặc thư mục khác
git clone https://github.com/Thanhho1909/screenyy.git
cd screenyy
```

### Bước 5: Tạo Virtual Environment

```bash
# Tạo venv
python3 -m venv venv

# Kích hoạt
source venv/bin/activate
```

### Bước 6: Cài đặt dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Cài requirements
pip install -r requirements.txt
```

### Bước 7: Chạy ứng dụng

```bash
# GUI
python screen_translator.py

# CLI
python translate_cli.py
```

### Xử lý lỗi Ubuntu/Debian

#### Lỗi: "No module named '_tkinter'"

```bash
sudo apt-get install python3-tk
```

#### Lỗi: "ImportError: libGL.so.1"

```bash
sudo apt-get install libgl1-mesa-glx
```

#### Lỗi: "ImportError: libgthread-2.0.so.0"

```bash
sudo apt-get install libglib2.0-0
```

#### Lỗi: Screen capture không hoạt động trên Wayland

**Giải pháp:** Chuyển sang X11

```bash
# Logout
# Tại màn hình login, click icon gear
# Chọn "Ubuntu on Xorg" thay vì "Ubuntu"
# Login lại
```

---

## Fedora/RHEL

### Bước 1: Update system

```bash
sudo dnf update
```

### Bước 2: Cài đặt Python và dependencies

```bash
# Cài Python
sudo dnf install python3 python3-pip python3-devel

# Cài Tkinter
sudo dnf install python3-tkinter

# Dependencies cho OpenCV
sudo dnf install mesa-libGL
```

### Bước 3: Cài Git

```bash
sudo dnf install git
```

### Bước 4-7: Giống Ubuntu

```bash
# Clone
git clone https://github.com/Thanhho1909/screenyy.git
cd screenyy

# Venv
python3 -m venv venv
source venv/bin/activate

# Install
pip install --upgrade pip
pip install -r requirements.txt

# Run
python screen_translator.py
```

---

## Arch Linux

### Bước 1: Update system

```bash
sudo pacman -Syu
```

### Bước 2: Cài đặt Python và dependencies

```bash
# Python (thường đã có)
sudo pacman -S python python-pip

# Tkinter
sudo pacman -S tk

# Dependencies
sudo pacman -S python-pillow
```

### Bước 3: Cài Git

```bash
sudo pacman -S git
```

### Bước 4-7: Giống Ubuntu

```bash
git clone https://github.com/Thanhho1909/screenyy.git
cd screenyy
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python screen_translator.py
```

---

## Xử lý lỗi cài đặt

### ❌ "Failed building wheel for ..."

**Nguyên nhân:** Thiếu compiler hoặc development tools

**Giải pháp:**

**Ubuntu/Debian:**
```bash
sudo apt-get install build-essential python3-dev
```

**Fedora:**
```bash
sudo dnf groupinstall "Development Tools"
sudo dnf install python3-devel
```

**macOS:**
```bash
xcode-select --install
```

### ❌ "Could not find a version that satisfies the requirement"

**Nguyên nhân:** Sai version Python hoặc package không tương thích

**Giải pháp:**

1. Kiểm tra Python version: `python --version` (cần 3.8+)

2. Upgrade pip: `pip install --upgrade pip`

3. Install từng package:
   ```bash
   pip install mss
   pip install pillow
   pip install easyocr
   pip install opencv-python
   pip install googletrans==4.0.0rc1
   pip install numpy
   ```

### ❌ "Timeout error" khi download packages

**Nguyên nhân:** Mạng chậm hoặc PyPI server issue

**Giải pháp:**

```bash
# Tăng timeout
pip install -r requirements.txt --timeout 100

# Hoặc dùng mirror (VN)
pip install -r requirements.txt -i https://pypi.org/simple --trusted-host pypi.org
```

### ❌ Không đủ dung lượng đĩa

**Nguyên nhân:** OCR models (~1GB) + dependencies (~500MB)

**Giải pháp:**

1. Kiểm tra dung lượng:
   ```bash
   df -h  # Linux/macOS
   ```

2. Xóa cache pip:
   ```bash
   pip cache purge
   ```

3. Giải phóng dung lượng đĩa

---

## Kiểm tra cài đặt hoàn tất

Chạy script kiểm tra:

```bash
python -c "
import sys
print(f'Python version: {sys.version}')

import mss
print('✓ mss')

import PIL
print('✓ Pillow')

import cv2
print('✓ OpenCV')

import easyocr
print('✓ EasyOCR')

import googletrans
print('✓ googletrans')

import numpy
print('✓ NumPy')

try:
    import tkinter
    print('✓ Tkinter')
except:
    print('✗ Tkinter (required for GUI)')

print('\n✅ All dependencies installed successfully!')
"
```

Nếu tất cả đều ✓, bạn đã sẵn sàng sử dụng Screen Translator!

---

## Gỡ cài đặt

Nếu muốn gỡ bỏ:

```bash
# Deactivate venv (nếu đang active)
deactivate

# Xóa thư mục dự án
cd ..
rm -rf screenyy

# Xóa OCR models cache
rm -rf ~/.EasyOCR
```

---

## Cập nhật phiên bản mới

```bash
cd screenyy

# Pull latest code
git pull origin main

# Activate venv
source venv/bin/activate  # Linux/macOS
# hoặc
venv\Scripts\activate     # Windows

# Update dependencies
pip install -r requirements.txt --upgrade
```

---

**Nếu gặp vấn đề không có trong tài liệu, hãy mở issue trên GitHub!**
