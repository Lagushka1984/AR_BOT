import cv2
import os
import numpy as np
from mpu6050 import mpu6050

mpu = mpu6050(0x68)
path = 'C:/Users/turki/Desktop/ROBOCUP/PYTHON/buffer'

class Robot():
    def __init__(self):
        self.picture = cv2.imread(os.path.join(path , 'picture.jpg'), cv2.IMREAD_GRAYSCALE)

    def SendPicture(self, picture):
        cv2.imwrite(os.path.join(path , 'picture.jpg'), picture)
    
    def SendData(self, data):
        with open(os.path.join(path, 'data.txt'), 'w') as f:
            f.write(str(data))

    def GetGyro(self):
        gyro = []
        gyro_data = mpu.get_gyro_data()
        gyro.append(gyro_data['x'])
        gyro.append(gyro_data['y'])
        gyro.append(gyro_data['z'])
        return gyro

    def GetAccel(self):
        accel = []
        accel_data = mpu.get_accel_data()
        accel.append(accel_data['x'])
        accel.append(accel_data['y'])
        accel.append(accel_data['z'])
        return accel

    def GetTemp(self):
        temp = mpu.get_temp()
        return temp