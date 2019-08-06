'''
    line segmentation
'''



import os
import pandas as pd
import cv2

csvpath="/home/wipro/PycharmProjects/hocr/fileconverter_batch/pdf//out.csv"


df=pd.read_csv(csvpath)

#print("\n\t df=",df.head())

fileName1="ProjectReport_page12.png"
image = cv2.imread("/home/wipro/PycharmProjects/hocr/fileconverter_batch/pdf/images//"+fileName1)
image1 = cv2.imread("/home/wipro/PycharmProjects/hocr/fileconverter_batch/pdf/images//"+fileName1)
#print("\n\t shape=",image.shape)

df1=df[df["fileName"]==fileName1]
print("\n\t df1=",df1.shape)

#print("\n\t df1.head()=",df1.head())
print("\n\t df1.columns()=",df1.columns)

yStart=0
yDict={}

yLoc1=df1.columns.get_loc("y1")
yLoc2=df1.columns.get_loc("y2")

print("",yLoc1,"\t ",yLoc2)

import numpy as np


def getNearestPoints(l,d,image1):

    sortCord=[]

    if len(l)>=1:
        #sortCord.append(l[0])
        print("\n\t l[0]=",l[0])
        dd = d[l[0]][0]
        tempX1, tempY1 = int(dd[0]), int(dd[1])
        tempX2, tempY2 = int(dd[2]), int(dd[3])
        print("\n\t 1.tempX1, tempY1 =",tempX1, tempY1 )
        print("\n\t 1.tempX1, tempY1 =",tempX2, tempY2 )

        sortCord.append([tempX1, tempY1,tempX2, tempY2])

    if len(l)>=2:
        #sortCord.append(l[1])
        dd = d[l[1]][0]
        tempX1, tempY1 = int(dd[0]), int(dd[1])
        tempX2, tempY2 = int(dd[2]), int(dd[3])

        print("\n\t 2.tempX1, tempY1 =",tempX1, tempY1 )
        print("\n\t 2.tempX1, tempY1 =",tempX2, tempY2 )

        sortCord.append([tempX1, tempY1,tempX2, tempY2])

    return sortCord


def lineSegmentation(df1):

    lineSegment={}
    print("\n\t this segments line")
    threshold=25
    image = cv2.imread("/home/wipro/PycharmProjects/hocr/fileconverter_batch/pdf/images//" + fileName1)
    image1 = cv2.imread("/home/wipro/PycharmProjects/hocr/fileconverter_batch/pdf/images//" + fileName1)
    lastX,lastY=None,None
    lastX2,lastY2=None,None
    startX,startY=None,None
    lineCount=0
    countWords=0
    w=""
    tempWord = []# stores actual word
    tempWordCord=[] # stores actual word cordinate for single line
    wordCorLine={} # this store line lever word cordinate information
    wordLine={}

    df=pd.DataFrame(columns=["fileName","x1","y1","x11","y11","lineNo"])


    def getWords(image11,curtLineNo,currentCor,countWords,wordCorLine,wordIndx,wordLine,cor,cor1,wordFeatureIndx):
        #print("\n\t\t this gives near words")

        x1,x2=currentCor[0],currentCor[2]
        y1,y2=currentCor[1],currentCor[3]

        overlapFlag=0
        forWord=wordLine[curtLineNo][wordIndx]
        cor.loc[wordFeatureIndx,"word"]=forWord

        '''
            current word coordinate
        '''
        cor.loc[wordFeatureIndx,"0"]=[x1,y1,x2,y2]
        cor1.loc[wordFeatureIndx,"0"]=forWord
        print("\n\t\t 2.current word coordinate:",currentCor)
        print("\n\t\t 2.current word:",wordLine[curtLineNo][wordIndx])
        print("\n\t\t 2.current line no:",curtLineNo)
        print("\n\t\t 2.last line dict=",wordLine[curtLineNo-1])

        try:
            print("\n\t\t 2.next line dict=",wordLine[curtLineNo+1])
        except Exception as e:
            pass

        lastWord,nextWord="",""

        for indx1,val1 in enumerate(wordCorLine[curtLineNo-1]):

            byWord=wordLine[curtLineNo-1][indx1]
            nextWord, prevWord = "", ""
            #print("\n\t val1=",val1)

            allTemp=val1
            #print("\n\t allTemp=",allTemp)

            xTemp1,xTemp2=allTemp[0],allTemp[2]
            yTemp1,yTemp2=allTemp[1],allTemp[3]


            if yTemp1 >=y1 or yTemp1 >=y2 or yTemp2 >=y1 or yTemp2 >=y2 :
                break

            # print("\n\t rule 1:",xTemp1<=x2 and xTemp2>x2)
            # print("\n\t rule 2:",xTemp2>=x1 and xTemp1<=x1)
            # print("\n\t rule 3:",xTemp1>=x1 and xTemp2>=x2)
            # print("\n\t rule 4:",xTemp1>=x1 and x2>=xTemp2)
            # print("\n\t rule 5:",x2>=xTemp1 and x2<=xTemp1)

            if xTemp1<=x2 and xTemp2>x2:
                #print("\n\t overlap 1")
                overlapFlag =1

            elif xTemp2>=x1 and xTemp1<=x1:
                #print("\n\t overlap2")
                overlapFlag =2
            elif xTemp1>=x1 and x2>=xTemp2:
                #print("\n\t overlap4")
                overlapFlag = 4

            elif x2>=xTemp1 and x2<=xTemp1:
                #print("\n\t overlap5")
                overlapFlag = 5


            if overlapFlag>0:
                # print("\n\t 2.word x1:",x1,"\t 2.x2:",x2)
                # print("\n\t 2.overlap word xTemp1:",xTemp1,"\t 2.xTemp2:",xTemp2)
                # print("\n\t 2.flag=",overlapFlag)
                cv2.rectangle(image11,(xTemp2, yTemp2), (xTemp1, yTemp1),(0, 255, 0), 5)
                cv2.rectangle(image11,(x1, y1), (x2, y2),(255,0, 0), 5)
                cv2.line(image1,(x1,y1),(x2,y2), (0, 0, 255), 3)
                cv2.line(image11,(xTemp2,yTemp2),(xTemp1,yTemp1), (0, 0, 255), 3)
                cv2.line(image11,(x1,y1),(xTemp2,yTemp2), (0, 255,0), 5)
                ims=cv2.resize(image11,(700,700))

                #print("\n\t forWOrd-",str(forWord),"\t byWord-",str(byWord))

                # cv2.imshow(str(forWord)+"_"+str(byWord)+"_"+str(nextWord)+"_"+str(prevWord), ims)
                # cv2.moveWindow(str(forWord)+"_"+str(byWord)+"_"+str(nextWord)+"_"+str(prevWord), 100, 100)
                # cv2.waitKey()
                overlapFlag=0
                #cv2.destroyAllWindows()

                '''
                    above word coordinate
                '''
                cor.loc[wordFeatureIndx, "8"] = [xTemp1, yTemp1, xTemp2, yTemp2]
                cor1.loc[wordFeatureIndx, "8"] = byWord

                print("\n\t 0.wordCorLine::>", len(wordCorLine[curtLineNo - 1]))
                print("\n\t 1.wordCorLine::>", len(wordCorLine[curtLineNo - 1][indx1 - 1]))
                print("\n\t 2.wordCorLine:", len(wordCorLine[curtLineNo - 1][indx1]))

                if indx1 > 0:
                    prevCord = wordCorLine[curtLineNo - 1][indx1 - 1]
                    xTempL0, xTempL1 = prevCord[0], prevCord[2]
                    yTempL0, yTempL1 = prevCord[1], prevCord[3]
                    print("\n\t above prev=", prevCord)
                    prevWord = wordLine[curtLineNo - 1][indx1 - 1]
                    print("\n\t above prevWord =", prevWord)

                    '''
                        above left word coordinate
                    '''
                    cor.loc[wordFeatureIndx, "7"] = [xTempL0, yTempL0, xTempL1, yTempL1]
                    cor1.loc[wordFeatureIndx, "7"] = prevWord

                if (indx1 + 1) < len(wordCorLine[curtLineNo - 1]):
                    nextCord = wordCorLine[curtLineNo - 1][indx1 + 1]
                    xTempR1, xTempR2 = nextCord[0], nextCord[2]
                    yTempR1, yTempR2 = nextCord[1], nextCord[3]
                    print("\n\t nextCord=", nextCord)

                    # nextCord=wordCorLine[curtLineNo - 1][indx1+1]

                    nextWord = wordLine[curtLineNo - 1][indx1 + 1]
                    print("\n\t nextWord =", nextWord)

                    '''
                        above right word coordinate
                    '''
                    cor.loc[wordFeatureIndx, "1"] = [xTempR1, yTempR1, xTempR2, yTempR2]
                    cor1.loc[wordFeatureIndx, "1"] = nextWord

                #del image1
                #input("check")


        #################

        for indx1,val1 in enumerate(wordCorLine[curtLineNo+1]):

            allTemp=val1
            xTemp1,xTemp2=allTemp[0],allTemp[2]
            yTemp1,yTemp2=allTemp[1],allTemp[3]

            '''
                below word coordinate
            '''
            cor.loc[wordFeatureIndx, "4"] =[xTemp1,yTemp1,xTemp2,yTemp2]


            print("\n\t 00.wordCorLine::>",len(wordCorLine[curtLineNo + 1]))
            print("\n\t 11.wordCorLine::>",len(wordCorLine[curtLineNo + 1][indx1-1]))
            print("\n\t 22.wordCorLine:",len(wordCorLine[curtLineNo + 1][indx1]))


            if yTemp1 >=y1 or yTemp1 >=y2 or yTemp2 >=y1 or yTemp2 >=y2 :
                break

            # print("\n\t rule 1:",xTemp1<=x2 and xTemp2>x2)
            # print("\n\t rule 2:",xTemp2>=x1 and xTemp1<=x1)
            # print("\n\t rule 3:",xTemp1>=x1 and xTemp2>=x2)
            # print("\n\t rule 4:",xTemp1>=x1 and x2>=xTemp2)
            # print("\n\t rule 5:",x2>=xTemp1 and x2<=xTemp1)

            if xTemp1<=x2 and xTemp2>x2:
                #print("\n\t overlap 1")
                overlapFlag =1

            elif xTemp2>=x1 and xTemp1<=x1:
                #print("\n\t overlap2")
                overlapFlag =2
            elif xTemp1>=x1 and x2>=xTemp2:
                #print("\n\t overlap4")
                overlapFlag = 4

            elif x2>=xTemp1 and x2<=xTemp1:
                #print("\n\t overlap5")
                overlapFlag = 5

            if overlapFlag > 0:
                # print("\n\t 2.word x1:",x1,"\t 2.x2:",x2)
                # print("\n\t 2.overlap word xTemp1:",xTemp1,"\t 2.xTemp2:",xTemp2)
                # print("\n\t 2.flag=",overlapFlag)
                cv2.rectangle(image11, (xTemp2, yTemp2), (xTemp1, yTemp1), (0, 255, 0), 5)
                cv2.rectangle(image11, (x1, y1), (x2, y2), (255, 0, 0), 5)
                cv2.line(image1, (x1, y1), (x2, y2), (0, 0, 255), 3)
                cv2.line(image11, (xTemp2, yTemp2), (xTemp1, yTemp1), (0, 0, 255), 3)
                cv2.line(image11, (x1, y1), (xTemp2, yTemp2), (0, 255, 0), 5)
                ims = cv2.resize(image11, (700, 700))

                # print("\n\t forWOrd-",str(forWord),"\t byWord-",str(byWord))
                # cv2.imshow(str(forWord) + "_" + str(byWord) + "_" + str(nextWord) + "_" + str(prevWord), ims)
                # cv2.moveWindow(str(forWord) + "_" + str(byWord) + "_" + str(nextWord) + "_" + str(prevWord), 100, 100)
                # cv2.waitKey()
                overlapFlag = 0
                #cv2.destroyAllWindows()

                if indx1 > 0:
                    prevCord = wordCorLine[curtLineNo + 1][indx1 - 1]
                    xTempL0, xTempL1 = prevCord[0], prevCord[2]
                    yTempL0, yTempL1 = prevCord[1], prevCord[3]
                    print("\n\t prev below line=", prevCord)
                    prevWord = wordLine[curtLineNo + 1][indx1 - 1]
                    print("\n\t prevWord =", prevWord)

                    '''
                        above left word coordinate
                    '''
                    cor.loc[wordFeatureIndx, "5"] = [xTempL0, yTempL0, xTempL1, yTempL1]
                    cor1.loc[wordFeatureIndx, "5"] = prevWord

                if (indx1 + 1) < len(wordCorLine[curtLineNo + 1]):
                    nextCord = wordCorLine[curtLineNo + 1][indx1 + 1]
                    xTempR1, xTempR2 = nextCord[0], nextCord[2]
                    yTempR1, yTempR2 = nextCord[1], nextCord[3]
                    print("\n\t nextCord=", nextCord)
                    nextWord = wordLine[curtLineNo + 1][indx1 + 1]
                    print("\n\t nextWord =", nextWord)

                    '''
                        above right word coordinate
                    '''
                    cor.loc[wordFeatureIndx, "3"] = [xTempR1, yTempR1, xTempR2, yTempR2]
                    cor1.loc[wordFeatureIndx, "3"] = nextWord

        #return image
        return cor,cor1,wordFeatureIndx


    for rowNo, row in df1.iterrows():

        #print("\n\t rowNo:",rowNo)

        print("\n\t 1.line no:",lineCount)
        print("\n\t\t 1.word no from csv:",countWords)
        print("\n\t\t 1.word=",df1.loc[rowNo,"word_1"])

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
        #print("\n\t ",abs(cuY-lastY)>threshold,"\t abs(cuY-lastY):",abs(cuY-lastY))

        if abs(cuY-lastY)>threshold:

            wordCorLine[lineCount] = tempWordCord
            tempWordCord=[]
            tempWordCord.append([cuX,cuY,cuX2,cuY2])
            lineSegment[lineCount]=[startX, startY,lastX2,lastY2]
            #cv2.line(image, (startX,startY), (xTemp2, yTemp2), (0, 0, 255), 3)
            #df = cellPushCordinate(df, rowNo, cuX, cuY, cuX2, cuY2,lineCount)
            wTemp=w.split("_")[-1][0]

            # getWords(image,lineCount, currentCor,countWords,wordCorLine)

            # try:
            #
            #     crop = image[startY:cuY2, startX:lastX]
            #     #crop = image[startX:cuX2,startY:cuY2] #cuX2,cuY2
            #     #print("\n\t crop=", crop.shape)
            #     #cv2.imshow("crop",crop)
            #     #cv2.imwrite("/home/wipro/PycharmProjects/hocr/fileconverter_batch/pdf//delMe//"+str(lineCount)+".jpg",crop)
            #
            # except Exception as e:
            #     pass

            '''
                entire row line segment
            '''
            #cv2.line(image, (startX, startY), (lastX2,lastY2), (255, 0, 0), 3)

            countWords=0

            winname = w+"_"+str(abs(cuY - lastY))

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
            # print("\n\t all word in dict=",wordLine[lineCount])

            cv2.namedWindow(winname)
            cv2.moveWindow(winname, 40, 30)
            ims = cv2.resize(image, (940, 940))
            cv2.imshow(winname, ims)
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

    ##def getWords(image,curtLineNo,currentCor,countWords,wordCorLine)

    print("\n\t ###################################################")

    cor=pd.DataFrame(columns=["word","0","1","2","3","4","5","6","7","8"])
    cor1=pd.DataFrame(columns=["word","0","1","2","3","4","5","6","7","8"])
    wordFeatureIndx=0

    totKeys=len(wordCorLine.keys())

    for curtLineNo in wordCorLine:

        print("\n\t Line no from dictionary=",curtLineNo)
        print("\n\t value:",wordCorLine[curtLineNo])
        print("\n\t number of word cordinates:",len(wordCorLine[curtLineNo]))

        print("\n\t allWords in current line=",wordLine[curtLineNo])
        print("\n\t number of word=",len(wordLine[curtLineNo]))

        if curtLineNo>1:
            print("\n\t lineNo:--->",curtLineNo)

            for wordIndx,currentCor1 in enumerate(wordCorLine[curtLineNo]):
                image11 = image

                try:
                    cor,cor1,wordFeatureIndx=getWords(image11, curtLineNo, currentCor1, countWords, wordCorLine,wordIndx,wordLine,cor,cor1,wordFeatureIndx)
                    wordFeatureIndx+=1
                    del image11
                except Exception as e:
                    print("\n\ exception")
                    input("exception")
                    pass


                #input("check")

    cor.to_csv("/home/wipro/PycharmProjects/hocr/fileconverter_batch//feature.csv")
    cor1.to_csv("/home/wipro/PycharmProjects/hocr/fileconverter_batch//feature1.csv")
    print("\n\t *******************************************************")
lineSegmentation(df1)



