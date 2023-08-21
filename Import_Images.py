import cv2
import os
import glob

def import_images():
    images = [cv2.imread(file) for file in glob.glob("Sample_Images/*.tiff")]
    return images

def get_image_size():
    size = {} 
    images = import_images()
    for i in range(len(images)):
        border = images[i].shape
        size[i] = []
        size[i].append(border[0])
        size[i].append(border[1]) 
    return size
