class Prompt:
    @staticmethod
    def question_prompt():
        return """
            Ekstrak soal fisika dari gambar dan dapatkan nomor soal, teks dan topik nya. Jika ada gambar pada soal, ekstrak informasi:
            - image_type: tipe gambar pada soal apakah dalam bentuk grafik, diagram atau ilustrasi.
            - description_image: deskripsi singkat yang menjelaskan makna visual dari gambar seperti objek yang ditampilkan, hubungan antar objek dan kondisi penting (sudut, arah, posisi, gaya, dll).
            - ocr_text: teks literal yang ada pada gambar seperti label, angka, sumbu, simbol, sudut.
            """