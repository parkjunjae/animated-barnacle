from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import xacro  # ROS 2에서 pip install xacro

def generate_launch_description():
    # 디렉토리 경로
    pkg_my_robot_sim = get_package_share_directory('my_robot_sim')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # Xacro 파일 경로
    xacro_file = os.path.join(pkg_my_robot_sim, 'urdf', 'lidar_tank.xacro')
    robot_desc = xacro.process_file(xacro_file).toxml()

    # World 파일 경로
    world_path = os.path.join(get_package_share_directory('my_robot_gazebo'), 'worlds', 'my_world.world')

    return LaunchDescription([
        # Gazebo 실행
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
            ),
            launch_arguments={'world': world_path, 'gui': 'true'}.items()
        ),

        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True   
            }]
        ),

        # Spawn Entity
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-entity', 'lidar_tank',
                '-file', xacro_file,
                '-x', '0.0',
                '-y', '0.0',
                '-z', '0.0'
            ],
            output='screen'
        ),
        

        # (선택) Nav2 bringup 포함 시
        #IncludeLaunchDescription(
        #    PythonLaunchDescriptionSource(
        #        os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py')
        #    ),
        #    launch_arguments={
        #        'use_sim_time': 'true',
        #        'autostart': 'true'
        #    }.items()
        #),
    ])

