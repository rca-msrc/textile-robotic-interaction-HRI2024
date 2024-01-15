#!/usr/bin/env python3
#
"""
Tour for open-loop scanning of hanging materials
"""

import os
import sys
import time
import datetime
import json

from robot import Robot

# xarm api
from xarm import version
from xarm.wrapper import XArmAPI

# ip
LEFT_ROBOT_IP = '192.168.1.225'
RIGHT_ROBOT_IP = '192.168.1.244'

# apis
left_arm_api = XArmAPI(LEFT_ROBOT_IP, baud_checkset=False)
right_arm_api = XArmAPI(RIGHT_ROBOT_IP, baud_checkset=False)

# robots
left_robot = Robot(left_arm_api)
right_robot = Robot(right_arm_api)

#
# Initialise the robots
# 

# left
# - adjusted to accomodate the assymetry of the tablet's camera
left_robot.pprint("INIT LEFT ROBOT")
pinch_pos = [479.599762, 44.4063, 839.999634, 179.999963, -69.999973, 0]
left_robot.linear_move([pinch_pos], wait=True)

# right
right_robot.pprint("INIT RIGHT ROBOT")
center_center_start = [390.826996, -2.239847, 519.205505, -103.282518, -3.548614, -91.735356]
right_robot.linear_move([center_center_start], wait=True)

### Scan Positions
pos = {
    "top_center_close": [478.501587, 5.682164, 695.844788, -106.91232, -3.167826, -94.963687],
    "center_center_close": [496.765289, -2.239839, 519.205505, -103.403527, 0.448626, -91.73209],
    "center_left_close": [639.464722, 28.043819, 496.917847, -90.127923, 2.532989, -176.475298],
    "center_right_close": [532.332581, -124.216591, 519.204163, -91.173571, -1.023016, -3.77837],
    # 5cm -x dir - offset by 5cm
    "top_center_mid": [428.701965, 5.682153, 695.844788, -98.812416, -3.849532, -92.530048],
    "center_center_mid": [447.926514, -2.239841, 519.205505, -103.34308, -1.550137, -91.732663],
    "center_left_mid": [615.916809, 77.506714, 496.917603, -90.127865, 2.532932, -165.47554],
    "center_right_mid": [532.33252, -176.839905, 519.203979, -91.173571, -1.023016, -3.77837],
    # offset by 5 cm
    "center_center": [390.826996, -2.239847, 519.205505, -103.282518, -3.548614, -91.735356],
    "center_center_down": [390.826996, -2.239847, 519.205505, -171.807812, -2.916756, -87.335613],
    "center_center_up": [390.826996, -2.239846, 519.205505, -57.925174, -6.232348, -92.114138],
    "top_center": [380.611633, 5.682147, 695.844788, -98.772767, -4.736012, -92.533028],
    "center_left": [615.916809, 130.79837, 496.917603, -89.364456, -3.19126, -168.471994],
    "center_right": [490.284393, -226.00264, 519.203796, -91.173456, -1.023016, -16.237567],
    # offset by 10 cm
    "center_center_far": [390.826996, -2.239847, 519.205505, -103.282518, -3.548614, -91.735356],
    "center_left_far": [568.579102, 230.583801, 496.918274, -88.703492, 0.498301, -161.117279],
    "center_right_far": [431.683014, -326.67807, 519.202881, -92.135051, -3.682801, -24.985028],
    "top_center_far": [279.753265, 5.682115, 759.225586, -108.944201, -5.107804, -91.658064],
    # furthest reach
    "center_center_super_far": [132.933121, 5.681428, 552.347168, -91.647006, -3.493209, -91.356459],
    "center_center_super_far_down": [132.933136, 5.68113, 552.347107, -146.378283, -3.126172, -87.933265],
    "top_center_super_far": [132.93309, 5.681316, 702.554382, -91.889883, -3.498881, -91.341677],
    "top_center_super_far_down": [132.93309, 5.681316, 702.554382, -154.184432, -2.816775, -87.528012]
}

scan_test = ["center_center", "top_center", "center_center"]

scan = [
    "center_center", # start
    # close
    "top_center_close", 
    "center_center_close", "center_left_close", # go left
    "center_center_close", "center_right_close", # go right
    "center_center_close",  
    "top_center_close", "center_left_close", # swoop left
    "top_center_close", "center_right_close", # swoop right
    "top_center_close",
    # mid
    "top_center_mid", 
    "center_center_mid", "center_left_mid", # go left
    "center_center_mid", "center_right_mid", # go right
    "center_center_mid",  
    "top_center_mid", "center_left_mid", # swoop left
    "top_center_mid", "center_right_mid", # swoop right
    "top_center_mid",
    # center    
    "top_center", 
    "center_center", "center_left", # go left
    "center_center", "center_right", # go right
    "center_center",  
    "top_center", "center_left", # swoop left
    "top_center", "center_right", # swoop right
    "top_center",
    # center look up / down
    "center_center", "center_center_up", 
    "center_center", "center_center_down",
    "center_center",
    # far
    "top_center_far", 
    "center_center_far", "center_left_far", # go left
    "center_center_far", "center_right_far", # go right
    "center_center_far",  
    "top_center_far", "center_left_far", # swoop left
    "top_center_far", "center_right_far", # swoop right
    "top_center_far",
    # super far - look down
    "center_center_super_far", "center_center_super_far_down", 
    "center_center_super_far",
    "top_center_super_far", "top_center_super_far_down",
    "top_center_super_far",
    # back to center
    "center_center"
]

SPEED = 50
PAUSE = 1 # sec

#
# progress of scanning
#
if len(sys.argv) >= 2:
    scan_name = sys.argv[1] # name of this scan provided on the command line
else: # default to datetime
    scan_name = "scan_{}".format(datetime.datetime.now())
progress = {"name": scan_name, "progress": []}

# start
progress["start"] = str(datetime.datetime.now())
right_robot.pprint("--- start ---")

# scanning - scan_test
for i, move in enumerate(scan):
    # record progress
    progress["progress"].append({
        "i": i,
        "move": move,
        "current_pos": left_robot._arm.get_position(),
        "datetime": str(datetime.datetime.now())
    })
    right_robot.pprint("--- %s ---" % move.upper())
    right_robot.linear_move([pos[move]], speed=SPEED)

    # maybe pause
    time.sleep(PAUSE)
    
# end
progress["end"] = str(datetime.datetime.now())

# dump progress
with open("scan_{}.json".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")), 'w') as fd:
    json.dump(progress,fd)

