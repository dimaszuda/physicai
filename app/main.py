import streamlit as st
from components.student_answer import add_student

st.set_page_config(
    page_title="Physicai",
    layout="wide"
)

if "students" not in st.session_state:
    st.session_state.students = []

st.title("Physicai")
st.header("Low Effort Phyiscs Essay Assesment Evaluation")

st.text_input("Nama Ujian")
kelas = st.selectbox(
    "Kelas",
    ("X", "XI", "XII")
)
st.text_input("Group Kelas", placeholder="IPA 1")

tab_full_ai, tab_with_keys, tab_with_rubrics = st.tabs([
    "Full AI",
    "Evaluate with Keys",
    "Evaluate with Rubrics"
])

with tab_full_ai:
    st.write("Evaluate Student Physics Essay Assessment using full AI. " \
    "Let AI decide the correct answer and step by step process.")
    st.write("NOTE: AI may cause incorrect evaluation because its hallucination. \
             You can switch to others tab to provide keys/rubrics above to get more precise evaluation score.")

    
    left, right = st.columns([2, 1])  # Hapus vertical_alignment
    
    with left:
        with st.container(border=True): 
            st.subheader("Upload Exam Question and Student Answer here")

            upload_question = st.file_uploader(
                "Upload Exam Question", 
                key="question_uploader_ai",
                accept_multiple_files=True,
                type=["pdf", "jpg", "png", "jpeg"]
            )

            st.write("Add student answer")
            for student in st.session_state.students:
                add_student(student, "ai") 

            if st.button("Add Student", key="add full ai"):
                st.session_state.students.append({
                    "id": len(st.session_state.students) + 1,
                    "files": []
                })
                st.rerun()
    
    with right:
        with st.container(border=True):
            st.subheader("Tentukan Bobot untuk setiap aspek penilaian")
            step_by_step_weight = st.slider("Bobot untuk proses perhitungan", 0, 10)
            final_answer_weight = st.slider("Bobot untuk jawaban akhir", 0, 10)
    
    if st.button("Start Evaluate", key="button full ai"):
        pass

with tab_with_keys:
    st.write("Provide answer keys correspond to the exam questions and decide what weight used to score the answer")

    uploader, parameter = st.columns([2, 1])

    with uploader:
        with st.container(border=True):
            st.subheader("Upload Soal, Kunci Jawaban dan Jawaban siswa disini")
            upload_question = st.file_uploader(
                "Upload Soal Ujian", 
                key="question_uploader_keys",
                accept_multiple_files=True,
                type=["pdf", "jpg", "png", "jpeg"]
            )
            upload_keys = st.file_uploader(
                "Upload Kunci Jawaban", 
                key="keys_uploader",
                accept_multiple_files=True,
                type=["pdf", "jpg", "png", "jpeg"]
            )

            st.write("Add student answer")
            for student in st.session_state.students:
                add_student(student, "keys")              
            
            if st.button("Add Student", key="add with keys"):
                st.session_state.students.append({
                    "id": len(st.session_state.students) + 1,
                    "files": []
                })
                st.rerun()

    with parameter:
        with st.container(border=True):
            st.subheader("Tentukan bobot untuk setiap aspek penilaian")
            known_weight = st.slider("Bobot untuk \"Diketahui\"", 0, 10)
            asked_weight = st.slider("Bobot untuk \"Ditanya\"", 0, 10)
            answer_weight = st.slider("Bobot untuk \"Dijawab\"", 0, 10)

    if st.button("Start Evaluate", key="button with keys"):
        pass

with tab_with_rubrics:
    st.write("Provide Assesment Rubrics correspond to the exam questions to get more precise assesment score")
    
    st.subheader("Upload soal, rubrik penilaian dan jawaban siswa disini")

    upload_question = st.file_uploader(
        "Upload Soal Ujian", 
        key="question_uploader_rubrics",
        accept_multiple_files=True,
        type=["pdf", "jpg", "png", "jpeg"]
    )
    upload_keys = st.file_uploader(
        "Upload Kunci Jawaban", 
        key="keys_uploader_rubrics",
        accept_multiple_files=True,
        type=["pdf", "jpg", "png", "jpeg"]
    )

    st.write("Add student answer")
    for student in st.session_state.students:
        add_student(student, "rubrics") 
    
    if st.button("Add Student", key="add with rubrics"):
        st.session_state.students.append({
            "id": len(st.session_state.students) + 1,
            "files": []
        })
        st.rerun()
     

    if st.button("Start Evaluate", key="button with rubrics"):
        pass

    
