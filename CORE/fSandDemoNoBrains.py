# ---------------------------------------------------------------------# Description
# Agent no making decisions (Just sandbox steps | Random | Builtin)
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
delay = 0.0  # Delay for slow motion in debugging
mode = None  # or "Random"
box = allBox()  # Sandbox creating
a = box.getPlayer().actions  # Get list of actions
a_len = len(a)  # Get length of list of actions

# Main
while True:
    step()
    if mode == "Random":
        act_code = np.random.randint(a_len)
        box.getPlayer().actions[act_code]()
    time.sleep(delay)


# ---------------------------------------------------------------------#