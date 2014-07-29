# ---------------------------------------------------------------------# IMPORTS


import sys
import pygame
import numpy as np
from numpy import *
from fSandBox import *
import time


#---------------------------------------------------------------------# MAIN

delay = 0.0

box = allBox()

while True:
    # if sys.stdin.read(1):
    if True:
        state = box.oneStep(draw=True).getStatus()
        time.sleep(delay)
        # print state


#---------------------------------------------------------------------#