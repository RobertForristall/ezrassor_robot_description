# ROS2 Humble python launch file to launch the ezrassor rover
# in the gazebo simulation program
# 
# Written by Robert Forristall

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, IncludeLaunchDescription, DeclareLaunchArgument
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit, OnExecutionComplete
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.conditions import UnlessCondition, IfCondition
import xacro

def generate_launch_description():

    # Get relevant package directories
    pkg_self = get_package_share_directory('ezrassor_robot_description')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_auto = get_package_share_directory('ezrassor_autonomous_control')
    pkg_key_listener = get_package_share_directory('keyboard_listener')

    basic_model = 'ezrassor_basic.xacro'

    # Generate robot description based on model launch condition
    model_description_basic = {'robot_description': 
        xacro.process_file(
            os.path.join(pkg_self, 'urdf', basic_model)
        ).toxml()}

    world_file = os.path.join(pkg_self, 'worlds', 'base.world')

    # Include the gazebo launch to load the simulation
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={"world": world_file}.items()
    )   

    auto_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_auto, 'launch', 'test_controls_launch.py')
        )
    )

    keyboard_listener = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_key_listener, 'launch', 'listener_launch.py')
        )
    )

    # Launch robot state publisher
    robot_state_publisher_basic = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[model_description_basic],
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
    
    joint_state_broad = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )

    diff_drive = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'diff_drive_base_controller'],
        output='screen'
    )

    arm_front = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'arm_front_controller'],
        output='screen',
    )

    arm_back = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'arm_back_controller'],
        output='screen'
    )

    drum_front = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'drum_front_controller'],
        output='screen',
    )

    drum_back = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'drum_back_controller'],
        output='screen'
    )

    wheel_driver = Node(
        package='ezrassor_robot_description',
        executable ='wheel_driver',
        output='screen'
    )

    drum_driver = Node(
        package='ezrassor_robot_description',
        executable ='drum_driver',
        output='screen'
    )

    drum_arm_driver = Node(
        package='ezrassor_robot_description',
        executable ='drum_arm_driver',
        output='screen'
    )
    

    delay_controller_after_spawn = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[
                joint_state_broad, 
                diff_drive, 
                arm_front, 
                arm_back, 
                drum_front, 
                drum_back,
                wheel_driver,
                drum_arm_driver,
                drum_driver,
                auto_launch,
                keyboard_listener
            ]
        )
    )

    return LaunchDescription([
        DeclareLaunchArgument('spawn_x', default_value='0'),
        DeclareLaunchArgument('spawn_y', default_value='0'),
        DeclareLaunchArgument('target_x', default_value='5'),
        DeclareLaunchArgument('target_y', default_value='5'),
        DeclareLaunchArgument('world', default_value=world_file),
        DeclareLaunchArgument('controls', default_value='auto'),
        DeclareLaunchArgument('model', default_value='basic'),
        gazebo,
        robot_state_publisher_basic,
        spawn_entity,
        delay_controller_after_spawn
    ])