#import PySpin
import matplotlib.pyplot as plt
#import keyboard
import numpy as np

import cv2

for i in range(10):  # Try indices from 0 to 9
    cap = cv2.VideoCapture(i)
    if not cap.isOpened():
        break
    cap.release()
    print(f"Camera index {i} is available.")




#nodemap_tldevice = cam.GetTLDeviceNodeMap()

        # Initialize camera
#cam.Init()

        # Retrieve GenICam nodemap
#nodemap = cam.GetNodeMap()

        # Acquire images
#result &= acquire_and_display_images(cam, nodemap, nodemap_tldevice)

        # Deinitialize camera
#cam.DeInit()