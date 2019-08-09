from PIL import Image, ImageDraw, ImageFont
import PIL.ImageOps

import math
import os,sys
import random
import re
import numpy as np
import scipy.ndimage as scipy_ndimage
import matplotlib.pyplot as plt
import matplotlib.image as mpimage
import cv2
import matplotlib.image as mt
from copy import deepcopy
from collections import defaultdict
import re
import codecs
import pandas as pd

'''
    copy of ssyntheticDocGeneration_2.py copy is made to make code remove hard coded paths
    copy of generateFiles_3.py
    The aim of the code is to generate images with and without table
  
  
    # Document Image location:"//imageWord//"
    # Segment Mask location: "//segWord//"

'''

#dumpPath = "/home/aniket/PycharmProjects/textSpotting/TextSegmentationFromImages-master/progress4/dump/"


class TextDetectorTrainer:
    """
        A class that generates random training examples for the text detector neural net.
        Some examples are pictures of text, some examples are adversarial (to prevent the network from
        learning a simpler function than what we want).
    """

    def __init__(self, corpus=None, fonts=None):

        '''

        :param corpus:
        :param fonts:
        at below location necessary results will be dumped
        '''

        self.basePath = "/home/wipro/PycharmProjects/wsl/wsl-master/publicationData//"
        self.expNo=str(9)

        '''
            this contains document images
        '''
        self.dumpPath = self.basePath+self.expNo+"//train//table//"

        '''
            contains segmented images of above
        '''
        self.dumpPath1 = self.basePath+self.expNo+"//train//nonTable//"
        self.dumpPathS = self.basePath+self.expNo+"//train//segWord//"
        #self.idDir(self, self.dumpPathS)

        # '''

        self.cropLocation = self.basePath+self.expNo+"//"
        #self.idDir(self, self.hitImagesPath)
        '''
            if this  variable is 1 this will mask text otherwise only mask non text structures
        '''
        self.maskText=0

        # already generated table location
        self.hitImagesPath=self.basePath+self.expNo+"//textTables//"

        self.df=pd.DataFrame(columns=["fileName","x1","y1","x2","y2"])


        if corpus is not None:
            self.TEXT_CORPUS = corpus
        else:
            #self.TEXT_CORPUS = open("text/corpus.txt",encoding="utf-16").read().replace('\n', ' ')

            with codecs.open("/home/wipro/PycharmProjects/wsl/wsl-master/dataGeneration./text/corpus.txt", 'r', encoding='utf8') as f:
                self.TEXT_CORPUS = f.read()

                #self.TEXT_CORPUS=re.sub(r'\W+', '', self.TEXT_CORPUS)

                PERMITTED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_- "
                self.TEXT_CORPUS = "".join(c for c in self.TEXT_CORPUS if c in PERMITTED_CHARS)

        if fonts is not None:
            self.FONT_LIST = fonts
        else:
            self.FONT_LIST = [
                "text/arial.ttf",
                "text/arialbd.ttf",
                "text/calibri.ttf",
                "text/times.ttf",
                "text/timesbd.ttf",
                "text/timesi.ttf",
            ]

        self.FONT_OBJECTS = [
            ImageFont.truetype(font, size)
            for font in self.FONT_LIST
            for size in range(15,20)
        ]

        # When generating adversarial examples (using `genEvilExample()`), we will flip the Y axis of the image.
        # We want the resulting image to look like text, but not contain any valid letters. This way, the network
        # will be forced to learn what some letters look like, instead of just learning to detect the presence of
        # black ink or noise.
        #
        # When we flip the Y axis, some letters will still look like valid letters, so if the network has learned
        # to recognize valid letters, there is no reason to punish it for recognizing these letters. We will remove
        # a few specific letters from the sample text when building counter-examples.
        self.MIRROR_LETTERS_REGEX = re.compile(r"[BbCcDdEHIKlOopqXx038\[\]]")

        # A couple of images, used as temporary buffers when generating training examples.
        # After an images is painted, `numpy.array(image)` makes a copy, to be sent to the network.

        '''
            this defines total image height and width
        '''
        self.CANVAS_WIDTH =600
        self.CANVAS_HEIGHT = 800

        self.CANVAS_RECTANGLE = (0, 0, self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        self.tempCanvas = Image.new("L", (self.CANVAS_WIDTH, self.CANVAS_HEIGHT))
        self.tempCanvasCopy=Image.new("L", (self.CANVAS_WIDTH, self.CANVAS_HEIGHT))
        self.tempHeatMap = Image.new("L", (self.CANVAS_WIDTH, self.CANVAS_HEIGHT))
        self.tempHeatMapCopy = Image.new("L", (self.CANVAS_WIDTH, self.CANVAS_HEIGHT))

        # "Painter" objects encapsulate the implementation of algorithms for drawing to an image.
        # With these objects, we will use `.rectangle()` and `.text()` to cause updates to the `temp*` images above.
        self.tempCanvasPainter = ImageDraw.Draw(self.tempCanvas)
        self.tempCanvasPainterCopy = ImageDraw.Draw(self.tempCanvasCopy)

        # self.hh = ImageDraw.Draw(self.tempCanvas)
        # self.hh = ImageDraw.Draw(self.tempHeatMap)
        self.hh = np.zeros((self.CANVAS_WIDTH, self.CANVAS_HEIGHT, 3))
        self.tempHeatMapPainter = ImageDraw.Draw(self.tempHeatMap)
        self.tempHeatMapPainterCopy = ImageDraw.Draw(self.tempHeatMapCopy)

        self.tabAndTabLess=1 # creates table in image and in another copy same document without table
        self.textAroundTable = 1 # want text around table

        self.genEvilExmpl=0

    def getRandomFont(self):
        fonts = self.FONT_OBJECTS
        return fonts[random.randint(0, len(fonts) - 1)]

    def getRandomSnippet(self, snippetLength=100):
        corpus = self.TEXT_CORPUS
        corpusLength = len(corpus)
        snippetLength = min(snippetLength, corpusLength)

        #print("\n\t corpusLength =",corpusLength,"\t snippetLength =",snippetLength)

        '''
            70 % time begin with 0 as a x co-ordinate
        '''

        if random.random()>0.70:
            snippetStart = random.randint(int((corpusLength - snippetLength - 1)/2), corpusLength - snippetLength - 1)
        else:
            snippetStart = random.randint(0, int(((corpusLength - snippetLength - 1))/2))


        snippetStop = snippetStart + snippetLength # total length of line

        #print "\n\n\t snippetStart =",snippetStart,"\t snippetStop =",snippetStop,"\t length=",(snippetStop-snippetStart)
        return corpus[snippetStart:snippetStop]

    @staticmethod

    def getRandomForegroundAndBackground():
        a = random.randint(0, 120)
        b = random.randint(a + 30, 255)

        if random.randint(0, 1) == 0:
            a, b = b, a
        # a,b=0,255
        return "rgb(%d,%d,%d)" % (a, a, a), "rgb(%d,%d,%d)" % (b, b, b)

    def show(self, canvas, heatMap, canvas1, heatMap1):
        plt.ion()
        plt.clf()
        plt.subplot(2, 2, 1)
        plt.title("canvas")
        # plt.imshow(canvas, plt.get_cmap('gray'), clim=(0, 255))  # [y:(y+32), x:(x+32)]
        plt.imshow(canvas)  # [y:(y+32), x:(x+32)]
        plt.subplot(2, 2, 2)
        plt.title("heatMap")
        plt.imshow(heatMap)

        plt.subplot(2, 2, 3)
        plt.title("canvasNew")
        # plt.imshow(canvas, plt.get_cmap('gray'), clim=(0, 255))  # [y:(y+32), x:(x+32)]
        plt.imshow(canvas1)  # [y:(y+32), x:(x+32)]
        plt.subplot(2, 2, 4)
        plt.title("heatMapNew")
        plt.imshow(heatMap1)

        plt.show()
        plt.pause(.001)

    def idDir(path):
        #print("\n\t this function creates dir if not present")

        if not os.path.isdir(path):
            os.mkdir(path)
            print("\n\t Directory created ", path)
        else:
            print("\n\t Already present")


    '''
        when table is inserted in image the same copy of image needs to inserted with some other text this part handles that
    '''
    def handleNonTableInsertion(self,LineWordLoc,fontObj,lineBegining,oldTextWidth,textHeight,x,y,yLimit,lineSpacing):

        y=y + textHeight


        try:
            for i in LineWordLoc.keys():

                textLine = LineWordLoc[i]

                '''
                    this part updates single line and only modify x-cordinate on it
                '''
                for wordNo, wordDict in enumerate(textLine):

                    wordSampleKey = wordDict.keys()
                    # print "\n\t\t key=", wordSampleKey[0]
                    wordSizeValue = wordDict[list(wordSampleKey)[0]]

                    #print ("\n\t\t worNo=", wordNo, "\t word=", list(wordSampleKey)[0], "\t size=", wordSizeValue)
                    textWidth, textHeight = wordSizeValue[0], wordSizeValue[1]
                    #print ("\n\t\t textWidth=", textWidth, "\t textHeight=", textHeight)

                    if wordNo == 0 and lineBegining == 0:
                        # x = random.randint(-textWidth,
                        #                    self.CANVAS_WIDTH)  # text may (intentionally) fall outside the canvas
                        if random.random() > 0.95:
                            x = random.randint(-textWidth,
                                               self.CANVAS_WIDTH)  # text may (intentionally) fall outside the canvas
                        else:
                            x = 0
                    elif wordNo == 0:
                        lineBegining = (self.CANVAS_WIDTH / 10)
                    else:
                        x = x + oldTextWidth + (textWidth / 5)

                    '''
                        write text in the image and updates corresponding heatmap
                        below part responsible for insertion of text in image
                    '''
                    if 1:
                        heatRect = (x, y, x + textWidth, y + textHeight)

                        if self.maskText == 1:
                            self.tempHeatMapPainterCopy.rectangle(heatRect, "green")
                        oldTextWidth = textWidth
                        self.tempCanvasPainterCopy.text((x, y), list(wordSampleKey)[0], font=fontObj, fill='white')  # fg
                        # print "\n\t\t word=",wordSampleKey[0],"\t location=",(x,y)

                    if x > self.CANVAS_WIDTH:
                        # print "x exceeds","\t location=",(x,y),"\t width=",self.CANVAS_WIDTH
                        break

                if y<yLimit:
                    y = y + textHeight + lineSpacing

                else:
                    break

        except Exception as e2:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("\n\t handleNonTableInsertion line no of exception=", exc_tb.tb_lineno,"\n \t exception is=",e2)

    '''
        important parameters are
        line spacing, line count , disableJunk, lineBegining,
    
    '''
    def genTextAndHeatMap(self,nm):

        # generate a random paragraph
        lineBegining=0 # starting x-cordinate
        disableJunk=1
        lineCount = random.randint(15,25)    # how many lines we want in our paragraph
        lineSpacing = random.randint(25,35)  # how many pixels to leave between lines
        insertTabOrFig=0.9 # keeps space for table or figure with mentioned probability
        maxTabFig= 1 #random.randint(0,3) # maximum table or figure
        tabFigCount=0 # table or figure count

        fontObj = self.getRandomFont()  # the font of our paragraph
        textSamples = [self.getRandomSnippet() for _ in range(lineCount)]  # text fragments to use for each line


        '''
            below 2 parameters are from table generation module
        '''
        avgTableWidth=300
        avgTableHeight=600

        self.insertDict=defaultdict(list) # these stores places where space is kept blank to store figure/table

        junkCharList = ["~", "#", "^", "*", "!", "%", "^", "(", ")", ":", "<", ">", "/", "{", "}"]
        noJunk = len(junkCharList) - 1
        # print "textSamples =",textSamples

        # compute the size of the text (note: text height is probably the same for all samples using the same font)

        '''
            below code creates dictionary (LineWordLoc) in which line no is key
            value is list containing many dictionaries (wordSize), wordSize contains word as a key
            and size as a cordinate
        '''
        LineWordLoc = defaultdict(list)  # dict()# line no is key

        for lineNo, wrdLine in enumerate(textSamples):

            #print "\n\t Line No:",lineNo,"\t wrdLine=",wrdLine
            #LineWordLoc[lineNo]=[wrdLine]
            #print "\n\t lineNo= ",lineNo,"\t word=", LineWordLoc[lineNo]
            # wordSize={}

            for wordNo, wrd in enumerate(wrdLine.split(" ")):
                wordSize = {}
                # print "\n\t\t Word no:",wordNo,"\t word=",wrd
                # print "\n\t\t size=",fontObj.getsize(wrd)
                # print("\n\t t=",t)

                '''
                    below part is commented to reduce size
                '''

                t = fontObj.getsize(wrd)
                # t=([math.ceil(x*0.5) for x in t])
                #print "\n\t font Size=",t
                #wordSize[wrd] = fontObj.getsize(wrd)
                wordSize[wrd] = t
                # print "\n\t\t WordSize=",wordSize[wrd]
                LineWordLoc[lineNo].append(wordSize)  # = [wrdLine]

                '''
                    below change is to make word size small
                '''

                # random.randint()
                # LineWordLoc[lineNo].append(wordSize) #= [wrdLine]
            # print "\n\t LineWordLoc[lineNo]=",LineWordLoc[lineNo]

        sampleSizes = [fontObj.getsize(t) for t in textSamples]  # (width, height) tuples for each line of text

        # print("\n\t sampleSizes =",sampleSizes)

        totalParagraphHeight = (lineCount - 1) * lineSpacing + sum([sizeTuple[1] for sizeTuple in sampleSizes])

        # reset the image and heat map
        # fg, bg = self.getRandomForegroundAndBackground()
        self.tempCanvasPainter.rectangle(self.CANVAS_RECTANGLE, 'black')  # rgb(255, 255, 255)
        # self.tempCanvasPainter.rectangle(self.CANVAS_RECTANGLE, "black")
        self.tempHeatMapPainter.rectangle(self.CANVAS_RECTANGLE, "black")

        self.tempCanvasPainterCopy.rectangle(self.CANVAS_RECTANGLE, 'black')  # rgb(255, 255, 255)
        self.tempHeatMapPainterCopy.rectangle(self.CANVAS_RECTANGLE, "black")

        # paint the text and heat map (to their respective images)
        #y = (self.CANVAS_HEIGHT / 2) - (totalParagraphHeight / 2)

        y = (self.CANVAS_HEIGHT / 20)# - (totalParagraphHeight / 2)
        tabStart=[self.CANVAS_HEIGHT / 10,self.CANVAS_HEIGHT / 5,self.CANVAS_HEIGHT / 2,self.CANVAS_HEIGHT /1.5,
                  self.CANVAS_HEIGHT / 1.75,self.CANVAS_HEIGHT /1.25,self.CANVAS_HEIGHT /1.1]

        '''
            below mentioned 2 variables make sure text lines present does not 
            more than total height of the canvas or page
        '''
        yStart=deepcopy(y)
        #yEnd=0
        #draw1 = ImageDraw.Draw(self.tempCanvas)

        '''
            one by one takes line and brakes into words then put it in image also keep empty space for table/ figure
        '''
        for i in LineWordLoc.keys():

            textLine = LineWordLoc[i]

            # if i%100==0:
            #     print "\n\t Line No:",i #,"\t textLine=",textLine

            noWords = len(textLine) - 1  # no of words in line (1 subtracted to use it as index)

            try:
                junkIndx = random.randint(1, noWords)  # here we r going to insert junk char
                # print "\n\t Junk index=",junkIndx
            except Exception as e:
                junkIndx=1

            '''
                this part updates single line and only modify x-cordinate on it
            '''
            for wordNo, wordDict in enumerate(textLine):

                wordSampleKey = wordDict.keys()
                #print ("\n\t\t key=", list(wordSampleKey)[0])
                wordSizeValue = wordDict[list(wordSampleKey)[0]]

                # print "\n\t\t worNo=", wordNo, "\t word=", wordSampleKey, "\t size=", wordSizeValue
                textWidth, textHeight = wordSizeValue[0], wordSizeValue[1]
                # print "\n\t\t textWidth=", textWidth, "\t textHeight=", textHeight

                if wordNo == 0 and lineBegining==0:
                    # x = random.randint(-textWidth,
                    #                    self.CANVAS_WIDTH)  # text may (intentionally) fall outside the canvas
                    if random.random() > 0.95:
                        x = random.randint(-textWidth,
                                           self.CANVAS_WIDTH)  # text may (intentionally) fall outside the canvas
                    else:
                        x = 0
                elif  wordNo==0:
                    lineBegining= (self.CANVAS_WIDTH/10)
                else:
                    x = x + oldTextWidth + (textWidth / 5)

                '''
                    write text in the image and updates corresponding heatmap
                    below part responsible for insertion of text in image
                '''
                if not wordNo == junkIndx:
                    heatRect = (x, y, x + textWidth, y + textHeight)

                    if self.maskText==1:
                        self.tempHeatMapPainter.rectangle(heatRect, "green")
                        self.tempHeatMapPainterCopy.rectangle(heatRect, "green")
                    oldTextWidth = textWidth
                    self.tempCanvasPainter.text((x, y), list(wordSampleKey)[0], font=fontObj, fill='white')  # fg
                    self.tempCanvasPainterCopy.text((x, y), list(wordSampleKey)[0], font=fontObj, fill='white')  # fg
                    #print "\n\t\t word=",wordSampleKey[0],"\t location=",(x,y)

                else:
                    # print "\n\t\t its junk index",wordSampleKey[0]
                    # print "\n\t\t Length of junk index is=",len(wordSampleKey[0])
                    replaceLength = len(list(wordSampleKey)[0])

                    if disableJunk!=1:
                        junkString = ""

                        for junkText in range(replaceLength):
                            junkChar = junkCharList[
                                random.randint(0, noJunk)]  # randomly junk char is selected for replacement
                            junkString = junkString + junkChar

                        # print "\n\t\t WORD:",wordSampleKey,"\t REPLACED BY:",junkString
                        self.tempCanvasPainter.text((x, y), junkString, font=fontObj, fill='white')  # fg

                if x> self.CANVAS_WIDTH:
                    #print "x exceeds","\t location=",(x,y),"\t width=",self.CANVAS_WIDTH
                    break

            totTables=len(self.imagesList)

            '''
                after above for loop fills a line with word then below part try to insert table
            '''
            try:
                #print("\n\t nm=",nm,"\t ",totTables)
                self.randTabIndx= nm%totTables #(totTables-1)
            except Exception  as e:
                #if self.randTabIndx==0:
                self.randTabIndx=nm
                #print(nm)

            self.tempImg=self.imagesList[self.randTabIndx]
            xLen,yLen=self.tempImg.size

            '''
                if part deals with table BB generation
                else part updates y cordinate of line as usaual
            '''

            tabY=random.randint(0,len(tabStart))-1
            if random.random()<1.0 and insertTabOrFig!=0 and tabFigCount<maxTabFig and y>=tabStart[tabY]:

                # if random.random()>0.5:
                #     if y>=(self.CANVAS_HEIGHT/2):
                #             continue
                #     else:
                #         break

                #print "\n\t insert table or figure coordinate called y=",y

                try:
                    '''
                        randomly generating bounding box CC for table
                    '''
                    xTab1 = random.randint(0, abs(self.CANVAS_WIDTH-xLen))
                    xTab2 = xTab1+xLen #random.randint(0, self.CANVAS_WIDTH)
                    yTab1 = (y+2*lineSpacing)#random.randint(y, self.CANVAS_HEIGHT-yLen)
                    yTab2 = yTab1+yLen #random.randint(0, self.CANVAS_HEIGHT)

                    # xTab1, xTab2 = min(xTab1, xTab2), max(xTab1, xTab2)
                    # yTab1, yTab2 = (y+2*lineSpacing), (y+yLen)#min(yTab1, yTab2), max(yTab1, yTab2)
                    self.insertDict[nm]=[xTab1,yTab1,xTab2,yTab2]
                    #print("\n\t nm=",self.insertDict[nm])

                    if self.tabAndTabLess==1:
                        self.handleNonTableInsertion(LineWordLoc, fontObj,lineBegining,oldTextWidth,textHeight,x,y,yTab2-1*lineSpacing,lineSpacing)


                except Exception as e:
                    print("\n\t Exception in coordinate generation=",e)
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print("\n\t line no of exception=", exc_tb.tb_lineno)


                #self.insertDict[tabFigCount]=[xTab1,yTab1,xTab2,yTab2]
                #self.tempCanvasPainter.rectangle((xTab1,yTab1,xTab2,yTab2), fill='white')

                '''
                    next line y-ordinate
                    
                    if want text around table set textAroundTable=1
                '''

                if self.textAroundTable==1:
                    y = lineSpacing  # y + textHeight + 10* lineSpacing   #+ abs(yTab2-yTab1)
                else:
                    y =  yTab2+lineSpacing #y + textHeight + 10* lineSpacing   #+ abs(yTab2-yTab1)




                #self.tempCanvasPainter.text((x, y), "INSERT TABLE ABOVE", font=fontObj, fill='white')  # fg

                '''
                    # of tables
                '''
                tabFigCount=tabFigCount+1

            else:
                y = y + textHeight + lineSpacing

            #print "\n\t y=",y

            #input("press")

            if abs(yStart-y)>self.CANVAS_HEIGHT:
                break

        # blur the heat map

        #blurredHeatMap = scipy_ndimage.gaussian_filter(self.tempHeatMap, 4)


        canvas = np.array(self.tempCanvas, dtype=np.float32)
        heatMap = np.array(self.tempHeatMap, dtype=np.float32)
        heatMap = heatMap / 255

        return canvas, heatMap, self.tempCanvas, self.tempHeatMap,self.tempCanvasCopy,self.tempHeatMapCopy

    def genEvilExample(self):
        # generate a random paragraph
        lineCount = 10  # random.randint(1, 5)                                   # how many lines we want in our paragraph
        lineSpacing = random.randint(0, 10)  # how many pixels to leave between lines
        fontObj = self.getRandomFont()  # the font of our paragraph
        textSamples = [self.getRandomSnippet() for _ in range(lineCount)]  # text fragments to use for each line
        textSamples = [self.MIRROR_LETTERS_REGEX.sub('', ts) for ts in textSamples]  # see `MIRROR_LETTERS_REGEX`

        # compute the size of the text (note: text height is probably the same for all samples using the same font)
        sampleSizes = [fontObj.getsize(t) for t in textSamples]  # (width, height) tuples for each line of text
        totalParagraphHeight = (lineCount - 1) * lineSpacing + sum([sizeTuple[1] for sizeTuple in sampleSizes])

        # reset the image and heat map
        fg, bg = self.getRandomForegroundAndBackground()
        self.tempCanvasPainter.rectangle(self.CANVAS_RECTANGLE, bg)

        # paint the text and heat map (to their respective images)
        y = (self.CANVAS_HEIGHT / 2) - (totalParagraphHeight / 2)
        for i in range(lineCount):
            # figure out where and what we're going to draw
            textSample = textSamples[i]
            textWidth, textHeight = sampleSizes[i]
            x = random.randint(-textWidth, self.CANVAS_WIDTH)  # text may (intentionally) fall outside the canvas

            # draw the text
            self.tempCanvasPainter.text((x, y), textSample, font=fontObj, fill=fg)

            # update the "y" component to prepare for the next line
            y = y + textHeight + lineSpacing

        # clone the generated image a pair of numpy array; add some noise and blur
        canvas = np.array(self.tempCanvas, dtype=np.float32)
        canvas = scipy_ndimage.gaussian_filter(canvas, random.random())
        canvas += 0.5 * np.random.poisson(canvas) * random.random()

        return canvas[::-1, :]  # "[::-1, :]" is used to flip the Y axis

    '''
        insert rectangular shape in original image and insert mask in corresponding ground truth
    '''
    def genNoEasyEdges1(self,inserImage,nm):

        fg, bg = self.getRandomForegroundAndBackground()
        #self.tempCanvasPainter.rectangle(self.CANVAS_RECTANGLE, 'black')
        # self.hh.rectangle(self.CANVAS_RECTANGLE, 'black')
        # print("\n\t type=",type(self.tempHeatMap))
        # print("\n\t insert size=",inserImage.size)
        # print("\n\t original image size=",inserImage.size)

        draw = ImageDraw.Draw(self.tempHeatMap)

        '''
            get location of table insertion co-ordinate that location is already kept blank
        '''
        insertKeys=self.insertDict.keys()
        #print("\n\t insertKeys=",insertKeys)

        for indx,key in enumerate(insertKeys):

            '''
                this creates co-ordinates for insert image
            '''
            x1 = self.insertDict[key][0] #random.randint(0, self.CANVAS_WIDTH)
            x2 = self.insertDict[key][2] #random.randint(0, self.CANVAS_WIDTH)
            y1 = self.insertDict[key][1] #random.randint(0, self.CANVAS_HEIGHT)
            y2 = self.insertDict[key][3] #random.randint(0, self.CANVAS_HEIGHT)



            '''
            x1 = self.insertDict[key][0]  # random.randint(0, self.CANVAS_WIDTH)
            y1 = self.insertDict[key][1]  # random.randint(0, self.CANVAS_HEIGHT)


            dx,dy=inserImage.size
            
            
            x2 = x1+dx
            y2 = y1+dy
            '''


            #print "\n TABLE COORDINATE= 1.\t x1=",x1,"\t y1=",y1,"\t x2=",x2,"\t y2=",y2

            #print("\n\t width=",abs(x2-x1),"\t height=",abs(y2-y1))
            image = inserImage #.resize((abs(x2-x1),abs(y2-y1)))
            #image=inserImage

            shape =1 #random.randint(0, 4)
            if shape == 0:  # line
                r=random.randint(1, 32)
                self.tempCanvasPainter.line((x1, x2, y1, y2), "white", r)
                draw.line((x1, x2, y1, y2), "white", r)

            elif shape == 1:  # rectangle
                x1, x2 = min(x1, x2), max(x1, x2)
                y1, y2 = min(y1, y2), max(y1, y2)
                #print "\n 2s.\t x1=", x1, "\t y1=", y1, "\t x2=", x2, "\t y2=", y2
                #self.tempCanvasPainter.rectangle((x1, x2, y1, y2), "white")

                #draw.rectangle((x1, x2, y1, y2), "white")  # unable when drawing
                draw.rectangle((x1, y1, x2, y2), "white") #unable for inserting from other


                #self.tempHeatMap.paste(image,(x1,y1,x2,y2))

                try:
                    #from PIL import Image
                    #import PIL.ImageOps
                    #print("\n\t type=",type(image))

                    import PIL
                    #image=PIL.ImageOps.invert(image)

                    #input("check")
                    dfRowNo=self.df.shape[0]
                    self.df.loc[dfRowNo]=[str(nm)+"_"+"slastNormalCanvas.jpg",int(x1),int(x2),int(y1),int(y2)]

                    # self.df.iloc[dfRowNo,0]=nm
                    # self.df.iloc[dfRowNo,1]=int(x1)
                    # self.df.iloc[dfRowNo,1]=int(x2)
                    # self.df.iloc[dfRowNo,1]=int(y1)
                    # self.df.iloc[dfRowNo,1]=int(y2)

                    self.tempCanvas.paste(image,(int(x1),int(y1),int(x2),int(y2)))
                    #print "original image size=",self.tempCanvas.size
                    #print "\n\t insert image size",image.size
                    #self.tempCanvas.save(self.dumpPath + str(0) + "_slastNormalCanvas0.jpg")
                    #input("\n\t check")

                except Exception as e:
                    print ("original image size=",self.tempCanvas.size)

                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print("\n\t line no of exception=", exc_tb.tb_lineno)

                    #print ("\n\t insert image size",image.shape)
                    print("\n\t exception is e=",e)
                #self.tempCanvas.paste(image,(y2,y1,x2,x1))

        image = np.array(self.tempCanvas, dtype=np.float32)
        image = scipy_ndimage.gaussian_filter(image, random.random())
        image += 0.5 * np.random.poisson(image) * random.random()
        return image, self.tempCanvas, self.hh


    def genNoEasyEdges(self):
        fg, bg = self.getRandomForegroundAndBackground()
        self.tempCanvasPainter.rectangle(self.CANVAS_RECTANGLE, 'black')
        # self.hh.rectangle(self.CANVAS_RECTANGLE, 'black')

        for _ in range(3):
            x1 = random.randint(0, self.CANVAS_WIDTH)
            x2 = random.randint(0, self.CANVAS_WIDTH)
            y1 = random.randint(0, self.CANVAS_HEIGHT)
            y2 = random.randint(0, self.CANVAS_HEIGHT)

            shape = random.randint(0, 4)
            if shape == 0:  # line
                self.tempCanvasPainter.line((x1, x2, y1, y2), "white", random.randint(1, 32))
            elif shape == 1:  # rectangle
                x1, x2 = min(x1, x2), max(x1, x2)
                y1, y2 = min(y1, y2), max(y1, y2)
                self.tempCanvasPainter.rectangle((x1, x2, y1, y2), "white")
            elif shape == 2:  # ellipse
                x1, x2 = min(x1, x2), max(x1, x2)
                y1, y2 = min(y1, y2), max(y1, y2)
                self.tempCanvasPainter.ellipse((x1, x2, y1, y2), "white")
            elif shape == 3:  # triangle
                x3 = random.randint(0, self.CANVAS_WIDTH)
                y3 = random.randint(0, self.CANVAS_HEIGHT)
                self.tempCanvasPainter.polygon([(x1, y1), (x2, y2), (x3, y3)], "white")
            else:  # some vertical and horizontal lines
                self.tempCanvasPainter.line((x1, 0, x1, self.CANVAS_HEIGHT), "white")
                self.tempCanvasPainter.line((x2, 0, x2, self.CANVAS_HEIGHT), "white")
                self.tempCanvasPainter.line((0, y1, self.CANVAS_WIDTH, y1), "white")
                self.tempCanvasPainter.line((0, y2, self.CANVAS_WIDTH, y2), "white")

        image = np.array(self.tempCanvas, dtype=np.float32)
        image = scipy_ndimage.gaussian_filter(image, random.random())
        image += 0.5 * np.random.poisson(image) * random.random()
        return image, self.tempCanvas, self.hh

    lastNormalCanvas = None
    lastEvilCanvas = None
    lastNoEasyCanvas = None
    trainingHistory = []

    '''
        inserts verticle column in page 
    '''
    def insertColumn(self):
        # print "**"
        # print("\n\t 0.self.tempCanvas=",self.tempCanvas.size)
        # print("\n\t 1.self.tempHeatMap=",self.tempHeatMap.size)
        noColumns=1

        columnHeightEnd=random.random()*self.CANVAS_HEIGHT

        columnRect = (self.CANVAS_WIDTH/2, 0, self.CANVAS_WIDTH/2 + 20, columnHeightEnd)
        #self.tempHeatMapPainter.rectangle(heatRect, "white")
        self.tempCanvasPainter.rectangle(columnRect, 'black')  # rgb(255, 255, 255)
        self.tempCanvasPainterCopy.rectangle(columnRect, 'black')  # rgb(255, 255, 255)
        # self.tempCanvasPainter.rectangle(self.CANVAS_RECTANGLE, "black")
        self.tempHeatMapPainter.rectangle(columnRect, "black")


    '''
        ^.0 THIS FUNCTION MUST BE MERGED WITH readimages
        READS ALL FILES IN A FOLDER
    '''

    def readAllImages(self):

        self.imageNameList = os.listdir(self.hitImagesPath)
        self.imagesList = []
        self.imagesListPath = []
        self.readImageCount=50

        for indx, img in enumerate(self.imageNameList):
            # print "\n\t img=",img
            # print "\n\t location=",location

            # print "\n\t is image=",os.path.isfile(location+img)
            #tempImage = cv2.imread(self.location + img)

            tempImage=Image.open(self.hitImagesPath +"//"+ img)
            self.imagesListPath.append(self.hitImagesPath +"//"+ img)

            # print "\n\t tempImage shape= ",tempImage.shape
            #gray=rgb

            self.imagesList.append(tempImage)

            if self.readImageCount>1000000:
                break

            #tempImage = cv2.resize(tempImage, (15, 15))
            #cv2.imwrite("/home/kapitsa/Documents/Dataset/crop/hitImages_resize//" + img, tempImage)
            tempImage.close()
        #return imagesList


    def insertFigure(self,nm):

        #print("\n\t this function inserts figures")
        #inserImage= Image.open(imagePath)

        #imgNo=random.randint(0,self.readImageCount)

        '''
            randomly choosing table image
        '''
        imgNo=self.randTabIndx #nm#%len(self.imagesList)
        inserImage = self.imagesList[imgNo]
        
        '''
            important change
        '''
        inserImage =Image.open(self.imagesListPath[imgNo])

        _,self.tempCanvas,self.hh_=self.genNoEasyEdges1(inserImage,nm)


    def genTrainingSet(self, nm):

        evilProb = 0.95  # this is evil images probability
        canvas, heatMap, self.tempCanvas, self.tempHeatMap,self.tempCanvasCopy,self.tempHeatMapCopy = self.genTextAndHeatMap(nm)
        '''
            column insert
        '''
        self.insertColumn()

        #print "\n\t insert dict=",self.insertDict
        # self.tempHeatMap.save(self.dumpPathS + str(nm)+"_sheatMap.jpg")

        '''
        self.tempCanvas.save(self.dumpPath + str(nm) + "_slastNormalCanvas0.jpg")
        self.tempHeatMap.save(self.dumpPathS + str(nm) + "_slastNormalCanvas0.jpg")
        '''
        self.insertFigure(nm)

        self.tempCanvas.save(self.dumpPath + str(nm) + "_slastNormalCanvas.jpg")
        self.tempCanvasCopy.save(self.dumpPath1+ str(nm) + "_slastNormalCanvas.jpg")
        # self.tempHeatMap.save(self.dumpPathS + str(nm)+"_sheatMap.jpg")
        self.tempHeatMap.save(self.dumpPathS + str(nm) + "_slastNormalCanvas.jpg")

        #self.hh.save(self.dumpPathS + str(nm) + "_slastNormalCanvas.jpg")
        #cv2.imwrite(self.dumpPathS + str(nm) + "_slastNormalCanvas.jpg",self.hh)
        self.lastNormalCanvas = canvas
        # self.lastHeatMap=heatMap

        if random.random() > evilProb and self.genEvilExmpl==1:
            _, _, self.hh = self.genNoEasyEdges()
            self.tempCanvas.save(self.dumpPath + str(nm) + "_genNoEasyEdges.jpg")
            cv2.imwrite(self.dumpPathS + str(nm) + "_genNoEasyEdges.jpg", self.hh)
            # input("check")
            self.lastNoEasyCanvas = canvas


    def trainingRound(self, nm):

        # print("\n\t nm=",nm,"\t type=",type(nm))
        self.genTrainingSet(nm)

        return 1

    def trainingLoop(self, n, interactive=True):

        self.readAllImages() # this reads all images that we want to insert currently re
        for i in range(n):
            if i % 1000 == 0:
                print ("\n\t image no=", i)
            loss = self.trainingRound(i)  # here training happens
        self.df.to_csv("/home/wipro/PycharmProjects/wsl/wsl-master/publicationData/9/tableRelatedAll/delMe//train.csv")
            #input("New Page")


tr = TextDetectorTrainer()

tr.trainingLoop(50)  # 1000 shows no of Document Images to generate

os.system('spd-say "your program has finished"')
