from nanny.logger import Logger
from nanny.microphone import Microphone

if __name__ == "__main__":
    logger = Logger()
    microphone = Microphone(logger)
    microphone.save_locally()

