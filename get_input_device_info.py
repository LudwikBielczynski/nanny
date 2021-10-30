from pyaudio import PyAudio

pyaudio = PyAudio()

default_host_api_info = pyaudio.get_default_host_api_info()
host_api_idx = default_host_api_info['index']
# print(default_host_api_info)

device_count = default_host_api_info.get('deviceCount')
rpi_simple_card_info = None
for device_idx in range(0, device_count):
    device_name = pyaudio.get_device_info_by_host_api_device_index(host_api_idx, device_idx) \
                               .get('name')
    if "snd_rpi_simple_card" in device_name:
        rpi_simple_card_info = pyaudio.get_device_info_by_host_api_device_index(host_api_idx,
                                                                                device_idx)

print(rpi_simple_card_info)
# print(pyaudio.get_default_input_device_info())
