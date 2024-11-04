from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    # Define path to your Xacro file
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')
    xacro_file = os.path.join(
        get_package_share_directory('my_bot'),  # Replace with your package name
        'description',
        'robot.urdf.xacro'  # Replace with your Xacro file name
    )

    # Define path to your custom Gazebo world file
    world = os.path.join(
        get_package_share_directory('my_bot'),  # Replace with your package name
        'worlds',  # Replace with the directory containing your world file
        'floorplan.world'  # Replace with your world file name
    )
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )
    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )
    # Convert Xacro to URDF at runtime
    robot_description_content = Command(['xacro ', xacro_file])
    robot_description = {'robot_description': robot_description_content}

        # Run the robot_state_publisher node
    robot_state_publisher_cmd=Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[robot_description]
            )

        # Spawn the robot in Gazebo
    spawn_cmd= Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-topic', 'robot_description', '-entity', 'my_robot',             
            '-x', x_pose,
            '-y', y_pose,
            '-z', '0.01'],
            output='screen'
            )
    ld = LaunchDescription()

    # Add the commands to the launch description
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_cmd)

    return ld