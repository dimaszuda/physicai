import sys
import json
from io import BytesIO
from pathlib import Path
from datetime import datetime

# Add parent directory to path to allow imports from core and other modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from core.prompt import Prompt
from core.schema import LLMSchema
from core.evaluator import Evaluator
from core.processor import Processor
from core.post_processing import PostProcessing
from components.student_answer import add_student

prompt_schema = Prompt()
schema = LLMSchema()
process = Processor()
evaluator = Evaluator()
post_processing = PostProcessing()

st.set_page_config(
    page_title="Physicai",
    layout="wide"
)

if "students" not in st.session_state:
    st.session_state.students = []

st.title("Physicai")
st.header("Low Effort with High Accuracy. AI-Based Physics Exam Evaluator")

nama_ujian = st.text_input("Nama Ujian")
kelas = st.selectbox(
    "Kelas",
    ("X", "XI", "XII")
)
group = st.text_input("Group Kelas", placeholder="IPA 1")

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
            basic_concept_weight = st.slider("Bobot untuk Konsep Dasar", 1, 10)
            step_by_step_weight = st.slider("Bobot untuk proses perhitungan", 1, 10)
            final_answer_weight = st.slider("Bobot untuk jawaban akhir", 1, 10)
    
    responses = []

    if st.button("Start Evaluate", key="button full ai"):
        if upload_question is not None and st.session_state.students is not None:
            with st.spinner("Parsing question... this may take a while."):
                soal_soal = evaluator.parse_question(
                    question=upload_question,
                    process=process,
                    schema=schema,
                    prompt=prompt_schema
                )

            with st.spinner("Parsing answer... this may take a while"):
                for idx, student in enumerate(st.session_state.students):
                    with st.spinner(f"Scoring student absent {idx+1}"):
                        score = evaluator.full_ai(
                            soal=soal_soal,
                            answers=student["files"],
                            prompt=prompt_schema,
                            schema=schema,
                            process=process
                        )

                    if score is not None:
                        responses.append(score)
            
            with st.spinner("Scoring student answer..."):
                result = post_processing.process_ai(
                    responses=responses,
                    basic_concept_weight=basic_concept_weight,
                    step_by_step_weight=step_by_step_weight,
                    final_answer_weight=final_answer_weight
                )

            if result is not None:
                st.session_state['last_result_df'] = result
                buf = BytesIO()
                result.to_excel(buf, index=False, engine="openpyxl")
                buf.seek(0)
                st.session_state['last_result_bytes'] = buf.getvalue()
                st.session_state['last_result_filename'] = f"Nilai_{nama_ujian}_kelas_{kelas}_{group}_{datetime.now().strftime('%Y%m%d')}_full_ai.xlsx"

    if 'last_result_bytes' in st.session_state and st.session_state.get('last_result_filename', '').endswith('_full_ai.xlsx'):
        with st.expander("Show score"):
            st.dataframe(
                st.session_state['last_result_df'].style.format(
                    {
                        "basic_concept_weighted": "{:.1f}",
                        "step_by_step_weighted": "{:.1f}",
                        "final_answer_weighted": "{:.1f}",
                        "total_score": "{:.1f}"
                    }
                ).hide(axis="index"),
                width="content"
            )

        st.download_button(
            label="Download Result",
            data=st.session_state['last_result_bytes'],
            file_name=st.session_state['last_result_filename'],
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

elif method == "Evaluate with Keys":
    st.write("Provide answer keys correspond to the exam questions and decide what weight used to score the answer. In this method, you don't need to provide the score each number or component.")
    st.write("Note that AI may produce an incorrect evaluation due to hallucinations.")

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
            known_weight = st.slider("Bobot untuk \"Diketahui\"", 1, 10)
            asked_weight = st.slider("Bobot untuk \"Ditanya\"", 1, 10)
            answer_weight = st.slider("Bobot untuk \"Dijawab\"", 1, 10)
            final_weight = st.slider("Bobot untuk jawaban akhir", 1, 10)

    responses = []

    if st.button("Start Evaluate", key="button with keys"):
        if upload_question is not None and st.session_state.students is not None:
            with st.spinner("Parsing question... this may take a while."):
                soal_soal = evaluator.parse_question(
                    question=upload_question,
                    process=process,
                    schema=schema,
                    prompt=prompt_schema
                )
            
            with st.spinner("Parsing answer key... This may take a while"):
                keys = evaluator.parsing_keys(
                    keys=upload_keys,
                    prompt=prompt_schema,
                    schema=schema,
                    process=process
                )

            with st.spinner("Parsing student answer... this may take a while"):
                for idx, student in enumerate(st.session_state.students):
                    with st.spinner(f"Scoring student absent {idx+1}"):
                        score = evaluator.with_keys(
                            soal=soal_soal,
                            answers=student["files"],
                            prompt=prompt_schema,
                            keys=keys,
                            schema=schema,
                            process=process
                        )
                    if score is not None:
                        responses.append(score)
                    else:
                        st.text("None")

            with st.spinner("Scoring student answer..."):
                result = post_processing.process_keys(
                    responses=responses,
                    known_weight=known_weight,
                    asked_weight=asked_weight,
                    answer_weight=answer_weight,
                    final_weight=final_weight
                )
                
            if result is not None:
                st.session_state['last_result_df'] = result
                buf = BytesIO()
                result.to_excel(buf, index=False, engine="openpyxl")
                buf.seek(0)
                st.session_state['last_result_bytes'] = buf.getvalue()
                st.session_state['last_result_filename'] = f"Nilai_{nama_ujian}_kelas_{kelas}_{group}_{datetime.now().strftime('%Y%m%d_%H%M')}_with_keys.xlsx"

    if 'last_result_bytes' in st.session_state and st.session_state.get('last_result_filename', '').endswith('_with_keys.xlsx'):
        with st.expander("Show score"):
            st.dataframe(
                st.session_state['last_result_df'].style.format(
                    {
                        "skor_diketahui_dengan_bobot": "{:.2f}",
                        "skor_ditanya_dengan_bobot": "{:.2f}",
                        "skor_dijawab_dengan_bobot": "{:.2f}",
                        "skor_jawaban_akhir_dengan_bobot": "{:.2f}",
                        "total_score": "{:.2f}"
                    }
                ).hide(axis="index"),
                width="content"
            )

        st.download_button(
            label="Download Result",
            data=st.session_state['last_result_bytes'],
            file_name=st.session_state['last_result_filename'],
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

elif method == "Evaluate with Rubrics":
    st.write("Provide Assesment Score Rubrics correspond to the exam questions to get more precise assesment score. In this method, You can use hollistic, analytic or component based structure rubric for scoring")
    st.write("Note that AI may produce an incorrect evaluation due to hallucinations.")
    with st.container(border=True):
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

    responses = []
     
    if st.button("Start Evaluate", key="button with rubrics"):
        if upload_question is not None and st.session_state.students is not None:
            with st.spinner("Parsing question... this may take a while."):
                soal_soal = evaluator.parse_question(
                    question=upload_question,
                    process=process,
                    schema=schema,
                    prompt=prompt_schema
                )
            
            with st.spinner("Detect scoring rubrics type... This may take a while"):
                rubric_type = evaluator.detect_rubric(
                    keys=upload_keys,
                    prompt=prompt_schema,
                    schema=schema,
                    process=process
                )

            if rubric_type is not None:
                if rubric_type["rubric_type"] == "hollistik":
                    schema_rubrics = schema.hollistik_schema()
                    schema_scores = schema.rubrics_score()
                    postprocess = post_processing.process_rubrics(responses=responses)
                elif rubric_type["rubric_type"] == "analitik":
                    schema_rubrics = schema.analytic_schema()
                    schema_scores = schema.rubrics_score()
                    postprocess = post_processing.process_rubrics(responses=responses)
                elif rubric_type["rubric_type"] == "component":
                    schema_rubrics = schema.component_schema()
                    schema_scores = schema.component_score()
                    postprocess = post_processing.process_component(responses=responses)

                with st.spinner("Parsing scoring rubric... This may take a while"):
                    rubrics = evaluator.parsing_rubrics(
                        keys=upload_keys,
                        prompt=prompt_schema,
                        schema_rubrics=schema_rubrics,
                        process=process
                    )
            
            if rubrics is not None:
                with st.spinner("Parsing student answer... this may take a while"):
                    for idx, student in enumerate(st.session_state.students):
                        with st.spinner(f"Scoring student absent {idx+1}"):
                            score = evaluator.with_rubrics(
                                soal=soal_soal,
                                answers=student["files"],
                                prompt=prompt_schema,
                                rubrics=rubrics,
                                schema_scores=schema_scores,
                                process=process
                            )
                        if score is not None:
                            responses.append(score)
                        else:
                            st.text("None")
                
                with st.spinner("Scoring student answer..."):
                    if rubric_type["rubric_type"] == "hollistik" or rubric_type["rubric_type"] == "analitik":
                        result = post_processing.process_rubrics(responses=responses)
                    elif rubric_type["rubric_type"] == "component":
                        result = post_processing.process_component(responses=responses)
                
                if result is not None:
                    # persist rubrics result
                    st.session_state['last_result_df'] = result
                    buf = BytesIO()
                    result.to_excel(buf, index=False, engine="openpyxl")
                    buf.seek(0)
                    st.session_state['last_result_bytes'] = buf.getvalue()
                    st.session_state['last_result_filename'] = f"Nilai_{nama_ujian}_kelas_{kelas}_{group}_{datetime.now().strftime('%Y%m%d_%H%M')}_with_rubrics.xlsx"

    # show persisted rubrics result if present
    if 'last_result_bytes' in st.session_state and st.session_state.get('last_result_filename', '').endswith('_with_rubrics.xlsx'):
        with st.expander("Show score"):
            st.dataframe(st.session_state['last_result_df'].style.hide(axis="index"), width="content")

        st.download_button(
            label="Download Result",
            data=st.session_state['last_result_bytes'],
            file_name=st.session_state['last_result_filename'],
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
