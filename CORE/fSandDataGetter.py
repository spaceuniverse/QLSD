# ---------------------------------------------------------------------# IMPORTS


import time
import pygame
import numpy as np
from numpy import *
from fSandBox import *
from fSandFun import *
from fSandController import *


# ---------------------------------------------------------------------# MAIN


# brainType == "ifelse" for comparing with Q
def step():
    state = box.oneStep(draw=True, brainType=None).getStatus()
    agent_state = (item for item in state if item["class"] == "blockplayer").next()
    features = Features.get(agent_state)
    return features


# Init sandbox
epsilon = 0.5
delay = 0.0
box = allBox()
a = box.getPlayer().actions
al = len(a)
f = Features.get(box.getPlayer().statusreport())
controller = Controll(a, f, report=True)
i = 0


# Main step
while True:
    if i < 2000:
        features = step()
        Q1, F1 = controller.oneStep(features)
        if np.random.rand(1.0) < epsilon:
            act_code = np.argmax(Q1)
        else:
            act_code = np.random.randint(al)
            #box.getPlayer().randomAction()
        box.getPlayer().actions[act_code]()
        features = step()
        Q2, F2 = controller.twoStep(features, act_code)
        controller.wUpdate(Q1, Q2, F1, act_code)
        print i
        i += 1
        time.sleep(delay)
    else:
        features = step()
        Q1, F1 = controller.oneStep(features)
        act_code = np.argmax(Q1)
        box.getPlayer().actions[act_code]()
        time.sleep(delay)


# ---------------------------------------------------------------------#