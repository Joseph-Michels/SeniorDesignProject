import face_recognition as frec
from pathlib import Path

IMG_FOLDER = Path("img") / "lfw"
ENC_FOLDER = Path("enc")

def get_enc_path_dir(img_path):
    s = str(img_path)
    return Path(s[ s.rfind('\\')+1 : s.rfind('_') ])


def get_enc_path_name(img_path):
    s = str(img_path)
    return Path(s[ s.rfind('\\')+1 : s.rfind('.') ] + '.txt')

if __name__ == "__main__":
    N = 0
    
    for person_folder_path in IMG_FOLDER.iterdir():
        if person_folder_path.is_dir():
            for img_path in person_folder_path.iterdir():
                enc_dir = ENC_FOLDER / get_enc_path_dir(img_path)
                if not enc_dir.exists():
                    enc_dir.mkdir()
                enc_path = enc_dir / get_enc_path_name(img_path)
                if not enc_path.exists():
                    multi_encs = frec.face_encodings( frec.load_image_file(img_path) )
                    if len(multi_encs) > 0:
                        enc = multi_encs[0]
                        with open( enc_dir / get_enc_path_name(img_path) , 'w') as wf:
                            wf.write(' '.join(str(v) for v in enc))
                        N += 1
