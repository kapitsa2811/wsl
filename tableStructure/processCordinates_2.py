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

    lineBrake=0

    xTemp1Old, yTemp1Old = 0,0
    xTemp2Old, yTemp2Old = 0,0
    xTemp1, yTemp1=None,None
    xTemp11, yTemp11 =None,None
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
    tempLastLineWords={} # only stores last line words key is word and value is coordinate

    df=pd.DataFrame(columns=["fileName","x1","y1","x11","y11","lineNo"])


    def cellPushCordinate(df,lineNo,x1,y1,x11,y11,cellLineNo):

            '''
               current cell
            '''

            df.loc[lineNo,"x1"]=x1
            df.loc[lineNo,"y1"]=y1
            df.loc[lineNo,"x11"]=x11
            df.loc[lineNo, "y11"] = y11
            df.loc[lineNo, "lineNo"] = cellLineNo
            return df


    def getWords(image,curtLineNo,currentCor,countWords,wordCorLine):
        #print("\n\t\t this gives near words")

        x1,x2=currentCor[0],currentCor[2]
        y1,y2=currentCor[1],currentCor[3]
        overlapFlag=0

        print("\n\t\t 2.current word coordinate:",currentCor)

        #print("\n\t\t 2.last line coordinate:")

        # for key in wordCorLine.keys():
        #
        #     print("\n\t 3.key=",key,"\t value:",wordCorLine[key])

        dist = 0
        keyCount=0

        # for key in wordCorLine.keys():
        #     print("n\\t key=",key)


        for key1 in wordCorLine.keys():

            if not key1==(lineCount-1):
                continue


            print("\n\t\t 2. keyManage",int(key1)==(curtLineNo-1))
            print("\n\t\t 2. keyManage", key1,"\t curtLineNo - 1:", (curtLineNo - 1))

            input("key")
            if not int(key1)==(curtLineNo-1):
                 continue
            input("keyMatch")

            print("\n\t\t\t 2.key:",key1,"\t 2.value:",wordCorLine[key])

            allTemp=wordCorLine[key][0]
            print("\n\t allTemp=",allTemp)

            xTemp1,xTemp2=allTemp[0],allTemp[2]
            yTemp1,yTemp2=allTemp[1],allTemp[3]

            midX,midY=(x1+x2)/2,(y1+y2)/2
            midTempX,midTempY=(xTemp1+xTemp2)/2,(yTemp1+yTemp2)/2


            if yTemp1 >=y1 or yTemp1 >=y2 or yTemp2 >=y1 or yTemp2 >=y2 :
                break

            print("\n\t rule 1:",xTemp1<=x2 and xTemp2>x2)
            print("\n\t rule 2:",xTemp2>=x1 and xTemp1<=x1)
            print("\n\t rule 3:",xTemp1>=x1 and xTemp2>=x2)
            print("\n\t rule 4:",xTemp1>=x1 and x2>=xTemp2)
            print("\n\t rule 5:",x2>=xTemp1 and x2<=xTemp1)

            if xTemp1<=x2 and xTemp2>x2:
                print("\n\t overlap 1")
                overlapFlag =1

            elif xTemp2>=x1 and xTemp1<=x1:
                print("\n\t overlap2")
                overlapFlag =2
            elif xTemp1>=x1 and xTemp2>=x2:
                print("\n\t overlap3")
                #overlapFlag = 3

            elif xTemp1>=x1 and x2>=xTemp2:
                print("\n\t overlap4")
                overlapFlag = 4

            elif x2>=xTemp1 and x2<=xTemp1:
                print("\n\t overlap5")
                overlapFlag = 5


            if 1:#overlapFlag>0:
                print("\n\t 2.word x1:",x1,"\t 2.x2:",x2)
                print("\n\t 2.overlap word xTemp1:",xTemp1,"\t 2.xTemp2:",xTemp2)
                print("\n\t 2.flag=",overlapFlag)

                cv2.rectangle(image1,(xTemp2, yTemp2), (xTemp1, yTemp1),(0, 255, 0), 5)
                cv2.rectangle(image1,(x1, y1), (x2, y2),(255,0, 0), 5)
                cv2.line(image1,(x1,y1),(x2,y2), (0, 0, 255), 3)
                cv2.line(image1,(xTemp2,yTemp2),(xTemp1,yTemp1), (0, 0, 255), 3)
                cv2.line(image1,(x1,y1),(xTemp2,yTemp2), (0, 255,0), 5)

                ims=cv2.resize(image1,(1000,1000))
                cv2.imshow("features", ims)
                cv2.waitKey()
                overlapFlag=0
                cv2.destroyAllWindows()
                #input("check")

        return image


    for rowNo, row in df1.iterrows():

        #print("\n\t rowNo:",rowNo)

        print("\n\t 1.line no:",lineCount)
        print("\n\t\t 1.word no:",countWords)
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
        cv2.line(image, (cuX, cuY), (cuX2, cuY2), (0, 0, 255), 3)

        #print("\n\t ",abs(cuY-lastY)>threshold,"\t abs(cuY-lastY):",abs(cuY-lastY))

        if abs(cuY-lastY)>threshold:

            lineBrake=1
            lastLine=lineCount

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
                line segment
            '''
            cv2.line(image, (startX, startY), (lastX2,lastY2), (255, 0, 0), 3)

            countWords=0

            winname = w+"_"+str(abs(cuY - lastY))

            '''
                puts all words in last line to dictionary
            '''
            wordLine[lineCount]=tempWord
            print("\n\t wordLine[lineCount]=",wordLine[lineCount])
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
            # cv2.imshow(winname, ims)
            # cv2.waitKey()
            # cv2.destroyWindow(winname)

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


        # if lineCount>0:
        #     #print("\n\t extract Above line words")
        #image=getWords(image,lineCount, currentCor,countWords,wordCorLine)
        #     print("\n\t w=",w)
        #     #input("out")


        lastX, lastY = cuX,cuY
        lastX2, lastY2 = cuX2,cuY2
        countWords+=1

    ##def getWords(image,curtLineNo,currentCor,countWords,wordCorLine)

    print("\n\t ###################################################")
    for curtLineNo in wordCorLine:

        print("\n\t lineNo=",curtLineNo)
        print("\n\t value:",wordCorLine[curtLineNo])
        print("\n\t no of word:",len(wordCorLine[curtLineNo]))

        print("\n\t allWords=",wordLine[curtLineNo])
        print("\n\t allWords=",len(wordLine[curtLineNo]))

        if curtLineNo>0:
            print("\n\t lineNo:--->",curtLineNo)

            for currentCor in wordCorLine[curtLineNo]:
                getWords(image, curtLineNo, currentCor, countWords, wordCorLine)


    print("\n\t *******************************************************")
lineSegmentation(df1)

exit()

for rowNo,row in df1.iterrows():

    image1 = cv2.imread("/home/wipro/PycharmProjects/hocr/fileconverter_batch/pdf/images//" + fileName1)
    print("--->",df1.loc[rowNo,'x1'])

    '''
        x1,y1 : current word
    '''
    xTemp1,yTemp1=int(df1.loc[rowNo,'x1']),int(df1.loc[rowNo,'y1'])
    xTemp2,yTemp2=int(df1.loc[rowNo,'x2']),int(df1.loc[rowNo,'y2'])

    cv2.line(image1, (xTemp1, yTemp1), (xTemp2, yTemp2), (255, 255, 0), 5)
    #cv2.rectangle(image1,(xTemp1, yTemp1), (xTemp2, yTemp2),(0, 255, 0), 5)


    #print("\n\t rowNo=",rowNo)
    #print("\n\r row=",row)

    print("\n\t current word=",row["word_2"])
    cWord=row["word_2"]

    yMid=row["y1"]+row["y2"]

    #print("\n\t yMid=",yMid)

    k=int(yMid/10)
    if int(yMid/10) in yDict.keys():
        l=yDict[k]
        l.append(row["word_2"])
    else:
        l=list()
        l.append(row["word_2"])
        yDict[k]=l


    '''
        8 nearest neighbour
    '''

    '''
        on this cell we r currently focusing
    '''
    x,y=int(df1.loc[rowNo,'x1']),int(df1.loc[rowNo,'y1'])
    xx,yy=int(df1.loc[rowNo,'x2']),int(df1.loc[rowNo,'y2'])

    '''
        dictionary d stores smaller distances with other cells
        here distance value is key and coordinates is value
    '''
    d={}
    cellDist=[]

    '''
        this loop finds out distance with all other cells 
        it cheks 2 diagonal coordinates
    '''

    for rowNo2, row2 in df1.iterrows():

        xMid1, yMid1 = int(df1.loc[rowNo2, 'mid_cordinate_1_x']), int(df1.loc[rowNo, 'mid_cordinate_1_y'])

        '''
            other cell coordinate
        '''
        x1, y1 = int(df1.loc[rowNo2, 'x1']), int(df1.loc[rowNo2, 'y1'])
        x2, y2 = int(df1.loc[rowNo2, 'x2']), int(df1.loc[rowNo2, 'y2'])

        '''
        dist1=(x-x1)**2+(y-y1)**2
        dist2=(x-x2)**2+(y-y2)**2
        dist3=(xx-x1)**2+(yy-y1)**2
        dist4=(xx-x2)**2+(yy-y2)**2
        '''

        dist1=(xMid1-x1)**2+(yMid1-y1)**2
        dist2=(xMid1-x2)**2+(yMid1-y2)**2
        dist3=(xMid1-x1)**2+(yMid1-y1)**2
        dist4=(xMid1-x2)**2+(yMid1-y2)**2
        

        allDist=np.array([dist1,dist2,dist3,dist4])
        minDist=np.argmin(allDist)

        if allDist[minDist]==0:
            continue

        # print("\n\t distances=",allDist)
        # print("\n\t minDist=",minDist)

        if minDist==0:
            dist=dist1
            # fmX,fmY=x,y
            # toX,toY=x1,y1
        elif minDist==1:
            dist=dist2
            # fmX,fmY=x,y
            # toX,toY=x2,y2

        elif minDist==2:
            dist = dist3
            # fmX,fmY=xx,yy
            # toX,toY=x1,y1

        elif minDist==3:
            dist = dist4
            # fmX,fmY=xx,yy
            # toX,toY=x2,y2

        d[dist]=[[df1.loc[rowNo2,'x1'],df1.loc[rowNo2,'y1'],df1.loc[rowNo2,'x2'],df1.loc[rowNo2,'y2']]]
        cellDist.append(dist)
    cellDist.sort()
    #print("\n\t sorted dist list=\n",len(cellDist))
    #input("check")

    d1XY={}
    d2XY={}
    d3XY={}
    d4XY={}

    d1=[]
    d2=[]
    d3=[]
    d4=[]

    '''
        d is directory containing distances with all other words
        from single dir, 4 different directories quadrant wise are created
    '''

    #print("\n\t d=",d)

    for key in d.keys():
        dd = d[key][0]
        tempX1, tempY1 = int(dd[0]), int(dd[1])
        tempX2, tempY2 = int(dd[2]), int(dd[3])

        '''
            1st quadrant
        '''
        corList=[tempX1, tempY1,tempX2, tempY2]
        if tempX1>=x and tempY1>=y and abs(tempX1-x1)>150 and abs(tempY1-y1)>150:
            d1XY[key]=[corList]
            d1.append(key)

        if tempX1>=x and tempY1<=y and abs(tempX1-x1)>150 and abs(tempY1-y1)>150:
            d4XY[key]=[corList]
            d4.append(key)

        if tempX1<x and tempY1>=y and abs(tempX1-x1)>150 and abs(tempY1-y1)>150:
            d2XY[key]=[corList]
            d2.append(key)

        if tempX1<x and tempY1<y and abs(tempX1-x1)>150 and abs(tempY1-y1)>150:
            d3XY[key]=[corList]
            d3.append(key)

    d1.sort()
    d2.sort()
    d3.sort()
    d4.sort()


    '''
        quadrantwise nearest point
    '''

    '''
        quadrant 1
    '''
    print("\n\t d1=")
    sortCord=getNearestPoints(d1, d1XY,image1)
    # print("\n\t 1.sortCord=",sortCord[0])
    # print("\n\t 2.sortCord=",sortCord[1])

    try:
        cv2.line(image1, (x, y), (sortCord[0][0], sortCord[0][1]), (0, 0, 255), 3)
    except Exception as e:
        pass

    try:
        cv2.line(image1, (x, y), (sortCord[1][0], sortCord[1][1]), (0, 0, 255), 3)
    except Exception as e:
        pass

    try:
        print("\n\t ")
        cv2.rectangle(image1,(sortCord[0][0], sortCord[0][1]),(sortCord[0][2], sortCord[0][3]),(0, 0, 255), 3)
        cv2.rectangle(image1,(sortCord[1][0], sortCord[1][1]),(sortCord[1][2], sortCord[1][3]),(0, 0, 255), 3)
    except Exception as e:
        print("\n\t Exception in drawing rectangle d1XY")
        pass


    '''
        quadrant 2
    '''

    #input("\n\t 1.key")

    print("\n\t d2=")
    sortCord=getNearestPoints(d2, d2XY,image1)

    try:
        cv2.line(image1, (x, y), (sortCord[0][0], sortCord[0][1]), (0, 255, 0), 3)
    except Exception as e:
        pass


    try:
        cv2.rectangle(image1,(sortCord[0][0], sortCord[0][1]),(sortCord[0][2], sortCord[0][3]),(0, 255,0), 3)
        cv2.rectangle(image1,(sortCord[1][0], sortCord[1][1]),(sortCord[1][2], sortCord[1][3]),(0,255,0), 3)
    except Exception as e:
        print("\n\t Exception in drawing rectangle d1XY")
        pass


    print("\n\t 2.sortCord=",sortCord)
    #input("\n\t 2.key")

    '''
        quadrant 3
    '''

    print("\n\t d3=")
    sortCord=getNearestPoints(d3, d3XY,image1)


    try:
        cv2.line(image1, (x, y), (sortCord[0][0], sortCord[0][1]), (255, 0,0), 3)
    except Exception as e:
        pass

    try:
        cv2.line(image1, (x, y), (sortCord[1][0], sortCord[1][1]), (255, 0,0), 3)
    except Exception as e:
        pass

    try:
        cv2.rectangle(image1,(sortCord[0][0], sortCord[0][1]),(sortCord[0][2], sortCord[0][3]),(255,0,0), 3)
        cv2.rectangle(image1,(sortCord[1][0], sortCord[1][1]),(sortCord[1][2], sortCord[1][3]),(255,0,0), 3)
    except Exception as e:
        print("\n\t Exception in drawing rectangle d1XY")
        pass


    print("\n\t 3.sortCord=",sortCord)
    #input("\n\t 3.key")

    '''
        quadrant 4
    '''

    print("\n\t d4=")
    sortCord=getNearestPoints(d4, d4XY,image1)

    try:
        cv2.line(image1, (x, y), (sortCord[0][0], sortCord[0][1]), (0, 255, 255), 3)
    except Exception as e:
        pass

    try:
        cv2.line(image1, (x, y), (sortCord[1][0], sortCord[1][1]), (0, 255, 255), 3)
    except Exception as e:
        pass

    try:
        cv2.rectangle(image1,(sortCord[0][0], sortCord[0][1]),(sortCord[0][2], sortCord[0][3]),(0, 255, 255), 3)
        cv2.rectangle(image1,(sortCord[1][0], sortCord[1][1]),(sortCord[1][2], sortCord[1][3]),(0, 255, 255), 3)
    except Exception as e:
        print("\n\t Exception in drawing rectangle d1XY")
        pass

    print("\n\t 4.sortCord=",sortCord)
    #input("\n\t 4.key")

    '''
    for lineNo,horDist in enumerate(cellDist):
        print("\n\t horDist=",horDist)
        #print("\n\t d=",d[horDist][0])
        dd=d[horDist][0]
        tempX1,tempY1=int(dd[0]),int(dd[1])
        tempX2,tempY2=int(dd[2]),int(dd[3])
        if lineNo==0:
            cv2.line(image1, (x, y), (tempX1, tempY1), (0, 0, 255), 3)
        elif lineNo==1:
            cv2.line(image1, (x, y), (tempX1, tempY1), (0,255, 0), 3)
        elif lineNo==2:
            cv2.line(image1, (x, y), (tempX1, tempY1), (255, 0,0), 3)
        elif lineNo==3:
            cv2.line(image1, (x, y), (tempX1, tempY1), (0, 255, 255), 3)
        elif lineNo==4:
            cv2.line(image1, (x, y), (tempX1, tempY1), (255, 0, 255), 3)
        elif lineNo==5:
            cv2.line(image1, (x, y), (tempX1, tempY1), (255, 255, 0), 3)
        elif lineNo==6:
            cv2.line(image1, (x, y), (tempX1, tempY1), (0, 0, 155), 3)
        elif lineNo==7:
            cv2.line(image1, (x, y), (tempX1, tempY1), (0, 155,0), 3)
        else:
            cv2.line(image1, (x, y), (tempX1, tempY1), (0, 255,0), 5)

        #cv2.line(image1, (fmX,fmY), (toX, toY), (0, 0, 255), 3)

        if lineNo>=8:
            break
    '''
    '''
    '''
    ims=cv2.resize(image1,(940,940))
    cv2.imshow("map",ims)
    cv2.waitKey()

print("\n\t yDict=",yDict)




pathWrite="/home/wipro/PycharmProjects/hocr/fileconverter_batch/pdf/images//"
cv2.imwrite(pathWrite+"out.jpg",image)

