from setuptools import setup
import glob
import os

package_name = 'my_robot_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # ✅ urdf 디렉토리 추가
        ('share/' + package_name + '/urdf', glob.glob('urdf/*.xacro')),
        # ✅ launch 디렉토리 추가 (필요시)
        ('share/' + package_name + '/launch', glob.glob('launch/*.py')),
        # ✅ models 예시 (필요시)
        # ('share/' + package_name + '/models/lidar_tank', [
        #     'models/lidar_tank/model.config',
        #     'models/lidar_tank/model.sdf',
        # ]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='atoz',
    maintainer_email='atoz@example.com',
    description='PointCloud to Scan Node',
    license='MIT',
    entry_points={
        'console_scripts': [
            'pointcloud_to_scan = my_robot_sim.pointcloud_to_scan:main',
        ],
    },
)

