import streamlit as st


def render():
    # protect page
    if not st.session_state.get("logged_in"):
        st.warning("Silakan login terlebih dahulu untuk melihat halaman ini.")
        st.write("Silakan login terlebih dahulu untuk melihat halaman ini.")
        return

    st.title("📤 Hasil Export")
    st.write("Halaman ini nantinya menampilkan pilihan export dan download.")
    # tambahan konten ekspor bisa diletakkan di sini


if __name__ == "__main__":
    render()
