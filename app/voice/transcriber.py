from faster_whisper import WhisperModel


class SpeechTranscriber:
    """
    Converts speech to text using Faster Whisper.
    """

    def __init__(self):

        print("Loading Whisper model...")

        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

        print("Whisper Loaded!")

    def transcribe(self, audio_path):

        segments, info = self.model.transcribe(audio_path)

        text = ""

        for segment in segments:
            text += segment.text + " "

        return text.strip()