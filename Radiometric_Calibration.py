# -*- coding: utf-8 -*-
import cv2 as cv

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import output







def offset_gain(gray):
    Height, width = gray.shape
    zuobiao_file = open('zuobiao.txt', 'r')
    data = zuobiao_file.read()
    zuobiao_file.close()
    number = []
    points = []
    for i in data:
        if i.isdigit():
            points.append(i)
        if i == ',':
            number.append(''.join(points))
            points.clear()
        if i.isspace():
            number.append(''.join(points))
            points.clear()
    x = np.array(number)
    n = int(len(x) / 2)
    x = x.reshape((n, 2))
    DN = np.array([0, 0, 0, 0, 0])
    for i in range(n):
        h = int(x[i][0])
        d = int(x[i][1])
        DN[i] = gray[d][h]
    DN[3] = min_DN_value(gray)
    DN[4] = max_DN_value(gray)
    T = input_Temperature()

    offset, gain = optimize.curve_fit(f_1, DN, T)[0]
    return offset, gain



def input_Temperature():
    Temperature = np.array([0.0, 2.0, -2.4, -8.5, 7.2])
    # print('请依次输入点的温度值与最小最大温度值：')
    # for i in range(5):
    #     if i == 3:
    #         T = input('最小温度为：')
    #         Temperature[i] = T
    #     elif i == 4:
    #         T = input('最大温度为：')
    #         Temperature[i] = T
    #     else:
    #         T = input('第%d个点温度：' % (i + 1))
    #         Temperature[i] = T
    return Temperature


def f_1(x,offset, gain):
    return offset * x + gain


def New_T_image(gray_image):
    offset, gain = offset_gain(gray_image)
    print("定标方程为")
    if gain< 0 :
        print('          T_img = %f * DN %f' %(offset,gain))
    elif gain==0:
        print('          T_img = %f * DN ' %offset)
    else:
        print('          T_img = %f * DN + %f' %(offset,gain))
    Height, width = gray_image.shape
    A = Height * width
    N_image = np.random.uniform(0,1,A).reshape(Height,width)
    for a in range(Height):
        for b in range(width):
            N_image[a][b] = float((offset * gray_image[a][b] + gain ))
    name = 'LW_result'
    output.result_output(name, N_image)
    return N_image

def min_DN_value(image):
    Height, width, image_gray = gray(image)
    DN_min_value = image_gray[0][0]
    for i in range(Height):
        for j in range(width):
            if image_gray[i][j] > DN_min_value:
                continue
            else:
                DN_min_value = image_gray[i][j]
    return DN_min_value

def max_DN_value(image):
    Height, width, image_gray = gray(image)
    DN_max_value = image_gray[0][0]
    for i in range(Height):
        for j in range(width):
            if image_gray[i][j] < DN_max_value:
                continue;
            else:
                DN_max_value = image_gray[i][j]
   # print(DN_max_value)
    return DN_max_value

def gray(image):
    Height = image.shape[0]
    width = image.shape[1]
    index = is_color_image(image)
    if index == 1:
        return Height, width, image
    else:
        image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        print(image_gray.shape[0])
        return Height, width, image_gray

#判断是否为灰度图像：范围值1为灰度  0为彩色
def is_color_image(im):
    pix=cv.cvtColor(im, cv.COLOR_GRAY2BGR)
    height=im.shape[0]
    width=im.shape[1]
    for x in range(width):
        for y in range(height):
            r=int(pix[y][x][0])
            g=int(pix[y][x][1])
            b=int(pix[y][x][2])
            if (r==g) and (g==b):
                pass
            else:
                return 0
    return 1


# img_2 = cv.imread('20191212TIR/20191212T1354-1.jpg')
# gray_2 = cv.cvtColor(img_2, cv.COLOR_BGR2GRAY)
# a = New_T_image(gray_2)
