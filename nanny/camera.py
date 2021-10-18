import io
import time
import threading
from typing import Optional

from picamera import PiCamera

class Camera:
    # current frame is stored here by any camera object
    frame = b''
    frame_change_time = 0.

    def __init__(self):
        self.thread = None

    def get_frame(self) -> bytes:
        Camera.frame_change_time = time.time()
        self._initialize()
        return self.frame

    def _initialize(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self._run_thread)
            self.thread.start()

            # wait until frames start to be available
            while self.frame == b'':
                time.sleep(0)

    def _run_thread(self) -> None:
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
        camera.start_preview()
        time.sleep(2)

    def _stream(self, camera: PiCamera) -> None:
        stream = io.BytesIO()
        while camera.capture_continuous(stream, 'jpeg',
                                        resize=(768, 576),
                                        use_video_port=True):
            # store frame
            stream.seek(0)
            Camera.frame = stream.read()

            # reset stream for next frame
            stream.seek(0)
            stream.truncate()

            # Stop the thread if in the last 10 seconds no clients for frames
            if time.time() - Camera.frame_change_time > 10:
                break
