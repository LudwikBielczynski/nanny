"""PyAudio Example: Play a wave file."""

import sys

from nanny.microphone import Microphone
import wave

microphone = Microphone()

# Open stream
stream = pyaudio.open(format=get_format_from_width(wave_file.getsampwidth()),
                      channels=wave_file.getnchannels(),
                      rate=wave_file.getframerate(),
                      output=True)

# read data
data = wave_file.readframes(CHUNK)

# Play stream
while len(data) > 0:
    stream.write(data)
    data = wave_file.readframes(CHUNK)

# Stop stream
stream.stop_stream()
stream.close()

# Close PyAudio
pyaudio.terminate()
