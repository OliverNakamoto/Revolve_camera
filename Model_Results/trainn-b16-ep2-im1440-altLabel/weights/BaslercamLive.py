from pypylon import pylon
import tkinter as tk
import numpy as np
from ultralytics import YOLO
from PIL import Image, ImageTk
import cv2
import math

model = YOLO("best.pt")

# object classes
classNames = ["yellow", "blule", "orange", "large", "unknown", 
              "M_yellow", "M_blue", "M_orange", "M_large", "M_unknown",
              "F_yellow", "F_blue", "F_orange", "F_large", "F_unknown"
              ]

def update_image():
    global img_reference  # Declare img_reference as a global variable
    if camera.IsGrabbing():
        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grab_result.GrabSucceeded():
            img_array = grab_result.Array
            img_array_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)  # Convert to BGR format
            img = Image.fromarray(img_array_bgr)
            img_np = np.asarray(img)  # Convert image to numpy array
            img_reference = ImageTk.PhotoImage(img)

            label.config(image=img_reference)

            results = model(img_np, stream=True)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]

                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values
                    print(x1, y1, x2, y2)
                    confidence = math.ceil((box.conf[0]*100))/100
                    print("Confidence --->",confidence)

                    # class name
                    cls = int(box.cls[0])
                    print("Class name -->", classNames[cls])

            grab_result.Release()

    # Schedule the next update after 100 milliseconds
    root.after(100, update_image)

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

# Set camera parameters and start grabbing
camera.Width = camera.Width.Max
camera.Height = camera.Height.Max
camera.PixelFormat = "BGR8"  # Set pixel format to BGR8 for color
camera.StartGrabbing(pylon.GrabStrategy_LatestImages)

# Create a tkinter window
root = tk.Tk()
root.title("Live Feed")

# Create a label to display the image
label = tk.Label(root)
label.pack()

# Initialize img_reference
img_reference = None

# Schedule the first update
root.after(100, update_image)

# Start the tkinter main loop
root.mainloop()

# Cleanup when the tkinter window is closed
camera.StopGrabbing()
camera.Close()
