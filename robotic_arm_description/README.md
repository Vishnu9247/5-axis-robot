# Five-axis arm with parallel gripper - ROS 2 / RViz2

**For an easy introduction, open `HOW_TO_READ_THE_ROBOT.md` in the package, or `START HERE - Understanding the Robot.md` in the delivery folder.**

This is a separate assembly and visualization package. The previously finalized robot and gripper print folders are preserved. No new print parts are required for the tool mounting interface.

## Open the model

Import `Assembly/Five Axis Arm With Gripper.f3d` into Fusion 360. The gripper mounts to the existing four M4 holes on the 32 mm square tool interface. Use the original gripper guide for the required metal hub, shaft, bearings and mounting hardware. Confirm screw engagement and actual purchased interfaces before assembly.

## Run RViz2

Use a Linux environment with ROS 2 already installed and sourced. Copy the included `ros2_ws` folder there. Install the viewing dependencies:

```sh
sudo apt install ros-$ROS_DISTRO-xacro ros-$ROS_DISTRO-rviz2 ros-$ROS_DISTRO-robot-state-publisher ros-$ROS_DISTRO-joint-state-publisher-gui python3-colcon-common-extensions
cd ros2_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch robotic_arm_description display.launch.py
```

The sliders move J1 through J5 and `gripper_opening`. That slider is half the jaw opening: 0.015 m means 30 mm between the pads; the maximum is 0.03 m for a 60 mm opening. The opposite jaw and pinion follow through mimic joints. Motor rotor visualization includes the provisional 4:1 base and shoulder reductions.

For a slow illustrative pose preview instead of sliders:

```sh
ros2 launch robotic_arm_description display.launch.py demo:=true
```

Use one launch mode at a time. The preview publishes joint states only; it does not command hardware or check collisions. To inspect frames, enable Joint Frames in RViz. The `grasp_tcp` frame is at the nominal gripping-pad center, 96 mm forward of the tool mounting plane.

## Scope and limits

The URDF uses CAD-derived meshes in meters and the measured Fusion joint origins and axes. Visual and collision meshes have the same geometry. Collision meshes include fasteners and are detailed; simplify them before performance-sensitive planning. They are assembly visualization meshes, not files for printing.

RViz2 displays kinematics; it does not perform physics, self-collision checking, load testing or motor control. No inertias, controllers, transmission hardware interfaces or dynamics model are supplied. Joint effort values are zero because actuator capability is unvalidated; velocity limits are preliminary display values. This is not a Gazebo or hardware-ready package.

The independent joint limits do not make every combination collision-free. Some combinations can strike the base or mounting surface. The preview pose is illustrative and must not be sent to motors as a verified trajectory. See Review for the exact scope of CAD checks. No continuous collision sweep is claimed.

The gripper still has no selected actuator. Its simulated opening represents the manual rack-and-pinion mechanism, not a working powered gripper. CAD-envelope mass was approximately 578 g before selecting an actuator. The earlier motor/load screen found the shoulder torque insufficient for the assumed fully extended load. Adding this gripper does not resolve that issue. No 700 g payload rating or structural validation is claimed. Secure the base to a rigid bench with the specified metal anchors before powered tests.

ROS 2 and RViz2 are unavailable on the authoring computer. XML, meshes, tree connectivity and numerical forward kinematics are checked offline; the ROS launch has not been runtime-tested here.

## Files

- `Assembly`: separate editable Fusion archive.
- `ros2_ws/src/robotic_arm_description/urdf/robot.urdf.xacro`: short main description, including one file per joint.
- `ros2_ws/src/robotic_arm_description/HOW_TO_READ_THE_ROBOT.md`: illustrated-by-examples reading guide.
- `urdf/robot.urdf`: generated compatibility copy; regenerate it after editing the smaller files.
- `meshes`: CAD assembly meshes in meters.
- `launch/display.launch.py`: RViz2 and state publishers.
- `scripts/pose_preview.py`: joint-state visualization preview.
- `Review`: native CAD and export validation reports.

ROS behavior references: [robot_state_publisher](https://github.com/ros/robot_state_publisher), [joint_state_publisher](https://github.com/ros/joint_state_publisher).

## Completed offline checks

- URDF parser accepted the robot: 15 links and 14 joints, including fixed frames and mimic joints.
- All 12 CAD mesh files resolve and pass binary-mesh integrity and unit checks.
- Tool transforms match seven native Fusion motion samples, with a maximum matrix error below 5e-12.
- Four listed CAD configurations have no unexpected solid interference or parts below the mounting plane; collar/set-screw thread envelopes are recorded separately in the report. This is a sampled check, not a continuous sweep.
- All 106 files in the finalized source robot and gripper packages retain their original hashes.
