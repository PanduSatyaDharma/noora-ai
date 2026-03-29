from rapidfuzz import fuzz

class TextMatcher:
    @staticmethod
    def calculate_similarity(expected_text: str, transcribed_text: str) -> float:
        """
        Menghitung persentase kemiripan (0.0 - 100.0) antara dua string
        menggunakan Levenshtein Distance.
        """
        # fuzz.ratio mengembalikan nilai 0 sampai 100
        score = fuzz.ratio(expected_text, transcribed_text)
        return round(score, 2)