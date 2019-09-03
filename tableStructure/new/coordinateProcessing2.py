import copy
import os
import pandas as pd
import cv2
import sys
#from "/home/wipro/PycharmProjects/hocr/fileconverter_batch/extractTextFeatures//" import getWords
import getWords #import *


def initialize(cor,cor1,wordFeatureIndx,fileName1):


    cor.loc[wordFeatureIndx, "fileName"] = fileName1
    cor.loc[wordFeatureIndx, "0"] = [0, 0, 0, 0]
    cor.loc[wordFeatureIndx, "1"] = [0, 0, 0, 0]
    cor.loc[wordFeatureIndx, "2"] = [0, 0, 0, 0]
    cor.loc[wordFeatureIndx, "3"] = [0, 0, 0, 0]

    cor.loc[wordFeatureIndx, "4"] = [0, 0, 0, 0]
    cor.loc[wordFeatureIndx, "5"] = [0, 0, 0, 0]
    cor.loc[wordFeatureIndx, "6"] = [0, 0, 0, 0]
    cor.loc[wordFeatureIndx, "7"] = [0, 0, 0, 0]
    cor.loc[wordFeatureIndx, "8"] = [0, 0, 0, 0]

    return cor,cor1


def plot(image,name):
    ims = cv2.resize(image, (700, 700))

    # print("\n\t forWOrd-",str(forWord),"\t byWord-",str(byWord))

    cv2.imshow(name, ims)
    cv2.moveWindow(name, 700, 100)
    cv2.waitKey()
    # overlapFlag=0
    cv2.destroyAllWindows()



def cordinateProcessing(fileName1,image,wordCorLine,wordLine,cor,cor1):

    #print("\n\t cordinateProcessing")

    wordFeatureIndx=cor.shape[0]
    totKeys=len(wordCorLine.keys())
    zeroIndexCount,lastIndexCount=0,0
    imageDim=image.shape

    for curtLineNo in wordCorLine:
        #try:
        print("\n\t current line no:",curtLineNo)
        #cor.loc[wordFeatureIndx, "lineNo"] = curtLineNo
        #cor.loc[wordFeatureIndx, "wordIndex"] = curtLineNo
        #print("\n\t Line no from dictionary=",curtLineNo,"\t total lines=",len(wordCorLine))
        # print("\n\t value:",wordCorLine[curtLineNo])
        # print("\n\t number of word cordinates:",len(wordCorLine[curtLineNo]))
        # print("\n\t allWords in current line=",wordLine[curtLineNo])
        # print("\n\t number of word=",len(wordLine[curtLineNo]))

        '''
            requires previous line co-ordinates so below condition
        '''

        #print("\n\t lineNo:--->",curtLineNo)

        for wordIndx,currentCor1 in enumerate(wordCorLine[curtLineNo]):
            image11 = image

            cor.loc[wordFeatureIndx, "fileName"] = fileName1
            cor.loc[wordFeatureIndx, "lineNo"] = curtLineNo
            #cor.loc[wordFeatureIndx, "wordIndex"] = curtLineNo

            cuLinePrev,cuLineNext="",""
            #cor,cor1=initialize(cor, cor1, wordFeatureIndx,fileName1)

            '''
                adds the previous words if 1st word then hard code
            '''

            if wordIndx == 0:
                cuLinePrev =[0,0,0,0]
                zeroIndexCount+=1
            else:
                cuLinePrev=wordCorLine[curtLineNo][wordIndx-1] # previous word
            #print("\n\t cuLinePrev=",cuLinePrev)
            cor.loc[wordFeatureIndx, "6"] = cuLinePrev
            #print("\n\t cuLineNext =",cuLineNext)

            '''
                last word in the line
            '''

            if wordIndx == (len(wordCorLine[curtLineNo]) - 1):
                cor.loc[wordFeatureIndx, "2"] = [imageDim[0], imageDim[1], imageDim[0], imageDim[1]]
                lastIndexCount += 1

            else:
                cuLineNext = wordCorLine[curtLineNo][wordIndx + 1]
                cor.loc[wordFeatureIndx, "2"] = cuLineNext
                # print("\n\t cuLineNext =",cuLineNext)

            cor.loc[wordFeatureIndx, "8"] = [0,0,0,0]
            print("\n\t (curtLineNo+1)<len(wordCorLine)=",(curtLineNo+1)<len(wordCorLine),"\t curtLineNo>0:",curtLineNo>0)
            if (curtLineNo+1)<len(wordCorLine) and curtLineNo>0 :
            #wordIndx<(len(wordCorLine[curtLineNo])) and  (curtLineNo+1)<(len(wordCorLine)): #

                print("\n\t curtLineNo:",curtLineNo)
                '''
                    for last word next set to high
                '''
                print("\n\t calling getWords")
                cor,cor1,wordFeatureIndx,image11=getWords.getWords(fileName1,image11, curtLineNo, currentCor1, wordCorLine,wordIndx,wordLine,cor,cor1,wordFeatureIndx)
                #plot(image111,str(wordFeatureIndx))

                #wordFeatureIndx+=1
            elif curtLineNo==0 or (curtLineNo+1)==(len(wordCorLine)): # this should handle 1st and last line
                #print("1st and last line handling")
                cor.loc[wordFeatureIndx, "8"] = [currentCor1[0], currentCor1[1], currentCor1[2], currentCor1[3]]
                cv2.line(image11, (currentCor1[0], currentCor1[1]), (currentCor1[2], currentCor1[3]), (0,0, 0), 2)
                if curtLineNo==0:
                    cor.loc[wordFeatureIndx, "1"] = [0,0, 0, 0]
                    cor.loc[wordFeatureIndx, "7"] = [0,0, 0, 0]

                elif (curtLineNo+1)==(len(wordCorLine)):
                    cor.loc[wordFeatureIndx, "3"] = [0,0, 0, 0]
                    cor.loc[wordFeatureIndx, "4"] = [0,0, 0, 0]
                    cor.loc[wordFeatureIndx, "5"] = [100000, 100000, 100000, 100000]


                # if wordIndx == (len(wordCorLine[curtLineNo])-1):
                #     cor.loc[wordFeatureIndx, "2"] = [100000, 100000, 100000, 100000]
                # else:
                #     cuLineNext =wordCorLine[curtLineNo][wordIndx+1]
                #     cor.loc[wordFeatureIndx, "2"] = cuLineNext
                #     #print("\n\t cuLineNext =",cuLineNext)

                #del image11
            #cv2.line(image11, (currentCor1[0], currentCor1[1]), (xTemp2, yTemp2), (255, 255, 0), 5)

            try:
                nm=str(cor.loc[wordFeatureIndx,"8"])
            except Exception as e:
                nm="NoName"

            curCord=currentCor1


            aboveCordinate = cor.loc[wordFeatureIndx, "8"]
            print("\n\t curCord=",curCord)
            print("\n\t aboveCordinate =",aboveCordinate)
            cv2.line(image11, (curCord[0], curCord[1]), (aboveCordinate[2], aboveCordinate[3]),   (255, 0, 255), 3)
            print("\n\t NM=",nm)
            #plot(image11,nm)

            wordFeatureIndx += 1
                #input("testing")
        # except Exception as e:
        #     print("\n\t wordIndex=",wordIndx,"\t line no:",curtLineNo)
        #     print("\n\t\t exception in coordinateProcessing:",e)
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #     print("\n\t\t exception location inside  cordinateProcessing:---->", exc_tb.tb_lineno)
        #     input("exception pause")
        #     pass

    print("\n\t\t zero index:",zeroIndexCount)
    print("\n\t\t last index:",lastIndexCount)

    cv2.imwrite("/home/kapitsa/PycharmProjects/objectLocalization/wsl/tableStructure/delMe2//" + fileName1,image11)
                #input("check")


    print("\n\t\t cor=",cor.shape)

    #input("coordinate processing")

    return cor,cor1


