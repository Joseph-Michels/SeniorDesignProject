import face_recognition as frec
import numpy as np
from pathlib import Path

if __name__ == "__main__":
    imgs = []
    encs = []
    for img_path in Path("img").iterdir():
        imgs.append( frec.load_image_file(img_path) )
        encs.append( frec.face_encodings(imgs[-1])[0] )
    imgs = np.array(imgs)
    encs = np.array(encs)

    print(imgs.shape)
    print(encs.shape)

    print("Distances")
    print(f"Obama 1 / Obama 2: {np.linalg.norm(encs[2] - encs[1])}")
    print(f"Obama 1 / Biden: {np.linalg.norm(encs[2] - encs[0])}")
    print(f"Obama 2 / Biden: {np.linalg.norm(encs[2] - encs[0])}")