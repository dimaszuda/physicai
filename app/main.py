import streamlit as st

st.title("Physicai")
st.header("Low Effort Phyiscs Essay Assesment Evaluation")

tab_full_ai, tab_with_keys, tab_with_rubrics = st.tabs([
    "Full AI",
    "Evaluate with Keys",
    "Evaluate with Rubrics"
])

with tab_full_ai:
    st.write("Evaluate Student Physics Essay Assessment using full AI. " \
    "Let AI decide the correct answer and step by step process.")
    st.write("NOTE: AI may cause incorrect evaluation because its hallucination.")
    
    left, right = st.columns([0.8, 0.2])  # Hapus vertical_alignment
    
    with left:
        upload_question = st.file_uploader("Upload Soal Ujian", key="question_uploader_ai")
        upload_answer = st.file_uploader("Upload Jawaban Siswa", key="answer_uploader_ai")
    
    with right:
        step_by_step_weight = st.slider("Bobot untuk proses perhitungan", 0, 10)
        final_answer_weight = st.slider("Bobot untuk jawaban akhir", 0, 10)
    
    st.button("Start Evaluate", key="ai_evaluation")

with tab_with_keys:
    st.write("Provide answer keys correspond to the exam questions and decide what weight used to score the answer")

    uploader, parameter = st.columns([0.8, 0.2])

    with uploader:
        upload_question = st.file_uploader("Upload Soal Ujian", key="question_uploader_keys")
        upload_keys = st.file_uploader("Upload Kunci Jawaban", key="keys_uploader")
        upload_answer = st.file_uploader("Upload Jawaban Siswa", key="answer_uploader_keys")
    
        known_weight = parameter.slider("Bobot untuk \"Diketahui\"", 0, 10)
        asked_weight = parameter.slider("Bobot untuk \"Ditanya\"", 0, 10)
        answer_weight = parameter.slider("Bobot untuk \"Dijawab\"", 0, 10)

        st.button("Start Evaluate", key="key evalution")

with tab_with_rubrics:
    st.write("Provide Assesment Rubrics correspond to the exam questions to get more precise assesment score")

    upload_question = st.file_uploader("Upload Soal Ujian", key="question_uploader_rubrics")
    upload_keys = st.file_uploader("Upload Kunci Jawaban", key="keys_uploader_rubrics")
    upload_answer = st.file_uploader("Upload Jawaban Siswa", key="answer_uploader_rubrics")

    st.button("Start Evaluate", key="rubrics evalution")
