#!/usr/bin/env python
import random
import sys
import os
import numpy
from PIL import Image, ImageDraw
import cv2

versionNo=3

'''
    this code creates a tables.
    aim of the code is to modify random table for paper publication
    Insert text inside table make tables with and without border
    
    module is replacing the randomTablesPaper.py mpodule
    it creates 2 images for single pass one is table with all row and column border present and other is table with random row and column
    missing
    
'''

basePath = "///home/kapitsa/pyCharm/segmentation/weaklySupervisedSegmentation/publicationData//"

experimentNo=str(8)
writePath = basePath + experimentNo+"//table//" # at this location we are writing tables
dumyThreshold=0.6

'''
    no: No of tables
'''
def drawTable(no,hstep_count=random.randint(1,100),height=600,width=600):

    try:
        '''
            height and width of table
            step_count =?
            hstep_size: indicates horizontal width of the cell
        '''
        #height,width=random.randint(1,1000),random.randint(1,1000)
        #hstep_count =0

        noTablesWritten = 0
        tableList=[]

        print "\n\t NO OF ROWS=",hstep_count
        #print "h=",height,"\t w=",width,"\t hstep_count=",hstep_count

        sHstep,sVstep=0,0
        tabInfo={}# image name is key and value is 2nd dict containing horizontal and verticle lines

        for indx in range(no):
            tempLines={}# stores verticle and horizontal lines and parameters
            if random.random() > 0.85:
                if random.random() > 0.25:
                    hstep_count = random.randint(3, 7)
                else:
                    hstep_count = random.randint(7, 12)

            tabCor=[None]*4
            #height,width=100+random.randint(0,height),100+random.randint(0,width)
            height,width=100+random.randint(0,200),100+random.randint(0,500)
            image=numpy.ones((height,width))*255
            dumyImage=numpy.ones((height,width))*255
            # Draw some lines
            y_start = 0
            y_end = height

            '''
                hstep_size = no of columns    
            '''
            hstep_size = int(width / hstep_count)

            if hstep_size==0:
                hstep_size =3

            tempLines["hstep_count"]=hstep_count
            tempLines["hstep_size"]=hstep_size

            w1=random.randint(1,2)
            lineThickness= 1 #w1
            tempLines["lineThickness"]=lineThickness
            '''
                draws verticle line
            '''
            vLines=[]
            for x in range(0, width, hstep_size):
                #line = ((x, y_start), (x, y_end))
                cv2.line(image, (x, y_start), (x, y_end), (0, 255, 0), lineThickness)
                vLines.append([x, y_start, x, y_end])

                if random.random()>dumyThreshold:
                    cv2.line(dumyImage, (x, y_start), (x, y_end), (0, 255, 0), lineThickness)

            tabCor[1],tabCor[3]=y_start,y_end

            x_start = 0
            x_end = width

            tabCor[0],tabCor[2]=x_start,x_end

            w2=random.randint(1,2)
            #w2=random.random()*w2

            lineThickness=1
            tempLines["lineThickness2"]=lineThickness
            if random.random() > 0.5:
                step_count = abs(hstep_count+random.randint(2,hstep_count))+1
            else:
                step_count = abs(hstep_count-random.randint(2,hstep_count))+1

            #print("\n\t width=",width,"\t step_count=",step_count)
            step_size = int(height / step_count)

            if step_size==0:
                step_size =2


            tempLines["step_count"]=step_count
            tempLines["step_size"]=step_size
            hLines=[]

            '''
                draws horizontal line
            '''
            for y in range(0,height, step_size):
                line = ((x_start, y), (x_end, y))
                cv2.line(image, (x_start, y), (x_end, y), (0, 255, 0), lineThickness)
                hLines.append([x_start, y, x_end, y])

                if random.random()>dumyThreshold:
                    cv2.line(dumyImage, (x_start, y), (x_end, y), (0, 255, 0), lineThickness)


            tempLines["horizontal_lines="]=hLines
            tempLines["verticle_lines="] = vLines

            nm = str(indx) + "_" + str(step_count) + "_" + str(hstep_count) + "_" + str(tabCor) + "_" + str(step_size)+"_"+str(hstep_size) + ".jpg"
            nmd = str(indx) + "_" + str(step_count) + "_" + str(hstep_count) + "_" + str(tabCor) + "_" + str(step_size)+"_"+str(hstep_size) + "_dummy_.jpg"

            '''
                below circles are to verify start and end
            '''
            #cv2.circle(image, (x_start,y_start),30, thickness=8, lineType=8, shift=0,color=1)
            #cv2.circle(image, (x_end,y_end),30, thickness=8, lineType=8, shift=0,color=1)


            '''
                below if condition is determined by trail and error it makes table look better
            '''
            if  (step_count*hstep_count<40)and (step_count*hstep_count>20) and(step_size<40 and step_size>20) and(hstep_size<200 and hstep_size>100):
                cv2.imwrite(writePath+nm, 255-image)
                cv2.imwrite(writePath+nmd, 255-dumyImage)
                tabInfo[nm] = tempLines
                noTablesWritten+=1
                tableList.append(image)

            '''    
            elif random.random()>0.9:

                cv2.imwrite(writePath+nm, 255-image)
                tabInfo[nm] = tempLines
                noTablesWritten+=1
                tableList.append(image)
            '''

            sHstep=sHstep+hstep_count
            sVstep=sVstep+step_count
            '''
            print "\n\t indx=",indx
            print "\n\t\t h=", height, "\t w=", width
            print "\n\t\t  step_size=",step_size,"\t width=",width
            print "\n\t\t  w1=",w1,"\t w2=",w2
            '''
            tableList.append(image)
            #print("\n\t TOTAL TABLES WRITTEN=", noTablesWritten)

    except Exception as e:
        print "\n\t e=",e
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("\n\t line no=", exc_tb.tb_lineno)

    #print("\n\t horizontal avg=",int(sHstep/no*1.0),"\t verticle avg=",int(sVstep/no*1.0))

    #return tableList


if __name__ == "__main__":
    try:

        tableList=drawTable(15000,5,500,500)

    except Exception as e:
        pass
