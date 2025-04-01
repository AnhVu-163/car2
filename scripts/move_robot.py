#!/usr/bin/env python
import rospy
import sys, select, termios, tty
from geometry_msgs.msg import Twist

# Khai báo các phím điều khiển
KEY_BINDINGS = {
    'w': (1, 0),  # Tiến
    's': (-1, 0), # Lùi
    'a': (0, 1),  # Quay trái
    'd': (0, -1), # Quay phải
    ' ': (0, 0)   # Dừng lại
}

def get_key():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def control_robot():
    rospy.init_node('robot_keyboard_controller', anonymous=True)
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    twist = Twist()
    speed = 3.0  # Tốc độ di chuyển
    turn = 3.0   # Tốc độ quay
    
    rospy.loginfo("Use 'WASD' to move, 'Space' to stop, and 'Ctrl+C' to exit.")
    
    while not rospy.is_shutdown():
        key = get_key()
        if key in KEY_BINDINGS:
            linear, angular = KEY_BINDINGS[key]
            twist.linear.x = linear * speed
            twist.angular.z = angular * turn
        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
        
        cmd_vel_pub.publish(twist)
        rospy.loginfo(f"Moving: linear={twist.linear.x}, angular={twist.angular.z}")
        
        if key == '\x03':  # Ctrl+C để thoát
            break

if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)
    try:
        control_robot()
    except rospy.ROSInterruptException:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)