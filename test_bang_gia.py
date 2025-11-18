# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd

# Đọc bảng giá giấy
file_path = 'Bang tinh gia.xlsx'

# Thử các cách đọc khác nhau
print("="*80)
print("CACH 1: Doc voi header=1")
print("="*80)
df1 = pd.read_excel(file_path, sheet_name='Bảng giá giấy', header=1)
print(df1.head(20))
print(f"\nColumns: {df1.columns.tolist()}")

print("\n" + "="*80)
print("CACH 2: Doc voi header=0")
print("="*80)
df2 = pd.read_excel(file_path, sheet_name='Bảng giá giấy', header=0)
print(df2.head(20))
print(f"\nColumns: {df2.columns.tolist()}")

print("\n" + "="*80)
print("CACH 3: Doc toan bo khong header")
print("="*80)
df3 = pd.read_excel(file_path, sheet_name='Bảng giá giấy', header=None)
print(df3.head(25))
print(f"\nColumns: {df3.columns.tolist()}")

# Lọc và làm sạch dữ liệu
print("\n" + "="*80)
print("LAM SACH DU LIEU")
print("="*80)

df = pd.read_excel(file_path, sheet_name='Bảng giá giấy', header=1)
df.columns = ['Ten_giay', 'Ma_giay', 'Dinh_luong', 'Gia']

# Xem trước khi lọc
print("\nTRUOC KHI LOC:")
print(df.head(30))

# Lọc bỏ dòng trống
df_clean = df.dropna(subset=['Ma_giay'])
print("\nSAU KHI LOC (dropna Ma_giay):")
print(df_clean.head(30))
print(f"\nTong so dong: {len(df_clean)}")

# Kiểm tra các mã giấy đặc biệt
print("\n" + "="*80)
print("KIEM TRA CAC MA GIAY DAC BIET")
print("="*80)

ma_giay_test = ['C80', 'C100', 'i210', 'i300', 'Op70', 'D250']
for ma in ma_giay_test:
    result = df_clean[df_clean['Ma_giay'] == ma]
    if len(result) > 0:
        print(f"{ma}: Dinh luong = {result['Dinh_luong'].values[0]}, Gia = {result['Gia'].values[0]}")
    else:
        print(f"{ma}: KHONG TIM THAY")
