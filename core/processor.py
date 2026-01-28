import fitz
from google.genai import types  
from io import BytesIO

class Processor:  
    def read_pdf(self, file_soal):
        parts = []
        zoom_x, zoom_y = 2.0, 2.0
        mat = fitz.Matrix(zoom_x, zoom_y)

        # Handle both file paths and bytes
        if isinstance(file_soal, bytes):
            docs = fitz.open(stream=file_soal, filetype="pdf")
        else:   
            docs = fitz.open(file_soal)

        for page_num in range(len(docs)):
            page = docs.load_page(page_num)
            pixmap = page.get_pixmap(matrix=mat)

            parts.append(
                types.Part.from_bytes(
                    data=pixmap.tobytes("jpg"),
                    mime_type="image/jpeg"
                )
            )

        docs.close()
        return parts

    def read_img(self, file_soal, mime_type: str = "image/jpeg"):
        # Handle both file paths and bytes and return a types.Part
        if isinstance(file_soal, bytes):
            data = file_soal
        else:
            with open(file_soal, 'rb') as image:
                data = image.read()

        return types.Part.from_bytes(
            data=data,
            mime_type=mime_type
        )
        