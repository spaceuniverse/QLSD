# ---------------------------------------------------------------------# IMPORTS


import numpy as np


# ---------------------------------------------------------------------# MAIN


class Features(object):
    @staticmethod
    def get(objState):
        if objState["class"] == "blockplayer":
            vector = np.reshape(objState["environment"] / 10.0, 18)  # 18 is total length of 2*3*3 matrix of environment
            vector = np.append(vector, objState["health"] / 100.0)
            vector = np.append(vector, int(objState["live"]))
            vector = np.append(vector, int(objState["plus"]))
            vector = np.append(vector, int(objState["minus"]))
        else:
            vector = None
        return vector


# ---------------------------------------------------------------------#