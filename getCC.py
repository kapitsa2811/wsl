import numpy as np
import argparse
import imutils
import glob
import cv2
import os
import pandas as pd
from copy import deepcopy
import glob
import sys
import random
from collections import defaultdict

cwd=os.getcwd()+"//"
templatePaths="/home/kapitsa/PycharmProjects/MyOCRService/myTable/allTemplates//"
#dataPath="/home/kapitsa/Documents/Dataset/tableDetection/marmot_dataset_v1.0/data/English/Positive/Raw//"
dataPath="/home/kapitsa/PycharmProjects/MyOCRService/myTable/patent1//"

outPath="/home/kapitsa/PycharmProjects/MyOCRService/myTable/cc//"

def drawRect(cor,image):
    cv2.rectangle(image,(cor[0],cor[1]),(cor[2],cor[3]),(0,0,255),1)
    return image

def writeImageCC(OutImage,tempCopy,ii):
    ''''
    temporary change
    '''
    #print "\n\t OutImage+str(ii)+.jpg=",str(ii)+".jpg"
    nameImage=str(ii).split("/")[-1]
    compID=str(ii).split("_")[0]+"_"
    #print("nameImage=",compID+nameImage)#+"_"+str(ii)+".jpg")
    nameImage=compID+nameImage
    cv2.imwrite(outPath+nameImage,tempCopy)


def writeImageCC1(OutImage,tempCopy,ii):
    ''''
    temporary change
    '''

    print("\n\t OutImage path=",OutImage,"\t ii=",ii)
    #print "\n\t OutImage+str(ii)+.jpg=",str(ii)+".jpg"
    nameImage=str(ii).split("/")[-1]
    compID=str(ii) #str(ii).split("_")[1]
    #print("nameImage=",compID+nameImage)#+"_"+str(ii)+".jpg")
    nameImage=compID+".jpg" #+nameImage
    print("\n\t nameImage=",nameImage)
    cv2.imwrite(OutImage+nameImage,tempCopy)



def readFile(fileRead,blackOnWhite):

    #img=cv2.imread(location+fileRead)
    img = cv2.imread(fileRead)
    im=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret2,th2=cv2.threshold(im,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    if blackOnWhite==1:
        th2=(255-th2)

    return th2,fileRead,img

def displayAndSaveComponents(nm,original,labels,stats,ii,cc_threshold):
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
        writeImageCC(outPath,crop,str(ii)+"_"+nm)

        #original=drawRect([y,x,y+dy,x+dx],original)
        original=drawRect([x,y,x+dx,y+dy],original)
        writeImageCC1("/home/kapitsa/PycharmProjects/MyOCRService/myTable///cc//delMe//",tempCopy,ii)
        #input("check")
    return original


def findConnectedComponents(file):
    #print "**"

    connectivity=4
    output=cv2.connectedComponentsWithStats(file,connectivity,cv2.CV_32S)
    labels=output[1]
    stats=output[2]

    return output,labels,stats


def readImages(dataPath):

    files = glob.glob(dataPath + "/*.jpg") + glob.glob(dataPath + "/*.bmp")+ glob.glob(dataPath + "/*.png")
    #files=glob.glob(cwd+"//cc//"+"*/")  #os.listdir(inputImages)
    totImages=len(files)


    print "\\nt files=",len(files)

    print "\n\t reads images"
    newImages=10
    exceptionCount=0
    #r,c=img.shape[0],img.shape[1]

    for indx,nm in enumerate(files):

        if indx>10:
            break

        try:
            #img1=cv2.imread(inputImages+nm)
            #print "\n\t shape=", img1.shape

            '''
            0. read file and convert to gray 
            '''
            img1,fileName,original=readFile(nm,0)
            #print "\n\t shape=>", img1.shape

            '''
            1.get cc
            '''
            output,labels,stats=findConnectedComponents(255-img1)
            print "\n\t no of unique labels=",len(np.unique(labels))
            #labels=labels[1:len(labels)]

            '''
            2. save individual cc
            '''

            for ii in np.unique(labels):
                # print "\n\t cc no=", ii
                # print "\n\t file name=",nm
                if ii==0:
                    continue
                if ii%100==0:
                    print "\n\t image no=", indx, "\t tot images=", totImages
                    print "\n\t cc no=",ii

                original=displayAndSaveComponents(nm,original,labels,stats,ii,cc_threshold=50)
            #writeImageCC1(outPath+"//delMe//",original,nm[:-4])

            #input("check")
        except Exception as e:
            print "\n\t fileName=",nm
            exceptionCount+=1

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("\n\t LINE NO:", exc_tb.tb_lineno)


        print "\n\t exceptionCount=",exceptionCount



def getCrops(labels,allRectTables):
    #print("***")

    allUniqueComp=[]
    unqElements=defaultdict(int)
    unqCCList=[]

    for rect in allRectTables:

        # print("\n\t rect=",rect)
        # print("\n\t UNIQUE COMPONETS=")

        x1,x2=rect[0][0],rect[1][0]
        y1,y2=rect[0][1],rect[1][1]
        # print("\n\t x1,y1=",x1,"\t",y1)
        # print("\n\t x2,y2=",x2,"\ty2=",y2)
        crop=labels[y1:y2, x1:x2]
        #crop=labels[x1:x2,y1:y2]

        allUniqueComp.append(np.unique(crop))

        #cv2.imwrite("/home/kapitsa/PycharmProjects/MyOCRService/myTable//rect//"+ranName+".jpg",255-crop)
        #cv2.imwrite("/home/kapitsa/PycharmProjects/MyOCRService/myTable//rect//s_"+ranName+".jpg",crop)

    #print("\n\t allUniqueComp=",allUniqueComp)


    for unq in allUniqueComp:
        #print "\n\t unq=",unq,"\t type=",type(unq)

        for ele in unq:
            #print "\n\t ele=",ele
            unqElements[ele]+=1

    #print("\n\t unqElements=",unqElements)
    #print("\n\t unqElements=",unqElements.keys())
    return unqElements



def extractTableCC(tableCCID,unqElements,labels,nm,img1,phase,scndPhaseImages,folderName1):
    #print("**")

    all=[]
    tempImage=np.zeros(shape=(labels.shape[0],labels.shape[1]))
    tempImage2=np.zeros(shape=(labels.shape[0],labels.shape[1],3))

    tempImage2[:,:,0]=img1
    tempImage2[:,:,1]=img1
    tempImage2[:,:,2]=img1
    tempImage3=deepcopy(tempImage2)

    blackIndx=[]

    #print("\n\t img1",img1.shape)

    for ccID in tableCCID:
        tempIndx=np.where(labels == ccID)
        # print "\n\t 1.tempIndx=",tempIndx[0],"\t max=",np.max(tempIndx[0]),"\t min=",np.min(tempIndx[0])
        # print "\n\t 1.tempIndx=",tempIndx[1],"\t max=",np.max(tempIndx[1]),"\t min=",np.min(tempIndx[1])

        startX, startY=np.min(tempIndx[1]),np.min(tempIndx[0])
        endX, endY=np.max(tempIndx[1]),np.max(tempIndx[0])

        tempImage2 = cv2.rectangle(tempImage2, (startX, startY), (endX, endY), (0, 0, 255), 5)

        #print("\n\t 2.",np.max())

        #input("tempIndx")
        blackIndx.append(tempIndx)
        tempImage[tempIndx]=255
        #img1[tempIndx]=255
        all.append(tempIndx)
        #tempImage2[tempIndx] =255
        tempImage3[tempIndx] =255
    # tempImage3 [:,:,0]=tempImage2
    # tempImage3 [:,:,1]=tempImage2
    # tempImage3 [:,:,2]=tempImage2
    # tempImage3 [tempIndx,0]=255
    # tempImage3[tempIndx, 1] = 0
    # tempImage3[tempIndx, 2] = 0
        # tempImage2[tempIndx,1] =0
        # tempImage2[tempIndx,2] =0
        #img1[tempIndx] =
        # img1[tempIndx]=0
        # img1[tempIndx]=0

    # tempImage3= tempImage3
    # tempImage3 =
    # tempImage3 =


    imagename=nm.split("/")[-1]
    #cv2.imwrite(cwd+"//res//"+imagename+"_1_phase"+str(phase)+".jpg",img1)
    # cv2.imwrite(cwd+"//res//"+imagename+"_phase_colTab_"+str(phase)+".jpg",tempImage2)
    # cv2.imwrite(cwd+"//HE_Design_Data_Digest1//"+imagename+"_phase_colTab_"+str(phase)+".jpg",tempImage2)


    cv2.imwrite(cwd+"//"+folderName1+"//"+imagename+"_phase_colTab_"+str(phase)+".jpg",tempImage2)
    cv2.imwrite(cwd+"//"+folderName1+"//"+imagename+"_phase_colTab_"+str(phase)+".jpg",tempImage2)


    #cv2.imwrite(cwd + "//HE_Design_Data_Digest1//" + str(indx) + "_" + str(indxTemp) + "1_" + "_.jpg", image)
    if phase==1:
        # cv2.imwrite(cwd+"//delMe//"+imagename+"_phase"+"_table_"+str(phase)+".jpg",tempImage3)
        # cv2.imwrite(cwd+"//HE_Design_Data_Digest1//"+imagename+"_table"+"_0_"+str(phase)+".jpg",tempImage)

        cv2.imwrite(cwd+"//"+folderName1+"//"+imagename+"_phase"+"_table_"+str(phase)+".jpg",tempImage3)
        cv2.imwrite(cwd+"//"+folderName1+"//"+imagename+"_table"+"_0_"+str(phase)+".jpg",tempImage)


        scndPhaseImages.append(cwd+"//delMe//"+imagename+"_phase"+"_table_"+str(phase)+".jpg")
    #print("\n\t blackIndx=",)
    return scndPhaseImages,tempImage



def singleImage(nm,allRectTables,phase,scndPhaseImages,fileNameOriginal,folderName1):

    #nm="/home/kapitsa/Documents/Dataset/tableDetection/marmot_dataset_v1.0/data/English/Positive/Raw//10.1.1.1.2006_3.bmp"
    img1, fileName, original = readFile(nm, 0)

    '''
    1.get cc
    '''
    output, labels, stats = findConnectedComponents(255 - img1)
    print "\n\t no of unique labels=", len(np.unique(labels))
    # labels=labels[1:len(labels)]

    '''
    2. save individual cc
    '''

    '''
    for ii in np.unique(labels):
        # print "\n\t cc no=", ii
        # print "\n\t file name=",nm
        if ii == 0:
            continue
        if ii % 100 == 0:
            #print "\n\t image no=", indx, "\t tot images=", totImages
            print "\n\t cc no=", ii

        #original = displayAndSaveComponents(nm, original, labels, stats, ii, cc_threshold=50)
    '''

    '''
        below function extracts all unique CC which comes under proposed region
    '''
    unqElements=getCrops(labels,allRectTables)
    tableCCID=unqElements.keys()# unique CC id
    del tableCCID[0]  # remove background CC

    #print("2.unqElements=",tableCCID)

    '''
        plot those CC
    '''
    scndPhaseImages,tableImage=extractTableCC(tableCCID,unqElements,labels,nm,img1,phase,scndPhaseImages,folderName1)

    if phase==2:
        print "extract cell"

    return scndPhaseImages

if __name__=="__main__":
    readImages(dataPath)
