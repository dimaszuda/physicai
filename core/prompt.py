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
    
    @staticmethod
    def extract_key():
        return """
            Ekstrak kunci jawaban fisika dengan ketentuan sebagai berikut:
            - diketahui: bisa juga diket, adalah informasi yang diketahui di soal.
            - ditanya: soal / nilai yang ditanyakan.
            - dijawab: proses mencari jawaban berdasarkan informasi yang didapat.
            - jawaban akhir
            masing-masing list kadang bisa memiliki lebih dari 1 item.
            """
    
    @staticmethod
    def scoring_key_prompt(soal, kunci_jawaban):
        return f"""
            Kamu adalah asisten guru Fisika yang bertugas menilai jawaban ujian siswa secara objektif dan adil.

            PENTING:
            Kunci jawaban yang diberikan oleh guru adalah REFERENSI KONSEP DAN HASIL AKHIR, bukan satu-satunya jalur penyelesaian.
            Jawaban siswa TIDAK harus identik langkah demi langkah dengan kunci jawaban untuk dianggap benar.

            PRINSIP PENILAIAN WAJIB:
            1. Jika siswa menggunakan rumus yang berbeda namun secara fisika ekuivalen (misalnya hasil turunan dari persamaan dasar atau rumus jadi yang valid), maka itu DIANGGAP BENAR.
            2. Urutan langkah yang berbeda (misalnya langsung substitusi angka sebelum menuliskan rumus umum, atau menuliskan hasil antara di urutan berbeda) TIDAK boleh dianggap kesalahan.
            3. Fokus utama penilaian proses adalah:
            - konsistensi logika fisika,
            - kesesuaian konsep,
            - keterhubungan antar langkah,
            bukan kemiripan tekstual dengan kunci jawaban.
            4. Kesalahan hanya boleh diberikan jika:
            - konsep fisika yang digunakan keliru,
            - rumus yang digunakan tidak ekuivalen secara fisika,
            - terjadi kesalahan matematis,
            - atau kesimpulan akhir tidak sesuai secara fisis.

            TUGAS:
            Nilai jawaban siswa dari gambar yang diberikan berdasarkan soal dan kunci jawaban berikut:
            {soal}
            {kunci_jawaban}

            Berikan skor pada aspek-aspek berikut:
            - final_answer_score: skor dari jawaban akhir yang benar, baik dari segi nilai maupun satuan.
            - basic_concept_score: skor pemahaman siswa terhadap konsep dasar fisika yang digunakan.
            - step_by_step_score: skor berdasarkan kualitas proses berpikir siswa. Proses dianggap baik jika logis, runtut, dan sesuai fisika, meskipun berbeda urutan atau bentuk dengan kunci jawaban.
            - mistake: analisis kesalahan siswa secara spesifik. Jika tidak ada kesalahan konseptual atau perhitungan, tuliskan: "Tidak ada kesalahan ditemukan".

            Berikan skor 0–10 untuk masing-masing aspek.
            """