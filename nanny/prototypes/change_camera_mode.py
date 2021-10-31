import picamera

camera = picamera.PiCamera()
camera.led = True
camera.capture('foo.jpg')
