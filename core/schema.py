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

    def key_schema():
        pass