import logging
import sys
from typing import Optional

from nanny.singleton import SingletonMeta

class Logger(metaclass=SingletonMeta):

    def __init__(self, logger_name: Optional[str] = None) -> None:
        if logger_name is None:
            logger_name = __name__
        self.logger = logging.getLogger(logger_name)
        logs_format = ('%(asctime)s.%(msecs).0f - %(levelname)s - PID:%(process)d ' \
                       '{%(name)s.%(funcName)s:%(lineno)d} %(message)s'
                      )
        formatter = logging.Formatter(fmt=logs_format, datefmt="%Y-%m-%d %H:%M:%S")

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(stream_handler)

        self.info('Try the newly created logger')

    def info(self, *args, **kwargs):
        return self.logger.info(*args, **kwargs)


    def debug(self, *args, **kwargs):
        return self.logger.debug(*args, **kwargs)

    def warn(self, *args, **kwargs):
        return self.logger.warn(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self.logger.error(*args, **kwargs)

