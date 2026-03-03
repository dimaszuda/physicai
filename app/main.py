import sys
import streamlit as st
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.evaluation import main
from page.hasil_export import render
from core.db.repository import BaseRepository
from core.auth import hash_password, verify_password


repo = BaseRepository()

st.set_page_config(
    page_title="PhysicAI - Login",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "new_username" not in st.session_state:
    st.session_state.new_username = ""
if "new_password" not in st.session_state:
    st.session_state.new_password = ""
if "new_password_confirm" not in st.session_state:
    st.session_state.new_password_confirm = ""

def login_user(username, password):
    resp = repo.select("users", {"user_name": username})
    rows = resp.data or []
    if not rows:
        return False

    stored = rows[0].get("password_hash")
    if stored and verify_password(password, stored):
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False




def create_account(username, email, password, password_confirm):
    if not username or not password or not email:
        return False, "Username,  email dan password tidak boleh kosong"
    
    if password != password_confirm:
        return False, "Password tidak cocok"
    
    if len(password) < 8:
        return False, "Password minimal 8 karakter"
    
    resp = repo.select("users", {"user_name": username})
    if resp.data:
        return False, "Username sudah terdaftar"
    
    try:
        hashed = hash_password(password)

        repo.insert(
            "users", {
                "user_name": username,
                "user_email": email,
                "created_at": datetime.now().timestamp(),
                "password_hash": hashed
        })
        return True, "Akun berhasil dibuat! Silakan login."
    except Exception as e:
        error_msg = str(e)
        if "row-level security" in error_msg.lower():
            return False, "Gagal membuat akun (RLS policy). Hubungi admin."
        return False, f"Gagal membuat akun: {error_msg}"


def show_login_page():
    """Tampilkan halaman login"""
    st.title("PhysicAI")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Masuk", use_container_width=True):
            if login_username and login_password:
                if login_user(login_username, login_password):
                    st.success("Login berhasil! Redirecting...")
                    st.rerun()
                else:
                    st.error("Username atau password salah")
            else:
                st.warning("Silakan isi semua field")
    
    with col2:
        st.subheader("Buat Akun Baru")
        new_username = st.text_input("Username", key="new_username")
        new_email = st.text_input("Email", key="new_email")
        new_password = st.text_input("Password", type="password", key="new_password")
        new_password_confirm = st.text_input("Konfirmasi Password", type="password", key="new_password_confirm")
        
        if st.button("Daftar", use_container_width=True):
            success, message = create_account(new_username, email=new_email, password=new_password, password_confirm=new_password_confirm)
            if success:
                st.success(message)
                st.session_state.new_username = ""
                st.session_state.new_password = ""
                st.session_state.new_email = ""
                st.session_state.new_password_confirm = ""
                st.sleep(1)
                st.rerun()
            else:
                st.error(message)


def show_main_app():
    st.title("📚 PhysicAI - Evaluator Essay")

    # sidebar navigation only visible post-login
    menu = st.sidebar.radio("Menu", ["Home", "Hasil Export"])

    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.write(f"Selamat datang, **{st.session_state.username}**!")
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

    st.markdown("---")

    if menu == "Home":
        st.info("🚀 Aplikasi evaluator essay siap digunakan!")
        try:
            from core.evaluation import main as evaluation_main
            evaluation_main()
        except ImportError:
            pass
    elif menu == "Hasil Export":
        render()

if not st.session_state.logged_in:
    show_login_page()
else:
    show_main_app()