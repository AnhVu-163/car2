#!/usr/bin/env python

import rospy
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from geometry_msgs.msg import Twist
import sys
import tty
import termios

def get_key():
    """Đọc phím không echo"""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] &= ~termios.ECHO
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def send_trajectory(pub, joints, positions, time=0.5, velocities=[0.1, 0.1]):
    """Gửi JointTrajectory cho tay máy"""
    traj = JointTrajectory()
    traj.header.frame_id = "car"
    traj.header.stamp = rospy.Time.now()
    traj.joint_names = joints
    point = JointTrajectoryPoint()
    point.positions = positions
    point.velocities = velocities
    point.time_from_start = rospy.Duration(time)
    traj.points.append(point)
    pub.publish(traj)
    if time > 1:
        rospy.sleep(time)

def control_robot_and_arm():
    rospy.init_node('robot_and_arm_controller', anonymous=True)
    arm_pub = rospy.Publisher('/car2/arm_trajectory_command', JointTrajectory, queue_size=10)
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    # Đợi Gazebo sẵn sàng
    rospy.loginfo("Waiting for Gazebo...")
    rospy.wait_for_service('/gazebo/spawn_urdf_model')
    rospy.sleep(2)

    # Khởi tạo tay máy
    joints = ['arm_base_joint', 'arm_joint']
    arm_base_pos, arm_pos = 0.0, -1.57
    step = 0.1
    arm_limits = {'base': (-3.14, 3.14), 'arm': (-3.14, 0.0)}
    send_trajectory(arm_pub, joints, [0.0, 0.0], 2.0)  # Home pose

    # Khởi tạo robot
    twist = Twist()
    speed, turn = 3.0, 3.0
    key_bindings = {
        'w': (1, 0), 's': (-1, 0),  # Robot: tiến, lùi
        'a': (0, 1), 'd': (0, -1),  # Robot: trái, phải
        ' ': (0, 0)                 # Robot: dừng
    }

    print("Control: WASD (robot), IJKL (arm), Space (stop), Q (quit)")
    
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        key = get_key()

        # Điều khiển tay máy
        if key == 'j': arm_base_pos = max(arm_limits['base'][0], arm_base_pos - step)
        elif key == 'l': arm_base_pos = min(arm_limits['base'][1], arm_base_pos + step)
        elif key == 'i': arm_pos = min(arm_limits['arm'][1], arm_pos + step)
        elif key == 'k': arm_pos = max(arm_limits['arm'][0], arm_pos - step)
        if key in 'jlik':
            send_trajectory(arm_pub, joints, [arm_base_pos, arm_pos])

        # Điều khiển robot
        if key in key_bindings:
            linear, angular = key_bindings[key]
            twist.linear.x = linear * speed
            twist.angular.z = angular * turn
        elif key not in 'jlikq':  # Không ảnh hưởng robot khi dùng phím tay máy
            twist.linear.x = 0.0
            twist.angular.z = 0.0
        cmd_vel_pub.publish(twist)

        # Thoát
        if key == 'q':
            rospy.loginfo("Exiting...")
            break
        
        rate.sleep()

if __name__ == "__main__":
    try:
        control_robot_and_arm()
    except rospy.ROSInterruptException:
        pass