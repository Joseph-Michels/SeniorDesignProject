import face_recognition as frec
import cv2
import numpy as np
from subprocess import call
from datetime import datetime

FILE_SEP = "/"
TARGET_IMG_PATH = "target.jpg"
IMG_FOLDER = "img"
IMG_DIR = f".{FILE_SEP}{IMG_FOLDER}{FILE_SEP}"
IMG_FORMAT = "jpg"

RESOLUTION = "1280x720" # "640x480" previously worked
THRESHOLD = 0.7

# returns file name
def save_picture():
    dt = datetime.now()
    file_name = dt[0:4]+dt[5:7]+dt[8:10]+dt[11:13]+dt[14:16]+dt[17:19]
    call(["fswebcam", "-d", "/dev/video0", "-r", RESOLUTION, "--no-banner", f"{IMG_DIR}{file_name}.{IMG_FORMAT}"]) 
    return file_name

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
    target_encoding = frec.face_encodings( target_img )[0]

    while True:
        # take picture, save name
        file_name = save_picture()
        img = frec.load_image_file( file_name )

        # load encodings from face_recognition library
        face_locations = frec.face_locations( img )
        encodings = frec.face_encodings( img, face_locations )

        # compare faces in picture to target image
        min_dist = THRESHOLD # need to beat threshold distance
        match_idx = -1
        for idx in range(len(encodings)):
            enc_dist = np.linalg.norm(encodings[idx]-target_encoding)
            if enc_dist < min_dist:
                min_dist = enc_dist
                match_idx = idx
        
        # display
        for idx, (top, right, bottom, left) in enumerate(face_locations):
            # face box
            cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
            
            # text box
            label = "MATCH" if idx == match_idx else "UNKNOWN"
            cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        # press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # close windows
    cv2.destroyAllWindows()
    