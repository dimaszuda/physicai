import fitz
from PIL import Image
from io import BytesIO
from google.genai import types  

class Processor:  
    def read_pdf(self, file_soal):
        parts = []
        zoom_x, zoom_y = 2.0, 2.0
        mat = fitz.Matrix(zoom_x, zoom_y)

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
        if isinstance(file_soal, (bytes, bytearray)):
            img = Image.open(BytesIO(file_soal))
        else:
            img = Image.open(file_soal)

        try:
            width, height = img.size
            print(f"image width: {width}")
            print(f"image height: {height}")

            if width >= 1000 or height >= 2000:
                img = img.resize((900, 1600), Image.LANCZOS)
            buf = BytesIO()
            fmt = "PNG" if "png" in mime_type.lower() else "JPEG"

            if fmt == "JPEG" and img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                background.save(buf, format=fmt, quality=85)
            else:
                img.save(buf, format=fmt)

            data = buf.getvalue()
        finally:
            img.close()

        return types.Part.from_bytes(
            data=data,
            mime_type=mime_type
        ) 