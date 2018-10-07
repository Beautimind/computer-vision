import numpy as np
import cv2 as cv
import math
import time

def gaussian(img,kernel):
    offset=int(len(kernel)/2)
    result=np.zeros(img.shape,dtype=np.float)
    img=img.astype(np.float)
    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            temp=0.0
            for k in range(-offset,offset+1):
                for l in range(-offset,offset+1):
                    i1=i+k;
                    j1=j+l;   #here is an error
                    if i1<0:
                        i1=0;
                    elif i1>img.shape[0]-1:
                        i1=img.shape[0]-1
                    if j1<0:
                        j1=0;
                    elif j1>=img.shape[1]-1:
                        j1=img.shape[1]-1
                    temp+=img[i1][j1]*kernel[k+offset][l+offset]
            result[i][j]=temp;
            # print(result[i][j])
    return result;

def fast_gausssian(img,kernel):
    offset = int(len(kernel) / 2)
    result = np.zeros(img.shape, dtype=np.float)
    img = img.astype(np.float)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            temp = 0.0
            for k in range(-offset, offset + 1):
                i1 = i + k;
                if i1 < 0:
                    i1 = 0;
                elif i1 > img.shape[0] - 1:
                    i1 = img.shape[0] - 1
                temp += img[i1][j] * kernel[k + offset]
            result[i][j]=temp;
    for j in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            temp = 0.0
            for k in range(-offset, offset + 1):
                j1 = j + k;
                if j1 < 0:
                    j1 = 0;
                elif j1 > img.shape[1] - 1:
                    j1 = img.shape[1] - 1
                temp += img[i][j1] * kernel[k + offset]
            result[i][j]=temp;
    return result

def downsample(img):
    result=np.zeros([int(img.shape[0]/2),int(img.shape[1]/2)],dtype=np.float)
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            result[i][j]=img[i*2][j*2]
    return result

def genkernel(o,size):
    l=int(size/2);
    result=np.zeros([size,size],dtype=np.float)
    sum=0.0;
    for i in range(-l,l+1):
        for j in range(-l,l+1):
            result[i+l][j+l]=math.exp(-(i*i+j*j)/(2*o**2))
            sum+=result[i+l][j+l];
    return result/sum;

def seperateKernel(size,omega):
    result=np.zeros([size,1],dtype=np.float)
    length=int(size/2)
    sum=0.0;
    for i in range(-length,length+1):
        result[i+length]=math.exp(-(i*i)/(2*omega**2))
        sum+=result[i+length]
    return result/sum

def findkeypoint(pre, tar,post):
    result=set()
    for i in range(1,tar.shape[0]-1):
        for j in range(1,tar.shape[1]-1):
            def largest():
                for k in range(-1,2):
                    for l in range(-1,2):
                        if k!=0 or l!=0:
                                if tar[i+k][j+l]>=tar[i][j] or pre[i+k][j+l]>=tar[i][j] or post[i+k][j+l]>=tar[i][j]:
                                    return False;
                        elif pre[i+k][j+l]>=tar[i][j] or post[i+k][j+l]>=tar[i][j]:
                            return False;
                return True;
            def smallest():
                for k in range(-1,2):
                    for l in range(-1,2):
                        if k!=0 or l!=0:
                            if tar[i+k][j+l]<=tar[i][j] or pre[i+k][j+l]<=tar[i][j] or post[i+k][j+l]<=tar[i][j]:
                                return False;
                        elif pre[i+k][j+l]<=tar[i][j] or post[i+k][j+l]<=tar[i][j]:
                            return False
                return True;
            if largest() or smallest():
                result.add((i,j))
            # maxpre=np.max(pre[i-1:i+2,j-1:j+2]);
            # minpre=np.min(pre[i-1:i+2,j-1:j+2]);
            # maxtar=np.max(tar[i-1:i+2,j-1:j+2]);
            # mintar=np.min(tar[i-1:i+2,j-1:j+2]);
            # maxpost=np.max(post[i-1:i+2,j-1:j+2]);
            # minpost=np.min(post[i-1:i+2,j-1:j+2])
            # if maxpre<=tar[i][j] and maxtar<=tar[i][j] and maxpost<=tar[i][j]:
            #     result.add((i,j));
            # # elif minpre>=tar[i][j] and mintar>=tar[i][j] and minpost>=tar[i][j]:
            # #     result.add((i,j))
    return result;




kernel1=genkernel(1,3);
kernel2=genkernel(10,3)

img=cv.imread('/Users/haochengtang/PycharmProjects/cv/proj1_cse573/task2.jpg',0)
img=img/255
#create sigma we need to use
sigmas=np.zeros([4,5],dtype=np.float)
root2=math.sqrt(2);
sigmas[0][0]=1.0/root2
for i in range(1,4):
    sigmas[i][0]=sigmas[i-1][0]*2;
for i in range(0,4):
    for j in range(1,5):
        sigmas[i][j]=sigmas[i][j-1]*root2

octaves=list()
imgs=list();

# downsample the image and store in list imgs
for i in range(0,4):
    # cv.imshow('downsample',img);
    # cv.waitKey();
    imgs.append(img);
    octaves.append(list());
    img=downsample(img);

# create octaves by blur the downsampled image using different kernel size=
for i in range(0,4):
    for j in range(0,5):
        kernel=genkernel(sigmas[i][j],7)
        octaves[i].append(gaussian(imgs[i],kernel));
        # cv.imwrite('blurred' + str(i) + '-' + str(j) + '.jpg', (octaves[i][j] * 255).astype(np.uint8));
        # print(octaves[i][-1][100][100])
        # print(kernel)

# Show the blurring result
for i in octaves:
    for j in i:
        cv.imshow('blurred', j)
        cv.waitKey()

# Creat DOG result and store in list DOGs
DOGs=list()
for i in range(0,4):
    DOGs.append(list())
    for j in range(0,4):
        DOGs[-1].append(np.subtract(octaves[i][j],octaves[i][j+1]));
        # a=np.absolute(DOGs[-1][-1])
        # cv.imshow('DOG',a/np.max(a))
        # cv.waitKey();
        max=np.max(DOGs[-1][-1]);
        min=np.min(DOGs[-1][-1]);
        tostore=(DOGs[-1][-1]-min)/(max-min)
        tostore=(DOGs[-1][-1]*255).astype(np.uint8)
        # cv.imwrite('DOG'+str(i)+'-'+str(j)+'.jpg',(DOGs[-1][-1]*255).astype(np.uint8))
        cv.imshow('DOG',tostore);
        cv.waitKey();
#
# # Detect the keypoint
keypoints = list();

for i in range(0,4):
    keypoints.append(set())
    for j in range(1,3):
        keypoints[-1]=keypoints[-1].union(findkeypoint(DOGs[i][j-1],DOGs[i][j],DOGs[i][j+1]))
    print(len(keypoints[-1]))

key=list()
for i in range(0,4):
    for p in keypoints[i]:
        key.append((p[0]*(i+1),p[1]*(i+1)))

a=sorted(key,key=lambda x: x[1])
print(a[0:6])
for i in key:
    imgs[0][i[0]][i[1]]=1.0;
cv.imshow('keypoints',img[0]);
cv.waitKey()
cv.imwrite("keypoints.jpg",(imgs[0]*255).astype(np.uint8))
# cv.imshow('origin',img);
# # cv.waitKey(0);
# g=gaussian(img,kernel);
# # a=downsample(img)
# cv.imshow('blurred',g);
# cv.waitKey()
#
# for i in range(1,5):
#     sigmas[0,i]=root2*sigmas[0][i-1];
# for j in range(1,4):
#     sigmas[j,:]=sigmas[j-1,:]*2;





