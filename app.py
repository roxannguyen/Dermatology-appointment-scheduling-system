import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. CẤU HÌNH TRANG
# ==========================================
st.set_page_config(
    page_title="Skin Clinic AI - Trang chủ",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. KHAI BÁO GIAO DIỆN (CSS & HTML)
# ==========================================
CUSTOM_CSS = """
<style>
   @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

   /* Ẩn các thành phần mặc định của Streamlit */
   #MainMenu, footer, header {visibility: hidden;}
   [data-testid="stHeader"] {display: none !important;}
   [data-testid="stButton"] {display: none !important;} /* Ẩn nút gốc của Streamlit */

   /* Nền đồng bộ với trang Booking */
   .stApp {
       background-color: #eef2f7 !important;
       font-family: 'Be Vietnam Pro', sans-serif !important;
   }
   .main .block-container {
       padding: 0 !important;
       max-width: 100% !important;
   }
</style>
"""

HOMEPAGE_HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8"/>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<style>
   body { font-family: 'Be Vietnam Pro', sans-serif; background-color: #eef2f7 !important; margin: 0; padding: 0; }
   .material-symbols-outlined { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24; }
   .glass-card { background: white; border-radius: 24px; box-shadow: 0 4px 24px rgba(0,0,0,0.06); transition: all 0.3s ease; border: 1px solid rgba(0,0,0,0.02); }
   .glass-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(74,144,226,0.12); }
   .action-button { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: linear-gradient(135deg, #4a90e2, #357abd); color: white; font-weight: 700; font-size: 0.75rem; border-radius: 9999px; box-shadow: 0 4px 10px rgba(74,144,226,0.3); transition: all 0.3s ease; cursor: pointer; border: none; }
   .action-button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(74,144,226,0.4); color: white; }
   .action-button:active { transform: translateY(0); }
</style>
</head>
<body class="min-h-screen flex flex-col items-center">
<header class="w-full py-5 px-10 flex items-center justify-between bg-white/70 backdrop-blur-md sticky top-0 z-50">
   <div class="flex items-center gap-2">
       <div style="width: 30px; height: 30px; background: linear-gradient(135deg, #4a90e2, #357abd); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">◆</div>
       <span style="font-weight: 700; font-size: 1.1rem; color: #1a1a2e;">Skin Clinic AI</span>
   </div>
   <div class="flex items-center gap-4">
       <span class="text-[#7a8898] text-sm">Hệ thống trợ lý thông minh</span>
   </div>
</header>

<main class="w-full max-w-[800px] flex flex-col gap-8 py-8 px-6">
   <div class="text-center space-y-5 pt-2">
       <div class="inline-flex items-center justify-center p-5 rounded-full bg-gradient-to-br from-[#f0f7ff] to-white shadow-sm mb-2">
           <span class="material-symbols-outlined text-[#4a90e2] text-5xl">psychology</span>
       </div>
       <h1 class="text-[#1a1a2e] tracking-tight text-[42px] font-extrabold leading-tight">Trợ lý AI Da liễu</h1>
       <p class="text-[#7a8898] text-lg font-medium max-w-2xl mx-auto leading-relaxed">
           Chào mừng bạn đến với hệ thống trợ lý thông minh. Chúng tôi sử dụng AI để giúp bạn thấu hiểu làn da và kết nối với chuyên gia.
       </p>
   </div>

   <div class="w-full">
       <div class="flex flex-col items-start gap-4 rounded-2xl border-l-4 border-amber-400 bg-white/90 p-6 shadow-sm">
           <div class="flex items-start gap-4">
               <span class="material-symbols-outlined text-amber-500 text-2xl">info</span>
               <div class="flex flex-col gap-1">
                   <p class="text-[#1a1a2e] text-base font-bold">Lưu ý quan trọng</p>
                   <p class="text-[#7a8898] text-sm font-normal">
                       Kết quả AI chỉ mang tính chất tham khảo sơ bộ, không thay thế chẩn đoán chuyên sâu từ bác sĩ chuyên khoa.
                   </p>
               </div>
           </div>
       </div>
   </div>

   <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
       <div class="glass-card p-8 flex flex-col items-start relative overflow-hidden group">
           <div class="absolute -top-6 -right-6 opacity-[0.03] group-hover:opacity-[0.08] transition-opacity">
               <span class="material-symbols-outlined text-[140px]">photo_camera</span>
           </div>
           <div class="h-14 w-14 rounded-xl bg-gradient-to-br from-[#f0f7ff] to-white flex items-center justify-center mb-8 text-[#4a90e2] shadow-sm">
               <span class="material-symbols-outlined text-3xl">add_a_photo</span>
           </div>
           <h3 class="text-xl font-bold text-[#1a1a2e] mb-3">1. Đánh giá da mụn</h3>
           <p class="text-[#7a8898] text-sm leading-relaxed mb-8 min-h-[60px]">
               Phân tích tình trạng da qua hình ảnh để nhận diện mức độ mụn và gợi ý sơ bộ.
           </p>
           <div class="mt-auto">
               <button onclick="clickHiddenButton('BTN_DIAGNOSIS')" class="action-button">
                   <span>Bắt đầu ngay</span>
                   <span class="material-symbols-outlined text-xs">arrow_forward</span>
               </button>
           </div>
       </div>

       <div class="glass-card p-8 flex flex-col items-start relative overflow-hidden group">
           <div class="absolute -top-6 -right-6 opacity-[0.03] group-hover:opacity-[0.08] transition-opacity">
               <span class="material-symbols-outlined text-[140px]">calendar_month</span>
           </div>
           <div class="h-14 w-14 rounded-xl bg-gradient-to-br from-[#f0f7ff] to-white flex items-center justify-center mb-8 text-[#4a90e2] shadow-sm">
               <span class="material-symbols-outlined text-3xl">event_available</span>
           </div>
           <h3 class="text-xl font-bold text-[#1a1a2e] mb-3">2. Đặt lịch tư vấn</h3>
           <p class="text-[#7a8898] text-sm leading-relaxed mb-8 min-h-[60px]">
               Kết nối với bác sĩ chuyên khoa để nhận phác đồ điều trị cá nhân hóa.
           </p>
           <div class="mt-auto">
               <button onclick="clickHiddenButton('BTN_BOOKING')" class="action-button">
                   <span>Đặt lịch hẹn</span>
                   <span class="material-symbols-outlined text-xs">arrow_forward</span>
               </button>
           </div>
       </div>
   </div>

   <div class="text-center mt-8 pb-4">
       <p class="text-[#94a3b8] text-xs">© 2024 Skin Clinic AI. Tất cả quyền được bảo lưu.</p>
   </div>
</main>

<script>
   // Gắn hiệu ứng hover
   document.querySelectorAll('.glass-card').forEach(card => {
       card.addEventListener('mouseenter', function() { this.style.transform = 'translateY(-4px)'; });
       card.addEventListener('mouseleave', function() { this.style.transform = 'translateY(0)'; });
   });

   // Hàm giả lập thao tác click vào nút Streamlit đang bị ẩn
   function clickHiddenButton(buttonText) {
       const parentDoc = window.parent.document;
       const buttons = parentDoc.querySelectorAll('button');
       for (let i = 0; i < buttons.length; i++) {
           if (buttons[i].innerText.includes(buttonText)) {
               buttons[i].click();
               break;
           }
       }
   }
</script>
</body>
</html>
"""

# ==========================================
# 3. RENDER GIAO DIỆN & XỬ LÝ SỰ KIỆN
# ==========================================
# Inject CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Nút ẩn Streamlit để nhận tín hiệu từ JS điều hướng trang
if st.button("BTN_DIAGNOSIS", key="btn_diag"):
    st.switch_page("pages/1_ai_diagnosis.py")

if st.button("BTN_BOOKING", key="btn_book"):
    st.switch_page("pages/2_booking.py")

# Render giao diện HTML chính
components.html(HOMEPAGE_HTML, height=1000, scrolling=False)
