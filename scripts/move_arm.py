#!/usr/bin/env python

import rospy
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import sys
import tty
import termios

def get_key():

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] &= ~termios.ECHO  # Tắt echo
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def send_trajectory(pub, joints, positions, time=0.5, velocities=[0.1, 0.1]):

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
    if time > 1:  # Chỉ sleep khi về home pose
        rospy.sleep(time)

def move_arm():
    rospy.init_node('arm_trajectory_node', anonymous=True)
    pub = rospy.Publisher('/car2/arm_trajectory_command', JointTrajectory, queue_size=10)
    
    rospy.loginfo("Waiting for Gazebo...")
    rospy.wait_for_service('/gazebo/spawn_urdf_model')
    rospy.sleep(2)
    
    joints = ['arm_base_joint', 'arm_joint']
    arm_base_pos, arm_pos = 0.0, -1.57
    step = 0.1
    limits = {'base': (-3.14, 3.14), 'arm': (-3.14, 0.0)}

    # Về home pose
    rospy.loginfo("Moving to home pose...")
    send_trajectory(pub, joints, [0.0, 0.0], 2.0)

    print("use 'ijkl' to move , 'q' to quit")
    
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        key = get_key()
        if key == 'j': arm_base_pos = max(limits['base'][0], arm_base_pos - step)
        elif key == 'l': arm_base_pos = min(limits['base'][1], arm_base_pos + step)
        elif key == 'i': arm_pos = min(limits['arm'][1], arm_pos + step)
        elif key == 'k': arm_pos = max(limits['arm'][0], arm_pos - step)
        elif key == 'q':
            rospy.loginfo("Exiting...")
            break
        
        if key in 'jlik':
            send_trajectory(pub, joints, [arm_base_pos, arm_pos])
        
        rate.sleep()

if __name__ == "__main__":
    try:
        move_arm()
    except rospy.ROSInterruptException:
        pass