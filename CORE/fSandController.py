# ---------------------------------------------------------------------# IMPORTS


import numpy as np


# ---------------------------------------------------------------------# MAIN


class Controll(object):
    def __init__(self, actions, features, report=False):
        self.W = np.random.rand(len(features), len(actions))
        if report:
            print self.W.shape

    def oneStep(self, features, report=False):
        features = features.reshape(-1, 1)
        if report:
            print features.shape
        out = self.W * features
        return out


# ---------------------------------------------------------------------#