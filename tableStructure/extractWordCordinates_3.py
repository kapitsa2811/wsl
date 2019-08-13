'''

This code is copy of extractWordCordinates_2.py
This assumes that already .hocr file is created and kept in folder hocr

'''

import csv
import cv2
#from pytesseract import pytesseract as pt
import copy
import os
#from allVariables import *
import subprocess
import warnings
import sys
import pandas as pd
from lxml.html import *

pwd=os.getcwd()
print ("\n\t pwd=",pwd)

hocrPaths=pwd+"//hocr//"
imagePath=pwd+"//image//"
imageNames=os.listdir(imagePath)
print ("\n\t imageNames=",imageNames)
print("\n\t length=",len(imageNames))
#indx=2
output = pd.DataFrame(columns=['indx', 'word_2'])

totalLineCount=0

for indx,imageName in enumerate(imageNames):
    print("\n\t indx=",indx,"\t ",imageName)
    in1=imagePath+imageName
    print("\n\t in1=",in1)
    #out1=pwd+"ocrOut_3.04\\out\\"
    #out1=imagePath+imageNames[indx][0].split(".")[-1:][0]

    out1=in1.split("//")[-1]
    out1=out1.split(".")[0]
    print("\n\t out1=",out1)

    image=cv2.imread(in1)
    print("\n\t image=",image.shape)


    # if not os.path.exists(out1+imageNames[indx][0].split(".")[-1:][0]):
    #     os.makedirs(out1+imageNames[indx][0].split(".")[-1:][0])

    print("\n\t out1=",out1)

    tempPath=pwd+"//csv//"
    #print("\n\t imagePath+out1",tempPath+out1)


    if not os.path.exists(tempPath+out1):
        os.makedirs(tempPath+out1)

    #output=pd.read_csv(tempPath+"out.csv")

    #output=pd.read_csv(pwd+"ocrOut\\"+imageNames[indx][0].split(".")[-1:][0]+"\\out.csv")
    #print ("output shape=",output.shape)


    # http://blog.humaneguitarist.org/2017/01/28/redacting-naughty-words-in-images-with-tesseract-imagemagick-and-dish-soap/
    # open HOCR XHTML file; get all OCR words as list "ocrWords".
    root = parse(hocrPaths+out1+".png.html")
    body = root.find('body')
    ocrWords = body.findall('.//span[@class="ocrx_word"]')

    i = 1
    wordDict = {}
    for indx,ocrWord in enumerate(ocrWords):
      node = ocrWord.text_content()
      if node != None:
        node = "".join([n for n in node.lower() if n.isalnum()]) # alphanumeric characters only.
        # if node != "tree":
        #   continue
        coordinates = ocrWord.get("title")
        coordinates = coordinates.split(" ")
        coordinate = coordinates.pop(0) # remove word "bbox" from attribute value.
        #print("\n\t coordinate=",coordinates)
        word = {}
        word["text"] = node
        word["left"] = coordinates[0]
        x1=int(coordinates[0])

        word["top"] = coordinates[1]
        y1=int(coordinates[1])

        word["right"] = coordinates[2]
        x2=int(coordinates[2])

        word["bottom"] = coordinates[3][0:-1]
        y2=int(word["bottom"])
        wordDict[i] = word

        #print("\n\t node=",node,"\t ",[x1,y1,x2,y2],"\t word=",word["text"])

        #print("\n\t node=",node,"\t ",[x1,y1,x2,y2],"\t word=",word)

        #print("\n\t indx=",indx)

        #print("\n\t node=",node,"\t ",[x1,y1,x2,y2],"\t word=",word)

        output.loc[totalLineCount+indx,"indx"]=indx

        output.loc[totalLineCount+indx,"fileName"]=imageName
        output.loc[totalLineCount+indx,'word_1']=word['text']
        output.loc[totalLineCount+indx, 'cordinate_1'] = str([x1,y1,x2,y2])
        output.loc[totalLineCount+indx,'mid_cordinate_1_x']=(x1+x2)/2*1.0
        output.loc[totalLineCount+indx,'mid_cordinate_1_y']=(y1+y2)/2*1.0


        try:
            if word['text']==output.loc[indx,'word_1']:
                #output.loc[indx,"indx_2"]=indx
                output.loc[totalLineCount+indx,'word_2']=word['text']
                output.loc[totalLineCount+indx,'mid_cordinate_2_x']=(x1+x2)/2*1.0
                output.loc[totalLineCount+indx,'mid_cordinate_2_y']=(y1+y2)/2*1.0
            elif word['text']==output.loc[indx,'word_1']:
                #output.loc[indx,"indx_1"]=indx
                output.loc[totalLineCount+(indx+1),'word_2']=word['text']
                output.loc[totalLineCount+(indx+1),'mid_cordinate_2_x']=(x1+x2)/2*1.0
                output.loc[totalLineCount+(indx+1),'mid_cordinate_2_y']=(y1+y2)/2*1.0
            else:
                output.loc[totalLineCount+indx,'word_2']=word['text']
                output.loc[totalLineCount+indx,'mid_cordinate_2_x']=(x1+x2)/2*1.0
                output.loc[totalLineCount+indx,'mid_cordinate_2_y']=(y1+y2)/2*1.0
        except Exception as e:
            pass

        try:
            nm=str([x1,y1,x2,y2])
            output.loc[indx,'cordinate_2']=nm
            crop_image=image[y1:y2, x1:x2]
            #showImage(crop_image,nm)
            del crop_image

            cv2.line(image, (x1,y1), (x2,y2), (255, 0, 0), 5)

            imS = cv2.resize(image, (540, 540))
            #cv2.imshow("temp", imS)
            #cv2.WaitKey()

            #cv2.waitKey(0)

            output.loc[totalLineCount+indx, 'x1'] = x1
            output.loc[totalLineCount+indx, 'y1'] = y1
            output.loc[totalLineCount+indx, 'x2'] = x2
            output.loc[totalLineCount+indx, 'y2'] = y2

        except Exception as e:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print("\n\t line no of exception in prep_data1:", exc_tb.tb_lineno)

            print("\n\t exception")

      i += 1
      totalLineCount=totalLineCount+indx

    print("\n\t totalLineCount=",totalLineCount)
    #input("check")
    #print ("\n\t out1=",out1)

output.to_csv(tempPath+"out.csv",encoding='utf-8',index=False)



