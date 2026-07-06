from pathlib import Path
import warnings
import os

import whisper


class SpeechTranscriber:
    """
    Converts speech to text using OpenAI Whisper.
    """

    MODEL_NAME = "base"

    def __init__(self):

        warnings.filterwarnings(
            "ignore",
            message="FP16 is not supported on CPU"
        )

        print("Loading Speech Engine...")

        self.model = whisper.load_model(self.MODEL_NAME)

        print("✅ Speech Engine Ready")

    def transcribe(self, audio_path: Path) -> str:

        if not os.path.exists(audio_path):
            print("❌ Audio file not found.")
            return ""

        try:

            result = self.model.transcribe(
                str(audio_path),
                fp16=False,
                language="en"
            )

            text = result["text"].strip()

            if text:
                print(f"You said : {text}")
            else:
                print("⚠ No speech detected.")

            return text

        except Exception as e:

            print(f"❌ Whisper Error : {e}")

            return ""