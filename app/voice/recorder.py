from pathlib import Path

import sounddevice as sd
import soundfile as sf


class AudioRecorder:
    """
    Records audio from the microphone and saves it as a WAV file.
    """

    SAMPLE_RATE = 16000
    CHANNELS = 1
    DEVICE = 2                     # Microphone Array (change later if needed)

    OUTPUT_PATH = Path("assets/audio/input.wav")

    def record(self, duration: int = 5) -> Path:

        print("\n🎤 Speak now...\n")

        audio = sd.rec(
            int(duration * self.SAMPLE_RATE),
            samplerate=self.SAMPLE_RATE,
            channels=self.CHANNELS,
            dtype="int16",
            device=self.DEVICE
        )

        sd.wait()

        sf.write(
            self.OUTPUT_PATH,
            audio,
            self.SAMPLE_RATE
        )

        print("✅ Audio Saved")

        return self.OUTPUT_PATH