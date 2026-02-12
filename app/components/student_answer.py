import streamlit as st

def add_student(student, method):
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 0.3, 0.5])
    
        with col1:
            st.subheader(f"Absen {student['id']}")
        
        with col2:
            st.write("") 
        
        with col3:
            if st.button("delete", key=f"delete_student_{method}_{student['id']}", type="secondary"):
                st.session_state.students = [
                    s for s in st.session_state.students if s['id'] != student['id']
                ]
                st.rerun()

        files = st.file_uploader(
            f"Upload jawaban Siswa dengan absen {student['id']}",
            accept_multiple_files=True,
            type=["pdf", "jpg", "png", "jpeg"],
            key=f"student_files_{student['id']}_{method}"
        ) or []

        student["files"] = files

        images = []
        pdfs = []

        for file in files:
            ftype = getattr(file, "type", "")
            if ftype == "application/pdf":
                pdfs.append(file)
            else:
                images.append(file)

        if images:
            cols = st.columns(min(len(images), 4))
            for i, img in enumerate(images):
                try:
                    img.seek(0)
                except Exception:
                    pass
                with cols[i % len(cols)]:
                    st.write(f"{getattr(img, 'name', 'file')} ({getattr(img, 'type', '')})")
                    try:
                        if hasattr(img, 'getvalue'):
                            data = img.getvalue()
                        else:
                            img.seek(0)
                            data = img.read()
                    except Exception:
                        try:
                            img.seek(0)
                            data = img.read()
                        except Exception:
                            data = None

                    if data is not None:
                        st.image(data, width=200)
                    else:
                        st.text("Unable to read image data")

        for pdf in pdfs:
            try:
                pdf.seek(0)
            except Exception:
                pass
            try:
                st.pdf(pdf)
            except Exception:
                st.write(f"PDF uploaded: {getattr(pdf, 'name', '')}")

