# Launch file for starting the ezrassor model in rviz
# Written by Robert Forristall

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from ament_index_python.packages import get_package_share_directory
import xacro

# Function for defining a ros launch command through python
def generate_launch_description():

    # Get the path of this package
    pkg_self = get_package_share_directory('ezrassor_robot_description')

    # Load the urdf file of the model
    model_description = xacro.process_file(
            os.path.join(pkg_self, 'urdf', 'ezrassor_rviz.xacro')
        ).toxml()

    # Get the filepath for rviz configuration
    rviz_config = os.path.join(pkg_self, 'config/ezrassor_rviz_config.rviz')

    # Get filepath for ros2_controllers config
    controllers = os.path.join(pkg_self, 'config/rviz_controllers.yaml')

    # Load the robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': model_description}]
    )

    # Load the controller_manager node
    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[{'robot_description': model_description}, controllers],
        output='screen'
    )

    # Spawn the joint state broadcaster
    joint_state_broad = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', "--controller-manager", "/controller_manager"],
        output='screen'
    )

    # Spawn all joint controllers
    diff_drive = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['diff_drive_controller', "-c", "/controller_manager"],
        output='screen'
    )

    arm_back = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['arm_back_velocity_controller', "-c", "/controller_manager"],
        output='screen'
    )

    arm_front = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['arm_front_velocity_controller', "-c", "/controller_manager"],
        output='screen'
    )

    drum_back = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['drum_back_velocity_controller', "-c", "/controller_manager"],
        output='screen'
    )

    drum_front = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['drum_front_velocity_controller', "-c", "/controller_manager"],
        output='screen'
    )

    # Spawn all drivers

    # Load rviz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=["-d", rviz_config]
    )

    delay_rviz_after_joint_state_broad = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broad,
            on_exit=[rviz],
        )
    )

    return LaunchDescription([
        robot_state_publisher,
        controller_manager,
        joint_state_broad,
        diff_drive,
        arm_back,
        arm_front,
        drum_back,
        drum_front,
        delay_rviz_after_joint_state_broad
    ])


