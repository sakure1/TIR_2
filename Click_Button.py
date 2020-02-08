# -*- coding: utf-8 -*-
# coding: utf-8
import cv2 as cv
import os

# -----------------文件读取---------------
#读取三个温度点的图片
img = cv.imread("20191212TIR/20191212T1354-2.jpg")
# -----------------文件读取---------------




path = 'zuobiao.txt'
if os.path.exists(path):
    os.remove(path)
else:
    print('OK！')


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        f = open('zuobiao.txt', 'a')
        f.write(xy)
        f.write('\n')
        f.close()
        cv.circle(img, (x, y), 1, (255, 0, 0), thickness=-1)
        cv.putText(img, xy, (x, y), cv.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv.imshow("image", img)

def pick_up_point(img):
    cv.namedWindow("image")
    cv.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
    cv.imshow("image", img)
    while (True):
        try:
            cv.waitKey(100)
        except Exception:
            cv.destroyWindow("image")
            break

    cv.waitKey(0)
    cv.destroyAllWindow()

pick_up_point(img)
