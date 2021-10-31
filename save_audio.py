from nanny.logger import LoggerSimple
from nanny.microphone import Microphone

if __name__ == "__main__":
    logger = LoggerSimple()
    microphone = Microphone()

    while True:
        try:
            microphone.save_locally(time_record_seconds=30)

        except Exception as e:
            logger.info('Exception was raised')
            logger.error(e)
