# ---------------------------------------------------------------------# IMPORTS


import numpy as np


# ---------------------------------------------------------------------# MAIN


class Features(object):
    @staticmethod
    def normal(wfn):
        fmax = np.max(wfn)
        if fmax == 0.0:
            fmax = 1.0
        koef = 1.0 / fmax
        wfn = wfn * koef
        return wfn

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
            vector = np.append(vector, np.reshape(objState["environment"] / 10.0, 18))  # 18 is total length of 2*3*3 matrix of environment; *17 /10.0
            vector = np.append(vector, np.sum(objState["environment"][0]) / 100.0)  # Hit num; 80 is idea that no more than 10 obj in one zone; *18 *0 /80.0
            vector = np.append(vector, np.sum(objState["environment"][1]) / 100.0)  # Heal num; *19 *1 /80.0
            vector = np.append(vector, np.sum(objState["environment_dist"][0]) / 1000.0)  # Hit dist; max range for 1 obj is 100 and 8 zones; *20 *2 /800.0
            vector = np.append(vector, np.sum(objState["environment_dist"][1]) / 1000.0)  # Heal dist; *21 *3 /800.0
            vector = np.append(vector, objState["ignition"] / 100.0)  # 22 max value of ignition; *22 *4 /22.0
            #vector = Features.normal(vector)
            #print "Vector: ", vector
        else:
            vector = None
        return vector


class Rewards(object):
    @staticmethod
    def get(objVector, objVectorOld):
        reward = 0.0
        rs = 0.0
        rb = 0.0
        rh = 0.0
        # Every square scan
        #for i in xrange(9):
        #    if objVector[i] > 0:
        #        reward -= 100 * objVector[i]
        #for i in xrange(9, 18):
        #    if objVector[i] > 0:
        #        reward += 100 * objVector[i]
        # More complex
        # Reward for speed
        if objVector[22] > 0:  # and objVector[18] == 0 and objVector[19] == 0
            reward -= 100.0 * objVector[22]  # 100 500
            rs -= 100.0 * objVector[22]  # 100 500
        #if objVector[22] == 0:
        #    reward += 10.0
        #    rs += 10.0
        print "RSpeed: ", rs
        # Reward for hit dist
        if objVector[20] < objVectorOld[20] and objVector[18] == objVectorOld[18]:
            reward -= 100000.0 * (np.abs(objVectorOld[20] - objVector[20]))
            rb -= 100000.0 * (np.abs(objVectorOld[20] - objVector[20]))
        if objVector[20] > objVectorOld[20] and objVector[18] == objVectorOld[18]:
            reward += 100000.0 * (np.abs(objVector[20] - objVectorOld[20]))
            rb += 100000.0 * (np.abs(objVector[20] - objVectorOld[20]))
        print "RBullet: ", rb
        # Reward for heal dist
        if objVector[21] >= objVectorOld[21] and objVector[19] == objVectorOld[19]:
            reward -= 100000.0 * (np.abs(objVector[21] - objVectorOld[21]))
            rh -= 100000.0 * (np.abs(objVector[21] - objVectorOld[21]))
        if objVector[21] < objVectorOld[21] and objVector[19] == objVectorOld[19]:
            reward += 100000.0 * (np.abs(objVectorOld[21] - objVector[21]))
            rh += 100000.0 * (np.abs(objVectorOld[21] - objVector[21]))
        print "RHeal: ", rh
        print reward, rs + rb + rh
        return reward


# ---------------------------------------------------------------------#