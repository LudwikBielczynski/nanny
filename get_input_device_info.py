from pyaudio import PyAudio

pyaudio = PyAudio()

default_host_api_info = pyaudio.get_default_host_api_info()
host_api_idx = default_host_api_info['index']
# print(default_host_api_info)

device_count = default_host_api_info.get('deviceCount')
input_devices = []
for device_idx in range(0, device_count):
    max_input_channel = pyaudio.get_device_info_by_host_api_device_index(host_api_idx, device_idx) \
                               .get('maxInputChannels')
    if max_input_channel > 0:
        device = pyaudio.get_device_info_by_host_api_device_index(host_api_idx, device_idx)
        input_devices.append(device)

print(input_devices)
print(pyaudio.get_default_input_device_info())
