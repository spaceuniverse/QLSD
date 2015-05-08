# ---------------------------------------------------------------------# IMPORTS


import time
import numpy as np
from fSandBox import *
from fSandWrapper import *
from PIL import Image


# ---------------------------------------------------------------------# MAIN

box = allBox()  # Sandbox object
data = GetData()  # Wrapper object

while True:
    state = box.oneStep(draw=True, brainType=None).getStatus()
    agent_state = (item for item in state if item["class"] == "blockplayer").next()
    img = box.img.resize((84, 84), resample=0)
    screen = np.array(img)
    print "+", agent_state["plus"], "-", agent_state["minus"]
    # img.save("../../img/scr/tst/main-tests.jpg", "JPEG", quality=100)
    # print screen.shape
    time.sleep(0.07)


# ---------------------------------------------------------------------#