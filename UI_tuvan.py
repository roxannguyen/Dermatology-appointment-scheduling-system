import streamlit as st
import streamlit.components.v1 as components
import base64
from io import BytesIO
import re

# Page config
st.set_page_config(
    page_title="Chẩn đoán Da mụn qua Ảnh",
    page_icon="🔬",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #f5f7fa;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        padding: 20px 0;
    }
    
    .main-title {
        font-size: 24px;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 10px;
    }
    
    .subtitle {
        font-size: 14px;
        color: #666;
        line-height: 1.5;
    }
    
    /* Instruction boxes */
    .instruction-box {
        background-color: #e8f4fd;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .instruction-number {
        background-color: #1e88e5;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        flex-shrink: 0;
    }
    
    .instruction-text {
        font-size: 14px;
        color: #333;
        flex: 1;
    }
    
    /* Upload area */
    .upload-area {
        background-color: white;
        border: 2px dashed #ccc;
        border-radius: 12px;
        padding: 40px 20px;
        text-align: center;
        margin: 20px 0;
    }
    
    .upload-icon {
        font-size: 48px;
        color: #999;
        margin-bottom: 10px;
    }
    
    .upload-text {
        font-size: 16px;
        font-weight: 600;
        color: #333;
        margin-bottom: 5px;
    }
    
    .upload-subtext {
        font-size: 12px;
        color: #999;
    }
    
    /* Primary button */
    .stButton > button {
        background-color: #1e88e5;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #1976d2;
    }
    

    /* Info box */
    .info-box {
        background-color: #EFF6FF;
        border-radius: 12px;
        border: 2px solid #CFE0F5;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .info-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .info-content {
        font-size: 14px;
        color: #666;
        line-height: 1.6;
        margin-bottom: 15px;
    }
    
    .info-list {
        list-style: none;
        padding-left: 0;
    }
    
    .info-list li {
        font-size: 13px;
        color: #1e88e5;
        margin: 8px 0;
        padding-left: 20px;
        position: relative;
    }
    
    .info-list li:before {
        content: "•";
        position: absolute;
        left: 5px;
        color: #1e88e5;
    }
    
    /* Email input section */
    .email-section {
    background-color: white;
    margin: 14px 0;
    }
    /* Secondary buttons */
    .secondary-btn {
        background-color: white;
        color: #1e88e5;
        border: 1px solid #1e88e5;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .secondary-btn:hover {
        background-color: #e8f4fd;
    }
    
        .step-card {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 14px;
        height: 100px;
        border: 1px solid #E0E0E0;
    }
    .step-number {
        background-color: #1A73E8;
        color: white;
        border-radius: 50%;
        width: 25px;
        height: 25px;
        display: inline-block;
        text-align: center;
        line-height: 25px;
        margin-bottom: 5px;
        font-weight: bold;
    }       
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <div class="main-title">Chẩn đoán Da mụn qua Ảnh</div>
    <div class="subtitle">Sử dụng trí tuệ nhân tạo để phân tích hình ảnh của bạn và cung cấp chẩn đoán. Thông<br>tin chỉ dùng để tham khảo dự định.</div>
</div>
""", unsafe_allow_html=True)

# Instructions
st.markdown("##### 📷 Hướng dẫn chụp ảnh")
c1, c2, c3 = st.columns(3)

# Sử dụng HTML để tạo các thẻ (Card) giống ảnh
with c1:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">1</div><br>
        Chụp trực diện vùng da cần chẩn đoán
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">2</div><br>
        Đảm bảo đủ ánh sáng tự nhiên
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">3</div><br>
        Không sử dụng các loại kính lọc (filter)
    </div>
    """, unsafe_allow_html=True)

st.write("") # Tạo khoảng cách



# File uploader (hidden, but functional)
uploaded_file = st.file_uploader("Chọn tập ảnh", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file

if "show_result" not in st.session_state:
    st.session_state.show_result = False
# Main action button
if st.button("⚡ Bắt đầu chẩn đoán", use_container_width=True):
    if uploaded_file is None:
        st.warning("⚠️ Vui lòng tải lên một ảnh để bắt đầu chẩn đoán.")
        st.session_state.show_result = False
    else:
        with st.spinner("Đang phân tích ảnh..."):
            import time
            time.sleep(2)

        st.success("✅ Phân tích hoàn tất!")
        st.session_state.show_result = True

# Info box about diagnosis
if st.session_state.show_result:
    st.markdown("""
    <div class="info-box">
        <div class="info-title">
            📋 Kết quả chẩn đoán sơ bộ
        </div>
        <div class="info-content">
            Dựa trên phân tích hình ảnh, hệ thống phát hiện các dấu hiệu về <strong>Mụn trứng cá (Acne Vulgaris)</strong> mức độ trung bình. Khuyên bạn nên giữ vệ sinh da mặt và tránh tự ý nặn mụn.
        </div>
    </div>
        <div class="info-box">
        <div class="info-title">
            📝 Phác đồ điều trị gợi ý
        </div>
        <div class="info-content">
            Dưới đây là phác đồ điều trị gợi ý cho tình trạng <strong>Mụn trứng cá (Acne Vulgaris)</strong> mức độ trung bình tại phòng khám của chúng tôi.
        </div>
    </div>
    """, unsafe_allow_html=True)

# email input section
st.markdown("""
<div class="email-section">
    <div class="info-title">
        📧 Nhận kết quả qua Email
    </div>
</div>
""", unsafe_allow_html=True)


col1, col2 = st.columns([3, 1])
with col1:
    email_input = st.text_input(
        "Email",
        label_visibility="collapsed",
        placeholder="Vui lòng nhập Email",
        key="email_input"
    )

with col2:
    submit = st.button("Nhận kết quả", use_container_width=True)

# Hàm kiểm tra email
def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

# Xử lý logic sau khi nhấn nút
if submit:
    if not email_input or not is_valid_email(email_input):
        st.warning("⚠️ Vui lòng nhập email chính xác.")
    else:
        # TODO: gọi hàm gửi email thật tại đây
        st.success("Đã gửi kết quả về email của bạn.")


st.markdown("""
<div style="font-size: 14px; color: #999; margin-top: 8px; font-style: italic; margin-bottom: 25px;">
    Lưu ý: Đây chỉ là kết quả phân tích ban đầu của AI, không thay thế chẩn đoán của bác sĩ chuyên khoa.
</div>
""", unsafe_allow_html=True)

# Help section
st.markdown("""
<div class='info-title'>
    📆 Đặt lịch hẹn
</div>
            
<div style='margin-bottom: 18px; font-size: 14px; color: #666; padding-left: 10px;'>
    Bạn có muốn đặt lịch tư vấn trực tiếp với bác sĩ để nhận phác đồ điều trị chi tiết không?
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.button("Đặt lịch ngay", use_container_width=True)
with col2:
    if st.button("Để sau", use_container_width=True):
         st.switch_page("app.py") #xử lí logic nhấn nút này thì back lại trang chủ, thay tên file giao diện trang chủ

# Footer spacing
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

