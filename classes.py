from collections import deque
import random

class CNC:
    def __init__(self, number = ' ', ground = ' ', ceiling = ' ', shape = ' ', type = ' '):
        self.number = number
        self.ground = ground
        self.ceiling = ceiling
        self.shape = shape
        self.type = type
        self.jobQ = deque()
        self.timeLeft = 0

    def print_info(self):
        print("CNC No. : %s\nSize : %s ~ %s\nshape : %s\ntype : %s\n"%(self.number,
                                                                        self.ground,
                                                                        self.ceiling,
                                                                        self.shape,
                                                                        self.type))
    def print_state(self):
        i = 0
        for j in self.jobQ:
            i = (i + 1) % 5
            print(j.getNumber(), end=' (')
            for n in range(3):
                print(j.getComponent(n).ifDone(), end = ' ')
            print(end = ')')
            if(i == 0): print(' ')
        print(' ')
        print(self.get_timeLeft())
        print('\n')

    def enQ(self, *element):
        if (type(element[0]) is job):
            self.jobQ.appendleft(element[0])
            self.update_timeLeft(element[0])

        if (type(element[0]) is component):
            self.jobQ.appendleft(element[0])
            self.update_timeLeft(element[0])

    def deQ(self):
        self.jobQ.pop()

    def update_timeLeft(self, *element):
        self.timeLeft += (element[0]).getTime()

    def get_jobQ(self):
        return self.jobQ

    def get_timeLeft(self):
        self.timeLeft = sum([job.getTime() for job in self.jobQ])
        return self.timeLeft

    def getGround(self):
        return self.ground

    def getCeiling(self):
        return self.ceiling

    def getNumber(self):
        return self.number

    def getShape(self):
        return self.shape

    def inProcess(self):
        j = self.jobQ[-1]
        for i in range(3):
            c = j.getComponent[i]
            if not c.ifDone():
                return c
class job:
    def __init__(self, number, time, type, size, quantity, due = 0):
        self.number = number
        self.timeLeft = sum(time) * quantity
        self.type = type
        self.size = size
        self.quantity = quantity
        self.series = []
        self.due  = sum(time) * quantity * random.choice(range(2, 6, 1))

        for i in range(0,3):
            self.series.append(component(time[i], self, quantity))

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

    def components(self,n):
        return self.series[n]

    def ifAllDone(self):
        return self.series[0].ifDone() and self.series[1].ifDone() and self.series[2].ifDone()



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