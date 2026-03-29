import librosa
import numpy as np
import sounddevice as sd
import queue
import sys

def load_and_resample_audio(file_path: str, target_sr: int = 16000) -> np.ndarray:
    """
    (Fungsi lama tetap dipertahankan jika sewaktu-waktu butuh testing via file)
    """
    try:
        speech_array, _ = librosa.load(file_path, sr=target_sr, mono=True)
        return speech_array
    except Exception as e:
        raise RuntimeError(f"Gagal memproses audio {file_path}. Error: {e}")

def record_audio_direct(sample_rate: int = 16000) -> np.ndarray:
    """
    Merekam audio langsung dari microphone pengguna.
    Mengembalikan numpy array 1D siap pakai untuk inference model ASR.
    """
    q = queue.Queue()

    def callback(indata, frames, time, status):
        """Callback ini dipanggil secara asinkron untuk setiap blok audio."""
        if status:
            print(status, file=sys.stderr)
        # Ambil channel pertama (mono) dan masukkan ke antrean
        q.put(indata[:, 0].copy())

    print("\n" + "="*40)
    print("🎤 [REKAMAN DIMULAI] - Silakan baca ayatnya.")
    print("   Tekan tombol ENTER di keyboard jika sudah selesai membaca...")
    print("="*40)
    
    # Membuka stream microphone dengan sample rate 16kHz (wajib untuk Wav2Vec2)
    with sd.InputStream(samplerate=sample_rate, channels=1, callback=callback):
        input() # Script akan berhenti di sini menahan stream sampai user menekan Enter
        
    print("🛑 [REKAMAN SELESAI] - Memproses suara ke teks...")
    
    # Menggabungkan semua potongan audio (chunk) dari queue menjadi satu array 1D
    audio_data = []
    while not q.empty():
        audio_data.append(q.get())
        
    if not audio_data:
        return np.array([])
        
    return np.concatenate(audio_data)