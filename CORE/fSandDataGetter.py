# ---------------------------------------------------------------------# IMPORTS


import time
import pygame
import numpy as np
from numpy import *
from fSandBox import *
from fSandFun import *
from fSandController import *


# ---------------------------------------------------------------------# MAIN


# Init sandbox
delay = 0.0
box = allBox()
actions = box.getPlayer().actions
features = Features.get(box.getPlayer().statusreport())
controller = Controll(actions, features, report=True)


# Main step
# brainType == "ifelse" for comparing with Q
while True:
    if True:
        state = box.oneStep(draw=True, brainType=None).getStatus()
        agent_state = (item for item in state if item["class"] == "blockplayer").next()
        features = Features.get(agent_state)
        time.sleep(delay)


# ---------------------------------------------------------------------#