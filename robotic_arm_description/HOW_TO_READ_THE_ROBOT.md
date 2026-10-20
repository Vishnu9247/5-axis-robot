# Read this first: understanding your robot files

Start with `urdf/robot.urdf.xacro`. It is a short contents page that loads the smaller files. The launch file combines them automatically into the single description ROS needs. You only need to read one joint at a time.

## 1. Which file should I open?

All component files are inside `urdf/parts/`.

| File | What it describes | Movement |
| --- | --- | --- |
| `00_base.xacro` | The bench reference and fixed base housing | Fixed |
| `01_j1_rotation.xacro` | The assembly turning above the base | Base rotation, J1 |
| `02_j2_shoulder.xacro` | The upper arm attached to the shoulder | Shoulder elevation, J2 |
| `03_j3_elbow.xacro` | The forearm attached to the elbow | Elbow bend, J3 |
| `04_j4_wrist_bend.xacro` | The wrist attached to the forearm | Wrist bend, J4 |
| `05_j5_tool_rotation.xacro` | The rotating tool plate and mounting face | Tool rotation, J5 |
| `06_gripper_mount.xacro` | The fixed gripper frame and gripping reference point | Fixed to tool |
| `07_gripper_fingers.xacro` | Both fingers and the pinion | Gripper opening |
| `08_motor_visuals.xacro` | The base and shoulder motor rotors | Automatically follow J1/J2 |

Read 00 through 05 first to understand the arm. Then read 06 and 07 for the gripper. File 08 is only needed to understand how the motor rotors are displayed.

The chain of connections is:

```text
world (bench)
  -> base_link (fixed housing)
    -> J1 -> shoulder_link (turning shoulder support)
      -> J2 -> upper_arm_link
        -> J3 -> forearm_link
          -> J4 -> wrist_link
            -> J5 -> tool_link
              -> tool_flange (mounting-face reference)
                -> gripper_base
                  -> right_jaw
                  -> left_jaw
                  -> gripper_pinion
                  -> grasp_tcp (gripping reference point)
```

The gripper's jaws are both attached to its frame. They are not attached to each other. The two motor rotors form additional branches from the base and shoulder support.

## 2. What is a link?

A **link** is a rigid piece or group of pieces that move together. It can contain many printed parts, bolts and bearings represented by one mesh.

```xml
<link name="upper_arm_link">
  ...
</link>
```

Inside a link:

- `visual` tells RViz what shape and color to draw.
- `mesh filename` points to the STL containing that shape.
- `collision` supplies geometry for software that checks contact. RViz alone does not check collisions.

Some links, such as `tool_flange`, have no mesh: they are named reference points rather than visible parts.

## 3. What is a joint?

A **joint** connects two links and describes how they move relative to each other. For example:

```xml
<joint name="j2" type="revolute">
  <parent link="shoulder_link" />
  <child link="upper_arm_link" />
  ...
</joint>
```

Here, the shoulder support is the parent and the upper arm is the child. `revolute` means a rotating hinge. `prismatic` means sliding movement, used for the gripper. `fixed` means the connection does not move.

Common joint fields:

| Field | Plain meaning |
| --- | --- |
| `parent` | The part supporting this joint |
| `child` | The part moved by this joint |
| `origin xyz` | Joint position measured from the parent link's reference frame |
| `origin rpy` | Orientation of the joint frame: roll, pitch and yaw |
| `axis xyz` | Direction of rotation or sliding, expressed in the joint frame |
| `limit lower/upper` | Minimum and maximum movement |
| `mimic` | Follow another joint automatically |

## 4. How do I read the numbers?

**Distances are meters. Angles are radians.** These differ from Fusion's millimeters and the degrees normally used to describe movement.

| In these files | Familiar value |
| --- | --- |
| `0.001` meter | 1 mm |
| `0.01` meter | 10 mm |
| `0.1` meter | 100 mm |
| `0.03` meter | 30 mm |
| `1.5708` radians | About 90 degrees |
| `3.14159` radians | About 180 degrees |

For example, `xyz="0 0 0.257468465415"` locates a joint about 257.47 mm up from its parent reference frame. It is not the dimension of a printed part.

An axis of `0 0 1` means positive Z. An axis of `0 -1 0` means negative Y. The sign determines which direction counts as positive movement. The exact J5 axis comes from the slightly tilted CAD geometry, so it is not a simple global X direction.

The `effort="0"` values are placeholders for unknown actuator capability. They are not tested torque ratings. Velocity values are preliminary visualization values.

## 5. How does the gripper work in RViz?

Use the `gripper_opening` slider. Its value is the travel of **one** finger:

| Slider value | Total space between pads |
| --- | --- |
| `0` | 0 mm |
| `0.015` | 30 mm |
| `0.03` | 60 mm |

The left finger follows the same travel in the opposite direction because its axis points the other way. The pinion follows through a `mimic` relationship. This avoids needing separate controls for the two fingers and the gear. The physical gripper still needs an actuator selection.

The base and shoulder motor rotors also use `mimic`, with the provisional 4:1 belt ratios. They are visualizations of the drive relationship, not extra independent arm axes.

## 6. Which files do I edit or run?

- **Read/edit:** the relevant file inside `urdf/parts/`.
- **Main entry:** `urdf/robot.urdf.xacro`; its includes connect all the smaller files.
- **Start RViz:** `launch/display.launch.py`, using the command below.
- **Shapes:** `meshes/*.stl`; these stay unchanged in this reorganization.
- **Compatibility export:** `urdf/robot.urdf`; this is the expanded, long copy for programs requiring plain URDF. It is generated from the smaller files.

To install the newly added dependency in your existing ROS 2 environment:

```sh
sudo apt install ros-$ROS_DISTRO-xacro
```

Then rebuild and run from the included workspace:

```sh
cd ros2_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch robotic_arm_description display.launch.py
```

RViz automatically uses the smaller files. If another program needs the plain URDF, regenerate it after editing:

```sh
ros2 run xacro xacro src/robotic_arm_description/urdf/robot.urdf.xacro -o src/robotic_arm_description/urdf/robot.urdf
```

That command assumes the current folder is `ros2_ws`. A change in an origin moves a connection; it does not resize the CAD mesh. Keep changes consistent with the Fusion design. All geometry, joint limits and existing print parts are unchanged by this split.

Xacro is the ROS tool used to combine these XML files. See the [official Xacro project](https://github.com/ros/xacro) for further details.

The same validation limits still apply: this package supports viewing and kinematic inspection; no local RViz runtime test, physical dynamics validation or payload certification is claimed.
