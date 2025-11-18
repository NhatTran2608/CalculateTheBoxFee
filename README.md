# 📦 HỆ THỐNG TÍNH GIÁ BAO BÌ - HỘP SÓNG

Ứng dụng web tính giá thành cho Hộp Sóng - Nắp Cài Pizza được xây dựng bằng Streamlit.

## 🚀 Tính năng

### 1. Tính giá NẮP
- ✅ Nhập kích thước chi tiết (Dài, Rộng, Cao, Thành, Tai cài, Bù, Nới xén)
- ✅ Chọn chất liệu giấy từ bảng giá
- ✅ Cấu hình in ấn (Số màu, Máy in, Số bát/tờ)
- ✅ Chọn loại cán (Mờ, Bóng, Không)
- ✅ Chọn loại bồi (Sóng E Nâu, Sóng B Nâu, Sóng E Trắng)
- ✅ Các gia công đặc biệt:
  - In mặt trong
  - Cán mặt trong
  - Ép nhũ (3 loại)
  - Thúc nổi (3 loại)
  - In Offset UV
  - Lăn vân
  - Ghép màng Metalize

### 2. Tính giá KHAY ĐỊNH HÌNH
- ✅ Tính giá khay riêng biệt
- ✅ Cấu hình kích thước và chất liệu
- ✅ Thêm chi phí thùng cao su/foam
- ✅ Bù hao khay riêng

### 3. Bảng giá giấy
- ✅ Hiển thị toàn bộ bảng giá giấy
- ✅ Tra cứu nhanh theo mã giấy
- ✅ Hiển thị định lượng và giá

### 4. Tính toán tự động
- ✅ Tính diện tích xả lô
- ✅ Tính số tờ cần in
- ✅ Chi phí chi tiết từng hạng mục
- ✅ Đơn giá từng sản phẩm
- ✅ Tổng hợp giá thành

## 📋 Yêu cầu hệ thống

- Python 3.7+
- Streamlit
- Pandas
- OpenPyXL

## ⚙️ Cài đặt

```bash
# Cài đặt các thư viện cần thiết
pip install streamlit pandas openpyxl

# Hoặc
pip install -r requirements.txt
```

## 🎯 Chạy ứng dụng

```bash
streamlit run app.py
```

Ứng dụng sẽ tự động mở trong trình duyệt tại địa chỉ: `http://localhost:8501`

## 📖 Hướng dẫn sử dụng

### Bước 1: Nhập thông tin NẮP
1. Điền số lượng sản phẩm cần làm
2. Nhập kích thước: Dài, Rộng, Cao, Thành, Tai cài, Bù, Nới xén
3. Chọn chất liệu giấy
4. Chọn loại cán (Mờ/Bóng)
5. Nhập số bát/tờ in (ví dụ: 1x1, 1x2)
6. Chọn loại bồi
7. Điền thông số in: Máy in, Số màu, Nội dung
8. Điền các thông số gia công (nếu có)

### Bước 2: Nhập thông tin KHAY (tùy chọn)
1. Điền số lượng khay (bỏ trống = 0 nếu không cần)
2. Nhập kích thước khay
3. Chọn chất liệu và cấu hình tương tự như Nắp
4. Thêm các thông số đặc biệt cho khay

### Bước 3: Tính giá
1. Bấm nút **"TÍNH GIÁ"**
2. Xem kết quả chi tiết:
   - Chi phí từng hạng mục
   - Đơn giá NẮP
   - Đơn giá KHAY (nếu có)
   - Tổng chi phí
   - Giá BỘ (Nắp + Khay)

## 📐 Công thức tính toán

### Xả lô NẮP
```
Dài xả lô = Dài + Rộng + (Thành × 2) + Tai cài + Bù
Rộng xả lô = Rộng + Cao + (Thành × 2) + Nới xén
Diện tích = (Dài xả lô × Rộng xả lô) / 10000 (m²)
```

### Xả lô KHAY
```
Dài xả lô = Dài + Bù xén
Rộng xả lô = Rộng + Cao + Bù xén
Diện tích = (Dài xả lô × Rộng xả lô) / 10000 (m²)
```

### Chi phí
```
Chi phí giấy = Diện tích × Số tờ × (1 + Bù hao%) × Giá giấy
Chi phí in = Giá pha × (Số màu ÷ 2) + (Số tờ ÷ 1000) × Giá lượt
Chi phí cán = Diện tích × Giá cán × Máy in
Chi phí bồi = Diện tích × (Giá giấy bồi + Giá gia công bồi)
Chi phí gia công = (Số lượng ÷ 1000) × Đơn giá gia công
```

### Đơn giá
```
Đơn giá = Tổng chi phí ÷ Số lượng
```

## 📊 Cấu trúc file

```
Convert-excel/
│
├── Bang tinh gia.xlsx          # File Excel chứa bảng giá
├── app.py                       # Ứng dụng Streamlit chính
├── analyze_excel.py            # Script phân tích Excel
├── requirements.txt            # Danh sách thư viện
└── README.md                   # File này
```

## 💡 Lưu ý

- **Đơn vị:** 
  - Kích thước: cm
  - Giá: VNĐ
  - Bù hao: % (ví dụ: 400 = 400%)
  
- **Số màu in:** 2 màu = 1 pha

- **Số bát:** 
  - 1x1 = 1 bát/tờ
  - 1x2 = 2 bát/tờ
  - 2x2 = 4 bát/tờ
  - v.v.

- **Bù hao:**
  - Bù hao giấy: Thường 300-400%
  - Bù hao bồi: Thường 100-300%
  - Bù hao khay: Thêm 20-50%

## 🎨 Giao diện

Ứng dụng có 3 tab chính:
1. **🎯 NẮP CÀI PIZZA:** Form nhập liệu và tính giá
2. **📋 BẢNG GIÁ GIẤY:** Tra cứu giá vật liệu
3. **ℹ️ HƯỚNG DẪN:** Hướng dẫn sử dụng chi tiết

## 🔧 Tùy chỉnh

Để cập nhật bảng giá giấy:
1. Mở file `Bang tinh gia.xlsx`
2. Chỉnh sửa sheet "Bảng giá giấy"
3. Lưu file
4. Khởi động lại ứng dụng

## 🐛 Xử lý lỗi

Nếu gặp lỗi:
1. Kiểm tra file Excel có đúng tên và định dạng
2. Đảm bảo đã cài đặt đầy đủ thư viện
3. Kiểm tra các giá trị nhập vào có hợp lệ
4. Xem log trong terminal để biết chi tiết lỗi

## 📞 Hỗ trợ

Nếu cần hỗ trợ:
- Xem tab "Hướng dẫn" trong ứng dụng
- Kiểm tra file README này
- Liên hệ bộ phận kỹ thuật

## 📝 Changelog

### Version 1.0.0 (2024)
- ✅ Tính giá NẮP với đầy đủ tham số
- ✅ Tính giá KHAY định hình
- ✅ Tích hợp bảng giá giấy từ Excel
- ✅ Giao diện thân thiện với Streamlit
- ✅ Tính toán chi tiết từng hạng mục
- ✅ Hỗ trợ nhiều loại gia công đặc biệt
- ✅ Responsive layout

## 📄 License

Copyright © 2024. All rights reserved.

---

**Phát triển bởi:** Streamlit & Python  
**Ngày cập nhật:** November 2024
