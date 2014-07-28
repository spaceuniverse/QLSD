import numpy as np
#---------------------------------------------------------------------#
oldHealth = None

def itThereWallDOWN(status, player, z):
    answer = 0
    playerXY = getPlayerXY(status)
    if playerXY[1] + z >= player.sandbox.screen[1] - 20:
        answer = 1
    return answer


def itThereWallLEFT(status, player, z):
    answer = 0
    playerXY = getPlayerXY(status)
    if playerXY[0] - z <= 0:
        answer = 1
    return answer


def itThereWallRIGHT(status, player, z):
    answer = 0
    playerXY = getPlayerXY(status)
    if playerXY[0] + z >= player.sandbox.screen[0] - 20:
        answer = 1
    return answer


def itThereWallUP(status, player, z):
    answer = 0
    playerXY = getPlayerXY(status)
    if playerXY[1] - z <= 0:
        answer = 1
    return answer


def getCodeState(s):
    #code = s[-1] + 2 * s[-2] + 4 * s[-3] + 8 * s[-4] + 16 * s[-6] - 16
    code = 0
    for i in range(1, len(s)):
        code += s[-len(s) + i] * (2 ** (i - 1))
    alternate_code = s[-1] + 2 * s[-2] + 4 * s[-3] + 8 * s[-4]
    return code - 2 ** (len(s) - 2) if s[1] == 1 else alternate_code


def getReward(f):
    dmg = 0 if f[0] == 0 else -500
    hld = 100 if f[1] == 1 else -5
    wall = np.sum(f[2] * -20)
    return dmg + hld + wall


def getExploreActions(a, s, q, e):
    if np.random.rand(1) > e:
        action, action_code = getOptimalActions(a, s, q)
    else:
        action, action_code = getRandomActions(a)
    return action, action_code


def getOptimalActions(a, s, q):
    idx = np.argmax(q[s, :])
    return a[idx], idx


def getRandomActions(a):
    rnd = np.random.randint(len(a))
    return a[rnd], rnd


def getDistanceToClosestItem(S, t):
    dst = 9999
    player = getPlayerXY(S)
    for o in S:
        if o['class'] != 'blockplayer' and o['class'] == t:
            X = o['x_position']
            Y = o['y_position']
            bullet = np.array([X, Y])
            toBullet = getDistanceBetweenPoints(player, bullet)
            if toBullet < dst:
                dst = toBullet

    return (dst if dst != 9999 else 0) / 100


def LineA(b, p):
    val = -b[0] + (p[0] + p[1])
    return val


def LineB(b, p):
    val = b[0] + (p[1] - p[0])
    return val


def isThereItemUP(S, r, t):
    answer = 0
    player = getPlayerXY(S)
    for o in S:
        if o['class'] != 'blockplayer' and o['class'] == t:
            X = o['x_position']
            Y = o['y_position']
            bullet = np.array([X, Y])
            dst = getDistanceBetweenPoints(player, bullet)
            isInUpperQ = LineA(bullet, player) >= Y and LineB(bullet, player) >= Y
            if dst < r and isInUpperQ:
                answer = 1
                break
    return answer


def isThereItemRIGHT(S, r, t):
    answer = 0
    player = getPlayerXY(S)
    for o in S:
        if o['class'] != 'blockplayer' and o['class'] == t:
            X = o['x_position']
            Y = o['y_position']
            bullet = np.array([X, Y])
            dst = getDistanceBetweenPoints(player, bullet)
            isInUpperQ = LineA(bullet, player) < Y < LineB(bullet, player)
            if dst < r and isInUpperQ:
                answer = 1
                break
    return answer


def isThereItemLEFT(S, r, t):
    answer = 0
    player = getPlayerXY(S)
    for o in S:
        if o['class'] != 'blockplayer' and o['class'] == t:
            X = o['x_position']
            Y = o['y_position']
            bullet = np.array([X, Y])
            dst = getDistanceBetweenPoints(player, bullet)
            isInUpperQ = LineA(bullet, player) > Y > LineB(bullet, player)
            if dst < r and isInUpperQ:
                answer = 1
                break
    return answer


def isThereItemDOWN(S, r, t):
    answer = 0
    player = getPlayerXY(S)
    for o in S:
        if o['class'] != 'blockplayer' and o['class'] == t:
            X = o['x_position']
            Y = o['y_position']
            bullet = np.array([X, Y])
            dst = getDistanceBetweenPoints(player, bullet)
            isInUpperQ = LineA(bullet, player) <= Y and LineB(bullet, player) <= Y
            if dst < r and isInUpperQ:
                answer = 1
                break
    return answer


def getDistanceBetweenPoints(a, b):
    dst = np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    return dst


def getPlayerXY(S):
    X = None
    Y = None
    for o in S:
        if o['class'] == 'blockplayer':
            X = o['x_position']
            Y = o['y_position']
            break
    return np.array([X, Y])


def isThereSomethingAround(S, r):
    answer = 0
    player = getPlayerXY(S)
    for o in S:
        if o['class'] != 'blockplayer':
            X = o['x_position']
            Y = o['y_position']
            block = np.array([X, Y])
            dst = getDistanceBetweenPoints(player, block)
            if dst < r:
                answer = 1
                break
    return answer


def getFeatures(s, p):
    safeBulletZone = 50
    healerZone = 100
    safeWallZone = 40
    bias = 1
    somethingAround = isThereSomethingAround(s, safeBulletZone)
    dstToClosestBullet = getDistanceToClosestItem(s, 'bullet')
    bulletUP = isThereItemUP(s, safeBulletZone, 'bullet')
    bulletRIGHT = isThereItemRIGHT(s, safeBulletZone, 'bullet')
    bulletLEFT = isThereItemLEFT(s, safeBulletZone, 'bullet')
    bulletDOWN = isThereItemDOWN(s, safeBulletZone, 'bullet')
    healerUP = isThereItemUP(s, healerZone, 'healthbox')
    healerRIGHT = isThereItemRIGHT(s, healerZone, 'healthbox')
    healerLEFT = isThereItemLEFT(s, healerZone, 'healthbox')
    healerDOWN = isThereItemDOWN(s, healerZone, 'healthbox')
    wallUP = itThereWallUP(s, p, safeWallZone)
    wallRIGHT = itThereWallRIGHT(s, p, safeWallZone)
    wallLEFT = itThereWallLEFT(s, p, safeWallZone)
    wallDOWN = itThereWallDOWN(s, p, safeWallZone)
    #Debug
    dstToClosestBullet = 0
    return np.array([bias, dstToClosestBullet, somethingAround,
                     wallUP, wallRIGHT, wallLEFT, wallDOWN,
                     bulletUP, bulletRIGHT, bulletLEFT, bulletDOWN,
                     healerUP, healerRIGHT, healerLEFT, healerDOWN])


def getFeaturesForReward(s, f):
    global oldHealth
    damaged = 0
    healed = 0
    for o in s:
        if o['class'] == 'blockplayer':
            playerHealth = o['health']
            if oldHealth == None:
                oldHealth = playerHealth
            else:
                if oldHealth > playerHealth:
                    damaged = 1
                    oldHealth = playerHealth
                elif oldHealth < playerHealth:
                    healed = 1
                    oldHealth = playerHealth
                else:
                    oldHealth = playerHealth
    #wall penalty
    wall = f[3:7]
    return [damaged, healed, wall]
