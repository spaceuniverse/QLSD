# ---------------------------------------------------------------------#

import SandBoxTest as sb
import numpy as np
import sys
from FUN import *

#---------------------------------------------------------------------#


#---------------------------------------------------------------------#
Box = sb.Box()
P = Box.getPlayer()
actions = [P.incSpeedToUP, P.incSpeedToRIGHT, P.incSpeedToLEFT, P.incSpeedToDOWN]
A = ['UP', 'RIGHT', 'LEFT', 'DOWN']

count = 0
steps = 30000

file_type = '.npy'
f = './W' + file_type
W = np.load(f)

while 1:
    #if sys.stdin.read(1):
    if 1:
        state = Box.getStatus()
        features = getFeatures(state, P).reshape(-1, 1)

        Q = np.sum(W * features, axis=0)

        act_code = np.argmax(Q)
        act = actions[act_code]
        act()
        '''
        if features[7]:
            P.incSpeedToDOWN()
        if features[8]:
            P.incSpeedToLEFT()
        if features[9]:
            P.incSpeedToRIGHT()
        if features[10]:
            P.incSpeedToUP()
        '''
        state = Box.oneStep(draw=True)

        if not P.live:
            P = Box.getPlayer()
            actions = [P.incSpeedToUP, P.incSpeedToRIGHT, P.incSpeedToLEFT, P.incSpeedToDOWN]

        count += 1
        wall = [A[i] for i in range(4) if features[3 + i] == 1]
        bullet = [A[i] for i in range(4) if features[7 + i] == 1]
        heal = [A[i] for i in range(4) if features[11 + i] == 1]
        #print str(count) + '\n'\
        #      + 'Action: ' + A[act_code] + '\n'\
        #      + 'Wall: ' + str(wall) + '\n'\
        #      + 'Bullet: ' + str(bullet) + '\n'\
        #      + 'Healer: ' + str(heal) + '\n'\
        #      + 'Q: ' + str(Q[act_code]) + '\n'\
        #      + '-------'
        #if count > steps:
        #    break

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
