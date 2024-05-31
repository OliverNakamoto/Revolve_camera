import numpy as np
import cv2

path_img = '/home/oliverz/Documents/Revolve/Data/Fuse_data/Matlab/Images/0013.png'
path_ptc =  '/home/oliverz/Documents/Revolve/Data/Fuse_data/Matlab/PointClouds/0013.pcd'

import open3d as o3d

# Load a point cloud from a PLY file
pcd = o3d.io.read_point_cloud(path_ptc)
image = cv2.imread(path_img)

pcd = o3d.io.read_point_cloud(path_ptc)
image = cv2.imread(path_img)

points3DD = np.asarray(pcd.points)


k=0
for i in range(len(points3DD)):
    point = points3DD[i-k]

    if np.sum(point) == 0:
        points3DD = np.delete(points3DD, i-k, axis=0)
        k+=1
'''
Calibrate the LiDAR and image points using OpenCV PnP RANSAC
Requires minimum 5 point correspondences

Inputs:
    points2D - [numpy array] - (N, 2) array of image points
    points3D - [numpy array] - (N, 3) array of 3D points

Outputs:
    Extrinsics saved in PKG_PATH/CALIB_PATH/extrinsics.npz
'''
# 1.6625, -0.49342, 0.17776 (top right)
# 1.7672 0.28416 0.18236 (top left)
# 1.8365 0.2841 -0.2336
# 1.7156 -0.48623 -0.26688 (bottom right)
# 1.7295 -0.095832 0.17759 (top middle)

# 255,189 (top left)
# 257 358 bottom left)
# 515, 371 (bottom right)
# 521, 193 (top right)
# 388, 188 (top middle)

# 1.5460032224655151 -0.5110288262367249 0.4096434712409973  #top right

# 1.6355332136154175 0.26288822293281555 0.41618677973747253 #top left

# 1.7309733629226685 0.28883734345436096 0.01857459731400013 #bottom left

# 1.5499382019042969 -0.5120304822921753 -0.010385407134890556 #bottom right

#1.5890835523605347 -0.1273287981748581 0.40174639225006104  #middle top

#2.1821534633636475 -0.24240534007549286 -0.5536116361618042 #knee

#2.589376449584961 1.1658991575241089 -0.23723167181015015 #fridge


# 521 191 #top right

# 253 187 #top left

# 257 358 #bottom left

# 517 374 #bottom right

#388 185 # top middle

#413 414 #knee

#84 317 #fridge



# points3D = np.array([[1.6625, -0.49342, 0.17776],[1.7672,0.28416,0.18236],[1.8365, 0.2841, -0.2336], [1.7156, -0.48623, -0.26688],[1.7295, -0.095832, 0.17759]])
# points2D = np.array([[255.0,189.0],[257.0,358.0],[515.0,371.0],[521.0,371.0],[388.0,188.0]])
# camera_matrix = np.array([[328.66410109, 0, 378.9984531],[0, 398.55625977, 257.00558892],[0, 0, 1]])
# dist_coeffs = np.array([[-0.21268231, 0.18445857, -0.00401462, -0.00214662, -0.22491632]])

points3D = np.array([[1.54600, -0.51103, 0.40964],[1.63553, 0.26289, 0.41619 ],[1.73097, 0.28884, 0.01857], [1.58908, -0.12733, 0.40175], [2.18215, -0.242405, -0.55361]]) #[1.54994, -0.51203, -0.01039]])#, [2.58937645, 1.1658992, -0.2372317] ]) [1.54994, -0.51203, -0.01039]
points2D = np.array([[521.0, 191.0],[253.0, 187.0],[257.0, 358.0],[388.0, 185.0], [413.0, 424.0]]) #, [517.0, 374.0]])#, [84.0, 317.0]])
camera_matrix3 = np.array([[328.66410109, 0, 378.9984531],[0, 398.55625977, 257.00558892],[0, 0, 1]])
camera_matrix2 = np.array([[328.66410109, 0, 0.9984531],[0, 398.55625977, 0.00558892],[0, 0, 1]])
camera_matrix = np.array([[463.13148894, 0, 336.32127523], [0, 461.01237831, 251.5707013], [0, 0, 1]])
cx = camera_matrix[0][2]
cy = camera_matrix[1][2]
dist_coeffs2 = np.array([[-0.21268231, 0.18445857, -0.00401462, -0.00214662, -0.22491632]])
dist_coeffs = np.array([[-0.284588649, 0.236290744, -0.0000924157224, -0.000555732358, -0.189868352]]) #-0.0000924157224, -0.000555732358]])
dist_coeffs3 = np.array([[0.0,0.0,0.0,0.0,0.0]])



print(points2D.dtype)
print(points3D.dtype)
print(points2D.shape)
print(points3D.shape)

success, rotation_vector, translation_vector, inliers = cv2.solvePnPRansac(points3D, 
        points2D, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

print(rotation_vector)
print(translation_vector)
print(inliers)


if success:
    # Transform point cloud to camera coordinate system
    #print(points3DD)
    points3D_cam = cv2.Rodrigues(rotation_vector)[0].dot(points3D.T - translation_vector).T
    #print(points3D_cam)

    # Project LiDAR points onto the image
    #print(points3D_cam)
    # for i in range(len(points3DD)):
    #     points3DD[i][0] = round(points3DD[i][0], 5)
    #     points3DD[i][1] = round(points3DD[i][1], 5)

    for point in points3DD:
        print(point)

    img_points, _ = cv2.projectPoints(points3DD, rotation_vector, translation_vector, camera_matrix, dist_coeffs)
    #print(img_points)
    img_points = np.squeeze(img_points)

    # Convert float values to integers for drawing
    img_points = img_points.astype(int)
    #print(img_points)
    # Draw circles at the projected points on the image
    i = 0
    for point in img_points:
        print(point)
        if 550>point[0]>240 and 2000>point[1]>105:
            i +=1
            print(point)
            cv2.circle(image, (round(point[0], 5), round(point[1], 5)), 1, (255, 0, 0), -1)  # Draw a filled green circle with radius 5
            print(i)
            if i >3420:
                break

    # Display the image with marked points
    cv2.imshow("Image with marked points", image)
    cv2.waitKey(0)  # Wait for a key press to close the window



import numpy as np

def project_points(point_3d, intrinsic_matrix, rotation_matrix, translation_vector, dist_coeffs):
    # Add homogeneous coordinates to 3D points
    #points_3d_homo = np.hstack((points_3d, np.ones((points_3d.shape[0], 1))))
    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
    translation_vector = np.vstack([translation_vector, [1]])
    print('wtfs happenign',  point_3d.shape)
    point_3d = np.vstack([point_3d.reshape(3,1), [1]])
    rotation_matrix = np.vstack([rotation_matrix, [1,1,1]])
    transformation = np.hstack([rotation_matrix, translation_vector])
    point_3d_cam = np.dot(transformation, point_3d) 
    #translation_vector_tiled = np.tile(translation_vector.T, (points_3d.shape[0], 1))


    # Transform points to camera coordinate system
    # print(rotation_matrix.shape, points_3d.shape, translation_vector.shape)
    # points_3d_cam = np.dot(rotation_matrix, points_3d).T + translation_vector
    # print(points_3d_cam.shape)
    point_3d_cam = point_3d_cam[:-1]

    point_2d_homo = np.dot(intrinsic_matrix, point_3d_cam)

    # Apply perspective projection 
    passs = 1
    if (1000>point_2d_homo[0]>-50):
        if (1000>point_2d_homo[1]>-10):
            passs = 0
    if passs:
        return None

    dist_coeffs = [np.concatenate((row[:2], [row[-1]])) for row in dist_coeffs][0]
    
    r_squared = (point_2d_homo[0] - cx)**2+(point_2d_homo[1] - cy)**2
    r_squared = float(r_squared)
    distortion = 1 + np.sum(dist_coeffs.reshape(1,3) * [r_squared, r_squared ** 2, r_squared ** 3], axis=1)

    point_2d_homo[:2] *= distortion
   
    points_2d = point_2d_homo[:2] / point_2d_homo[2:]

    return points_2d.T




# Project 3D points onto the image plane
points_2d = []
for point in points3DD:
    proj = project_points(point, camera_matrix, rotation_vector, translation_vector, dist_coeffs)
    if proj is None:
        pass
    else:
        points_2d.append(proj)

print("\n\n\nProjected 2D points:")
points_2d = combined_array = np.concatenate(points_2d, axis=0)
#print(points_2d)

image2 = cv2.imread(path_img)
img_points = points_2d.astype(int)


i = 0
for point in img_points:
    #print(point)
    print(point)
    if 550>point[0]>240 and 2000>point[1]>105:
        i +=1
        #print(point)
        cv2.circle(image2, (round(point[0], 5), round(point[1], 5)), 1, (255, 0, 0), -1)  # Draw a filled green circle with radius 5
        #print(i)
        if i >3420:
            break

# Display the image with marked points
cv2.imshow("Image with marked points", image2)
cv2.waitKey(0)  # Wait for a key press to close the window





