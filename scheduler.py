from cnc import *
from job import *
import xlrd
import random
import numpy as np
from itertools import permutations

def read_CNCs(input, CNCs):
    workbook = xlrd.open_workbook(input)

    worksheet = workbook.sheet_by_name("기계정보")

    n_cols = worksheet.ncols
    n_rows = worksheet.nrows

    for i in (2, 3, 7, 9, 10, 11,17, 23): #1, 2, 6, 8, 10, 16, 22번 cnc
        row = worksheet.row_values(i)
        number = str(row[1])
        if str(row[2]) == "2JAW":   #2JAW 면 shape이 0, 3JAW면 shape이 1
            shape = 0
        else :
            shape = 1
        type = str(row[3])
        size = str(row[4])

        if (size.find('~') == -1):
            continue
        ground = size.split('~')[0]
        ground = ground[1:]
        ceiling = size.split('~')[1]

        cnc = CNC(number, ground, ceiling, shape, type)
        CNCs.append(cnc)

def calculate_cycle_time_avgs(cycle_time_avgs, input, item_numbers):
    workbook = xlrd.open_workbook(input)
    worksheet = workbook.sheet_by_name("품번별 싸이클 타임 정보")

    n_rows = worksheet.nrows

    cycle_time_sums = {}
    n = {}

    for j in item_numbers:
        cycle_time_sums[j] = [0,0,0]
        cycle_time_avgs[j] = [0,0,0]
        n[j] = [0,0,0]

    for i in range(1, n_rows):
        row = worksheet.row_values(i)
        for j in item_numbers:
            if str(row[0]) == j:

                if((row[9]) == 'P1    '):
                    (cycle_time_sums[j])[0] += row[12]
                    n[j][0] += 1

                elif((row[9]) == 'P2    '):
                    (cycle_time_sums[j])[1] += row[12]
                    n[j][1] += 1

                elif ((row[9]) == 'P3    '):
                    (cycle_time_sums[j])[2] += row[12]
                    (n[j])[2] += 1

                break

    for i in item_numbers:
        if ((n[i])[2] == 0):  #HEX BAR인 경우 2단계 공정까지밖에 없기 때문에 세번째 element 지움
            (cycle_time_sums[i]).pop(2)
            (cycle_time_avgs[i]).pop(2)
            (n[i]).pop(2)
        for j in range(len(n[i])):
            (cycle_time_avgs[i])[j] = int( (cycle_time_sums[i])[j] / ((n[i])[j]  * 5 ) )


    return 0

def make_job_pool(job_pool, input, item_numbers, cycle_time_avgs, how_many):

    workbook = xlrd.open_workbook(input)
    worksheet1 = workbook.sheet_by_name("단조 사용 품번")
    worksheet2 = workbook.sheet_by_name("HEX BAR 사용 품번")
    n_rows1 = worksheet1.nrows
    n_rows2 = worksheet2.nrows


    for i in range(how_many):  #how_many개의 작업 만들어냄
        n = random.randrange(0, len(item_numbers)) # len(item_numbers)개의 일 종류
        quantity = random.randrange(50, 100)
        flag = 0
        for j in range(1, n_rows1):
            row = worksheet1.row_values(j)
            if str(row[4]) == item_numbers[n]:
                size = str(row[9])
                job_pool.appendleft(Job(item_numbers[n], cycle_time_avgs[item_numbers[n]], 0, size, quantity))  # 단조 사용 품번은 type 0으로 설정
                flag = 1 #단조 사용품번에서 찾았으면  flag를 설정해서 다음 if문(HEX BAR 품번 찾는)을 무시하도록 함
                break

        if not flag: #단조 사용 품번에 없을 경우 HEX BAR 사용 품번으로 감
            for j in range(1, n_rows2):
                row = worksheet2.row_values(j)
                if str(row[4]) == item_numbers[n]:
                    size = str(row[9])
                    job_pool.appendleft(Job(item_numbers[n], cycle_time_avgs[item_numbers[n]], 1, size, quantity))   # HEX BAR 사용 품번은 type 1로 설정
                    break
    return 0

def schedule(CNCs, job_pool, machines):
    total_delayed_time = 0
    total_delayed_jobs_count = 0
    last_job_execution = 0
    for cnc in CNCs:
        machines[cnc.getNumber()] = list()

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



    for i, j in enumerate(normPool):

        selected_CNCs = []
        for c in normCNCs:
            if (float(c.getGround()) <= float(j.getSize()) < float(c.getCeiling())):  # size 맞는 CNC는 모두 찾음
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
        notice = "a new job(" + str(j.getNumber()) + ") asggined to CNC #(" + \
                 str(cnc.getNumber()) + ")!\n"

        time_left_of_cnc = sum([j.getTime() for j in machines[cnc.getNumber()]])
        if last_job_execution < time_left_of_cnc:
            last_job_execution = time_left_of_cnc

        diff = j.getDue() - (time_left_of_cnc + j.getTime())
        if diff < 0:
            notice += "(" + str((-1) * diff) + "more time units needed to meet duetime)\n"
            total_delayed_jobs_count += 1
            total_delayed_time += (-1) * diff
        j.setMsg(notice)

    for i, j in enumerate(hexPool):
        selected_CNCs = []
        for c in hexCNCs:
            if (float(c.getGround()) <= float(j.getSize()) < float(c.getCeiling())):  # size 맞는 CNC는 모두 찾음
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
        notice = "a new job(" + str(j.getNumber()) + ") asggined to CNC #(" + \
                 str(cnc.getNumber()) + ")!\n"

        time_left_of_cnc = sum([j.getTime() for j in machines[cnc.getNumber()]])
        if last_job_execution < time_left_of_cnc:
            last_job_execution = time_left_of_cnc

        diff = j.getDue() - (time_left_of_cnc + j.getTime())
        if diff < 0:
            notice += "(" + str((-1) * diff) + "more time units needed to meet duetime)\n"
            total_delayed_jobs_count += 1
            total_delayed_time += (-1) * diff
        j.setMsg(notice)

    msg = [total_delayed_time, total_delayed_jobs_count, last_job_execution, machines]
    return msg


def assign(CNCs, job_pool, ready_pool, in_progress):  #CNC에 job들을 분배하는 함수

    total_delayed_time = 0
    total_delayed_jobs_count = 0
    last_job_execution = 0
    avg_time = sum(list(job.getTime() for job in job_pool)) / len(job_pool)

    normPool = []
    hexPool = []
    splitPool(job_pool,normPool,hexPool)
    normPool.sort(key = lambda x : x.getDue())
    hexPool.sort(key=lambda x: x.getDue())
    #normPool = permutations(normPool,len(normPool))
    #hexPool = permutations(hexPool,len(hexPool))
    normCNCs = list(filter(lambda x : x.getShape() == 0, CNCs))
    hexCNCs = list(filter(lambda x : x.getShape() == 1, CNCs))
   # sortedNormPool = sorted(normPool, key = lambda j : j.getDue())
    #sortedHexPool = sorted(hexPool, key = lambda j: j.getDue())



    for i,j in enumerate(normPool):

        selected_CNCs = []

        for c in normCNCs:
            if (float(c.getGround()) <= float(j.getSize()) < float(c.getCeiling())):  # size 맞는 CNC는 모두 찾음
                selected_CNCs.append(c)

        timeLefts = [c.get_timeLeft() for c in selected_CNCs]
        minValue = min(timeLefts)
        minIndex = timeLefts.index(minValue)
        cnc = selected_CNCs[minIndex]
        cnc.enQ(j, in_progress = in_progress)
        j.assignedTo(cnc)
        ready_pool.appendleft(j)
        job_pool.remove(j)
        notice = "a new job(" + str(j.getNumber()) + ") asggined to CNC #(" + \
                 str(cnc.getNumber()) + ")!\n"

        if last_job_execution < cnc.get_timeLeft():
            last_job_execution = cnc.get_timeLeft()
        diff = cnc.on_time(j)
        if  diff < 0:
            notice += "(" + str((-1)*diff) + "more time units needed to meet duetime)\n"
            total_delayed_jobs_count += 1
            total_delayed_time += (-1)*diff
        j.setMsg(notice)


    for i,j in enumerate(hexPool):
        selected_CNCs = []
        for c in hexCNCs:
            if (float(c.getGround()) <= float(j.getSize()) < float(c.getCeiling())):  # size 맞는 CNC는 모두 찾음
                selected_CNCs.append(c)

        timeLefts = [c.get_timeLeft() for c in selected_CNCs]
        minValue = min(timeLefts)
        minIndex = timeLefts.index(minValue)
        cnc = selected_CNCs[minIndex]
        cnc.enQ(j, in_progress=in_progress)
        ready_pool.appendleft(j)
        job_pool.remove(j)
        notice = "a new job(" + str(j.getNumber()) + ") asggined to CNC #(" + \
                 str(cnc.getNumber()) + ")!\n"

        if last_job_execution < cnc.get_timeLeft():
            last_job_execution = cnc.get_timeLeft()
        diff = cnc.on_time(j)
        if diff < 0:
            notice += "(" + str((-1) * diff) + "more time units needed to meet duetime)\n"
            total_delayed_jobs_count += 1
            total_delayed_time += (-1) * diff
        j.setMsg(notice)

    msg = [total_delayed_time, total_delayed_jobs_count, last_job_execution]
    return msg

def newJobs():
    return np.random.choice([0,1], 1, p = [0.9995, 0.0005])


def update(CNCs, unitTime, ready_pool, in_progress):
    for c in CNCs:
        try:
            job = c.get_jobQ()[-1]
        except IndexError as e:
            #print(e)
            continue
        for i in range(len(job.getSeries())):
            component = job.getComponent(i)
            if not component.ifDone():  #3개의 콤포넌트 중 아직 안끝난 것이 나오면
                component.spendTime(unitTime) #주어진 unitTime만큼 뺌
                break
            if(i == len(job.getSeries()) - 1):  ##마지막 콤포넌트까지 모두 done이면
                if(job.ifAllDone()): #job의 함수를 통해 한번더 검사하고
                    c.deQ() #job을 jobQ에서 뺀다.
                    in_progress.appendleft((c.get_jobQ())[-1]) #inprogress에 넣고
                    ready_pool.remove((c.get_jobQ())[-1]) #reaypool에서는 뺀다

def splitPool(job_pool, normPool, hexPool):

    for i,assignment in enumerate(job_pool):
        if assignment.getType() == 0:
            normPool.append(assignment)

        elif assignment.getType() == 1:
            hexPool.append(assignment)

    return 0

def permutation(pool):
    per = list()
    while(len(pool) != 0):
        i = random.randrange(0, len(pool))
        newElement =  pool.pop(i)
        per.append(newElement)
    return per