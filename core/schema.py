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
    
    @staticmethod
    def detect_rubric_schema():
        return {
            "type": "object",
            "properties": {
                "rubric_type": {
                    "type": "string",
                    "description": "Tipe rubrik penilaian yang digunakan pada kunci jawaban",
                    "enum": ["hollistik", "analitik", "component"]
                }
            },
            "required": ["rubric_type"]
        }
    
    @staticmethod
    def hollistik_schema():
        return {
            "type": "object",
            "properties": {
                "score_rubrics": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "answer_number": {
                                "type": "integer"
                            },
                            "level": {
                                "type": "string",
                                "description": "Nama level (mis. sangat baik, cukup, kurang)"
                            },
                            "score_range": {
                                "type": "array",
                                "items": { "type": "number" },
                                "minItems": 2,
                                "maxItems": 2,
                                "description": "Rentang skor minimum dan maksimum"
                            },
                            "description_level": {
                                "type": "string",
                                "description": "a description explaining the criteria that indicate the score level"
                            }
                        },
                        "required": ["answer_number", "score_range", "description_level"]
                        }
                    }
                },
            "required": ["score_rubrics"]
        }
    
    @staticmethod
    def analytic_schema():
        return {
            "type": "object",
            "properties": {
                "score_rubrics": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "answer_number": {
                                "type": "integer",
                                "description": "Nomor soal atau jawaban"
                            },
                            "criterion_name": {
                                "type": "string",
                                "description": "Nama kriteria (mis. konsep, langkah penyelesaian, ketelitian)"
                            },
                            "levels": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "level_name": {
                                            "type": "string",
                                            "description": "Nama level (mis. sangat baik, cukup, kurang)"
                                        },
                                        "score": {
                                            "type": "integer",
                                            "description": "Skor untuk level ini"
                                        },
                                        "description": {
                                            "type": "string",
                                            "description": "Deskripsi kriteria pada level tersebut"
                                        }
                                    },
                                    "required": ["score", "description"]
                                }
                            }
                        },
                        "required": ["answer_number", "levels"]
                    }
                }
            },
            "required": ["score_rubrics"]
        }
    
    @staticmethod
    def component_schema():
        return {
            "type": "object",
            "properties": {
                "score_rubrics": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "answer_number": {
                                "type": "integer",
                                "description": "Nomor soal atau jawaban"
                            },
                            "components": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "component_name": {
                                            "type": "string",
                                            "enum": ["diketahui", "ditanya", "dijawab", "jawaban akhir"]
                                        },
                                        "score": {
                                            "type": "integer",
                                            "description": "Skor untuk komponen ini"
                                        },
                                        "component_description": {
                                            "type": "string",
                                            "description": "Deskripsi kriteria pada level tersebut"
                                        }
                                    },
                                    "required": ["component_name", "score"]
                                }
                            }
                        },
                        "required": ["answer_number", "components"]
                    }
                }
            },
            "required": ["score_rubrics"]
        }
    
    @staticmethod
    def rubrics_score():
        return {
            "type": "object",
            "properties": {
                "scores": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question_number": {"type": "integer"},
                            "score": {"type": "integer"},
                            "mistake": {"type": "string"}
                        },
                        "required": ["question_number", "score"]
                    }
                }
            },
            "required": ["scores"]
        }
    
    @staticmethod
    def component_score():
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
                            "diketahui": {
                                "type": "integer",
                            },
                            "ditanya": {
                                "type": "integer"
                            },
                            "dijawab": {
                                "type": "integer"
                            },
                            "jawaban_akhir": {
                                "type": "integer"
                            },
                            "mistake": {
                                "type": "string"
                            }
                        },
                        "required": ["question_number", "diketahui", "ditanya", "dijawab"]
                    }
                }
            },
            "required": ["scores"]
        }
    

