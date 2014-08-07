# ---------------------------------------------------------------------# IMPORTS


import sys
import pygame
import numpy as np
from numpy import *


# ---------------------------------------------------------------------# CONSTANTS


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# ---------------------------------------------------------------------#


class Sand(object):
    def __init__(self):
        self.screen = (800, 600)
        self.firerate = 60
        self.enum = 7
        self.fun = True
        self.report = False


# ---------------------------------------------------------------------#


class Enemy(pygame.sprite.Sprite):
    def __init__(self, sandbox, color=WHITE, report=False, width=20, height=20):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.live = True
        self.speed = np.array([-1, 0, 1, 2, -2])
        self.bonusx = 0.0
        self.bonusy = 0.0
        np.random.shuffle(self.speed)
        self.sandbox = sandbox
        self.rect.x = np.random.randint(0, self.sandbox.screen[0] - self.width)
        self.rect.y = np.random.randint(0, self.sandbox.screen[1] - self.height)
        self.health = 100.0
        self.hMonitor = self.health
        self.hPlus = False
        self.hMinus = False
        self.fuel = 100.0
        self.ignition = np.array([0.0, 0.0])
        self.report = report
        self.uptime = 0.0
        self.environment = np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]])
        self.ignitionspeed = 0.5
        self.ignitionstop = 0.1
        self.vfield = 50.0

    def harassment(self, bullet):
        self.health = self.health - bullet.damage + (bullet.speed[0] - self.speed[0]) * 1.5 + (bullet.speed[1] -
                                                                                               self.speed[1]) * 1.5
        self.bonusx = bullet.speed[0]
        self.bonusy = bullet.speed[1]
        if self.report:
            print self.health
        if self.health <= 0:
            self.death()

    def heal(self, health):
        self.health = self.health + health.heal
        if self.report:
            print self.health

    def death(self):
        self.live = False
        if self.report:
            print self.statusreport()

    def fire(self):
        bullet = Bullet(self.sandbox, self.rect.x, self.rect.y)
        return bullet

    def __shuffling_(self):
        np.random.shuffle(self.speed)
        self.bonusx = 0
        self.bonusy = 0
        self.__stop__()

    def __wall__(self):
        if self.rect.x > self.sandbox.screen[0] - self.width:
            self.rect.x = self.sandbox.screen[0] - self.width
            self.__shuffling_()
        if self.rect.x < 0:
            self.rect.x = 0
            self.__shuffling_()
        if self.rect.y > self.sandbox.screen[1] - self.height:
            self.rect.y = self.sandbox.screen[1] - self.height
            self.__shuffling_()
        if self.rect.y < 0:
            self.rect.y = 0
            self.__shuffling_()

    def __move_00__(self):
        self.ignition[0] -= self.ignitionspeed
        self.ignition[1] -= self.ignitionspeed
        self.__clipSpeed__()

    def __move_01__(self):
        self.ignition[1] -= self.ignitionspeed
        self.__clipSpeed__()

    def __move_02__(self):
        self.ignition[0] += self.ignitionspeed
        self.ignition[1] -= self.ignitionspeed
        self.__clipSpeed__()

    def __move_10__(self):
        self.ignition[0] -= self.ignitionspeed
        self.__clipSpeed__()

    def __move_11__(self):
        self.__clipSpeed__()

    def __move_12__(self):
        self.ignition[0] += self.ignitionspeed
        self.__clipSpeed__()

    def __move_20__(self):
        self.ignition[0] -= self.ignitionspeed
        self.ignition[1] += self.ignitionspeed
        self.__clipSpeed__()

    def __move_21__(self):
        self.ignition[1] += self.ignitionspeed
        self.__clipSpeed__()

    def __move_22__(self):
        self.ignition[0] += self.ignitionspeed
        self.ignition[1] += self.ignitionspeed
        self.__clipSpeed__()

    def __stop__(self):
        if np.absolute(self.ignition[0]) >= self.ignitionstop:
            self.ignition[0] = self.ignition[0] + (-1) * np.sign(self.ignition[0]) * self.ignitionstop
        else:
            self.ignition[0] = 0.0
        if np.absolute(self.ignition[1]) >= self.ignitionstop:
            self.ignition[1] = self.ignition[1] + (-1) * np.sign(self.ignition[1]) * self.ignitionstop
        else:
            self.ignition[1] = 0.0

    def __clipSpeed__(self):
        self.ignition = np.clip(self.ignition, -11.0, 11.0)

    def __healthMonitor__(self):
        if self.hMonitor > self.health:
            self.hMinus = True
        elif self.hMonitor < self.health:
            self.hPlus = True
        else:
            self.hMinus = False
            self.hPlus = False
        self.hMonitor = self.health

    def move(self):
        self.rect.x = self.rect.x + self.speed[0] + self.bonusx + self.ignition[0]
        self.rect.y = self.rect.y + self.speed[1] + self.bonusy + self.ignition[1]
        #if self.report:
        #    print self.speed[0], self.bonusx, self.ignition[0], "---", self.speed[0] + self.bonusx + self.ignition[0]
        #    print self.speed[1], self.bonusy, self.ignition[1], "---", self.speed[1] + self.bonusy + self.ignition[1]
        self.uptime = self.uptime + 0.01
        self.__healthMonitor__()
        self.__wall__()

    def statusreport(self):
        status = {"class": "blockagent", "x_position": self.rect.x, "y_position": self.rect.y, "x_speed": self.speed[0],
                  "y_speed": self.speed[1], "x_speed_bonus": self.bonusx, "y_speed_bonus": self.bonusy,
                  "health": self.health, "uptime": self.uptime}
        return status


# ---------------------------------------------------------------------#


class Player(Enemy):
    def __init__(self, sandbox, color=BLUE, report=False, width=15, height=15):
        self.actions = [self.__move_00__, self.__move_01__, self.__move_02__, self.__move_10__, self.__move_11__,
                        self.__move_12__, self.__move_20__, self.__move_21__, self.__move_22__, self.__stop__]
        super(Player, self).__init__(sandbox, color, report, width, height)

    def statusreport(self):
        status = {"live": self.live, "environment": self.environment, "class": "blockplayer", "x_position": self.rect.x,
                  "y_position": self.rect.y, "x_speed": self.speed[0], "y_speed": self.speed[1],
                  "x_speed_bonus": self.bonusx, "y_speed_bonus": self.bonusy, "health": self.health,
                  "uptime": self.uptime, "plus": self.hPlus, "minus": self.hMinus}
        return status

    def scan(self, list, type=None):
        if type == "hit":
            t = 0
        elif type == "heal":
            t = 1
        for block in list:
            if self.rect.x - self.vfield <= block.rect.x < self.rect.x and self.rect.y - self.vfield <= block.rect.y < self.rect.y:
                self.environment[t][0][0] += 1
            if self.rect.x <= block.rect.x < self.rect.x + self.width and self.rect.y - self.vfield <= block.rect.y < self.rect.y:
                self.environment[t][0][1] += 1
            if self.rect.x + self.width <= block.rect.x < self.rect.x + self.width + self.vfield and self.rect.y - self.vfield <= block.rect.y < self.rect.y:
                self.environment[t][0][2] += 1
            if self.rect.x - self.vfield <= block.rect.x < self.rect.x and self.rect.y <= block.rect.y < self.rect.y + self.height:
                self.environment[t][1][0] += 1
            #if self.rect.x <= block.rect.x < self.rect.x + self.width and self.rect.y <= block.rect.y < self.rect.y + self.height:
            #    self.environment[t][1][1] += 1
            if self.rect.x + self.width <= block.rect.x < self.rect.x + self.width + self.vfield and self.rect.y <= block.rect.y < self.rect.y + self.height:
                self.environment[t][1][2] += 1
            if self.rect.x - self.vfield <= block.rect.x < self.rect.x and self.rect.y + self.height <= block.rect.y < self.rect.y + self.height + self.vfield:
                self.environment[t][2][0] += 1
            if self.rect.x <= block.rect.x < self.rect.x + self.width and self.rect.y + self.height <= block.rect.y < self.rect.y + self.height + self.vfield:
                self.environment[t][2][1] += 1
            if self.rect.x + self.width <= block.rect.x < self.rect.x + self.width + self.vfield and self.rect.y + self.height <= block.rect.y < self.rect.y + self.height + self.vfield:
                self.environment[t][2][2] += 1

    def clean(self):
        self.environment = np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]])

    def brain(self, type=None):
        decision_heal = np.argmax(self.environment[1])
        decision_bullet = np.argmax(self.environment[0])
        decision = 9
        if type == "healcatch" and np.sum(self.environment[1]) != 0:
            decision = decision_heal
        elif type == "bulletdodge" and np.sum(self.environment[0]) != 0:
            decision = 8 - decision_bullet
        self.actions[decision]()

    def randomAction(self):
        rnd = np.random.randint(len(self.actions))
        self.actions[rnd]()


# ---------------------------------------------------------------------#


class Health(pygame.sprite.Sprite):
    def __init__(self, sandbox):
        pygame.sprite.Sprite.__init__(self)
        self.width = 5
        self.height = 5
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.live = True
        self.sandbox = sandbox
        self.rect.x = np.random.randint(0, self.sandbox.screen[0] - self.width)
        self.rect.y = np.random.randint(0, self.sandbox.screen[1] - self.height)
        self.heal = 5.0
        self.ttl = 500

    def death(self):
        self.live = False

    def move(self):
        self.ttl = self.ttl - 1
        self.heal = self.heal + 0.01
        if self.ttl <= 0:
            self.death()

    def statusreport(self):
        status = {"class": "healthbox", "x_position": self.rect.x, "y_position": self.rect.y, "heal_rate": self.heal,
                  "ttl": self.ttl}
        return status


# ---------------------------------------------------------------------#


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sandbox, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 5
        self.height = 5
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.live = True
        self.speed = np.array([-5, 5, 0, 4, -4, 3, -3, 2, -2, 1, -1])
        np.random.shuffle(self.speed)
        self.sandbox = sandbox
        self.rect.x = x  # + 8
        self.rect.y = y  # + 8
        self.damage = 10.0 + 6.5 * np.maximum(np.absolute(self.speed[0]), np.absolute(self.speed[1]))

    def death(self):
        self.live = False

    def __wall__(self):
        if self.rect.x > self.sandbox.screen[0] - self.width:
            self.rect.x = self.sandbox.screen[0] - self.width
            self.death()
        if self.rect.x < 0:
            self.rect.x = 0
            self.death()
        if self.rect.y > self.sandbox.screen[1] - self.height:
            self.rect.y = self.sandbox.screen[1] - self.height
            self.death()
        if self.rect.y < 0:
            self.rect.y = 0
            self.death()

    def move(self):
        self.rect.x = self.rect.x + self.speed[0]
        self.rect.y = self.rect.y + self.speed[1]
        self.__wall__()

    def statusreport(self):
        status = {"class": "bullet", "x_position": self.rect.x, "y_position": self.rect.y, "x_speed": self.speed[0],
                  "y_speed": self.speed[1], "damage": self.damage}
        return status


# ---------------------------------------------------------------------#


class Collision(object):
    @staticmethod
    def test(list, obj, type=None):
        for block in list:
            if block.rect.x >= obj.rect.x:
                if block.rect.y >= obj.rect.y:
                    if block.rect.x < obj.rect.x + obj.width:
                        if block.rect.y < obj.rect.y + obj.height:
                            block.death()
                            if type == "hit":
                                obj.harassment(block)
                            elif type == "heal":
                                obj.heal(block)


# ---------------------------------------------------------------------#


class Agent(object):
    @staticmethod
    def create(sand):
        random = (np.random.randint(50, 100), np.random.randint(50, 100), np.random.randint(200, 250))
        agent = Player(sand, random, report=True)
        return agent


# ---------------------------------------------------------------------#


class Cleaner(object):
    @staticmethod
    def clean(list):
        for block in list:
            if block.live is False and block.statusreport()["class"] != "blockplayer":
                list.remove(block)


# ---------------------------------------------------------------------#


class Global(object):
    @staticmethod
    def report(list):
        status = []
        for block in list:
            status.append(block.statusreport())
        return status


# ---------------------------------------------------------------------#


class allBox(object):
    def __init__(self):
        pygame.init()
        self.sand = Sand()
        self.window = pygame.display.set_mode((self.sand.screen[0], self.sand.screen[1]))
        self.enemy_list = []
        self.bullet_list = []
        self.health_list = []
        self.all_list = pygame.sprite.Group()
        for i in xrange(self.sand.enum):
            block = Enemy(self.sand)
            self.enemy_list.append(block)
            self.all_list.add(block)
        self.agent = Agent.create(self.sand)
        self.all_list.add(self.agent)
        self.clock = pygame.time.Clock()
        self.brain = np.array(range(self.sand.firerate))

    def oneStep(self, draw=True, brainType=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        self.window.fill(BLACK)
        if self.agent.live is False:
            self.all_list.remove(self.agent)
            self.agent = Agent.create(self.sand)
            self.all_list.add(self.agent)
        Collision.test(self.bullet_list, self.agent, type="hit")
        Collision.test(self.health_list, self.agent, type="heal")
        Cleaner.clean(self.all_list)
        Cleaner.clean(self.bullet_list)
        Cleaner.clean(self.health_list)
        self.agent.clean()
        self.agent.scan(self.bullet_list, type="hit")
        self.agent.scan(self.health_list, type="heal")
        if brainType == "ifelse":
            self.agent.brain(type="healcatch")
            self.agent.brain(type="bulletdodge")
        for block in self.all_list:
            block.move()
        for block in self.enemy_list:
            np.random.shuffle(self.brain)
            if self.brain[0] == 0:
                fire = block.fire()
                self.bullet_list.append(fire)
                self.all_list.add(fire)
        np.random.shuffle(self.brain)
        if self.brain[0] == 0:
            apt = Health(self.sand)
            self.health_list.append(apt)
            self.all_list.add(apt)
        if self.sand.report:
            print len(self.all_list), len(self.enemy_list), len(self.bullet_list), len(self.health_list)
        self.all_list.draw(self.window)
        if draw:
            self.clock.tick(60)
            pygame.display.update()
        return self

    def getPlayer(self):
        return self.agent

    def getStatus(self):
        return Global.report(self.all_list)


# ---------------------------------------------------------------------#