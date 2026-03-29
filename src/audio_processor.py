import librosa
import numpy as np

def load_and_resample_audio(file_path: str, target_sr: int = 16000) -> np.ndarray:
    """
    Memuat file audio .mp3 dan melakukan resampling ke target_sr (default 16kHz).
    Mengembalikan numpy array 1D.
    """
    try:
        # librosa otomatis melakukan convert ke mono dan resample jika sr ditentukan
        speech_array, _ = librosa.load(file_path, sr=target_sr, mono=True)
        return speech_array
    except Exception as e:
        raise RuntimeError(f"Gagal memproses audio {file_path}. Pastikan file ada dan valid. Error: {e}")