import cv2
import glob #import glob
import os
import numpy as np
from getCC import *
from horizontalAndVerticalLines import *

cwd=os.getcwd()+"//"
#path=cwd+"predict"+"//"

#basePath = "///home/kapitsa/pyCharm/segmentation/weaklySupervisedSegmentation/publicationData//"
basePath="/home/kapitsa/pyCharm/segmentation/weaklySupervisedSegmentation/publicationData//"

expNo = str(8)

path=basePath+expNo+"//results//"

allFiles=glob.glob(path + "/*.png")

#print(allFiles)


tempImg=cv2.imread(path+"2_original.png")
tempImg=255-tempImg
#print(tempImg.shape)


def lineExtract(img):

    dummyImage=np.zeros(img.shape)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(img.shape)
    # Apply edge detection method on the image
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    print(edges.shape)
    cv2.imwrite(cwd+"lineResults//edges.jpg",edges)

    # This returns an array of r and theta values
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

    print("\n\t lines=",len(lines))

    # The below for loop runs till r and theta values
    # are in the range of the 2d array

    '''
    for r, theta in lines[0]:
        # Stores the value of cos(theta) in a
        a = np.cos(theta)

        # Stores the value of sin(theta) in b
        b = np.sin(theta)

        # x0 stores the value rcos(theta)
        x0 = a * r

        # y0 stores the value rsin(theta)
        y0 = b * r

        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
        x1 = int(x0 + 1000 * (-b))

        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
        y1 = int(y0 + 1000 * (a))

        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
        x2 = int(x0 - 1000 * (-b))

        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
        y2 = int(y0 - 1000 * (a))

        # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
        # (0,0,255) denotes the colour of the line to be
        # drawn. In this case, it is red.
        cv2.line(dummyImage, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # All the changes made in the input image are finally
    # written on a new image houghlines.jpg
    '''

    minLineLength = img.shape[1] - 300
    lines = cv2.HoughLinesP(image=edges, rho=0.02, theta=np.pi / 180, threshold=10, lines=np.array([]),
                            minLineLength=minLineLength, maxLineGap=100)

    a, b, c = lines.shape
    for i in range(a):
        cv2.line(dummyImage, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)

    cv2.imwrite(cwd+'lineResults//linesDetected.jpg', dummyImage)

#lineExtract(tempImg)

'''
    1.from result file get location of aura
    2.find cc on original image 
    3. find out which cc present in aura rgion
    4. extract and write only those cc
'''


def LinesEnhancement(indx,img):
    print("\n\t this function extracts table lines")
    #img = cv2.imread(img_for_box_extraction_path, 0)


    # Thresholding the image
    #(thresh, img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Invert the image
    img_bin = img#255 - img_bin
    #cv2.imwrite("./lineResults//Image_bin.jpg", img_bin)

    kernel_length =1 #np.array(img).shape[1] / 30

    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.

    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))


    # Morphological operation to detect vertical lines from an image
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=5)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=5)
    cv2.imwrite("./lineResults//"+str(indx)+"b1_verticle_lines.jpg",verticle_lines_img)


    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=5)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=5)
    cv2.imwrite(basePath+expNo+ "/delMe/lineResults//"+str(indx)+"b3_img_final_bin_E"+str(100)+"33.jpg",horizontal_lines_img)

    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    # img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=1)
    #(thresh, img_final_bin) = cv2.threshold(img_final_bin, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imwrite(basePath+expNo+ "/delMe/lineResults//"+str(indx)+"b3_img_final_bin_D"+str(100)+"33.jpg",img_final_bin)

    return img_final_bin

def tableLines(indx,img):

    finalTable=np.ones(shape=img.shape)
    #print(img.shape)
    #img = cv2.imread('dave.jpg')
    #gray =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = cv2.merge((img, img, img))
    acticeLoc=np.where(img2<30)


    finalTable=np.ones(shape=img2.shape)
    #print(img2.shape)

    #img=LinesEnhancement(indx, img)

    edges = cv2.Canny(np.uint8(img2), 0, 200, apertureSize=3)
    cv2.imwrite(basePath+expNo+ "/delMe/lineResults//"+str(indx)+"b3_img_final_bin_"+str(10)+"33.jpg",edges)


    edges1 = cv2.Canny(np.uint8(img2), 100, 200, apertureSize=3)
    cv2.imwrite(basePath+expNo+ "/delMe/lineResults//"+str(indx)+"b3_img_final_bin_"+str(100)+"33.jpg",edges1)

    minLineLength = 200
    maxLineGap = 100

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 15, minLineLength, maxLineGap)
    for x in range(0, len(lines)):
        for x1, y1, x2, y2 in lines[x]:
            cv2.line(finalTable, (x1, y1), (x2, y2), (255, 255, 0), 2)


    cv2.imwrite(basePath+expNo+ "/delMe/lineResults//"+str(indx)+"b3_img_final_bin_"+str(100)+"3.jpg",finalTable)
    #print(img2.shape)

def tableFromAura(indx,originalImage,auraImageName):

    try:
        #originalImage="2_original.png"
        #print(path)
        #print("\n\t is file=",os.path.isfile(path + originalImage))
        #input("***")

        originalImg=cv2.imread(path + originalImage)

        #tempLocation="/home/kapitsa/pyCharm/segmentation/weaklySupervisedSegmentation/publicationData/8/delMe/lineResults//"
        #cv2.imwrite(tempLocation+str(indx)+'_bcoriginal.jpg',originalImg)
        cv2.imwrite(basePath+expNo+ "/delMe/lineResults//"+ str(indx) + '_original.jpg', originalImg)
        #print(tempImg.shape)

        tempOriginal=cv2.cvtColor(originalImg,cv2.COLOR_BGR2GRAY)
        #print(tempImg.shape)
        output,labels,stats=findConnectedComponents(tempOriginal)
        #print("\n\t label non zero=",len(np.where(labels>0)))

        #auraImageName="2_cam_map.png"

        #print("\n\t is aura image present=",os.path.isfile(path+auraImageName))
        #print("\n\t aura image path=",path+auraImageName)
        auraImage=cv2.imread(path+auraImageName)
        #print("\n\t shape=>>>",auraImage.shape)
        #input("***")
        #cv2.imwrite(cwd+'lineResults//aura.jpg', auraImage)
        #print(tempImg.shape)

        #rows,col=np.where(auraImage==threshold)
        #print("\n\t row=",rows,"\t col=",col)
        #print("\n\t average pixel value =", np.average(auraLocation))
        #print("\n\t len=",len(auraLocation))
        #print("\n\t auraLocation=",len(auraLocation))

        # for loc in auraLocation:
        #     print("\n\t loc=",loc,"\t ",len(loc))

        '''
            from heatmap locations where value is >1 is choosen
        '''

        tempAura=cv2.cvtColor(auraImage,cv2.COLOR_BGR2GRAY)
        activeLocations=np.where(tempAura>0)

        tempAura1=np.zeros(shape=tempAura.shape)
        tempAura1[activeLocations]=1.0


        # print("\n\t tempAura1 len",tempAura1.shape[0]*tempAura1.shape[1])
        # print("\n\t tempAura1 sum=",tempAura1.sum())
        # print("\n\t tempAura1 sum=",tempAura.sum()/255)

        # print("\n\t average pixel value in tempAura=", np.average(tempAura))
        # print("\n\t average pixel value in tempAura1=", np.average(tempAura1))

        #print("\n\t len=",len(auraLocation))


        '''
        labels1=255*labels
        cv2.imwrite(cwd+'lineResults//labels.jpg', labels1)
        '''

        duplicateLabels=np.zeros(shape=labels.shape)
        #duplicateLabels =np.logical_and(tempAura,labels)


        '''
            below multiplication merges aura image with original image and projects 
            models area of interest  it does not include any other part
        '''
        focusImage =np.multiply(tempAura,tempOriginal)
        focusImage=255*focusImage
        #cv2.imwrite(basePath+expNo+ "/delMe/lineResults//"+str(indx)+'_afocusImage.jpg', focusImage)


        '''
            below multiplication merges aura image with label image and projects 
            which component we should extract 
        '''

        #cv2.imwrite(cwd + 'lineResults//' + str(indx)  + '_label.jpg',255 * labels)

        '''
            in below multiplication tempAura1 has value 1 where model is focusing
            so duplicateImage contains component which we should focus
        '''
        duplicateImage =np.multiply(tempAura1,labels)
        #duplicateImage=255*duplicateImage
        uniueID=np.unique(duplicateImage)
        nonPresentID=[]#
        allCompId=np.unique(labels)

        '''
        print("\n\t 1.allCompId=",len(allCompId))

        for idIndx,idComp in enumerate(allCompId):

            if idComp not in uniueID:
                nonPresentID.append(idComp)

        print("\n\t 2.nonPresentID=",len(nonPresentID))
        '''

        # print("\n\t labels len",labels.shape[0]*labels.shape[1])
        # print("\n\t labels sum=",labels.sum())
        # print("\n\t duplicateImage sum=",duplicateImage.sum())
        # print("\n\t is equal len=",len(np.where(duplicateImage==labels)))
        # print("\n\t is equal=",np.where(duplicateImage==labels))
        a,b=np.where(duplicateImage==labels)
        # print("\n\t a len=",len(a))
        # print("\n\t b len=",len(b))


        '''
        labels2=labels[np.where(labels==uniueID)]
        cv2.imwrite(cwd + 'lineResults//' + str(indx)+"_"+str(len(np.where(labels==uniueID))) +'_label2.jpg',255 * labels2)
        '''
        # print("\n\t uniueID2 in duplicateImage=",len(uniueID))
        # print("\n\t uniueID1 in labels =",len(np.unique(labels)))

        #input("debug check")
        tempCopy=np.ones(shape=labels.shape)
        extract=np.ones(shape=originalImg.shape)
        '''
            extract components of interest
        '''
        print("\n\n")

        for comID in uniueID:

            if comID >0:
                # tempCopy[tempCopy > comID] = 0
                # tempCopy[tempCopy < comID] = 0
                tempCopy[labels == comID] = 0
                #print("\n\n")
                #print("\n\t 1.compID=",comID)
                al,bl=np.where(labels==comID)
                #print("\n\t in labels","\n\t \t a len=",len(al),"\t b len=",len(bl))
                ad,bd=np.where(labels==comID)
                #print("\n\t in duplicateImage","\n\t \t a len=",len(ad),"\t b len=",len(bd),"\t is same ",len(bd)==len(bl))
                # if comID%10==0:
                #     input("debug")


        tempCopy1=tempOriginal#np.ones(shape=labels.shape)

        for comID in np.unique(allCompId):

            if comID in uniueID:
                if comID > 0:
                    # tempCopy[tempCopy > comID] = 0
                    # tempCopy[tempCopy < comID] = 0
                    tempCopy1[labels == comID] = 0

                    x = stats[comID][0]
                    dx = stats[comID][2]
                    y = stats[comID][1]
                    dy = stats[comID][3]

                    tempCopy1[y:(y + dy), x:(x + dx)]=0

                    crop = originalImg[y:(y + dy), x:(x + dx)]
                    extract[y:(y + dy), x:(x + dx)] = crop

        cv2.imwrite(basePath + expNo + "/delMe/nonFocus//" + str(indx) + "nonFocus.jpg", 255-tempCopy1)
        cv2.imwrite(basePath+expNo+ "/delMe/nonFocus//"+str(indx)+'Focus.jpg', 255*extract)
        cv2.imwrite(basePath+expNo+ "/delMe/nonFocus//"+ str(indx) + '_original.jpg', originalImg)
        #tableLines(indx, 255*tempCopy)
        call(255*tempCopy,originalImg, basePath, expNo,indx)
        #input("check")
    except Exception as e:
        print("\n\t exception is e=",e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("\n\t line no:", exc_tb.tb_lineno)




for indx in range(1,125):

    print("\n\t indx=",indx)

    try:
        originalImage=str(indx)+"_original.png"
        auraImageName=str(indx)+"_cam_map.png"

        tableFromAura(indx,originalImage,auraImageName)
        #input("*****")
        #input("check")

        # if indx>10:
        #     break

        #input("check")

    except Exception as e:
        print(indx)
