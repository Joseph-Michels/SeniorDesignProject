import face_recognition as frec
import numpy as np
from pathlib import Path

if __name__ == "__main__":
    names = []
    imgs = []
    encs = []
    N = 0
    
    for img_path in Path("img").iterdir():
        s = str(img_path)
        names.append( s[s.find('\\')+1:s.find('.')] )
        imgs.append( frec.load_image_file(img_path) )
        encs.append( frec.face_encodings(imgs[-1])[0] )
        N += 1

    encs = np.array(encs)

    print(f"Each encoding has {encs.shape[1]} values")

    print("Distances:")
    for i in range(N):
        for j in range(i):
            print(f"  {names[j]} to {names[i]}: {np.linalg.norm(encs[j]-encs[i])}")