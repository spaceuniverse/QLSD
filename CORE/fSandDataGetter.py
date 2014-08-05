# ---------------------------------------------------------------------# IMPORTS


import sys
import pygame
import numpy as np
from numpy import *
from fSandBox import *
from fSandFun import *
import time


#---------------------------------------------------------------------# MAIN

delay = 0.0

box = allBox()

while True:
    #if sys.stdin.read(1):
    if True:
        state = box.oneStep(draw=True, brainType="ifelse").getStatus()
        agent_state = (item for item in state if item["class"] == "blockplayer").next()
        #print Features.get(agent_state)
        time.sleep(delay)


#---------------------------------------------------------------------#