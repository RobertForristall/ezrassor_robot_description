from setuptools import setup

package_name = 'ezrassor_robot_description'
data_files = []

configs = [
    'config/standard_rover/default_position_controllers.yaml',
    'config/rviz_controllers.yaml',
    'config/ezrassor_rviz_config.rviz',
    'config/ezrassor_basic_controllers.yaml'
]

urdfs = [
    'urdf/ezrassor.gazebo',
    'urdf/ezrassor.xacro',
    'urdf/macros.xacro',
    'urdf/materials.xacro',
    'urdf/ezrassor_rviz.xacro',
    'urdf/ezrassor_basic.xacro',
    'urdf/wheel.xacro',
    'urdf/ezrassor_basic.gazebo',
    'urdf/drum_arm.xacro',
    'urdf/drum.xacro'
]

meshes = [
    'meshes/arm_camera.dae',
    'meshes/base_station.dae',
    'meshes/base_unit.dae',
    'meshes/d435.dae',
    'meshes/drum_arm.dae',
    'meshes/drum.dae',
    'meshes/grabber1.dae',
    'meshes/grabber2.dae',
    'meshes/link1.dae',
    'meshes/link2.dae',
    'meshes/link3.dae',
    'meshes/link4.dae',
    'meshes/link5.dae',
    'meshes/link6_old.dae',
    'meshes/link6.1.dae',
    'meshes/link6.dae',
    'meshes/platform.dae',
    'meshes/processor_housing.dae',
    'meshes/rover_arm_back.dae',
    'meshes/wheel.dae',
]

data_files.append(('share/ament_index/resource_index/packages',['resource/' + package_name]))
data_files.append(('share/' + package_name, ['package.xml']))
data_files.append(('share/' + package_name + '/launch', ['launch/rviz_launch.py', 'launch/gazebo_launch.py', 'launch/basic_gazebo_launch.py']))
data_files.append(('share/' + package_name + '/meshes', meshes))
data_files.append(('share/' + package_name + '/urdf', urdfs))
data_files.append(('share/' + package_name + '/config', configs))

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robert',
    maintainer_email='robert@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = ezrassor_robot_description.my_node:main',
            'spawn_rover = ezrassor_robot_description.spawn_rover:main',
            'wheel_driver = ezrassor_robot_description.wheel_driver:main',
            'drum_driver = ezrassor_robot_description.drum_driver:main',
            'drum_arm_driver = ezrassor_robot_description.drum_arm_driver:main'
        ],
    },
)
