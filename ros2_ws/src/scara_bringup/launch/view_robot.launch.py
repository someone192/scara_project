import os

from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg = FindPackageShare('scara_description')
    urdf_file = PathJoinSubstitution([pkg, 'urdf', 'scara_exosceleton.urdf'])
    rviz_config = PathJoinSubstitution([pkg, 'rviz', 'scara.rviz'])

    robot_description = ParameterValue(
        Command([FindExecutable(name='xacro'), ' ',urdf_file]),
        value_type=str,
    )

    return LaunchDescription([
        Node(package='robot_state_publisher',
             executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description}],
             output='screen'),
        Node(package='joint_state_publisher_gui',
             executable='joint_state_publisher_gui'),
        Node(package='rviz2',
             executable='rviz2',
             arguments=['-d', rviz_config],
             output='screen')
    ])