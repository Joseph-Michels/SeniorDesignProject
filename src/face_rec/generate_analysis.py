from pathlib import Path
import numpy as np

IMG_FOLDER = Path("img\\lfw")
ENC_FOLDER = Path("enc")

def get_enc(path):
    with open(path, 'r') as rf:
        return np.array( [float(v) for v in rf.readline().split(' ')] )

if __name__ == "__main__":
    person_names = {} # key is name, value is (start_index, end_index) of the person's encodings in the array below
    encodings = []

    # load names and encodings
    N = 0
    for person_folder_path in ENC_FOLDER.iterdir():
        per_str = str(person_folder_path)
        name = per_str[ per_str.find('\\')+1 : ]
        start_i = N
        for enc_path in person_folder_path.iterdir():
            encodings.append( get_enc(enc_path) )
            N += 1
        person_names[name] = (start_i, N)
    print(f"Encodings and Names Loaded; N={N}")

    # generate distances lower left matrix (y>x to avoid repeats)
    distances = []
    for y in range(N):
        arr = []
        for x in range(0, y):
            arr.append( np.linalg.norm( encodings[y]-encodings[x] ) )
        distances.append(arr)
    print("Distances Calculated")
    
    # analyze
    with open("analysis.txt", 'w') as wf:
        for person_name, (start_i, end_i) in person_names.items():
            # within person
            within_min, within_max, within_total, within_n = -1, -1, 0, 0
            for y in range(start_i, end_i):
                for x in range(start_i, y):
                    dist = distances[y][x]
                    if within_min == -1 or dist < within_min:
                        within_min = dist
                    if within_max == -1 or dist > within_max:
                        within_max = dist
                    within_total += dist
                    within_n += 1
            within_avg = -1 if within_n == 0 else within_total/within_n

            # outside person
            outside_min, outside_max, outside_total, outside_n = -1, -1, 0, 0
            for y in range(start_i, end_i):
                for x in range(0, N):
                    if x < start_i or x >= end_i:
                        dist = distances[ max(y,x) ][ min(y,x) ]
                        if outside_min == -1 or dist < outside_min:
                            outside_min = dist
                        if outside_max == -1 or dist > outside_max:
                            outside_max = dist
                        outside_total += dist
                        outside_n += 1
            outside_avg = -1 if outside_n == 0 else outside_total/outside_n
            
            # write
            wf.write(f"{person_name}: within({within_min},{within_avg},{within_max}); outside({outside_min},{outside_avg},{outside_max})\n")
            