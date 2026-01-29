import streamlit as st

def add_student(student, method):
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 0.3, 0.5])
    
        with col1:
            st.subheader(f"Absen {student['id']}")
        
        with col2:
            st.write("")  # Spacer
        
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
        )

        student["files"] = files


        images = []
        pdfs = []

        for file in files:
            if file.type == "application/pdf":
                pdfs.append(file)
            else:
                images.append(file)

        if images:
            cols = st.columns(min(len(images), 4))
            for i, img in enumerate(images):
                img.seek(0)
                with cols[i % len(cols)]:
                    st.image(img, width=200)

        for pdf in pdfs:
            pdf.seek(0)
            st.pdf(pdf)

