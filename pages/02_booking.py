import streamlit as st
import calendar
from datetime import date, datetime

# ==========================================
# 1. CẤU HÌNH & KHỞI TẠO STATE
# ==========================================
st.set_page_config(
    page_title="Skin Clinic AI - Đặt lịch hẹn",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Khởi tạo Session State
if "selected_date" not in st.session_state: st.session_state.selected_date = date.today().isoformat()
if "selected_time" not in st.session_state: st.session_state.selected_time = None
if "cal_year" not in st.session_state: st.session_state.cal_year = date.today().year
if "cal_month" not in st.session_state: st.session_state.cal_month = date.today().month
if "booked" not in st.session_state: st.session_state.booked = False
if "name_val" not in st.session_state: st.session_state.name_val = ""
if "form_data" not in st.session_state: st.session_state.form_data = {"name": "", "phone": "", "email": ""}

# Xử lý URL params (Dữ liệu gửi từ trang khác qua URL)
if "pick_date" in st.query_params:
    st.session_state.selected_date = st.query_params["pick_date"]
    try: del st.query_params["pick_date"]
    except: pass

if "pick_month" in st.query_params:
    direction = st.query_params["pick_month"]
    m, y = st.session_state.cal_month, st.session_state.cal_year
    if direction == "prev":
        m = 12 if m == 1 else m - 1
        y = y - 1 if m == 12 else y
    else:
        m = 1 if m == 12 else m + 1
        y = y + 1 if m == 1 else y
    st.session_state.cal_month, st.session_state.cal_year = m, y
    try: del st.query_params["pick_month"]
    except: pass

if "pick_time" in st.query_params:
    st.session_state.selected_time = st.query_params["pick_time"]
    try: del st.query_params["pick_time"]
    except: pass

# ==========================================
# 2. KHAI BÁO CSS CHUYÊN SÂU
# ==========================================
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"], * { font-family: 'Be Vietnam Pro', sans-serif !important; }

    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stDecoration"], [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: #eef2f7 !important; }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 3rem !important; max-width: 1050px !important; margin: 0 auto !important; }

    /* Typography */
    .page-title { text-align: center; font-size: 2.2rem; font-weight: 800; color: #1a1a2e; margin-bottom: 0.4rem; }
    .page-subtitle { text-align: center; font-size: 1.05rem; color: #7a8898; margin-bottom: 2rem; }
    .section-label { font-size: 1.05rem !important; font-weight: 700 !important; color: #000000 !important; margin-bottom: 0.6rem; margin-top: 1.5rem; display: block; }
    .date-chosen, .time-slots-label { text-align: center; font-size: 1rem; color: #4a90e2; font-weight: 600; margin: 8px 0 0; }
    .confirm-note { text-align: center; font-size: 0.9rem; color: #94a3b8; margin-top: 1.2rem; }
    .confirm-note a { color: #4a90e2; text-decoration: none; font-weight: 500;}

    /* Success Box */
    .success-box { background: linear-gradient(135deg, #d1fae5, #a7f3d0); border-radius: 16px; padding: 2rem; text-align: center; border: 1.5px solid #6ee7b7; margin-bottom: 2rem; }
    .success-box h3 { color: #065f46; font-weight: 800; font-size: 1.4rem; margin-bottom: 0.5rem; }
    .success-box p { color: #047857; font-size: 1rem; margin: 0; line-height: 1.6;}

    /* Text Inputs */
    div[data-testid="stTextInput"] label p { font-size: 1.05rem !important; font-weight: 700 !important; color: #000000 !important; }
    div[data-testid="stTextInput"] div[data-baseweb="input"] { border-radius: 10px !important; border: 1.5px solid #e2e8f0 !important; background-color: #ffffff !important; padding: 0px !important; overflow: hidden !important; }
    div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within { border-color: #4a90e2 !important; box-shadow: 0 0 0 2px rgba(74,144,226,0.15) !important; }
    div[data-testid="stTextInput"] input { color: #1a1a2e !important; font-size: 1rem !important; padding: 12px 14px !important; background: transparent !important; border: none !important; outline: none !important; box-shadow: none !important; }
    div[data-testid="stTextInput"] input::placeholder { color: #94a3b8 !important; -webkit-text-fill-color: #94a3b8 !important; opacity: 1 !important; font-weight: 400 !important; }
    div[data-testid="stTextInput"] div[data-baseweb="base-input"] { background: transparent !important; border: none !important; }

    /* Date Input */
    div[data-testid="stDateInput"] label { display: none !important; }
    div[data-testid="stDateInput"] div[data-baseweb="input"] { border-radius: 10px !important; border: 1.5px solid #e2e8f0 !important; background: #ffffff !important; padding: 8px 16px !important; cursor: pointer !important; }
    div[data-testid="stDateInput"] div[data-baseweb="input"]:focus-within { border-color: #4a90e2 !important; box-shadow: 0 0 0 2px rgba(74,144,226,0.15) !important; }
    div[data-testid="stDateInput"] input { font-family: 'Be Vietnam Pro', sans-serif !important; font-size: 1rem !important; color: #1a1a2e !important; font-weight: 600 !important; }

    /* Buttons Override (Khóa nhấc lún) */
    [data-testid="stButton"] { display: flex; justify-content: center; }
    [data-testid="stButton"] button { transform: translateY(0px) scale(1) !important; transition: background-color 0.2s, border-color 0.2s, box-shadow 0.2s, color 0.2s !important; }
    [data-testid="stButton"] button:active, [data-testid="stButton"] button:focus:active { transform: translateY(0px) scale(1) !important; outline: none !important; }

    /* Button Tùy chỉnh */
    [data-testid="stButton"] button[kind="primary"]:not(.time-btn) { background: linear-gradient(135deg, #4a90e2, #357abd) !important; color: white !important; border: none !important; border-radius: 12px !important; height: 56px !important; font-size: 1.1rem !important; font-weight: 700 !important; width: 340px !important; margin: 1.5rem auto 0 !important; display: block !important; box-shadow: 0 4px 14px rgba(74,144,226,0.35) !important; }
    [data-testid="stButton"] button[kind="primary"]:not(.time-btn):hover { box-shadow: 0 6px 18px rgba(74,144,226,0.45) !important; background: linear-gradient(135deg, #357abd, #2a5f8a) !important; }
    [data-testid="stButton"] button[kind="secondary"] { background: #ffffff !important; color: #374151 !important; border: 1.5px solid #e2e8f0 !important; border-radius: 10px !important; padding: 12px 0 !important; font-weight: 500 !important; height: auto !important; font-size: 1rem !important; width: 100% !important; box-shadow: none !important; margin: 0 !important; }
    [data-testid="stButton"] button[kind="secondary"]:hover { border-color: #4a90e2 !important; color: #4a90e2 !important; background: #f0f7ff !important; transform: none !important; }
    [data-testid="column"] [data-testid="stButton"] button[kind="primary"] { background: #4a90e2 !important; color: white !important; border: 1.5px solid #4a90e2 !important; border-radius: 10px !important; padding: 12px 0 !important; font-weight: 700 !important; height: auto !important; font-size: 1rem !important; width: 100% !important; margin: 0 !important; display: flex !important; box-shadow: 0 2px 8px rgba(74,144,226,0.35) !important; }
    [data-testid="column"] [data-testid="stButton"] button[kind="primary"]:hover { background: #357abd !important; border-color: #357abd !important; transform: none !important; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==========================================
# 3. RENDER UI - HEADER
# ==========================================
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2.5rem;">
    <a href="/" style="color: #7a8898; font-size: 16px; font-weight: 600; text-decoration: none; cursor: pointer;">← Quay lại</a>
    <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 16px; color: #4a90e2;">
        <div style="width: 24px; height: 24px; background: #4a90e2; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px;">◆</div> 
        Skin Clinic AI
    </div>
</div>
<div class="page-title">Đặt Lịch Hẹn Tư vấn</div>
<div class="page-subtitle">Vui lòng để lại thông tin, đội ngũ bác sĩ sẽ liên hệ xác nhận lịch hẹn của bạn trong 15 phút.</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. RENDER UI - MAIN CONTENT
# ==========================================
# KỊCH BẢN 1: KHI ĐÃ ĐẶT LỊCH THÀNH CÔNG
if st.session_state.booked:
    name = st.session_state.get("name_val", "")
    d_obj = date.fromisoformat(st.session_state.selected_date)
    st.markdown(f"""
    <div class="success-box">
      <h3>Đặt lịch thành công!</h3>
      <p>Xin chào <strong>{name}</strong>, lịch hẹn lúc <strong>{st.session_state.selected_time}</strong>
      ngày <strong>{d_obj.strftime('%d/%m/%Y')}</strong> đã được ghi nhận.<br>
      Bác sĩ sẽ liên hệ xác nhận trong 15 phút.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Đặt lịch mới", use_container_width=True, type="primary"):
        st.session_state.booked = False
        st.session_state.selected_time = None
        st.session_state.form_data = {"name": "", "phone": "", "email": ""}
        st.rerun()

# KỊCH BẢN 2: FORM ĐẶT LỊCH
else:
    # 4.1. Form thông tin cá nhân
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.form_data["name"] = st.text_input("Họ và tên", placeholder="Nguyễn Văn A", key="nm", value=st.session_state.form_data["name"])
    with col2:
        st.session_state.form_data["phone"] = st.text_input("Số điện thoại", placeholder="090xx", key="ph", value=st.session_state.form_data["phone"])
    with col3:
        st.session_state.form_data["email"] = st.text_input("Email", placeholder="vidu@gmail.com", key="em", value=st.session_state.form_data["email"])

    # 4.2. Chọn ngày hẹn
    st.markdown('<span class="section-label">Chọn ngày hẹn</span>', unsafe_allow_html=True)
    min_date = date.today()
    selected_date_obj = st.date_input(
        "Chọn ngày",
        value=date.fromisoformat(st.session_state.selected_date) if st.session_state.selected_date else min_date,
        min_value=min_date, format="DD/MM/YYYY", label_visibility="collapsed", key="date_picker"
    )
    st.session_state.selected_date = selected_date_obj.isoformat()
    st.markdown(f"<div class='date-chosen'>Đã chọn: {selected_date_obj.strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)

    # 4.3. Chọn khung giờ
    st.markdown('<span class="section-label">Chọn khung giờ</span>', unsafe_allow_html=True)
    slots = ["08:00", "09:30", "11:00", "14:00", "15:30", "17:00", "18:30", "20:00"]
    cols = st.columns(4)
    for i, slot in enumerate(slots):
        with cols[i % 4]:
            btn_type = "primary" if slot == st.session_state.selected_time else "secondary"
            if st.button(slot, key=f"time_{slot}", use_container_width=True, type=btn_type):
                st.session_state.selected_time = None if st.session_state.selected_time == slot else slot
                st.rerun()

    if st.session_state.selected_time:
        st.markdown(f"<div class='time-slots-label'>Đã chọn: {st.session_state.selected_time}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='time-slots-label' style='color:#94a3b8;'>Chưa chọn khung giờ</div>", unsafe_allow_html=True)

    # 4.4. Nút Xác nhận đặt lịch
    if st.button("Xác nhận đặt lịch", key="confirm", use_container_width=True, type="primary"):
        if not st.session_state.form_data["name"] or not st.session_state.form_data["phone"] or not st.session_state.form_data["email"]:
            st.error("Vui lòng điền đầy đủ thông tin!")
        elif not st.session_state.selected_time:
            st.error("Vui lòng chọn khung giờ!")
        elif st.session_state.selected_date < date.today().isoformat():
            st.error("Không thể chọn ngày trong quá khứ!")
        else:
            st.session_state.booked = True
            st.session_state.name_val = st.session_state.form_data["name"]
            st.rerun()

    # Footer
    st.markdown("""
    <div class="confirm-note">
      Bằng cách nhấn xác nhận, bạn đồng ý với các <a href="#">Điều khoản &amp; Chính sách bảo mật</a> của Skin Clinic.
    </div>
    """, unsafe_allow_html=True)