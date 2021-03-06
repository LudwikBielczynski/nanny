from nanny.logger import Logger
from nanny.microphone import Microphone

if __name__ == "__main__":
    # sys.settrace(trace)
    logger = Logger()
    microphone = Microphone(logger)

    while True:
        try:
            microphone.save_locally(time_record_seconds=30)

        except Exception as e:
            logger.info('Exception was raised')
            logger.error(e)
