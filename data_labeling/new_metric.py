import os
from PIL import Image
import PIL
import sys
import matplotlib.pyplot as plt
import numpy as np

img_pth = '/home/oliverz/Documents/Revolve/fsoco/FSOCO_data/dataset/labels/val'

areas = []

medium_range = 0.000509
far_range = 0.00007524

for file in os.listdir(img_pth):
    paths = os.path.join('val', file)
    f = open(paths)
    #print(f)
    for line in f:
        lists = line.split()
        width = float(lists[3])
        height = float(lists[4])
        area = width*height
        areas.append(area)
        
    
#print(areas)

#plt.scatter(range(len(areas)), areas, marker='o', s=1)
#plt.plot(areas, marker='o', linestyle='-')
#plt.xlabel('x-axis')
#plt.ylabel('y-axis')
#plt.title('plotting areas of cones')
#plt.yscale('log')
#plt.show()

bin_edges = np.arange(0, 0.0007, 0.000005)

hist, bin_edges = np.histogram(areas, bins = bin_edges)

plt.bar(bin_edges[:-1], hist, width=0.00001, align='edge')
total = areas
total = len([value for value in areas if 0 <= value <= medium_range])
plt.title(f'total cones in range is: {total}')

plt.show()

