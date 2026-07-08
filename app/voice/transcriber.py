from pathlib import Path
import warnings
import os

import whisper


class SpeechTranscriber:
    """
    Converts speech to text using OpenAI Whisper.
    """

    MODEL_NAME = "base"

    _shared_model = None

    def __init__(self):

        warnings.filterwarnings(
            "ignore",
            message="FP16 is not supported on CPU"
        )

        if SpeechTranscriber._shared_model is None:
            print("Loading Speech Engine...")
            SpeechTranscriber._shared_model = whisper.load_model(self.MODEL_NAME)
            print("[OK] Speech Engine Ready")

        self.model = SpeechTranscriber._shared_model

    def transcribe(self, audio_path: Path) -> str:

        if not os.path.exists(audio_path):
            print("[ERROR] Audio file not found.")
            return ""

        try:

            result = self.model.transcribe(
                str(audio_path),
                fp16=False,
                language="en"
            )

            text = result["text"].strip()

            # If the transcription contains no alphabetic characters, discard it as noise/hallucination
            if text and not any(c.isalpha() for c in text):
                text = ""

            # Filter out common Whisper static/silence hallucinations
            hallucinations = {
                "thank you", "thank you.", "thank you for watching", "thank you for watching.",
                "thanks for watching", "thanks for watching.", "thank you very much", "thank you very much.",
                "subtitles by amara.org", "subtitles by amara.org.", "subtitles", "subtitles.",
                "you", "go", "oh", "yeah", "so", "bye", "bye."
            }
            if text.lower().strip() in hallucinations:
                text = ""

            if text:
                print(f"You said : {text}")
            else:
                print("[WARNING] No speech detected.")

            return text

        except Exception as e:

            print(f"[ERROR] Whisper Error : {e}")

            return ""