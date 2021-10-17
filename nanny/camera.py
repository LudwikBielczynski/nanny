import io
import time
import threading

from picamera import PiCamera

class Camera:
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)


    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @staticmethod
    def _apply_settings(camera):
        camera.resolution = camera.MAX_RESOLUTION
        camera.hflip = True
        camera.vflip = True

        return camera

    @staticmethod
    def _warm_up(camera) -> None:
        camera.start_preview()
        time.sleep(2)

    @classmethod
    def _stream(cls, camera):
        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, 'jpeg',
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

    @classmethod
    def _thread(cls):
        with PiCamera() as camera:
            camera = cls._apply_settings(camera)
            cls._warm_up(camera)
            cls._stream(camera)

        cls.thread = None
