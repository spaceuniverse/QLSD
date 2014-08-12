# ---------------------------------------------------------------------# IMPORTS


import time
import pygame
import numpy as np
from numpy import *
from fSandBox import *
from fSandFun import *
from fSandController import *


# ---------------------------------------------------------------------# MAIN
# Main file for sandbox, run it and enjoy

# brainType == "ifelse" for comparing with Q
def step():
    state = box.oneStep(draw=True, brainType=None).getStatus()
    agent_state = (item for item in state if item["class"] == "blockplayer").next()
    features = Features.get(agent_state)
    return features


# Init sandbox
epsilon = 0.6  # Chance of random or not action
delay = 0.0  # Delay for slow motion in debugging
box = allBox()  # Sandbox creating
a = box.getPlayer().actions  # Get list of actions
a_len = len(a)  # Get length of list of actions
f = Features.get(box.getPlayer().statusreport())  # Get start state features
controller = Controll(a, f, report=True)  # Q controller
i = 0  # Iterator
steps = 20000  # Number of training steps
epsilon_inc = (1.0 - epsilon) / steps


# Main step
while True:
    if i < steps:
        features = step()
        Q1, F1 = controller.oneStep(features)
        if np.random.rand(1.0) < epsilon:
            act_code = np.argmax(Q1)
        else:
            act_code = np.random.randint(a_len)
        box.getPlayer().actions[act_code]()
        features = step()
        Q2, F2 = controller.twoStep(features, F1, act_code)
        controller.wUpdate(Q1, Q2, F1, act_code)
        print i, epsilon, act_code
        i += 1
        epsilon += epsilon_inc
        time.sleep(delay)
    else:
        features = step()
        Q1, F1 = controller.oneStep(features)
        act_code = np.argmax(Q1)
        print act_code
        box.getPlayer().actions[act_code]()
        time.sleep(delay)


# ---------------------------------------------------------------------#