# -*- coding: utf-8 -*-  

# Birdy 17/11/27
import os
import PIL.Image as Image

def difference(hist1,hist2):
    sum1 = 0
    for i in range(len(hist1)):
       if (hist1[i] == hist2[i]):
          sum1 += 1
       else:
           sum1 += 1 - float(abs(hist1[i] - hist2[i]))/ max(hist1[i], hist2[i])
    return sum1/len(hist1)

def similary_calculate(path1 , path2 , mode):
    if(mode == 3):
        img1 = Image.open(path1).resize((8,8)).convert('1')  
        img2 = Image.open(path2).resize((8,8)).convert('1')
        hist1 = list(img1.getdata())
        hist2 = list(img2.getdata())
        return difference(hist1, hist2)

    # 预处理
    img1 = Image.open(path1).resize((256,256)).convert('RGB')  
    img2 = Image.open(path2).resize((256,256)).convert('RGB')
    if(mode == 1):
        return difference(img1.histogram(), img2.histogram())
    if(mode == 2):
        sum = 0;
        for i in range(4):
            for j in range(4):
                hist1 = img1.crop((i*64, j*64, i*64+63, j*64+63)).copy().histogram()
                hist2 = img2.crop((i*64, j*64, i*64+63, j*64+63)).copy().histogram()
                sum += difference(hist1, hist2)
                #print difference(hist1, hist2)
        return sum/16
    return 0


def recognize(folder,pic, mode=1):

    # 不同的mode对应不同的类型
    file_list = []
    t = 0
    t1_hash = 0
    t2_devide = 0
    t3_straight = 0
    file_temp = ''
    for root,directors,files in os.walk(folder):#os.getcwd() + 

        for filename in files:

            filepath = os.path.join(root,filename)
            if (filepath.endswith(".png") or filepath.endswith(".jpg")):

                remember1_hash = similary_calculate(pic, folder + filename,3)

                remember2_devide = similary_calculate(pic, folder + filename,2)

                remember3_straight = similary_calculate(pic, folder + filename,1)

                remember = (remember1_hash + remember2_devide + remember3_straight) / 3

                # print filename
                # print remember
                if (remember > t):# and remember!= 1
                   file_temp = filename
                   t = remember
                   t1_hash = remember1_hash
                   t2_devide = remember2_devide
                   t3_straight = remember3_straight

    return file_temp,t,t1_hash,t2_devide,t3_straight

# if __name__ == '__main__': 
#     print "###########直方图的距离计算#############"
#     print "相似度最高的图是" + recognize('./','1.jpg',1)[0]
#     print "###########分块直方图的距离计算#############"
#     print "相似度最高的图是" + recognize('./','1.jpg',2)[0]
#     print "##############感知哈希算法###############"
#     print "相似度最高的图是" + recognize('./','1.jpg',3)[0]




# #判断一张图片是否存在于另一张图片
# import aircv as ac
# def matchImg(imgsrc,imgobj,confidencevalue=0.5):#imgsrc=原始图像，imgobj=待查找的图片
#     imsrc = ac.imread(imgsrc)
#     imobj = ac.imread(imgobj)
 
#     match_result = ac.find_template(imsrc,imobj,confidence)  # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)}
#     if match_result is not None:
#         match_result['shape']=(imsrc.shape[1],imsrc.shape[0])#0为高，1为宽

#     return match_result






def get_rect(path_read,path_write,size=256):


    rect_color = (0, 255, 0)
    size = size


    # try:

    # import the necessary packages
    #from pyimagesearch import imutils
    #from skimage import exposure
    import numpy as np
    #import argparse
    import imutils
    import cv2

    # load the query image, compute the ratio of the old height
    # to the new height, clone it, and resize it
    #image = cv2.imread(args["query"])
    image = cv2.imread(path_read)
    ratio = image.shape[0] / float(size)
    orig = image.copy()
    image = imutils.resize(image, height = size)
     
    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None

    # loop over our contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
     
        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break

    # get the gotten image
    x1 = min([screenCnt[0][0][0],screenCnt[1][0][0]])
    y1 = min([screenCnt[0][0][1],screenCnt[1][0][1]])

    x2 = max([screenCnt[2][0][0],screenCnt[3][0][0]])
    y2 = max([screenCnt[2][0][1],screenCnt[3][0][1]])

    hight = y2 - y1
    width = x2 - x1
    crop_img= image[y1:y1+hight, x1:x1+width]
    # #draw the 
    #cv2.imshow('crop_img', crop_img)

    # #draw rect in the orignal image
    # cv2.drawContours(image, [screenCnt], -1, rect_color, 3)
    # cv2.imshow("Game Boy Screen", image)
    #cv2.waitKey(0)

    # #draw the 
    cv2.imwrite(path_write, crop_img)

    return True
    # except:
    #     return False


# path_read = '../images2/11.jpg'

# path_write = '../images2/11_write.jpg'

# get_rect(path_read,path_write)