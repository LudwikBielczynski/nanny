import io
import time
import threading
from typing import TYPE_CHECKING, Optional

from picamera import PiCamera

if TYPE_CHECKING:
    from nanny.logger import Logger

class Camera:
    frame = None # type: Optional[bytes]
    frame_change_time = 0.
    thread = None # type: Optional[threading.Thread]

    def __init__(self, logger: 'Logger'):
        self.logger = logger

    def initialize(self):
        if Camera.thread is None:
            self.logger.info('Initialized a new frame')
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            while self.frame is None:
                time.sleep(0)


    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        self.logger.info('Fetched frame')
        return self.frame

    @classmethod
    def _thread(cls):
        with PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break

        cls.thread = None
