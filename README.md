# Robot Simulation with ROS and Gazebo
Mô phỏng robot di động 2 bánh với tay máy 2 bậc tự do (xoay) và tích hợp cảm biến.

## Mô tả
Dự án mô phỏng một **robot di động 2 bánh** tích hợp:
- **Tay máy**: 2 bậc tự do (rotation).
- **Cảm biến**: LiDAR, Camera, Encoder (đo vị trí và vận tốc bánh xe).

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

## 🚀 Cài đặt

### 🔧 Bước 1: Tạo ROS Workspace
```bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
catkin_init_workspace
📥 Bước 2: Clone Repository
bash
git clone https://github.com/thaithinhhl/ROS.git
mv ROS Assem2
cd ~/catkin_ws
catkin_make
🧠 Bước 3: Source Workspace
bash
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
🛰️ Mô phỏng
🎯 Bước 4: Khởi chạy mô phỏng trong Gazebo
bash
roslaunch Assem2 gazebo.launch

Kết quả: Mở Gazebo với robot và môi trường mô phỏng.
⚙️ Bước 5: Load các Controller cho Robot
bash
roslaunch Assem2 start_controllers.launch

Kết quả: Kích hoạt các controller cho robot (bánh xe và tay máy).
🌐 Bước 6: Mở RViz để quan sát Robot
bash
roslaunch Assem2 display.launch

Kết quả: Hiển thị robot trong RViz để theo dõi trạng thái.
🦾 Bước 7: Điều khiển tay máy (Arm Controller)

    Cách thực hiện: Dùng 4 phím mũi tên trên bàn phím.

bash
rosrun Assem2 arm_teleop_keyboard.py
🎮 Bước 8: Điều khiển robot di chuyển
🧭 Cách 1: Gửi lệnh trực tiếp qua topic /cmd_vel
bash
rostopic pub /cmd_vel geometry_msgs/Twist "linear:
  x: 3.5
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 1.5" -r 10

Kết quả: Robot di chuyển với vận tốc tuyến tính 3.5 m/s và góc quay 1.5 rad/s.
🕹️ Cách 2: Chạy script điều khiển bằng bàn phím
bash
rosrun Assem2 teleop_keyboard.py

Kết quả: Điều khiển robot bằng phím.
🧾 Bước 9: Đọc giá trị Encoder từ bánh xe

    Cách thực hiện: Đọc topic /joint_states.

bash
rostopic echo /joint_states
