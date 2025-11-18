import streamlit as st
import pandas as pd
import math

# Cấu hình trang
st.set_page_config(page_title="Hệ thống Tính Giá Bao Bì", layout="wide", page_icon="📦")

# Load bảng giá giấy
@st.cache_data
def load_bang_gia_giay(file_path='Bang tinh gia.xlsx'):
    """Load bảng giá từ file Excel"""
    try:
        df = pd.read_excel(file_path, sheet_name='Bảng giá giấy', header=1)
        # Giữ nguyên tên cột từ Excel: 'Tên giấy', 'Mã giấy', 'Định lượng', 'Giá'
        df = df.dropna(subset=['Mã giấy'])
        # Chuẩn hóa mã giấy - uppercase và loại bỏ khoảng trắng
        df['Mã giấy'] = df['Mã giấy'].astype(str).str.upper().str.strip()
        return df
    except Exception as e:
        st.error(f"Lỗi khi đọc file: {str(e)}")
        return pd.DataFrame(columns=['Tên giấy', 'Mã giấy', 'Định lượng', 'Giá'])

def load_bang_gia_from_uploaded_file(uploaded_file):
    """Load bảng giá từ file được upload"""
    try:
        # Thử đọc với nhiều sheet name khác nhau
        sheet_names_to_try = ['Bảng giá giấy', 'Bang gia giay', 'Sheet1', 0]
        
        df = None
        sheet_used = None
        
        # Đọc danh sách sheet trong file
        try:
            xl_file = pd.ExcelFile(uploaded_file)
            available_sheets = xl_file.sheet_names
            st.info(f"📑 File có {len(available_sheets)} sheet: {', '.join(available_sheets)}")
        except Exception as e:
            st.warning(f"Không đọc được danh sách sheet: {e}")
            available_sheets = []
        
        # Thử đọc từng sheet
        for sheet_name in sheet_names_to_try:
            try:
                uploaded_file.seek(0)  # Reset file pointer
                df_temp = pd.read_excel(uploaded_file, sheet_name=sheet_name, header=1)
                
                # Kiểm tra xem có đúng cột cần thiết không
                if 'Mã giấy' in df_temp.columns or len(df_temp.columns) >= 4:
                    df = df_temp
                    sheet_used = sheet_name
                    st.success(f"✓ Đọc thành công từ sheet: '{sheet_name}'")
                    break
            except:
                continue
        
        if df is None:
            st.error(f"❌ Không tìm thấy sheet 'Bảng giá giấy' hoặc dữ liệu phù hợp!")
            st.info("💡 File Excel cần có sheet 'Bảng giá giấy' với format:\n- Dòng 1: Tiêu đề\n- Dòng 2: Tên giấy | Mã giấy | Định lượng | Giá")
            return None
        
        # Xử lý tên cột
        if 'Mã giấy' not in df.columns:
            # Tự động đặt tên cột nếu không có
            if len(df.columns) >= 4:
                df.columns = ['Tên giấy', 'Mã giấy', 'Định lượng', 'Giá']
                st.warning("⚠️ Tự động đặt tên cột: Tên giấy | Mã giấy | Định lượng | Giá")
        
        # Giữ nguyên tên cột từ Excel
        df = df.dropna(subset=['Mã giấy'])
        
        if df.empty:
            st.error("❌ Không có dữ liệu sau khi lọc! Kiểm tra cột 'Mã giấy' có giá trị không.")
            return None
        
        # Chuẩn hóa mã giấy - uppercase và loại bỏ khoảng trắng
        df['Mã giấy'] = df['Mã giấy'].astype(str).str.upper().str.strip()
        
        # Kiểm tra dữ liệu
        st.success(f"✅ Đã đọc {len(df)} loại giấy từ sheet '{sheet_used}'")
        
        # Hiển thị preview
        with st.expander("👁️ Xem trước dữ liệu (5 dòng đầu)"):
            st.dataframe(df.head())
        
        return df
        
    except Exception as e:
        st.error(f"❌ Lỗi khi đọc file upload: {str(e)}")
        st.info("🔍 Chi tiết lỗi: " + str(type(e).__name__))
        return None

# Khởi tạo session state để lưu bảng giá
if 'bang_gia_giay' not in st.session_state:
    st.session_state.bang_gia_giay = load_bang_gia_giay()

bang_gia_giay = st.session_state.bang_gia_giay

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
    .info-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📦 HỆ THỐNG TÍNH GIÁ BAO BÌ - HỘP SÓNG</div>', unsafe_allow_html=True)

# Tabs chính
tab1, tab2, tab3 = st.tabs(["🎯 NẮP CÀI PIZZA", "📋 BẢNG GIÁ GIẤY", "ℹ️ HƯỚNG DẪN"])

with tab1:
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown('<div class="section-header">📊 THÔNG TIN CHUNG - NẮP</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            so_luong = st.number_input("Số lượng (cái)", min_value=1, value=10000, step=1000)
        with col2:
            st.metric("Đơn giá tính toán", "Tự động")
        
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
        st.markdown('<div class="section-header">🎨 CHẤT LIỆU & IN ẤN NẮP</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            # Lọc danh sách giấy
            chat_lieu_options = bang_gia_giay['Mã giấy'].unique().tolist()
            default_index = chat_lieu_options.index('I300') if 'I300' in chat_lieu_options else 0
            nap_chat_lieu = st.selectbox("Chất liệu", options=chat_lieu_options, index=default_index, key="nap_chat_lieu")
        with col2:
            nap_can = st.selectbox("Cán", options=['Mờ', 'Bóng', 'Không'], index=0, key="nap_can")
        
        col1, col2 = st.columns(2)
        with col1:
            nap_so_bat = st.selectbox("Số bát/tờ", options=['1x1', '1x2', '2x2', '2x3', '3x3'], index=0, key="nap_so_bat")
        with col2:
            nap_day_xach = st.number_input("Dây xách", min_value=0, value=0, key="nap_day_xach")
        
        col1, col2 = st.columns(2)
        with col1:
            nap_van_chuyen = st.number_input("Vận chuyển", min_value=0, value=0, key="nap_van_chuyen")
        with col2:
            nap_boi = st.selectbox("Bồi", options=['Không', 'Sóng E Nâu', 'Sóng B Nâu', 'Sóng E Trắng'], index=1, key="nap_boi")
        
        # Định lượng & Bù hao
        st.markdown('<div class="section-header">⚙️ THÔNG SỐ GIẤ & BỒI - NẮP</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            nap_dinh_luong = st.number_input("Định lượng giấy", min_value=0, value=300, key="nap_dinh_luong")
        with col2:
            nap_bu_hao = st.number_input("Bù hao (%)", min_value=0, value=400, key="nap_bu_hao")
        with col3:
            nap_dinh_luong_boi = st.number_input("Định lượng bồi", min_value=0, value=1, key="nap_dinh_luong_boi")
        with col4:
            nap_bu_hao_boi = st.number_input("Bù hao bồi", min_value=0, value=300, key="nap_bu_hao_boi")
        
        # Máy in
        st.markdown('<div class="section-header">🖨️ THÔNG SỐ IN - NẮP</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            nap_may_in = st.selectbox("Máy in", options=[10, 16, 20, 24], index=1, key="nap_may_in")
        with col2:
            nap_so_mau = st.number_input("Số màu", min_value=0, value=4, key="nap_so_mau")
        with col3:
            nap_noi_dung = st.number_input("Nội dung", min_value=1, value=1, key="nap_noi_dung")
        
        nap_cai_thung = st.number_input("Cái/Thùng", min_value=1, value=200, key="nap_cai_thung")
        
        # Gia công
        st.markdown('<div class="section-header">✨ GIA CÔNG ĐẶC BIỆT - NẮP</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            nap_gia_can = st.number_input("Giá cán", min_value=0.0, value=0.22, step=0.01, key="nap_gia_can")
        with col2:
            nap_gia_in = st.number_input("Giá in", min_value=0, value=230000, step=1000, key="nap_gia_in")
        with col3:
            nap_gia_luot = st.number_input("Giá lượt", min_value=0, value=80, key="nap_gia_luot")
        with col4:
            nap_gia_giay = st.number_input("Giá giấy", min_value=0.0, value=17.4, step=0.1, key="nap_gia_giay")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            nap_gia_giay_boi = st.number_input("Giá Giấy Bồi", min_value=0, value=3800, key="nap_gia_giay_boi")
        with col2:
            nap_gia_boi = st.number_input("Giá Bồi", min_value=0, value=1300, key="nap_gia_boi")
        with col3:
            nap_gia_metalize = st.number_input("Giá Metalize", min_value=0, value=0, key="nap_gia_metalize")
        with col4:
            nap_ghep_metalize = st.checkbox("Ghép Màng Metalize", value=False, key="nap_ghep_metalize")
        
        # Các gia công khác
        col1, col2 = st.columns(2)
        with col1:
            nap_in_mat_trong = st.number_input("In Mặt trong (màu)", min_value=0, value=0, key="nap_in_mat_trong")
            nap_gia_in_mat_trong = st.number_input("Giá in mặt trong", min_value=0, value=250000, key="nap_gia_in_mat_trong")
            nap_chi_phi_in_mat_trong = st.number_input("Chi phí in mt/1000", min_value=0, value=100, key="nap_chi_phi_in_mat_trong")
        with col2:
            nap_can_mat_trong = st.number_input("Cán Mặt trong", min_value=0, value=0, key="nap_can_mat_trong")
            nap_gia_can_mat_trong = st.number_input("Giá cán mặt trong", min_value=0, value=150000, key="nap_gia_can_mat_trong")
            nap_chi_phi_can_mat_trong = st.number_input("Chi phí cán mt/1000", min_value=0, value=50, key="nap_chi_phi_can_mat_trong")
        
        nap_lan_van = st.number_input("Lăn Vân", min_value=0, value=0, key="nap_lan_van")
        nap_in_offset_uv = st.number_input("In Offset UV", min_value=0, value=0, key="nap_in_offset_uv")
        
        # Ép nhũ và thúc nổi
        st.markdown("**Ép nhũ & Thúc nổi**")
        col1, col2, col3 = st.columns(3)
        with col1:
            nap_ep_nhu_1 = st.number_input("Ép nhũ 1", min_value=0, value=0, key="nap_ep_nhu_1")
            nap_ep_nhu_1_mat = st.selectbox("Mặt ép 1", options=['1 Mặt', '2 Mặt'], key="nap_ep_nhu_1_mat")
        with col2:
            nap_ep_nhu_2 = st.number_input("Ép nhũ 2", min_value=0, value=0, key="nap_ep_nhu_2")
            nap_ep_nhu_2_mat = st.selectbox("Mặt ép 2", options=['1 Mặt', '2 Mặt'], key="nap_ep_nhu_2_mat")
        with col3:
            nap_ep_nhu_3 = st.number_input("Ép nhũ 3", min_value=0, value=0, key="nap_ep_nhu_3")
            nap_ep_nhu_3_mat = st.selectbox("Mặt ép 3", options=['1 Mặt', '2 Mặt'], key="nap_ep_nhu_3_mat")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            nap_thuc_noi_1 = st.number_input("Thúc nổi 1", min_value=0, value=0, key="nap_thuc_noi_1")
        with col2:
            nap_thuc_noi_2 = st.number_input("Thúc nổi 2", min_value=0, value=0, key="nap_thuc_noi_2")
        with col3:
            nap_thuc_noi_3 = st.number_input("Thúc nổi 3", min_value=0, value=0, key="nap_thuc_noi_3")

    with col_right:
        st.markdown('<div class="section-header">📊 THÔNG TIN KHAY ĐỊNH HÌNH</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            khay_so_luong = st.number_input("Số lượng khay", min_value=0, value=0, step=100, key="khay_so_luong")
        with col2:
            st.metric("Đơn giá khay", "Tự động")
        
        # Kích thước Khay
        st.markdown('<div class="section-header">📐 KÍCH THƯỚC KHAY</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            khay_dai = st.number_input("Dài (cm)", min_value=0.0, value=31.0, step=0.1, key="khay_dai")
        with col2:
            khay_rong = st.number_input("Rộng (cm)", min_value=0.0, value=21.6, step=0.1, key="khay_rong")
        with col3:
            khay_cao = st.number_input("Cao (cm)", min_value=0.0, value=4.0, step=0.1, key="khay_cao")
        
        khay_bu_xen = st.number_input("Bù xén Cao su/Foam", min_value=0.0, value=0.4, step=0.1, key="khay_bu_xen")
        
        # Chất liệu Khay
        st.markdown('<div class="section-header">🎨 CHẤT LIỆU & IN ẤN KHAY</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            khay_chat_lieu = st.selectbox("Chất liệu", options=chat_lieu_options, index=default_index, key="khay_chat_lieu")
        with col2:
            khay_can = st.selectbox("Cán", options=['Mờ', 'Bóng', 'Không'], index=0, key="khay_can")
        
        col1, col2 = st.columns(2)
        with col1:
            khay_so_bat = st.selectbox("Số bát/tờ", options=['1x1', '1x2', '2x2', '2x3', '3x3'], index=1, key="khay_so_bat")
        with col2:
            khay_bu_hao_khay = st.number_input("Bù hao khay (%)", min_value=0, value=20, key="khay_bu_hao_khay")
        
        col1, col2 = st.columns(2)
        with col1:
            khay_day_xach = st.number_input("Dây xách", min_value=0, value=0, key="khay_day_xach")
        with col2:
            khay_van_chuyen = st.number_input("Vận chuyển", min_value=0, value=0, key="khay_van_chuyen")
        
        khay_boi = st.selectbox("Bồi", options=['Không', 'Sóng E Nâu', 'Sóng B Nâu', 'Sóng E Trắng'], index=1, key="khay_boi")
        
        # Định lượng & Bù hao Khay
        st.markdown('<div class="section-header">⚙️ THÔNG SỐ GIẤY & BỒI - KHAY</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            khay_dinh_luong = st.number_input("Định lượng giấy", min_value=0, value=300, key="khay_dinh_luong")
        with col2:
            khay_bu_hao = st.number_input("Bù hao (%)", min_value=0, value=100, key="khay_bu_hao")
        with col3:
            khay_dinh_luong_boi = st.number_input("Định lượng bồi", min_value=0, value=1, key="khay_dinh_luong_boi")
        with col4:
            khay_bu_hao_boi = st.number_input("Bù hao bồi", min_value=0, value=100, key="khay_bu_hao_boi")
        
        # Máy in Khay
        st.markdown('<div class="section-header">🖨️ THÔNG SỐ IN - KHAY</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            khay_may_in = st.selectbox("Máy in", options=[10, 16, 20, 24], index=0, key="khay_may_in")
        with col2:
            khay_so_mau = st.number_input("Số màu", min_value=0, value=1, key="khay_so_mau")
        with col3:
            khay_noi_dung = st.number_input("Nội dung", min_value=1, value=1, key="khay_noi_dung")
        
        khay_cai_thung = st.number_input("Cái/Thùng", min_value=1, value=1500, key="khay_cai_thung")
        
        # Gia công Khay
        st.markdown('<div class="section-header">✨ GIA CÔNG ĐẶC BIỆT - KHAY</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            khay_gia_can = st.number_input("Giá cán", min_value=0.0, value=0.22, step=0.01, key="khay_gia_can")
        with col2:
            khay_gia_in = st.number_input("Giá in", min_value=0, value=100000, step=1000, key="khay_gia_in")
        with col3:
            khay_gia_luot = st.number_input("Giá lượt", min_value=0, value=40, key="khay_gia_luot")
        with col4:
            khay_gia_giay = st.number_input("Giá giấy", min_value=0.0, value=17.4, step=0.1, key="khay_gia_giay")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            khay_gia_giay_boi = st.number_input("Giá Giấy Bồi", min_value=0, value=3800, key="khay_gia_giay_boi")
        with col2:
            khay_gia_boi = st.number_input("Giá Bồi", min_value=0, value=1300, key="khay_gia_boi")
        with col3:
            khay_gia_metalize = st.number_input("Giá Metalize", min_value=0, value=0, key="khay_gia_metalize")
        with col4:
            khay_ghep_metalize = st.checkbox("Ghép Màng Metalize", value=False, key="khay_ghep_metalize")
        
        # Thùng Cao Su
        st.markdown('<div class="section-header">🔧 THÔNG SỐ THÙNG CAO SU/FOAM</div>', unsafe_allow_html=True)
        khay_thung_cao_su = st.number_input("Thùng Cao Su", min_value=0, value=0, key="khay_thung_cao_su")
        
        # Gia công khác cho khay
        col1, col2 = st.columns(2)
        with col1:
            khay_in_mat_trong = st.number_input("In Mặt trong (màu)", min_value=0, value=0, key="khay_in_mat_trong")
            khay_gia_in_mat_trong = st.number_input("Giá in mặt trong", min_value=0, value=150000, key="khay_gia_in_mat_trong")
        with col2:
            khay_can_mat_trong = st.number_input("Cán Mặt trong", min_value=0, value=0, key="khay_can_mat_trong")
            khay_gia_can_mat_trong = st.number_input("Giá cán mặt trong", min_value=0, value=100000, key="khay_gia_can_mat_trong")
        
        khay_lan_van = st.number_input("Lăn Vân", min_value=0, value=0, key="khay_lan_van")
        khay_in_offset_uv = st.number_input("In Offset UV", min_value=0, value=0, key="khay_in_offset_uv")
        
        # Ép nhũ và thúc nổi khay
        st.markdown("**Ép nhũ & Thúc nổi - KHAY**")
        col1, col2, col3 = st.columns(3)
        with col1:
            khay_ep_nhu_1 = st.number_input("Ép nhũ 1", min_value=0, value=0, key="khay_ep_nhu_1")
        with col2:
            khay_ep_nhu_2 = st.number_input("Ép nhũ 2", min_value=0, value=0, key="khay_ep_nhu_2")
        with col3:
            khay_ep_nhu_3 = st.number_input("Ép nhũ 3", min_value=0, value=0, key="khay_ep_nhu_3")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            khay_thuc_noi_1 = st.number_input("Thúc nổi 1", min_value=0, value=0, key="khay_thuc_noi_1")
        with col2:
            khay_thuc_noi_2 = st.number_input("Thúc nổi 2", min_value=0, value=0, key="khay_thuc_noi_2")
        with col3:
            khay_thuc_noi_3 = st.number_input("Thúc nổi 3", min_value=0, value=0, key="khay_thuc_noi_3")

    # TÍNH TOÁN GIÁ
    st.markdown("---")
    st.markdown('<div class="section-header">💰 TÍNH TOÁN GIÁ THÀNH</div>', unsafe_allow_html=True)
    
    if st.button("🧮 TÍNH GIÁ", type="primary", use_container_width=True):
        # Hàm tính toán
        def tinh_xalo(dai, rong, cao, thanh, tai_cai, bu, noi_xen):
            """Tính diện tích xả lô"""
            xa_lo_dai = dai + rong + (thanh * 2) + tai_cai + bu
            xa_lo_rong = rong + cao + (thanh * 2) + noi_xen
            return xa_lo_dai, xa_lo_rong
        
        def tinh_so_bat(so_bat_str):
            """Chuyển số bát thành số nguyên"""
            parts = so_bat_str.split('x')
            return int(parts[0]) * int(parts[1])
        
        def tinh_gia_nap():
            """Tính giá nắp"""
            # Tính xả lô
            xa_lo_dai, xa_lo_rong = tinh_xalo(nap_dai, nap_rong, nap_cao, nap_thanh, nap_tai_cai, nap_bu, nap_noi_xen)
            dien_tich_xalo = (xa_lo_dai * xa_lo_rong) / 10000  # m2
            
            # Số bát
            so_bat = tinh_so_bat(nap_so_bat)
            
            # Số tờ cần
            so_to = math.ceil(so_luong / so_bat)
            
            # Chi phí giấy
            gia_giay_m2 = nap_gia_giay
            tong_dien_tich = dien_tich_xalo * so_to * (1 + nap_bu_hao / 100)
            chi_phi_giay = tong_dien_tich * gia_giay_m2
            
            # Chi phí in
            chi_phi_in = 0
            if nap_so_mau > 0:
                chi_phi_pha = nap_gia_in * math.ceil(nap_so_mau / 2)  # 2 màu = 1 pha
                chi_phi_in_luot = (so_to / 1000) * nap_gia_luot
                chi_phi_in = chi_phi_pha + chi_phi_in_luot
            
            # Chi phí cán
            chi_phi_can = 0
            if nap_can != 'Không':
                chi_phi_can = tong_dien_tich * nap_gia_can * nap_may_in
            
            # Chi phí bồi
            chi_phi_boi = 0
            if nap_boi != 'Không':
                chi_phi_boi_giay = tong_dien_tich * nap_gia_giay_boi
                chi_phi_boi_gia_cong = tong_dien_tich * nap_gia_boi
                chi_phi_boi = chi_phi_boi_giay + chi_phi_boi_gia_cong
            
            # Chi phí lượt (gia công)
            chi_phi_gia_cong = (so_luong / 1000) * 350  # Gia công nắp cài
            
            # Chi phí in mặt trong
            chi_phi_in_mt = 0
            if nap_in_mat_trong > 0:
                chi_phi_in_mt = nap_gia_in_mat_trong + (so_luong / 1000) * nap_chi_phi_in_mat_trong
            
            # Chi phí cán mặt trong
            chi_phi_can_mt = 0
            if nap_can_mat_trong > 0:
                chi_phi_can_mt = nap_gia_can_mat_trong + (so_luong / 1000) * nap_chi_phi_can_mat_trong
            
            # Chi phí ép nhũ
            chi_phi_ep_nhu = 0
            for ep_nhu in [nap_ep_nhu_1, nap_ep_nhu_2, nap_ep_nhu_3]:
                if ep_nhu > 0:
                    chi_phi_ep_nhu += 250000 + (so_luong / 1000) * 100
            
            # Chi phí thúc nổi
            chi_phi_thuc_noi = 0
            for thuc_noi in [nap_thuc_noi_1, nap_thuc_noi_2, nap_thuc_noi_3]:
                if thuc_noi > 0:
                    chi_phi_thuc_noi += 250000 + (so_luong / 1000) * 100
            
            # Chi phí metalize
            chi_phi_metalize = 0
            if nap_ghep_metalize:
                chi_phi_metalize = tong_dien_tich * nap_gia_metalize
            
            # Chi phí vận chuyển
            chi_phi_van_chuyen = nap_van_chuyen
            
            # Tổng chi phí
            tong_chi_phi = (chi_phi_giay + chi_phi_in + chi_phi_can + chi_phi_boi + 
                           chi_phi_gia_cong + chi_phi_in_mt + chi_phi_can_mt + 
                           chi_phi_ep_nhu + chi_phi_thuc_noi + chi_phi_metalize + chi_phi_van_chuyen)
            
            don_gia = tong_chi_phi / so_luong
            
            return {
                'xa_lo_dai': xa_lo_dai,
                'xa_lo_rong': xa_lo_rong,
                'dien_tich_xalo': dien_tich_xalo,
                'so_to': so_to,
                'chi_phi_giay': chi_phi_giay,
                'chi_phi_in': chi_phi_in,
                'chi_phi_can': chi_phi_can,
                'chi_phi_boi': chi_phi_boi,
                'chi_phi_gia_cong': chi_phi_gia_cong,
                'chi_phi_in_mt': chi_phi_in_mt,
                'chi_phi_can_mt': chi_phi_can_mt,
                'chi_phi_ep_nhu': chi_phi_ep_nhu,
                'chi_phi_thuc_noi': chi_phi_thuc_noi,
                'chi_phi_metalize': chi_phi_metalize,
                'chi_phi_van_chuyen': chi_phi_van_chuyen,
                'tong_chi_phi': tong_chi_phi,
                'don_gia': don_gia
            }
        
        def tinh_gia_khay():
            """Tính giá khay"""
            if khay_so_luong == 0:
                return None
            
            # Tính diện tích khay (đơn giản hóa - không có tai cài)
            xa_lo_dai = khay_dai + khay_bu_xen
            xa_lo_rong = khay_rong + khay_cao + khay_bu_xen
            dien_tich_xalo = (xa_lo_dai * xa_lo_rong) / 10000  # m2
            
            # Số bát
            so_bat = tinh_so_bat(khay_so_bat)
            
            # Số tờ cần
            so_to = math.ceil(khay_so_luong / so_bat)
            
            # Chi phí giấy
            gia_giay_m2 = khay_gia_giay
            tong_dien_tich = dien_tich_xalo * so_to * (1 + (khay_bu_hao + khay_bu_hao_khay) / 100)
            chi_phi_giay = tong_dien_tich * gia_giay_m2
            
            # Chi phí in
            chi_phi_in = 0
            if khay_so_mau > 0:
                chi_phi_pha = khay_gia_in * math.ceil(khay_so_mau / 2)
                chi_phi_in_luot = (so_to / 1000) * khay_gia_luot
                chi_phi_in = chi_phi_pha + chi_phi_in_luot
            
            # Chi phí cán
            chi_phi_can = 0
            if khay_can != 'Không':
                chi_phi_can = tong_dien_tich * khay_gia_can * khay_may_in
            
            # Chi phí bồi
            chi_phi_boi = 0
            if khay_boi != 'Không':
                chi_phi_boi_giay = tong_dien_tich * khay_gia_giay_boi
                chi_phi_boi_gia_cong = tong_dien_tich * khay_gia_boi
                chi_phi_boi = chi_phi_boi_giay + chi_phi_boi_gia_cong
            
            # Chi phí gia công (lượt + định hình)
            chi_phi_gia_cong = (khay_so_luong / 1000) * 500  # Gia công định hình
            
            # Chi phí thùng cao su
            chi_phi_cao_su = 0
            if khay_thung_cao_su > 0:
                chi_phi_cao_su = 1500000 + (khay_so_luong / 1000) * 200
            
            # Tổng chi phí
            tong_chi_phi = (chi_phi_giay + chi_phi_in + chi_phi_can + chi_phi_boi + 
                           chi_phi_gia_cong + chi_phi_cao_su + khay_van_chuyen)
            
            don_gia = tong_chi_phi / khay_so_luong if khay_so_luong > 0 else 0
            
            return {
                'xa_lo_dai': xa_lo_dai,
                'xa_lo_rong': xa_lo_rong,
                'dien_tich_xalo': dien_tich_xalo,
                'so_to': so_to,
                'chi_phi_giay': chi_phi_giay,
                'chi_phi_in': chi_phi_in,
                'chi_phi_can': chi_phi_can,
                'chi_phi_boi': chi_phi_boi,
                'chi_phi_gia_cong': chi_phi_gia_cong,
                'chi_phi_cao_su': chi_phi_cao_su,
                'tong_chi_phi': tong_chi_phi,
                'don_gia': don_gia
            }
        
        # Tính giá nắp
        ket_qua_nap = tinh_gia_nap()
        
        # Tính giá khay
        ket_qua_khay = tinh_gia_khay()
        
        # Hiển thị kết quả
        st.markdown("### 📊 KẾT QUẢ TÍNH TOÁN CHI TIẾT")
        
        col_nap, col_khay = st.columns(2)
        
        with col_nap:
            st.markdown("#### 📦 NẮP")
            st.markdown(f"**Kích thước xả lô:** {ket_qua_nap['xa_lo_dai']:.2f} x {ket_qua_nap['xa_lo_rong']:.2f} cm")
            st.markdown(f"**Diện tích xả lô:** {ket_qua_nap['dien_tich_xalo']:.4f} m²")
            st.markdown(f"**Số tờ cần in:** {ket_qua_nap['so_to']:,} tờ")
            st.markdown("---")
            
            st.markdown("**Chi phí chi tiết:**")
            st.markdown(f"- Chi phí giấy: {ket_qua_nap['chi_phi_giay']:,.0f} đ")
            st.markdown(f"- Chi phí in: {ket_qua_nap['chi_phi_in']:,.0f} đ")
            st.markdown(f"- Chi phí cán: {ket_qua_nap['chi_phi_can']:,.0f} đ")
            st.markdown(f"- Chi phí bồi: {ket_qua_nap['chi_phi_boi']:,.0f} đ")
            st.markdown(f"- Chi phí gia công: {ket_qua_nap['chi_phi_gia_cong']:,.0f} đ")
            if ket_qua_nap['chi_phi_in_mt'] > 0:
                st.markdown(f"- Chi phí in mặt trong: {ket_qua_nap['chi_phi_in_mt']:,.0f} đ")
            if ket_qua_nap['chi_phi_can_mt'] > 0:
                st.markdown(f"- Chi phí cán mặt trong: {ket_qua_nap['chi_phi_can_mt']:,.0f} đ")
            if ket_qua_nap['chi_phi_ep_nhu'] > 0:
                st.markdown(f"- Chi phí ép nhũ: {ket_qua_nap['chi_phi_ep_nhu']:,.0f} đ")
            if ket_qua_nap['chi_phi_thuc_noi'] > 0:
                st.markdown(f"- Chi phí thúc nổi: {ket_qua_nap['chi_phi_thuc_noi']:,.0f} đ")
            if ket_qua_nap['chi_phi_metalize'] > 0:
                st.markdown(f"- Chi phí metalize: {ket_qua_nap['chi_phi_metalize']:,.0f} đ")
            if ket_qua_nap['chi_phi_van_chuyen'] > 0:
                st.markdown(f"- Chi phí vận chuyển: {ket_qua_nap['chi_phi_van_chuyen']:,.0f} đ")
            
            st.markdown("---")
            st.markdown(f"**💰 Tổng chi phí:** {ket_qua_nap['tong_chi_phi']:,.0f} đ")
            st.markdown(f'<div class="price-display">Đơn giá NẮP: {ket_qua_nap["don_gia"]:,.2f} đ/cái</div>', unsafe_allow_html=True)
        
        with col_khay:
            if ket_qua_khay:
                st.markdown("#### 🍕 KHAY ĐỊNH HÌNH")
                st.markdown(f"**Kích thước xả lô:** {ket_qua_khay['xa_lo_dai']:.2f} x {ket_qua_khay['xa_lo_rong']:.2f} cm")
                st.markdown(f"**Diện tích xả lô:** {ket_qua_khay['dien_tich_xalo']:.4f} m²")
                st.markdown(f"**Số tờ cần in:** {ket_qua_khay['so_to']:,} tờ")
                st.markdown("---")
                
                st.markdown("**Chi phí chi tiết:**")
                st.markdown(f"- Chi phí giấy: {ket_qua_khay['chi_phi_giay']:,.0f} đ")
                st.markdown(f"- Chi phí in: {ket_qua_khay['chi_phi_in']:,.0f} đ")
                st.markdown(f"- Chi phí cán: {ket_qua_khay['chi_phi_can']:,.0f} đ")
                st.markdown(f"- Chi phí bồi: {ket_qua_khay['chi_phi_boi']:,.0f} đ")
                st.markdown(f"- Chi phí gia công: {ket_qua_khay['chi_phi_gia_cong']:,.0f} đ")
                if ket_qua_khay['chi_phi_cao_su'] > 0:
                    st.markdown(f"- Chi phí thùng cao su: {ket_qua_khay['chi_phi_cao_su']:,.0f} đ")
                
                st.markdown("---")
                st.markdown(f"**💰 Tổng chi phí:** {ket_qua_khay['tong_chi_phi']:,.0f} đ")
                st.markdown(f'<div class="price-display">Đơn giá KHAY: {ket_qua_khay["don_gia"]:,.2f} đ/cái</div>', unsafe_allow_html=True)
            else:
                st.info("Không có khay định hình (số lượng = 0)")
        
        # Tổng hợp
        st.markdown("---")
        st.markdown("### 🎯 TỔNG HỢP GIÁ THÀNH")
        
        tong_chi_phi_nap = ket_qua_nap['tong_chi_phi']
        tong_chi_phi_khay = ket_qua_khay['tong_chi_phi'] if ket_qua_khay else 0
        tong_chi_phi_chung = tong_chi_phi_nap + tong_chi_phi_khay
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Tổng chi phí NẮP", f"{tong_chi_phi_nap:,.0f} đ")
        with col2:
            st.metric("Tổng chi phí KHAY", f"{tong_chi_phi_khay:,.0f} đ")
        with col3:
            st.metric("TỔNG CHI PHÍ", f"{tong_chi_phi_chung:,.0f} đ", delta="All-in")
        with col4:
            if khay_so_luong > 0:
                don_gia_bo = (tong_chi_phi_nap / so_luong) + (tong_chi_phi_khay / khay_so_luong)
                st.metric("Giá BỘ (Nắp+Khay)", f"{don_gia_bo:,.2f} đ")
            else:
                st.metric("Giá BỘ", "N/A")

with tab2:
    st.markdown('<div class="section-header">📋 BẢNG GIÁ GIẤY & VẬT LIỆU</div>', unsafe_allow_html=True)
    
    # Phần import file Excel
    st.markdown("### 📂 Cập nhật Bảng Giá")
    
    # Hướng dẫn format
    with st.expander("ℹ️ Hướng dẫn format file Excel"):
        st.markdown("""
        **File Excel cần có:**
        1. **Sheet name:** 'Bảng giá giấy' (hoặc Sheet1 cũng được)
        2. **Dòng 1:** Tiêu đề tổng (có thể bỏ qua)
        3. **Dòng 2:** Tên cột chính xác:
           - `Tên giấy` | `Mã giấy` | `Định lượng` | `Giá`
        4. **Từ dòng 3:** Dữ liệu giấy
        
        **Ví dụ:**
        ```
        Dòng 1:  [Bảng giá Giấy]         (tiêu đề - bỏ qua)
        Dòng 2:  Tên giấy | Mã giấy | Định lượng | Giá
        Dòng 3:           | C80     | 80         | 23.6
        Dòng 4:           | I300    | 300        | 17.4
        ```
        
        **Hỗ trợ:** .xlsx, .xls, .xlsm, .xlsb
        """)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Import file Excel mới để cập nhật bảng giá giấy",
            type=['xlsx', 'xls', 'xlsm', 'xlsb'],
            help="Hỗ trợ: .xlsx, .xls, .xlsm, .xlsb\nFile phải có sheet 'Bảng giá giấy' hoặc Sheet1 với format: Tên giấy | Mã giấy | Định lượng | Giá"
        )
    
    with col2:
        if uploaded_file is not None:
            st.info(f"📁 File: {uploaded_file.name} ({uploaded_file.size:,} bytes)")
            if st.button("🔄 Cập nhật Bảng Giá", type="primary"):
                with st.spinner("⏳ Đang đọc file..."):
                    new_bang_gia = load_bang_gia_from_uploaded_file(uploaded_file)
                    if new_bang_gia is not None and not new_bang_gia.empty:
                        st.session_state.bang_gia_giay = new_bang_gia
                        bang_gia_giay = st.session_state.bang_gia_giay
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Không thể cập nhật bảng giá!")
        
        if st.button("↩️ Reset về mặc định"):
            st.session_state.bang_gia_giay = load_bang_gia_giay()
            bang_gia_giay = st.session_state.bang_gia_giay
            st.info("Đã reset về bảng giá mặc định")
            st.rerun()
    
    # Hiển thị thông tin bảng giá hiện tại
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Tổng số loại giấy", len(bang_gia_giay))
    with col2:
        min_price = bang_gia_giay['Giá'].min()
        st.metric("💵 Giá thấp nhất", f"{min_price:,.0f} VNĐ")
    with col3:
        max_price = bang_gia_giay['Giá'].max()
        st.metric("💰 Giá cao nhất", f"{max_price:,.0f} VNĐ")
    
    st.markdown("---")
    
    # Hiển thị bảng giá
    st.markdown("### 📋 Danh sách Giá Giấy")
    df_display = bang_gia_giay.copy()
    
    # Đổi tên cột hiển thị với đơn vị
    df_display = df_display.rename(columns={
        'Tên giấy': 'Tên giấy',
        'Mã giấy': 'Mã giấy',
        'Định lượng': 'Định lượng (g/m²)',
        'Giá': 'Giá (VNĐ)'
    })
    
    # Format số tiền
    df_display['Giá (VNĐ)'] = df_display['Giá (VNĐ)'].apply(lambda x: f"{x:,.2f}")
    
    st.dataframe(df_display, use_container_width=True, height=600)
    
    # Tìm kiếm giấy
    st.markdown("---")
    st.markdown("### 🔍 Tra cứu giá giấy")
    col1, col2 = st.columns(2)
    with col1:
        ma_giay_tim = st.selectbox("Chọn mã giấy", options=bang_gia_giay['Mã giấy'].unique())
    with col2:
        if ma_giay_tim:
            gia_tim = bang_gia_giay[bang_gia_giay['Mã giấy'] == ma_giay_tim]['Giá'].values[0]
            dinh_luong_tim = bang_gia_giay[bang_gia_giay['Mã giấy'] == ma_giay_tim]['Định lượng'].values[0]
            st.success(f"**Giá:** {gia_tim:,.2f} VNĐ | **Định lượng:** {dinh_luong_tim} g/m²")

with tab3:
    st.markdown('<div class="section-header">📖 HƯỚNG DẪN SỬ DỤNG</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Chức năng chính
    
    Ứng dụng này giúp bạn tính giá thành cho **Hộp Sóng - Nắp Cài Pizza** với đầy đủ các tham số:
    
    #### 📦 Tính giá NẮP:
    - Nhập kích thước: Dài, Rộng, Cao, Thành, Tai cài, Bù, Nới xén
    - Chọn chất liệu giấy từ bảng giá
    - Chọn loại cán (Mờ/Bóng/Không)
    - Nhập số bát/tờ in (1x1, 1x2, 2x2, ...)
    - Chọn loại bồi (Sóng E Nâu, Sóng B Nâu, ...)
    - Nhập thông số in: Máy in, Số màu, Nội dung
    - Các gia công đặc biệt: Ép nhũ, Thúc nổi, In offset UV, Lăn vân, Metalize
    
    #### 🍕 Tính giá KHAY ĐỊNH HÌNH:
    - Nhập số lượng khay (để trống = 0 nếu không cần)
    - Nhập kích thước khay
    - Chọn chất liệu và thông số tương tự như Nắp
    - Thêm thông số: Thùng Cao Su, Bù hao khay
    
    #### 💰 Tính toán giá thành:
    - Hệ thống tự động tính:
        - Diện tích xả lô
        - Số tờ cần in
        - Chi phí giấy, in, cán, bồi
        - Chi phí gia công
        - Đơn giá từng loại
        - Tổng chi phí
    
    ### 📊 Bảng giá giấy
    - Xem danh sách đầy đủ các loại giấy
    - Tra cứu giá theo mã giấy
    - Hiển thị định lượng và giá
    
    ### ⚙️ Công thức tính toán
    
    **Xả lô Nắp:**
    - Dài xả lô = Dài + Rộng + (Thành × 2) + Tai cài + Bù
    - Rộng xả lô = Rộng + Cao + (Thành × 2) + Nới xén
    
    **Xả lô Khay:**
    - Dài xả lô = Dài + Bù xén
    - Rộng xả lô = Rộng + Cao + Bù xén
    
    **Chi phí:**
    - Chi phí giấy = Diện tích × Số tờ × (1 + Bù hao%) × Giá giấy
    - Chi phí in = Giá pha × (Số màu / 2) + Chi phí lượt
    - Chi phí cán = Diện tích × Giá cán × Máy in
    - Chi phí bồi = Diện tích × (Giá giấy bồi + Giá gia công bồi)
    
    ### 💡 Lưu ý
    - Tất cả giá trị được tính bằng VNĐ
    - Kích thước tính bằng cm
    - Bù hao được nhập theo % (ví dụ: 400 = 400%)
    - Số màu in: 2 màu = 1 pha
    - Đơn giá là giá thành trên 1 cái sản phẩm
    
    ### 📞 Hỗ trợ
    Nếu có thắc mắc về cách tính hoặc các tham số, vui lòng liên hệ bộ phận kinh doanh.
    """)
    
    st.markdown("---")
    st.info("💾 **Mẹo:** Bạn có thể điều chỉnh các tham số và bấm 'TÍNH GIÁ' nhiều lần để so sánh các phương án khác nhau!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Hệ thống Tính Giá Bao Bì - Hộp Sóng | © 2024</p>
    <p>Phát triển bởi: Trần Công Nhật</p>
</div>
""", unsafe_allow_html=True)
