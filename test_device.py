import sounddevice as sd
import soundfile as sf
import numpy as np

DEVICE = int(input("Enter device number: "))

print("Speak loudly...")

audio = sd.rec(
    int(5 * 16000),
    samplerate=16000,
    channels=1,
    dtype=np.int16,
    device=DEVICE,
)

sd.wait()

sf.write("test.wav", audio, 16000)

print("Saved.")

print("Maximum:", np.max(np.abs(audio)))