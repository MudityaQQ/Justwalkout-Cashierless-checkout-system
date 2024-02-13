# import package
import cv2
import numpy as np
from PIL import Image
from pyzbar.pyzbar import decode

class ProductQrCode():
    

    def detectID(self):
        cap = cv2.VideoCapture(0)
        # cap = cv2.VideoCapture(2)
        # cap = cv2.VideoCapture(-1)

        cap.set(3,600)
        cap.set(4,480)
        while True:
            _,img = cap.read()
            code = decode(img)
            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')
                pts = np.array([barcode.polygon],np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(img,[pts],True,(0,255,0),5)
                pts2 = barcode.rect
                cv2.putText(img,myData,(pts2[0],pts2[1]-10),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2)
                
                # print(productIDList)

                # while myData:
                #     return myData
            # cv2.imshow("output", img)
                return myData
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()