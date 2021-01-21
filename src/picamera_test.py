from picamera import PiCamera
from time import time as get_time

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

# Camera warm-up time
start_time = get_time()
while get_time() < start_time + 2:
    pass
camera.capture('foo.jpg')