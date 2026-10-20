#!/usr/bin/env python3
"""Slow joint-state visualization only. Does not command motors or check collisions."""
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class Preview(Node):
    def __init__(self):
        super().__init__('arm_pose_preview')
        self.pub = self.create_publisher(JointState, 'joint_states', 10)
        self.start = self.get_clock().now()
        self.timer = self.create_timer(0.05, self.tick)
    def tick(self):
        t = (self.get_clock().now() - self.start).nanoseconds * 1e-9
        a = math.sin(t * 0.15)
        q = [math.radians(20)*a, math.radians(45), math.radians(-85), math.radians(40), math.radians(15)*a, 0.015+0.01*a]
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['j1','j2','j3','j4','j5','gripper_opening','j1_motor_rotation','j2_motor_rotation','left_jaw_mimic','gripper_pinion_mimic']
        msg.position = q + [4*q[0],-4*q[1],q[5],-q[5]/0.018]
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = Preview()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
if __name__ == '__main__': main()
