# ---------------------------------------------------------------------# IMPORTS


import numpy as np


# ---------------------------------------------------------------------# MAIN


class Features(object):
    @staticmethod
    def get(objState):
        if objState["class"] == "blockplayer":
            # Other features
            #vector = np.append(vector, objState["health"] / 100.0)
            #vector = np.append(vector, int(objState["live"]))
            #vector = np.append(vector, int(objState["plus"]))
            #vector = np.append(vector, int(objState["minus"]))
            # Features
            vector = np.array([])
            #vector = np.append(vector, np.reshape(objState["environment"] / 10.0, 18))  # 18 is total length of 2*3*3 matrix of environment 17
            """
            vector = np.append(vector, np.sum(objState["environment"][0] / 10.0))  # Hit num 18 0
            vector = np.append(vector, np.sum(objState["environment"][1] / 10.0))  # Heal num 19 1
            vector = np.append(vector, np.sum(objState["environment_dist"][0] / 100.0))  # Hit dist 20 2
            vector = np.append(vector, np.sum(objState["environment_dist"][1] / 100.0))  # Heal dist 21 3
            """
            vector = np.append(vector, objState["ignition"] / 22.0)  # 22 max value of ignition 22 4
        else:
            vector = None
        return vector


class Rewards(object):
    @staticmethod
    def get(objVector, objVectorOld):
        reward = 0
        # Every square scan
        #for i in xrange(9):
        #    if objVector[i] > 0:
        #        reward -= 100 * objVector[i]
        #for i in xrange(9, 18):
        #    if objVector[i] > 0:
        #        reward += 100 * objVector[i]
        # More complex
        # Reward for speed
        if objVector[0] > 0:
            reward -= 100.0 * objVector[0]
        """
        if objVector[0] == 0:
            reward += 100
        """
        # Reward for hit
        """
        if objVector[2] < objVectorOld[2] and objVector[0] == objVectorOld[0]:
            reward -= 10.0
        if objVector[2] > objVectorOld[2] and objVector[0] == objVectorOld[0]:
            reward += 10.0
        """
        # Reward for heal
        """
        if objVector[3] > objVectorOld[3] and objVector[1] == objVectorOld[1]:
            reward -= 10.0
        if objVector[3] < objVectorOld[3] and objVector[1] == objVectorOld[1]:
            reward += 10.0
        """
        return reward


# ---------------------------------------------------------------------#