import numpy as np
import cv2 as cv
import math

dir='/Users/haochengtang/PycharmProjects/cv/proj1_cse573/task3/'
pos=list();
edgepos=list()
neg=list();
posnum=15
negnum=10;

for i in range(1,posnum+1):
    filename=dir+'pos_'+str(i)+'.jpg'
    pos.append(cv.imread(filename));

for i in range(1,posnum+1):
    filename=dir+'neg_'+str(i)+'.jpg'
    neg.append(cv.imread(filename));

cursor=cv.imread(dir+'cursor3.jpg')
# cursor=cv.resize(cursor,(0,0),2,2)
# _,cursor=cv.threshold(cursor,100,255,cv.THRESH_BINARY)
# cursor=cv.Sobel(cursor,cv.CV_64F,1,1)
# _,cursor=cv.threshold(cursor,125,255,cv.THRESH_BINARY);
cv.imshow('result',cursor);
cv.waitKey();
# print(len(cursor))
# print(len(cursor[0]))
for i in pos:
    # _,temp=cv.threshold(i,200,255,cv.THRESH_BINARY)
    # cv.imshow('binary',temp);
    # cv.waitKey();
    result=cv.matchTemplate(i, cursor,method=cv.TM_CCOEFF_NORMED)
    # cv.imshow('result',result)
    # cv.waitKey()
    minVal, maxVal, minLoc, maxLoc=cv.minMaxLoc(result);
    print(maxVal,maxLoc)
    cv.rectangle(i,maxLoc,(maxLoc[0]+len(cursor[0]),maxLoc[1]+len(cursor)),(0,0,255));
    cv.imshow(str(maxVal),i);
    cv.waitKey()
for i in neg:
    result = cv.matchTemplate(i, cursor, method=cv.TM_CCOEFF_NORMED)
    # cv.imshow('result',result)
    # cv.waitKey()
    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result);
    print(maxVal, maxLoc)
    cv.rectangle(i, maxLoc, (maxLoc[0] + len(cursor[0]), maxLoc[1] + len(cursor)), (0, 0, 255));
    cv.imshow(str(maxVal), i);
    cv.waitKey()
# cv.imshow('cursor',cursor)
# cv.waitKey()
# for i in pos:
#     cv.imshow('pos',i);
#     cv.waitKey()
# for i in neg:
#     cv.imshow('neg',i)
#     cv.waitKey()

# a1=np.array([75,127,52,87,86,0,12,188,176])
#
# a2=np.array([3,10,20,18,1,15,2,30,3])
# m1=np.mean(a1);
# m2=np.mean(a2);
# a1=a1-m1;
# a2=a2-m2;
# upper=np.sum(a1*a2)
# lower=math.sqrt(np.sum(a1*a1)*np.sum(a2*a2))
# print(upper/lower)