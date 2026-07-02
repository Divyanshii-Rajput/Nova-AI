from faster_whisper import WhisperModel


class SpeechTranscriber:
    """
    Converts speech into text using Faster Whisper.
    """

    def __init__(self):

        print("Loading Whisper model...")

        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8",
        )

        print("Whisper Loaded!")

    def transcribe(self, audio_path):

        segments, info = self.model.transcribe(
            audio_path,
            language="en",
            beam_size=5,
            vad_filter=True,
        )

        text = " ".join(segment.text.strip() for segment in segments)

        return text.strip()