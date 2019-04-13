import cv2
import os,sys
from copy import deepcopy
import numpy as np

def writeImageCC(OutImage,tempCopy,ii):
    ''''
    temporary change
    '''
    #print "\n\t OutImage+str(ii)+.jpg=",str(ii)+".jpg"
    nameImage=str(ii).split("/")[-1]
    compID=str(ii).split("_")[0]+"_"
    #print("nameImage=",compID+nameImage)#+"_"+str(ii)+".jpg")
    nameImage=compID+nameImage
    #cv2.imwrite(outPath+nameImage,tempCopy)
    cv2.imwrite(OutImage+nameImage,tempCopy)

def writeImageCC1(OutImage,tempCopy,ii):
    ''''
    temporary change
    '''

    #print("\n\t OutImage path=",OutImage,"\t ii=",ii)
    #print "\n\t OutImage+str(ii)+.jpg=",str(ii)+".jpg"
    nameImage=str(ii).split("/")[-1]
    compID=str(ii) #str(ii).split("_")[1]
    #print("nameImage=",compID+nameImage)#+"_"+str(ii)+".jpg")
    nameImage=compID+".jpg" #+nameImage
    #print("\n\t nameImage=",nameImage)
    cv2.imwrite(OutImage+nameImage,tempCopy)



def drawRect(cor,image):
    cv2.rectangle(image,(cor[0],cor[1]),(cor[2],cor[3]),(0,255,0),1)
    return image

def displayAndSaveComponents(nm,imgCopy,original1,copyriginal,original1Sub,original2,labels,stats,ii,cc_threshold):
    imageFlag=0
    tempCopy=deepcopy(labels)
    tempCopy[tempCopy>ii]=0
    tempCopy[tempCopy<ii]=0
    tempCopy[tempCopy==ii]=255

    i=ii

    x=stats[i][0]
    dx=stats[i][2]
    y=stats[i][1]
    dy=stats[i][3]

    multi=dx*dy

    if 1:#multi>cc_threshold:
        imageFlag=1


        #drawContour2(tempCopy,ii)
        crop=255-tempCopy[y:(y+dy),x:(x+dx)]
        crop1 = 255-original1[y:(y + dy), x:(x + dx)]

        writeImageCC(resultDump+"//cc//",crop1,str(ii)+"_"+nm)

        #original=drawRect([y,x,y+dy,x+dx],original)
        imgCopy=drawRect([x,y,x+dx,y+dy],imgCopy)
        original1=drawRect([x,y,x+dx,y+dy],original1)
        #copyriginal[y,y+dy,x,x+dx]=original1[y,y+dy,x,x+dx]


        # print("\n\t copyriginal shape=",copyriginal.shape)
        # print("\n\t crop shape=",crop.shape)
        #copyriginal[y, y + dy, x, x + dx,0] =crop[:,:,0]
        copyriginal[y:(y + dy), x:(x + dx)]=crop1
        original1Sub[y:(y + dy), x:(x + dx)]=original1Sub[y:(y + dy), x:(x + dx)]-original2[y:(y + dy), x:(x + dx)]

        #writeImageCC1(resultDump+"//cc//",tempCopy,ii)
        #writeImageCC1(resultDump + "//cc//", tempCopy, ii)
        #input("check")
    return imgCopy,original1,copyriginal,original1Sub


def readFile(fileRead,blackOnWhite):

    #img=cv2.imread(location+fileRead)
    img = cv2.imread(fileRead)
    im=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret2,th2=cv2.threshold(im,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    if blackOnWhite==1:
        th2=(255-th2)

    return th2,fileRead,img


def findConnectedComponents(file):
    #print "**"

    connectivity=4
    output=cv2.connectedComponentsWithStats(file,connectivity,cv2.CV_32S)
    labels=output[1]
    stats=output[2]

    return output,labels,stats


def getContours(img):

    print("\n\t finds contours")

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
    ret, thresh = cv2.threshold(imgray, 127, 255, 0);
    image,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);

    # draw a three pixel wide outline
    cv2.drawContours(img, contours, -1, (0, 255, 0), 3);

    cv2.imwrite(resultDump+"contours1.jpg",img)

    #print(contours[0])

    for c in contours:
        # get the bounding rect
        x, y, w, h = cv2.boundingRect(c)
        # draw a green rectangle to visualize the bounding rect
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        print(x, y, w, h)

    cv2.imwrite(resultDump+"contours.jpg",img)


def LinesEnhancement(img):


    #img = cv2.imread("/home/kapitsa/pyCharm/segmentation/weaklySupervisedSegmentation/publicationData/8/test.jpg", 0)
    #print(img.shape)

    # Thresholding the image
    (thresh, img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Invert the image
    img_bin = 255 - img_bin
    #cv2.imwrite("Image_bin.jpg", img_bin)

    # Defining a kernel length
    kernel_length = np.array(img).shape[1] // 80

    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Morphological operation to detect vertical lines from an image
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=5)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=5)
    #cv2.imwrite(basePath+expNo+ "/delMe/lineResults//"+str(indx)+"verticle_lines.jpg", verticle_lines_img)

    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=5)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=5)
    #cv2.imwrite(basePath+expNo+ "/delMe/lineResults//"+str(indx)+"horizontal_lines.jpg", horizontal_lines_img)

    return horizontal_lines_img+verticle_lines_img



if __name__=="__main__":
    basePath = "/home/kapitsa/pyCharm/segmentation/weaklySupervisedSegmentation/publicationData//"
    expNo = str(8)

    for i in range(1,125):

        print ("\n\t i=",i)
        nm=str(i)+"all_lines.jpg"
        #nm="1all_lines.jpg"
        filePath = basePath + expNo + "//delMe//lineResults//"+nm
        #oriFilePath = basePath + expNo + "//delMe//lineResults//" + "1_original.jpg"

        oriFilePath = basePath + expNo + "//delMe//lineResults//" + str(i)+"_original.jpg"

        resultDump = basePath + expNo + "//delMe//contours//"

        img = cv2.imread(filePath)
        #print(img.shape)


        original1 = cv2.imread(oriFilePath)
        original2 = cv2.imread(oriFilePath)
        copyriginal=np.zeros(shape=original1.shape)
        original1Sub =deepcopy(original1)

        #print(original.shape)

        #getContours(img)

        '''
        0. read file and convert to gray 
        '''
        img1, fileName, imgCopy = readFile(filePath, 0)
        print "\n\t shape=>", img1.shape

        #img1=LinesEnhancement(img1)
        #cv2.imwrite(resultDump + "enhance.jpg",img1)
        #input("*****")


        output, labels, stats = findConnectedComponents(img1)

        '''    cv2.imwrite(resultDump+"contours.jpg",img)
        2. save individual cc
        '''


        for indx,ii in enumerate(np.unique(labels)):
            # print "\n\t cc no=", ii
            # print "\n\t file name=",nm
            if ii == 0 or ii == 1: #or ii == 1 or ii == 2:
                continue
            if ii % 100 == 0:
                #print "\n\t image no=", indx, "\t tot images=", totImages
                print "\n\t cc  indx=", indx,"\t tot cc=",len(np.unique(labels))

            imgCopy,original1,copyriginal,original1Sub = displayAndSaveComponents(nm, imgCopy,original1,copyriginal,original1Sub,original2, labels, stats, ii, cc_threshold=500)

        #original1Sub =original1Sub-copyriginal
        cv2.imwrite(resultDump+"//newData//"+str(i)+"_originalSub1.jpg",original1Sub)
        cv2.imwrite(resultDump+str(i)+"_in.jpg",img1)
        cv2.imwrite(resultDump+str(i)+"_contours1.jpg",original1)
        cv2.imwrite(resultDump +str(i)+"_contoursCopy1.jpg", copyriginal)
        cv2.imwrite(resultDump +str(i)+"_contours2.jpg", imgCopy)


        #cv2.imwrite(resultDump+"//newData//"+str(i)+"_original.jpg",original2)
        #input("check")
        #print(output)


