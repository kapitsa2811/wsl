#-*- coding: utf-8 -*-

from keras.applications.resnet50 import preprocess_input
import numpy as np
import cv2

from src.model_builder import CamModelBuilder
from src.utils import plot_img, list_files


if __name__ == "__main__":

    expNo = str(8)
    indx=40
    #comment="newTabData_40.h5"
    modelName="newTabData_"+str(indx)+".h5"
    basePath = "///home/kapitsa/pyCharm/segmentation/weaklySupervisedSegmentation/publicationData//"
    modelPath=basePath+"//"+expNo+"//model//"+modelName
    results=basePath+"//"+expNo+"//results//"
    testData=basePath+"//"+expNo+"//test//"

    # results=basePath+"//"+expNo+"//results1//"
    # testData=basePath+"//"+expNo+"//delMe//nonFocus//"

    detector = CamModelBuilder().get_cam_model(indx)
    #t="/home/kapitsa/PycharmProjects/MyOCRService/objectDetection/Weakly-Supervised-Text-Detection/backUP/paperModel"
    #detector.load_weights(".//backUP//weights.19-0.01.h5", by_name=True)

    detector.load_weights(modelPath, by_name=True)

    #hardPath="/home/kapitsa/PycharmProjects/MyOCRService/objectDetection/Weakly-Supervised-Text-Detection//"#backUP/paperModel//"
    #detector.load_weights(hardPath+"//weights.19-0.01.h5", by_name=True)
    detector.summary()
    imgs = list_files(testData)
     
    for i, img_path in enumerate(imgs):
        original_img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
         
        img = cv2.resize(255-original_img, (224, 224))
        #img = cv2.resize(original_img, (224, 224))

        img = np.expand_dims(img, 0).astype(np.float64)
     
        cam_map = detector.predict(preprocess_input(img))
        cam_map = cam_map[0, :, :, 1]

        cam_map1=cv2.cvtColor(cam_map, cv2.COLOR_GRAY2BGR)
        cam_map1 = cv2.resize(cam_map1, (original_img.shape[1], original_img.shape[0]))

        cam_map = cv2.resize(cam_map, (original_img.shape[1], original_img.shape[0]))
        cam_map1=cam_map1+original_img

        #plot_img(original_img, cam_map, show=False, save_filename="{}.png".format(i+1))

        #plot_img(i, original_img, cam_map, cam_map1, show=False, save_filename=".//predict//{}_0.png".format(i + 1))
        plot_img(i,indx,results, original_img, cam_map, cam_map1, show=False, save_filename=".//predictVGG//{}_0.png".format(i + 1))
    
