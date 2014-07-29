import interface
import numpy as np
import time
import matplotlib.pyplot as plt
import random


class controller(object):
    def __init__(self, interface, discountFactor=0.99, learningRate=0.1, featureOrder=1, \
                 derivativeHistoryRec=3, plotHistory=None, combineTimeDate=False, rmsProp=False, mmsLimit=0.):

        self.interface = interface
        self.actions = ['doNothing', 'startServer1', 'startServer4', 'startServer10', 'stopServer1', 'stopServer4',
                        'stopServer10']
        self.discountFactor = discountFactor

        self.derivativeHistoryRec = derivativeHistoryRec
        self.plotHistory = plotHistory
        self.featureOrder = featureOrder
        self.combineTimeDate = combineTimeDate
        self.rmsProp = rmsProp
        self.learningRate = learningRate
        self.mmsLimit = mmsLimit

        self.serverPrice = 1
        self.prevCPULoad = []
        self.prevMemoryLoad = []
        self.prevRequests = []
        self.mms = []
        self.history = {'maxCPULoad': [], 'meanCPULoad': [], 'maxMemoryLoad': [], 'meanMemoryLoad': [],
                        'totalRequests': [], 'serversRunning': [], 'serversStarting': []}

        self.weights = self.__initializeWeights__()
        self.mms = self.__initializeMms__()

    def __initializeWeights__(self):
        state = self.getNextState()
        features = self.getFeatures(state)
        return [np.zeros(len(features)) for i in range(len(self.actions))]

    def __initializeMms__(self):
        return [np.ones(len(self.weights[i])) for i in range(len(self.actions))]

    def updateMms(self, derivative, actionId):
        self.mms[actionId] = (self.rmsProp * self.mms[actionId] + (1 - self.rmsProp) * (derivative ** 2)) * (
            derivative != 0) + self.rmsProp * (derivative == 0)
        self.mms[actionId] = self.mms[actionId] * (self.mms[actionId] >= self.mmsLimit) + self.mmsLimit * (
            self.mms[actionId] < self.mmsLimit)

    def getNextState(self):
        data = self.interface.getData()

        totalRequests = data['numberOfTotalRequests']
        self.prevRequests = np.append(self.prevRequests, totalRequests)
        if len(self.prevRequests) > self.derivativeHistoryRec * 2: self.prevRequests = np.delete(self.prevRequests, 0)

        # derivativeRequests = self.getDerivatives()

        serversStarting = data['numberOfServersStarting']
        weekend = int(data['weekEnd'])
        weekday = int(not (data['weekEnd']))
        serversRunning = data['numberOfServersRunning']
        maxCPU = max([i['cpuLoad'] for i in data['serverMetrics']])
        maxMemory = max([i['memoryUsage'] for i in data['serverMetrics']])
        meanCPU = np.mean([i['cpuLoad'] for i in data['serverMetrics']])
        meanMemory = np.mean([i['memoryUsage'] for i in data['serverMetrics']])

        startTimestamp = 1388559300236
        timestamp = data['timestamp']
        hour = (np.floor((timestamp - startTimestamp) / (1000. * 60. * 60.)) + 9) % 24

        if self.plotHistory is not None:
            self.history['meanCPULoad'].append(meanCPU)
            self.history['maxCPULoad'].append(maxCPU)
            self.history['meanMemoryLoad'].append(meanMemory)
            self.history['maxMemoryLoad'].append(maxMemory)
            self.history['totalRequests'].append(totalRequests)
            self.history['serversRunning'].append(serversRunning)
            self.history['serversStarting'].append(serversStarting)

            if len(self.history['meanCPULoad']) > self.plotHistory:
                self.history['meanCPULoad'] = self.history['meanCPULoad'][1:]
            if len(self.history['maxCPULoad']) > self.plotHistory:
                self.history['maxCPULoad'] = self.history['maxCPULoad'][1:]
            if len(self.history['meanMemoryLoad']) > self.plotHistory:
                self.history['meanMemoryLoad'] = self.history['meanMemoryLoad'][1:]
            if len(self.history['maxMemoryLoad']) > self.plotHistory:
                self.history['maxMemoryLoad'] = self.history['maxMemoryLoad'][1:]
            if len(self.history['totalRequests']) > self.plotHistory:
                self.history['totalRequests'] = self.history['totalRequests'][1:]
            if len(self.history['serversStarting']) > self.plotHistory:
                self.history['serversStarting'] = self.history['serversStarting'][1:]
            if len(self.history['serversRunning']) > self.plotHistory:
                self.history['serversRunning'] = self.history['serversRunning'][1:]

        return {'bias': 1, \
                'serversRunning': serversRunning, \
                'serversStarting': serversStarting, \
                # 'derivativeRequests':derivativeRequests, \
                'maxCPU': maxCPU, \
                'maxMemory': maxMemory, \
                'CPUOverload': (maxCPU > 1.) * (maxCPU - 1.), \
                'memoryOverload': (maxMemory > 0.8) * (maxMemory - 0.8), \
                'totalRequests': totalRequests, \
                '0am': 1. * (hour == 0), \
                '1am': 1. * (hour == 1), \
                '2am': 1. * (hour == 2), \
                '3am': 1. * (hour == 3), \
                '4am': 1. * (hour == 4), \
                '5am': 1. * (hour == 5), \
                '6am': 1. * (hour == 6), \
                '7am': 1. * (hour == 7), \
                '8am': 1. * (hour == 8), \
                '9am': 1. * (hour == 9), \
                '10am': 1. * (hour == 10), \
                '11am': 1. * (hour == 11), \
                '12pm': 1. * (hour == 12), \
                '1pm': 1. * (hour == 13), \
                '2pm': 1. * (hour == 14), \
                '3pm': 1. * (hour == 15), \
                '4pm': 1. * (hour == 16), \
                '5pm': 1. * (hour == 17), \
                '6pm': 1. * (hour == 18), \
                '7pm': 1. * (hour == 19), \
                '8pm': 1. * (hour == 20), \
                '9pm': 1. * (hour == 21), \
                '10pm': 1. * (hour == 22), \
                '11pm': 1. * (hour == 23), \
                'weekday': weekday, \
                'weekend': weekend, }



        # Extracting features from data

    def evaluateState(self, state):
        reward = - self.serverPrice * state['serversRunning'] \
                 - self.serverPrice * state['serversStarting'] \
                 - (state['maxCPU'] > 1) * (state['maxCPU'] - 1) * 500 \
                 - (state['maxMemory'] > 0.8) * (state['maxMemory'] - 0.8) * 1000
        print 'Reward: ' + str(reward)
        return reward

    """
    def getDerivatives(self):
        if len(self.prevRequests) <= 1: return 0

        median = round(len(self.prevRequests)) / 2

        prevRequestsAvg = np.mean(self.prevRequests[:median])
        currentRequestsAvg = np.mean(self.prevRequests[median:])
        derivativeRequests = (currentRequestsAvg - prevRequestsAvg) / median

        return derivativeRequests

    """

    def __getCombinedTimestampFeatures__(self, features, time, weekday):
        featuresTime = np.dot(features.reshape(-1, 1), np.array([time])).reshape(1, -1)[0]
        featuresDate = np.dot(featuresTime.reshape(-1, 1), np.array([weekday])).reshape(1, -1)[0]
        return featuresDate

    def getFeatures(self, state):
        infoFeatures = np.array([state['bias'], \
                                 state['serversRunning'], \
                                 state['serversStarting'], \
                                 (state['serversRunning'] + state['serversStarting'] - 1 > 0) * (
                                     state['serversRunning'] + state['serversStarting'] - 1), \
                                 state['serversRunning'] + state['serversStarting'] + 1, \
                                 (state['serversRunning'] + state['serversStarting'] - 4 > 0) * (
                                     state['serversRunning'] + state['serversStarting'] - 4), \
                                 state['serversRunning'] + state['serversStarting'] + 4, \
                                 (state['serversRunning'] + state['serversStarting'] - 10 > 0) * (
                                     state['serversRunning'] + state['serversStarting'] - 10), \
                                 state['serversRunning'] + state['serversStarting'] + 10, \
                                 # state['derivativeRequests'], \
                                 # state['derivativeRequests'] / (1. * state['serversRunning']), \
                                 state['maxCPU'], \
                                 state['maxCPU'] - 1., \
                                 state['maxMemory'], \
                                 state['maxMemory'] - 0.8, \
                                 float(state['totalRequests']) / float(state['serversRunning']) \
            ])

        time = np.array([state['0am'], state['1am'], state['2am'], state['3am'], \
                         state['4am'], state['5am'], state['6am'], state['7am'], \
                         state['8am'], state['9am'], state['10am'], state['11am'], \
                         state['12pm'], state['1pm'], state['2pm'], state['3pm'], \
                         state['4pm'], state['5pm'], state['6pm'], state['7pm'], \
                         state['8pm'], state['9pm'], state['10pm'], state['11pm']])
        weekday = np.array([state['weekday'], state['weekend']])

        singleorder = infoFeatures
        if self.featureOrder == 1:
            if self.combineTimeDate: return self.__getCombinedTimestampFeatures__(features=singleorder, time=time,
                                                                                  weekday=weekday)
            return singleorder
        square = np.dot(singleorder.reshape(-1, 1), np.array([singleorder])).reshape(1, -1)[0]
        if self.featureOrder == 2:
            if self.combineTimeDate: return self.__getCombinedTimestampFeatures__(features=square, time=time,
                                                                                  weekday=weekday)
            return square
        cube = np.dot(singleorder.reshape(-1, 1), [square]).reshape(1, -1)[0]
        if self.featureOrder == 3:
            if self.combineTimeDate: return self.__getCombinedTimestampFeatures__(features=cube, time=time,
                                                                                  weekday=weekday)
            return cube

    def getValidActions(self, state):
        validActions = range(len(self.actions))

        if state['maxCPU'] >= 1 or state['maxMemory'] >= 0.8:
            if 0 in validActions: validActions.remove(0)
            if 4 in validActions: validActions.remove(4)
            if 5 in validActions: validActions.remove(5)
            if 6 in validActions: validActions.remove(6)

        if state['maxCPU'] < 0.1 and state['maxMemory'] < 0.1:
            if 0 in validActions: validActions.remove(0)
            if 1 in validActions: validActions.remove(1)
            if 2 in validActions: validActions.remove(2)
            if 3 in validActions: validActions.remove(3)

        print validActions
        return validActions

    def estimateAction(self, state, actionId):
        features = self.getFeatures(state)
        Q = sum(features * self.weights[actionId])
        return Q

    def estimateBestAction(self, state):
        features = self.getFeatures(state)
        actions = self.getValidActions(state)
        Q = [sum(features * self.weights[i]) for i in actions]
        maxQ = max(Q)
        actionId = actions[Q.index(maxQ)]

        return [maxQ, actionId, features]

    def takeAction(self, actionId):
        print 'Take actionID: ' + str(actionId)
        if actionId == 1: self.interface.startServer(1)
        if actionId == 2: self.interface.startServer(4)
        if actionId == 3: self.interface.startServer(10)
        if actionId == 4: self.interface.stopServer(1)
        if actionId == 5: self.interface.stopServer(4)
        if actionId == 6: self.interface.stopServer(10)

    def updateWeights(self, Q, actionId, features, newState):
        reward = self.evaluateState(newState)
        [V, a, f] = self.estimateBestAction(newState)
        print 'Reward + V: ' + str(reward + V)
        print 'Difference: ' + str(Q - (reward + V))
        derivative = (Q - (reward + V)) * features
        if self.rmsProp != False:
            self.updateMms(derivative=derivative, actionId=actionId)

        self.weights[actionId] = self.weights[actionId] - self.learningRate / np.sqrt(self.mms[actionId]) * derivative

    def control(self, numSteps=1000, exploration=0.01, verbose=0, delay=0, autosavePeriod=1000,
                autosaveFile='autosave.npy'):
        state = self.getNextState()
        # print state
        if verbose > 3:
            plt.ion()
            plt.show()
            f = open('control_log.csv', 'w')
            f.write('num_requests,num_servers_running,num_servers_starting,max_cpu,max_memory,action,reward\n')

        for step in range(numSteps):
            if delay != 0: time.sleep(delay)
            if np.random.uniform() < exploration:
                features = self.getFeatures(state)
                actionId = random.choice(self.getValidActions(state))
                maxQ = self.estimateAction(state, actionId)
                self.takeAction(actionId)
            else:
                maxQ, actionId, features = self.estimateBestAction(state)
                self.takeAction(actionId)

            if verbose >= 1:
                print '------------------------------------------------------------'
                print 'Step: ' + str(step) + ', action: ' + self.actions[actionId]

            if verbose >= 4:
                plt.clf()
                self.visualize()
                f.write(str(state['totalRequests']) + ',' + str(state['serversRunning']) + ',' + str(
                    state['serversStarting']) + ',' + str(state['maxCPU']) + ',' + str(state['maxMemory']) + ',' + str(
                    self.actions[actionId]) + ',')

            if verbose >= 2:
                print'Servers running: ' + str(state['serversRunning'])
                print'Max CPU: ' + str(state['maxCPU'])
                print'Max Memory: ' + str(state['maxMemory'])
                # print 'Derivative: ' + str(state['derivativeRequests'])

            if step % autosavePeriod == 0 and step != 0:
                self.saveWeights(autosaveFile)

            state = self.getNextState()
            if verbose >= 4:
                f.write(str(self.evaluateState(state)) + '\n')
            self.updateWeights(Q=maxQ, actionId=actionId, features=features, newState=state)

    def saveWeights(self, file):
        np.save(file, self.weights)

    def loadWeights(self, file):
        self.weights = np.load(file)

    def visualize(self):
        if self.plotHistory == None: pass
        x = np.array([-len(self.history['meanCPULoad']) + i + 1 for i in range(len(self.history['meanCPULoad']))]) * 5

        plt.subplot(3, 2, 1)
        plt.axis([(-self.plotHistory + 1) * 5, 0, 0.0, 2.0])
        ax = plt.gca()
        ax.set_autoscale_on(False)
        plt.plot(x, self.history['meanCPULoad'])
        plt.xlabel('Time (minutes)')
        plt.ylabel('Mean CPU Load (%)')
        plt.grid(True)

        plt.subplot(3, 2, 2)
        plt.axis([(-self.plotHistory + 1) * 5, 0, 0.0, 2.0])
        ax = plt.gca()
        ax.set_autoscale_on(False)
        plt.plot(x, self.history['maxCPULoad'])
        plt.xlabel('Time (minutes)')
        plt.ylabel('Max CPU Load (%)')
        plt.grid(True)

        plt.subplot(3, 2, 3)
        plt.axis([(-self.plotHistory + 1) * 5, 0, 0.0, 2.0])
        ax = plt.gca()
        ax.set_autoscale_on(False)
        plt.plot(x, self.history['meanMemoryLoad'])
        plt.xlabel('Time (minutes)')
        plt.ylabel('Mean Memory Load (%)')
        plt.grid(True)

        plt.subplot(3, 2, 4)
        plt.axis([(-self.plotHistory + 1) * 5, 0, 0.0, 2.0])
        ax = plt.gca()
        ax.set_autoscale_on(False)
        plt.plot(x, self.history['maxMemoryLoad'])
        plt.xlabel('Time (minutes)')
        plt.ylabel('Max Memory Load (%)')
        plt.grid(True)

        plt.subplot(3, 2, 5)
        # plt.axis(xmin=(-self.plotHistory+1)*5,xmax=0)
        # ax = plt.gca()
        # ax.set_autoscale_on(False)
        plt.plot(x, self.history['totalRequests'])
        plt.xlabel('Time (minutes)')
        plt.ylabel('Number of Requests')
        plt.grid(True)

        plt.subplot(3, 2, 6)
        # plt.axis([(-self.plotHistory+1)*5,0, 0.0,20.0])
        # ax = plt.gca()
        # ax.set_autoscale_on(False)
        plt.plot(x, self.history['serversRunning'])
        plt.plot(x, self.history['serversStarting'])
        plt.legend(["Running", "Starting"], loc=2, prop={'size': 10})
        plt.xlabel('Time (minutes)')
        plt.ylabel('Servers')
        plt.grid(True)

        plt.draw()
        plt.pause(0.0001)

















