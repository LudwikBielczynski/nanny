import sys

from nanny.test.fixtures import camera, logger

def test_singleton(logger):
    '''Mock up the module import as it cannot be imported on anything else than raspberry pi.'''
    module = type(sys)('picamera')
    module.PiCamera = object
    sys.modules['picamera'] = module

    from nanny.camera import Camera

    camera_1 = Camera(logger)

    # Act
    camera_2 = Camera(logger)

    # Assert
    camera_1 == camera_2

def test_get_frame(camera):
    # Act
    frame = camera.get_frame()

    # Assert
    assert frame == b''
