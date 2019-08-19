
'''
    line segmentation
'''

import copy
import os
import pandas as pd
import cv2
import sys
#from "/home/wipro/PycharmProjects/hocr/fileconverter_batch/extractTextFeatures//" import getWords

from getWords import *
from coordinateProcessing import *

cwd=os.getcwd()+"//"
csvpath=cwd+"//extractTextFeatures//csv//out.csv"

print("cwd=",cwd)

df=pd.read_csv(csvpath)

print("\n\t df=",df.head())

#
# fileName1="1_slastNormalCanvas.jpg"
# image = cv2.imread(cwd+"//image//"+fileName1)
# image1 = cv2.imread(cwd+"/image//"+fileName1)
# print("\n\t shape=",image.shape)
#
# df1=df[df["fileName"]==fileName1]
# print("\n\t df1=",df1.shape)

#print("\n\t df1.head()=",df1.head())
#print("\n\t df1.columns()=",df1.columns)

yStart=0
yDict={}


'''
    for all files present in folder
'''

cor = pd.DataFrame(columns=["fileName","lineNo","wordIndex","word", "0", "1", "2", "3", "4", "5", "6", "7", "8", "table"])
cor1 = pd.DataFrame(columns=["fileName","lineNo","wordIndex","word", "0", "1", "2", "3", "4", "5", "6", "7", "8", "table"])


# yLoc1=df1.columns.get_loc("y1")
# yLoc2=df1.columns.get_loc("y2")
#
# print("",yLoc1,"\t ",yLoc2)


def plot(image,name):
    ims = cv2.resize(image, (700, 700))

    # print("\n\t forWOrd-",str(forWord),"\t byWord-",str(byWord))

    cv2.imshow(name, ims)
    cv2.moveWindow(name, 700, 100)
    cv2.waitKey()
    # overlapFlag=0
    cv2.destroyAllWindows()


def lineSegmentation(df1,fileName1,cor,cor1):

    #try:
    wordCorLine={} # this store line level word cordinate information
    wordLine={}
    lineSegment={}
    #print("\n\t this segments line")
    threshold=10
    image = cv2.imread(cwd+"//extractTextFeatures//image//" + fileName1)

    print("\n\t shape=>>>",image.shape)

    #image1 = cv2.imread(cwd+"//image//" + fileName1)
    lastX,lastY=None,None
    lastX2,lastY2=None,None
    startX,startY=None,None
    lineCount=0
    countWords=0
    w=""
    tempWord = []# stores actual word
    tempWordCord=[] # stores actual word cordinate for single line
    totWordProcess=0 # no of words processed by line segmentation module

    #df=pd.DataFrame(columns=["fileName","x1","y1","x11","y11","lineNo","table"])


    '''
        line segmentation
    '''
    for rowNo, row in df1.iterrows():

        #print("\n\t rowNo:++++",rowNo)

        # print("\n\t 1.line no:",lineCount)
        # print("\n\t\t 1.word no from csv:",countWords)
        # print("\n\t\t 1.word=",df1.loc[rowNo,"word_1"])

        cuX,cuY= int(df1.loc[rowNo, 'x1']), int(df1.loc[rowNo,'y1'])
        cuX2,cuY2= int(df1.loc[rowNo, 'x2']), int(df1.loc[rowNo,'y2'])
        midX,midY=(cuX+cuX2)/2,(cuY+cuY2)/2 ## current cell mid coordinate
        currentCor=[cuX,cuY,cuX2,cuY2]

        w = df1.loc[rowNo, "word_1"]

        #print("\n\t cuX:",cuX,"\t cuY:",cuY)

        '''
            current line begining
        '''
        if countWords==0:
            startX, startY = cuX, cuY
            lastX,lastY=startX, startY

        if countWords==0 and rowNo==0:
            lastX,lastY=startX, startY

        '''
            word line
        '''
        #cv2.line(image, (cuX, cuY), (cuX2, cuY2), (0, 0, 255), 3)
        cv2.putText(image,str(rowNo),(cuX2, cuY),cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 0))#, lineType=cv2.LINE_AA
        #print("\n\t ",abs(cuY-lastY)>threshold,"\t abs(cuY-lastY):",abs(cuY-lastY))

        if abs(cuY-lastY)>threshold:

            wordCorLine[lineCount] = tempWordCord
            totWordProcess=totWordProcess+len(tempWordCord)
            tempWordCord=[]
            tempWordCord.append([cuX,cuY,cuX2,cuY2])
            lineSegment[lineCount]=[startX, startY,lastX2,lastY2]

            '''
                entire row line segment
            '''
            #cv2.line(image, (startX, startY), (lastX2,lastY2), (255, 0, 0), 3)

            countWords=0

            #print("\n\t cuY=",cuY,"\t lastY=",lastY)
            winname = str(w)+"_"+str(int(abs(cuY - lastY)))

            '''
                puts all words in last line to dictionary
            '''
            wordLine[lineCount]=tempWord
            #print("\n\t wordLine[lineCount]=",wordLine[lineCount])
            #print("\n\t last line co-ordinate:",wordCorLine[lineCount])

            tempWord=[]
            tempWord.append(df1.loc[rowNo, "word_1"])
            # print("\n\t words=",winname)
            # print("\n\t wTemp=",wTemp)
            #
            # print("\n\t all word 0in dict=",wordLine[lineCount])

            # cv2.namedWindow(winname)
            # cv2.moveWindow(winname, 40, 30)
            # ims = cv2.resize(image, (940, 940))
            # cv2.imshow(winname, ims)
            #cv2.waitKey()
            #cv2.destroyWindow(winname)

            startX, startY = cuX, cuY
            lineCount+=1
        else:

            try:
                w = w + "\t " + str(df1.loc[rowNo, "word_1"])
            except Exception as e:
                w=w
            tempWord.append(df1.loc[rowNo, "word_1"])
            #tempLastLineWords[df1.loc[rowNo, "word_1"]]=[cuX,cuY,cuX2,cuY2]
            try:

                #wordCorLine[lineCount]=[cuX,cuY,cuX2,cuY2]
                tempWordCord.append([cuX,cuY,cuX2,cuY2])

                #xTemp11,yTemp11=xTemp1,yTemp1
            except Exception as e:
                pass

        lastX, lastY = cuX,cuY
        lastX2, lastY2 = cuX2,cuY2
        countWords+=1


    '''
        inserts last line on page not working
    '''
    # lineCount += 1
    # wordCorLine[lineCount] = tempWordCord

    #print("\n\t outside the for loop")

    totWordProcess = totWordProcess + len(tempWordCord)
    delmePath="/home/wipro/PycharmProjects/hocr/fileconverter_batch/extractTextFeatures/delMe//"

    cv2.imwrite(delmePath+fileName1,image)

    # print("\n\t keys:",len(wordCorLine.keys()),"\t df1.shape:",df1.shape,"\t rowNo:",rowNo)
    # input("no of keys")

    '''
        extracts co-ordinate level features for each coordinate present in wordCorLine
    '''
    print("\n\t image shaping::::",image.shape)
    cor,cor1=cordinateProcessing(fileName1,image,wordCorLine,wordLine,cor,cor1)

    return cor,cor1,totWordProcess
    # except Exception as e:
    #     print("\n\t processCordinatesIntermediate")
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     print("\n\t exception location:---->", exc_tb.tb_lineno)




#imagePath=cwd+"//images//"
imagePath=cwd+"//extractTextFeatures//image//"


for fileIndx,fileName in enumerate(os.listdir(imagePath)):

    #print("\n\t imagePath=",imagePath)
    print("\n\t is file:",os.path.isfile(imagePath+fileName))
    print("\n\t fileIndx:",fileIndx,"\t fileName:",fileName)

    df1 = df[df["fileName"] == fileName]
    df1.reset_index(inplace=True)

    #try:

    oldCorShape=cor.shape

    #print("\n\t 1.oldCorShape====",oldCorShape)
    cor,cor1,totWordProcess=lineSegmentation(df1,fileName,cor,cor1)
    newCorShape=cor.shape
    print("\n\t 2.oldCorShape=",oldCorShape,"\t newCorShape=",newCorShape)
    print("\n\t lines adde:",newCorShape[0]-oldCorShape[0])
    print("\n\t df1 shape=",df1.shape)
    print("\n\t tempWordCord=",totWordProcess)
    newCorShape =oldCorShape
    input("shape")
    # except Exception as e:
    #
    #     print("\n\t Exception in processCordinateIntermediate:",e)
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     print("\n\t Exception in for loop:::", fname, exc_tb.tb_lineno)
    #     input("processCordinateIntermediate")




    cor.to_csv(cwd+"//extractTextFeatures//csv//feature.csv")
    cor1.to_csv(cwd+"//extractTextFeatures//csv//feature1.csv")
    #cv2.imwrite(cwd+"//featureImage//"+fileName1+".png",image11)


