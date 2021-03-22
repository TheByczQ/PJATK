import numpy as np
import cv2
image = cv2.VideoCapture("C0800.MP4")
fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=70,detectShadows=False,history=100)
k=0
x1=None
y1=None
dron=False
while True:
    k+=1
    ret, frame=image.read()
    # znalezienie pozycji poczatkowej drona wzgledem wykrytego bialego/pomaranczowego koloru
    # po to by moc okreslic obszar sledzenia drona (250x250 px)
    # po to by ograniczyc margines bledu
    if dron==False:
        output1 = cv2.bitwise_and(frame, frame)
        # maski na wykrycie koloru pomaranczowego razem z zakresem barw RGB
        color = cv2.cvtColor(output1, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(color, np.array([96, 84, 170]), np.array([255, 255, 255]))
        mask2 = cv2.erode(mask, kernel=None, iterations=1)
        mask3 = cv2.dilate(mask2, kernel=None, dst=None, iterations=8)
        output = cv2.bitwise_and(frame,frame, mask=mask3)
        # maski na wykrycie kolor bialego razem z zakresem barw RGB
        mask11 = cv2.inRange(output1, np.array([195,195,200]), np.array([255, 255, 255]))
        mask21 = cv2.erode(mask11, kernel=None, iterations=1)
        mask31 = cv2.dilate(mask21, kernel=None, dst=None, iterations=8)
        output2 = cv2.bitwise_and(frame,frame, mask=mask31)
        # proba wykrycia koordynatow koloru bialego i stworzenie zmiennych x1 i y1
        # ktore pomoga w tworzeniu okna przesuwnego za dronem
        try:
            kupa1, kupa2 = cv2.findContours(mask31, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_SIMPLE)
            for i in kupa1:
                epsilon = 0.001 * cv2.arcLength(i, True)
                approx = cv2.approxPolyDP(i, epsilon, True)
                rect = cv2.minAreaRect(approx)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                if box[0][0] > 126 and box[0][1] > 126:
                    x1 = box[0][0] - 125
                    y1 = box[0][1] - 125
            cv2.drawContours(frame, [box], 0, (255, 255, 255), 2)
        except:
            print('Nie wykryto piłeczek1')
        # proba wykrycia koordynatow koloru pomaranczowego i stworzenie zmiennych x1 i y1
        # ktore pomoga w tworzeniu okna przesuwnego za dronem
        try:
            kupa1, kupa2 = cv2.findContours(mask3, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_SIMPLE)
            for i in kupa1:
                epsilon = 0.001 * cv2.arcLength(i, True)
                approx = cv2.approxPolyDP(i, epsilon, True)
                rect = cv2.minAreaRect(approx)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                if box[0][0] > 126 and box[0][1] > 126:
                    x1 = box[0][0] - 125
                    y1 = box[0][1] - 125
            cv2.drawContours(frame, [box], 0, (0, 0, 0), 2)
        except:
            print('Nie wykryto piłeczek2')
        # warunek stopu znajdywania drona na calym obrazku
        # przejscie do wykrywania go na ograniczonym obszarze
        if x1 is not None and y1 is not None:
            dron=True
    if ret==False:
        break
    # ograniczenie obszaru poszukiwan wzgledem wspolrzednych x1 i y1
    kozak = frame[y1:y1 + 250, x1:x1 + 250]
    fgmask=fgbg.apply(kozak)
    output1=cv2.bitwise_and(kozak,kozak,mask=fgmask)
    # maski na wykrycie koloru pomaranczowego razem z zakresem barw RGB
    color=cv2.cvtColor(output1,cv2.COLOR_RGB2HSV)
    mask=cv2.inRange(color,np.array([96,84,150]),np.array([255,255,255]))
    mask2 =cv2.erode(mask,kernel=None,iterations=1)
    mask3 = cv2.dilate(mask2,kernel=None,dst=None,iterations=8)
    output=cv2.bitwise_and(kozak,kozak,mask=mask3)
    # maski na wykrycie kolor bialego razem z zakresem barw RGB
    mask11=cv2.inRange(output1,np.array([195,195,200]),np.array([255,255,255]))
    mask21 =cv2.erode(mask11,kernel=None,iterations=1)
    mask31 = cv2.dilate(mask21,kernel=None,dst=None,iterations=8)
    output2=cv2.bitwise_and(kozak,kozak,mask=mask31)
    # bierzace wykrywanie koordynatow kolorow na wyznaczonym juz obszarze
    # wykrywanie jest co druga klatke aby ograniczyc wyskakiwanie spamu wykrytych obszarow
    kupa1, kupa2 = cv2.findContours(mask31, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_SIMPLE)

    for i in kupa1:
        epsilon = 0.001 * cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i, epsilon, True)
        rect = cv2.minAreaRect(approx)
        box2 = cv2.boxPoints(rect)
        box2 = np.int0(box2)
        # korygowanie wspolrzednych wektorem [x1,y1] ktorym wycinamy obszr poszukiwan
        for i in range(len(box2)):
            box2[i][0]+=x1
            box2[i][1]+=y1
        cv2.drawContours(frame, [box2], 0, (255,255,255), 2)
    # bierzace wykrywanie koordynatow kolorow na wyznaczonym juz obszarze
    # wykrywanie jest co druga klatke aby ograniczyc wyskakiwanie spamu wykrytych obszarow
    kupa1, kupa2 = cv2.findContours(mask3, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_SIMPLE)

    for i in kupa1:
        epsilon = 0.001 * cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i, epsilon, True)
        rect = cv2.minAreaRect(approx)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # korygowanie wspolrzednych wektorem [x1,y1] ktorym wycinamy obszr poszukiwan
        for i in range(len(box)):
            box[i][0] += x1
            box[i][1] += y1
        cv2.drawContours(frame, [box], 0, (0, 0, 0), 2)


    if box[0][0]>126and box[0][1]>126:
        x1=box[0][0]-125
        y1=box[0][1]-125
    elif box2[0][0]<box[0][0]:
        x1 = box2[0][0] - 125
        y1 = box2[0][1] - 125
    else:
        print(f"cos pojebales{k}")
    cv2.drawContours(frame, [np.array([[x1, y1+75], [x1, y1 + 200], [x1+300 , y1 + 200], [x1 + 300, y1+75]])], 0,
                     (0, 0, 255), 2)

    if cv2.waitKey(5) & 0xFF ==ord('q'):
        break
    cv2.imshow("frame",frame)
    cv2.imshow("ijfoia",output2)