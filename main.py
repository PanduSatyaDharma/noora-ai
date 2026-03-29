import os
import time
from src.asr_engine import QuranASR
from src.audio_processor import load_and_resample_audio
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

    # 1. Inisialisasi Modul
    try:
        tracker = QuranTracker(JSON_PATH)
    except FileNotFoundError:
        print(f"Error: File {JSON_PATH} tidak ditemukan.")
        return

    asr = QuranASR()
    matcher = TextMatcher()

    # 2. Setup Sesi Muroja'ah
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

        # Tampilkan placeholder
        print(f"\n[ Ayat {ayah_num} DISEMBUNYIKAN ]")
        
        # Minta input audio
        audio_path = input(f"Masukkan path audio untuk Surah {surah_num} Ayat {ayah_num} (Ketik 'exit' untuk keluar): ").strip(' "\'')
        
        if audio_path.lower() == 'exit':
            print("Sesi muroja'ah dihentikan.")
            break

        if not os.path.exists(audio_path):
            print("File audio tidak ditemukan. Silakan cek kembali path file Anda.")
            continue

        print("Memproses audio dan mendeteksi bacaan...")
        start_time = time.time()

        try:
            # Pipeline Proses
            audio_array = load_and_resample_audio(audio_path)
            raw_asr_text = asr.transcribe(audio_array)
            
            # Normalisasi kedua belah pihak (ASR dan JSON)
            normalized_expected = normalize_arabic_text(clean_text_json)
            normalized_asr = normalize_arabic_text(raw_asr_text)
            
            # Hitung skor
            score = matcher.calculate_similarity(normalized_expected, normalized_asr)
            
            # Tampilkan log debug (bisa di-comment untuk production)
            # print(f"DEBUG Expected (Norm): {normalized_expected}")
            # print(f"DEBUG ASR      (Norm): {normalized_asr}")
            print(f"Skor Akurasi: {score}% (Waktu proses: {time.time() - start_time:.2f} detik)")

            # Evaluasi Logika
            if score >= THRESHOLD_SCORE:
                print("✅ BACAAN BENAR!")
                print(f"Teks Ayat: {original_text}")
                tracker.advance()
            else:
                print("❌ BACAAN KURANG TEPAT / TIDAK COCOK. Silakan coba lagi ayat ini.")

        except Exception as e:
            print(f"Terjadi kesalahan saat memproses ayat: {e}")

    if tracker.is_finished():
        print(f"\n🎉 Alhamdulillah! Muroja'ah Surah {surah_num} selesai.")

if __name__ == "__main__":
    main()