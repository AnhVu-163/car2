
```markdown
# Robot Simulation with ROS and Gazebo

## Mô tả
Dự án mô phỏng một **robot di động 2 bánh** tích hợp:
- **Tay máy**: 2 bậc tự do (rotation).
- **Cảm biến**: IMU, Camera, Encoder.

## Yêu cầu
- **Hệ điều hành**: Ubuntu 20.04
- **ROS**: ROS Noetic
- **Gazebo**: Phiên bản 11
- **Các package phụ thuộc**:
  - `gazebo_ros_control`
  - `joint_state_controller`
  - `position_controllers`
  - `diff_drive_controller`
 Killed- `robot_state_publisher`
  - `joint_state_publisher`

##  Cài đặt

###  Bước 1: Tạo ROS Workspace
```bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
catkin_init_workspace
```

###  Bước 2: Clone Repository
```bash
git clone https://github.com/thaithinhhl/ROS.git
cd ~/catkin_ws
catkin_make
```

###  Bước 3: Source Workspace
```bash
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

##  Mô phỏng

###  Bước 4: Khởi chạy mô phỏng trong Gazebo
```bash
roslaunch car2 gazebo.launch
```
*Kết quả*: Mở Gazebo với robot và môi trường mô phỏng.

###  Bước 5: Mở RViz để quan sát Robot
```bash
roslaunch car2 display.launch
```
*Kết quả*: Hiển thị robot trong RViz để theo dõi trạng thái.

###  Bước 6: Điều khiển robot di chuyển 
- **Cách thực hiện**: Dùng 4 phím WASD bàn phím để di chuyển robot
```bash
rosrun car2 move_robot.py
```
*Kết quả*: Robot di chuyển theo lệnh chỉ định.

###  Bước 7: Điều khiển cánh tay robot
- **Cách thực hiện**: Dùng 4 phím IJKL bàn phím để chuyển động tay
```bash
rosrun car2 move_arm.py
```
*Kết quả*: Điều khiển cánh tay robot robot bằng phím.

###  Bước 8: Đọc giá trị các cảm biến 
#### IMU
```bash
rostopic echo /imu/data
```
#### Encoder
```bash
rostopic echo /odom
```
#### Camera
```bash
rosrun image_view image_view image:=/camera/image_raw
```
