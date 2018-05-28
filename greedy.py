from job import  *
import datetime

def sort_pool(job_pool):
    return sorted(job_pool, key = lambda job : job.getDue(), reverse = True)

def splitPool(job_pool, normPool, hexPool):

    for i,assignment in enumerate(job_pool):
        if assignment.getType() == 0:
            normPool.append(assignment)

        elif assignment.getType() == 1:
            hexPool.append(assignment)

    return 0

def assign(machines, chromosome, CNCs):
    for v in machines.values():  # 각 machine에 있는 작업들 제거(초기화)
        v.clear()
    unAssigned = []
    '''for cnc in CNCs:
        machines[cnc.getNumber()] = list()'''
    normPool = list()
    hexPool = list()
    splitPool(chromosome, normPool, hexPool)
    # normPool.sort(key=lambda x: x.getDue())
    # hexPool.sort(key=lambda x: x.getDue())
    # normPool = permutations(normPool,len(normPool))
    # hexPool = permutations(hexPool,len(hexPool))
    normCNCs = list(filter(lambda x: x.getShape() == 0, CNCs))
    hexCNCs = list(filter(lambda x: x.getShape() == 1, CNCs))
    # sortedNormPool = sorted(normPool, key = lambda j : j.getDue())
    # sortedHexPool = sorted(hexPool, key = lambda j: j.getDue())

    for i, j in enumerate(normPool):

        selected_CNCs = []
        for c in normCNCs:
            if c.getGround() <= j.getSize() <= c.getCeiling():  # size 맞는 CNC는 모두 찾음
                selected_CNCs.append(c)

        timeLefts = [sum([j.getTime() for j in machines[c.getNumber()]]) for c in selected_CNCs]
        if len(timeLefts) <= 0:  # 조건에 맞는 CNC가 하나도 없으면
            unAssigned.append(j)
            continue
        minValue = min(timeLefts)
        minIndex = timeLefts.index(minValue)
        cnc = selected_CNCs[minIndex]
        (machines[cnc.getNumber()]).append(j)
        j.assignedTo(cnc)


    for i, j in enumerate(hexPool):

        selected_CNCs = []
        for c in hexCNCs:
            if (c.getGround() <= j.getSize() <= c.getCeiling()):  # size 맞는 CNC는 모두 찾음
                selected_CNCs.append(c)

        timeLefts = [sum([j.getTime() for j in machines[c.getNumber()]]) for c in selected_CNCs]
        if len(timeLefts) <= 0:  # 조건에 맞는 CNC가 하나도 없으면
            unAssigned.append(j)
            continue
        minValue = min(timeLefts)
        minIndex = timeLefts.index(minValue)
        cnc = selected_CNCs[minIndex]
        (machines[cnc.getNumber()]).append(j)
        j.assignedTo(cnc)

    interpreted = {}
    for k, v in machines.items():
        interpreted[k] = []
        for j in v:
            new = unit(j)
            interpreted[k].append(new)

    return interpreted

def evaluate(interpreted_chromosome, standard, CNCs):
    output1 = time_related_score(interpreted_chromosome, standard)
    #output2 = size_type_related_score(interpreted_chromosome, CNCs)

    '''    global INAPPROPRIATE_SIZE_COUNT
    global INAPPROPRIATE_TYPE_COUNT
    global LAST_JOB_EXECUTION
    global TOTAL_DELAYED_JOBS_COUNT
    global TOTAL_DELAYED_TIME
    TOTAL_DELAYED_TIME = 10000
    LAST_JOB_EXECUTION = 10000
    INAPPROPRIATE_TYPE_COUNT *= 10
    INAPPROPRIATE_SIZE_COUNT *= 2
    TOTAL_DELAYED_JOBS_COUNT *= 8'''

    scores = {}
    for k, v in output1.items():
        scores[k] = v
    #for k, v in output2.items():
    #    scores[k] = v

    return scores

def time_related_score(machines, standard):
    TOTAL_DELAYED_JOBS_COUNT = 0
    TOTAL_DELAYED_TIME = 0
    LAST_JOB_EXECUTION = 0
    output = {}
    for m in machines.values():
        component_start_time = standard
        component_end_time = component_start_time
        #time_left_of_machine = sum([j.getTime() for j in m])
        time_left_of_machine = 0

        for u in m:
            #each_job_execution_time += j.getTime()
            times = []
            j = u.get_job()
            for comp in j.getComponent():
                time = []
                time_taken = comp.getTime()
                component_end_time = component_start_time + time_taken
                startTime = datetime.datetime.fromtimestamp(int(component_start_time)).strftime('%Y-%m-%d %H:%M:%S')
                endTime = datetime.datetime.fromtimestamp(int(component_end_time)).strftime('%Y-%m-%d %H:%M:%S')
                time.append(startTime)
                time.append(endTime)
                times.append(time)
                component_start_time = component_end_time
                time_left_of_machine += time_taken

            u.set_times(times)
            diff = j.getDue() - component_end_time
            #time_left_of_machine += j.getTime()
            if diff < 0:
                TOTAL_DELAYED_JOBS_COUNT += 1
                TOTAL_DELAYED_TIME += (-1) * diff

        if time_left_of_machine > LAST_JOB_EXECUTION :
            LAST_JOB_EXECUTION = time_left_of_machine


    output['jobs'] = int(TOTAL_DELAYED_JOBS_COUNT)
    output['time'] = int(TOTAL_DELAYED_TIME / (3600))
    output['last'] = int(LAST_JOB_EXECUTION / (3600))

    return output

def start(job_pool, machines, CNCs, standard):
    interpreted = assign(machines, job_pool, CNCs)
    scores = evaluate(interpreted, standard, CNCs)
    print(scores['jobs'])
    print(scores['time'])
    print(scores['last'])