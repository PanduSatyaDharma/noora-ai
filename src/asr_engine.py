import torch
import numpy as np
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

class QuranASR:
    def __init__(self, model_id: str = "jonatasgrosman/wav2vec2-large-xlsr-53-arabic"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[ASR] Memuat model {model_id} ke {self.device}...")
        
        self.processor = Wav2Vec2Processor.from_pretrained(model_id)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_id).to(self.device)
        self.target_sr = 16000
        print("[ASR] Model berhasil dimuat.")

    def transcribe(self, audio_array: np.ndarray) -> str:
        """
        Melakukan inferensi dari numpy array audio 16kHz menjadi teks Arab mentah.
        """
        # Prepare inputs
        inputs = self.processor(
            audio_array, 
            sampling_rate=self.target_sr, 
            return_tensors="pt", 
            padding=True
        )
        
        input_values = inputs.input_values.to(self.device)
        attention_mask = inputs.attention_mask.to(self.device) if "attention_mask" in inputs else None

        # Inference
        with torch.no_grad():
            logits = self.model(input_values, attention_mask=attention_mask).logits

        # Decode
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]
        
        return transcription