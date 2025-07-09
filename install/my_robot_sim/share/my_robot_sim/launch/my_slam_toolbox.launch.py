from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=['/home/atoz/ros2_ws/src/my_robot_sim/config/slam_toolbox_params.yaml']
        )


    ])