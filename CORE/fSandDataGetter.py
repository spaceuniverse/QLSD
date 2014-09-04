# ---------------------------------------------------------------------# IMPORTS


import time
import pygame
import numpy as np
from numpy import *
from fSandBox import *
from fSandFun import *
from fSandController import *


# ---------------------------------------------------------------------# MAIN
# Main file for sandbox, run it and enjoy ^_^
# ---------------------------------------------------------------------#

# brainType == "ifelse" for comparing with Q
def step():
    state = box.oneStep(draw=True, brainType=None).getStatus()
    agent_state = (item for item in state if item["class"] == "blockplayer").next()
    features = Features.get(agent_state)
    return features

# Init sandbox
epsilon = 0.7  # Chance of random or not action
delay = 0.0  # Delay for slow motion in debugging
box = allBox()  # Sandbox creating
a = box.getPlayer().actions  # Get list of actions
a_len = len(a)  # Get length of list of actions
f = Features.get(box.getPlayer().statusreport())  # Get start state features
controller = Controll(a, f, report=True, rms=0.9)  # Q controller
i = 0  # Iterator
steps = 2000000  # Number of training steps 100000
epsilon_inc = (1.0 - epsilon) / steps

# Loading model
"""
file_type = ".npy"
f = "./W" + file_type
controller.W = np.load(f)
"""
print "\n", controller.W, "\n"

# Main
while True:
    #features = step()
    if i < steps:
        # First step
        features = step()
        Q1, F1 = controller.oneStep(features)
        dsg = np.random.rand(1.0)[0]
        if dsg < epsilon:
            act_code = np.argmax(Q1)
        else:
            act_code = np.random.randint(a_len)
        box.getPlayer().actions[act_code]()
        # Second step
        features = step()
        #features = step()
        # Added more steps
        Q2, F2 = controller.twoStep(features, F1, act_code)
        controller.wUpdate(Q1, Q2, F1, act_code)
        # Updates
        print i, dsg, epsilon, act_code, "\n"
        i += 1
        epsilon += epsilon_inc
        time.sleep(delay)
    elif i == steps:
        f = "./W_final_wd_2"
        np.save(f, controller.W)
        print "\n", controller.W, "\n"
        print "\nSAVED\n"
        i += 1
    else:
        features = step()
        Q1, F1 = controller.oneStep(features)
        act_code = np.argmax(Q1)
        print act_code
        box.getPlayer().actions[act_code]()
        time.sleep(delay)


# ---------------------------------------------------------------------#