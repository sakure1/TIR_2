# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
import Radiometric_Calibration
import math
from scipy import integrate
import output
# LST = ε·f·B（T） + （1-ε）Ra⬇
# （LST - （1-ε）Ra⬇ ）/ε = f·B（T）  → T
# 建立f·B（T）与T的查找表



# -----------------文件读取---------------
img = cv.imread('20191212TIR/20191212T1354-1.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# -----------------文件读取---------------


# -----------------参数输入---------------
#ε = input('Emissivity:')
#Ra = input('Downward ATM radiation')
ε = 0.94             #通道发射率
Ra = 0.6029517        #下行辐射
# -----------------参数输入---------------



def R_T(gray):
    h = 6.626 * pow(10, -34)  # 普朗克常数
    c = 2.998 * pow(10, 8)  # 光速，单位：m
    k = 1.3806 * pow(10, -23)
    Height, Width = gray.shape
    L_Temperature = Radiometric_Calibration.New_T_image(gray)
    pixel = Height * Width
    LST = np.random.uniform(0, 1, pixel).reshape(Height, Width)
    subtracted = np.random.uniform(0, 1, pixel).reshape(Height, Width)
    JD = 0
    for i in range(Height):
        JD_1 = int(i/Height*100)
        if JD < JD_1:
            print('进度：%d%%'%(JD))
        JD = JD_1
        for j in range(Width):
            T = L_Temperature[i][j] + 273.15
#            print(L_Temperature[i][j])
            def Planck(lamda):
                return (2 * h * c * c / pow(lamda, 5) * 1 / (math.exp(h * c / (k * T * lamda)) - 1))
            B_T1, err =integrate.quad(Planck, 7.063609467*pow(10,-6), 12.5887574*pow(10,-6))
            fBT = (B_T1 * 0.9 - (1 - ε ) * Ra )/ε
            LST[i][j] = look_up(fBT)
    name = 'LST_result'
    output.result_output(name, LST)
    for i in range(Height):
        for j in range(Width):
            subtracted[i][j] = LST[i][j] - L_Temperature[i][j]
#    subtracted = cv.subtract(LST, L_Temperature, dtype = float)
    name_1 = 'difference'
    output.result_output(name_1, subtracted)
    return 0

def look_up(fBI):
    LUT = np.loadtxt('table.txt')
    height = LUT.shape[0]
    for i in range (height):
        if fBI > LUT[i][0]:
            continue
        else:
            break
    return LUT[i-1][1]+(fBI-LUT[i-1][0])/(LUT[i][0]-LUT[i-1][0])*(LUT[i][1]-LUT[i-1][1])




if __name__ == '__main__':
    # img = cv.imread('20191212TIR/20191212T1354-1.jpg')
    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    R_T(gray)




