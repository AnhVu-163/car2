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
