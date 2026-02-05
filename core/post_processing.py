import pandas as pd

class PostProcessing:
    def __init__(
            self,
            method = None,
            schema = None,
            responses = None,
            basic_concept_weight: int | None = None,
            step_by_step_weight: int | None = None,
            final_answer_weight: int | None = None,
            known_weight: int | None = None,
            asked_weight: int | None = None,
            answer_weight: int | None = None,
            final_weight: int | None = None
    ):
        self.method = method
        self.schema = schema
        self.responses = responses
        self.basic_concept_weight = basic_concept_weight 
        self.step_by_step_weight = step_by_step_weight 
        self.final_answer_weight = final_answer_weight
        self.known_weight = known_weight
        self.asked_weight = asked_weight
        self.answer_weight = answer_weight
        self.final_weight = final_weight

    def process_ai(
            self, 
            responses,
            basic_concept_weight,
            step_by_step_weight,
            final_answer_weight,
        ) -> pd.DataFrame:
        """
        Hitung dulu numerator yang digunakan untuk menghitung total skor tiap nomor.
        numerator itu didapat dari total bobot dibagi 10.
        sehingga nanti ketika total score dibagi numerator, akan mendapatkan nilai 10.
        """
        final_scores = []

        total_weight = (
            basic_concept_weight +
            step_by_step_weight +
            final_answer_weight
        )

        try:
            for num_std, student in enumerate(responses):
                for answer in student["scores"]:

                    basic_raw = answer["basic_concept_score"]
                    step_raw = answer["step_by_step_score"]
                    final_raw = answer["final_answer_score"]

                    basic_weighted = basic_raw * basic_concept_weight / 10
                    step_weighted = step_raw * step_by_step_weight / 10
                    final_weighted = final_raw * final_answer_weight / 10

                    total_score = (
                        basic_weighted +
                        step_weighted +
                        final_weighted
                    ) / total_weight * 10

                    score = {
                        "student": num_std+1,
                        "question_number": answer["question_number"],

                        "basic_concept_raw": basic_raw,
                        "step_by_step_raw": step_raw,
                        "final_answer_raw": final_raw,

                        "basic_concept_weighted": round(basic_weighted, 1),
                        "step_by_step_weighted": round(step_weighted, 1),
                        "final_answer_weighted": round(final_weighted, 1),

                        "total_score": round(total_score, 1),
                    }

                    if answer.get("mistake") is not None:
                        score["mistake"] = answer["mistake"]

                    final_scores.append(score)
            df = pd.DataFrame(final_scores)
            return df
        except Exception as E:
            print(f"error>> {E}")
            return None
        
    def process_keys(
            self, 
            responses,
            known_weight,
            asked_weight,
            answer_weight,
            final_weight
        ) -> pd.DataFrame:
        final_scores = []

        total_weight = (
            known_weight +
            asked_weight +
            answer_weight +
            final_weight
        )

        try:
            for num_std, student in enumerate(responses):
                for answer in student["scores"]:

                    known_raw= answer["score_diketahui"]
                    asked_raw = answer["score_ditanya"]
                    answer_raw = answer["score_dijawab"]
                    final_raw = answer["score_jawaban_akhir"]

                    known_weighted = known_raw * known_weight / 10
                    asked_weighted = asked_raw * asked_weight / 10
                    answer_weighted = answer_raw * answer_weight / 10
                    final_weighted = final_raw * final_weight / 10

                    total_score = (
                        known_weighted +
                        asked_weighted +
                        answer_weighted +
                        final_weighted
                    ) / total_weight * 10

                    score = {
                        "student": num_std+1,
                        "question_number": answer["question_number"],

                        "skor_diketahui_mentah": known_raw,
                        "skor_ditanya_mentah": asked_raw,
                        "skor_dijawab_mentah": answer_raw,
                        "skor_jawaban_akhir_mentah": final_raw,

                        "skor_diketahui_dengan_bobot": round(known_weighted, 1),
                        "skor_ditanya_dengan_bobot": round(asked_weighted, 1),
                        "skor_dijawab_dengan_bobot": round(answer_weighted, 1),
                        "skor_jawaban_akhir_dengan_bobot": round(final_weighted, 1),
                        "total_score": round(total_score, 1),
                    }


                    if answer.get("mistake") is not None:
                        score["mistake"] = answer["mistake"]

                    final_scores.append(score)
            df = pd.DataFrame(final_scores)
            return df
        except Exception as E:
            return None
    
    def process_rubrics(
            self,
            responses
    ) -> pd.DataFrame:
        final_scores = []
        try:
            for num_std, student in enumerate(responses):
                for answer in student["scores"]:
                    score = {
                        "student": num_std+1,
                        "question_number": answer["question_number"],
                        "score": answer["score"]
                    }

                    if answer.get("mistake") is not None:
                        score["mistake"] = answer["mistake"]

                    final_scores.append(score)
            df = pd.DataFrame(final_scores)
            return df
        except Exception as E:
            return None
        
    def process_component(
            self, 
            responses
        ) -> pd.DataFrame:
        final_scores = []
        try:
            for num_std, student in enumerate(responses):
                for answer in student["scores"]:                   
                    score_diketahui = answer["score_diketahui"]
                    skor_ditanya = answer["score_ditanya"]
                    skor_dijawab = answer["score_dijawab"]
                    skor_jawaban_akhir = answer["score_jawaban_akhir"]
                    
                    total_score = float(
                        score_diketahui +
                        skor_ditanya +
                        skor_dijawab +
                        skor_jawaban_akhir
                    )

                    score = {
                        "student": num_std+1,
                        "question_number": answer["question_number"],
                        "score_diketahui": round(score_diketahui, 1),
                        "skor_ditanya": round(skor_ditanya, 1),
                        "skor_dijawab": round(skor_dijawab, 1),
                        "skor_jawaban_akhir": round(skor_jawaban_akhir, 1),
                        "total_score": round(total_score, 1),
                    }

                    if answer.get("mistake") is not None:
                        score["mistake"] = answer["mistake"]

                    final_scores.append(score)
            df = pd.DataFrame(final_scores)
            return df
        except Exception as E:
            return None