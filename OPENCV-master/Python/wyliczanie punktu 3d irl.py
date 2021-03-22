import numpy as np
import cv2
#macierz R|T
rotacjaitranslacja=np.array([[ 3.11664586e-02 ,-5.32364646e-04, -9.99514066e-01,1253.72176163],
 [ 1.54623293e-01 , 9.87964164e-01 , 4.29519045e-03,-32.04345308],
 [ 9.87481792e-01, -1.54682022e-01,  3.08736602e-02,974.11997952]])
#camera matrix
kamera1=np.array([[4.56094516e+03, 0.00000000e+00,8.29290621e+02],
 [0.00000000e+00, 4.28301037e+03, 6.30447644e+02],
 [0.00000000e+00 ,0.00000000e+00 ,1.00000000e+00]])
#punkt w pixelach na klatce video
x=np.array([[1146],
            [544],
            [1]])
x2=np.array([[1298],
                [663],
                [1]])
kamera2=np.array([[4.46479976e+03 ,0.00000000e+00, 1.03132561e+03],
 [0.00000000e+00, 4.47554747e+03, 6.85670509e+02],
 [0.00000000e+00 ,0.00000000e+00 ,1.00000000e+00]])
#macierze projekcji
projekcji2=kamera2@rotacjaitranslacja
projekcji=kamera1@rotacjaitranslacja
#odwrocone macierze projekcji
projekcjinv=cv2.invert(projekcji,flags=cv2.DECOMP_SVD)
projekcjinv2=cv2.invert(projekcji2,flags=cv2.DECOMP_SVD)
print(projekcjinv)
#wektor 4x1 z punktami i skalarem
punkt2=projekcjinv2[1]@x2
punkt=projekcjinv[1]@x
punkt2=punkt2/punkt2[3]
punkt=punkt/punkt[3]
print(punkt)
#wysrednienie 1 punktu z 2 kamer
punktsredni=(punkt+punkt2)/2
print(np.sqrt(punktsredni[0]**2+punktsredni[1]**2+punktsredni[2]**2))

