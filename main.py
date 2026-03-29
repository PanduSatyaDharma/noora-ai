import os
import time
from src.asr_engine import QuranASR
from src.audio_processor import load_and_resample_audio, record_audio_direct # <-- Update Import
from src.text_normalizer import normalize_arabic_text
from src.matcher import TextMatcher
from src.sequence_manager import QuranTracker

# Konfigurasi
JSON_PATH = "quran_data.json"
THRESHOLD_SCORE = 80.0

def main():
    print("="*50)
    print("AI Muroja'ah Engine (Proof of Concept)")
    print("="*50)

    try:
        tracker = QuranTracker(JSON_PATH)
    except FileNotFoundError:
        print(f"Error: File {JSON_PATH} tidak ditemukan.")
        return

    asr = QuranASR()
    matcher = TextMatcher()

    while True:
        try:
            surah_input = input("\nMasukkan nomor Surah yang ingin dimuroja'ah (1-114): ")
            surah_num = int(surah_input.strip())
            if tracker.set_surah(surah_num):
                break
            else:
                print("Surah tidak ditemukan di dataset. Coba lagi.")
        except ValueError:
            print("Input tidak valid. Harap masukkan angka.")

    print(f"\n--- Memulai Muroja'ah Surah {surah_num} ---")

    # 3. Loop Muroja'ah
    while not tracker.is_finished():
        current_ayah_data = tracker.get_current_ayah()
        ayah_num = current_ayah_data.get("ayah")
        original_text = current_ayah_data.get("text")
        clean_text_json = current_ayah_data.get("clean_text", original_text)

        print(f"\n[ Ayat {ayah_num} DISEMBUNYIKAN ]")
        
        # --- PERUBAHAN LOGIKA INPUT DI SINI ---
        action = input(f"Tekan ENTER untuk mulai merekam ayat {ayah_num}, atau ketik 'exit' untuk keluar: ")
        
        if action.lower() == 'exit':
            print("Sesi muroja'ah dihentikan.")
            break

        start_time = time.time()

        try:
            # Panggil mic langsung! (Output otomatis berformat Numpy Array 16kHz)
            audio_array = record_audio_direct()
            
            if len(audio_array) == 0:
                print("❌ Rekaman kosong, silakan coba lagi.")
                continue

            # Proses Inference (Numpy array langsung masuk ke ASR, mem-bypass disk I/O)
            raw_asr_text = asr.transcribe(audio_array)
            
            # Normalisasi
            normalized_expected = normalize_arabic_text(clean_text_json)
            normalized_asr = normalize_arabic_text(raw_asr_text)
            
            # Hitung skor
            score = matcher.calculate_similarity(normalized_expected, normalized_asr)
            
            print(f"Skor Akurasi: {score}% (Waktu proses AI: {time.time() - start_time:.2f} detik)")

            # Evaluasi
            if score >= THRESHOLD_SCORE:
                print("✅ BACAAN BENAR!")
                print(f"Teks Ayat: {original_text}")
                tracker.advance()
            else:
                print("❌ BACAAN KURANG TEPAT / TIDAK COCOK. Silakan coba lagi ayat ini.")
                print(f"(Debug - Yang terdeteksi AI: {raw_asr_text})") # Tambahan debug untuk membantu Anda

        except Exception as e:
            print(f"Terjadi kesalahan saat memproses ayat: {e}")

    if tracker.is_finished():
        print(f"\n🎉 Alhamdulillah! Muroja'ah Surah {surah_num} selesai.")

if __name__ == "__main__":
    main()