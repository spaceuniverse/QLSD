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
            vector = np.append(vector, objState["ignition"] / 22.0)  # 22 max value of ignition
        else:
            vector = None
        return vector


class Rewards(object):
    @staticmethod
    def get(objVector):
        reward = 0
        """
        for i in xrange(9):
            if objVector[i] > 0:
                reward -= 300 * objVector[i]
        for i in xrange(9, 18):
            if objVector[i] > 0:
                reward += 300 * objVector[i]
        """
        if objVector[22] > 0:
            reward -= 50 * objVector[22]
        if objVector[22] == 0:
            reward += 50
        return reward


# ---------------------------------------------------------------------#