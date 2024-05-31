Various scripts and models/data for camera implementation


In the repo you will find:

Model_Results (containing the model weights and validation data from performance for an early model)

trainn-b16-ep38-im1440-altLbl (best model trained and its validation results)

ext_calibrate (extrinsic calibration files, based off of manually inputing correspondence points, and then it also has a lidar projection script which produces ok results but somewhat off.

data_labeling (all the changes made to the FSOCO labels, just made different categories of small cones based off of their distance to the car).

intrinsics (folder with intrinsic calibration file and example data, in addition to an example of the camera intrinsic being used to correct an image)
