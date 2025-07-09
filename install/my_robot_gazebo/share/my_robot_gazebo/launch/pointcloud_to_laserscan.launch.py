from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            output='screen',
            remappings=[
                ('cloud_in', '/velodyne_plugin/out'),
                ('scan', '/scan')
            ],
            parameters=[{
                'target_frame': 'base_link',          # 입력 프레임(보통 빈 문자열이면 자동)
                'transform_tolerance': 0.01,
                'min_height': -0.302,          # z 범위 지정 예시
                'max_height': 0.202,
                'angle_min': -3.14,
                'angle_max': 3.14,
                'angle_increment': 0.01,
                'scan_time': 0.2,
                'range_min': 0.3,
                'range_max': 30.0,
                'use_inf': True,
                'inf_epsilon': 1.0,
                'use_sim_time': True
            }]
        )
    ])

