from pdf2image import convert_from_path
import os
import cv2

#pdfPath="/home/kapitsa/PycharmProjects/MyOCRService/images//"
pdfPath="/home/kapitsa/pyCharm/segmentation/weaklySupervisedSegmentation/publicationData/8/tableRelatedAll/chartPDF//"
extension=".pdf"
#file="Engineering drawing third edition"
#file="HE_Design_Data_Digest"


fileFolderPath=pdfPath

for no, nm in enumerate(os.listdir(fileFolderPath)):

    file=nm

    print(file)

    #continue
    fileName=file#+extension

    pages = convert_from_path(pdfPath+fileName,10)

    outFolder="/home/kapitsa/pyCharm/segmentation/weaklySupervisedSegmentation/publicationData/8/tableRelatedAll/pdf2img//"

    outDir=outFolder+file

    try:
        os.mkdir(outDir)
    except Exception as e:
        pass
    #Saving pages in jpeg format

    #os.system("convert -density 300\\"+pdfPath+fileName+"\\ -quality 100"+pdfPath+file+"//"+str(indx)+'out.jpg')


    for indx,page in enumerate(pages):


        if indx%5==0:
            print "\n\t indx=",indx
        elif indx>14:
            break

        infile=pdfPath + fileName
        outfile=outFolder + "//" +file +"//"+str(indx)+ 'out.jpg'

        print("\n\t in",infile)
        print("\n\t out=",outfile)
        # os.system("convert -density 100\\" + pdfPath + fileName + "\\ -quality 100" + pdfPath + file + "//" + str(indx) + 'out.jpg')
        #command = 'convert {} -blur 2x1 -sharpen 0x3 -sharpen 0x3 -quality 1000 -morphology erode diamond -auto-orient -enhance -contrast -contrast-stretch 0 -gamma .45455 -unsharp 0.25x0.25+8+0.065 -fuzz 2% {}'.format(
            #infile, outfile)

        #command ="convert " + infile + "\\ -quality 300" + outfile
        command ="convert -density 100 \"" + infile + "\" -quality 300 " + outfile
        os.system(command)



        #     page.save(pdfPath+file+"//"+str(indx)+'out.jpg', 'JPEG')



    #imgPath=pdfPath+"//"+outFolder+"//"

    imgPath=outFolder + "//" +file +"//"
    allImages=os.listdir(imgPath)

    print("\n\t no of images=",len(allImages))
    for indx,page in enumerate(allImages):

        if indx%5==0:
            print "\n\t indx=",indx

        infile=imgPath + page
        outfile=imgPath  + "//" + str(indx) + page
        print("\n\t in",infile,"\t is file=",os.path.isfile(infile))
        print("\n\t out=",outfile)

        tempImg=cv2.imread(infile)
        print("\n\t size=",tempImg.size)
        tempImg=255-tempImg
        cv2.imwrite(outfile,tempImg)
