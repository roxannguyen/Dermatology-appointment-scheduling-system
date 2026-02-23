import streamlit as st
import calendar
from datetime import date
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Skin Clinic AI - Đặt lịch hẹn",
    page_icon="💎",
    layout="centered"
)

# --- Session State ---
if "selected_date" not in st.session_state:
    st.session_state.selected_date = date.today().isoformat()
if "selected_time" not in st.session_state:
    st.session_state.selected_time = None
if "cal_year" not in st.session_state:
    st.session_state.cal_year = date.today().year
if "cal_month" not in st.session_state:
    st.session_state.cal_month = date.today().month
if "booked" not in st.session_state:
    st.session_state.booked = False

# ============ XỬ LÝ URL PARAMS TRƯỚC TIÊN ============
# KHÔNG dùng st.rerun() ở đây để tránh Streamlit bị reset session_state
# khi trang vừa mới tải lại qua URL (nguyên nhân gây mất màu xanh và kẹt ngày).
if "pick_date" in st.query_params:
    st.session_state.selected_date = st.query_params["pick_date"]
    del st.query_params["pick_date"]

if "pick_month" in st.query_params:
    direction = st.query_params["pick_month"]
    m, y = st.session_state.cal_month, st.session_state.cal_year
    if direction == "prev":
        m -= 1
        if m < 1: m, y = 12, y - 1
    else:
        m += 1
        if m > 12: m, y = 1, y + 1
    st.session_state.cal_month, st.session_state.cal_year = m, y
    del st.query_params["pick_month"]

if "pick_time" in st.query_params:
    st.session_state.selected_time = st.query_params["pick_time"]
    del st.query_params["pick_time"]

# --- GLOBAL CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], * {
    font-family: 'Be Vietnam Pro', sans-serif !important;
}

/* Hide ALL streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #eef2f7 !important;
}

/* Biến container mặc định thành cái card trắng (Sửa lỗi label/box thừa) */
.block-container {
    background: white !important;
    border-radius: 18px !important;
    padding: 2.2rem 2.5rem 2rem !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.07) !important;
    max-width: 680px !important;
    margin: 2rem auto !important;
}

/* TOP NAV */
.top-nav {
    display: flex; align-items: center; justify-content: center;
    position: relative; margin-bottom: 1rem;
}
.back-btn { position: absolute; left: 0; color: #4a90e2; font-size: 0.88rem; font-weight: 600; cursor: pointer; }
.logo { display: flex; align-items: center; gap: 7px; font-weight: 700; font-size: 1rem; color: #1a1a2e; }
.logo-icon {
    width: 26px; height: 26px;
    background: linear-gradient(135deg, #4a90e2, #357abd);
    border-radius: 7px; display: inline-flex; align-items: center;
    justify-content: center; color: white; font-size: 13px;
}

/* TITLE */
.page-title { text-align: center; font-size: 1.75rem; font-weight: 800; color: #1a1a2e; margin-bottom: 0.2rem; }
.page-subtitle { text-align: center; font-size: 0.83rem; color: #7a8898; margin-bottom: 1.2rem; }

/* SECTION LABEL */
.section-label {
    font-size: 0.88rem; font-weight: 600; color: #1a1a2e !important;
    margin-bottom: 0.4rem; margin-top: 1rem; display: block;
}

/* TEXT INPUTS */
.stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 1.5px solid #e2e8f0 !important;
    padding: 10px 12px !important;
    font-size: 0.86rem !important;
    color: #1a1a2e !important;
    background: #fafbfc !important;
    box-shadow: none !important;
}
.stTextInput > div > div > input:focus {
    border-color: #4a90e2 !important;
    box-shadow: 0 0 0 3px rgba(74,144,226,0.12) !important;
}
.stTextInput label {
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: #1a1a2e !important;
}
div[data-baseweb="base-input"] { background: transparent !important; border: none !important; }

/* NÚT BUTTON STREAMLIT (Căn giữa & Màu xanh) */
[data-testid="stButton"] {
    display: flex;
    justify-content: center;
    margin-top: 1.5rem;
}
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #4a90e2, #357abd) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    height: 48px !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    width: 280px !important;
    box-shadow: 0 4px 14px rgba(74,144,226,0.35) !important;
    transition: all 0.15s !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(74,144,226,0.4) !important;
    color: white !important;
}
[data-testid="stButton"] > button p { color: white !important; }

/* DATE CHOSEN & TIME CHOSEN */
.date-chosen { text-align: center; font-size: 0.8rem; color: #4a90e2; font-weight: 600; margin: 4px 0 0; }
.time-slots-label { text-align: center; font-size: 0.8rem; color: #4a90e2; font-weight: 600; margin: 6px 0 4px; }

.confirm-note { text-align: center; font-size: 0.75rem; color: #94a3b8; margin-top: 0.8rem; }
.confirm-note a { color: #4a90e2; text-decoration: none; font-weight: 500;}

.success-box {
    background: linear-gradient(135deg, #d1fae5, #a7f3d0);
    border-radius: 14px; padding: 1.5rem; text-align: center;
    border: 1.5px solid #6ee7b7;
}
.success-box h3 { color: #065f46; font-weight: 800; font-size: 1.15rem; margin-bottom: 0.35rem; }
.success-box p { color: #047857; font-size: 0.86rem; margin: 0; }
</style>
""", unsafe_allow_html=True)


# ============ CALENDAR HTML (Tích hợp chặn ngày/tháng quá khứ) ============
def build_calendar(year, month, selected_iso):
    today_date = date.today()
    today_iso = today_date.isoformat()
    month_vn = ["Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6",
                "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"]

    first_wd, num_days = calendar.monthrange(year, month)
    if month == 1:
        py, pm = year - 1, 12
    else:
        py, pm = year, month - 1
    _, prev_num = calendar.monthrange(py, pm)
    if month == 12:
        ny, nm = year + 1, 1
    else:
        ny, nm = year, month + 1

    cells = []
    for i in range(first_wd):
        cells.append(("other", date(py, pm, prev_num - first_wd + 1 + i)))
    for d in range(1, num_days + 1):
        cells.append(("cur", date(year, month, d)))
    rem = (7 - len(cells) % 7) % 7
    for i in range(1, rem + 1):
        cells.append(("other", date(ny, nm, i)))

    rows = [cells[i:i + 7] for i in range(0, len(cells), 7)]

    rows_html = ""
    for row in rows:
        rows_html += "<tr>"
        for kind, d_obj in row:
            iso = d_obj.isoformat()
            if kind == "other":
                rows_html += f'<td><span class="day other">{d_obj.day}</span></td>'
            else:
                cls = "day"
                # CHẶN CHỌN NGÀY TRONG QUÁ KHỨ
                if d_obj < today_date:
                    cls += " past"
                    rows_html += f'<td><span class="{cls}">{d_obj.day}</span></td>'
                else:
                    if iso == selected_iso:
                        cls += " selected"
                    elif iso == today_iso:
                        cls += " today"
                    rows_html += f'<td><span class="{cls}" onclick="pickDate(\'{iso}\', this)">{d_obj.day}</span></td>'
        rows_html += "</tr>"

    # KIỂM TRA ĐỂ CHẶN NÚT PREV (LÙI THÁNG) NẾU LÀ THÁNG HIỆN TẠI
    is_current_month = (year == today_date.year and month == today_date.month)
    prev_disabled = "disabled" if is_current_month else ""

    return f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Be Vietnam Pro',sans-serif; background:transparent; }}
.cal-box {{ border: 1.5px solid #e2e8f0; border-radius: 14px; background: #fafbfc; width: 100%; }}
.cal-head {{ display: flex; align-items: center; justify-content: space-between; padding: 11px 16px; background: white; border-bottom: 1px solid #f0f2f5; border-radius: 14px 14px 0 0;}}
.cal-title {{ font-weight: 700; font-size: 0.95rem; color: #1a1a2e; }}
.nav-btn {{ background: white; border: 1.5px solid #e2e8f0; border-radius: 8px; width: 30px; height: 30px; cursor: pointer; font-size: 1.2rem; color: #4a90e2; font-weight: 700; display: inline-flex; align-items: center; justify-content: center; transition: all 0.15s; line-height: 1; padding: 0 0 2px 0; }}
.nav-btn:hover:not(:disabled) {{ background: #e8f0fe; border-color: #4a90e2; }}
.nav-btn:disabled {{ opacity: 0.3; cursor: not-allowed; }}
.cal-body {{ padding: 8px 14px 12px; }}
table {{ width: 100%; border-collapse: collapse; }}
th {{ text-align: center; font-size: 0.75rem; font-weight: 600; color: #94a3b8; padding: 6px 0 8px; }}
td {{ text-align: center; padding: 3px 0; }}
.day {{ display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; font-size: 0.85rem; font-weight: 500; color: #1a1a2e; cursor: pointer; transition: all 0.12s; user-select: none; }}
.day:hover:not(.past):not(.other) {{ background: #e8f0fe; color: #4a90e2; }}
.day.selected {{ background: #4a90e2 !important; color: white !important; font-weight: 700; box-shadow: 0 2px 8px rgba(74,144,226,0.4); }}
.day.today {{ border: 2px solid #4a90e2; color: #4a90e2; font-weight: 600; }}
.day.other {{ color: #cbd5e1; cursor: default; font-size: 0.8rem; pointer-events: none; }}
.day.past {{ color: #cbd5e1; cursor: not-allowed; text-decoration: line-through; }}
</style>
</head><body>
<div class="cal-box">
  <div class="cal-head">
    <button class="nav-btn" id="prevBtn" onclick="navigateMonth('prev')" {prev_disabled}>&#8249;</button>
    <span class="cal-title">{month_vn[month - 1]} {year}</span>
    <button class="nav-btn" id="nextBtn" onclick="navigateMonth('next')">&#8250;</button>
  </div>
  <div class="cal-body">
    <table>
      <thead><tr><th>T2</th><th>T3</th><th>T4</th><th>T5</th><th>T6</th><th>T7</th><th>CN</th></tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
  </div>
</div>
<script>
function pickDate(iso, element) {{
    // Phản hồi UI tức thì khi click
    document.querySelectorAll('.day').forEach(d => d.classList.remove('selected'));
    element.classList.add('selected');

    // Đẩy dữ liệu lên URL
    let url = new URL(window.parent.location.href);
    url.searchParams.set('pick_date', iso);
    window.parent.location.href = url.toString();
}}
function navigateMonth(dir) {{
    if (dir === 'prev' && document.getElementById('prevBtn').disabled) return;
    let url = new URL(window.parent.location.href);
    url.searchParams.set('pick_month', dir);
    window.parent.location.href = url.toString();
}}
</script>
</body></html>"""


# ============ TIME SLOTS HTML ============
def build_timeslots(slots, selected_time):
    sel = selected_time or ""
    btns = ""
    for t in slots:
        cls = "time-btn selected" if t == sel else "time-btn"
        btns += f'<button class="{cls}" onclick="pickTime(\'{t}\', this)">{t}</button>\n'

    return f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Be Vietnam Pro',sans-serif; background:transparent; }}
.grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; width: 100%; }}
.time-btn {{ background: white; border: 1.5px solid #dde3ec; border-radius: 10px; padding: 11px 0; font-size: 0.9rem; font-weight: 500; color: #374151; cursor: pointer; transition: all 0.15s; text-align: center; width: 100%; }}
.time-btn:hover {{ border-color: #4a90e2; color: #4a90e2; background: #f0f7ff; }}
.time-btn.selected {{ background: #4a90e2 !important; color: white !important; border-color: #4a90e2 !important; font-weight: 700; box-shadow: 0 2px 8px rgba(74,144,226,0.35); }}
</style>
</head><body>
<div class="grid">{btns}</div>
<script>
function pickTime(t, element) {{
    // Phản hồi UI tức thì khi click
    document.querySelectorAll('.time-btn').forEach(btn => btn.classList.remove('selected'));
    element.classList.add('selected');

    // Đẩy dữ liệu lên URL
    let url = new URL(window.parent.location.href);
    url.searchParams.set('pick_time', encodeURIComponent(t));
    window.parent.location.href = url.toString();
}}
</script>
</body></html>"""


# ============ RENDER UI GIAO DIỆN CHÍNH ============
st.markdown("""
<div class="top-nav">
  <span class="back-btn">← Quay lại</span>
  <div class="logo"><div class="logo-icon">◆</div> Skin Clinic AI</div>
</div>
<div class="page-title">Đặt Lịch Hẹn Tư vấn</div>
<div class="page-subtitle">Vui lòng để lại thông tin, đội ngũ bác sĩ sẽ liên hệ xác nhận lịch hẹn của bạn trong 15 phút.</div>
""", unsafe_allow_html=True)

if st.session_state.booked:
    name = st.session_state.get("name_val", "")
    d_obj = date.fromisoformat(st.session_state.selected_date)
    st.markdown(f"""
    <div class="success-box">
      <h3>✅ Đặt lịch thành công!</h3>
      <p>Xin chào <strong>{name}</strong>, lịch hẹn lúc <strong>{st.session_state.selected_time}</strong>
      ngày <strong>{d_obj.strftime('%d/%m/%Y')}</strong> đã được ghi nhận.<br>
      Bác sĩ sẽ liên hệ xác nhận trong 15 phút.</p>
    </div><br>
    """, unsafe_allow_html=True)

    if st.button("Đặt lịch mới"):
        st.session_state.booked = False
        st.session_state.selected_time = None
        st.rerun()

else:
    # --- Thông tin ---
    c1, c2, c3 = st.columns(3)
    with c1:
        name = st.text_input("Họ và tên", placeholder="Nguyễn Văn A", key="nm")
    with c2:
        phone = st.text_input("Số điện thoại", placeholder="090xxx...", key="ph")
    with c3:
        email = st.text_input("Email", placeholder="vidu@email.com", key="em")

    # --- Lịch hẹn ---
    st.markdown('<span class="section-label">Chọn ngày hẹn</span>', unsafe_allow_html=True)
    cal_html = build_calendar(
        st.session_state.cal_year,
        st.session_state.cal_month,
        st.session_state.selected_date
    )
    components.html(cal_html, height=295, scrolling=False)

    if st.session_state.selected_date:
        d_obj = date.fromisoformat(st.session_state.selected_date)
        st.markdown(f"<div class='date-chosen'>📅 Đã chọn: {d_obj.strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)

    # --- Khung giờ ---
    st.markdown('<span class="section-label">Chọn khung giờ</span>', unsafe_allow_html=True)
    slots = ["08:00", "09:30", "11:00", "14:00", "15:30", "17:00", "18:30", "20:00"]
    time_html = build_timeslots(slots, st.session_state.selected_time)
    components.html(time_html, height=115, scrolling=False)

    # Text hiển thị giờ đã chọn cập nhật tức thì
    if st.session_state.selected_time:
        st.markdown(f"<div class='time-slots-label'>⏰ Đã chọn: {st.session_state.selected_time}</div>",
                    unsafe_allow_html=True)
    else:
        st.markdown("<div class='time-slots-label' style='color:#94a3b8;'>⏰ Chưa chọn khung giờ</div>",
                    unsafe_allow_html=True)

    # --- Button Xác nhận ---
    if st.button("Xác nhận đặt lịch", key="confirm"):
        if not name or not phone or not email:
            st.error("⚠️ Vui lòng điền đầy đủ thông tin!")
        elif not st.session_state.selected_time:
            st.error("⚠️ Vui lòng chọn khung giờ!")
        elif st.session_state.selected_date < date.today().isoformat():
            st.error("⚠️ Không thể chọn ngày trong quá khứ!")
        else:
            st.session_state.booked = True
            st.session_state.name_val = name
            st.rerun()

    st.markdown("""
    <div class="confirm-note">
      Bằng cách nhấn xác nhận, bạn đồng ý với các
      <a href="#">Điều khoản &amp; Chính sách bảo mật</a> của Skin Clinic.
    </div>
    """, unsafe_allow_html=True)