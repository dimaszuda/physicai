import os
import json
from google import genai
from dotenv import load_dotenv
from google.genai import types
from google.genai.types import GenerateContentConfig
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
        answer=None
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
                print(f"question file {file.name}")
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
            print(f"Error occured: {e}")
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
                    answer_img.append(parts)
                elif answer.type == "image/jpeg":
                    parts = process.read_img(answer.read(), mime_type=answer.type)
                    answer_img.append(parts)
                
            if answer_img is not None:
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[  
                        *answer_img,
                        prompt.scoring_key_prompt(soal, keys)
                    ],
                    config=GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=schema.component_score(),
                    )
                )

                return json.loads(response.text)
        except Exception as e:
            print(f"Error occured: {e}")
            return None
        
    def detect_rubric(
            self,
            keys,
            prompt,
            schema,
            process
    ):
        keys = json.dumps(keys)

        try:
            key = keys[0]
            if key.type == "application/pdf":
                key_img = process.read_pdf(key.read())
            elif key.type == "image/jpeg":
                key_img = process.read_img(key.read(), mime_type=key.type)
            
            if key_img is not None:
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        types.Part.from_bytes(
                            data=key_img,
                            mime_type="image/jpeg",
                        ),
                        prompt.detect_rubric_prompt()
                    ],
                    config= {
                        "response_mime_type": "application/json",
                        "response_json_schema": schema.detect_rubric_schema(),
                    }
                )

                return json.loads(response.text)
        except Exception as e:
            print(f"Error occured: {e}")
            return None
    
    def parsing_rubrics(
            self,
            keys,
            prompt,
            schema_rubrics,
            process,
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
                            prompt.extract_rubric()
                        ],
                        config={
                            "response_mime_type": "application/json",
                            "response_json_schema": schema_rubrics,
                        }
                    )
                return json.loads(response.text)
        except Exception as e:
            print(f"Error occured: {e}")
            return None
        
    def with_rubrics(
            self,
            soal,
            answers,
            rubrics,
            prompt,
            schema_scores,
            process
    ):
        soal = json.dumps(soal)
        rubrics = json.dumps(rubrics)
        answer_img = []

        try:
            for answer in answers:
                if answer.type == "application/pdf":
                    parts = process.read_pdf(answer.read())
                    answer_img.append(parts)
                elif answer.type == "image/jpeg":
                    parts = process.read_img(answer.read(), mime_type=answer.type)
                    answer_img.append(parts)
                
            if answer_img is not None:
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        *answer_img,
                        prompt.scoring_rubric_prompt(soal, rubrics)
                    ],
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": schema_scores,
                    }
                )

                return json.loads(response.text)
        except Exception as e:
            print(f"Error occured: {e}")
            return None