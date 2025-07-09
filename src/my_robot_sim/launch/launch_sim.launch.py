from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction, LogInfo  # ✅ LogInfo 직접 추가
from launch.substitutions import Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import xacro

def generate_launch_description():
    pkg_path = get_package_share_directory('my_robot_sim')
    xacro_path = os.path.join(pkg_path, 'urdf', 'lidar_tank.xacro')
    robot_description_config = xacro.process_file(xacro_path).toxml()

    print_node = LogInfo(msg="🔥 static_map_to_base 시작됨")  # ✅ 이렇게만

    return LaunchDescription([
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),
        Node(
    	    package='my_robot_sim',
            executable='pointcloud_to_map',
            name='pointcloud_to_map',
            output='screen'
	),
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen'
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description_config
            }]
        ),
        TimerAction(
            period=5.0,
            actions=[
                ExecuteProcess(
                    cmd=[
                        'ros2', 'run', 'gazebo_ros', 'spawn_entity.py',
                        '-entity', 'lidar_tank',
                        '-topic', 'robot_description',
                        '-x', '0', '-y', '0', '-z', '0.1'
                    ],
                    output='screen'
                )
            ]
        )
    ])

