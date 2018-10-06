import cv2 as cv
import numpy as np;


img=cv.imread('/Users/haochengtang/PycharmProjects/cv/proj1_cse573/task1.png',0)


Vertical=np.zeros([img.shape[0],img.shape[1]]);
Horizontal=np.zeros([img.shape[0],img.shape[1]]);
Gx=np.array([[-1,0,1],[-2,0,2],[-1,0,1]]);
Gy=np.array([[-1,-2,-1],[0,0,0],[1,2,1]]);

#convolute sobel operator with image
for i in range(0,img.shape[0]-2):
    for j in range(0,img.shape[1]-2):
        for k in range(0,Gx.shape[0]):
            for l in range(0,Gx.shape[1]):
                Vertical[i + 1][j + 1] += img[i + k][j + l] * Gx[k][l];
                Horizontal[i + 1][j + 1] += img[i + k][j + l] * Gy[k][l];

#using two different ways to eliminate negative number in Vertical result
posV1=(Vertical-np.min(Vertical))/(np.max(Vertical)-np.min(Vertical));
posV2=np.abs(Vertical)/np.max(np.abs(Vertical));

cv.imshow('Vertical1',posV1)
cv.waitKey(0)

cv.imshow('Vertical2',posV2)
cv.waitKey(0)

#using two different ways to eliminate negative number in horizontal result
posH1=(Horizontal-np.min(Horizontal))/(np.max(Horizontal)-np.min(Horizontal));
posH2=np.abs(Horizontal)/np.max(np.abs(Horizontal));

cv.imshow('Horizontal1',posH1)
cv.waitKey(0)

cv.imshow('Horizontal2',posH2)
cv.waitKey(0)
