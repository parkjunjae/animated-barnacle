import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, LaserScan
import sensor_msgs_py.point_cloud2 as pc2
import math
from std_msgs.msg import Header

class PC2ToScan(Node):
    def __init__(self):
        super().__init__('pc2_to_scan')
        self.sub = self.create_subscription(PointCloud2, '/velodyne_points/out', self.callback, 10)
        self.pub = self.create_publisher(LaserScan, '/scan', 10)

    def callback(self, msg):
        scan = LaserScan()
        scan.header = Header()
        scan.header.stamp = self.get_clock().now().to_msg()
        scan.header.frame_id = "base_link"
        scan.angle_min = -math.pi
        scan.angle_max = math.pi
        scan.angle_increment = math.radians(0.5)
        scan.range_min = 0.1
        scan.range_max = 30.0
        scan.ranges = [float('inf')] * int((scan.angle_max - scan.angle_min) / scan.angle_increment)

        for p in pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True):
            x, y, z = p
            if abs(z) > 0.2:  
                continue
            angle = math.atan2(y, x)
            dist = math.hypot(x, y)
            idx = int((angle - scan.angle_min) / scan.angle_increment)
            if 0 <= idx < len(scan.ranges) and dist < scan.ranges[idx]:
                scan.ranges[idx] = dist

        scan.ranges = [r if r != float('inf') else 0.0 for r in scan.ranges]
        self.pub.publish(scan)

def main():
    rclpy.init()
    node = PC2ToScan()
    rclpy.spin(node)
    rclpy.shutdown()

