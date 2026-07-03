from pathlib import Path

import sounddevice as sd
import soundfile as sf


class AudioRecorder:
    """
    Records audio from the default microphone.
    """

    SAMPLE_RATE = 16000
    CHANNELS = 1

    # Device 1 works correctly on your laptop.
    DEVICE = 1

    OUTPUT_PATH = Path("assets/audio/input.wav")

    def record(self, duration: int = 6) -> Path:

        print("\n🎤 Speak after the countdown...\n")

        for i in range(3, 0, -1):
            print(f"{i}...")
            sd.sleep(1000)

        print("🎙️ Recording...")

        audio = sd.rec(
            int(duration * self.SAMPLE_RATE),
            samplerate=self.SAMPLE_RATE,
            channels=self.CHANNELS,
            dtype="int16",
            device=self.DEVICE,
        )

        sd.wait()

        sf.write(
            self.OUTPUT_PATH,
            audio,
            self.SAMPLE_RATE,
        )

        print("✅ Audio Saved")

        return self.OUTPUT_PATH