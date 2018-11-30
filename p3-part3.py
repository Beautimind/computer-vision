import cv2
import numpy as np
import function as mf
dir="/Users/haochengtang/cv/project3/"
fname=dir+"hough 2.jpg"
img=cv2.imread(fname,0)
# edge=cv2.Sobel(img,cv2.CV_64F,1,0,ksize=9)


kernel1=np.array([[-1,0,1],[-2,0,2],[-1,0,1]]);
edge1=mf.convolution(img,kernel1)
edge1=np.abs(edge1);


kernel2=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
edge2=mf.convolution(img,kernel2)
edge2=np.abs(edge2)
edge=np.sqrt(edge1*edge1+edge2*edge2)

edge=edge/np.max(edge)
edge[edge<0.2]=0;
edge[edge>=0.2]=1;
# cv2.imshow("edge",edge)
# cv2.waitKey()


# edge=np.abs(edge);
# edge=edge/np.max(edge)
# edge[edge<0.2]=0;
# edge[edge>=0.2]=1;
kernel=np.ones((1,3));
edge=mf.closing(edge,kernel)
# edge=mf.closing(edge,np.eye(3))
# edge=mf.erosion(edge,np.ones((3,1)))
# edge=mf.erosion(edge,np.eye(3))
#
#
#
#
cv2.imshow("edge",edge)
cv2.waitKey()
#
def houghline(source):
    a=np.array(np.deg2rad(range(0,360)));
    sint=np.sin(a);
    cost=np.cos(a)
    diagnal=np.int(np.sqrt(source.shape[0]*source.shape[0]+source.shape[1]*source.shape[1]))
    result=np.zeros((360,diagnal),dtype=np.uint16);
    for i in range(source.shape[0]):
        for j in range(source.shape[1]):
            if source[i][j] == 1:
                for k in range(result.shape[0]):
                    l=i * cost[k] + j * sint[k];
                    ln=np.int(l+0.5)
                    if ln>0:
                        result[k, ln] += 1;
    return result;


def houghcircle(source):
    diagnal = np.int(np.sqrt(source.shape[0] * source.shape[0] + source.shape[1] * source.shape[1]))
    angles = np.deg2rad(np.array(range(0,360)))
    sint=np.sin(angles);
    cost=np.cos(angles)
    result=np.zeros((source.shape[0],source.shape[1],15));
    for i in range(source.shape[0]):
        for j in range(source.shape[1]):
            if source[i][j] == 1:
                for k in range(len(angles)):
                    for R in range(5,20):
                        a=np.int(i-R*cost[k]+0.5)
                        b=np.int(j-R*sint[k]+0.5)
                        if 0<=a<result.shape[0] and 0<=b<result.shape[1]:
                            result[a,b,R-5]+=1;
    return result;

def drawline(img,angle,r):
        s=np.sin(np.deg2rad(angle))
        c=np.cos(np.deg2rad(angle))
        if angle==0:
            cv2.line(img, (0,r), ( img.shape[0],r), color=255)
        elif 0<angle<90:
            i=np.int(r/c+0.5)
            j=np.int(r/s+0.5)
            cv2.line(img, (j, 0), (0, i), color=255);
        elif angle==90:
            cv2.line(img, (r, 0), (r, img.shape[1]), color=255)
        elif 90<angle<180:
            j1=img.shape[1];
            i1=np.int((r-j1*s)/c+0.5);
            i2=0;
            j2=np.int(r/s+0.5);
            cv2.line(img,(j1,i1),(j2,i2),color=255)
        elif 270<angle<360:
            i1=np.int(r/c+0.5)
            j1=0;
            i2=img.shape[0];
            j2=np.int((r-i2*c)/s+0.5);
            cv2.line(img,(j1,i1),(j2,i2),color=255)

def expectedratio(shape,angle,r):
    s = np.sin(np.deg2rad(angle))
    c = np.cos(np.deg2rad(angle))
    diagonal=np.sqrt(img.shape[0]*img.shape[0]+img.shape[1]*img.shape[1])
    result=100000
    if angle == 0:
        result=shape[0]
    elif 0 < angle < 90:
        i1=np.int(r / c + 0.5);
        i2=0;
        j1=0;
        j2=np.int(r / s + 0.5);
        if i1>shape[0]:
            i1=shape[0]
            j1=np.int((r-c*i1)/s+0.5)
        elif j2>shape[1]:
            j2=shape[1]
            i2=np.int((r-s*j2)/c+0.5)
        result = np.sqrt((i1 - i2) * (i1 - i2) + (j1 - j2) * (j1 - j2))
    elif angle == 90:
        result=shape[1];
    elif 90 < angle < 180:
        j1 = shape[1];
        i1 = np.int((r - j1 * s) / c + 0.5);
        i2 = 0;
        j2 = np.int(r / s + 0.5);
        if i1>shape[0]:
            i1=shape[0]
            j1=np.int((r-c*i1)/s+0.5)
        result=np.sqrt((i1-i2)*(i1-i2)+(j1-j2)*(j1-j2))
    elif 270 < angle < 360:
        i1 = np.int(r / c + 0.5)
        j1 = 0;
        i2 = shape[0];
        j2 = np.int((r - i2 * c) / s + 0.5);
        result = np.sqrt((i1 - i2) * (i1 - i2) + (j1 - j2) * (j1 - j2))
    return diagonal/result;

# test=np.zeros((100,100),dtype=np.uint8)
# drawline(test,120,50)
# cv2.imshow("funk",test);
# cv2.waitKey()


lines=houghline(edge)
for i in range(lines.shape[0]):
    for j in range(lines.shape[1]):
        if lines[i][j]>50:
            ratio=expectedratio(img.shape,i,j)
            lines[i][j]=lines[i][j]*ratio
final=np.zeros(img.shape,dtype=np.uint8)
# drawline(final,306,200)
for i in range(lines.shape[0]):
    for j in range(lines.shape[1]):
        up=max(i-3,0);
        down=min(i+3,lines.shape[0])
        l=max(j-11,0);
        r=min(j+11,lines.shape[1]);
        if lines[i][j]>300 and lines[i][j]==np.max(lines[up:down+1,l:r+1]):
            print(i,j,lines[i][j]);
            drawline(final,i,j);
cv2.imshow("f",final);
cv2.waitKey();


#
circle_result=np.zeros(edge.shape,dtype=np.uint8);
circles=houghcircle(edge);
cv2.imshow(circle_result);
cv2.waitKey();

test=np.ones((100,100),dtype=np.uint8);
cv2.circle(test,(50,20),5,color=255)
cv2.imshow("result",test)
cv2.waitKey();
cv2.imshow("lines",test);
cv2.waitKey()
