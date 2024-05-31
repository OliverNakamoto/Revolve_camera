import numpy as np

dist_coeffs = np.array([[1,2,23,4,5]])

print(dist_coeffs[:,-1])

#print(np.stack((dist_coeffs[:, :2], dist_coeffs[:,-1]), axis=-1))# + dist_coeffs[:, -1])

result = [np.concatenate((row[:2], [row[-1]])) for row in dist_coeffs][0]
print(result)


camera_matrix = np.array([[463.13148894, 0, 336.32127523], [0, 461.01237831, 251.5707013], [0, 0, 1]])
cx = camera_matrix[0][2]
cy = camera_matrix[1][2]

print(cx, cy)





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






def project_points(points_3d, intrinsic_matrix, rotation_matrix, translation_vector, dist_coeffs, cx, cy):
    # Transform points to camera coordinate system
    points_3d_cam = np.dot(rotation_matrix, points_3d.T).T + translation_vector

    # Apply perspective projection
    points_2d_homo = np.dot(intrinsic_matrix, points_3d_cam.T)
    points_2d_homogeneous = points_2d_homo.T
    
    r_squared = np.sum((points_2d_homogeneous[:, :2] - np.array([cx, cy])) ** 2, axis=1)
    distortion = 1 + np.sum(dist_coeffs * np.stack([r_squared, r_squared ** 2, r_squared ** 3], axis=0), axis=0)

    points_2d_homogeneous[:, :2] *= distortion[:, np.newaxis]
    points_2d = points_2d_homogeneous[:, :2] / points_2d_homogeneous[:, 2:]

    return points_2d





dist_coeffs = [np.concatenate((row[:2], [row[-1]])) for row in dist_coeffs][0]



r_squared = 0.3
print('distsss', dist_coeffs.reshape(1,3) * [1,0,0])
distortion = 1 + np.sum(dist_coeffs.reshape(1,3) * np.array([r_squared, r_squared ** 2, r_squared ** 3]), axis=1)

print(distortion)