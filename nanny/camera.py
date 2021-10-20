import io
import time
import threading
from typing import Optional

from picamera import PiCamera

from nanny.singleton import SingletonMeta

class Camera(metaclass=SingletonMeta):
    def __init__(self):
        self.frame = b''
        self.frame_change_time = 0.
        self.thread = None

    def get_frame(self) -> bytes:
        '''Keep only camera running when there are clients for frames'''
        self.frame_change_time = time.time()
        self._initialize()
        return self.frame

    def _initialize(self):
        '''
        Initialize only when there is nothing running on the thread. Otherwise use frames generated
        by another thread.
        '''
        if self.thread is None:
            self.thread = threading.Thread(target=self._run_thread)
            self.thread.start()

            # wait until frames start to be available
            while self.frame == b'':
                time.sleep(0)

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

    @staticmethod
    def _apply_settings(camera: PiCamera) -> PiCamera:
        camera.resolution = camera.MAX_RESOLUTION
        camera.hflip = True
        camera.vflip = True

        return camera

    @staticmethod
    def _warm_up(camera: PiCamera) -> None:
        '''A warm-up of the camera is needed for good quality.'''
        camera.start_preview()
        time.sleep(2)

    def _stream(self, camera: PiCamera) -> None:
        stream = io.BytesIO()
        while camera.capture_continuous(stream, 'jpeg',
                                        resize=(768, 576),
                                        use_video_port=True):
            # store frame
            stream.seek(0)
            self.frame = stream.read()

            # reset stream for next frame
            stream.seek(0)
            stream.truncate()

            # Stop the thread if in the last 10 seconds no clients for frames
            if time.time() - self.frame_change_time > 10:
                break
