# gesture-swarm-ros2

ROS 2 package for gesture-controlled robot swarm using YOLO-based ASL gesture recognition and turtlesim as a demo environment.

## Structure

- `gesture_swarm_ros2/` – ROS 2 Python package with:
  - `gesture_detector_node` – webcam + YOLO11n detector, publishes `/gesture/symbol`.
  - `command_parser_node` – accumulates symbols, parses into commands, publishes `/swarm/command`.
  - `turtlesim_controller_node` – maps commands to `/turtle1/cmd_vel`.
  - `command_parser.py` – pure-Python command parsing logic.
  - `symbol_filter.py` – deduplication of consecutive symbols.

## Requirements

- ROS 2 (e.g. Lyrical / Humble)
- Python 3.10+
- `ultralytics`, `opencv-python`
- turtlesim: `sudo apt install ros-<distro>-turtlesim`

## Setup

In your ROS workspace (e.g. `~/gesture_ws`):

```bash
cd ~/gesture_ws
source .venv/bin/activate          # if you use a venv
source /opt/ros/<distro>/setup.bash
source install/setup.bash
```

## Run demo

Terminal 1 – turtlesim:

```bash
ros2 run turtlesim turtlesim_node
```

Terminal 2 – detector:

```bash
ros2 run gesture_swarm_ros2 gesture_detector_node --ros-args -p camera_id:=0
```

Terminal 3 – command parser:

```bash
ros2 run gesture_swarm_ros2 command_parser_node
```

Terminal 4 – turtlesim controller:

```bash
ros2 run gesture_swarm_ros2 turtlesim_controller_node
```

Show gestures (A, B, F, L, R, U, D, etc.) to control the turtle.
