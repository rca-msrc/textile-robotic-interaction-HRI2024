"""
Robot controller
"""

import sys
import math
import time
import queue
import datetime
import random
import traceback
import threading

# xarm api
# from xarm import version
# from xarm.wrapper import XArmAPI

class Robot(object):
    """Robot Main Class"""
    def __init__(self, robot, **kwargs):
        self.alive = True
        self._arm = robot
        self._tcp_speed = 100
        self._tcp_acc = 2000
        self._angle_speed = 20
        self._angle_acc = 500
        self._variables = {}
        self._robot_init()

    # Robot init
    def _robot_init(self):
        self._arm.clean_warn()
        self._arm.clean_error()
        self._arm.motion_enable(True)
        self._arm.set_mode(0)
        self._arm.set_state(0)
        time.sleep(1)
        self._arm.register_error_warn_changed_callback(self._error_warn_changed_callback)
        self._arm.register_state_changed_callback(self._state_changed_callback)
        if hasattr(self._arm, 'register_count_changed_callback'):
            self._arm.register_count_changed_callback(self._count_changed_callback)

    # Register error/warn changed callback
    def _error_warn_changed_callback(self, data):
        if data and data['error_code'] != 0:
            self.alive = False
            self.pprint('err={}, quit'.format(data['error_code']))
            self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)

    # Register state changed callback
    def _state_changed_callback(self, data):
        if data and data['state'] == 4:
            self.alive = False
            self.pprint('state=4, quit')
            self._arm.release_state_changed_callback(self._state_changed_callback)

    # Register count changed callback
    def _count_changed_callback(self, data):
        if self.is_alive:
            self.pprint('counter val: {}'.format(data['count']))

    def _check_code(self, code, label):
        if not self.is_alive or code != 0:
            self.alive = False
            ret1 = self._arm.get_state()
            ret2 = self._arm.get_err_warn_code()
            self.pprint('{}, code={}, connected={}, state={}, error={}, ret1={}. ret2={}'.format(label, code, self._arm.connected, self._arm.state, self._arm.error_code, ret1, ret2))
        return self.is_alive

    @staticmethod
    def pprint(*args, **kwargs):
        try:
            stack_tuple = traceback.extract_stack(limit=2)[0]
            print('[{}][{}] {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), stack_tuple[1], ' '.join(map(str, args))))
        except:
            print(*args, **kwargs)

    @property
    def is_alive(self):
        if self.alive and self._arm.connected and self._arm.error_code == 0:
            if self._arm.state == 5:
                cnt = 0
                while self._arm.state == 5 and cnt < 5:
                    cnt += 1
                    time.sleep(0.1)
            return self._arm.state < 4
        else:
            return False

    def linear_move(self, positions, speed=100, accel=10000, wait=True):
        try:
            # Linear Motion
            self._tcp_speed = speed
            self._tcp_acc = accel
            if not self.is_alive:
                self.pprint('Robot is already alive: %s' % self.alive)
            for i,pos in enumerate(positions):
                self.pprint('Move %3.d: %s' % (i,pos))
                code = self._arm.set_position(*pos, speed=self._tcp_speed, mvacc=self._tcp_acc, radius=-1.0, wait=wait)
                self._check_code(code, 'set_position')
                self.pprint('(%d) ----> %s' % self._arm.get_position())
        except Exception as e:
            self.pprint('MainException: {}'.format(e))
        self.alive = False
        self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)
        self._arm.release_state_changed_callback(self._state_changed_callback)
        if hasattr(self._arm, 'release_count_changed_callback'):
            self._arm.release_count_changed_callback(self._count_changed_callback)
     
    def set_gripper(self, position=600, speed=100):
        code = self._arm.set_gripper_mode(0)
        self._check_code(code, 'set_gripper_mode')
        code = self._arm.set_gripper_enable(True)
        self._check_code(code, 'set_gripper_enable')
        code = self._arm.set_gripper_speed(speed)
        self._check_code(code, 'set_gripper_speed')
        code = self._arm.set_gripper_position(position, wait=True)
        self._check_code(code, 'set_gripper_position')
        
    def open_gripper(self):
        self.set_gripper(100, 3000)

    def close_gripper(self):
        self.set_gripper(-1, 1000)

    def test_square(self):
        try:
            # Linear Motion
            self._tcp_speed = 200
            self._tcp_acc = 10000
            for i in range(int(10)):
                if not self.is_alive:
                    break
                code = self._arm.set_position(*[300.0, 100.0, 100.0, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=-1.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                code = self._arm.set_position(*[300.0, 100.0, 300.0, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=-1.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                code = self._arm.set_position(*[300.0, -100.0, 300.0, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=-1.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                code = self._arm.set_position(*[300.0, -100.0, 100.0, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=-1.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
        except Exception as e:
            self.pprint('MainException: {}'.format(e))
        self.alive = False
        self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)
        self._arm.release_state_changed_callback(self._state_changed_callback)
        if hasattr(self._arm, 'release_count_changed_callback'):
            self._arm.release_count_changed_callback(self._count_changed_callback)