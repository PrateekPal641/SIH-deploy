from deepface import DeepFace
import cv2
import numpy as np
import os

path = 'C:\Face_data'
n = len(os.listdir(path))
array = np.zeros((n , n))
i, j = 0, 0
li = []
for file in os.listdir(path):
    current_img = file
    for image in os.listdir(path):
        recognition = DeepFace.verify(img1_path=os.path.join(path, file), img2_path=os.path.join(path, image))
        distance = recognition['distance']
        if distance<.3:
            li.append((i,j))
        array[i, j] = distance
        j += 1
    i += 1
    j=0
j=0
li = [(i,j) for (i,j) in li if i!=j]
li = [(j,i) for (i,j) in li if j>i]
li = dict(li)
print('students at these image index should not be kept in same center',li)

