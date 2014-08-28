# ---------------------------------------------------------------------# IMPORTS


import numpy as np
from fSandFun import *


# ---------------------------------------------------------------------# MAIN


class Controll(object):
    def __init__(self, actions, features, report=False, rms=False):
        self.report = report
        # Randon W
        #self.W = np.random.rand(len(features), len(actions))
        # Zeros W
        self.W = np.zeros((len(features), len(actions)))
        self.rms = rms
        if self.rms:
            self.mms = np.ones((len(features), len(actions)))
        if self.report:
            print self.W.shape

    def __wNormalize__(self, wfn):  # Could be static
        fmax = np.abs(np.max(wfn))
        fmin = np.abs(np.min(wfn))
        m = np.maximum(fmax, fmin)
        if m == 0.0:
            m = 1.0
        koef = 1.0 / m
        wfn = wfn * koef
        return wfn

    def __updateMms__(self, derivative, act_code):
        self.mms[:, act_code] = (self.rms * self.mms[:, act_code] + (1.0 - self.rms) * (derivative ** 2)) * (derivative != 0) + self.rms * (derivative == 0)
        self.mms[:, act_code] = np.clip(self.mms[:, act_code], 1e-20, 1e+20)

    def oneStep(self, features):
        features = features.reshape(-1, 1)
        Q = np.sum(self.W * features, axis=0)
        return Q, features

    def twoStep(self, features, featuresold, act_code, gamma=0.9):
        features = features.reshape(-1, 1)
        reward = Rewards.get(features, featuresold)
        Q = reward + gamma * np.sum(self.W[:, act_code] * features.T)
        if self.report:
            print "------------------------ Reward --->", reward
        return Q, features

    def wUpdate(self, Q1, Q2, F1, act_code, alpha=0.1):
        print Q2, Q1[act_code], F1.T
        derivative = (Q2 - Q1[act_code]) * F1.T
        print derivative, derivative.shape
        if self.rms:
            self.__updateMms__(derivative, act_code)
            updater = alpha * derivative / np.sqrt(self.mms[:, act_code])
        else:
            updater = alpha * derivative  # -
        self.W[:, act_code] = self.W[:, act_code] + updater
        print self.mms[:, act_code]
        print updater, updater.shape
        if self.report:
            print "------------------------ Sum(W) --->", np.sum(self.W)


# ---------------------------------------------------------------------#