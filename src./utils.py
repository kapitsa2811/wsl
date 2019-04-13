#-*- coding: utf-8 -*-
import os
import cv2
import glob
import random
import re
import numpy as np
random.seed(111)

class FileSorter:
    def __init__(self):
        pass
    
    def sort(self, list_of_strs):
        list_of_strs.sort(key=self._alphanum_key)

    def _tryint(self, s):
        try:
            return int(s)
        except:
            return s
    
    def _alphanum_key(self, s):
        """ Turn a string into a list of string and number chunks.
            "z23a" -> ["z", 23, "a"]
        """
        return [ self._tryint(c) for c in re.split('([0-9]+)', s) ]


def files_to_images(files):
    images = []
    for fname in files:
        img = cv2.imread(fname)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        images.append(img)
    return images


def list_files(directory, pattern="*.*", n_files_to_sample=None, recursive_option=True, random_order=True):
    """list files in a directory matched in defined pattern.

    Parameters
    ----------
    directory : str
        filename of json file

    pattern : str
        regular expression for file matching
    
    n_files_to_sample : int or None
        number of files to sample randomly and return.
        If this parameter is None, function returns every files.
    
    recursive_option : boolean
        option for searching subdirectories. If this option is True, 
        function searches all subdirectories recursively.
        
    Returns
    ----------
    conf : dict
        dictionary containing contents of json file

    Examples
    --------
    """

    if recursive_option == True:
        dirs = [path for path, _, _ in os.walk(directory)]
    else:
        dirs = [directory]
    
    files = []
    for dir_ in dirs:
        for p in glob.glob(os.path.join(dir_, pattern)):
            files.append(p)
    
    FileSorter().sort(files)
        
    if n_files_to_sample is not None:
        if random_order:
            files = random.sample(files, n_files_to_sample)
        else:
            files = files[:n_files_to_sample]
    return files


def plot_img(i,indx,results,image, cam_map,cam_map1, show=True, save_filename=None):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(nrows=1, ncols=3)

    '''
    plt.subplot(3, 1, 1)
    plt.imshow(image)
    plt.subplot(3, 1, 2)
    plt.imshow(cam_map)
    plt.subplot(3, 1, 3)
    plt.imshow(image, alpha=0.7)
    plt.imshow(cam_map, cmap='jet', alpha=0.3)
    '''

    threshold=3
    unableThresholding=1
    if unableThresholding == 1:
        pixelDown = np.where(cam_map < threshold)
        cam_map[pixelDown] = 0

        pixelUP = np.where(cam_map >= threshold)

        countUP=len(pixelUP)
        #sumUP=np.average(cam_map[pixelUP])

        #aboveSUM=np.where(cam_map >=sumUP)

        cam_map[pixelUP] = 255

        #cam_map[aboveSUM] = 255


    # cv2.imwrite(".//predict//{}_cam_map000.png".format(i + 1),cam_map)
    # # cv2.imwrite(".//predict//{}_cam_map1.png".format(i + 1),255-cam_map1)
    # cv2.imwrite(".//predict//{}_original.png".format(i + 1),255-image)

    #cv2.imwrite(results+"//"+str(i)+"_cam_map1_"+str(indx)+".png".format(i + 1),cam_map)
    # cv2.imwrite(results+"//"+str(i)+"_cam_ma2_"+".png".format(i + 1),255-cam_map1)
    # cv2.imwrite(results+"//"+str(i)+"_original"+".png".format(i + 1),255-image)

    cv2.imwrite(results+"//"+str(i)+"_cam_map.png".format(i + 1),cam_map)
    #cv2.imwrite(results+"//"+str(i)+"_cam_ma2_"+".png".format(i + 1),255-cam_map1)
    cv2.imwrite(results+"//"+str(i)+"_original"+".png".format(i + 1),255-image)



    # if show:
    #     plt.show()
    # if save_filename:
    #     plt.savefig(save_filename, bbox_inches='tight')
    #     print("{} is saved".format(save_filename))


