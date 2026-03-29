import re

def normalize_arabic_text(text: str) -> str:
    """
    Menormalisasi teks Arab ke bentuk gundul dasar untuk keperluan matching ASR.
    """
    if not text:
        return ""

    # 1. Hapus Harakat (Tashkeel) dan Tatweel
    text = re.sub(r'[\u064B-\u065F\u0640]', '', text)
    
    # 2. Hapus Tanda Waqaf, Mad, dan Simbol Khusus Al-Qur'an
    # Termasuk: ۙ, ۗ, ۤ, ٰ, ۖ, ۚ, ۛ, ۜ, ۝, ۞, ۩, dll
    text = re.sub(r'[\u06D6-\u06ED\u06DF-\u06E8]', '', text)
    
    # 3. Normalisasi Huruf (Orthographic Normalization)
    # Normalisasi berbagai bentuk Alif menjadi Alif biasa
    text = re.sub(r'[إأآٱ]', 'ا', text)
    
    # Normalisasi Ya dan Alif Maqsura menjadi Ya biasa
    text = re.sub(r'[ىي]', 'ي', text)
    
    # Normalisasi Ta Marbutah menjadi Ha 
    # (Penting: ASR sering mendeteksi Ta Marbutah di akhir ayat sebagai 'Ha' karena waqaf)
    text = re.sub(r'ة', 'ه', text)
    
    # Normalisasi Hamzah (opsional, tapi berguna untuk ASR jonatasgrosman)
    text = re.sub(r'[ؤئ]', 'ء', text)
    
    # 4. Hapus tanda baca umum dan spasi berlebih
    text = re.sub(r'[^\w\s\u0600-\u06FF]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
