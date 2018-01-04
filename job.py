from collections import deque
import random
import numpy as np

class Job:
    def __init__(self, number, type, size, quantity, time = [0,0,0], due = 0):
        self.number = number
        self.timeLeft = sum(time) * quantity # 재셋팅 시간 1000 추가
        self.type = type
        self.size = size
        self.quantity = quantity
        self.series = []
        self.series  = [Component(time[i], self, quantity) for i in range(len(time))]
        self.due  = sum(time) * quantity * random.choice(range(5, 10, 1))
        self.cnc = None
        self.msg = None

    def ifAllDone(self):
        return np.all([(self.getSeries())[i].ifDone() for i in range(len(self.getSeries()))])

    def update_due(self):
        self.due -= 1

    def getSeries(self):
        return self.series

    def getComponent(self, n):
        return self.series[n]

    def getSize(self):
        return self.size

    def getNumber(self):
        return self.number

    def getTime(self):
        self.timeLeft = sum([component.getTime() for component in self.series])
        return self.timeLeft

    def getType(self):
        return self.type

    def getDue(self):
        return self.due

    def assignedTo(self, cnc):
        self.cnc = cnc

    def setMsg(self, msg):
        self.msg = msg

class Component:
    def __init__(self, cycleTime, job, quantity):
        self.cycleTime = cycleTime
        self.done = False
        self.partOf = job
        self.count = 0 #count가 cycletime 만큼 올라가면 제품 하나를 완성했다고 가정
        self.quantity = quantity
        self.timeLeft = cycleTime * quantity

    def spendTime(self, unitTime):
        self.timeLeft = self.timeLeft - unitTime
        self.counter(unitTime)
        if(self.timeLeft <= 0):
            self.setTime(0)
            self.turnDone()

    def counter(self, unitTime):
        self.count = (self.count + unitTime) % self.cycleTime
        if(self.count == 0):
            self.quantity += -1

    def getTime(self):
        return self.timeLeft

    def ifDone(self):
        return self.done

    def getJob(self):
        return self.partOf

    def turnDone(self):
        self.done = True

    def setTime(self, time):
        self.timeLeft = time

"""
class NormalCompoenet(Component):
    def __init__(self, cycleTime, job, quantity):
        super().__init__(cycleTime, job)
        self.quantity = quantity
        self.timeLeft = cycleTime * quantity

class ReplacementComponent(Component):
    def __init__(self, cycleTime, job):
        super().__init__(cycleTime, job)
"""