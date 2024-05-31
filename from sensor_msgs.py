from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import Image
import rclpy

class fusion:
    def __init__(self):
        self.node = rclpy.create_node('fusion')
        self.image_sub = self.node.create_subscription(PointCloud2, '/sensor/lidar0', self.lidar_callback, 2)
        self.image_sub = self.node.create_subscription(Image, '/flir_camera/image_raw', self.camera_callback, 2)
         ## self.transform = f
         # self.transform_inverse = f
          #self.threshold = 4
        self.PtC = None
        self.frame = None
    
    def lidar_callback(self, ptCloud):
        self.PtC = ptCloud
    
    def camera_callback(self, cam_frame):
        self.frame = cam_frame

    def process(self):
        if self.PtC is not None and self.frame is not None:
            if abs(self.frame.header.timestamp - self.PtC.header.timestamp)<0.01:
                save

                








if __name__ == '__main__':
    read_parameters()
    rclpy.init()