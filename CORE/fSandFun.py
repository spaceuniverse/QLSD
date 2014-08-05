# ---------------------------------------------------------------------# IMPORTS


import numpy as np


# ---------------------------------------------------------------------# MAIN


class Features(object):
    @staticmethod
    def get(objState):
        if objState["class"] == "blockplayer":
            vector = np.reshape(objState["environment"], 18)  # 18 is total length of 2*3*3 matrix
        else:
            vector = None
        return vector


# ---------------------------------------------------------------------#