# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt


def result_output(name,img):
    plt.figure()
    plt.imshow(img, cmap='rainbow')
    plt.colorbar()
    plt.savefig('%s.png'%(str(name)))
    plt.show()