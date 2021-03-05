import face_recognition as frec
from picamera import PiCamera
import numpy as np

from time import sleep as time_sleep, time as get_time
from os import sep as FILE_SEP

TARGET_IMG_PATH = "target.jpg"
OUT_IMG_PATH = "out" + FILE_SEP + "image.jpg"
OUT_READING_PATH = "out" + FILE_SEP + "reading.txt"

IMG_WIDTH = 1024
IMG_HEIGHT = 768
REQUIRES_MATCH = False
THRESHOLD = 0.7

def write_reading(s):
    with open(OUT_READING_PATH, 'w') as f:
        f.write(s+'\n')

if __name__ == "__main__":
    # Camera Initialization
    camera = PiCamera()
    camera.resolution = (IMG_WIDTH, IMG_HEIGHT)
    camera.start_preview()
    time_sleep(2) # warmup time (2s)

    # Load Target Image
    target_img = frec.load_image_file( TARGET_IMG_PATH )
    target_encs = frec.face_encodings( target_img )
    num_target_faces = len(target_encs)
    if REQUIRES_MATCH and num_target_faces != 1:
        print(f"Target image at \"{TARGET_IMG_PATH}\" needs to have 1 recognizable face.")
        print(f"Target image has {num_target_faces} recognizable faces.")
        exit()
    target_encoding = target_encs[0]

    while True: # sleeps for .2s at bottom of loop

        # Image Capture and Analysis
        camera.capture(OUT_IMG_PATH)
        time = get_time()
        img = frec.load_image_file(OUT_IMG_PATH)
        face_locs = frec.face_locations(img)
        num_faces = len(face_locs)
        print(f"Image taken; {num_faces} faces found")

        if num_faces > 0:
            # Compare Faces in Image to Target Image
            face_encs = frec.face_encodings(img, face_locs)
            min_dist = 10 # 10 should be big enough for min to always beat
            match_idx = -1
            for idx in range(len(face_encs)):
                enc_dist = np.linalg.norm(face_encs[idx]-target_encoding)
                if enc_dist < min_dist:
                    min_dist = enc_dist
                    match_idx = idx
            print(f"Closest Face Distance From Target: dist[{match_idx}]={min_dist}")

            # Write to Output Reading File
            if match_idx > -1:
                right, left = face_locs[match_idx][1], face_locs[match_idx][3]
                match = "N" if (REQUIRES_MATCH and min_dist < THRESHOLD) else "Y"
                location = (left+right)/IMG_WIDTH - 1 # ranges from -1 to 1 (but its hard to get to -1/1)
                # size = (right-left)/IMG_WIDTH
                write_reading(f"{time} {match} {location}")
            else:
                write_reading(f"{time} N 0")

        print("")
        time_sleep(.2)