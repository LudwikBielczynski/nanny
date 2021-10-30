"""PyAudio Example: Play a wave file."""

import sys

from pyaudio import PyAudio, get_format_from_width
import wave

CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wave_file = wave.open(sys.argv[1], 'rb')

# Instantiate PyAudio
pyaudio = PyAudio()

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
