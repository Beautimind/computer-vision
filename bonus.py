import numpy as np
import cv2 as cv
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
    cursors.append(cv.imread(fullpath))
    pos.append(list())

for i in range(0,curnum):
    for j in range(0,posnum):
        fullpath=dir+'t'+str(i+1)+'_'+str(j+1)+'.jpg'
        pos[i].append(cv.imread(fullpath));

for i in range(0,curnum):
    for j in range(0,posnum):
        result = cv.matchTemplate(pos[i][j], cursors[i], method=cv.TM_CCOEFF_NORMED)
        # cv.imshow('result',result)
        # cv.waitKey()
        minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result);
        print(maxVal, maxLoc)
        cv.rectangle(pos[i][j], maxLoc, (maxLoc[0] + len(cursors[i][0]), maxLoc[1] + len(cursors[i])), (0, 0, 255));
        cv.imshow(str(maxVal), pos[i][j]);
        cv.waitKey()