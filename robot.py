import cv2
import os
import numpy as np

path = 'C:/Users/turki/Desktop/ROBOCUP/PYTHON/buffer'

class Robot():
    def __init__(self):
        self.picture = cv2.imread(os.path.join(path , 'picture.jpg'), cv2.IMREAD_GRAYSCALE)

    def SendPicture(self, picture):
        cv2.imwrite(os.path.join(path , 'picture.jpg'), picture)
    
    def SendData(self, data):
        with open(os.path.join(path, 'data.txt'), 'w') as f:
            f.write(str(data))

