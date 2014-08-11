# ---------------------------------------------------------------------# IMPORTS


import numpy as np
from fSandFun import *


# ---------------------------------------------------------------------# MAIN


class Controll(object):
    def __init__(self, actions, features, report=False):
        #self.W = np.random.rand(len(features), len(actions))
        self.W = np.zeros((len(features), len(actions)))
        if report:
            print self.W.shape

    def oneStep(self, features):
        features = features.reshape(-1, 1)
        Q = np.sum(self.W * features, axis=0)
        return Q, features

    def twoStep(self, features, featuresold, act_code, gamma=0.6):
        features = features.reshape(-1, 1)
        reward = Rewards.get(features, featuresold)
        Q = reward + gamma * np.sum(self.W[:, act_code] * features.T)
        return Q, features

    def wUpdate(self, Q1, Q2, F1, act_code, alpha=0.1):
        self.W[:, act_code] = self.W[:, act_code] + alpha * (Q2 - Q1[act_code]) * F1.T
        print "-------------------->", np.sum(self.W)


# ---------------------------------------------------------------------#