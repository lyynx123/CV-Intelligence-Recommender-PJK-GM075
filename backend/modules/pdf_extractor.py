import fitz  # PyMuPDF
import re


def extract_text_from_pdf(file_path: str) -> str:
    """
    Membaca file PDF dan mengembalikan teks bersih.
    Hanya mendukung PDF digital (bukan hasil scan).
    """
    doc = fitz.open(file_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text("text")
    doc.close()
    return clean_text(full_text)


def extract_text_from_bytes(file_bytes: bytes) -> str:
    """
    Membaca PDF dari bytes (untuk upload via API) dan mengembalikan teks bersih.
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text("text")
    doc.close()
    return clean_text(full_text)


def clean_text(text: str) -> str:
    """
    Membersihkan teks hasil ekstraksi PDF.
    - Hapus karakter aneh
    - Normalisasi whitespace
    - Hapus baris kosong berlebih
    """
    text = re.sub(r'\s+', ' ', text)                # Normalisasi spasi
    text = re.sub(r'[^\w\s,.@+()/:=-]', '', text)  # Hapus karakter non-standar
    return text.strip()
