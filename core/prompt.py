class Prompt:
    @staticmethod
    def question_prompt():
        return """
            Ekstrak soal fisika dari gambar dan dapatkan nomor soal, teks dan topik nya. Jika ada gambar pada soal, ekstrak informasi:
            - image_type: tipe gambar pada soal apakah dalam bentuk grafik, diagram atau ilustrasi.
            - description_image: deskripsi singkat yang menjelaskan makna visual dari gambar seperti objek yang ditampilkan, hubungan antar objek dan kondisi penting (sudut, arah, posisi, gaya, dll).
            - ocr_text: teks literal yang ada pada gambar seperti label, angka, sumbu, simbol, sudut.
            """
    
    @staticmethod
    def full_ai_prompt(soal):
        return f"""
            Kamu adalah asistant guru Fisika . Evaluasi dan berikan skor untuk jawaban ujian siswa. Skor yang kamu berikan harus objektif dan adil.

            TUGAS:
            Nilai jawaban siswa berdasarkan gambar jawaban yang diberikan dan data soal di bawah ini.
            {soal}

            Berikan skor pada aspek-aspek berikut:
            - final_answer_score: skor dari jawaban akhir yang benar, baik dari segi nilai atau satuan.
            - basic_concept_score: skor pemahaman siswa terhadap konsep dasar fisika yang digunakan di soal.
            - step_by_step_score: berikan skor berdasarkan proses siswa menjawab pertanyaan. Jawaban harus komplit yang selalu menjelaskan informasi yang diketahui, pertanyaan yang ditanyakan, informasi yang harus dicari dulu, formula yang digunakan dan proses menghitungnya.
            - mistake: analisis kesalahan yang dibuat oleh siswa, identifikasi dimana siswa melakukan kesalahan. kesalahan bisa terjadi di konsep yang salah, perhitungan matematika, formula yang keliru atau kesalahan lain. Jika tidak ada kesalahan ditemukan, cukup respon "Tidak ada kesalahan ditemukan"
            Berikan skor antara 0-10 untuk masing-masing aspek.
            """