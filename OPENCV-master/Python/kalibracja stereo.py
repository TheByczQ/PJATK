
"""
wczytywanie danych potrzebnych do stereo kalibracji dwóch kamer
z plików formatu pickle

"""

import pickle
with open ("k2/objectpointsk1.pickle","rb") as file:
    objectpoints=pickle.load(file)
with open ("k3/imagepoints.pickle","rb") as file:
    imagepoints1=pickle.load(file)
with open ("k2/imagepoints.pickle","rb") as file:
    imagepoints2=pickle.load(file)
with open ("k3/mtxvideo.pickle","rb") as file:
    cameramatrix1=pickle.load(file)
with open ("k2/mtxvideo.pickle","rb") as file:
    cameramatrix2=pickle.load(file)
with open ("k3/distvideo.pickle","rb") as file:
    dist1=pickle.load(file)
with open ("k2/distvideo.pickle","rb") as file:
    dist2=pickle.load(file)

"""
stereo kalibracja dwóch kamer z użyciem flag zamrażających
skalibrowane już macierze kamer by zapobiec błędnej kalibracji
"""
import cv2
img_size=(1920,1200)
error,mtxx1,disst1,mtxx2,disst2,R,T,E,F=\
    cv2.stereoCalibrate(objectpoints,imagepoints1,imagepoints2,cameramatrix1,dist1,cameramatrix2,dist2,img_size,flags=cv2.CALIB_FIX_INTRINSIC+cv2.CALIB_USE_INTRINSIC_GUESS+cv2.CALIB_FIX_K1+cv2.CALIB_FIX_K2+cv2.CALIB_FIX_K3+cv2.CALIB_FIX_K4+cv2.CALIB_FIX_K5,criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 1*10**(-300)))
"""

error - blad reprojekcji stereo kalibracji
mtxx1 - macierz 1. wprowadzonej kamery
disst1 - parametry dystorsji 1. wprowadzonej kamery
mtxx2 - macierz 2. wprowadzonej kamery
disst2 - parametry dystorsji 2. wprowadzonej kamery
R - macierz rotacji kamery 2 względem kamery 1
T - wektor translacji kamery 2 względem kamery 1
F - macierz fundamentalna
E - essential matrix

"""
with open(f"stereok2k3/error.pickle","wb") as file:
    pickle.dump(error,file)
with open(f"stereok2k3/mtxx1.pickle","wb") as file:
    pickle.dump(mtxx1,file)
with open(f"stereok2k3/mtxx2.pickle", "wb") as file:
    pickle.dump(mtxx2,file)
with open(f"stereok2k3/disst1.pickle","wb") as file:
    pickle.dump(disst1,file)
with open(f"stereok2k3/disst2.pickle","wb") as file:
    pickle.dump(disst2,file)
with open(f"stereok2k3/R.pickle", "wb") as file:
    pickle.dump(R,file)
with open(f"stereok2k3/E.pickle","wb") as file:
    pickle.dump(T,file)
with open(f"stereok2k3/T.pickle","wb") as file:
    pickle.dump(E,file)
with open(f"stereok2k3/F.pickle", "wb") as file:
    pickle.dump(F,file)