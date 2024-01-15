#!/usr/bin/env python3

"""
Start the robots for experiment 1
"""

import os
import sys
import time
import datetime

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

# left
pinch_pos = [479.599762, 44.4063, 839.999634, 179.999963, -69.999973, 0]
left_robot.linear_move([pinch_pos], wait=False)

# right
center_center_start = [390.826996, -2.239847, 519.205505, -103.282518, -3.548614, -91.735356]
right_robot.linear_move([center_center_start], wait=False)

