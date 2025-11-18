import streamlit as st
import pandas as pd
import math

# Cấu hình trang
st.set_page_config(page_title="Hệ thống Tính Giá Bao Bì", layout="wide", page_icon="📦")

# Load bảng giá giấy
@st.cache_data
def load_bang_gia_giay():
    df = pd.read_excel('Bang tinh gia.xlsx', sheet_name='Bảng giá giấy', header=1)
    df.columns = ['Ten_giay', 'Ma_giay', 'Dinh_luong', 'Gia']
    df = df.dropna(subset=['Ma_giay'])
    return df

bang_gia_giay = load_bang_gia_giay()

# CSS tùy chỉnh
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .price-display {
        font-size: 2rem;
        color: #d62728;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        background-color: #fff3cd;
        border-radius: 10px;
        margin: 20px 0;
    }
    .detail-table {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📦 HỆ THỐNG TÍNH GIÁ BAO BÌ - HỘP SÓNG</div>', unsafe_allow_html=True)

# Tabs chính
tab1, tab2, tab3 = st.tabs(["🎯 TÍNH GIÁ", "📋 BẢNG GIÁ GIẤY", "ℹ️ HƯỚNG DẪN"])

with tab1:
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown('<div class="section-header">📊 THÔNG TIN CHUNG - NẮP</div>', unsafe_allow_html=True)
        
        so_luong = st.number_input("Số lượng (cái)", min_value=1, value=10000, step=1000)
        
        # Kích thước Nắp
        st.markdown('<div class="section-header">📐 KÍCH THƯỚC NẮP</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            nap_dai = st.number_input("Dài (cm)", min_value=0.0, value=32.0, step=0.1, key="nap_dai")
        with col2:
            nap_rong = st.number_input("Rộng (cm)", min_value=0.0, value=22.0, step=0.1, key="nap_rong")
        with col3:
            nap_cao = st.number_input("Cao (cm)", min_value=0.0, value=8.0, step=0.1, key="nap_cao")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            nap_thanh = st.number_input("Thành", min_value=0.0, value=0.5, step=0.1, key="nap_thanh")
        with col2:
            nap_tai_cai = st.number_input("Tai cài", min_value=0.0, value=0.0, step=0.1, key="nap_tai_cai")
        with col3:
            nap_bu = st.number_input("Bù", min_value=0.0, value=0.1, step=0.1, key="nap_bu")
        with col4:
            nap_noi_xen = st.number_input("Nới xén", min_value=0.0, value=0.4, step=0.1, key="nap_noi_xen")
        
        # Chất liệu Nắp
        st.markdown('<div class="section-header">🎨 CHẤT LIỆU & IN ẤN</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            chat_lieu_options = bang_gia_giay['Ma_giay'].unique().tolist()
            nap_chat_lieu = st.selectbox("Chất liệu giấy", options=chat_lieu_options, 
                                        index=chat_lieu_options.index('i300') if 'i300' in chat_lieu_options else 0, 
                                        key="nap_chat_lieu")
            # Lấy định lượng giấy từ bảng giá
            dinh_luong_giay = bang_gia_giay[bang_gia_giay['Ma_giay'] == nap_chat_lieu]['Dinh_luong'].values[0]
            gia_giay = bang_gia_giay[bang_gia_giay['Ma_giay'] == nap_chat_lieu]['Gia'].values[0]
            st.info(f"Định lượng: {dinh_luong_giay} g/m² | Giá: {gia_giay} VNĐ/kg")
        
        with col2:
            nap_can = st.selectbox("Loại cán", options=['Không', 'Mờ', 'Bóng'], index=1, key="nap_can")
        
        col1, col2 = st.columns(2)
        with col1:
            nap_so_bat = st.selectbox("Số bát/tờ", options=['1x1', '1x2', '2x2', '2x3', '3x3'], index=0, key="nap_so_bat")
            so_bat_value = int(nap_so_bat.split('x')[0]) * int(nap_so_bat.split('x')[1])
        with col2:
            nap_boi = st.selectbox("Loại bồi", options=['Không', 'Sóng E Nâu', 'Sóng B Nâu'], index=1, key="nap_boi")
        
        # Thông số in
        st.markdown('<div class="section-header">🖨️ THÔNG SỐ IN ẤN</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            nap_may_in = st.selectbox("Máy in", options=[8, 10, 12, 16, "UV"], index=3, key="nap_may_in")
        with col2:
            nap_so_mau = st.number_input("Số màu", min_value=0, value=4, key="nap_so_mau")
        with col3:
            nap_noi_dung = st.number_input("Nội dung", min_value=1, value=1, key="nap_noi_dung")
        
        nap_cai_thung = st.number_input("Cái/Thùng", min_value=1, value=200, key="nap_cai_thung")
        
        # Gia công đặc biệt
        st.markdown('<div class="section-header">✨ GIA CÔNG ĐẶC BIỆT</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            nap_in_mat_trong = st.checkbox("In Mặt trong", value=False, key="nap_in_mat_trong")
            nap_so_mau_mt = 0
            if nap_in_mat_trong:
                nap_so_mau_mt = st.number_input("Số màu mặt trong", min_value=1, value=1, key="nap_so_mau_mt")
        
        with col2:
            nap_can_mat_trong = st.checkbox("Cán Mặt trong", value=False, key="nap_can_mat_trong")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            nap_lan_van = st.checkbox("Lăn Vân", value=False, key="nap_lan_van")
        with col2:
            nap_in_offset_uv = st.checkbox("In Offset UV", value=False, key="nap_in_offset_uv")
        with col3:
            nap_ghep_metalize = st.checkbox("Ghép Màng Metalize", value=False, key="nap_ghep_metalize")
        
        # Ép nhũ và thúc nổi
        nap_ep_nhu_1 = st.checkbox("Ép nhũ 1", value=False, key="nap_ep_nhu_1")
        nap_ep_nhu_2 = st.checkbox("Ép nhũ 2", value=False, key="nap_ep_nhu_2")
        nap_ep_nhu_3 = st.checkbox("Ép nhũ 3", value=False, key="nap_ep_nhu_3")
        
        nap_thuc_noi_1 = st.checkbox("Thúc nổi 1", value=False, key="nap_thuc_noi_1")
        nap_thuc_noi_2 = st.checkbox("Thúc nổi 2", value=False, key="nap_thuc_noi_2")
        nap_thuc_noi_3 = st.checkbox("Thúc nổi 3", value=False, key="nap_thuc_noi_3")
        
        # Chi phí khác
        st.markdown('<div class="section-header">💰 CHI PHÍ KHÁC</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            nap_day_xach = st.number_input("Dây xách", min_value=0, value=0, key="nap_day_xach")
        with col2:
            nap_van_chuyen = st.number_input("Vận chuyển", min_value=0, value=0, key="nap_van_chuyen")

    with col_right:
        st.markdown('<div class="section-header">📊 KHAY ĐỊNH HÌNH</div>', unsafe_allow_html=True)
        
        khay_co_khay = st.checkbox("Có Khay định hình", value=False, key="khay_co_khay")
        
        if khay_co_khay:
            khay_so_luong = st.number_input("Số lượng khay", min_value=1, value=100, step=10, key="khay_so_luong")
            
            # Kích thước Khay
            st.markdown('<div class="section-header">📐 KÍCH THƯỚC KHAY</div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                khay_dai = st.number_input("Dài (cm)", min_value=0.0, value=31.0, step=0.1, key="khay_dai")
            with col2:
                khay_rong = st.number_input("Rộng (cm)", min_value=0.0, value=21.6, step=0.1, key="khay_rong")
            with col3:
                khay_cao = st.number_input("Cao (cm)", min_value=0.0, value=4.0, step=0.1, key="khay_cao")
            
            khay_bu_xen = st.number_input("Bù xén", min_value=0.0, value=0.4, step=0.1, key="khay_bu_xen")
            
            # Chất liệu khay
            st.markdown('<div class="section-header">🎨 CHẤT LIỆU KHAY</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                khay_chat_lieu = st.selectbox("Chất liệu giấy", options=chat_lieu_options, 
                                             index=chat_lieu_options.index('i300') if 'i300' in chat_lieu_options else 0, 
                                             key="khay_chat_lieu")
            with col2:
                khay_can = st.selectbox("Loại cán", options=['Không', 'Mờ', 'Bóng'], index=1, key="khay_can")
            
            col1, col2 = st.columns(2)
            with col1:
                khay_so_bat = st.selectbox("Số bát/tờ", options=['1x1', '1x2', '2x2', '2x3'], index=1, key="khay_so_bat")
            with col2:
                khay_boi = st.selectbox("Loại bồi", options=['Không', 'Sóng E Nâu'], index=1, key="khay_boi")
            
            # Thông số in khay
            st.markdown('<div class="section-header">🖨️ THÔNG SỐ IN KHAY</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                khay_may_in = st.selectbox("Máy in", options=[8, 10, 12, 16], index=0, key="khay_may_in")
            with col2:
                khay_so_mau = st.number_input("Số màu", min_value=0, value=1, key="khay_so_mau")
            
            khay_thung_cao_su = st.checkbox("Thùng Cao Su", value=False, key="khay_thung_cao_su")
        else:
            khay_so_luong = 0

    # TÍNH TOÁN
    st.markdown("---")
    st.markdown('<div class="section-header">💰 TÍNH TOÁN GIÁ THÀNH</div>', unsafe_allow_html=True)
    
    if st.button("🧮 TÍNH GIÁ", type="primary", use_container_width=True):
        
        # ===================== TÍNH GIÁ NẮP =====================
        
        # 1. TÍNH XẢ LÔ NẮP
        xa_lo_dai_nap = nap_dai + nap_rong + (nap_thanh * 2) + nap_tai_cai + nap_bu
        xa_lo_rong_nap = nap_rong + nap_cao + (nap_thanh * 2) + nap_noi_xen
        
        # 2. TÍNH SỐ TỜ VÀ BÙ HAO
        # Số tờ in = Số lượng / Số bát
        so_to_in = math.ceil(so_luong / so_bat_value)
        
        # Bù hao tính theo công thức Excel (dựa vào loại giấy và gia công)
        # Bù hao = IF(các điều kiện đặc biệt, 5%, 4%), tối thiểu 100 hoặc 150
        if nap_boi != 'Không' or nap_ghep_metalize or nap_in_offset_uv:
            bu_hao_pct = 0.05  # 5%
            bu_hao_min = 150
        else:
            bu_hao_pct = 0.04  # 4%
            bu_hao_min = 100
        
        bu_hao_to = max(bu_hao_min, so_to_in / so_bat_value * bu_hao_pct)
        so_to_co_bu_hao = so_to_in + bu_hao_to
        
        # 3. CHI PHÍ GIẤY IN
        # Công thức: (Dài/100) * (Rộng/100) * Số tờ * Định lượng * Giá giấy
        chi_phi_giay_in = (xa_lo_dai_nap / 100) * (xa_lo_rong_nap / 100) * so_to_co_bu_hao * dinh_luong_giay * gia_giay
        
        # 4. CHI PHÍ KẼM (In offset)
        # Kích thước kẽm phụ thuộc máy in
        kem_size = {8: (56, 67), 10: (60, 73), 12: (64.5, 83), 16: (83, 103), "UV": (60, 73)}
        kem_dai, kem_rong = kem_size.get(nap_may_in, (83, 103))
        so_to_kem = nap_so_mau * nap_noi_dung
        
        # Giá kẽm: 13,150 VNĐ/tờ (theo Excel row 90, col I)
        gia_kem = 13150
        chi_phi_kem = kem_dai * kem_rong * so_to_kem * gia_kem
        
        # 5. CHI PHÍ IN OFFSET
        # Giá in phụ thuộc máy in
        gia_in_map = {8: 90000, 10: 100000, 12: 170000, 16: 230000, "UV": 580000}
        gia_in = gia_in_map.get(nap_may_in, 230000)
        chi_phi_in_offset = so_to_kem * gia_in
        
        # 6. CHI PHÍ CÁN
        # Công thức: IF(chi phí < 100,000, 100,000, chi phí thực tế)
        # Bù hao cán = Số tờ - Bù hao/2
        so_to_can = so_to_co_bu_hao - bu_hao_to / 2
        gia_can_m2 = 0.22 if nap_can == "Mờ" else (0.2 if nap_can == "Bóng" else 0)
        
        if nap_can != 'Không':
            chi_phi_can_temp = (xa_lo_dai_nap / 100) * (xa_lo_rong_nap / 100) * so_to_can * gia_can_m2 * nap_may_in
            chi_phi_can = max(100000, chi_phi_can_temp)
        else:
            chi_phi_can = 0
        
        # 7. CHI PHÍ GIẤY BỒI
        chi_phi_giay_boi = 0
        chi_phi_cong_boi = 0
        if nap_boi != 'Không':
            # Bù hao bồi: 3% tối thiểu 100
            bu_hao_boi = max(100, so_to_in / so_bat_value * 0.03)
            so_to_boi = so_to_in + bu_hao_boi
            
            # Lấy định lượng bồi từ bảng giá
            dinh_luong_boi = bang_gia_giay[bang_gia_giay['Ma_giay'] == nap_boi.replace(' ', '')]['Dinh_luong'].values
            if len(dinh_luong_boi) == 0:
                dinh_luong_boi = 1  # Mặc định
            else:
                dinh_luong_boi = dinh_luong_boi[0]
            
            # Giá giấy bồi: 3,800 VNĐ/m2
            gia_giay_boi = 3800
            chi_phi_giay_boi = (math.ceil(xa_lo_dai_nap) / 100) * (math.ceil(xa_lo_rong_nap) / 100) * so_to_boi * dinh_luong_boi * gia_giay_boi
            
            # Công bồi: 1,300 VNĐ/m2, tối thiểu 150,000
            gia_cong_boi = 1300
            chi_phi_cong_boi_temp = (xa_lo_dai_nap / 100) * (xa_lo_rong_nap / 100) * so_to_boi * gia_cong_boi
            chi_phi_cong_boi = max(150000, chi_phi_cong_boi_temp) if chi_phi_cong_boi_temp > 0 else 0
        
        # 8. CHI PHÍ GIA CÔNG
        # Phụ thuộc có bồi hay không và số lượng
        if nap_boi == 'Không':
            chi_phi_gia_cong_base = 250 if so_luong < 5000 else 200
        else:
            chi_phi_gia_cong_base = 500 if so_luong < 5000 else 350
        
        chi_phi_gia_cong = max(300000 if nap_boi == 'Không' else 500000, 
                               chi_phi_gia_cong_base * (so_luong / 1000))
        
        # 9. CHI PHÍ IN MẶT TRONG
        chi_phi_in_mt = 0
        chi_phi_kem_mt = 0
        if nap_in_mat_trong:
            so_to_kem_mt = nap_so_mau_mt
            chi_phi_kem_mt = kem_dai * kem_rong * so_to_kem_mt * gia_kem
            
            gia_in_mt_map = {8: 120000, 10: 150000, 12: 200000, 16: 250000, "UV": 250000}
            gia_in_mt = gia_in_mt_map.get(nap_may_in, 250000)
            chi_phi_in_mt = so_to_kem_mt * gia_in_mt
        
        # 10. CHI PHÍ CÁN MẶT TRONG
        chi_phi_can_mt = 0
        if nap_can_mat_trong:
            chi_phi_can_mt_temp = (xa_lo_dai_nap / 100) * (xa_lo_rong_nap / 100) * so_to_co_bu_hao * gia_can_m2 * nap_may_in
            chi_phi_can_mt = max(100000, chi_phi_can_mt_temp)
        
        # 11. CHI PHÍ METALIZE
        chi_phi_metalize = 0
        if nap_ghep_metalize:
            gia_metalize = 15000  # VNĐ/m2
            chi_phi_metalize_temp = (xa_lo_dai_nap / 100) * (xa_lo_rong_nap / 100) * so_to_co_bu_hao * gia_metalize
            chi_phi_metalize = max(100000, chi_phi_metalize_temp) if chi_phi_metalize_temp > 0 else 0
        
        # 12. CHI PHÍ DÂY XÁCH
        chi_phi_day_xach = 0
        if nap_day_xach > 0:
            chi_phi_day_xach = max(100000, nap_day_xach * 50)  # 50 VNĐ/dây
        
        # 13. CHI PHÍ KHUÔN BẠC
        chi_phi_khuon_bac = 500000  # Cố định
        
        # 14. CHI PHÍ ÉP NHŨ
        chi_phi_ep_nhu = 0
        for ep_nhu in [nap_ep_nhu_1, nap_ep_nhu_2, nap_ep_nhu_3]:
            if ep_nhu:
                # Khuôn ép: 120,000
                # Ép: 250,000 + 100 VNĐ/1000 cái
                chi_phi_khuon_ep = 120000
                chi_phi_ep = max(250000, 250000 + (so_luong / 1000) * 100)
                chi_phi_ep_nhu += chi_phi_khuon_ep + chi_phi_ep
        
        # 15. CHI PHÍ THÚC NỔI
        chi_phi_thuc_noi = 0
        for thuc_noi in [nap_thuc_noi_1, nap_thuc_noi_2, nap_thuc_noi_3]:
            if thuc_noi:
                # Khuôn thúc: 120,000 * 2 (2 cái khuôn)
                # Thúc: 150,000 tối thiểu
                chi_phi_khuon_thuc = 120000 * 2 * so_bat_value
                chi_phi_thuc = max(150000, 100 * (so_luong / 1000))
                chi_phi_thuc_noi += chi_phi_khuon_thuc + chi_phi_thuc
        
        # 16. CHI PHÍ LĂN VÂN
        chi_phi_lan_van = 0
        if nap_lan_van:
            chi_phi_lan_van = max(300000, (xa_lo_dai_nap / 100) * (xa_lo_rong_nap / 100) * so_to_co_bu_hao * 50 + 100000)
        
        # 17. CHI PHÍ IN OFFSET UV
        chi_phi_offset_uv = 0
        if nap_in_offset_uv:
            chi_phi_offset_uv = max(700000, so_to_kem * 100000)
        
        # 18. CHI PHÍ THÙNG
        chi_phi_thung = max(15000, math.ceil(so_luong / nap_cai_thung) * 15000)
        
        # 19. CHI PHÍ VẬN CHUYỂN
        chi_phi_van_chuyen = nap_van_chuyen
        
        # TỔNG CHI PHÍ SẢN XUẤT NẮP
        tong_san_xuat_nap = (chi_phi_giay_in + chi_phi_kem + chi_phi_in_offset + 
                             chi_phi_can + chi_phi_giay_boi + chi_phi_cong_boi +
                             chi_phi_gia_cong + chi_phi_in_mt + chi_phi_kem_mt + 
                             chi_phi_can_mt + chi_phi_metalize + chi_phi_day_xach +
                             chi_phi_khuon_bac + chi_phi_ep_nhu + chi_phi_thuc_noi +
                             chi_phi_lan_van + chi_phi_offset_uv + chi_phi_thung +
                             chi_phi_van_chuyen)
        
        # LÃI SUẤT 25%
        lai_suat_nap = tong_san_xuat_nap * 0.25
        tong_sau_lai_nap = tong_san_xuat_nap + lai_suat_nap
        
        # ĐƠN GIÁ NẮP
        don_gia_nap = tong_sau_lai_nap / so_luong
        
        # ===================== TÍNH GIÁ KHAY (NẾU CÓ) =====================
        if khay_co_khay:
            # Tương tự như nắp nhưng đơn giản hơn
            xa_lo_dai_khay = khay_dai + khay_bu_xen
            xa_lo_rong_khay = khay_rong + khay_cao + khay_bu_xen
            
            so_bat_khay = int(khay_so_bat.split('x')[0]) * int(khay_so_bat.split('x')[1])
            so_to_khay = math.ceil(khay_so_luong / so_bat_khay)
            
            # Bù hao khay: 20% cộng thêm bù hao thường
            bu_hao_khay_pct = 0.20
            bu_hao_to_khay = max(100, so_to_khay / so_bat_khay * bu_hao_khay_pct)
            so_to_khay_co_bu_hao = so_to_khay + bu_hao_to_khay
            
            # Lấy thông tin giấy khay
            dinh_luong_giay_khay = bang_gia_giay[bang_gia_giay['Ma_giay'] == khay_chat_lieu]['Dinh_luong'].values[0]
            gia_giay_khay = bang_gia_giay[bang_gia_giay['Ma_giay'] == khay_chat_lieu]['Gia'].values[0]
            
            chi_phi_giay_khay = (xa_lo_dai_khay / 100) * (xa_lo_rong_khay / 100) * so_to_khay_co_bu_hao * dinh_luong_giay_khay * gia_giay_khay
            
            # Kẽm khay
            kem_size_khay = {8: (56, 67), 10: (60, 73), 12: (64.5, 83), 16: (83, 103)}
            kem_dai_khay, kem_rong_khay = kem_size_khay.get(khay_may_in, (56, 67))
            so_to_kem_khay = khay_so_mau
            chi_phi_kem_khay = kem_dai_khay * kem_rong_khay * so_to_kem_khay * gia_kem
            
            # In khay
            gia_in_khay_map = {8: 90000, 10: 100000, 12: 170000, 16: 230000}
            gia_in_khay = gia_in_khay_map.get(khay_may_in, 100000)
            chi_phi_in_khay = so_to_kem_khay * gia_in_khay
            
            # Cán khay
            chi_phi_can_khay = 0
            if khay_can != 'Không':
                gia_can_khay = 0.22 if khay_can == "Mờ" else 0.2
                chi_phi_can_khay_temp = (xa_lo_dai_khay / 100) * (xa_lo_rong_khay / 100) * so_to_khay_co_bu_hao * gia_can_khay * khay_may_in
                chi_phi_can_khay = max(100000, chi_phi_can_khay_temp)
            
            # Bồi khay
            chi_phi_boi_khay = 0
            if khay_boi != 'Không':
                chi_phi_boi_khay = (math.ceil(xa_lo_dai_khay) / 100) * (math.ceil(xa_lo_rong_khay) / 100) * so_to_khay_co_bu_hao * 3800
                chi_phi_cong_boi_khay_temp = (xa_lo_dai_khay / 100) * (xa_lo_rong_khay / 100) * so_to_khay_co_bu_hao * 1300
                chi_phi_boi_khay += max(150000, chi_phi_cong_boi_khay_temp)
            
            # Gia công khay (định hình)
            chi_phi_gia_cong_khay = max(500000, 500 * (khay_so_luong / 1000))
            
            # Thùng cao su
            chi_phi_cao_su = 0
            if khay_thung_cao_su:
                chi_phi_cao_su = 1500000 + (khay_so_luong / 1000) * 200
            
            tong_san_xuat_khay = (chi_phi_giay_khay + chi_phi_kem_khay + chi_phi_in_khay +
                                 chi_phi_can_khay + chi_phi_boi_khay + chi_phi_gia_cong_khay +
                                 chi_phi_cao_su)
            
            lai_suat_khay = tong_san_xuat_khay * 0.25
            tong_sau_lai_khay = tong_san_xuat_khay + lai_suat_khay
            don_gia_khay = tong_sau_lai_khay / khay_so_luong
        else:
            tong_sau_lai_khay = 0
            don_gia_khay = 0
        
        # HIỂN THỊ KẾT QUẢ
        st.markdown("### 📊 KẾT QUẢ TÍNH TOÁN")
        
        col_nap, col_khay = st.columns(2)
        
        with col_nap:
            st.markdown("#### 📦 NẮP")
            st.markdown(f"**Xả lô:** {xa_lo_dai_nap:.2f} x {xa_lo_rong_nap:.2f} cm")
            st.markdown(f"**Số tờ in:** {so_to_in:,} tờ (Bù hao: +{bu_hao_to:.0f} tờ)")
            st.markdown("---")
            
            with st.expander("📋 Chi tiết chi phí", expanded=True):
                st.markdown(f"- Giấy in: **{chi_phi_giay_in:,.0f}** đ")
                st.markdown(f"- Kẽm: **{chi_phi_kem:,.0f}** đ")
                st.markdown(f"- In offset: **{chi_phi_in_offset:,.0f}** đ")
                st.markdown(f"- Cán: **{chi_phi_can:,.0f}** đ")
                if chi_phi_giay_boi > 0:
                    st.markdown(f"- Giấy bồi: **{chi_phi_giay_boi:,.0f}** đ")
                    st.markdown(f"- Công bồi: **{chi_phi_cong_boi:,.0f}** đ")
                st.markdown(f"- Gia công: **{chi_phi_gia_cong:,.0f}** đ")
                st.markdown(f"- Khuôn bạc: **{chi_phi_khuon_bac:,.0f}** đ")
                if chi_phi_in_mt > 0:
                    st.markdown(f"- In mặt trong: **{chi_phi_in_mt:,.0f}** đ")
                    st.markdown(f"- Kẽm MT: **{chi_phi_kem_mt:,.0f}** đ")
                if chi_phi_can_mt > 0:
                    st.markdown(f"- Cán mặt trong: **{chi_phi_can_mt:,.0f}** đ")
                if chi_phi_metalize > 0:
                    st.markdown(f"- Metalize: **{chi_phi_metalize:,.0f}** đ")
                if chi_phi_ep_nhu > 0:
                    st.markdown(f"- Ép nhũ: **{chi_phi_ep_nhu:,.0f}** đ")
                if chi_phi_thuc_noi > 0:
                    st.markdown(f"- Thúc nổi: **{chi_phi_thuc_noi:,.0f}** đ")
                if chi_phi_lan_van > 0:
                    st.markdown(f"- Lăn vân: **{chi_phi_lan_van:,.0f}** đ")
                if chi_phi_offset_uv > 0:
                    st.markdown(f"- Offset UV: **{chi_phi_offset_uv:,.0f}** đ")
                st.markdown(f"- Thùng: **{chi_phi_thung:,.0f}** đ")
                if chi_phi_van_chuyen > 0:
                    st.markdown(f"- Vận chuyển: **{chi_phi_van_chuyen:,.0f}** đ")
                
                st.markdown("---")
                st.markdown(f"**Tổng sản xuất:** {tong_san_xuat_nap:,.0f} đ")
                st.markdown(f"**Lãi suất (25%):** {lai_suat_nap:,.0f} đ")
            
            st.markdown(f'<div class="price-display">Đơn giá NẮP<br/>{don_gia_nap:,.2f} đ/cái</div>', unsafe_allow_html=True)
        
        with col_khay:
            if khay_co_khay:
                st.markdown("#### 🍕 KHAY")
                st.markdown(f"**Xả lô:** {xa_lo_dai_khay:.2f} x {xa_lo_rong_khay:.2f} cm")
                st.markdown(f"**Số tờ in:** {so_to_khay:,} tờ")
                st.markdown("---")
                
                st.markdown(f"**Tổng sản xuất:** {tong_san_xuat_khay:,.0f} đ")
                st.markdown(f"**Lãi suất (25%):** {lai_suat_khay:,.0f} đ")
                
                st.markdown(f'<div class="price-display">Đơn giá KHAY<br/>{don_gia_khay:,.2f} đ/cái</div>', unsafe_allow_html=True)
            else:
                st.info("Không có khay định hình")
        
        # Tổng hợp
        st.markdown("---")
        st.markdown("### 🎯 TỔNG HỢP")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tổng chi phí NẮP", f"{tong_sau_lai_nap:,.0f} đ")
        with col2:
            if khay_co_khay:
                st.metric("Tổng chi phí KHAY", f"{tong_sau_lai_khay:,.0f} đ")
                tong_tat_ca = tong_sau_lai_nap + tong_sau_lai_khay
            else:
                tong_tat_ca = tong_sau_lai_nap
            st.metric("TỔNG", f"{tong_tat_ca:,.0f} đ")
        with col3:
            if khay_co_khay and khay_so_luong > 0 and so_luong > 0:
                don_gia_bo = don_gia_nap + don_gia_khay
                st.metric("Giá BỘ (Nắp+Khay)", f"{don_gia_bo:,.2f} đ")

with tab2:
    st.markdown('<div class="section-header">📋 BẢNG GIÁ GIẤY & VẬT LIỆU</div>', unsafe_allow_html=True)
    
    df_display = bang_gia_giay.copy()
    df_display.columns = ['Tên giấy', 'Mã giấy', 'Định lượng (g/m²)', 'Giá (VNĐ/kg)']
    
    st.dataframe(df_display, height=600)
    
    st.markdown("---")
    st.markdown("### 🔍 Tra cứu giá giấy")
    col1, col2 = st.columns(2)
    with col1:
        ma_giay_tim = st.selectbox("Chọn mã giấy", options=bang_gia_giay['Ma_giay'].unique())
    with col2:
        if ma_giay_tim:
            gia_tim = bang_gia_giay[bang_gia_giay['Ma_giay'] == ma_giay_tim]['Gia'].values[0]
            dinh_luong_tim = bang_gia_giay[bang_gia_giay['Ma_giay'] == ma_giay_tim]['Dinh_luong'].values[0]
            st.success(f"**Giá:** {gia_tim:,.2f} VNĐ/kg | **Định lượng:** {dinh_luong_tim} g/m²")

with tab3:
    st.markdown('<div class="section-header">📖 HƯỚNG DẪN SỬ DỤNG</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Hướng dẫn tính giá
    
    Ứng dụng tính giá dựa trên công thức chính xác từ file Excel gốc.
    
    #### 📝 Các bước thực hiện:
    
    1. **Nhập thông tin cơ bản:**
       - Số lượng sản phẩm
       - Kích thước: Dài, Rộng, Cao, Thành, Tai cài, Bù, Nới xén
    
    2. **Chọn chất liệu:**
       - Chọn loại giấy từ bảng giá
       - Chọn loại cán (Mờ/Bóng/Không)
       - Chọn loại bồi nếu cần
    
    3. **Cấu hình in ấn:**
       - Chọn máy in (8/10/12/16/UV)
       - Số màu in
       - Số bát/tờ (1x1, 1x2, 2x2...)
    
    4. **Gia công đặc biệt (nếu có):**
       - In/Cán mặt trong
       - Ép nhũ, Thúc nổi
       - Lăn vân, Metalize, UV
    
    5. **Nhấn "TÍNH GIÁ"** để xem kết quả
    
    ### 📐 Công thức tính toán
    
    **Xả lô:**
    - Dài = Dài + Rộng + (Thành × 2) + Tai cài + Bù
    - Rộng = Rộng + Cao + (Thành × 2) + Nới xén
    
    **Số tờ:**
    - Số tờ in = Số lượng ÷ Số bát
    - Bù hao = 4-5% (tối thiểu 100-150 tờ)
    
    **Chi phí:**
    - Giấy = (Dài/100) × (Rộng/100) × Số tờ × Định lượng × Giá
    - Kẽm = Kích thước × Số màu × Giá kẽm
    - In = Số màu × Giá in (theo máy in)
    - Cán = Diện tích × Giá cán × Máy in
    - Bồi = Giấy bồi + Công bồi
    - Gia công = Theo loại và số lượng
    
    **Lãi suất:** 25% trên tổng chi phí sản xuất
    
    ### 💡 Lưu ý quan trọng
    
    - Tất cả chi phí đã bao gồm lãi suất 25%
    - Kích thước tính bằng cm
    - Giá giấy tính theo VNĐ/kg
    - Các chi phí có mức tối thiểu theo quy định
    - Bù hao được tính tự động theo loại gia công
    
    ### 📞 Hỗ trợ
    
    Nếu có thắc mắc, vui lòng liên hệ bộ phận kỹ thuật.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Hệ thống Tính Giá Bao Bì - Hộp Sóng | © 2024</p>
    <p>Phát triển bởi: Streamlit & Python | Dựa trên công thức Excel chính xác</p>
</div>
""", unsafe_allow_html=True)
