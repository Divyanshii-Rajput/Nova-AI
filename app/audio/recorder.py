from pathlib import Path
import logging
import sounddevice as sd
import soundfile as sf
import numpy as np

logger = logging.getLogger(__name__)


class AudioRecorder:
    """
    Records audio from the default microphone using dynamic silence detection.
    """

    SAMPLE_RATE = 16000
    CHANNELS = 1

    # Device 1 works correctly on your laptop.
    DEVICE = 1

    OUTPUT_PATH = Path("assets/audio/input.wav")

    def record(self, duration: int = 10) -> Path:
        """
        Record audio dynamically. Starts recording immediately and stops
        when the user stops speaking (silence detected) or max duration is reached.
        """
        # Ensure the parent directory exists
        self.OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

        chunk_duration = 0.1  # 100ms chunks
        chunk_samples = int(self.SAMPLE_RATE * chunk_duration)

        logger.info("Starting recording...")
        recorded_chunks = []

        try:
            with sd.InputStream(
                samplerate=self.SAMPLE_RATE,
                channels=self.CHANNELS,
                dtype="int16",
                device=self.DEVICE,
            ) as stream:

                # Calibrate ambient noise threshold using first 2 chunks (0.2s)
                calib_chunks = []
                for _ in range(2):
                    chunk, _ = stream.read(chunk_samples)
                    calib_chunks.append(chunk)
                    recorded_chunks.append(chunk)

                calib_data = np.concatenate(calib_chunks)
                ambient_rms = np.sqrt(np.mean(calib_data.astype(np.float32) ** 2))

                # Dynamic threshold: 3.5x ambient noise, at least 80.0
                threshold = max(ambient_rms * 3.5, 80.0)
                logger.info("Ambient RMS: %.2f, Set Threshold: %.2f", ambient_rms, threshold)

                speech_detected = False
                silence_chunks_limit = int(1.5 / chunk_duration)  # 1.5s of silence to stop
                silence_counter = 0
                max_chunks = int(duration / chunk_duration)
                chunks_recorded = 2

                while chunks_recorded < max_chunks:
                    chunk, _ = stream.read(chunk_samples)
                    recorded_chunks.append(chunk)
                    chunks_recorded += 1

                    rms = np.sqrt(np.mean(chunk.astype(np.float32) ** 2))

                    if not speech_detected:
                        # Wait for speech to start
                        if rms > threshold:
                            speech_detected = True
                            logger.info("Speech detected, recording...")
                        elif chunks_recorded * chunk_duration > 4.0:
                            # Timeout: no speech detected in 4 seconds
                            logger.info("No speech detected (timeout).")
                            break
                    else:
                        # Speech is in progress; monitor for silence
                        if rms < threshold:
                            silence_counter += 1
                            if silence_counter >= silence_chunks_limit:
                                logger.info("Silence detected. Stopping recording.")
                                break
                        else:
                            silence_counter = 0

        except Exception as e:
            logger.exception("Error during audio recording stream: %s", e)
            raise

        if recorded_chunks:
            audio = np.concatenate(recorded_chunks)
        else:
            audio = np.zeros((chunk_samples,), dtype="int16")

        sf.write(
            self.OUTPUT_PATH,
            audio,
            self.SAMPLE_RATE,
        )

        logger.info("Audio saved to %s", self.OUTPUT_PATH)
        return self.OUTPUT_PATH