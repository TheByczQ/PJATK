import glob
import cv2
import numpy as np
fname= glob.glob("right\*.bmp")
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0), in this exercise they should be 100,200... etc
objp = np.zeros((7 * 10, 3), np.float32) #tworzenie tablicy dla object pointów o wielkośći wykrywanej tablicy
objp[:, :2] = np.mgrid[0:10, 0:7].T.reshape(-1, 2) #uzupełnianie jej przykładowymi parametrami
objp=objp*100 #skalowanie parametrów stukrotnie
# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space #pusta tablica do przechowywania objp
imgpoints = []  # 2d points in image plane of right camera #pusta tablica dla punktów naróżników lewej kamery
imgpoints2=[] # 2d points in image plane of left camera #pusta tablica dla punktów narożników prawej kamery
k=110 #iteracja obrazków od których zaczynamy sprawdzanie poszczególnych klatek prawej i lewej kamery
p=0
corners2OLD=[[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[0,0]]] #sztuczna tablica dla 1 iteracji sprawdzania warunków wyboru wartościowych klatek
przekatna=0
przekatna2=0
for image in fname: #pętla po wczytywanych klatkach
    k+=1
    print(k)
    img=cv2.imread(image) #wczytanie danej klatki prawej kamery
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #zmienianie barwy klatki na odcienie szarości dal usprawnienia prowadzonyhch obliczeń
    ret, corners=cv2.findChessboardCorners(gray, (10, 7), None) #szukanie narożników tablicy kalibracyjnej o danym rozmiarze 10:7
    if ret==True: #warunek znalezienia tablicy
        corners2 = cv2.cornerSubPix(gray, corners, (5,5), (-1, -1), criteria) #znalezienie narożników tablicy z subpixelową dokładnością
        xd=np.absolute(przekatna - (np.sqrt((corners2[0][0][0]-corners2[-1][0][0])**2)+np.sqrt((corners2[0][0][1]-corners2[-1][0][1])**2))) #warunek o roznicy dlugosci #1 przekątnej
        xd2=np.absolute(przekatna2 - (np.sqrt((corners2[9][0][0]-corners2[-10][0][0])**2+(corners2[9][0][1]-corners2[-10][0][1])**2))) #warunek o roznicy dlugosci #2 przekątnej
        # wartosc 15 dla warunkow jest wartoscia zeminna wg uznania
        if np.absolute(np.sqrt(corners2[0][0][0]**2+corners2[0][0][1]**2)-np.sqrt(corners2OLD[0][0][0]**2+corners2OLD[0][0][1]**2))>15 or xd>15 or xd2>15: #@warunek o zmianie lewego górnego pixela tablicy o jakąś wartość w dowolnym kierunku
            img2 = cv2.imread(f"left\img00{k}_l.bmp") #po spełnieniu warunku bierzemy pasujący iteracyjnie obrazek z lewej kamery
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) #skalujemy go na szaro
            ret2, corners3 = cv2.findChessboardCorners(gray2, (10, 7), None)
            if ret2==True:  #sprawdzanie czy tablica została wykryta, jeśli tak to dopiero zapisujemy wszystkie dane dla obu obrazków w 2 tablicach dla imagepointów przez zmienną dla narożników z subpixelową dokładnością
                corners2OLD=corners2
                ret2, corners3 = cv2.findChessboardCorners(gray2, (10, 7), None)
                corners4 = cv2.cornerSubPix(gray2, corners3, (5, 5), (-1, -1), criteria)
                imgpoints2.append(corners4)
                objpoints.append(objp)
                imgpoints.append(corners2)
                przekatna=np.sqrt((corners2OLD[0][0][0]-corners2OLD[-1][0][0])**2)+np.sqrt((corners2OLD[0][0][1]-corners2OLD[-1][0][1])**2)
                przekatna2=np.sqrt((corners2OLD[9][0][0]-corners2OLD[-10][0][0])**2+(corners2OLD[9][0][1]-corners2OLD[-10][0][1])**2)
                print(f"znalazlem{k}") #wypisanie która dokładnie klatka została znaleziona 
                p+=1
print(f"wzialem: {p} obrazkow, odrzucilem: {len(fname)-p}")
img=cv2.imread('img00111_r.bmp')
img_size = (img.shape[1], img.shape[0])
asd=np.array([[1200,0,1279/2],[0,1280,1023/2],[0.0,0.0,1.0]])
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size,distCoeffs=None,cameraMatrix=asd)
ret2, mtx2, dist2, rvecs2, tvecs2 = cv2.calibrateCamera(objpoints, imgpoints2, img_size,distCoeffs=None,cameraMatrix=asd)
print("blad:",ret)
dst = cv2.undistort(img, mtx, dist, None, mtx) #obrazek 111 jako przyklad usuniecia dystorsji



#zapisanie za pomocą pickle do plików do późniejszej analizy kalibracji kamer
import pickle
with open("IMAGEPOINTSRIGHT.pickle","wb") as file:
    pickle.dump(imgpoints,file)
with open("IMAGEPOINTSLEFT.pickle","wb") as file:
    pickle.dump(imgpoints2,file)
with open("OBJECTPOINTS.pickle", "wb") as file:
    pickle.dump(objpoints,file)
with open("cameramatrixright.pickle", "wb") as file:
    pickle.dump(mtx,file)
with open("cameramatrixleft.pickle", "wb") as file:
    pickle.dump(mtx2,file)
with open("disstleft.pickle", "wb") as file:
    pickle.dump(dist2,file)
with open("disstright.pickle", "wb") as file:
    pickle.dump(dist,file)


img=cv2.imread('img00111_r.bmp')
img_size = (img.shape[0], img.shape[1])
#użycie funkcji stereocalibrate z kolejnością wpisania parametrów #1 lewa kamera #2 prawa kamera
error,mtxx1,disst1,mtxx2,disst2,R,E,T,F=\
    cv2.stereoCalibrate(objpoints,imgpoints2,imgpoints,mtx2,dist2,mtx,dist,img_size,flags=cv2.CALIB_FIX_INTRINSIC+cv2.CALIB_USE_INTRINSIC_GUESS+cv2.CALIB_FIX_K1+cv2.CALIB_FIX_K2+cv2.CALIB_FIX_K3+cv2.CALIB_FIX_K4+cv2.CALIB_FIX_K5,criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 1*10**(-300)))


#zapisanie danych stereo kalibracji do późniejszej analizy parametrów czy program kamery dobrze się kalibrują
with open(f"error.pickle","wb") as file:
    pickle.dump(error,file)
with open(f"mtxx1.pickle","wb") as file:
    pickle.dump(mtxx1,file)
with open(f"mtxx2.pickle", "wb") as file:
    pickle.dump(mtxx2,file)
with open(f"disst1.pickle","wb") as file:
    pickle.dump(disst1,file)
with open(f"disst2.pickle","wb") as file:
    pickle.dump(disst2,file)
with open(f"R.pickle", "wb") as file:
    pickle.dump(R,file)
with open(f"E.pickle","wb") as file:
    pickle.dump(T,file)
with open(f"T.pickle","wb") as file:
    pickle.dump(E,file)
with open(f"F.pickle", "wb") as file:
    pickle.dump(F,file)
