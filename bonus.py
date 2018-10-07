import numpy as np
import cv2 as cv

def findcursor(i,cursor):
    _, t = cv.threshold(i, 150, 255, cv.THRESH_TOZERO)
    # t=cv.resize(i,(i.shape[1]*2,i.shape[0]*2))
    # t=cv.GaussianBlur(t,(3,3),1)
    # t = cv.resize(t, (int(i.shape[1] / 2), int(i.shape[0] / 2)))
    t = cv.Laplacian(t, cv.CV_64F, ksize=3)
    _, t = cv.threshold(t, 200, 255, cv.THRESH_BINARY)
    t = t.astype(np.uint8)
    cv.imshow('edge',t)
    cv.waitKey()
    result = cv.matchTemplate(t, cursor, method=cv.TM_SQDIFF)
    # cv.imshow('result',result)
    # cv.waitKey()
    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result);
    return minVal,minLoc

dir='/Users/haochengtang/PycharmProjects/cv/proj1_cse573/task3_bonus/'

pos=list();
edgepos=list()
neg=list();
posnum=6;
negnum=12;
curnum=3;
cursors=list()
for i in range(0,curnum):
    fullpath=dir+'cursor'+str(i+1)+'.jpg';
    cursor=cv.imread(fullpath,0)
    _, cursor = cv.threshold(cursor, 170, 255, cv.THRESH_TOZERO)
    _, bg = cv.threshold(cursor, 170, 125, cv.THRESH_BINARY_INV)
    cursor = cv.Laplacian(cursor, cv.CV_64F, ksize=5)
    _, cursor = cv.threshold(cursor, 150, 255, cv.THRESH_BINARY)
    cursor = cursor.astype(np.uint8)
    cv.imshow('result',cursor)
    cv.waitKey()
    cursors.append(cursor)
    pos.append(list())

for i in range(0,curnum):
    for j in range(0,posnum):
        fullpath=dir+'t'+str(i+1)+'_'+str(j+1)+'.jpg'
        pos[i].append(cv.imread(fullpath,0));

for i in range(0,curnum):
    for j in range(0,posnum):
        maxVal,maxLoc=findcursor(pos[i][j],cursors[i]);
        print(maxVal, maxLoc)
        cv.rectangle(pos[i][j], maxLoc, (maxLoc[0] + len(cursors[i][0]), maxLoc[1] + len(cursors[i])), 255,thickness=2);
        # cv.imshow(str(maxVal), pos[i][j]);
        # cv.waitKey()