# 🎬 Prompt untuk Gemini Generate Video — Panduan Penggunaan CV-IR

Berikut adalah kumpulan prompt yang bisa Anda gunakan di **Google Gemini** (atau Google Veo) untuk membuat video panduan penggunaan aplikasi **CV-Intelligence Recommender** dari sisi pengguna (user).

> **Cara Pakai:** Copy-paste salah satu prompt di bawah ke Gemini, lalu sesuaikan jika diperlukan.

---

## 🎯 Prompt Utama (Video Lengkap - Rekomendasi)

```
Buatkan video panduan penggunaan aplikasi web bernama "CV-Intelligence Recommender" (CV-IR). Aplikasi ini adalah sistem rekomendasi pekerjaan berbasis AI yang membantu pencari kerja menemukan pekerjaan yang sesuai hanya dengan mengunggah CV dalam format PDF.

Tampilan aplikasi menggunakan dark theme premium berwarna gelap (navy/slate) dengan aksen gradasi ungu-biru. Font modern sans-serif.

Berikut adalah alur video yang harus dibuat (dari sudut pandang pengguna):

SCENE 1 - PEMBUKAAN (5 detik)
Tampilkan judul besar "CV-Intelligence Recommender" dengan tagline "Upload CV. Temukan Karir. Raih Masa Depan." di tengah layar dengan background gelap dan efek gradasi ungu-biru yang elegan.

SCENE 2 - HALAMAN UTAMA (8 detik)
Tampilkan halaman utama aplikasi web dengan:
- Sidebar di sebelah kiri bertuliskan "CV-IR" dengan logo target emoji 🎯, instruksi penggunaan, dan daftar tech stack (spaCy, Scikit-Learn, FastAPI, Streamlit, PyMuPDF)
- Area utama di tengah bertuliskan heading besar "CV-Intelligence Recommender" dengan subtitle "Upload CV kamu dan dapatkan rekomendasi pekerjaan yang sesuai dengan skill-mu!"
- Area upload bertuliskan "Upload CV Kamu" dengan ikon dokumen 📄 dan keterangan "Mendukung format PDF - Maksimal 10MB"
- Tombol besar berwarna gradasi ungu bertuliskan "Analisis CV Saya" dalam keadaan disabled (abu-abu)

SCENE 3 - UPLOAD CV (8 detik)
Animasikan kursor mouse yang mengklik area upload, lalu muncul dialog file browser. User memilih file PDF bernama "CV_Ahmad_Izzuddin.pdf". Setelah file terpilih, muncul bar kecil menampilkan nama file dan ukurannya (misal "CV_Ahmad_Izzuddin.pdf — 0.45 MB"). Tombol "Analisis CV Saya" berubah menjadi aktif (berwarna gradasi ungu cerah).

SCENE 4 - PROSES ANALISIS (5 detik)
Kursor mengklik tombol "Analisis CV Saya". Muncul loading spinner dengan teks "Menganalisis CV kamu... Mohon tunggu sebentar." di tengah layar.

SCENE 5 - HASIL PREDIKSI PEKERJAAN (8 detik)
Loading selesai, muncul hasil analisis:
- Card besar berwarna gradasi ungu-biru di tengah dengan ikon target 🎯, bertuliskan prediksi pekerjaan "Data Science" dan di bawahnya "Tingkat Kepercayaan: 87.3%"
- Di bawahnya ada 3 kotak statistik berdampingan: "10 Skill Terdeteksi", "5 Lowongan Cocok", "89% Top Match Score"

SCENE 6 - SKILL YANG TERDETEKSI (8 detik)
Scroll ke bawah, tampilkan bagian "Skill yang Terdeteksi" dengan badge-badge kecil berwarna biru gelap bertuliskan skill seperti: Python, Machine Learning, SQL, TensorFlow, Pandas, NumPy, Deep Learning, NLP, Docker, Git. Badge-badge ini tersusun rapi dalam baris-baris.

SCENE 7 - ESTIMASI GAJI (5 detik)
Di bawah skill, tampilkan card "Estimasi Gaji" dengan angka rentang gaji berwarna cyan/tosca: "Rp 12,000,000 - Rp 27,000,000" dan keterangan kecil "Berdasarkan skill dan pengalaman yang terdeteksi".

SCENE 8 - REKOMENDASI LOWONGAN (10 detik)
Di kolom sebelah kanan, tampilkan 5 card lowongan kerja dengan tampilan elegan:
- Card 1: "Data Scientist" di "Google" — Mountain View, CA — badge hijau "94%"
- Card 2: "Machine Learning Engineer" di "Meta" — Menlo Park, CA — badge hijau "89%"
- Card 3: "AI Research Engineer" di "Microsoft" — Redmond, WA — badge kuning "85%"
- Card 4: "Data Analyst" di "Amazon" — Seattle, WA — badge kuning "81%"
- Card 5: "NLP Engineer" di "OpenAI" — San Francisco, CA — badge kuning "78%"
Setiap card memiliki link berwarna ungu bertuliskan "🔗 Lihat Lowongan".

SCENE 9 - KLIK LOWONGAN (5 detik)
Kursor mengklik link "🔗 Lihat Lowongan" pada card pertama, kemudian tampilkan transisi halaman seolah-olah membuka tab baru menuju halaman LinkedIn.

SCENE 10 - PENUTUP (5 detik)
Tampilkan layar penutup dengan teks:
"CV-Intelligence Recommender (CV-IR) v1.0.0"
"Capstone Project PJK-GM075 | Pijak × IBM SkillsBuild"
"© 2026 Tim PJK-GM075"
dengan background gelap dan efek gradasi yang sama seperti pembukaan.

Gaya video: profesional, modern, smooth transitions, dark theme. Durasi total sekitar 60-70 detik. Resolusi 1920x1080 (landscape). Tanpa narasi suara, cukup teks di layar dan musik latar yang tenang/corporate.
```

---

## 🎞️ Prompt Alternatif (Versi Pendek - 30 Detik)

```
Buatkan video demo singkat 30 detik untuk aplikasi web "CV-Intelligence Recommender". 

Aplikasi ini memiliki dark theme (warna gelap navy dengan aksen gradasi ungu-biru). 

Alur video:
1. (5 detik) Tampilkan judul "CV-Intelligence Recommender" dengan tagline "Upload CV. Temukan Karir. Raih Masa Depan."
2. (5 detik) Tampilkan halaman web dengan area upload PDF dan tombol ungu "Analisis CV Saya"
3. (5 detik) User mengupload file PDF, klik tombol analisis, muncul loading spinner
4. (10 detik) Hasil muncul: prediksi pekerjaan "Data Science" dengan confidence 87%, daftar 10 skill terdeteksi dalam badge biru, estimasi gaji Rp 12-27 juta, dan 5 card rekomendasi lowongan kerja dari LinkedIn dengan match score
5. (5 detik) Penutup dengan logo dan teks "Capstone Project PJK-GM075 | Pijak × IBM SkillsBuild"

Gaya: profesional, modern, smooth. Resolusi 1920x1080 landscape. Tanpa suara narasi, hanya musik latar corporate yang tenang.
```

---

## 🖼️ Prompt Tambahan: Generate Thumbnail Video

```
Buatkan thumbnail untuk video panduan aplikasi web "CV-Intelligence Recommender". 

Desain:
- Background gelap (dark navy/slate) dengan efek gradasi ungu-biru
- Di tengah ada mockup tampilan aplikasi web dengan dark theme yang menampilkan hasil analisis CV (prediksi pekerjaan, skill badges, dan rekomendasi lowongan)
- Judul besar "CV-Intelligence Recommender" di atas mockup
- Emoji target 🎯 di samping judul
- Tagline kecil "Upload CV → AI Analisis → Rekomendasi Pekerjaan"
- Di pojok bawah kanan ada badge "Capstone Project PJK-GM075"
- Gaya modern, premium, profesional
- Resolusi 1920x1080
```

---

## 📝 Tips Penggunaan

1. **Pilih prompt yang sesuai kebutuhan:**
   - Prompt Utama → Untuk video panduan lengkap (~60 detik)
   - Prompt Alternatif → Untuk video demo singkat (~30 detik)
   - Prompt Thumbnail → Untuk gambar cover video

2. **Sesuaikan data di prompt** jika ingin menampilkan nama/data yang berbeda (misal nama file CV, skill yang terdeteksi, nama perusahaan di rekomendasi)

3. **Jika Gemini tidak bisa generate video panjang**, pecah prompt utama menjadi beberapa bagian per-scene, lalu gabungkan hasilnya menggunakan video editor

4. **Alternatif tools** jika Gemini belum mendukung video generation:
   - **Google Veo 3** (via AI Studio) — Untuk generate video dari teks
   - **Canva AI** — Untuk membuat video presentasi dengan template
   - **CapCut** — Untuk screen recording + editing
   - **OBS Studio** — Untuk screen recording langsung dari aplikasi yang sudah berjalan di localhost
