import cv2
import os
import glob

images = [cv2.imread(file) for file in glob.glob("Sample_Images/*.tiff")]
