from pathlib import Path
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    share = Path(get_package_share_directory('robotic_arm_description'))
    # Expand the small per-joint files into the complete description for ROS.
    description = xacro.process_file(str(share / 'urdf/robot.urdf.xacro')).toxml()
    demo = LaunchConfiguration('demo')
    return LaunchDescription([
        DeclareLaunchArgument('demo', default_value='false', description='Publish preview poses instead of sliders; no hardware commands.'),
        Node(package='robot_state_publisher', executable='robot_state_publisher', parameters=[{'robot_description': description}]),
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui', condition=UnlessCondition(demo), parameters=[{'robot_description': description, 'zeros': {'j2': 0.7853981634, 'j3': -1.4835298642, 'j4': 0.6981317008, 'gripper_opening': 0.015}}]),
        Node(package='robotic_arm_description', executable='pose_preview.py', condition=IfCondition(demo)),
        Node(package='rviz2', executable='rviz2', arguments=['-d', str(share / 'rviz/arm.rviz')]),
    ])
