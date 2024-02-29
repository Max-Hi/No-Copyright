import cv2
import numpy as np
import os

drive = "drive2"

files = os.listdir(f"../videos/{drive}")
filenumber = len(files)

for fileidx, filename in enumerate(files):
    id_ = filename.split(".",2)[0]
    if any([f"{id_}_{x}.jpg" not in os.listdir("../pictures") for x in [0,1,2,3,4,5,6,7]]):
        try:
            cap = cv2.VideoCapture(f"../videos/{drive}/{id_}.mp4")
            total_frames = cap.get(7)
            h, w = cap.get(4), cap.get(3)
            while w>800: # results in a width<400
                h/=2
                w/=2
            h = int(h)
            w = int(w)
            for idx,frame_number in enumerate( map(round, total_frames/np.array([25,20,10,6,5,4,3,2])) ):
                cap.set(1,frame_number)
                _, frame = cap.read()
                frame_resized = cv2.resize(frame, (w, h), interpolation = cv2.INTER_AREA)
                cv2.imwrite(f"../pictures/{id_}_{idx}.jpg", frame_resized)
            cap.release()
            cv2.destroyAllWindows()
        except Exception:
            print(idx,filename)
    if fileidx%200 == 0:
        print(f"{fileidx}/{filenumber}")
    
