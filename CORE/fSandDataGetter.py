# ---------------------------------------------------------------------# IMPORTS


import sys
import pygame
import numpy as np
from numpy import *
from fSandBox import *
from fSandFun import *
from fSandController import *
import time


# ---------------------------------------------------------------------# MAIN
# brainType == "ifelse" for comparing with Q


delay = 0.0
box = allBox()

while True:
    if True:
        state = box.oneStep(draw=True, brainType=None).getStatus()
        agent_state = (item for item in state if item["class"] == "blockplayer").next()
        features = Features.get(agent_state)
        print features
        time.sleep(delay)


# ---------------------------------------------------------------------#