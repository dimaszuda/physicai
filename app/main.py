import sys
import json
from pathlib import Path

# Add parent directory to path to allow imports from core and other modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from components.student_answer import add_student
from core.evaluator import Evaluator
from core.processor import Processor
from core.prompt import Prompt
from core.schema import LLMSchema

prompt_schema = Prompt()
schema = LLMSchema()
process = Processor()
evaluator = Evaluator()

st.set_page_config(
    page_title="Physicai",
    layout="wide"
)

if "students" not in st.session_state:
    st.session_state.students = []

st.title("Physicai")
st.header("Low Effort with High Accuracy. AI-Based Phycis Exam Evaluator")

st.text_input("Nama Ujian")
kelas = st.selectbox(
    "Kelas",
    ("X", "XI", "XII")
)
st.text_input("Group Kelas", placeholder="IPA 1")

method = st.selectbox(
    "Pilih Metode Evaluasi",
    ("Full AI", "Evaluate with Keys", "Evaluate with Rubrics")
)

if method == "Full AI":
    st.write("Use full AI to evaluate student physics essay assessments. \
             Let the AI determine the correct answer and the step-by-step process.")
    st.write("Note that AI may produce an incorrect evaluation due to hallucinations. \
             You can switch to the other method and provide the keys or rubrics above to get a more precise evaluation score.")

    left, right = st.columns([2, 1])

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
        if upload_question is not None and st.session_state.students is not None:
            with st.spinner("Parsing question... this may take a while."):
                soal_soal = evaluator.parse_question(
                    question=upload_question,
                    process=process,
                    schema=schema,
                    prompt=prompt_schema
                )
            if soal_soal is not None:
                st.text_area(
                    "response",
                    value=json.dumps(soal_soal, indent=2, ensure_ascii=False),
                    height=400
                )
            else:
                st.text_area("response", value="Error")
            with st.spinner("Parsing answer... this may take a while"):
                for idx, student in enumerate(st.session_state.students):
                    print(f"Student: {student}")
                    with st.spinner(f"Scoring student absent {idx+1}"):
                        score = evaluator.full_ai(
                            soal=soal_soal,
                            answers=student["files"],
                            prompt=prompt_schema,
                            schema=schema,
                            process=process
                        )
                    if score is not None:
                        st.text_area(
                            f"Score Absen {idx+1}",
                            value=json.dumps(score, indent=2, ensure_ascii=False),
                            height=400
                        )
                    else:
                        st.text("None")

elif method == "Evaluate with Keys":
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
        if upload_question is not None and st.session_state.students is not None:
            with st.spinner("Parsing question... this may take a while."):
                soal_soal = evaluator.parse_question(
                    question=upload_question,
                    process=process,
                    schema=schema,
                    prompt=prompt_schema
                )
            if soal_soal is not None:
                st.text_area("response", value=soal_soal)
            else:
                st.text_area("response", value="Error")

elif method == "Evaluate with Rubrics":
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
     

    if st.button("Start Evaluate", key="button full ai"):
        if upload_question is not None and st.session_state.students is not None:
            with st.spinner("Parsing question... this may take a while."):
                soal_soal = evaluator.parse_question(
                    question=upload_question,
                    process=process,
                    schema=schema,
                    prompt=prompt_schema
                )
            if soal_soal is not None:
                st.text_area("response", value=soal_soal)
            else:
                st.text_area("response", value="Error")
