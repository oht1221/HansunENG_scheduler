import scheduler
import random
POPULATION = 10
chromosomes = [POPULATION]

def genetic_algorithm(job_pool):
    for i in range(POPULATION):
        chromosomes[i] = initial_permutation(job_pool)

def initial_permutation(pool):
    per = list()
    while (len(pool) != len(per)):
        i = random.randrange(0, len(pool))
        newElement = pool[i]
        per.append(newElement)
    return per

def cross_over():

def mutation():

def total_delayed_time():

def total_delayed_jobs_count():

def last_job_execution():

def evaluate():

def schedule(CNCs, job_pool, machines):
    total_delayed_time = 0
    total_delayed_jobs_count = 0
    last_job_execution = 0
    unAssigned = []
    '''for cnc in CNCs:
        machines[cnc.getNumber()] = list()'''

    avg_time = sum(list(job.getTime() for job in job_pool)) / len(job_pool)

    normPool = list()
    hexPool = list()
    splitPool(job_pool, normPool, hexPool)
    #normPool.sort(key=lambda x: x.getDue())
    #hexPool.sort(key=lambda x: x.getDue())
    normPool = permutation(normPool)
    hexPool = permutation(hexPool)
    # normPool = permutations(normPool,len(normPool))
    # hexPool = permutations(hexPool,len(hexPool))
    normCNCs = list(filter(lambda x: x.getShape() == 0, CNCs))
    hexCNCs = list(filter(lambda x: x.getShape() == 1, CNCs))
    # sortedNormPool = sorted(normPool, key = lambda j : j.getDue())
    # sortedHexPool = sorted(hexPool, key = lambda j: j.getDue())
    standard = input("schedule starts on : ")
    standard = (lambda x: int(time.time()) if (x == 'now') else time.mktime((int(x[0:4]), int(x[4:6]), int(x[6:8]), 12, 0, 0, 0, 0, 0)))(standard)
    standard = int(standard)
    print("----standard----")
    print(standard)
    print("----standard----")
    for i, j in enumerate(normPool):

        selected_CNCs = []
        for c in normCNCs:
            if c.getGround() <= j.getSize() <= c.getCeiling():  # size 맞는 CNC는 모두 찾음
                selected_CNCs.append(c)

        timeLefts = [sum([j.getTime() for j in machines[c.getNumber()]]) for c in selected_CNCs]
        if len(timeLefts) <= 0: #조건에 맞는 CNC가 하나도 없으면
            unAssigned.append(j)
            continue
        minValue = min(timeLefts)
        minIndex = timeLefts.index(minValue)
        cnc = selected_CNCs[minIndex]
        #cnc.enQ(j, in_progress=in_progress)
        (machines[cnc.getNumber()]).append(j)
        j.assignedTo(cnc)
        #ready_pool.appendleft(j)
        #job_pool.remove(j)
        notice = "a new job(" + str(j.getGoodNum()) + ") asggined to CNC #(" + \
                 str(cnc.getNumber()) + ")!\n"

        time_left_of_cnc = sum([j.getTime() for j in machines[cnc.getNumber()]])
        if last_job_execution < time_left_of_cnc:
            last_job_execution = time_left_of_cnc

        diff = j.getDue() - (time_left_of_cnc + j.getTime() + standard)
        print('----------')
        print(j.getDue())
        if diff < 0:
            notice += "(" + str((-1) * diff) + "more time units needed to meet duetime)\n"
            total_delayed_jobs_count += 1
            total_delayed_time += (-1) * diff
        j.setMsg(notice)

    for i, j in enumerate(hexPool):
        selected_CNCs = []
        for c in hexCNCs:
            if (c.getGround() <= j.getSize() <= c.getCeiling()):  # size 맞는 CNC는 모두 찾음
                selected_CNCs.append(c)

                timeLefts = [sum([j.getTime() for j in machines[c.getNumber()]]) for c in selected_CNCs]
        minValue = min(timeLefts)
        minIndex = timeLefts.index(minValue)
        cnc = selected_CNCs[minIndex]
        #cnc.enQ(j, in_progress=in_progress)
        (machines[cnc.getNumber()]).append(j)
        j.assignedTo(cnc)
        #ready_pool.appendleft(j)
        #job_pool.remove(j)
        notice = "a new job(" + str(j.getGoodNum()) + ") asggined to CNC #(" + \
                 str(cnc.getNumber()) + ")!\n"

        time_left_of_cnc = sum([j.getTime() for j in machines[cnc.getNumber()]])
        if last_job_execution < time_left_of_cnc:
            last_job_execution = time_left_of_cnc

        diff = j.getDue() - (time_left_of_cnc + j.getTime() + standard)
        print('----------')
        print(j.getDue())
        if diff < 0:
            notice += "(" + str((-1) * diff) + "more time units needed to meet duetime)\n"
            total_delayed_jobs_count += 1
            total_delayed_time += (-1) * diff
        j.setMsg(notice)

    msg = [total_delayed_time, total_delayed_jobs_count, last_job_execution, machines]
    return msg


def splitPool(job_pool, normPool, hexPool):

    for i,assignment in enumerate(job_pool):
        if assignment.getType() == 0:
            normPool.append(assignment)

        elif assignment.getType() == 1:
            hexPool.append(assignment)

    return 0
