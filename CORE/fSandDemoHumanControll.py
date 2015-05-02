# ---------------------------------------------------------------------# Description
# Agent human decisions (Key pressed)
#
# Keys:
# |q| |w| |e|
# |a| |s| |d|
# |z| |x| |c|  |space|
#
# w a s d - up left down right
# space - stop
#
# Important:
# |x| and |s| should be replaced for auto mode when training
# ---------------------------------------------------------------------# IMPORTS


import time
import pygame
import numpy as np
from numpy import *
from fSandBox import *
from fSandFun import *
from fSandController import *


# ---------------------------------------------------------------------# MAIN
brainType = None
# brainType == "ifelse" (Builtin function)


def step():
    box.oneStep(draw=True, brainType=brainType).getStatus()

# Init sandbox
delay = 0.03  # Delay for slow motion in debugging
box = allBox()  # Sandbox creating
a = box.getPlayer().actions  # Get list of actions
a_len = len(a)  # Get length of list of actions
# "Steam flow" [on | off] for first agent
box.getPlayer().speed = np.array([0, 0, 0, 0, 0])

# Main
while True:
    step()
    key = pygame.key.get_pressed()
    keys = [key[pygame.K_q], key[pygame.K_w], key[pygame.K_e], key[pygame.K_a], key[pygame.K_x], key[pygame.K_d],
            key[pygame.K_z], key[pygame.K_s], key[pygame.K_c], key[pygame.K_SPACE]]  # K_x and K_s place changed
    print keys
    if np.sum(keys) > 0:
        act_code = np.argmax(keys)
    else:
        act_code = 9  # Do nothing 4 or Stop 9
    print act_code
    box.getPlayer().actions[act_code]()
    time.sleep(delay)


# ---------------------------------------------------------------------#