# ---------------------------------------------------------------------#
import sys
import pygame
import numpy as np
from numpy import *
from fSandBox import *
# import time
#---------------------------------------------------------------------#
box = allBox()
while True:
    # if sys.stdin.read(1):
    if True:
        state = box.oneStep(draw=True).getStatus()
        # time.sleep(0.1)
        # print state
        #---------------------------------------------------------------------#