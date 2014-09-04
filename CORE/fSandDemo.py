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
# brainType == "ifelse" for comparing with Q


def step():
    state = box.oneStep(draw=True, brainType=brainType).getStatus()
    agent_state = (item for item in state if item["class"] == "blockplayer").next()
    #print agent_state
    features = Features.get(agent_state)
    return features

# Init sandbox
delay = 0.0  # Delay for slow motion in debugging
box = allBox()  # Sandbox creating
a = box.getPlayer().actions  # Get list of actions
f = Features.get(box.getPlayer().statusreport())  # Get start state features
controller = Controll(a, f, report=True, rms=0.9)  # Q controller

# Loading model
file_type = ".npy"
f = "./W_final_wd_stoper" + file_type
controller.W = np.load(f)
print "\n", controller.W, "\n"

# Main
while True:
    features = step()
    if brainType is None:
        Q1, F1 = controller.oneStep(features)
        """
        if F1[18] + F1[19] == 0 and F1[22] == 0:
            Q1 = Q1 * np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0]) + np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0])
        """
        print Q1, F1[18] + F1[19]
        act_code = np.argmax(Q1)
        print act_code
        box.getPlayer().actions[act_code]()
    time.sleep(delay)


# ---------------------------------------------------------------------#