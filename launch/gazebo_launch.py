# ROS2 Humble python launch file to launch the ezrassor rover
# in the gazebo simulation program
# 
# Written by Robert Forristall

from ast import arguments
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit, OnExecutionComplete
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():

    # Get relevant package directories
    pkg_self = get_package_share_directory('ezrassor_robot_description')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # Generate robot description
    model_description = {'robot_description': 
        xacro.process_file(
            os.path.join(pkg_self, 'urdf', 'ezrassor.xacro')
        ).toxml()}

    # Get the world file
    #world_file = os.path.join(pkg_self, 'world', 'base.world')

    # Get filepath for ros2_controllers config
    # controllers = os.path.join(pkg_self, 'config/default_position_controllers.yaml')
    
    # Include Moveit configuration for paver arm

    # Include the gazebo launch to load the simulation
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        )
    )

    # Launch robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[model_description]
    )

    # Spawn the model using the spawn entity node
    
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'ezrassor',
            '-topic', 'robot_description',
            '-x', '0',
            '-y', '0',
            '-z', '0.5',
            '-Y', '0'
        ],
        output='screen'
    )
    

    """
    # Arguments for the spawn_entity node in the ezrassor_arm_v2 package
    spawn_entity_args = [
        'standard', 
        '1', 
        '0.0', 
        '0.0', 
        '0.5', 
        '0.0', 
        '0.0', 
        '0.0'
    ]

    # Launch the spawn entity node 
    spawn_entity = Node(
        package='ezrassor_robot_description',
        executable ='spawn_rover',
        arguments=spawn_entity_args,
        output='screen'
    )

    """

    """
    # Load the controller_manager node
    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[model_description, controllers],
        output='screen'
    )
    """

    # Spawn the joint state broadcaster
    joint_state_broad = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', "--controller-manager", "/controller_manager"],
        output='screen'
    )

    diff_drive = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'diff_drive_controller'],
        output='screen'
    )

    arm_front = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'arm_front_velocity_controller'],
        output='screen'
    )

    arm_back = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'arm_back_velocity_controller'],
        output='screen'
    )

    drum_front = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'drum_front_velocity_controller'],
        output='screen'
    )

    drum_back = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'drum_back_velocity_controller'],
        output='screen'
    )

    delay_controller_after_spawn = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[joint_state_broad, diff_drive, arm_front, arm_back, drum_front, drum_back]
        )
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity,
        delay_controller_after_spawn
    ])
    


