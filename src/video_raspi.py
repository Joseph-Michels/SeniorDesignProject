import face_recognition as frec
import dlib
import cv2
import numpy as np
from datetime import datetime
from picamera import PiCamera
from time import time as get_time

FONT = cv2.FONT_HERSHEY_DUPLEX
FILE_SEP = "/"
TARGET_IMG_PATH = "target.jpg"
IMG_FOLDER = "img"
OUT_PREFIX = "out_"
IMG_DIR = f"{IMG_FOLDER}{FILE_SEP}" # f".{FILE_SEP}{IMG_FOLDER}{FILE_SEP}"
IMG_FORMAT = "jpg"

THRESHOLD = 0.7

CAMERA = PiCamera()
CAMERA.resolution = (1024, 768)
CAMERA.start_preview()

FACE_DETECTOR = dlib.get_frontal_face_detector()

# returns path
def save_picture():
    dt = str(datetime.now())
    path = f"{IMG_DIR}{dt[0:4]+dt[5:7]+dt[8:10]+dt[11:13]+dt[14:16]+dt[17:19]}.{IMG_FORMAT}"
    CAMERA.capture(path)
    print(path)
    return path

'''
previously had processing minimizations with:
- quarter by quarter video resolution using cv2
- processing every other frame
'''

if __name__ == "__main__":
    # camera warm-up time
    start_time = get_time()
    while get_time() < start_time + 2: # 2 secs
        pass

    face_locations = []
    face_encodings = []
    face_names = []

    # load actual target image
    target_img = frec.load_image_file( TARGET_IMG_PATH )

    target_encs = frec.face_encodings( target_img )

    if len(target_encs) == 1:
        target_encoding = target_encs[0]
        print(f"target encoding has length {len(target_encoding)}")

        print("before loop")
        last_time = get_time()
        while True:
            this_time = get_time()
            if this_time > last_time + 1:
                # take picture, save name
                print("\nsaving picture to ", end='')
                path = save_picture()
                img = frec.load_image_file( path )

                # load encodings from face_recognition library
                face_locations = frec.face_locations( img )
                encodings = frec.face_encodings( img, face_locations )
                print(f"len = {len(face_locations)}, {len(encodings)}")

                # compare faces in picture to target image
                min_dist = THRESHOLD # need to beat threshold distance
                match_idx = -1
                for idx in range(len(encodings)):
                    enc_dist = np.linalg.norm(encodings[idx]-target_encoding)
                    print(f"\tdist[{idx}]={enc_dist}")
                    if enc_dist < min_dist:
                        min_dist = enc_dist
                        match_idx = idx
                print(f" match_idx {match_idx}")
                
                # boxes
                for idx, (top, right, bottom, left) in enumerate(face_locations):
                    # face box
                    img = cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
                    
                    # text box
                    label = "MATCH" if idx == match_idx else "UNKNOWN"
                    img = cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    img = cv2.putText(img, label, (left + 6, bottom - 6), FONT, 1.0, (255, 255, 255), 1)

                # save image
                cv2.imwrite(OUT_PREFIX+path, img)

                # press q to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                last_time = this_time

        # close windows
        cv2.destroyAllWindows()
    else:
        print(f"target image has {len(target_encs)} faces")
    