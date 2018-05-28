from scheduler import *
import xlwt
import time
import datetime
import AccessDB
import numpy as np
import copy
import random
import math

POPULATION = list()
INTERPRETED_POPULATION = list()
POPULATION_NUMBER = 25
LAST_GENERATION = 10000
MUTATION_RATE = 0.1
DISPLAY_INTERVAL = 50
BEST10 = [None] * 10

'''
LAST_JOB_EXECUTION = 0
TOTAL_DELAYED_TIME = 0
TOTAL_DELAYED_JOBS_COUNT = 0
INAPPROPRIATE_SIZE_COUNT = 0
INAPPROPRIATE_TYPE_COUNT = 0
SCORE_AVG = 0
'''
def initialize_population(job_pool):
    for i in range(POPULATION_NUMBER):
        POPULATION.append(initial_permutation(job_pool))

def initial_permutation(pool):
    per = list()
    while (len(pool) != len(per)):
        i = random.randrange(0, len(pool))
        newElement = pool[i]
        if newElement in per:
            continue
        per.append(newElement)
    return per

def show_pool(machines, pool = None):
    if pool == None:
        pool = POPULATION
    for i, c in enumerate(pool):
        print(" -------------------------------------------- chromosome %d start -------------------------------------------- "%(i+1))
        for k, v in machines.items():
            newLine = 0
            print(k)
            for j in v:
                print(end='|  ')
                print(j.getWorkno(), end='  ')
                print(j.getGoodNum(), end=' (')
                for n in range(len(j.getSeries())):
                    print(j.getComponent(n).ifDone(), end=' ')
                print(end=') ')
                print(j.getTime(), end='  |')
                newLine = (newLine + 1) % 3
                if (newLine == 0): print(' ')
            print(' ')
            print('\n')
        print(" -------------------------------------------- chromosome %d end -------------------------------------------- " % (i + 1))
        print("")

def interpret1(machines, chromosome):
    for v in machines.values():  # 각 machine에 있는 작업들 제거(초기화)
        v.clear()
    position = 0
    i = 0
    machine_numbers = list(machines.keys())
    direction = 1
    while position < len(chromosome):
        try :
            machine = machines[machine_numbers[i]]
            machine.append(chromosome[position])
        except IndexError as e:
            print(e)
            break
        i, direction = choose_next_machine(i, direction, len(machines) - 1)
    interpreted = {}
    for k, v in machines.items():
        interpreted[k] = []
        for j in v:
            new = unit(j)
            interpreted[k].append(new)
    return interpreted

def interpret2(machines, chromosome, CNCs):
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

def choose_next_machine(machineIndex, direction, upper_limit):
    next_machine = machineIndex
    next_direction = direction #0도, 1도 아닌 값
    if direction == 1:
        next_machine = next_machine + 1
    elif direction == 0:
        next_machine = machineIndex - 1
    if next_machine > upper_limit:  # 맨 뒷자리 machine에 도달하면
        next_direction = 0  # 이동방향 전환
        next_machine = next_machine - 1  #
    elif next_machine < 0:  # 맨 앞자리 machine으로 돌아오면
        next_direction = 1
        next_machine = next_machine + 1

    return [next_machine, next_direction]

def splitPool(job_pool, normPool, hexPool):

    for i,assignment in enumerate(job_pool):
        if assignment.getType() == 0:
            normPool.append(assignment)

        elif assignment.getType() == 1:
            hexPool.append(assignment)

    return 0

def show_chromosome(chromosome, output):
    i = 0
    for j in chromosome:
        output.write('|  ')
        output.write(str(j.getWorkno()) + '  ')
        output.write(str(j.getGoodNum()) + ' (')
       #for n in range(len(j.getSeries())):
            #output.write(str(j.getComponent(n).ifDone()) + ' ')
        output.write(') ')
        output.write(str(j.getTime()) + '  |')
        i = (i + 1) % 3
        if (i == 0): output.write("\n")
    output.write("\n\n")

def show_chromosomes(output):
    for c in POPULATION:
        show_chromosome(c, output)
'''def next_generation(chromosomes):
    order_corssover(parent_1, parent_2, start, end)'''

def order_crossover(parent_1, parent_2, start, end):
    print("chromosome %2d X chromosome %2d" % (parent_1, parent_2))
    p1 = POPULATION[parent_1]
    p2 = POPULATION[parent_2]
    start = start
    end = end
    offspring = []
    for j in p1:
        offspring.append(j)
    not_selected = list(range(0, len(p2))) #p1에서
    for i in range(start, end+1):
        selected = p2.index(p1[i])
        not_selected.remove(selected)#여기서 선택 안된 것은 p2에서 선택할 것들
    i = end + 1
    j = end + 1
    while 1:
        if i%len(p2) in not_selected:
            offspring[j%len(offspring)] = p2[i%len(p2)]
            not_selected.remove(i%len(p2))
            j = j + 1
        i = i + 1
        if not not_selected:
            break
    mutation = np.random.choice(2, replace = False, p = [1 - MUTATION_RATE, MUTATION_RATE])
    if mutation == 1:
        inversion_mutation(offspring)
    return offspring

def inversion_mutation(chromosome):
    total = len(chromosome)
    interval = round(len(chromosome) / 3)
    start = random.randrange(0, total) #시작점 (왼쪽)
    end = start + interval - 1
    i = 0
    print(start)
    print(end)
    while i < (interval / 2):
        temp = chromosome[(start + i) % total]
        chromosome[(start + i) % total] = chromosome[(end - i) % total]
        chromosome[(end - i) % total] = temp
        i += 1
    return chromosome

def inversion_with_displacement_mutation(chromosome):
    position1 = random.randrange(0, len(chromosome))
    position2 = random.randrange(0, len(chromosome))

    temp = chromosome[position1]
    chromosome[position1] = chromosome[position2]
    chromosome[position2] = temp

    left1 = chromosome[position1 - 1]
    right1 = chromosome[position1 + 1 % len(chromosome)]
    chromosome[position1 - 1] = chromosome[position2 + 1]
    chromosome[position1 + 1  % len(chromosome)] = chromosome[position2 - 1]

    chromosome[position2 - 1] = right1
    chromosome[position2 + 1 % len(chromosome)] = left1

    return

def time_related_score(ichr, standard):
    TOTAL_DELAYED_JOBS_COUNT = 0
    TOTAL_DELAYED_TIME = 0
    LAST_JOB_EXECUTION = 0
    output = {}
    for m in ichr.values():
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

def size_type_related_score(machines, CNCs):
    INAPPROPRIATE_TYPE_COUNT = 0
    INAPPROPRIATE_SIZE_COUNT = 0
    output = {}
    for k, m in machines.items(): # machines 번호(key)와 ,포인터 반환
        for c in CNCs:
            if c.getNumber() == k: # 해당 번호의 CNC 찾고
                for j in m: #job과 CNC의 type이 일치하는지 확인
                    if j.getType() !=  c.getShape():
                        INAPPROPRIATE_TYPE_COUNT += 1
                    if j.getSize() < c.getGround() or j.getSize() > c.getCeiling():
                        INAPPROPRIATE_SIZE_COUNT += 1
                break

    output['type'] = INAPPROPRIATE_TYPE_COUNT
    output['size'] = INAPPROPRIATE_SIZE_COUNT
    return output

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
    #   scores[k] = v

    return scores

def next_generation(job_pool, machines, standard, CNCs, pool_size, genN):
    global BEST10
    global POPULATION
    global LAST_GENERATION
    global MUTATION_RATE
    DELAYED_TIMEs = []
    DELAYED_JOBSs = []
    LAST_JOBs = []
    TYPEs = []
    SIZEs = []
    new_population = []
    INTERPRETED_POPULATION.clear()

    if genN % DISPLAY_INTERVAL == 0:
        output1 = open("./results/generation_%d_result.txt"%genN, "w")
        output2 = xlwt.Workbook(encoding='utf-8')  # utf-8 인코딩 방식의 workbook 생성
        output2.default_style.font.height = 20 * 11  # (11pt) 기본폰트설정 다양한건 찾아보길
        font_style = xlwt.easyxf('font: height 280, bold 1;')  # 폰트 스타일 생성
    else :
        output1 = None
        output2 = None

    for i, chr in enumerate(POPULATION):
        INTERPRETED_POPULATION.append(interpret2(machines, chr, CNCs))

    for i, ichr in enumerate(INTERPRETED_POPULATION):
        scores = evaluate(ichr, standard, CNCs)
        DELAYED_TIME = scores['time']
        DELAYED_JOBS = scores['jobs']
        LAST_JOB = scores['last']
        #TYPE = scores['type']
        #SIZE = scores['size']
        DELAYED_JOBSs.append(DELAYED_JOBS)
        DELAYED_TIMEs.append(DELAYED_TIME)
        LAST_JOBs.append(LAST_JOB)
        #TYPEs.append(TYPE)
        #SIZEs.append(SIZE)

    if genN == 0:
        BEST10 = sorted(DELAYED_TIMEs, reverse= True)[0:10] #BEST10 초기화
        sorted(job_pool, key=lambda job: job.getDue(), reverse=True)
    else:
        update_best(DELAYED_TIMEs)

    #norm_DELAYED_JOBSs = invert_linear_normalize(DELAYED_JOBSs)
    norm_DELAYED_TIMEs = invert_sigma_normalize(DELAYED_TIMEs, 3)
    norm_LAST_JOBs = invert_sigma_normalize(LAST_JOBs, 3)
    #norm_TYPEs = invert_linear_normalize(TYPEs)
    #norm_SIZEs = invert_linear_normalize(SIZEs)

    Min = min(DELAYED_TIMEs)
    indexOfBest = DELAYED_TIMEs.index(Min)
    if output1 != None: #파일이 열려있으면
        print_score_output(output1, DELAYED_TIMEs, DELAYED_JOBSs, LAST_JOBs)
    if output2 != None:
        print_job_schedule(output2, indexOfBest, genN)

    weighted_sum = []
    for i in range(0, POPULATION_NUMBER):
        weighted_sum.append(norm_DELAYED_TIMEs[i] + norm_LAST_JOBs[i])
    PROB = calculate_prob(weighted_sum)
    '''-----starting reproduction-----'''
    chrN = 0
    while POPULATION_NUMBER > chrN:
        print(chrN)
        parents = np.random.choice(POPULATION_NUMBER, 2, replace=False, p=PROB)
        rate = 1 + 0.5 * float(genN / LAST_GENERATION) #crossover시 초반에는 50%를 보존, 최후에는 90% 보존
        p1 = parents[0]
        p2 = parents[1]
        end = np.random.choice(pool_size, 1)
        end = int(end[0])
        start = int(end - (pool_size) * 0.6 * rate)
        #end = int(start + pool_size / 2)

        offspring = order_crossover(p1, p2, start, end)
        new_population.append(offspring)
        chrN += 1
    '''----end reproduction-----'''

    POPULATION = new_population

def start(job_pool, machines, standard, CNCs, pool_size):
    genN = 0
    while genN <= LAST_GENERATION:
        next_generation(job_pool, machines, standard, CNCs, pool_size, genN)
        genN += 1

def print_job_schedule(output, indexOfMin, genN):
    schedule = INTERPRETED_POPULATION[indexOfMin]
    for key, value in schedule.items():
        row = 0
        worksheet = output.add_sheet(str(key))  # 시트 생성
        worksheet.write(row, 0, "작업지시서 번호")
        worksheet.write(row, 1, "공정")
        worksheet.write(row, 2, "품번")
        worksheet.write(row, 3, "시작")
        worksheet.write(row, 4, "종료")
        worksheet.write(row, 5, str(indexOfMin))
        row += 1
        for i, unit in enumerate(value):
            times = unit.get_times()
            job = unit.get_job()
            for j, time in enumerate(times):
                start = time[0]
                end = time[1]
                #start = comp.getStartDateTime()
                #end = comp.getEndDateTime()
                worksheet.write(row, 0, job.getWorkno())
                worksheet.write(row, 1, "P%d" % (j + 1))
                worksheet.write(row, 2, job.getGoodNum())
                worksheet.write(row, 3, start)
                worksheet.write(row, 4, end)
                row += 1
    output.save("./schedules/schedule%d.xls"%genN)  # 엑셀 파일 저장 및 생성
    return

def invert_linear_normalize(score):
    scaled = []
    avg = sum(score)
    avg /= len(score)
    minimum = min(score)
    for s in score:
        new = avg * (s - minimum) / (avg - minimum)
        scaled.append(new)
    for i, s in enumerate(score):
        scaled[i] = (1 / (1 + s))
    return scaled

def invert_sigma_normalize(score, c):
    scaled = []
    avg = sum(score) / len(score)
    sigma = np.std(score)
    for s in score:
        new = ((s - avg + c * sigma) / sigma) #standardization
        if new > 0:
            scaled.append(1 / (1 + new))
        else:
            scaled.append(0)
    return scaled

def print_score_output(output, delayed_times, delayed_jobs, last_job):
    global POPULATION
    for i in range(0, POPULATION_NUMBER):
        output.write("------------------- chromosome %d -------------------\n" % (i + 1))
        #output.write("inappropriate_size_count: %d\n" % (sizes[i]))
        #output.write("inappropriate_type_count: %d\n" % (types[i]))
        output.write("last_job_execution: %d\n" % (last_job[i]))
        output.write("total_delayed_jobs_count: %d\n" % (delayed_jobs[i]))
        output.write("total_delayed_time: %d\n" % (delayed_times[i]))
        output.write("------------------- chromosome %d -------------------\n" % (i + 1))
        output.write("\n")
    for b in BEST10:
        output.write(str(b))
        output.write("\n")
    return

def calculate_prob(delayed_times):
    SUM = sum(delayed_times)
    PROB = []
    for dt in delayed_times:
        PROB.append(dt/SUM)

    return PROB

def update_best(a):
    global BEST10
    Sorted = sorted(a)
    move = 1
    for i, s in enumerate(Sorted):
        if move == 0:
            break
        move = 0
        for j, b in enumerate(BEST10):
            if s >= b:
                if j == 0:
                    break
                BEST10[j - 1] = s
                # print(BEST10)
                break
            if j == len(BEST10) - 1:
                BEST10[len(BEST10) - 1] = s
                #print(BEST10)
            move += 1
    return