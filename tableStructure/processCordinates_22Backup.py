'''
    line segmentation
'''


import copy
import os
import pandas as pd
import cv2
import sys

cwd=os.getcwd()+"//"
csvpath=cwd+"//csv//out.csv"


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

cor = pd.DataFrame(columns=["fileName","word", "0", "1", "2", "3", "4", "5", "6", "7", "8", "table"])
cor1 = pd.DataFrame(columns=["fileName","word", "0", "1", "2", "3", "4", "5", "6", "7", "8", "table"])


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

def getWords(fileName1,image11,curtLineNo,currentCor,wordCorLine,wordIndx,wordLine,cor,cor1,wordFeatureIndx):


        try:
            #print("\n\t\t this gives near words")

            x1,x2=currentCor[0],currentCor[2]
            y1,y2=currentCor[1],currentCor[3]

            '''
                table coordinate from original file
            '''
            annot1 = annot[annot["fileName"] == fileName]
            #print("\n\t annot1:\n\t",[annot1["x1"],annot1["y1"],annot1["x2"],annot1["y2"]])

            #print("\n\t type=",type(annot1["x1"]))
            #print("\n\t annot1:\n\t",annot1["x1"].values[0])
            # print("\n\t annot1:\n\t",annot1["y1"][1])
            # print("\n\t annot1:\n\t",annot1["x2"][1])
            # print("\n\t annot1:\n\t",annot1["y1"][1])
            #input("check")

            forWord=wordLine[curtLineNo][wordIndx]

            '''
                table related code
            '''

            t,oriX, oriY, oriX1, oriY1=tableInsert(fileName1,image11,cor,currentCor,annot1,wordFeatureIndx,forWord)
            cv2.rectangle(image11, (oriX, oriX1), (oriY, oriY1), (0, 0, 255), 5)
            if t >= 0:
                 print("\n\t t=",t)
                 cor.loc[wordFeatureIndx, "table"] = 1
                 cv2.rectangle(image11, (currentCor[0], currentCor[1]), (currentCor[2], currentCor[3]), (0, 255, 0), 2)
                 #cv2.rectangle(image11, (currentCor[0], currentCor[2]), (currentCor[1], currentCor[3]), (0, 0, 255), 5)


                 #cv2.rectangle(image11, (oriX1, oriY1), (oriX, oriY), (0,255,0), 5)
                 #cv2.rectangle(image11, (oriX, oriX1), (oriY, oriY1), (0,0, 255), 5)
                 #cv2.rectangle(image11, (oriX, oriY), (oriX1, oriY1), (0,0, 255), 5)
                 #print("\n\t t=", t)
                 #input("t")
                 name=str(str(currentCor[0])+"\t"+ str(currentCor[1])+"\t"+str(currentCor[2])+"\t"+ str(currentCor[3])+"\t")
                 #plot(image11, name)

            else:
                 cor.loc[wordFeatureIndx, "table"] = 0

            #print("\n\t t=>>>", t)



            overlapFlag=0

            cor.loc[wordFeatureIndx,"word"]=forWord

            '''
                current word coordinate
            '''
            cor.loc[wordFeatureIndx,"0"]=[x1,y1,x2,y2]
            cor1.loc[wordFeatureIndx,"0"]=forWord
            #cor.loc[wordFeatureIndx,"table"]=1

            # print("\n\t\t 2.current word coordinate:",currentCor)
            # print("\n\t\t 2.current word:",wordLine[curtLineNo][wordIndx])
            # print("\n\t\t 2.current line no:",curtLineNo)
            # print("\n\t\t 2.last line dict=",wordLine[curtLineNo-1])

            # try:
            #     print("\n\t\t 2.next line dict=",wordLine[curtLineNo+1])
            # except Exception as e:
            #     pass

            lastWord,nextWord="",""

            '''
                gathers last line neccessary features
            '''

            for indx1,val1 in enumerate(wordCorLine[curtLineNo-1]):

                #print("***********************************************************")
                image3=image11 #copy.deepcopy(image11)
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
                    #cv2.rectangle(image3,(xTemp2, yTemp2), (xTemp1, yTemp1),(0, 255, 0), 5)
                    #cv2.rectangle(image3,(x1, y1), (x2, y2),(255,0, 0), 5)
                    cv2.line(image3,(x1,y1),(x2,y2), (0, 0, 255), 3)
                    #cv2.line(image3,(xTemp2,yTemp2),(xTemp1,yTemp1), (0, 0, 255), 3)
                    #cv2.line(image3,(x1,y1),(xTemp2,yTemp2), (0, 255,0), 5)
                    ims=cv2.resize(image3,(700,700))
                    overlapFlag=0
                    #print("\n\t forWOrd-",str(forWord),"\t byWord-",str(byWord))
                    name=str(forWord)+"_"+str(byWord)+"_"+str(nextWord)+"_"+str(prevWord)
                    '''
                    cv2.imshow(name, ims)
                    cv2.moveWindow(name, 100, 100)
                    cv2.waitKey()
                    '''
                    #plot(image3,name)

                    '''
                        above word coordinate
                    '''

                    cor.loc[wordFeatureIndx, "8"] = [xTemp1, yTemp1, xTemp2, yTemp2]
                    cor1.loc[wordFeatureIndx, "8"] = byWord

                    # print("\n\t 0.wordCorLine::>", len(wordCorLine[curtLineNo - 1]))
                    # print("\n\t 1.wordCorLine::>", len(wordCorLine[curtLineNo - 1][indx1 - 1]))
                    # print("\n\t 2.wordCorLine:", len(wordCorLine[curtLineNo - 1][indx1]))

                    if indx1 > 0:
                        prevCord = wordCorLine[curtLineNo - 1][indx1 - 1]
                        xTempL0, xTempL1 = prevCord[0], prevCord[2]
                        yTempL0, yTempL1 = prevCord[1], prevCord[3]
                        #print("\n\t above prev=", prevCord)
                        prevWord = wordLine[curtLineNo - 1][indx1 - 1]
                        #print("\n\t above prevWord =", prevWord)

                        '''
                            above left word coordinate
                        '''
                        cor.loc[wordFeatureIndx, "7"] = [xTempL0, yTempL0, xTempL1, yTempL1]
                        cor1.loc[wordFeatureIndx, "7"] = prevWord

                    if (indx1 + 1) < len(wordCorLine[curtLineNo - 1]):
                        nextCord = wordCorLine[curtLineNo - 1][indx1 + 1]
                        xTempR1, xTempR2 = nextCord[0], nextCord[2]
                        yTempR1, yTempR2 = nextCord[1], nextCord[3]
                        #print("\n\t nextCord=", nextCord)

                        # nextCord=wordCorLine[curtLineNo - 1][indx1+1]

                        nextWord = wordLine[curtLineNo - 1][indx1 + 1]
                        #print("\n\t nextWord =", nextWord)

                        '''
                            above right word coordinate
                        '''
                        cor.loc[wordFeatureIndx, "1"] = [xTempR1, yTempR1, xTempR2, yTempR2]
                        cor1.loc[wordFeatureIndx, "1"] = nextWord

            #plot(image11, name)
            '''
                next line features
            '''

            for indx1,val1 in enumerate(wordCorLine[curtLineNo+1]):

                allTemp=val1
                xTemp1,xTemp2=allTemp[0],allTemp[2]
                yTemp1,yTemp2=allTemp[1],allTemp[3]

                '''
                    below word coordinate
                '''
                cor.loc[wordFeatureIndx, "4"] =[xTemp1,yTemp1,xTemp2,yTemp2]

                # print("\n\t 00.wordCorLine::>",len(wordCorLine[curtLineNo + 1]))
                # print("\n\t 11.wordCorLine::>",len(wordCorLine[curtLineNo + 1][indx1-1]))
                # print("\n\t 22.wordCorLine:",len(wordCorLine[curtLineNo + 1][indx1]))

                #
                # if yTemp1 >=y1 or yTemp1 >=y2 or yTemp2 >=y1 or yTemp2 >=y2 :
                #     break

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
                    #print("\n\t 2.flag=",overlapFlag)
                    #cv2.rectangle(image3, (xTemp2, yTemp2), (xTemp1, yTemp1), (0, 255, 0), 5)
                    cv2.rectangle(image3, (x1, y1), (x2, y2), (255, 0, 0), 5)
                    #cv2.line(image3, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    #cv2.line(image3, (xTemp2, yTemp2), (xTemp1, yTemp1), (0, 0, 255), 3)
                    cv2.line(image3, (x1, y1), (xTemp2, yTemp2), (255, 255, 0), 5)
                    #ims = cv2.resize(image3, (700, 700))

                    # print("\n\t forWOrd-",str(forWord),"\t byWord-",str(byWord))
                    # cv2.imshow(str(forWord) + "_" + str(byWord) + "_" + str(nextWord) + "_" + str(prevWord), ims)
                    # cv2.moveWindow(str(forWord) + "_" + str(byWord) + "_" + str(nextWord) + "_" + str(prevWord), 100, 100)
                    # cv2.waitKey()
                    #plot(image3,name)
                    overlapFlag = 0
                    #cv2.destroyAllWindows()

                    if indx1 > 0:
                        prevCord = wordCorLine[curtLineNo + 1][indx1 - 1]
                        xTempL0, xTempL1 = prevCord[0], prevCord[2]
                        yTempL0, yTempL1 = prevCord[1], prevCord[3]
                        #print("\n\t prev below line=", prevCord)
                        prevWord = wordLine[curtLineNo + 1][indx1 - 1]
                        #print("\n\t prevWord =", prevWord)

                        '''
                            above left word coordinate
                        '''
                        cor.loc[wordFeatureIndx, "5"] = [xTempL0, yTempL0, xTempL1, yTempL1]
                        cor1.loc[wordFeatureIndx, "5"] = prevWord

                    if (indx1 + 1) < len(wordCorLine[curtLineNo + 1]):
                        nextCord = wordCorLine[curtLineNo + 1][indx1 + 1]
                        xTempR1, xTempR2 = nextCord[0], nextCord[2]
                        yTempR1, yTempR2 = nextCord[1], nextCord[3]
                        #print("\n\t nextCord=", nextCord)
                        nextWord = wordLine[curtLineNo + 1][indx1 + 1]
                        #print("\n\t nextWord =", nextWord)

                        '''
                            above right word coordinate
                        '''
                        cor.loc[wordFeatureIndx, "3"] = [xTempR1, yTempR1, xTempR2, yTempR2]
                        cor1.loc[wordFeatureIndx, "3"] = nextWord

            #return image
            return cor,cor1,wordFeatureIndx,image11
        except Exception as e:
            print("\n\t exception in getWords:",e)
            import sys
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("\n\t line no::", fname, exc_tb.tb_lineno)
            input("exception in getWords")



def lineSegmentation(df1,fileName1,cor,cor1):

    wordCorLine={} # this store line level word cordinate information
    wordLine={}
    lineSegment={}
    #print("\n\t this segments line")
    threshold=10
    image = cv2.imread(cwd+"//images//" + fileName1)

    #print("\n\t shape=>>>",image.shape)

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

        print("\n\t rowNo:",rowNo)

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

    totWordProcess = totWordProcess + len(tempWordCord)
    delmePath="/home/kapitsa/PycharmProjects/objectLocalization/wsl/tableStructure/delMe//"

    cv2.imwrite(delmePath+fileName1,image)

    # print("\n\t keys:",len(wordCorLine.keys()),"\t df1.shape:",df1.shape,"\t rowNo:",rowNo)
    # input("no of keys")

    '''
        extracts co-ordinate level features for each coordinate present in wordCorLine
    '''
    cor,cor1=cordinateProcessing(fileName1,image,wordCorLine,wordLine,cor,cor1)
    print("\n\t ###################################################",image.shape)

    return cor,cor1,totWordProcess


def cordinateProcessing(fileName1,image,wordCorLine,wordLine,cor,cor1):

    wordFeatureIndx=cor.shape[0]
    totKeys=len(wordCorLine.keys())

    for curtLineNo in wordCorLine:

        # print("\n\t Line no from dictionary=",curtLineNo,"\t total lines=",len(wordCorLine))
        # print("\n\t value:",wordCorLine[curtLineNo])
        # print("\n\t number of word cordinates:",len(wordCorLine[curtLineNo]))
        # print("\n\t allWords in current line=",wordLine[curtLineNo])
        # print("\n\t number of word=",len(wordLine[curtLineNo]))

        '''
            requires previous line co-ordinates so below condition
        '''

        if curtLineNo>1:
            #print("\n\t lineNo:--->",curtLineNo)

            for wordIndx,currentCor1 in enumerate(wordCorLine[curtLineNo]):
                image11 = image

                try:

                    cuLinePrev,cuLineNext="",""
                    cor,cor1=initialize(cor, cor1, wordFeatureIndx,fileName1)

                    '''
                        adds the previous words if 1st word then hard code
                    '''
                    if 1:

                        if wordIndx == 0:
                            cuLinePrev =[0,0,0,0]

                        cuLinePrev=wordCorLine[curtLineNo][wordIndx-1] # previous word
                        #print("\n\t cuLinePrev=",cuLinePrev)
                        cor.loc[wordFeatureIndx, "6"] = cuLinePrev
                        #print("\n\t cuLineNext =",cuLineNext)

                    '''
                        last word in the line
                    '''

                    if wordIndx<(len(wordCorLine[curtLineNo])) and  (curtLineNo+1)<(len(wordCorLine)): #(wordIndx+1)<(len(wordCorLine[curtLineNo])) and  (curtLineNo+1)<(len(wordCorLine)) :

                        '''
                            for last word next set to high
                        '''
                        if wordIndx == (len(wordCorLine[curtLineNo])):
                            cor.loc[wordFeatureIndx, "2"] = [100000, 100000, 100000, 100000]
                        else:
                            cuLineNext =wordCorLine[curtLineNo][wordIndx+1]
                            cor.loc[wordFeatureIndx, "2"] = cuLineNext
                            #print("\n\t cuLineNext =",cuLineNext)

                        cor,cor1,wordFeatureIndx,image111=getWords(fileName1,image11, curtLineNo, currentCor1, wordCorLine,wordIndx,wordLine,cor,cor1,wordFeatureIndx)
                        #plot(image111,str(wordFeatureIndx))

                        wordFeatureIndx+=1
                        del image11
                except Exception as e:
                    print("\n\ exception")

                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print("\n\t exception location:---->", exc_tb.tb_lineno)

                    #input("exception")
                    pass

    cv2.imwrite("/home/kapitsa/PycharmProjects/objectLocalization/wsl/tableStructure/delMe2//" + fileName1,image11)
                #input("check")

    return cor,cor1



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


def tableInsert(fileName1,image11,cor,currentCor,annot1,wordFeatureIndx,forWord):

    t=0
    try:
        #print("inside 1")

        from shapely.geometry import Polygon
        #print("inside 2")
        x1, x2 = currentCor[0], currentCor[2]
        y1, y2 = currentCor[1], currentCor[3]
        #print("inside 3")

        #print("\n\t ------>",annot1.values[0][0])


        '''
            table coordinates
        '''

        oriX, oriY, oriX1, oriY1 = annot1.values[0][2], annot1.values[0][3], annot1.values[0][4], annot1.values[0][5]
        #print("inside 4")
        #print("\n\t co-ordinates:",oriX, oriY, oriX1, oriY1 )
        #print("\n\t x1=",x1)


        # if (x1>oriX and x1<oriX1 and x2>oriX and x2<oriX1 ):
        #     if (y1<oriY and y1>oriY1 and y2<oriY1 and y2>oriY1):
        #         t=1
        # else:
        #     t=0


        if (x1>oriX and x1<oriX1) and (y1>oriY and y1<oriY1):
            if (x2>oriX and x2<oriX1) and (y2>oriY and y2<oriY1):
                t=1
                print("\n\t fileName=",fileName1)
                print("\n\t rectangle:",(oriX, oriY),"\t",(oriX1, oriY1))
                print("\n\t coordinate:",(x1, y1),"\t",(x2, y2))
                print("\n\t word in table:",forWord)
                #input("rectangle")
        else:
            t=-1
        # a = Polygon([(oriX, oriY), (oriX1, oriY), (oriX1, oriY1), (oriX, oriY1)])
        # b = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y1)])

        #t = a.intersection(b).area / a.union(b).area
    except Exception as e:

        print("\n\t e:",e)
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("\n\t line no::", fname, exc_tb.tb_lineno)
        input("exception")

    return t,oriX, oriY, oriX1, oriY1

imagePath=cwd+"//images//"


annotateFilePath="/home/kapitsa/PycharmProjects/objectLocalization/wsl/publicationData/8/tableRelatedAll/delMe//train.csv"

annot=pd.read_csv(annotateFilePath)

for fileIndx,fileName in enumerate(os.listdir(imagePath)):

    #print("\n\t imagePath=",imagePath)
    print("\n\t is file:",os.path.isfile(imagePath+fileName))
    print("\n\t fileIndx:",fileIndx,"\t fileName:",fileName)

    df1 = df[df["fileName"] == fileName]
    df1.reset_index(inplace=True)

    #print("\n\t df1 =",df1.head())
    #input("check df")

    #cor.loc[rowNo, "0"]
    try:

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
    except Exception as e:
        print("\n\t Exception in lineSegmentation:",e)
        import sys

        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("\n\t Exception in for loop:::", fname, exc_tb.tb_lineno)
        input("exception in getWords")
        pass



    cor.to_csv(cwd+"//csv//feature.csv")
    cor1.to_csv(cwd+"//csv//feature1.csv")
    #cv2.imwrite(cwd+"//featureImage//"+fileName1+".png",image11)


