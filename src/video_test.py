import face_recognition as frec
import cv2
import numpy as np
from datetime import datetime
from picamera import PiCamera
from time import time as get_time

CAMERA = PiCamera()
CAMERA.resolution = (1024, 768)
CAMERA.start_preview()

# Camera warm-up time
start_time = get_time()
while get_time() < start_time + 2: # 2 secs
    pass

FILE_SEP = "/"
TARGET_IMG_PATH = "target.jpg"
IMG_FOLDER = "img"
IMG_DIR = f".{FILE_SEP}{IMG_FOLDER}{FILE_SEP}"
IMG_FORMAT = "jpg"

THRESHOLD = 0.7

# returns path
def save_picture():
    dt = datetime.now()
    path = f"{IMG_DIR}{dt[0:4]+dt[5:7]+dt[8:10]+dt[11:13]+dt[14:16]+dt[17:19]}.{IMG_FORMAT}"
    print(path)
    CAMERA.capture(path)
    return path

'''
previously had processing minimizations with:
- quarter by quarter video resolution using cv2
- processing every other frame
'''

if __name__ == "__main__":
    face_locations = []
    face_encodings = []
    face_names = []

    # load actual target image
    target_img = frec.load_image_file( TARGET_IMG_PATH )
    print(len(target_img))
    target_encoding = frec.face_encodings( target_img )[0]
    print(len(target_encoding))
    print("target", target_encoding)

    print("before loop")
    last_time = get_time()
    while True:
        this_time = get_time()
        if this_time > last_time + 1:
            # take picture, save name
            print("before saving picture")
            path = save_picture()
            img = frec.load_image_file( path )
            print(img)

            # load encodings from face_recognition library
            face_locations = frec.face_locations( img )
            print(f"# face_locs={len(face_locations)}")
            encodings = frec.face_encodings( img, face_locations )
            print(f"# encs={len(encodings)}")

            # compare faces in picture to target image
            min_dist = THRESHOLD # need to beat threshold distance
            match_idx = -1
            for idx in range(len(encodings)):
                enc_dist = np.linalg.norm(encodings[idx]-target_encoding)
                if enc_dist < min_dist:
                    min_dist = enc_dist
                    match_idx = idx
            print(match_idx)
            
            # display
            for idx, (top, right, bottom, left) in enumerate(face_locations):
                print(f"loop {idx}")
                # face box
                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
                
                # text box
                label = "MATCH" if idx == match_idx else "UNKNOWN"
                cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(img, label, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow('Video', img)

            # press q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            last_time = this_time

    # close windows
    cv2.destroyAllWindows()
    