import numpy as np
import cv2
from copy import deepcopy
import os,sys



# im = cv2.imread('lines.jpg')
# im = cv2.imread('test2.jpg')
# im = cv2.imread('line.jpg')

def LinesEnhancement(indx,img):
    expNo=str(8)

    img = cv2.imread("/home/kapitsa/pyCharm/segmentation/weaklySupervisedSegmentation/publicationData/8/test.jpg", 0)
    #print(img.shape)

    # Thresholding the image
    (thresh, img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Invert the image
    img_bin = 255 - img_bin
    cv2.imwrite("Image_bin.jpg", img_bin)

    # Defining a kernel length
    kernel_length = np.array(img).shape[1] // 80

    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Morphological operation to detect vertical lines from an image
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    cv2.imwrite(basePath+expNo+ "/delMe/lineResults//"+str(indx)+"verticle_lines.jpg", verticle_lines_img)

    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    cv2.imwrite(basePath+expNo+ "/delMe/lineResults//"+str(indx)+"horizontal_lines.jpg", horizontal_lines_img)



#LinesEnhancement(0,im)


def getVerticleLines(image,vlines,vLineLength):

    try:

        #print image.shape
        tempImage= image#deepcopy(image)
        #print(tempImage.shape)

        height,width=image.shape
        pix=tempImage

        tempVLine=[]

        iter=0

        for x in range(width):

            y1,y2=(None,None)

            flag,black,run=0,0,0

            for y in range(height):

                #print(pix[y,x])
                if int(pix[y,x])<=0:
                    #print(iter)
                    iter=iter+1
                    black=black+1

                    if black>=2 and flag!=1:
                        flag=1


                    if not y1:
                        y1=y

                    y2=y

                    if abs(y2-y1)>=vLineLength and y==(height-1) and flag==1 and (y1!=y2):

                        if (x-1,y1,x-1,y2) not in vlines or (x-2,y1,x-2,y2) not in vlines or (x-3,y1,x-3,y2) not in vlines or (x-4,y1,x-4,y2) not in vlines or (x - 5, y1, x - 5, y2) not in vlines:
                            vlines.append((x,y1,x,y2))
                            tempVLine.append((x,y1,x,y2))

                else:
                    iter=iter+1

                    ''' line break'''

                    if black>run or flag:
                        run=black

                        if flag==1:
                            flag=0

                            '''
                                only insert and end of line
                            '''

                            if abs(y2-y1) >=vLineLength and (y1!=y2):
                                if (x-1,y1,x-1,y2) not in vlines or (x-2,y1,x-2,y2) not in vlines or (x-3,y1,x-3,y2) not in vlines or (x-4,y1,x-4,y2) not in vlines or (x - 5, y1, x - 5, y2) not in vlines:
                                    vlines.append((x,y1,x,y2))
                                    tempVLine.append((x,y1,x,y2))
                    black=0
                    flag=0
                    y1,y2=(None,None)

        temp=np.zeros(shape=tempImage.shape)
        for h in tempVLine:
            #print(h)
            cv2.line(temp,(h[0],h[1]),(h[2],h[3]),(255,255,0),1)


        #cv2.imwrite(basePath+expNo+ "/delMe/lineResults//"+str(999)+"verticle_lines.jpg",temp)

    except Exception as e:

        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("\n\t line no:", exc_tb.tb_lineno)



    return vlines,tempVLine,temp


def getHorozontalLines(image,hlines,hLineLength):

    try:

        tempImage= image #[:,:,0]#deepcopy(image)
        #(tempImage.shape)

        height,width=image.shape
        pix=tempImage

        tempHLine=[]

        iter=0

        for  y in range(height):

            x1,x2=(None,None)

            flag,black,run=0,0,0

            for x in range(width):

                if int(pix[y,x])<=0:

                    iter=iter+1
                    black=black+1

                    if black>=2 and flag!=1:
                        flag=1

                    if not x1:
                        x1=x

                    x2=x

                    if abs(x2-x1)>=hLineLength and x==(width-1) and flag==1 and (x1!=x2):

                        if (x1,y-1,x2,y-1) not in hlines or (x1,y-2,x2,y-2) not in hlines or \
                                (x1,y-3,x2,y-3) not in hlines \
                                or (x1,y-4,x2,y-4) not in hlines or (x1, y-5, x2, y-5) not in hlines:
                            hlines.append((x1,y,x2,y))
                            tempHLine.append((x1,y,x2,y))

                else:
                    iter=iter+1

                    ''' line break'''

                    if black>run or flag:
                        run=black

                        if flag==1:
                            flag=0

                            '''
                                only insert and end of line
                            '''

                            if abs(x2-x1) >=hLineLength and (x1!=x2):
                                if (x1,y-1,x2,y-1) not in hlines or (x1,y-2,x2,y-2) not in hlines or (x1,y-3,x2,y-3) not in hlines or (x1,y-4,x2,y-4) not in hlines or (x1, y-5, x2 , y- 5) not in hlines:
                                    hlines.append((x1,y,x2,y))
                                    tempHLine.append((x1,y,x2,y))
                    black=0
                    flag=0
                    x1,x2=(None,None)

        temp=np.zeros(shape=tempImage.shape)
        for h in tempHLine:
            #print(h)
            cv2.line(temp,(h[0],h[1]),(h[2],h[3]),(255,255,0),1)


        #cv2.imwrite(basePath+expNo+ "/delMe/lineResults//"+str(999)+"horizontal_lines.jpg",temp)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("\n\t line no:", exc_tb.tb_lineno)

    return hlines,tempHLine,temp




def call(file,originalImg,basePath,expNo,indx):#
    vlines = []
    vLineLength = 25

    hlines = []
    hLineLength = 25

    # basePath = "/home/kapitsa/pyCharm/segmentation/weaklySupervisedSegmentation/publicationData//"
    # expNo = str(8)

    #image = cv2.imread("/home/kapitsa/pyCharm/segmentation/weaklySupervisedSegmentation/publicationData/8/test.jpg")

    #cv2.imwrite(basePath+expNo+ "/delMe/lineResults//"+str(indx)+"tempCopy.jpg",file)

    image = file #cv2.imread(filePath)

    #cv2.imwrite(basePath + expNo + "/delMe/lineResults//" + str(999) + "original.jpg", image)

    #print "\n\t vlines"

    try:
        vlines,tempVLine,v=getVerticleLines(image,vlines,vLineLength)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("\n\t line no:", exc_tb.tb_lineno)


    try:
        hlines,tempHLine,h=getHorozontalLines(image,hlines,hLineLength)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("\n\t line no:", exc_tb.tb_lineno)

    i=v+h


    cv2.imwrite(basePath+expNo+ "/delMe/lineResults//"+str(indx)+"all_lines.jpg",i)

    '''
        extract contours and its co-ordinates crop that part from original image
    '''



# basePath = "/home/kapitsa/pyCharm/segmentation/weaklySupervisedSegmentation/publicationData//"
# expNo = str(8)
#
# filePath = "/home/kapitsa/pyCharm/segmentation/weaklySupervisedSegmentation/publicationData/8/test.jpg"

#call(filePath,basePath,expNo)






























