from imutils import face_utils, translate, resize
import dlib
import cv2
import numpy as np
"""
znajdywanie i wyświetlanie punktów szczególnych twarzy z video na podstawie
biblioteki opnecv oraz dlib
"""
p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)
camera = cv2.VideoCapture("Z:\BazaNexus\Praktykanci\P3.avi")
while True:
    _, image = camera.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    dist=np.array([[-4.31349472e-01 , 2.83291049e+01 ,-2.90680923e-03 , 1.45047909e-03,-8.00154071e+02]])
    mtx=np.array([[4.35910328e+03, 0.00000000e+00 ,1.05139738e+03],[0.00000000e+00,4.37245777e+03, 6.24011532e+02],[0.00000000e+00 ,0.00000000e+00, 1.00000000e+00]])
    gray=cv2.undistort(gray,mtx,dist)
    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        """
        punkty szczególne twarzy są przechowywane w zmiennej shape
        """
        for point in shape:
            cv2.circle(image, tuple(point), 3, (0, 255, 0), -1)
    cv2.imshow("image",image)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
camera.release()
