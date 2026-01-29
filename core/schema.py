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
    def score_schema():
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
            "required": ["scores"]
        }
    
    @staticmethod
    def key_schema():
        return {
            "type": "object",
            "properties": {
                "keys": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "nomor_soal": {
                                "type": "integer"
                            },
                            "diketahui": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "variable": { "type": "string" },
                                        "value": { "type": "string" },
                                        "unit": { "type": "string" }
                                    },
                                    "required": ["variable", "value"]
                                }
                            },
                            "ditanya": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "dijawab": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "step": { "type": "string" },
                                        "formula": { "type": "string" },
                                        "calculation": { "type": "string" },
                                    },
                                    "required": ["step", "formula"]
                                }
                            },
                            "jawaban_akhir": {
                                "type": "string"
                            }

                        },
                        "required": ["nomor_soal", "diketahui", "ditanya", "dijawab", "jawaban_akhir"]
                    }
                }
            },
            "required": ["keys"]
        }

