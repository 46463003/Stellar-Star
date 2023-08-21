import cv2
import os
import glob


size = {"x": "", "y": ""}
images = [cv2.imread(file) for file in glob.glob("Sample_Images/*.tiff")]
#print(images[0].shape)
for i in range(len(images)):
    print(i)
    border = images[i].shape
    print(border)
