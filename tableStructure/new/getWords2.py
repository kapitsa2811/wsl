import cv2
import os
import pandas as pd


annotateFilePath="/home/wipro/PycharmProjects/wsl/wsl-master/publicationData/9/tableRelatedAll/delMe//train.csv"
annot=pd.read_csv(annotateFilePath)


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

def plot(image,name):
    ims = cv2.resize(image, (700, 700))

    # print("\n\t forWOrd-",str(forWord),"\t byWord-",str(byWord))

    cv2.imshow(name, ims)
    cv2.moveWindow(name, 700, 100)
    cv2.waitKey()
    # overlapFlag=0
    cv2.destroyAllWindows()


def getWords(fileName1, image11, curtLineNo, currentCor, wordCorLine, wordIndx, wordLine, cor, cor1, wordFeatureIndx):
    try:
        #print("\n\t\t this gives near words")

        #input("inside getWords")

        x1, x2 = currentCor[0], currentCor[2]
        y1, y2 = currentCor[1], currentCor[3]
        top=[x1,y1,x2,y2]


        '''
            table coordinate from original file
        '''
        annot1 = annot[annot["fileName"] == fileName1]
        # print("\n\t annot1:\n\t",[annot1["x1"],annot1["y1"],annot1["x2"],annot1["y2"]])this gives near words

        # print("\n\t type=",type(annot1["x1"]))
        # print("\n\t annot1:\n\t",annot1["x1"].values[0])
        # print("\n\t annot1:\n\t",annot1["y1"][1])
        # print("\n\t annot1:\n\t",annot1["x2"][1])
        # print("\n\t annot1:\n\t",annot1["y1"][1])
        # input("check")

        forWord = wordLine[curtLineNo][wordIndx]

        '''
            table related code
        '''
        '''
        t, oriX, oriY, oriX1, oriY1 = tableInsert(fileName1, image11, cor, currentCor, annot1, wordFeatureIndx, forWord)
        cv2.rectangle(image11, (oriX, oriX1), (oriY, oriY1), (0, 0, 255), 5)
        if t >= 0:
            print("\n\t t=", t)
            cor.loc[wordFeatureIndx, "table"] = 1
            cv2.rectangle(image11, (currentCor[0], currentCor[1]), (currentCor[2], currentCor[3]), (0, 255, 0), 2)
            # cv2.rectangle(image11, (currentCor[0], currentCor[2]), (currentCor[1], currentCor[3]), (0, 0, 255), 5)

            # cv2.rectangle(image11, (oriX1, oriY1), (oriX, oriY), (0,255,0), 5)
            # cv2.rectangle(image11, (oriX, oriX1), (oriY, oriY1), (0,0, 255), 5)
            # cv2.rectangle(image11, (oriX, oriY), (oriX1, oriY1), (0,0, 255), 5)
            # print("\n\t t=", t)
            # input("t")
            name = str(str(currentCor[0]) + "\t" + str(currentCor[1]) + "\t" + str(currentCor[2]) + "\t" + str(
                currentCor[3]) + "\t")
            # plot(image11, name)

        else:
            cor.loc[wordFeatureIndx, "table"] = 0

        # print("\n\t t=>>>", t)
        '''
        overlapFlag = 0

        cor.loc[wordFeatureIndx, "word"] = forWord

        '''
            current word coordinate
        '''
        cor.loc[wordFeatureIndx, "0"] = [x1, y1, x2, y2]
        cor1.loc[wordFeatureIndx, "0"] = forWord
        # cor.loc[wordFeatureIndx,"table"]=1

        # print("\n\t\t 2.current word coordinate:",currentCor)
        # print("\n\t\t 2.current word:",wordLine[curtLineNo][wordIndx])
        # print("\n\t\t 2.current line no:",curtLineNo)
        # print("\n\t\t 2.last line dict=",wordLine[curtLineNo-1])

        # try:
        #     print("\n\t\t 2.next line dict=",wordLine[curtLineNo+1])
        # except Exception as e:
        #     pass

        lastWord, nextWord = "", ""

        '''
            gathers last line neccessary features
        '''

        for indx1, val1 in enumerate(wordCorLine[curtLineNo - 1]):

            print("***********************************************************")
            image3 = image11  # copy.deepcopy(image11)
            byWord = wordLine[curtLineNo - 1][indx1]
            nextWord, prevWord = "", ""
            # print("\n\t val1=",val1)

            allTemp = val1
            # print("\n\t allTemp=",allTemp)

            xTemp1, xTemp2 = allTemp[0], allTemp[2]
            yTemp1, yTemp2 = allTemp[1], allTemp[3]

            if yTemp1 >= y1 or yTemp1 >= y2 or yTemp2 >= y1 or yTemp2 >= y2:
                break

            # print("\n\t rule 1:",xTemp1<=x2 and xTemp2>x2)
            # print("\n\t rule 2:",xTemp2>=x1 and xTemp1<=x1)
            # print("\n\t rule 3:",xTemp1>=x1 and xTemp2>=x2)
            # print("\n\t rule 4:",xTemp1>=x1 and x2>=xTemp2)
            # print("\n\t rule 5:",x2>=xTemp1 and x2<=xTemp1)

            if xTemp1 <= x2 and xTemp2 > x2:
                # print("\n\t overlap 1")
                overlapFlag = 1

            elif xTemp2 >= x1 and xTemp1 <= x1:
                # print("\n\t overlap2")
                overlapFlag = 2
            elif xTemp1 >= x1 and x2 >= xTemp2:
                # print("\n\t overlap4")
                overlapFlag = 4

            elif x2 >= xTemp1 and x2 <= xTemp1:
                # print("\n\t overlap5")
                overlapFlag = 5

            if overlapFlag > 0:
                # print("\n\t 2.word x1:",x1,"\t 2.x2:",x2)
                # print("\n\t 2.overlap word xTemp1:",xTemp1,"\t 2.xTemp2:",xTemp2)
                # print("\n\t 2.flag=",overlapFlag)
                # cv2.rectangle(image3,(xTemp2, yTemp2), (xTemp1, yTemp1),(0, 255, 0), 5)
                # cv2.rectangle(image3,(x1, y1), (x2, y2),(255,0, 0), 5)
                #cv2.line(image3, (x1, y1), (x2, y2), (0, 0, 255), 3)
                # cv2.line(image3,(xTemp2,yTemp2),(xTemp1,yTemp1), (0, 0, 255), 3)
                # cv2.line(image3,(x1,y1),(xTemp2,yTemp2), (0, 255,0), 5)
                #ims = cv2.resize(image3, (700, 700))
                overlapFlag = 0
                # print("\n\t forWOrd-",str(forWord),"\t byWord-",str(byWord))
                name = str(forWord)# + "_" + str(byWord) + "_" + str(nextWord) + "_" + str(prevWord)
                '''
                cv2.imshow(name, ims)
                cv2.moveWindow(name, 100, 100)
                cv2.waitKey()
                '''
                plot(image3,name)

                '''
                    above word coordinate
                '''

                cor.loc[wordFeatureIndx, "8"] = [xTemp1, yTemp1, xTemp2, yTemp2]
                cor1.loc[wordFeatureIndx, "8"] = byWord
                top=[xTemp1, yTemp1, xTemp2, yTemp2]
                # print("\n\t 0.wordCorLine::>", len(wordCorLine[curtLineNo - 1]))
                # print("\n\t 1.wordCorLine::>", len(wordCorLine[curtLineNo - 1][indx1 - 1]))
                # print("\n\t 2.wordCorLine:", len(wordCorLine[curtLineNo - 1][indx1]))

                '''
                    gathers last line previous word features
                '''
                if indx1 > 0:
                    prevCord = wordCorLine[curtLineNo - 1][indx1 - 1]
                    xTempL0, xTempL1 = prevCord[0], prevCord[2]
                    yTempL0, yTempL1 = prevCord[1], prevCord[3]
                    # print("\n\t above prev=", prevCord)
                    prevWord = wordLine[curtLineNo - 1][indx1 - 1]
                    # print("\n\t above prevWord =", prevWord)

                    '''
                        above left word coordinate
                    '''
                    cor.loc[wordFeatureIndx, "7"] = [xTempL0, yTempL0, xTempL1, yTempL1]
                    cor1.loc[wordFeatureIndx, "7"] = prevWord
                elif indx1 == 0:
                    cor.loc[wordFeatureIndx, "7"] = [x1, y1, x2, y2]
                    cor1.loc[wordFeatureIndx, "7"] = [x1, y1, x2, y2]

                '''
                    gathers last line next word features
                '''
                if (indx1 + 1) < len(wordCorLine[curtLineNo - 1]):
                    nextCord = wordCorLine[curtLineNo - 1][indx1 + 1]
                    xTempR1, xTempR2 = nextCord[0], nextCord[2]
                    yTempR1, yTempR2 = nextCord[1], nextCord[3]
                    # print("\n\t nextCord=", nextCord)

                    # nextCord=wordCorLine[curtLineNo - 1][indx1+1]

                    nextWord = wordLine[curtLineNo - 1][indx1 + 1]
                    # print("\n\t nextWord =", nextWord)

                    '''
                        above right word coordinate
                    '''
                    cor.loc[wordFeatureIndx, "1"] = [xTempR1, yTempR1, xTempR2, yTempR2]
                    cor1.loc[wordFeatureIndx, "1"] = nextWord

                elif (indx1) == len(wordCorLine[curtLineNo - 1]):

                    cor.loc[wordFeatureIndx, "1"] = [10000, 10000, 10000, 10000]
                    cor1.loc[wordFeatureIndx, "1"] = [10000, 10000, 10000, 10000]

                else:
                    cor.loc[wordFeatureIndx, "8"] = [currentCor[0], currentCor[1], currentCor[2], currentCor[3]]
                    top=[currentCor[0], currentCor[1], currentCor[2], currentCor[3]]
                    cor.loc[wordFeatureIndx, "1"] = [currentCor[0], currentCor[1], currentCor[2], currentCor[3]]
                    cor.loc[wordFeatureIndx, "7"] = [currentCor[0], currentCor[1], currentCor[2], currentCor[3]]
                    cor1.loc[wordFeatureIndx, "1"] = [currentCor[0], currentCor[1], currentCor[2], currentCor[3]]
            else:
                cor.loc[wordFeatureIndx, "1"] = [currentCor[0], currentCor[1], currentCor[2], currentCor[3]]
                cor.loc[wordFeatureIndx, "7"] = [currentCor[0], currentCor[1], currentCor[2], currentCor[3]]
                cor.loc[wordFeatureIndx, "8"] = [currentCor[0], currentCor[1], currentCor[2], currentCor[3]]
                top = [currentCor[0], currentCor[1], currentCor[2], currentCor[3]]

        # plot(image11, name)
        '''
            next line features
        '''

        for indx1, val1 in enumerate(wordCorLine[curtLineNo + 1]):

            allTemp = val1
            xTemp1, xTemp2 = allTemp[0], allTemp[2]
            yTemp1, yTemp2 = allTemp[1], allTemp[3]

            '''
                below word coordinate
            '''
            cor.loc[wordFeatureIndx, "4"] = [xTemp1, yTemp1, xTemp2, yTemp2]

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

            if xTemp1 <= x2 and xTemp2 > x2:
                # print("\n\t overlap 1")
                overlapFlag = 1

            elif xTemp2 >= x1 and xTemp1 <= x1:
                # print("\n\t overlap2")
                overlapFlag = 2
            elif xTemp1 >= x1 and x2 >= xTemp2:
                # print("\n\t overlap4")
                overlapFlag = 4

            elif x2 >= xTemp1 and x2 <= xTemp1:
                # print("\n\t overlap5")
                overlapFlag = 5

            if overlapFlag > 0:
                # print("\n\t 2.word x1:",x1,"\t 2.x2:",x2)
                # print("\n\t 2.overlap word xTemp1:",xTemp1,"\t 2.xTemp2:",xTemp2)
                # print("\n\t 2.flag=",overlapFlag)
                cv2.rectangle(image3, (xTemp2, yTemp2), (xTemp1, yTemp1), (0, 255, 0), 1)
                cv2.rectangle(image3, (x1, y1), (x2, y2), (255, 0, 0), 1)
                # cv2.line(image3, (x1, y1), (x2, y2), (0, 0, 255), 3)
                # cv2.line(image3, (xTemp2, yTemp2), (xTemp1, yTemp1), (0, 0, 255), 3)
                cv2.line(image3, (x1, y1), (xTemp2, yTemp2), (255, 255, 0), 3)
                # ims = cv2.resize(image3, (700, 700))

                # print("\n\t forWOrd-",str(forWord),"\t byWord-",str(byWord))
                # cv2.imshow(str(forWord) + "_" + str(byWord) + "_" + str(nextWord) + "_" + str(prevWord), ims)
                # cv2.moveWindow(str(forWord) + "_" + str(byWord) + "_" + str(nextWord) + "_" + str(prevWord), 100, 100)
                # cv2.waitKey()
                # plot(image3,name)
                overlapFlag = 0
                # cv2.destroyAllWindows()

                '''
                    gathers next line previous word
                '''

                if indx1 > 0:
                    prevCord = wordCorLine[curtLineNo + 1][indx1 - 1]
                    xTempL0, xTempL1 = prevCord[0], prevCord[2]
                    yTempL0, yTempL1 = prevCord[1], prevCord[3]
                    # print("\n\t prev below line=", prevCord)
                    prevWord = wordLine[curtLineNo + 1][indx1 - 1]
                    # print("\n\t prevWord =", prevWord)

                    '''
                        above left word coordinate
                    '''
                    cor.loc[wordFeatureIndx, "5"] = [xTempL0, yTempL0, xTempL1, yTempL1]
                    cor1.loc[wordFeatureIndx, "5"] = prevWord

                elif indx1 == 0:

                    cor.loc[wordFeatureIndx, "5"] = [0, 0, 0, 0]
                    cor1.loc[wordFeatureIndx, "5"] = [0, 0, 0, 0]

                '''
                    next line next word
                '''
                if (indx1 + 1) < len(wordCorLine[curtLineNo + 1]):
                    nextCord = wordCorLine[curtLineNo + 1][indx1 + 1]
                    xTempR1, xTempR2 = nextCord[0], nextCord[2]
                    yTempR1, yTempR2 = nextCord[1], nextCord[3]
                    # print("\n\t nextCord=", nextCord)
                    nextWord = wordLine[curtLineNo + 1][indx1 + 1]
                    # print("\n\t nextWord =", nextWord)

                    '''
                        above right word coordinate
                    '''
                    cor.loc[wordFeatureIndx, "3"] = [xTempR1, yTempR1, xTempR2, yTempR2]
                    cor1.loc[wordFeatureIndx, "3"] = nextWord


                elif indx1 == len(wordCorLine[curtLineNo + 1]):
                    cor.loc[wordFeatureIndx, "3"] = [10000, 10000, 10000, 10000]
                    cor1.loc[wordFeatureIndx, "3"] = [10000, 10000, 10000, 10000]

        # return image
        aboveCordinate = cor.loc[wordFeatureIndx, "8"]
        cv2.line(image11, (aboveCordinate[2], aboveCordinate[3]), (aboveCordinate[0], aboveCordinate[1]), (0, 0, 255), 3)
        return cor, cor1, wordFeatureIndx, image11
    except Exception as e:
        print("\n\t\t\t exception in getWords:", e)
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("\n\t\t line no::", fname, exc_tb.tb_lineno)
        input("\n\t\t\exception in getWords")


