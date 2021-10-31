from typing import TYPE_CHECKING

from pyaudio import PyAudio, get_format_from_width, paInt16, paFloat32
import wave

if TYPE_CHECKING:
    from nanny.logger import Logger

CHUNK = 1024
FORMAT = paInt16
CHANNELS = 1 # pyaudio supports only 1-channel (mono) audio
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

class Microphone:
    def __init__(self, logger: 'Logger'):
        self.logger = logger

        self.pyaudio = PyAudio()
        self.device_name_partial = "snd_rpi_simple_card"
        self.device_info = self._get_device_info()
        self._rate = self.device_info["defaultSampleRate"]
        self._stream = None

    def _get_device_info(self):
        default_host_api_info = self.pyaudio.get_default_host_api_info()
        host_api_idx = default_host_api_info['index']
        # print(default_host_api_info)

        device_count = default_host_api_info.get('deviceCount')
        device_info = None
        for device_idx in range(0, device_count):
            device_name = self.pyaudio.get_device_info_by_host_api_device_index(host_api_idx, device_idx) \
                                      .get('name')
            if self.device_name_partial in device_name:
                device_info = self.pyaudio.get_device_info_by_host_api_device_index(
                    host_api_idx, device_idx)

        return device_info

    def stream(self):
        print(FORMAT, CHANNELS, self._rate, self.device_info["index"], CHUNK)
        stream = self.pyaudio.open(format=FORMAT,
                                   channels=CHANNELS,
                                   input=True,
                                   rate=self._rate,
                                   input_device_index=self.device_info["index"],
                                   frames_per_buffer=CHUNK,
                                #    stream_callback=callback
                                  )
        self.logger.info("Started stream")
        return stream

    def save_locally(self):
        stream = self.stream()

        frames = []
        for _ in range(0, int(self._rate / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        self.pyaudio.terminate()
        self.logger.info("Stopped stream")


        file_audio = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        file_audio.setnchannels(CHANNELS)
        file_audio.setsampwidth(self.pyaudio.get_sample_size(FORMAT))
        file_audio.setframerate(self._rate)
        file_audio.writeframes(b''.join(frames))
        file_audio.close()
        self.logger.info(f"Written file {file_audio}")
