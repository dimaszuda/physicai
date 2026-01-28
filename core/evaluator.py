import os
import json
from google import genai
from dotenv import load_dotenv
from google.genai import types
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from streamlit.runtime.uploaded_file_manager import UploadedFile
else:
    UploadedFile = object

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class Evaluator:
    def __init__(
        self,
        prompt=None,
        process=None,
        schema=None,
        method: str | None = None,
        question: list[UploadedFile] | None = None,
        keys: list[UploadedFile] | None = None,
        rubrics: list[UploadedFile] | None = None,
        answer: list[UploadedFile] | None = None
    ):
        self.method = method
        self.question = question
        self.keys = keys
        self.rubrics = rubrics
        self.answer = answer
        self.process = process
        self.schema = schema
        self.prompt = prompt
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def parse_question(self, 
                       question, 
                       process,
                       schema,
                       prompt):
        try:
            soal_soal = {"question": []}
            soal_img = []
            for file in question:
                if file.type == 'application/pdf':
                    parts = process.read_pdf(file.read())
                    response = self.client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[  
                            *parts,
                            prompt.question_prompt()
                        ],
                        config={
                            "response_mime_type": "application/json",
                            "response_json_schema": schema.question_schema(),
                        }
                    )
                    parsed = json.loads(response.text)
                    soal_soal["question"].extend([question for question in parsed.get("question", [])])
                elif file.type == 'image/jpeg':
                    part = process.read_img(file.read(), mime_type=file.type)
                    soal_img.append(part)
            if soal_img is not None:
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[  
                        *soal_img,
                        prompt.question_prompt()
                    ],
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": schema.question_schema(),
                    }
                )
                parsed = json.loads(response.text)
                soal_soal["question"].extend([question for question in parsed["question"]])
            return soal_soal
        except Exception as E:
            print(f"Error occured: {E}")
            return None



    
    def full_ai():
        pass