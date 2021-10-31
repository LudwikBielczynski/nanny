from nanny.logger import Logger
from nanny.microphone import Microphone

if __name__ == "__main__":
    logger = Logger('werkzeug')
    microphone = Microphone(logger)
    microphone.save_locally()

