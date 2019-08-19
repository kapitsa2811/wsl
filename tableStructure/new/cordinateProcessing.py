import copy
import os
import pandas as pd
import cv2
import sys
#from "/home/wipro/PycharmProjects/hocr/fileconverter_batch/extractTextFeatures//" import getWords
from getWords import *


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


def cordinateProcessing(fileName1,image,wordCorLine,wordLine,cor,cor1):

    #print("\n\t cordinateProcessing")

    wordFeatureIndx=cor.shape[0]
    totKeys=len(wordCorLine.keys())
    zeroIndexCount,lastIndexCount=0,0
    imageDim=image.shape


    try:
        for curtLineNo in wordCorLine:

            print("\n\t current line no:",curtLineNo)
            cor.loc[wordFeatureIndx, "lineNo"] = curtLineNo
            cor.loc[wordFeatureIndx, "wordIndex"] = curtLineNo
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


                if (curtLineNo+1)<(len(wordCorLine)) and curtLineNo>0 :
                #wordIndx<(len(wordCorLine[curtLineNo])) and  (curtLineNo+1)<(len(wordCorLine)): #
                    '''
                        for last word next set to high
                    '''

                    cor,cor1,wordFeatureIndx,image111=getWords(fileName1,image11, curtLineNo, currentCor1, wordCorLine,wordIndx,wordLine,cor,cor1,wordFeatureIndx)
                    #plot(image111,str(wordFeatureIndx))

                    wordFeatureIndx+=1
                elif curtLineNo==0 or (curtLineNo+1)==(len(wordCorLine)): # this should handle 1st and last line
                    #print("1st and last line handling")

                    if curtLineNo==0:
                        cor.loc[wordFeatureIndx, "1"] = [0,0, 0, 0]
                        cor.loc[wordFeatureIndx, "7"] = [0,0, 0, 0]
                        cor.loc[wordFeatureIndx, "8"] = [100000, 100000, 100000, 100000]
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

        print("\n\t\t zero index:",zeroIndexCount)
        print("\n\t\t last index:",lastIndexCount)

        #input("testing")
    except Exception as e:
        print("\n\t\t exception in coordinateProcessing")
        input("\n\t\t exception in coordinateProcessing ")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("\n\t\t exception location inside  cordinateProcessing:---->", exc_tb.tb_lineno)



    cv2.imwrite("/home/kapitsa/PycharmProjects/objectLocalization/wsl/tableStructure/delMe2//" + fileName1,image11)
                #input("check")


    print("\n\t\t cor=",cor.shape)

    #input("coordinate processing")

    return cor,cor1


