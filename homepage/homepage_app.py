import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(layout="wide")

# Đọc file HTML
html_file = Path(__file__).parent / "homepage.html"

if html_file.exists():
    html_content = html_file.read_text(encoding="utf-8")

    # Nhúng HTML vào Streamlit
    components.html(
        html_content,
        height=1200,  # chỉnh nếu bị cắt
        scrolling=True
    )
else:
    st.error("Không tìm thấy homepage.html")