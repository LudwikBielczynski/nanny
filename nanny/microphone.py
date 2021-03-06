from datetime import datetime
from os import EX_SOFTWARE
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from pyaudio import PyAudio, get_format_from_width, paInt32, paFloat32
import wave

from nanny.logger import LoggerSimple

if TYPE_CHECKING:
    from nanny.logger import Logger

CHUNK = 4096
FORMAT = paInt32
CHANNELS = 1  # pyaudio supports only 1-channel (mono) audio
OUTPUT_DIR = Path.home() / "audio"
TIME_RECORD_SECONDS = 60  # Default setting
KEEP_RECORDS_SECONDS = 600  # Last 10 minutes
WAVE_OUTPUT_FORMAT = "wav"


class Microphone:
    def __init__(self, logger: Optional['Logger'] = None):
        if logger is None:
            self.logger = LoggerSimple()
        else:
            self.logger = logger

        self.pyaudio = PyAudio()
        self.device_name_partial = "snd_rpi_simple_card"
        self.device_info = self._get_device_info()
        self._stream = None
        self.file_audio = None

        # Sample rate should be int
        self._rate = int(self.device_info["defaultSampleRate"])
        self._output_format = "%Y-%m-%d %H:%M:%S"
        if not OUTPUT_DIR.is_dir():
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def _get_device_info(self):
        default_host_api_info = self.pyaudio.get_default_host_api_info()
        host_api_idx = default_host_api_info['index']

        device_count = default_host_api_info.get('deviceCount')
        device_info = None
        for device_idx in range(0, device_count):
            device_name = self.pyaudio.get_device_info_by_host_api_device_index(host_api_idx, device_idx) \
                                      .get('name')
            if self.device_name_partial in device_name:
                device_info = self.pyaudio.get_device_info_by_host_api_device_index(
                    host_api_idx, device_idx)

        self.logger.info(f"Device selected: {device_info}")
        return device_info

    def _create_stream(self):
        stream = self.pyaudio.open(format=FORMAT,
                                   channels=CHANNELS,
                                   input=True,
                                   rate=self._rate,
                                   input_device_index=self.device_info["index"],
                                   frames_per_buffer=CHUNK,
                                   start=False,
                                   )
        self.logger.info("Created stream")
        return stream

    def _start(self, stream):
        stream.start_stream()
        self.logger.info("Started stream")

    def _stop(self, stream):
        stream.stop_stream()
        self.logger.info("Stopped stream")

    def terminate(self):
        self.pyaudio.terminate()
        self.logger.info("Terminating microphone")

    def _record(self, time_record_seconds, reuse=True):
        self.logger.info("Starting recording")

        if self._stream is None:
            self._stream = self._create_stream()
        self._start(self._stream)

        frames = []
        for _ in range(0, int(self._rate / CHUNK * time_record_seconds)):
            data = self._stream.read(CHUNK)
            frames.append(data)

        self._stop(self._stream)
        self.logger.info("Stopped recording")

        return frames

    def _save_audio(self, frames):
        now = datetime.now().strftime(self._output_format)
        file_name = f"{now}.{WAVE_OUTPUT_FORMAT}"
        with wave.open(str(OUTPUT_DIR / file_name), 'wb') as file_audio:
            file_audio.setnchannels(CHANNELS)
            file_audio.setsampwidth(self.pyaudio.get_sample_size(FORMAT))
            file_audio.setframerate(self._rate)
            file_audio.writeframes(b''.join(frames))
            file_audio.close()

        self.logger.info(f"Written file {file_name}")

    def _delete_old_audio(self):
        now = datetime.now()
        for path in OUTPUT_DIR.iterdir():
            time_recording = datetime.strptime(
                path.name.split(".")[0], self._output_format)
            seconds_from_now = (now - time_recording).seconds

            if seconds_from_now > KEEP_RECORDS_SECONDS:
                self.logger.info(f"Deleted file {path.name}")
                try:
                    path.unlink()
                except:
                    self.logger.warn(f"Path was missing: {path}")

    def save_locally(self, time_record_seconds=None):
        if time_record_seconds is None:
            time_record_seconds = TIME_RECORD_SECONDS
        frames = self._record(time_record_seconds)
        self._save_audio(frames)
        self._delete_old_audio()
