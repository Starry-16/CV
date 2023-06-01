import cv2 as cv
import numpy as np

def Dark_Channel(image_min, r = 7):
    '''最小值滤波，滤波的半径由窗口大小决定'''
    return cv.erode(image_min, np.ones((2 * r + 1, 2 * r + 1))) 


def Guided_Filter(img, p, r, eps):  
    '''引导滤波'''
    # blur(src, dst, ksize, anchor, borderType)等价于boxFilter(src, dst,src.type(), anchor, true, borderType)
    mean_I = cv.blur(img, (r, r)) #I的均值平滑
    mean_p = cv.blur(p, (r, r)) #p的均值平滑

    mean_II = cv.blur(img * img, (r, r)) #I*I的均值平滑
    mean_Ip = cv.blur(img * p, (r, r)) #I*p的均值平滑

    var_I = mean_II - mean_I * mean_I #方差
    cov_Ip = mean_Ip - mean_I * mean_p #协方差

    a = cov_Ip / (var_I +eps) #相关因子a
    b = mean_p - a *mean_I #相关因子b

    mean_a = cv.blur(a, (r, r)) #对a进行均值平滑
    mean_b = cv.blur(b, (r, r)) #对b进行均值平滑

    q = mean_a * img + mean_b
    # print("q",q)
    return q

def get_A_t(Image, img_origin, V):
#输入：Image最小值图像，img_origion原图，w是t之前的修正参数，t0阈值，V导向滤波结果
#对于灰度图像：bright = R = G = B
#对于RGB图像，bright = (0.114 * B) + (0.587 * G) + (0.299 * R)
    rows, cols, channels = img_origin.shape
    size = rows * cols
    list = [0 for i in range(size)]
    m = 0
    for t in range(0, rows):
        for j in range(0, cols):
            list[m] = Image[t][j]
            m = m+1

    list.sort(reverse=True) #降序排序
    index =int(size * 0.001) #从暗通道中选取亮度最大的前0.1%
    Threshold = list[index+1] #阈值，后面要比这个大才行
    A = 0
    for i in range(0, rows):
        for j in range(0, cols):
            B = img_origin[i][j][0]
            G = img_origin[i][j][1]
            R = img_origin[i][j][2]
            bright = 0.114 * B + 0.587 * G + 0.299 * R
            if Image[i][j] > Threshold and bright > A:
                A = bright
    t = 1 - 0.95 * (V/A) #原文中w等于0.95，作者认为为了保持图像的真实感需要保留少量的“雾气”
    # t = np.maximum(t, 0.1) #把数组中小于某个值的数都设为0.1
    return A, t

def repair(Image, t, A, t0 = 0.1):
    rows, cols, channels = Image.shape
    J = np.zeros(Image.shape)
    for i in range(0, rows):
        for j in range(0, cols):
            for c in range(0, channels):
                t[i][j] = t[i][j] - 0.12 #调参感觉舒服多了
                J[i][j][c] = (Image[i][j][c]-A/255.0)/max(t[i][j],t0)+A/255.0
    return J

if __name__ == '__main__':
    img = cv.imread('./HazeRemoval/HazeRemoval/test.png')
    img_arr = np.array(img/255.0) #归一化
    img_min = np.min(img_arr, 2) #求出每个像素RGB分量中的最小值，存入一副和原始图像大小相同的灰度图中
    img_dark = Dark_Channel(img_min)
    A, t = get_A_t(img_dark, img, Guided_Filter(img_dark, img_min, r=81, eps=0.001))
    target = repair(img_arr, t, A)


    
    cv.namedWindow("Origin", 0)
    cv.resizeWindow("Origin", 350, 500)
    cv.imshow('Origin', img)
    cv.namedWindow("Target", 0)
    cv.resizeWindow("Target", 350, 500)
    cv.imshow('Target', target)
    
    cv.waitKey()