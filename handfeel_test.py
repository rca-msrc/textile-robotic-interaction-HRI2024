import sys
import math
import time
import queue
import datetime
import random
import traceback
import threading
# xarm api
from xarm import version
from xarm.wrapper import XArmAPI
# 
from robot import Robot

left_arm_api = XArmAPI('192.168.1.225', baud_checkset=False)
right_arm_api = XArmAPI('192.168.1.244', baud_checkset=False)

left_robot = Robot(left_arm_api)
right_robot = Robot(right_arm_api)


### 
### Round
###
## 

# Y
left_round_y_center = [622.806396, -42.040199, 142.041245, -146.58134, 31.117223, -38.068061]
left_round_y_center_down = [622.806396, -42.040199, 134.912399, -146.58134, 31.117223, -38.068061]
left_round_y_back = [622.806335, -163.967209, 142.041214, -146.58134, 31.117223, -38.068061]
left_round_y_back_down = [622.806335, -163.967209, 134.912399, -146.58134, 31.117223, -38.068061]

right_round_y_center = [599.093933, -6.745806, 46.341305, -153.866555, 28.627894, -43.04036]
right_round_y_center_down = [599.093933, -6.745806, 39, -153.866555, 28.627894, -43.04036]
right_round_y_back = [599.093933, -123.964081, 46.341267, -153.866555, 28.627894, -43.04036]
right_round_y_back_down = [599.093933, -123.964081, 39, -153.866555, 28.627894, -43.04036]

# X
left_round_x_center =  [559.59137, 15.291674, 143.041229, -148.524583, 30.021384, -123.720725]
left_round_x_center_down = [559.590759, 15.291673, 134.941605, -148.524411, 30.021212, -123.720438]
left_round_x_back =  [468.352417, 15.291691, 143.041199, -148.524583, 30.021384, -123.720725]
left_round_x_back_down =  [468.352417, 15.291691,  134.941605, -148.524583, 30.021384, -123.720725]

right_round_x_center =  [614.858765, -19.32655, 44.763313, -153.866613, 28.627894, -127.381753]
right_round_x_center_down = [614.858765, -19.326902, 38.341522, -153.866555, 28.627894, -127.381753]
right_round_x_back = [528.529663, -19.326597, 44.763256, -153.866613, 28.627894, -127.381753]
right_round_x_back_down = [528.529663, -19.326597, 38.341522, -153.866613, 28.627894, -127.381753]

# XY

left_round_xy_center = [595.031189, -36.275436, 144.468384, -146.58134, 31.117223, -62.629329]
left_round_xy_center_down = [595.031189, -36.27544, 135.215225, -146.58134, 31.117223, -62.629329]
left_round_xy_back = [518.361023, -161.156662, 144.468384, -146.58134, 31.117223, -62.629329]
left_round_xy_back_down = [518.361023, -161.156662, 135.215225, -146.58134, 31.117223, -62.629329]

right_round_xy_center = [606.605652, -6.745358, 47.09613, -152.121498, 26.530983, -68.702911]
right_round_xy_center_down = [606.605652, -6.745358, 38.096127, -152.121498, 26.530983, -68.702911]
right_round_xy_back = [512.559082, -115.024704, 47.09613, -152.121498, 26.530983, -68.702911]
right_round_xy_back_down = [512.559082, -115.024704, 38.096127, -152.121498, 26.530983, -68.702911]


####
### Sharp
##
#

# Y

left_sharp_y_center = [622.806274, -50.55183, 145.040909, 143.6278, -27.443762, 147.963486]
left_sharp_y_center_down = [622.806274, -50.55183, 134.912399, 143.6278, -27.443762, 147.963486]
left_sharp_y_back = [622.806396, -163.967102, 142.041367, 142.848462, -26.294638, 149.68763]
left_sharp_y_back_down = [622.806396, -163.967102, 134.912399, 142.848462, -26.294638, 149.68763]

right_sharp_y_center = [599.093872, -15.745597, 46.341263, 154.007331, -28.753658, 136.666534]
right_sharp_y_center_down = [599.093933, -15.745597, 36, 154.007331, -28.753658, 136.666534]
right_sharp_y_back = [599.093811, -123.963943, 46.341263, 150.007914, -24.515031, 145.567434]
right_sharp_y_back_down = [599.093811, -123.963943, 36, 150.007914, -24.515031, 145.567434]

# X

left_sharp_x_center = [553.798645, 15.291856, 142.041382, 145.644382, -26.557682, 62.349267]
left_sharp_x_center_down = [553.798645, 15.291856, 135.356995, 145.644382, -26.557682, 62.349267]
left_sharp_x_back = [468.352417, 15.291856, 147.040756, 145.644382, -26.557682, 62.349267]
left_sharp_x_back_down = [468.352417, 15.291855, 135.356995, 145.644382, -26.557682, 62.349267]

right_sharp_x_center =  [613.324402, -16.111862, 43.341274, 154.214799, -28.936489, 51.895079]
right_sharp_x_center_down =   [613.324402, -16.111862, 37.341209, 154.214799, -28.936489, 51.895079]
right_sharp_x_back =  [528.529663, -16.111862, 43.34127, 154.214799, -28.936489, 51.895079]
right_sharp_x_back_down =  [528.529663, -16.111862, 37.341209, 154.214799, -28.936489, 51.895079]

# XY

left_sharp_xy_center = [594.031189, -40.275467, 139.359009, 146.57985, -31.115562, 117.373498]
left_sharp_xy_center_down = [594.031189, -40.275467, 131.437881, 146.57985, -31.115562, 117.373498]
left_sharp_xy_back = [518.360901, -161.156952, 139.359009, 148.289212, -32.863427, 114.147861]
left_sharp_xy_back_down = [518.360901, -161.156952, 131.437881, 148.289212, -32.863427, 114.147861]

right_sharp_xy_center =  [606.605713, -6.745147, 44.096176, 151.468555, -25.818567, 112.777116]
right_sharp_xy_center_down = [606.605713, -6.745148, 35.096165, 151.468555, -25.818567, 112.777116]
right_sharp_xy_back = [512.55896, -115.02433, 44.095943, 152.820907, -27.249873, 109.750753]
right_sharp_xy_back_down = [512.55896, -115.02433, 35.096165, 152.820907, -27.249873, 109.750753]


#
# Transitions
#

## Round 
print("=== Round ===")
# Start Y
print("----- Y -----")
left_robot.linear_move([left_round_y_center], wait=False)
right_robot.linear_move([right_round_y_center])

left_robot.linear_move([left_round_y_back], wait=False)
right_robot.linear_move([right_round_y_back])

# Start X
print("----- X -----")
left_robot.linear_move([left_round_x_center], wait=False)
right_robot.linear_move([right_round_x_center])

left_robot.linear_move([left_round_x_back], wait=False)
right_robot.linear_move([right_round_x_back])

# Start XY
print("----- XY ----")
left_robot.linear_move([left_round_xy_center], wait=False)
right_robot.linear_move([right_round_xy_center])

left_robot.linear_move([left_round_xy_back], wait=False)
right_robot.linear_move([right_round_xy_back])

# Back to X
print("----- X -----")
left_robot.linear_move([left_round_x_back], wait=False)
right_robot.linear_move([right_round_x_back])

left_robot.linear_move([left_round_x_center], wait=False)
right_robot.linear_move([right_round_x_center])

# Back to Y
print("----- Y -----")
left_robot.linear_move([left_round_y_back], wait=False)
right_robot.linear_move([right_round_y_back])

left_robot.linear_move([left_round_y_center], wait=False)
right_robot.linear_move([right_round_y_center])

## Sharp
print("=== Sharp ===")

# Start Y
print("----- Y -----")
left_robot.linear_move([left_sharp_y_center], wait=False)
right_robot.linear_move([right_sharp_y_center])

left_robot.linear_move([left_sharp_y_back], wait=False)
right_robot.linear_move([right_sharp_y_back])

# Start X
print("----- X -----")
left_robot.linear_move([left_sharp_x_center], wait=False)
right_robot.linear_move([right_sharp_x_center])

left_robot.linear_move([left_sharp_x_back], wait=False)
right_robot.linear_move([right_sharp_x_back])

# Start XY
print("----- XY -----")
left_robot.linear_move([left_sharp_xy_center], wait=False)
right_robot.linear_move([right_sharp_xy_center])

# Prepare to Reset
print("=== Prepare ===")
left_reset = [586.499084, -43.446308, 287.829834, 146.57985, -31.115562, 117.373498]
right_reset = [594.292725, -20.638094, 181.862991, 151.468498, -25.818567, 112.777116]

left_robot.linear_move([left_reset], wait=False)
right_robot.linear_move([right_reset])

# Servo Reset
print("=== Reset ===")
left_init = [0, -12, 0, 31.4, 0, 43.4, 0]
right_init = [0, -22.3, 0, 25.1, 0, 47.3, 0]

left_robot._arm.set_servo_angle(angle=left_init, speed=50, is_radian=False, wait=False)
right_robot._arm.set_servo_angle(angle=right_init, speed=50, is_radian=False, wait=True)

print("Done.")
