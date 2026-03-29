import json
from typing import List, Dict, Optional

class QuranTracker:
    def __init__(self, json_path: str):
        self.data: List[Dict] = self._load_json(json_path)
        self.current_surah_data: List[Dict] = []
        self.current_index: int = 0

    def _load_json(self, path: str) -> List[Dict]:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def set_surah(self, surah_number: int) -> bool:
        """
        Menyiapkan tracker untuk Surah tertentu.
        Mengembalikan True jika Surah ditemukan.
        """
        self.current_surah_data = [
            ayah for ayah in self.data if ayah.get("surah") == surah_number
        ]
        # Urutkan berdasarkan nomor ayat untuk memastikan sekuens benar
        self.current_surah_data.sort(key=lambda x: x.get("ayah", 0))
        self.current_index = 0
        
        return len(self.current_surah_data) > 0

    def get_current_ayah(self) -> Optional[Dict]:
        """
        Mengambil data ayat yang sedang ditunggu.
        """
        if self.current_index < len(self.current_surah_data):
            return self.current_surah_data[self.current_index]
        return None

    def advance(self) -> None:
        """Maju ke ayat berikutnya."""
        self.current_index += 1

    def is_finished(self) -> bool:
        return self.current_index >= len(self.current_surah_data)