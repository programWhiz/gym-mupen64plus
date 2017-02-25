from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import array
import os
import signal
import subprocess
import threading
import time
import pygame
from termcolor import cprint

import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym_mario_kart.envs.mupen64plus_env import Mupen64PlusEnv, Config, INTERNAL_STATE, IMAGE_HELPER

import numpy as np

import wx
wx.App()

###############################################
class MarioKartConfig:

    DEFAULT_STEP_REWARD = -1
    END_DETECTION_REWARD_REFUND = 215

    END_EPISODE_THRESHOLD = 30

    BLACK_PIXEL = (0, 0, 0)

    PLAYER_ROW = 1
    PLAYER_COL = 1

    MAP_SERIES = 0
    MAP_CHOICE = 0


###############################################
class MarioKartEnv(Mupen64PlusEnv):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(MarioKartEnv, self).__init__('/home/brian/Programming/TensorKart/marioKart.n64')
        
    def _get_reward(self, episode_over):
        #cprint('Get Reward called!','red')
        if episode_over:
            # Refund the reward lost in the frames following the race finish until end episode detection
            return MarioKartConfig.END_DETECTION_REWARD_REFUND
        else:
            # Currently just -1 per step
            return MarioKartConfig.DEFAULT_STEP_REWARD

    def _evaluate_end_state(self):
        #cprint('Evaluate End State called!','red')
        pix_arr = INTERNAL_STATE.pixel_array

        upper_left = IMAGE_HELPER.GetPixelColor(pix_arr, 19, 19)
        upper_right = IMAGE_HELPER.GetPixelColor(pix_arr, 620, 19)
        bottom_left = IMAGE_HELPER.GetPixelColor(pix_arr, 19, 460)
        bottom_right = IMAGE_HELPER.GetPixelColor(pix_arr, 620, 460)

        if upper_left == upper_right == bottom_left == bottom_right == MarioKartConfig.BLACK_PIXEL:
            INTERNAL_STATE.end_episode_confidence += 1
        else:
            INTERNAL_STATE.end_episode_confidence = 0

        if INTERNAL_STATE.end_episode_confidence > MarioKartConfig.END_EPISODE_THRESHOLD:
            INTERNAL_STATE.is_end_episode = True

        return INTERNAL_STATE.is_end_episode

    def _navigate_menu(self):
        frame = 0
        cur_row = 0
        cur_col = 0

        while frame < 284:
            action = Config.NOOP

            #  10 - Nintendo screen
            #  80 - Mario Kart splash screen
            # 120 - Select number of players
            # 125 - Select GrandPrix or TimeTrials
            # 130 - Select TimeTrials
            # 132 - Select Begin
            # 134 - OK
            # 160 - Select player
            # 162 - OK
            # 201 - Select map series
            # 230 - Select map choice
            # 232 - OK
            # 284 - <Level loaded; turn over control>
            if frame in [10, 80, 120, 130, 132, 134, 160, 162, 202, 230, 232]:
                action = Config.A_BUTTON
            elif frame in [125]:
                action = Config.JOYSTICK_DOWN

            # Frame 150 is the 'Player Select' screen
            if frame == 150:
                print('Player row: ', str(MarioKartConfig.PLAYER_ROW))
                print('Player col: ', str(MarioKartConfig.PLAYER_COL))

                if cur_row != MarioKartConfig.PLAYER_ROW:
                    action = Config.JOYSTICK_DOWN
                    cur_row += 1

            if frame in range(151, 156) and frame % 2 == 0:
                if cur_col != MarioKartConfig.PLAYER_COL:
                    action = Config.JOYSTICK_RIGHT
                    cur_col += 1

            # Frame 195 is the 'Map Select' screen
            if frame == 195:
                cur_row = 0
                cur_col = 0
                print('Map series: ', str(MarioKartConfig.MAP_SERIES))
                print('Map choice: ', str(MarioKartConfig.MAP_CHOICE))

            if frame in range(195, 202) and frame %2 == 0:
                if cur_col != MarioKartConfig.MAP_SERIES:
                    action = Config.JOYSTICK_RIGHT
                    cur_col += 1

            if frame in range(223, 230) and frame %2 == 0:
                if cur_row != MarioKartConfig.MAP_CHOICE:
                    action = Config.JOYSTICK_DOWN
                    cur_row += 1

            if action != Config.NOOP:
                print('Frame ', str(frame), ': ', str(action))

            self._take_action(action)
            frame += 1