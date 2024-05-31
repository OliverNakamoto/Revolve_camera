# #import PySpin
# import sys
# #import keyboard
# import cv2
# import math
# from ultralytics import YOLO

# from simple_pyspin import Camera

# # dead_simple.py

# from simple_pyspin import Camera

# with Camera() as cam: # Acquire and initialize Camera
#     cam.start() # Start recording
#     imgs = [cam.get_array() for n in range(10)] # Get 10 frames
#     cam.stop() # Stop recording

# print(imgs[0].shape, imgs[0].dtype) # Each image is a numpy array!

# global continue_recording
# continue_recording = True

# def handle_close(evt):
#     global continue_recording
#     continue_recording = False

# def acquire_and_display_images(cam, nodemap, nodemap_tldevice):
#     global continue_recording

#     # YOLO model initialization
#     model = YOLO("best.pt")
#     classNames = ["yellow", "blue", "orange", "large", "unknown",
#                   "M_yellow", "M_blue", "M_orange", "M_large", "M_unknown",
#                   "F_yellow", "F_blue", "F_orange", "F_large", "F_unknown"]

#     # FLIR camera initialization and configuration
#     # Sett in kamera oppsett her




#     cam.BeginAcquisition()
    


#     while continue_recording:
#         try:
            
#             image_result = cam.GetNextImage(1000)
#             if image_result.IsIncomplete():
#                 print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
#             else:
#                 # Process image with YOLO
#                 image_data = image_result.GetNDArray()
#                 img = cv2.cvtColor(image_data, cv2.COLOR_GRAY2BGR)  # Convert to BGR format for OpenCV

#                 results = model(img, stream=True)
#                 for r in results:
#                     boxes = r.boxes
#                     for box in boxes:
#                         # bounding box
#                         x1, y1, x2, y2 = box.xyxy[0]
#                         x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values
#                         # put box in cam
#                         cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
#                         # confidence
#                         confidence = math.ceil((box.conf[0]*100))/100
#                         print("Confidence --->",confidence)
#                         # class name
#                         cls = int(box.cls[0])
#                         print("Class name -->", classNames[cls])
#                         # object details
#                         org = [x1, y1]
#                         font = cv2.FONT_HERSHEY_SIMPLEX
#                         fontScale = 1
#                         color = (255, 0, 0)
#                         thickness = 2
#                         cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

#                 cv2.imshow('FLIR Camera with YOLO', img)
#                 if cv2.waitKey(1) == ord('q'):
#                     continue_recording = False

#                 image_result.Release()
#         except PySpin.SpinnakerException as ex:
#             print('Error: %s' % ex)
#             return False

#     cam.EndAcquisition()
#     return True

# def run_single_camera(cam):
#     try:
#         result = True
#         nodemap_tldevice = cam.GetTLDeviceNodeMap()
#         cam.Init()
#         nodemap = cam.GetNodeMap()
#         result &= acquire_and_display_images(cam, nodemap, nodemap_tldevice)
#         cam.DeInit()
#     except PySpin.SpinnakerException as ex:
#         print('Error: %s' % ex)
#         result = False
#     return result

# def main():
#     result = True
#     system = PySpin.System.GetInstance()
#     version = system.GetLibraryVersion()
#     print('Library version: %d.%d.%d.%d' % (version.major, version.minor, version.type, version.build))
#     cam_list = system.GetCameras()
#     num_cameras = cam_list.GetSize()
#     print('Number of cameras detected: %d' % num_cameras)

#     if num_cameras == 0:
#         cam_list.Clear()
#         system.ReleaseInstance()
#         print('Not enough cameras!')
#         input('Done! Press Enter to exit...')
#         return False

#     for i, cam in enumerate(cam_list):
#         print('Running example for camera %d...' % i)
#         result &= run_single_camera(cam)
#         print('Camera %d example complete... \n' % i)

#     del cam
#     cam_list.Clear()
#     system.ReleaseInstance()
#     input('Done! Press Enter to exit...')
#     return result

# if __name__ == '__main__':
#     if main():
#         sys.exit(0)
#     else:
#         sys.exit(1)

from pypylon import pylon
from PIL import Image

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

# demonstrate some feature access
new_width = camera.Width.Value - camera.Width.Inc
if new_width >= camera.Width.Min:
    camera.Width.Value = new_width

numberOfImagesToGrab = 100
camera.StartGrabbingMax(numberOfImagesToGrab)

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data.
        print("SizeX: ", grabResult.Width)
        print("SizeY: ", grabResult.Height)
        img = grabResult.Array
        print("Gray value of first pixel: ", img[0, 0]) 
        camera.PixelFormat.SetValue(PixelFormat_BGR8)
        image = Image.fromarray(img)
        image.show() 

    grabResult.Release()
camera.Close()


