from collections import deque
import random
import numpy as np

class job:
    def __init__(self, number, time, type, size, quantity, due = 0):
        self.number = number
        self.timeLeft = sum(time) * quantity
        self.type = type
        self.size = size
        self.quantity = quantity
        self.series = [component(time[i], self, quantity) for i in range(len(time))]
        self.due  = sum(time) * quantity * random.choice(range(2, 6, 1))

        '''for i in size(time):
            self.series.append(component(time[i], self, quantity)) '''
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

    def ifAllDone(self):
        return np.all([ (self.getSeries())[i].ifDone() for i in range(len(self.getSeries())) ])




        #self.left = left #남은 작업량
        #self.sequence = [0,0] #n차 가공 끝낸 것
class component:
    def __init__(self, cycleTime, job, quantity):
        self.cycleTime = cycleTime
        self.done = False
        self.partOf = job
        self.quantity = quantity
        self.timeLeft = cycleTime * quantity
        self.count = 0 #count가 cycletime 만큼 올라가면 제품 하나를 완성했다고 가정

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