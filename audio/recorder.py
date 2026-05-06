import numpy as np
import sounddevice as sd
from config.constants import SAMPLE_RATE
from utils.logger import get_logger

logger = get_logger(__name__)

class AudioRecorder:
    def __init__(self, callback):
        self.callback = callback
        self.stream = None

    def start(self):
        try:
            self.stream = sd.InputStream(
                samplerate=SAMPLE_RATE, 
                channels=1, 
                callback=self._audio_callback
            )
            self.stream.start()
            logger.info("Audio input stream started.")
        except Exception as e:
            logger.error(f"Could not start audio recording: {e}")

    def _audio_callback(self, indata, frames, time, status):
        if status:
            logger.warning(f"Audio stream status: {status}")
        self.callback(indata.copy())

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            logger.info("Audio input stream stopped.")
