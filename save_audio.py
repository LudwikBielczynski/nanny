from nanny.microphone import Microphone

if __name__ == "__main__":
    microphone = Microphone()

    while True:
        microphone.save_locally(time_record_seconds=30)
