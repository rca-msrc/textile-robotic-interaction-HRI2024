import sys
import math
import time
import queue
import datetime
import random
import traceback
import threading
import json

# xarm api
from xarm import version
from xarm.wrapper import XArmAPI
# 
from robot import Robot

left_arm_api = XArmAPI('192.168.1.225', baud_checkset=False)
right_arm_api = XArmAPI('192.168.1.244', baud_checkset=False)

left_robot = Robot(left_arm_api)
right_robot = Robot(right_arm_api)

#
# progress of scanning
#
if len(sys.argv) >= 2:
    _name = sys.argv[1] # name of this scan provided on the command line
else: # default to datetime
    _name = "handfeel_{}".format(datetime.datetime.now())
progress = {"name": _name, "progress": []}

# start
progress["start"] = str(datetime.datetime.now())

def log(message):
    print("=== %s ===" % message)
    progress["progress"].append({
        "message": message,
        "datetime": str(datetime.datetime.now()),
        "left_pos": left_robot._arm.get_position(),
        "right_pos": right_robot._arm.get_position(),        
    })
    
    
def z(pos, offset):
    return pos[:2] + [pos[2] + offset] + pos[3:]

def motion(left_center, left_center_down, left_back, left_back_down,
           right_center, right_center_down, right_back, right_back_down, n=3, weight=2):
    # reset
    left_robot.linear_move([left_center], wait=False)
    right_robot.linear_move([right_center])

    # repeat n times
    for i in range(n):

        left_robot.linear_move([z(left_center_down, -i*weight)], wait=False)
        right_robot.linear_move([z(right_center_down, -i*weight)])

        left_robot.linear_move([z(left_back_down, -i*weight)], wait=False)
        right_robot.linear_move([z(right_back_down, -i*weight)])

        left_robot.linear_move([left_back], wait=False)
        right_robot.linear_move([right_back])

        time.sleep(0.5)

        left_robot.linear_move([left_center], wait=False)
        right_robot.linear_move([right_center])  


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
right_round_x_center_down = [614.858765, -19.326902, 37.341522, -153.866555, 28.627894, -127.381753]
right_round_x_back = [528.529663, -19.326597, 44.763256, -153.866613, 28.627894, -127.381753]
right_round_x_back_down = [528.529663, -19.326597, 37.341522, -153.866613, 28.627894, -127.381753]

# XY
left_round_xy_center = [595.031189, -36.275436, 144.468384, -146.58134, 31.117223, -62.629329]
left_round_xy_center_down = [595.031189, -36.27544, 135.215225, -146.58134, 31.117223, -62.629329]
left_round_xy_back = [518.361023, -161.156662, 144.468384, -146.58134, 31.117223, -62.629329]
left_round_xy_back_down = [518.361023, -161.156662, 135.215225, -146.58134, 31.117223, -62.629329]

right_round_xy_center = [606.605652, -6.745358, 47.09613, -152.121498, 26.530983, -68.702911]
right_round_xy_center_down = [606.605652, -6.745358, 36, -152.121498, 26.530983, -68.702911]
right_round_xy_back = [512.559082, -115.024704, 47.09613, -152.121498, 26.530983, -68.702911]
right_round_xy_back_down = [512.559082, -115.024704, 36, -152.121498, 26.530983, -68.702911]


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
left_sharp_x_center = [553.798645, 5.040157, 142.041382, 145.644382, -26.557682, 62.349267]
left_sharp_x_center_down = [553.798645, 5.040157, 133, 145.644382, -26.557682, 62.349267]
left_sharp_x_back = [468.352417, 5.040157, 147.040756, 145.644382, -26.557682, 62.349267]
left_sharp_x_back_down = [468.352417, 5.040157, 133, 145.644382, -26.557682, 62.349267]

right_sharp_x_center =  [613.324402, -16.111862, 43.341274, 154.214799, -28.936489, 51.895079]
right_sharp_x_center_down =   [613.324402, -16.111862, 35, 154.214799, -28.936489, 51.895079]
right_sharp_x_back =  [528.529663, -16.111862, 43.34127, 154.214799, -28.936489, 51.895079]
right_sharp_x_back_down =  [528.529663, -16.111862, 35, 154.214799, -28.936489, 51.895079]

# XY
left_sharp_xy_center = [594.031189, -40.275467, 142, 146.57985, -31.115562, 117.373498]
left_sharp_xy_center_down = [594.031189, -40.275467, 136.5, 146.57985, -31.115562, 117.373498]
left_sharp_xy_back = [518.360901, -161.156952, 142, 148.289212, -32.863427, 114.147861]
left_sharp_xy_back_down = [518.360901, -161.156952, 136.5, 148.289212, -32.863427, 114.147861]

right_sharp_xy_center =  [606.605713, -6.745147, 42, 151.468555, -25.818567, 112.777116]
right_sharp_xy_center_down = [606.605713, -6.745148, 33, 151.468555, -25.818567, 112.777116]
right_sharp_xy_back = [512.55896, -115.02433, 42, 152.820907, -27.249873, 109.750753]
right_sharp_xy_back_down = [512.55896, -115.02433, 33, 152.820907, -27.249873, 109.750753]


#
# Transitions
#
N=6
WEIGHT=1

log("Start, N = %d, WEIGHT = %s" % (N,WEIGHT))

## Round 
print("=== Round ===")

# Start Y
log("Round Y")
left_robot.linear_move([left_round_y_center], wait=False)
right_robot.linear_move([right_round_y_center])

motion(left_round_y_center, left_round_y_center_down, left_round_y_back, left_round_y_back_down,
       right_round_y_center, right_round_y_center_down, right_round_y_back, right_round_y_back_down, N, WEIGHT)

log("Switch")
left_robot.linear_move([left_round_y_back], wait=False)
right_robot.linear_move([right_round_y_back])

# Start X
log("Round X")
left_robot.linear_move([left_round_x_center], wait=False)
right_robot.linear_move([right_round_x_center])

motion(left_round_x_center, left_round_x_center_down, left_round_x_back, left_round_x_back_down,
       right_round_x_center, right_round_x_center_down, right_round_x_back, right_round_x_back_down, N, WEIGHT)

log("Switch")
left_robot.linear_move([left_round_x_back], wait=False)
right_robot.linear_move([right_round_x_back])

# Start XY
log("Round XY")
left_robot.linear_move([left_round_xy_center], wait=False)
right_robot.linear_move([right_round_xy_center])

motion(left_round_xy_center, left_round_xy_center_down, left_round_xy_back, left_round_xy_back_down,
       right_round_xy_center, right_round_xy_center_down, right_round_xy_back, right_round_xy_back_down, N, WEIGHT)


# Prepare to Reset
log("Prepare 1")
left_reset1 = [518.361023, -161.15657, 395.066772, -146.58134, 31.117223, -62.629329]
right_reset1 = [512.559021, -115.024704, 310.15274, -152.121498, 26.530983, -68.702911]
left_robot.linear_move([left_reset1], wait=False)
right_robot.linear_move([right_reset1])

# Servo Reset
log("Reset 1")
left_init = [0, -12, 0, 31.4, 0, 43.4, 0]
right_init = [0, -22.3, 0, 25.1, 0, 47.3, 0]

left_robot._arm.set_servo_angle(angle=left_init, speed=50, is_radian=False, wait=False)
right_robot._arm.set_servo_angle(angle=right_init, speed=50, is_radian=False, wait=True)

## Sharp
print("=== Sharp ===")

# Start Y
log("Sharp Y")
left_robot.linear_move([left_sharp_y_center], wait=False)
right_robot.linear_move([right_sharp_y_center])

motion(left_sharp_y_center, left_sharp_y_center_down, left_sharp_y_back, left_sharp_y_back_down,
       right_sharp_y_center, right_sharp_y_center_down, right_sharp_y_back, right_sharp_y_back_down, N, WEIGHT)

log("Switch")
left_robot.linear_move([left_sharp_y_back], wait=False)
right_robot.linear_move([right_sharp_y_back])

# Start X
log("Sharp X")
left_robot.linear_move([left_sharp_x_center], wait=False)
right_robot.linear_move([right_sharp_x_center])

motion(left_sharp_x_center, left_sharp_x_center_down, left_sharp_x_back, left_sharp_x_back_down,
       right_sharp_x_center, right_sharp_x_center_down, right_sharp_x_back, right_sharp_x_back_down, N, WEIGHT)

log("Switch")
left_robot.linear_move([left_sharp_x_back], wait=False)
right_robot.linear_move([right_sharp_x_back])

# Start XY
log("Sharp XY")
left_robot.linear_move([left_sharp_xy_center], wait=False)
right_robot.linear_move([right_sharp_xy_center])

motion(left_sharp_xy_center, left_sharp_xy_center_down, left_sharp_xy_back, left_sharp_xy_back_down,
       right_sharp_xy_center, right_sharp_xy_center_down, right_sharp_xy_back, right_sharp_xy_back_down, N, WEIGHT)


# Prepare to Reset
log("Prepare 2")
left_reset = [586.499084, -43.446308, 287.829834, 146.57985, -31.115562, 117.373498]
right_reset = [594.292725, -20.638094, 181.862991, 151.468498, -25.818567, 112.777116]

left_robot.linear_move([left_reset], wait=False)
right_robot.linear_move([right_reset])

# Servo Reset
log("Reset 2")
left_init = [0, -12, 0, 31.4, 0, 43.4, 0]
right_init = [0, -22.3, 0, 25.1, 0, 47.3, 0]

left_robot._arm.set_servo_angle(angle=left_init, speed=50, is_radian=False, wait=False)
right_robot._arm.set_servo_angle(angle=right_init, speed=50, is_radian=False, wait=True)

# end
progress["end"] = str(datetime.datetime.now())
print("Done.")

# dump progress
with open("handfeel_{}.json".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")), 'w') as fd:
    json.dump(progress,fd)
