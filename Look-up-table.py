# -*- coding: utf-8 -*-
import numpy as np
import math

def look_up_table():
    T_min = -25
    T_max = 35
    #    T_min = float(input('查找表中温度最小值：'))
    #    T_max = float(input('查找表中温度最大值：'))
    T = np.arange(T_min, T_max, 0.5)
    table = open('table.txt', 'w')
    ini_value = int(JF_3(T[0]+273.15))
    fnl_value = int(JF_3(T[-1]+273.15)) + 1
    for i in range(0, len(T)):
        FB = JF_3(T[i]+273.15)
        table.write(str(FB))
        table.write(' ')
        table.write(str(T[i]))
        table.write('\n')
    table.close()

def JF_3(T):
    f_function = np.loadtxt('热像仪宽波段响应函数.txt')
    len_1 = f_function.shape[0]
    sum = 0
    for i in range(len_1-1):
        L = Planck((f_function[i][0]+f_function[i+1][0])/2*pow(10,-6),T) * (f_function[i][1]+ f_function[i+1][1])* (f_function[i+1][0]-f_function[i][0])/2
        sum = sum + L
    return sum


def Planck(lamda, T):
    h = 6.626 * pow(10, -34)  # 普朗克常数
    c = 2.998 * pow(10, 8)  # 光速，单位：m
    k = 1.3806 * pow(10, -23)
    return (2 * h * c * c / pow(lamda, 5) * 1 / (math.exp(h * c / (k * T * lamda)) - 1) * pow(10,-6))


look_up_table()