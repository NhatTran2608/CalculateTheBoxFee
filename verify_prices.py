# -*- coding: utf-8 -*-
import pandas as pd
import sys
import io

# Set UTF-8 encoding cho output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Đọc bảng giá như trong app
df = pd.read_excel('Bang tinh gia.xlsx', sheet_name='Bảng giá giấy', header=1)
df.columns = ['Ten_giay', 'Ma_giay', 'Dinh_luong', 'Gia']
df = df.dropna(subset=['Ma_giay'])

# Chuẩn hóa mã giấy
df['Ma_giay'] = df['Ma_giay'].str.upper().str.strip()

print("\n" + "="*60)
print("KIỂM TRA GIÁ THEO HÌNH ẢNH BẠN CUNG CẤP")
print("="*60)

# Các mã giấy được highlight trong hình ảnh
test_codes = ['C80', 'C100', 'I210', 'I300', 'OP70']
expected_prices = {
    'C80': 23.6,
    'C100': 21.8,
    'I210': 18.2,  # Trong hình là i210 nhưng trong Excel là I210 (viết hoa)
    'I300': 17.4,
    'OP70': 22.0
}

print("\nKiểm tra các giá được highlight:")
for code in test_codes:
    result = df[df['Ma_giay'] == code]
    if not result.empty:
        row = result.iloc[0]
        expected = expected_prices.get(code, 'N/A')
        match = "✓ ĐÚNG" if row['Gia'] == expected else "✗ SAI"
        print(f"\n{code}:")
        print(f"  Tên: {row['Ten_giay']}")
        print(f"  Định lượng: {row['Dinh_luong']}g")
        print(f"  Giá Excel: {row['Gia']} VNĐ")
        print(f"  Giá mong đợi: {expected} VNĐ")
        print(f"  {match}")
    else:
        print(f"\n{code}: ✗ KHÔNG TÌM THẤY")

# Hiển thị toàn bộ bảng giá
print("\n" + "="*60)
print("TOÀN BỘ BẢNG GIÁ GIẤY (52 loại)")
print("="*60)
print(df.to_string(index=False))

print("\n" + "="*60)
print(f"Tổng số loại giấy: {len(df)}")
print("="*60)

# Test case-insensitive search
print("\n" + "="*60)
print("KIỂM TRA TÌM KIẾM KHÔNG PHÂN BIỆT HOA/THƯỜNG")
print("="*60)
test_searches = ['i300', 'I300', 'i210', 'I210', 'op70', 'OP70']
for search_code in test_searches:
    # Uppercase để tìm
    result = df[df['Ma_giay'] == search_code.upper()]
    status = "✓ TÌM THẤY" if not result.empty else "✗ KHÔNG TÌM THẤY"
    print(f"Tìm '{search_code}' → '{search_code.upper()}': {status}")
