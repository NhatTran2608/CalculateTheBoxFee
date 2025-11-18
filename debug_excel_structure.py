# -*- coding: utf-8 -*-
import pandas as pd
import sys
import io

# Set UTF-8 encoding cho output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("\n" + "="*60)
print("KIỂM TRA CẤU TRÚC SHEET 'Bảng giá giấy'")
print("="*60)

# Đọc với header=None để xem toàn bộ cấu trúc
df_raw = pd.read_excel('Bang tinh gia.xlsx', sheet_name='Bảng giá giấy', header=None)

print("\n1. 10 DÒNG ĐẦU TIÊN (RAW):")
print(df_raw.head(10))

print("\n2. KIỂM TRA DÒNG TIÊU ĐỀ:")
print("\nDòng 0:", df_raw.iloc[0].tolist())
print("Dòng 1:", df_raw.iloc[1].tolist())
print("Dòng 2:", df_raw.iloc[2].tolist())

print("\n3. ĐỌC VỚI HEADER=1:")
df_h1 = pd.read_excel('Bang tinh gia.xlsx', sheet_name='Bảng giá giấy', header=1)
print("\nColumns:", df_h1.columns.tolist())
print("\nDữ liệu đầu tiên:")
print(df_h1.head(10))

print("\n4. KIỂM TRA COLUMN INDEX:")
print("\nSố cột:", len(df_raw.columns))
for i, col in enumerate(df_raw.columns):
    print(f"Cột {i}: {df_raw.iloc[1, i]}")

print("\n5. TÌM COLUMN 'Mã giấy', 'Định lượng', 'Giá':")
header_row = df_raw.iloc[1]
for idx, val in enumerate(header_row):
    if pd.notna(val):
        print(f"Cột {idx}: '{val}'")
