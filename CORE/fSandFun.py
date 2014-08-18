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
            vector = np.append(vector, np.reshape(objState["environment"] / 10.0, 18))  # 18 is total length of 2*3*3 matrix of environment; *17
            vector = np.append(vector, np.sum(objState["environment"][0] / 80.0))  # Hit num; 80 is idea that no more than 10 obj in one zone; *18 *0
            vector = np.append(vector, np.sum(objState["environment"][1] / 80.0))  # Heal num; *19 *1
            vector = np.append(vector, np.sum(objState["environment_dist"][0] / 800.0))  # Hit dist; max range for 1 obj is 100 and 8 zones; *20 *2
            vector = np.append(vector, np.sum(objState["environment_dist"][1] / 800.0))  # Heal dist; *21 *3
            vector = np.append(vector, objState["ignition"] / 22.0)  # 22 max value of ignition; *22 *4
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
        if objVector[22] > 0:
            reward -= 500.0 * objVector[22]
        if objVector[22] == 0:
            reward += 50
        # Reward for hit dist
        if objVector[20] < objVectorOld[20] and objVector[18] == objVectorOld[18]:
            reward -= 100.0
        if objVector[20] > objVectorOld[20] and objVector[18] == objVectorOld[18]:
            reward += 100.0
        # Reward for heal dist
        if objVector[21] > objVectorOld[21] and objVector[19] == objVectorOld[19]:
            reward -= 100.0
        if objVector[21] < objVectorOld[21] and objVector[19] == objVectorOld[19]:
            reward += 100.0
        return reward


# ---------------------------------------------------------------------#