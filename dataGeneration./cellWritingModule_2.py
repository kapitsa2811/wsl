'''
    aim of this code is to write a text in cells of a table
    tables are generated by code randomTablePaper_2.py
    cellExtractionModule.py creates a dictionary of cells and its locations
    here it is supposed to read cells and write text in it
    further this tables will be used by syntheticDocGeneration_22.py for creating synthetic page level data
'''
import sys
from PIL import Image, ImageDraw, ImageFont
import math
import os
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

class TextDetectorTrainer:
    """
        A class that generates random training examples for the text detector neural net.
        Some examples are pictures of text, some examples are adversarial (to prevent the network from
        learning a simpler function than what we want).
    """

    def __init__(self, corpus=None, fonts=None):
        # self.net = model
        # self.dumpPath="/home/kapitsa/pyCharm/segmentation/Convolutional-Encoder-Decoder-for-Hand-Segmentation-master/newData//imageWord//"
        # self.dumpPathS="/home/kapitsa/pyCharm/segmentation/Convolutional-Encoder-Decoder-for-Hand-Segmentation-master/newData//segWord//"


        self.experimentNo = str(8)
        self.basePath = "///home/kapitsa/pyCharm/segmentation/weaklySupervisedSegmentation/publicationData//"

        # '''
        self.dumpPath = self.basePath+self.experimentNo+"//train//imageWord//"
        self.dumpPathS = self.basePath+self.experimentNo+"//train//segWord//"
        # '''

        self.cropLocation = self.basePath+self.experimentNo+"//"#"/home/kapitsa/Documents/Dataset/crop/"
        #self.hitImagesPath = os.path.join(self.cropLocation, "blackTable")  # already generated tables
        self.hitImagesPath = os.path.join(self.cropLocation, "table") +"//" # already generated table
        if corpus is not None:
            self.TEXT_CORPUS = corpus
        else:
            #self.TEXT_CORPUS = open("text/corpus.txt",encoding="utf-16").read().replace('\n', ' ')

            with codecs.open("text/corpus.txt", 'r', encoding='utf8') as f:
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
            #for size in range(10, 30)
            for size in range(15, 20)
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
        self.CANVAS_WIDTH = 500
        self.CANVAS_HEIGHT = 800

        self.CANVAS_RECTANGLE = (0, 0, self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        self.tempCanvas = Image.new("L", (self.CANVAS_WIDTH, self.CANVAS_HEIGHT))
        self.tempHeatMap = Image.new("L", (self.CANVAS_WIDTH, self.CANVAS_HEIGHT))

        # "Painter" objects encapsulate the implementation of algorithms for drawing to an image.
        # With these objects, we will use `.rectangle()` and `.text()` to cause updates to the `temp*` images above.
        self.tempCanvasPainter = ImageDraw.Draw(self.tempCanvas)
        # self.hh = ImageDraw.Draw(self.tempCanvas)
        # self.hh = ImageDraw.Draw(self.tempHeatMap)
        self.hh = np.zeros((self.CANVAS_WIDTH, self.CANVAS_HEIGHT, 3))
        self.tempHeatMapPainter = ImageDraw.Draw(self.tempHeatMap)

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
            snippetStart = random.randint((corpusLength - snippetLength - 1)/2, corpusLength - snippetLength - 1)
        else:
            snippetStart = random.randint(0, (corpusLength - snippetLength - 1)/2)


        snippetStop = snippetStart + snippetLength # total length of line

        #print "\n\n\t snippetStart =",snippetStart,"\t snippetStop =",snippetStop,"\t length=",(snippetStop-snippetStart)
        return corpus[snippetStart:snippetStop]



    #@staticmethod
    def genTextAndHeatMap(self):
        print("**")
        fontObj = self.getRandomFont()  # the font of our paragraph
        print("\n\t fontObj =",fontObj)


        # generate a random paragraph
        lineBegining=0
        disableJunk=1
        lineCount = 20  # random.randint(1, 50)          # how many lines we want in our paragraph
        lineSpacing = 20 #random.randint(10, 30)  # how many pixels to leave between lines
        fontObj = self.getRandomFont()  # the font of our paragraph
        textSamples = [self.getRandomSnippet() for _ in range(lineCount)]  # text fragments to use for each line

        #print("\n\t textSamples =",textSamples)

        LineWord =[] #defaultdict(list)  # dict()# line no is key

        '''
            words which contains less than 7 characters are choosen
        '''

        for lineNo, wrdLine in enumerate(textSamples):

            for wordNo, wrd in enumerate(wrdLine.split(" ")):
                # print "\n\t\t WordSize=",wordSize[wrd]
                if len(wrd)<7:
                    LineWord.append(wrd)  # = [wrdLine]

        #print("\n\t LineWord=",LineWord)

        listSize=len(LineWord)

        #self.tempCanvasPainter.text((10, 10),"hi", font=fontObj, fill='white')  # fg
        #canvas = np.array(self.tempCanvas, dtype=np.float32)

        #basePath = "/home/kapitsa/pyCharm/segmentation/Convolutional-Encoder-Decoder-for-Hand-Segmentation-master/paper/publicationData//"
        dictSave = self.basePath +self.experimentNo+ "//tableRelatedAll//"
        readImage=self.basePath+self.experimentNo+"//tableRelatedAll/delMe//"
        tableRead=self.basePath+self.experimentNo+"//table//"
        read_dictionary = np.load(dictSave + 'delMe//'+'cellLocation.npy').item()
        writePath=self.basePath+self.experimentNo+"//textTables//"
        #print("\n\t\t read_dictionary =",read_dictionary)


        for imageName in read_dictionary.keys():
            print("\n\t imageName=",imageName)

            if imageName.__contains__("_dummy_"):
                 continue

            #folderName=imageName.split(".jpg")[0]
            #print("\n\t\t folder name=",folderName)

            t=read_dictionary[imageName]
            #allComponents=os.listdir(readImage+folderName)
            #print("\n\t\t t=",t)

            try:
                dummyImageName=imageName.split(".jpg")[0]+"_dummy_"+".jpg"
                print("\n\t dummyImageName=",dummyImageName,"\t\t is present=",os.path.isfile(tableRead+ "//" +dummyImageName))

                '''
                    reads dummy table image
                '''
                self.temp = Image.open(tableRead+ "//" + dummyImageName)
                self.textWriter=ImageDraw.Draw(self.temp)

                '''
                    reads original image
                '''
                self.temp1 = Image.open(tableRead+ "//" + imageName)
                self.textWriter1=ImageDraw.Draw(self.temp1)

                print "\n\t\t\t image size=", self.temp.size

                for ccid in t:
                    # print "\n\t\t\t ccid=",ccid
                    # print("\n\t\t\t t[ccid]=",t[ccid])

                    '''                    
                    startX=t[ccid][0]+(t[ccid][0]+t[ccid][2])/10
                    startY=t[ccid][1]+(t[ccid][1]+t[ccid][3])/5

                    endX=t[ccid][2]-abs(t[ccid][0]+t[ccid][2])/10
                    endY=t[ccid][3]-abs(t[ccid][1]+t[ccid][3])/5
                    '''
                    startX=t[ccid][0]+abs(t[ccid][0]-t[ccid][2])/10
                    startY=t[ccid][1]+abs(t[ccid][1]-t[ccid][3])/3

                    endX=t[ccid][2]-abs(t[ccid][0]-t[ccid][2])/10
                    endY=t[ccid][3]-abs(t[ccid][1]-t[ccid][3])/3


                    #print("\n\t midX=",midX,"\t midY=",midY)

                    randWordIndx=random.randint(0,listSize)
                    randWord=LineWord[randWordIndx]
                    # self.textWriter.text((startX,startY,endX,endY), randWord, font=fontObj, fill='white')  # fg
                    # self.temp.save(writePath + dummyImageName)

                    startX=t[ccid][0]+abs(t[ccid][0]-t[ccid][2])/5
                    startY=t[ccid][1]#+abs(t[ccid][1]-t[ccid][3])

                    endX=t[ccid][2]-abs(t[ccid][0]-t[ccid][2])/5
                    endY=t[ccid][3]-abs(t[ccid][1]-t[ccid][3])

                    self.textWriter1.text((startX,startY,endX,endY), randWord, font=fontObj, fill='white')  # fg
                    self.temp1.save(writePath +"0"+imageName)

                    self.textWriter.text((startX,startY,endX,endY), randWord, font=fontObj, fill='white')  # fg
                    self.temp.save(writePath + dummyImageName)


            except Exception as e:
                print("\n\t\t\t exception for image=",imageName,"\t e=",e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("\n\t LINE NO:", exc_tb.tb_lineno)
                print("\n\t 1.type=",type(self.tempCanvas))
                print("\n\t 2.type=",type(self.temp))

            '''
            for compId in t.keys():
                print("\n\t\t\t compId=",compId)
            '''
            #input("check")
        #self.temp.save()
        #self.tempCanvas.save(writePath + "slastNormalCanvas0.jpg")


    #genTextAndHeatMap()

tr = TextDetectorTrainer()

tr.genTextAndHeatMap()