import os
import json
from google import genai
from dotenv import load_dotenv
from google.genai import types
from streamlit.runtime.uploaded_file_manager import UploadedFile

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

    def parse_question(
            self, 
            question, 
            process,
            schema,
            prompt
    ):
        try:
            soal_soal = {"question": []}
            soal_img = []
            for file in question:
                if file.type == 'application/pdf':
                    parts = process.read_pdf(file.read())
                    soal_img.extend(parts)
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
    
    def full_ai(
            self,
            soal,
            answers,
            prompt,
            schema,
            process
    ):
        soal = json.dumps(soal)
        answer_img = []
        try:
            for answer in answers:
                if answer.type == "application/pdf":
                    parts = process.read_pdf(answer.read())
                    answer_img.extend(parts)
                elif answer.type == 'image/jpeg':
                    part = process.read_img(answer.read(), mime_type=answer.type)
                    answer_img.append(part)

                if answer_img is not None:
                    print("process image soal")
                    response = self.client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[  
                            *answer_img,
                            prompt.full_ai_prompt(soal)
                        ],
                        config={
                            "response_mime_type": "application/json",
                            "response_json_schema": schema.score_schema(),
                        }
                    )
                    print(response.text)
                    return json.loads(response.text)
        except Exception as e:
            print(f"Error occured: {e}")
            return None

    def parsing_keys(
            self,
            keys,
            prompt,
            schema,
            process
    ):
        key_imgs = []
        key_result = []
        try:
            for key in keys:
                if key.type == "application/pdf":
                    parts = process.read_pdf(key.read())
                    key_imgs.extend(parts)
                elif key.type == "image/jpeg":
                    parts = process.read_img(key.read(), mime_type=key.type)
                    key_imgs.extend(parts)
            
            if key_imgs is not None:
                response = self.client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[  
                            *key_imgs,
                            prompt.extract_key()
                        ],
                        config={
                            "response_mime_type": "application/json",
                            "response_json_schema": schema.key_schema(),
                        }
                    )
                return json.loads(response.text)
        except Exception as e:
            print(f"Error Occured: {e}")
            return None
        
    def with_keys(
            self,
            soal,
            answers,
            keys,
            prompt,
            schema,
            process
    ):
        soal = json.dumps(soal)
        keys = json.dumps(keys)
        answer_img = []

        try:
            for answer in answers:
                if answer.type == "application/pdf":
                    parts = process.read_pdf(answer.read())
                    answer_img.extend(parts)
                elif answer.type == "image/jpeg":
                    parts = process.read_img(answer.read(), mime_type=answer.type)
                    answer_img.extend(parts)
                
                if answer_img is not None:
                    response = self.client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[  
                            *answer_img,
                            prompt.scoring_key_prompt(soal, keys)
                        ],
                        config={
                            "response_mime_type": "application/json",
                            "response_json_schema": schema.score_schema(),
                        }
                    )

                    return json.loads(response.text)
        except Exception as e:
            print(f"Error occured: {e}")
            return None
        