import numpy as np
import cv2
import glob
import pickle

"""
kalibracja kamery na podstawie zdjęć z nagrań kalibracyjnych
używana jest tablica kalibracyjna z szachownicą gdzie długość
jednej kratki to 251mm
"""

fname = glob.glob("Z:\BazaNexus\Praktykanci\K3\*.jpg") # wczytanie zdjęć we wskazanej ścieżce z końcówką .jpg
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001) # kryteria użyte w funkcji cornerSubPix
objp = np.zeros((6 * 9, 3), np.float32) # stworzenie macierzy z realnymi odległościami między kwadratami na szachownicy
objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
objp = objp * 25.1
objpoints = []
imgpoints = []
image_size = (1920, 1200) # zmienna z rozmiarem zdjęcia w pixelach
k = 0

for image in fname: # pętla po każdym zdjęciu we wskazanej ścieżce
    frame = cv2.imread(image) # wczytanie zdjęcia do postaci macierzy
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # przekształcenie zdjęcia z RGB do odcieni szarości

    """
    Funkcja findChessboardCorners wykrywa tablice kalibracyjną na zdjęciu, zwraca True/False w zależności czy znalazło tablice oraz koordynaty rogów tablicy.
    gray - zdjęcie w odcieniach szarości, 
    (9,6) - rozmiar tablicy kalibracyjnej """
    ret, corners = cv2.findChessboardCorners(gray, (9, 6))

    if not ret:
        print('Nie wykryto szachownicy.')

    if ret:
        objpoints.append(objp) # jeśli na danym zdjęciu wykryto tablice dodaję kolejne object pointy do listy
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria) # wyliczanie koordynatów rogów z sub pixelową dokładnością
        imgpoints.append(corners2) # do listy imgpoints dodawane są rogi tablicy, które wykryto na danym zdjęciu
        print(k) # wyświetla nr zdjecia
    k += 1

"""
Funkcja calibrateCamera znajduje wewnętrzne i zewnętrzne parametry kamery.
ret - błąd reprojekcji
mtx - macierz kamery
dist - parametry distorsji
rvecs - wektor rotacji
tvecs - wektor translacji """
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, image_size, None, None)

"""
zapisywanie potrzebnych wartości kalibracji kamery
do plików formatu pickle
potrzebne są potem do kalibracji stereo """
with open("k3\mret.pickle", "wb") as file:
    pickle.dump(ret, file)
with open("k3\mtxvideo.pickle", "wb") as file:
    pickle.dump(mtx, file)
with open("k3\distvideo.pickle", "wb") as file:
    pickle.dump(dist, file)
with open("k3/rvecs.pickle", "wb") as file:
    pickle.dump(rvecs, file)
with open("k3/tvecs.pickle", "wb") as file:
    pickle.dump(tvecs, file)
