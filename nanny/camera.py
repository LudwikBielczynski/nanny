import io
import time
import threading
from typing import TYPE_CHECKING, Optional

from picamera import PiCamera

from nanny.singleton import SingletonMeta

if TYPE_CHECKING:
    from nanny.logger import Logger

class Camera(metaclass=SingletonMeta):

    def __init__(self, logger: 'Logger'):
        self.frame = None # type: Optional[bytes]
        self.frame_change_time = 0.
        self.thread = None # type: Optional[threading.Thread]

        self.logger = logger

    def get_frame(self) -> Optional[bytes]:
        '''Keep only camera running when there are clients for frames'''
        self.frame_change_time = time.time()
        self._initialize()

        self.logger.info('Fetched frame')
        return self.frame

    def _initialize(self) -> None:
        '''
        Initialize only when there is nothing running on the thread. Otherwise use frames generated
        by another thread.
        '''
        if self.thread is None:
            self.logger.info('Initialized a new frame')
            self.thread = threading.Thread(target=self._run_thread)
            self.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

        else:
            self.logger.info('Using old thread')

    def _run_thread(self) -> None:
        '''
        As only one thread will be running this camera stream, there should not be any problems,
        with a race for the resources.
        '''
        with PiCamera() as camera:
            camera = self._apply_settings(camera)
            self._warm_up(camera)
            self._stream(camera)

        self.thread = None
        self.logger.info('Thread is closing')


    def _apply_settings(self, camera: PiCamera) -> PiCamera:
        if hasattr(camera, "MAX_RESOLUTION"):
            camera.resolution = camera.MAX_RESOLUTION
        camera.hflip = True
        camera.vflip = True

        self.logger.info('Applied camera settings')
        return camera

    def _warm_up(self, camera: PiCamera) -> None:
        '''A warm-up of the camera is needed for good quality.'''
        camera.start_preview()
        time.sleep(2)

        self.logger.info('Finished camera warm-up')

    def _stream(self, camera: PiCamera) -> None:
        stream = io.BytesIO()
        self.logger.info('Starting stream')
        while camera.capture_continuous(stream,
                                        format='jpeg',
                                        resize=(768, 576),
                                        use_video_port=True,
                                       ):
            # store frame
            stream.seek(0)
            self.frame = stream.read()

            self.logger.info('New frame')
            # reset stream for next frame
            stream.seek(0)
            stream.truncate()

            # Stop the thread if in the last 10 seconds no clients for frames
            if time.time() - self.frame_change_time > 10:
                self.logger.warn('Closing stream as there are no clients')
                break

        self.thread = None
