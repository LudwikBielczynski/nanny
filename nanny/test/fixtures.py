import pytest

from nanny.logger import Logger

@pytest.fixture(scope='function', autouse=True)
def logger():
    return Logger()

@pytest.fixture(scope='function', autouse=True)
def camera(logger):
    '''
    Before importing Camera which depends on picamera module, raspberry pi environment needs to
    mocked as otherwise an error will occur on import.
    '''
    import sys

    class PiCameraMock:
        '''__enter__ and __exit__ needs to be implemented for the context manager'''
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            ...

        def close(self):
            ...

        def start_preview(self):
            ...

        def capture_continuous(self, output, *args, **kwargs):
            yield output

    module = type(sys)('picamera')
    module.PiCamera = PiCameraMock
    sys.modules['picamera'] = module

    from nanny.camera import Camera

    return Camera(logger)
