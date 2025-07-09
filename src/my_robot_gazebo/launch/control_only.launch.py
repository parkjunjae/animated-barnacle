from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[
                {'robot_description': open('/home/atoz/ros2_ws/src/my_robot_sim/urdf/lidar_tank.urdf').read()},  # xacro 파일은 미리 urdf로 변환해서 사용 추천
                '/home/atoz/ros2_ws/src/my_robot_sim/config/robot_controllers.yaml'
            ],
            output='screen',
        )
    ])

