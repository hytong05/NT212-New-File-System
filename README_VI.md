# MyFS - Hệ Thống Tập Tin Bảo Mật

## Tổng Quan

MyFS (My File System) là một hệ thống quản lý tập tin bảo mật toàn diện được thiết kế để tạo, quản lý và bảo vệ tập tin trong các ổ đĩa ảo được mã hóa. Hệ thống cung cấp các tính năng bảo mật cấp doanh nghiệp bao gồm mã hóa tập tin, ủy quyền máy tính, xác minh tính toàn vẹn và khả năng khôi phục nâng cao.

## 🚀 Tính Năng Chính

### 🔐 **Tính Năng Bảo Mật**
- **Xác Thực Động**: Mật khẩu động theo thời gian thay đổi hàng ngày (định dạng: `myfs-YYYYMMDD`)
- **Ủy Quyền Máy Tính**: Đảm bảo MyFS chỉ chạy trên máy được ủy quyền thông qua dấu vân tay phần cứng
- **Mã Hóa AES-256**: Mã hóa cấp quân sự cho toàn bộ nội dung tập tin
- **Mật Khẩu Tập Tin Riêng**: Bảo vệ mật khẩu tùy chọn cho từng tập tin
- **Kiểm Tra Tính Toàn Vẹn**: Giám sát liên tục để phát hiện can thiệp và hỏng hóc

### 📁 **Quản Lý Tập Tin**
- **Tạo Ổ Đĩa Bảo Mật**: Tạo ổ đĩa `.DRI` được mã hóa với lưu trữ metadata riêng biệt
- **Import/Export Tập Tin**: Nhập tập tin vào MyFS và xuất ra một cách bảo mật với xác minh tính toàn vẹn
- **Xóa Mềm/Cứng**: Khả năng xóa có thể khôi phục và xóa vĩnh viễn
- **Khôi Phục Tập Tin**: Khôi phục tập tin đã xóa nhầm từ hệ thống thùng rác
- **Sao Lưu Metadata**: Tự động sao lưu metadata ổ đĩa để khôi phục thảm họa

### 🛡️ **Bảo Mật Nâng Cao**
- **Phát Hiện Can Thiệp**: Phát hiện thời gian thực các sửa đổi trái phép
- **Tự Động Khôi Phục**: Tự động khôi phục từ bản sao lưu khi phát hiện hỏng hóc
- **Ghi Log Toàn Diện**: Dấu vết kiểm toán chi tiết với ghi log vào tập tin có timestamp
- **Sửa Chữa Khẩn Cấp**: Chức năng sửa chữa ổ đĩa cho MyFS bị hỏng

## 📋 Yêu Cầu Hệ Thống

- Python 3.7 trở lên
- Hệ điều hành Windows, macOS hoặc Linux
- Các gói Python cần thiết (xem requirements.txt)

## 🔧 Cài Đặt

1. **Clone repository:**
   ```bash
   git clone <repository-url>
   cd myfs-project
   ```

2. **Cài đặt dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Kiểm tra cài đặt:**
   ```bash
   python src/main.py
   ```

## 📦 Thư Viện Phụ Thuộc

```
cryptography==3.4.7    # Các thao tác mã hóa nâng cao
psutil==5.9.5          # Thu thập thông tin hệ thống
pycryptodome==3.10.1   # Các chức năng mã hóa bổ sung
pytest==6.2.4         # Framework testing
Flask==2.0.1           # Web framework (giao diện web tương lai)
click==8.0.1           # Tiện ích giao diện dòng lệnh
```

## 🚀 Bắt Đầu Nhanh

1. **Khởi chạy MyFS:**
   ```bash
   python src/main.py
   ```

2. **Nhập xác thực động:**
   - Định dạng: `myfs-YYYYMMDD`
   - Ví dụ cho ngày 25/12/2024: `myfs-20241225`

3. **Tạo ổ đĩa đầu tiên:**
   - Chọn tùy chọn 1 từ menu chính
   - Chỉ định vị trí ổ đĩa và đường dẫn lưu trữ metadata
   - Đặt mật khẩu chính mạnh

4. **Bắt đầu quản lý tập tin:**
   - Nhập tập tin với tùy chọn 5
   - Liệt kê tập tin với tùy chọn 3
   - Xuất tập tin với tùy chọn 6

## 📖 Hướng Dẫn Sử Dụng Chi Tiết

### 🆕 Tạo Ổ Đĩa MyFS

1. Chọn **"Create/Format MyFS volume"** từ menu chính
2. **Chọn Thư Mục**: Chọn nơi lưu trữ tập tin `.DRI`
3. **Đặt Tên Ổ Đĩa**: Nhập tên cho ổ đĩa (phần mở rộng được thêm tự động)
4. **Vị Trí Metadata**: Chỉ định đường dẫn lưu trữ metadata (tốt nhất trên thiết bị di động)
5. **Mật Khẩu Chính**: Đặt mật khẩu mạnh để mã hóa ổ đĩa

**Ví dụ:**
```
Enter directory to store MyFS.DRI: C:\MySecureFiles
Enter name for MyFS volume (without extension): DuLieuCongTy
Enter path for metadata on removable disk: E:\Backup\DuLieuCongTy.IXF
Set master password: [Nhập mật khẩu mạnh]
```

### 🔑 Hệ Thống Xác Thực

**Định Dạng Mật Khẩu Động:** `myfs-YYYYMMDD`
- **Thay Đổi Hàng Ngày**: Mật khẩu tự động thay đổi mỗi ngày
- **Ví Dụ Mật Khẩu:**
  - 1 tháng 1, 2024: `myfs-20240101`
  - 31 tháng 12, 2024: `myfs-20241231`

**Ủy Quyền Máy Tính:**
- Lần truy cập đầu tạo dấu vân tay phần cứng
- Các lần truy cập sau yêu cầu cùng máy tính
- Ngăn chặn truy cập ổ đĩa trái phép từ máy tính khác

### 📂 Thao Tác Tập Tin

#### **Nhập Tập Tin**
1. Chọn tùy chọn 5: **"Import file to MyFS"**
2. Nhập đường dẫn đầy đủ đến tập tin muốn nhập
3. Chọn có thêm bảo vệ mật khẩu hay không
4. Nếu bảo vệ mật khẩu: nhập và xác nhận mật khẩu tập tin

**Tính Năng Hỗ Trợ:**
- Tập tin bất kỳ kích thước và loại nào
- Mã hóa tập tin riêng lẻ tùy chọn
- Tự động xác minh tính toàn vẹn
- Bảo tồn metadata (kích thước, timestamp)

#### **Xuất Tập Tin**
1. Chọn tùy chọn 6: **"Export file from MyFS"**
2. Chọn từ danh sách tập tin có sẵn
3. Chỉ định đường dẫn đích
4. Nhập mật khẩu tập tin nếu cần thiết
5. Chọn chế độ xuất:
   - **Thường**: Tập tin đã giải mã
   - **Raw**: Nội dung được mã hóa (để sao lưu)

#### **Liệt Kê Tập Tin**
- **Xem Tiêu Chuẩn**: Hiển thị tập tin hoạt động với metadata
- **Bao Gồm Đã Xóa**: Xem cả tập tin hoạt động và đã xóa mềm
- **Thông Tin Hiển Thị**:
  - Tên và kích thước tập tin
  - Timestamp nhập
  - Trạng thái bảo vệ
  - Trạng thái xóa

### 🗑️ Xóa và Khôi Phục

#### **Xóa Mềm (Có Thể Khôi Phục)**
1. Chọn tùy chọn 7: **"Delete file from MyFS"**
2. Chọn tùy chọn 1: **"Mark as deleted (recoverable)"**
3. Tập tin bị ẩn nhưng có thể khôi phục

#### **Xóa Cứng (Vĩnh Viễn)**
1. Chọn tùy chọn 7: **"Delete file from MyFS"**
2. Chọn tùy chọn 2: **"Permanently delete"**
3. Xác nhận xóa - **không thể hoàn tác**

#### **Khôi Phục Tập Tin**
1. Chọn tùy chọn 8: **"Recover deleted file"**
2. Xem danh sách tập tin có thể khôi phục
3. Nhập tên tập tin cần khôi phục
4. Tập tin được khôi phục về trạng thái hoạt động

#### **Xóa Vĩnh Viễn Tất Cả Tập Tin Đã Xóa**
1. Chọn tùy chọn 10: **"Purge deleted files"**
2. Xem danh sách tập tin sẽ bị xóa vĩnh viễn
3. Xác nhận với 'y' - **không thể hoàn tác**

### 🔒 Thao Tác Bảo Mật

#### **Thay Đổi Mật Khẩu Chính**
1. Chọn tùy chọn 2: **"Change MyFS password"**
2. Nhập mật khẩu chính hiện tại để xác minh
3. Nhập mật khẩu mới hai lần để xác nhận
4. Tất cả dữ liệu được mã hóa lại với mật khẩu mới

#### **Đặt/Thay Đổi Mật Khẩu Tập Tin**
1. Chọn tùy chọn 4: **"Set/Change file password"**
2. Chọn tập tin từ danh sách
3. Đối với mật khẩu hiện có: nhập mật khẩu hiện tại
4. Nhập mật khẩu mới hai lần để xác nhận
5. Tùy chọn buộc thay đổi không cần mật khẩu hiện tại

### 🛠️ Bảo Trì và Sửa Chữa

#### **Sửa Chữa Ổ Đĩa**
1. Chọn tùy chọn 11: **"Repair MyFS volume"**
2. Nhập đường dẫn đến tập tin `.DRI` bị hỏng
3. Hệ thống kiểm tra metadata sao lưu
4. Nhập mật khẩu chính để sửa chữa
5. Tự động khôi phục nếu có thể

**Khả Năng Sửa Chữa:**
- Khôi phục hỏng hóc metadata
- Tái tạo bảng tập tin
- Xác minh tính toàn vẹn
- Khôi phục từ sao lưu

#### **Xác Minh Tính Toàn Vẹn Hệ Thống**
- **Tự Động**: Chạy mỗi khi khởi động
- **Liên Tục**: Giám sát thay đổi trong quá trình hoạt động
- **Khôi Phục**: Tự động khôi phục từ sao lưu khi phát hiện hỏng hóc

## 🏗️ Tổng Quan Kiến Trúc

### **Thành Phần Lõi**

```
src/
├── filesystem/          # Thao tác hệ thống tập tin lõi
│   ├── myfs.py         # Class MyFS chính
│   ├── core/           # Chức năng lõi
│   │   ├── volume_operations.py
│   │   ├── file_table.py
│   │   └── myfs.py
│   ├── operations/     # Thao tác tập tin và bảo mật
│   └── utils/          # Hàm tiện ích
├── security/           # Hệ thống con bảo mật
│   ├── encryption.py   # Mã hóa AES-256
│   ├── authentication.py  # Xác thực động
│   └── integrity.py    # Kiểm tra tính toàn vẹn hệ thống
├── ui/                 # Giao diện người dùng
│   └── cli.py         # Giao diện dòng lệnh
└── utils/              # Tiện ích chung
    ├── logger.py       # Ghi log toàn diện
    ├── file_operations.py
    └── system_info.py
```

### **Kiến Trúc Bảo Mật**

1. **Mã Hóa Đa Lớp**:
   - Mã hóa cấp ổ đĩa với mật khẩu chính
   - Mã hóa tập tin riêng lẻ với mật khẩu tùy chọn
   - Mã hóa metadata cho cấu trúc ổ đĩa

2. **Chuỗi Xác Thực**:
   - Mật khẩu động hàng ngày để truy cập hệ thống
   - Mật khẩu chính để truy cập ổ đĩa
   - Mật khẩu tập tin riêng lẻ cho tập tin nhạy cảm
   - Ủy quyền máy tính để ràng buộc ổ đĩa

3. **Bảo Vệ Tính Toàn Vẹn**:
   - Xác minh tập tin dựa trên hash
   - Dấu vân tay hệ thống
   - Sao lưu và khôi phục tự động
   - Phát hiện và cảnh báo can thiệp

## 📊 Ví Dụ Cấu Trúc Tập Tin

```
Cấu Trúc Ổ Đĩa MyFS:
DuLieuCongTy.DRI         # Ổ đĩa mã hóa chính
DuLieuCongTy.IXF         # Tập tin metadata
DuLieuCongTy.DRI.machine # Tập tin ủy quyền máy tính

Nội Dung Ổ Đĩa:
├── tailieu.pdf          (Có bảo vệ mật khẩu)
├── bangtinh.xlsx        (Không có mật khẩu)
├── thuyettrình.pptx     (Đã xóa - có thể khôi phục)
└── [tập tin đã xóa]     (Các mục đã xóa mềm)
```

## 🔍 Tham Khảo Menu

| Tùy Chọn | Chức Năng | Mô Tả |
|----------|-----------|-------|
| 1 | Create/Format MyFS volume | Tạo ổ đĩa mã hóa mới |
| 2 | Change MyFS password | Cập nhật mật khẩu chính |
| 3 | List files in MyFS | Xem tất cả tập tin trong ổ đĩa |
| 4 | Set/Change file password | Quản lý mật khẩu tập tin riêng lẻ |
| 5 | Import file to MyFS | Thêm tập tin vào ổ đĩa |
| 6 | Export file from MyFS | Trích xuất tập tin từ ổ đĩa |
| 7 | Delete file from MyFS | Xóa tập tin (mềm/cứng) |
| 8 | Recover deleted file | Khôi phục tập tin đã xóa mềm |
| 9 | View deleted files | Liệt kê tập tin có thể khôi phục |
| 10 | Purge deleted files | Xóa vĩnh viễn tất cả tập tin đã xóa |
| 11 | Repair MyFS volume | Sửa ổ đĩa bị hỏng |
| 12 | Exit | Đóng ứng dụng |

## 🧪 Kiểm Thử

Chạy bộ test để xác minh chức năng hệ thống:

```bash
# Chạy tất cả test
pytest tests/

# Chạy module test cụ thể
pytest tests/test_filesystem.py
pytest tests/test_security.py

# Chạy với output chi tiết
pytest -v tests/
```

## 📝 Ghi Log và Giám Sát

**Vị Trí Log**: `logs/myfs_YYYYMMDD_HHMMSS.log`

**Cấp Độ Log**:
- **DEBUG**: Thông tin phát triển chi tiết
- **INFO**: Thông điệp hoạt động chung
- **WARNING**: Vấn đề tiềm ẩn
- **ERROR**: Điều kiện lỗi
- **CRITICAL**: Lỗi hệ thống

**Nội Dung Log**:
- Cố gắng xác thực người dùng
- Thao tác tập tin (import/export/delete)
- Sự kiện và vi phạm bảo mật
- Kiểm tra tính toàn vẹn hệ thống
- Điều kiện lỗi và khôi phục

## 🔧 Khắc Phục Sự Cố

### **Vấn Đề Thường Gặp**

#### **Xác Thực Thất Bại**
- Xác minh định dạng ngày: `myfs-YYYYMMDD`
- Kiểm tra cài đặt ngày/giờ hệ thống
- Đảm bảo múi giờ nhất quán

#### **Ủy Quyền Máy Tính Thất Bại**
- Ổ đĩa được tạo trên máy tính khác
- Cấu hình phần cứng thay đổi đáng kể
- Chuyển ổ đĩa về máy gốc hoặc tạo lại

#### **Ổ Đĩa Bị Hỏng**
- Sử dụng chức năng sửa chữa (tùy chọn 11)
- Đảm bảo metadata sao lưu tồn tại
- Kiểm tra tính toàn vẹn đĩa

#### **Không Tìm Thấy Tập Tin**
- Xác minh đường dẫn tập tin đúng
- Kiểm tra tập tin chưa bị xóa mềm
- Đảm bảo quyền thích hợp

### **Khôi Phục Khẩn Cấp**

Nếu ổ đĩa MyFS bị hỏng:

1. **Đừng hoảng sợ** - có sao lưu
2. Sử dụng **Repair MyFS volume** (tùy chọn 11)
3. Đảm bảo tập tin metadata sao lưu tồn tại
4. Chuẩn bị mật khẩu chính
5. Để quá trình sửa chữa hoàn thành

## 🤝 Đóng Góp

Chúng tôi hoan nghênh đóng góp! Vui lòng:

1. Fork repository
2. Tạo branch tính năng
3. Thực hiện thay đổi
4. Thêm test cho chức năng mới
5. Gửi pull request

## 📄 Giấy Phép

Dự án này được cấp phép theo Giấy phép MIT. Xem tập tin LICENSE để biết chi tiết.

## ⚠️ Thông Báo Bảo Mật

- Giữ mật khẩu chính của bạn an toàn
- Thường xuyên sao lưu tập tin metadata
- Giám sát log cho các sự kiện bảo mật
- Cập nhật hệ thống thường xuyên
- Báo cáo vấn đề bảo mật một cách có trách nhiệm

## 📞 Hỗ Trợ

Để được hỗ trợ, vấn đề hoặc yêu cầu tính năng:
- Mở issue trên GitHub
- Kiểm tra phần khắc phục sự cố
- Xem lại tập tin log để biết chi tiết lỗi

---

**MyFS** - Bảo Mật, Đáng Tin Cậy, Quản Lý Tập Tin Chuyên Nghiệp
