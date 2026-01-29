class LLMSchema:
    @staticmethod
    def question_schema():
        return {
            "type": "object",
            "properties": {
                "question": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                        "question_number": {
                            "type": "integer"
                        },
                        "question_text": {
                            "type": "string",
                            "description": "Teks soal utama tanpa interpretasi gambar"
                        },
                        "image_type": {
                            "type": "string",
                            "enum": ["diagram", "graph", "illustration", "photo"],
                            "description": "Jenis visual gambar"
                        },
                        "description_image": {
                            "type": "string",
                            "description": "makna visual dari gambar dalam bahasa alami"
                        },
                        "ocr_text": {
                            "type": "string",
                            "description": "teks literal pada gambar yang dapat dibaca"
                        },
                        "topic": {"type": "string", "description": "materi utama"}
                        },
                        "required": ["question_number", "question_text", "topic"]
                    }
                }
            },
            "required": ["question"]
        }

    @staticmethod
    def full_ai_schema():
        return {
            "type": "object",
            "properties": {
                "scores": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                    "question_number": {
                        "type": "integer"
                    },
                    "final_answer_score": {
                        "type": "integer",
                    },
                    "basic_concept_score": {
                        "type": "integer"
                    },
                    "step_by_step_score": {
                        "type": "integer"
                    },
                    "mistake": {
                        "type": "string"
                    }
                    },
                    "required": ["question_number", "final_answer_score", "basic_concept_score", "step_by_step_score"]
                }
                }
            },
            "required": ["answers"]
        }
