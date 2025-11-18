# -*- coding: utf-8 -*-
import pandas as pd
import sys
import io

# Set UTF-8 encoding cho output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("\n" + "="*60)
print("TEST ĐỌC BẢNG GIÁ GIẤY - GIỐNG CODE STREAMLIT")
print("="*60)

# Đọc giống như trong app.py
df = pd.read_excel('Bang tinh gia.xlsx', sheet_name='Bảng giá giấy', header=1)
print("\n1. TÊN CỘT TỰ ĐỘNG TỪ EXCEL:")
print(df.columns.tolist())

# Giữ nguyên tên cột từ Excel
df = df.dropna(subset=['Mã giấy'])
df['Mã giấy'] = df['Mã giấy'].astype(str).str.upper().str.strip()

print(f"\n2. SỐ DÒNG SAU KHI DROPNA: {len(df)}")

print("\n3. 10 DÒNG ĐẦU TIÊN:")
print(df.head(10))

print("\n4. KIỂM TRA CÁC GIÁ TỪ HÌNH ẢNH:")
test_codes = ['C80', 'C100', 'I210', 'I300', 'OP70']
for code in test_codes:
    row = df[df['Mã giấy'] == code]
    if not row.empty:
        print(f"\n{code}:")
        print(f"  Mã giấy: {row['Mã giấy'].values[0]}")
        print(f"  Định lượng: {row['Định lượng'].values[0]} g/m²")
        print(f"  Giá: {row['Giá'].values[0]} VNĐ")
    else:
        print(f"\n{code}: ✗ KHÔNG TÌM THẤY")

print("\n5. DANH SÁCH TẤT CẢ MÃ GIẤY:")
print(df['Mã giấy'].tolist())

print("\n6. GIẢI THÍCH:")
print("✓ Tên cột GIỮ NGUYÊN từ Excel: 'Tên giấy', 'Mã giấy', 'Định lượng', 'Giá'")
print("✓ KHÔNG đổi tên thành Ma_giay, Dinh_luong, Gia")
print("✓ Uppercase mã giấy: i300 → I300")
print("✓ Khi upload file mới, chỉ cần có đúng tên cột này là được!")
