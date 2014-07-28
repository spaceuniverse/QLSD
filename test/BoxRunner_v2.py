__author__ = 'rhrub'

import SandBoxTest as sb
import sys
from FUN import *
#---------------------------------------------------------------------#


#---------------------------------------------------------------------#
#[features, actions]
W = np.random.rand(15, 4)
alpha = 0.01
#---------------------------------------------------------------------#

Box = sb.Box()
P = Box.getPlayer()
actions = [P.incSpeedToUP, P.incSpeedToRIGHT, P.incSpeedToLEFT, P.incSpeedToDOWN]

count = 0
steps = 30000
epsilon = 0.7

while 1:
    #if sys.stdin.read(1):
    if 1:
        state = Box.getStatus()
        features = getFeatures(state, P).reshape(-1, 1)

        Q = np.sum(W * features, axis=0)
        #print features.shape, W.shape, Q.shape

        if np.random.rand(1) < epsilon:
            act_code = np.argmax(Q)
        else:
            act_code = np.random.randint(len(actions))

        act = actions[act_code]
        act()

        state = Box.oneStep(draw=True)
        features = getFeatures(state, P)

        featuresR = getFeaturesForReward(state, features)
        R = getReward(featuresR)

        newQ = np.sum(W[:, act_code] * features)

        derivative = (Q[act_code] - (R + newQ)) * features

        W[:, act_code] = W[:, act_code] - alpha * derivative


        if not P.live:
            P = Box.getPlayer()
            actions = [P.incSpeedToUP, P.incSpeedToRIGHT, P.incSpeedToLEFT, P.incSpeedToDOWN]

        count += 1
        print count
        if count > steps:
            break

        #dec epsilon to perform more optimal
        #if count > 50000:
        #    epsilon = 0.3

        #Noramlization
        if not count % 1000:
            f = './W'
            np.save(f, W)

print W






















'''
        if features[2]:
            P.incSpeedToDOWN()
        if features[3]:
            P.incSpeedToLEFT()
        if features[4]:
            P.incSpeedToRIGHT()
        if features[5]:
            P.incSpeedToUP()
'''