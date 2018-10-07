import numpy as np
import cv2 as cv
import math

dir='/Users/haochengtang/PycharmProjects/cv/proj1_cse573/task3/'
pos=list();
edgepos=list()
neg=list();
posnum=15
negnum=10;

def findcursor(i,cursor):
    _, t = cv.threshold(i, 150, 255, cv.THRESH_TOZERO)
    # t=cv.resize(i,(i.shape[1]*2,i.shape[0]*2))
    # t=cv.GaussianBlur(t,(3,3),1)
    # t = cv.resize(t, (int(i.shape[1] / 2), int(i.shape[0] / 2)))
    t = cv.Laplacian(t, cv.CV_64F, ksize=5)
    _, t = cv.threshold(t, 200, 255, cv.THRESH_BINARY)
    t = t.astype(np.uint8)
    result = cv.matchTemplate(t, cursor, method=cv.TM_SQDIFF)
    # cv.imshow('result',result)
    # cv.waitKey()
    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result);
    return minVal,minLoc

t=dir+'pos_'+str(5)+'.jpg'

for i in range(1,posnum+1):
    filename=dir+'pos_'+str(i)+'.jpg'
    pos.append(cv.imread(filename,0));

for i in range(1,posnum+1):
    filename=dir+'neg_'+str(i)+'.jpg'
    neg.append(cv.imread(filename,0));

cursor=cv.imread(dir+'cursor3.jpg',0)
_,cursor=cv.threshold(cursor,170,255,cv.THRESH_TOZERO)
_,bg=cv.threshold(cursor,170,125, cv.THRESH_BINARY_INV)
cursor=cv.Laplacian(cursor,cv.CV_64F,ksize=5)
_, cursor = cv.threshold(cursor, 150, 255, cv.THRESH_BINARY)
cursor=cursor.astype(np.uint8)
# cv.imshow('result',cursor)

# i=pos[10]
# maxVal,maxLoc=findcursor(i,cursor)
# if maxVal<3100000:
#     cv.rectangle(i,maxLoc,(maxLoc[0]+len(cursor[0]),maxLoc[1]+len(cursor)),255,thickness=2);
# cv.imwrite("pos11result"+".jpg",i)
# cv.imshow(str(maxVal),i);
# cv.waitKey()


cv.imshow('result',cursor);
cv.waitKey();
# print(len(cursor))
# print(len(cursor[0]))
# for k in range(0,15):
#     # # cv.imshow('i',i)
#     # # cv.waitKey()
#     # # _,temp=cv.threshold(i,200,255,cv.THRESH_BINARY)
#     # # cv.imshow('binary',temp);
#     # # cv.waitKey();
#     # _,t=cv.threshold(i,150,255,cv.THRESH_TOZERO)
#     # # t=cv.resize(i,(i.shape[1]*2,i.shape[0]*2))
#     # # t=cv.GaussianBlur(t,(3,3),1)
#     # # t = cv.resize(t, (int(i.shape[1] / 2), int(i.shape[0] / 2)))
#     # t=cv.Laplacian(t,cv.CV_64F,ksize=5)
#     # _, t = cv.threshold(t, 200, 255, cv.THRESH_BINARY)
#     # t=t.astype(np.uint8)
#     # # cv.imshow('s', t);
#     # # cv.waitKey()
#     #
#     # result=cv.matchTemplate(t, cursor,method=cv.TM_CCOEFF_NORMED)
#     # # cv.imshow('result',result)
#     # # cv.waitKey()
#     # minVal, maxVal, minLoc, maxLoc=cv.minMaxLoc(result);
#     i=pos[k]
#     maxVal,maxLoc=findcursor(i,cursor)
#     print(maxVal,maxLoc)
#     if maxVal<3200000:
#         cv.rectangle(i,maxLoc,(maxLoc[0]+len(cursor[0]),maxLoc[1]+len(cursor)),255,thickness=2);
#     cv.imwrite("pos"+str(k+1)+"result"+".jpg",i)
#     cv.imshow(str(maxVal),i);
#     cv.waitKey()
for k in range(0,negnum):
    i=neg[k];
    maxVal, maxLoc = findcursor(i, cursor)
    # result = cv.matchTemplate(i, cursor, method=cv.TM_SQDIFF_NORMED)                                                                                                                                                                                                                 
    # cv.imshow('result',result)
    # cv.waitKey()
    print(maxVal, maxLoc)
    if maxVal<3200000:
        cv.rectangle(i, maxLoc, (maxLoc[0] + len(cursor[0]), maxLoc[1] + len(cursor)), (0, 0, 255),thickness=2);
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