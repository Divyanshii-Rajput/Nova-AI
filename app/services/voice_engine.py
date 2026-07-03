from app.audio.recorder import AudioRecorder
from app.voice.transcriber import SpeechTranscriber


class VoiceEngine:
    """
    Handles the complete voice pipeline.

    Voice
        ↓
    Recorder
        ↓
    Whisper
        ↓
    Text
    """

    def __init__(self):

        self.recorder = AudioRecorder()
        self.transcriber = SpeechTranscriber()

    def listen(self):

        audio_path = self.recorder.record()

        text = self.transcriber.transcribe(audio_path)

        return text