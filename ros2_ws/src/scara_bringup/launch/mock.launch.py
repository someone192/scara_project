from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, PathSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "gui",
                default_value="true",
                description="Start RViz automatically"
            ),
            Node(
                package="controller_manager",
                executable="ros2_control_node",
                parameters=[
                    PathSubstitution(FindPackageShare("scara_bringup"))
                    / "config" 
                    / "scara_controllers.yaml" #review whether / inside the brackets or not
                ],
                output="both",
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                parameters=[
                    {
                        "robot_description":Command(
                            [
                                "xacro",
                                " ",
                                PathSubstitution(FindPackageShare("scara_description"))
                                / "urdf" 
                                / "scara_exosceleton.urdf.xacro",  #review whether / inside the brackets or not
                            ]
                        )
                    }
                ],
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="log",
                arguments=[
                    "-d",
                    PathSubstitution(FindPackageShare("scara_description"))
                    / "rviz"
                    / "scara_mock.rviz",
                ],
                condition=IfCondition(LaunchConfiguration("gui"))
            ),
            Node(
                package="controller_manager",
                executable="spawner",
                name="controller_spawner",
                arguments=[
                    "joint_state_broadcaster",
                    "joint_trajectory_controller",
                    "--param-file",
                    PathSubstitution(FindPackageShare("scara_bringup"))
                    / "config"
                    / "scara_controllers.yaml",
                ],
            ),

        ]
    )
