import streamlit as st
import time
import re
from PIL import Image

# ==========================================
# 1. CẤU HÌNH & KHỞI TẠO STATE
# ==========================================
st.set_page_config(
    page_title="Chẩn đoán Da mụn qua Ảnh",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Khởi tạo Session State
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "show_result" not in st.session_state:
    st.session_state.show_result = False

# Hàm Helper
def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email.strip()) is not None

# ==========================================
# 2. KHAI BÁO CSS CHUYÊN SÂU
# ==========================================
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stHeader"] {display: none !important;}
    html, body, [class*="css"], .stApp { font-family: 'Be Vietnam Pro', sans-serif !important; background-color: #f8f9fa !important; }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 1050px !important; margin: 0 auto !important; }

    /* Buttons */
    .stButton > button { background-color: #4a90e2 !important; color: white !important; border: none !important; border-radius: 12px !important; font-size: 1.1rem !important; font-weight: 700 !important; height: 56px !important; padding: 10px 24px !important; width: 100% !important; transition: all 0.3s ease !important; box-shadow: 0 4px 14px rgba(74,144,226,0.3) !important; }
    .stButton > button:hover { background-color: #357abd !important; transform: translateY(-2px); }

    /* Upload Zone */
    [data-testid="stFileUploadDropzone"] { background-color: white !important; border: 2px dashed #e0e0e0 !important; border-radius: 16px !important; padding: 50px !important; }
    [data-testid="stFileUploadDropzone"] * { font-size: 1.1rem !important; }

    /* Inputs */
    .stTextInput input { border-radius: 10px !important; border: 1.5px solid #e0e0e0 !important; padding: 14px 18px !important; font-size: 1rem !important; }
    .stTextInput input:focus { border-color: #4a90e2 !important; box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2) !important; }

    /* Buttons Hỗ trợ ở cuối */
    div[data-testid="stVerticalBlock"] > div:last-child div.stButton > button { background-color: white !important; color: #666 !important; border: 2px solid #dde3ec !important; border-radius: 12px !important; box-shadow: none !important; font-size: 1.05rem !important; font-weight: 600 !important; height: 54px !important; transition: all 0.3s ease !important; }
    div[data-testid="stVerticalBlock"] > div:last-child div.stButton > button:hover,
    div[data-testid="stVerticalBlock"] > div:last-child div.stButton > button:active { background-color: #4a90e2 !important; color: white !important; border-color: #4a90e2 !important; transform: translateY(-2px); }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==========================================
# 3. RENDER UI - HEADER & HƯỚNG DẪN
# ==========================================
# Top Navigation
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
    <a href="/" style="color: #7a8898; font-size: 16px; font-weight: 600; text-decoration: none; cursor: pointer;">← Quay lại</a>
    <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 16px; color: #4a90e2;">
        <div style="width: 24px; height: 24px; background: #4a90e2; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px;">◆</div> 
        Skin Clinic AI
    </div>
</div>
<div style="text-align: center; margin-top: 20px; margin-bottom: 45px;">
    <h1 style="font-size: 38px; font-weight: 800; color: #1a1a2e; margin-bottom: 12px;">Chẩn đoán Da mụn qua Ảnh</h1>
    <p style="font-size: 16px; color: #7a8898; max-width: 700px; margin: 0 auto; line-height: 1.6;">
        Sử dụng trí tuệ nhân tạo để phân tích tình trạng da của bạn trong tích tắc. Thông tin của bạn được bảo mật tuyệt đối.
    </p>
</div>
""", unsafe_allow_html=True)

# Hướng dẫn chụp
st.markdown("""
<div style="margin-bottom: 16px; font-weight: 700; color: #4a90e2; font-size: 18px; display: flex; align-items: center; gap: 8px;">
    <span style="font-size: 22px;"></span> Hướng dẫn chụp ảnh
</div>
<div style="display: flex; gap: 20px; margin-bottom: 35px;">
    <div style="flex: 1; background: white; border: 1px solid #eef2f7; border-radius: 16px; padding: 18px; display: flex; align-items: center; gap: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.02);">
        <div style="width: 32px; height: 32px; border-radius: 50%; background: #4a90e2; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; flex-shrink: 0;">1</div>
        <div style="font-size: 14px; font-weight: 500; color: #1a1a2e; line-height: 1.5;">Chụp trực diện vùng da cần chẩn đoán</div>
    </div>
    <div style="flex: 1; background: white; border: 1px solid #eef2f7; border-radius: 16px; padding: 18px; display: flex; align-items: center; gap: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.02);">
        <div style="width: 32px; height: 32px; border-radius: 50%; background: #4a90e2; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; flex-shrink: 0;">2</div>
        <div style="font-size: 14px; font-weight: 500; color: #1a1a2e; line-height: 1.5;">Đảm bảo đủ ánh sáng tự nhiên</div>
    </div>
    <div style="flex: 1; background: white; border: 1px solid #eef2f7; border-radius: 16px; padding: 18px; display: flex; align-items: center; gap: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.02);">
        <div style="width: 32px; height: 32px; border-radius: 50%; background: #4a90e2; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; flex-shrink: 0;">3</div>
        <div style="font-size: 14px; font-weight: 500; color: #1a1a2e; line-height: 1.5;">Không sử dụng các loại kính lọc (filter)</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. RENDER UI - UPLOAD & CHẨN ĐOÁN
# ==========================================
uploaded_file = st.file_uploader("Tải ảnh lên", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        image = Image.open(uploaded_file)
        st.image(image, caption="Ảnh đã tải lên", use_container_width=True)

st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
if st.button("Bắt đầu chẩn đoán", key="btn_analyze", use_container_width=True):
    if st.session_state.uploaded_file is None:
        st.warning("Vui lòng tải lên một ảnh để bắt đầu chẩn đoán.")
        st.session_state.show_result = False
    else:
        with st.spinner("Hệ thống đang phân tích hình ảnh..."):
            time.sleep(2)
        st.session_state.show_result = True

# ==========================================
# 5. RENDER UI - KẾT QUẢ & FORM EMAIL
# ==========================================
if st.session_state.show_result:
    st.markdown("""
    <div style="background: white; border-radius: 16px; border: 1px solid #eef2f7; border-left: 6px solid #4a90e2; padding: 32px; margin-top: 32px; box-shadow: 0 4px 16px rgba(0,0,0,0.04);">
        <div style="font-weight: 800; color: #1a1a2e; font-size: 20px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">Kết quả chẩn đoán sơ bộ</div>
        <div style="background: #f8f9fa; border: 1px solid #eef2f7; border-radius: 12px; padding: 20px; font-size: 16px; color: #333; line-height: 1.7; margin-bottom: 20px;">
            Dựa trên phân tích hình ảnh, hệ thống phát hiện các dấu hiệu của <strong>Mụn trứng cá (Acne Vulgaris)</strong> mức độ trung bình. Khuyên bạn nên giữ vệ sinh da mặt và tránh tự ý nặn mụn.
        </div>
        <div style="background: #f0f7ff; border-radius: 12px; padding: 20px; margin-bottom: 28px;">
            <div style="font-weight: 800; color: #4a90e2; font-size: 14px; text-transform: uppercase; margin-bottom: 16px; display: flex; align-items: center; gap: 10px;">PHÁC ĐỒ ĐIỀU TRỊ GỢI Ý</div>
            <ul style="margin: 0; padding-left: 24px; font-size: 15px; color: #4a5568; line-height: 2.0;">
                <li>Sử dụng sữa rửa mặt dịu nhẹ 2 lần/ngày.</li>
                <li>Thoa kem trị mụn chứa Benzoyl Peroxide vào buổi tối.</li>
                <li>Luôn sử dụng kem chống nắng khi ra ngoài.</li>
                <li>Hạn chế ăn đồ cay nóng và thức khuya.</li>
            </ul>
        </div>
        <hr style="border: none; border-top: 1.5px solid #eef2f7; margin-bottom: 24px;">
        <div style="font-weight: 700; color: #1a1a2e; font-size: 16px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">Nhận báo cáo chi tiết</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    col_em1, col_em2 = st.columns([2.5, 1])
    with col_em1:
        email_input = st.text_input("Email", label_visibility="collapsed", placeholder="Email của bạn...", key="email_input")
    with col_em2:
        submit = st.button("➤ Gửi kết quả qua email", use_container_width=True)

    st.markdown("""
        <div style="font-size: 13px; color: #94a3b8; font-style: italic; margin-top: 12px; margin-bottom: 35px;">
            Lưu ý: Đây chỉ là kết quả phân tích AI ban đầu, không thay thế chẩn đoán của bác sĩ chuyên khoa.
        </div>
    """, unsafe_allow_html=True)

    # Xử lý Logic Gửi Email
    if submit:
        email_clean = email_input.strip()
        if not email_clean:
            st.warning("Vui lòng nhập email của bạn trước khi gửi!")
        elif not is_valid_email(email_clean):
            st.error("Email chưa đúng định dạng. Ví dụ hợp lệ: vidu@gmail.com")
        else:
            st.success(f"Đã gửi kết quả chi tiết về email: {email_clean}")

# ==========================================
# 6. RENDER UI - ĐẶT LỊCH HẸN KHUYÊN DÙNG
# ==========================================
st.markdown("""
<div style="background: white; border-radius: 16px; overflow: hidden; border: 1px solid #eef2f7; box-shadow: 0 4px 16px rgba(0,0,0,0.04); margin-top: 32px;">
    <div style="background: #4a90e2; padding: 18px 24px; color: white; font-weight: 700; font-size: 18px; display: flex; align-items: center; gap: 10px;">Hỗ trợ Da liễu</div>
    <div style="padding: 28px;">
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; font-size: 16px; color: #1a1a2e; font-weight: 500; margin-bottom: 24px; text-align: center; line-height: 1.6;">
            Bạn có muốn đặt lịch tư vấn trực tiếp với bác sĩ để nhận phác đồ điều trị chi tiết không?
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='margin-top: -75px; padding: 0 28px 28px 28px; position: relative; z-index: 10;'>", unsafe_allow_html=True)
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("Đặt lịch ngay", key="btn_book_now", use_container_width=True):
        st.switch_page("pages/2_Booking.py")
with col_btn2:
    if st.button("Để sau", key="btn_later", use_container_width=True):
        st.switch_page("app.py")
st.markdown("</div><div style='height: 40px;'></div>", unsafe_allow_html=True)
