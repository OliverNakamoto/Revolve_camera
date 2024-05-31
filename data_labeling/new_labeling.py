import os
from PIL import Image
import PIL
import sys
import matplotlib.pyplot as plt
import numpy as np

img_pth = '/home/oliverz/Documents/Revolve/fsoco/FSOCO_data/dataset/labels/train'

areas = []

medium_range = 0.000509
far_range = 0.00007524

for file in os.listdir(img_pth):
    paths = os.path.join('train', file)
    f = open(paths)
    new_path = os.path.join('train2', file)
    lists2 = []
    for line in f:
        lists = line.split()
        width = float(lists[3])
        height = float(lists[4])
        area = width*height
        areas.append(area)
        if area < medium_range:
            lists[0] = int(lists[0]) + 5
            print(area, "m")
            if area < far_range:
                lists[0] = int(lists[0]) + 5
                print(area, "l")
        lists2.append(lists)
    
    with open(new_path, 'w') as file:
        for lists in lists2:
            for j in lists:
                file.write(str(j) + " ")
            file.write("\n")
