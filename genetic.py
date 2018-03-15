from scheduler import *
import xlwt
import time
import datetime
import AccessDB
import numpy as np
import copy
import random

PROB = list()
POPULATION = list()
INTERPRETED_POPULATION = list()
POPULATION_NUMBER = 25
LAST_GENERATION = 20000
MUTATION_RATE = 0.1
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
        position = position + 1
        i, direction = choose_next_machine(i, direction, len(machines) - 1)
    interpreted = {}
    for k, v in machines.items():
        interpreted[k] = []
        for j in v:
            interpreted[k].append(j)
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
            interpreted[k].append(j)
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

    return offspring

def inversion_mutation(chromosome):
    position = random.randrange(0, len(chromosome))
    left = chromosome[(position - 1) % len(chromosome)]
    chromosome[(position - 1) % len(chromosome)] = chromosome[(position + 1) % len(chromosome)]
    chromosome[(position + 1) % len(chromosome)] = left

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

def time_related_score(machines, standard):
    TOTAL_DELAYED_JOBS_COUNT = 0
    TOTAL_DELAYED_TIME = 0
    LAST_JOB_EXECUTION = 0
    output = {}
    for m in machines.values():
        each_job_execution_time = standard
        #time_left_of_machine = sum([j.getTime() for j in m])
        time_left_of_machine = 0

        for j in m:
            component_start_time = each_job_execution_time
            each_job_execution_time += j.getTime()
            time_left_of_machine += j.getTime()
            diff = j.getDue() - each_job_execution_time
            for comp in j.getComponent():
                startTime = datetime.datetime.fromtimestamp(int(component_start_time)).strftime('%Y-%m-%d %H:%M:%S')
                endTime = datetime.datetime.fromtimestamp(int(component_start_time + comp.getTime())).strftime('%Y-%m-%d %H:%M:%S')
                #    datetime.datetime.min + datetime.timedelta(seconds = int(component_start_time + comp.getTime()))
                comp.setStartDateTime(startTime)
                comp.setEndDateTime(endTime)
                component_start_time += comp.getTime()

            if diff < 0:
                TOTAL_DELAYED_JOBS_COUNT += 1
                TOTAL_DELAYED_TIME += (-1) * diff
        if time_left_of_machine > LAST_JOB_EXECUTION :
            LAST_JOB_EXECUTION = time_left_of_machine


    output['jobs'] = TOTAL_DELAYED_JOBS_COUNT
    output['time'] = TOTAL_DELAYED_TIME
    output['last'] = LAST_JOB_EXECUTION

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
    output2 = size_type_related_score(interpreted_chromosome, CNCs)

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
    for k, v in output2.items():
        scores[k] = v

    return scores

def next_generation(machines, standard, CNCs, pool_size, genN):

    fitness_total = 0
    summ = 0
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
    PROB.clear()
    if genN % 1000 == 0:
        output1 = open("./results/generation_%d_result.txt"%genN, "w")
        output2 = xlwt.Workbook(encoding='utf-8')  # utf-8 인코딩 방식의 workbook 생성
        output2.default_style.font.height = 20 * 11  # (11pt) 기본폰트설정 다양한건 찾아보길
        font_style = xlwt.easyxf('font: height 280, bold 1;')  # 폰트 스타일 생성
    else :
        output1 = None
        output2 = None
    # 50의 배수 repetition마다 output 파일 생성

    for i, chr in enumerate(POPULATION):
        #output.write("------------------- chromosome %d -------------------\n" % (i + 1))
        #show_chromosome(chr, output)
        #output.write("------------------- chromosome %d -------------------\n\n"%(i+1))
        INTERPRETED_POPULATION.append(interpret1(machines, chr))

    for i, ichr in enumerate(INTERPRETED_POPULATION):
        scores = evaluate(ichr, standard, CNCs)
        DELAYED_TIME = 1 / (1 + scores['time'])
        DELAYED_JOBS = 1/ (1 + scores['jobs'])
        LAST_JOB = 1 / (1 + scores['last'])
        TYPE = 1 / (1 + scores['type'])
        SIZE = 1 / (1 + scores['size'])
        DELAYED_JOBSs.append(DELAYED_JOBS)
        DELAYED_TIMEs.append(DELAYED_TIME)
        LAST_JOBs.append(LAST_JOB)
        TYPEs.append(TYPE)
        SIZEs.append(SIZE)

    '''xcel로 아웃풋 만드는 부분'''
    if output2 != None and i == 0:
            schedule = ichr
            for key, value in schedule.items():
                worksheet = output2.add_sheet(str(key))  # 시트 생성
                row = print_job_schedule(0, worksheet)
                for i, job in enumerate(value):
                    row = print_job_schedule(row, worksheet, job)
            output2.save("schedule.xls")  # 엑셀 파일 저장 및 생성
        '''xcel로 아웃풋 만드는 부분'''
        if output1 != None: #파일이 열려있으면
            output1.write("------------------- chromosome %d -------------------\n" % (i + 1))
            output1.write("inappropriate_size_count: %d\n" % (INAPPROPRIATE_SIZE_COUNT))
            output1.write("inappropriate_type_count: %d\n" % (INAPPROPRIATE_TYPE_COUNT))
            output1.write("last_job_execution: %d\n" % (LAST_JOB_EXECUTION))
            output1.write("total_delayed_jobs_count: %d\n" % (TOTAL_DELAYED_JOBS_COUNT))
            output1.write("total_delayed_time: %d\n" % (TOTAL_DELAYED_TIME))
            output1.write("total_score: %d\n" % (score))
            output1.write("------------------- chromosome %d -------------------\n" % (i + 1))
            output1.write("\n")

    if output1 != None:
        output1.write("score average of the generation : %d\n" %(SCORE_AVG))

    for i, p in enumerate(PROB):
        if i != len(PROB) - 1:
            PROB[i] = PROB[i] / fitness_total
        else:
            PROB[i] = 1 - summ
        summ += PROB[i]
    '''-----starting reproduction-----'''
    chrN = 0
    while POPULATION_NUMBER > chrN:
        print(chrN)
        parents = np.random.choice(POPULATION_NUMBER, 2, replace=False, p=PROB)
        rate = 1 + 0.8 * float(genN / LAST_GENERATION) #crossover시 초반에는 50%를 보존, 최후에는 90% 보존
        p1 = parents[0]
        p2 = parents[1]
        end = np.random.choice(pool_size, 1)
        end = int(end[0])
        start = int(end - (pool_size * rate) * 0.5)
        #end = int(start + pool_size / 2)

        '''output.write("-------- crossover #%d --------\n"%rep + str(start + 1))
        output.write("\n" + str(end) + "\nparent 1 | parent 2 : %d | %d\n" %(p1+1, p2+1))
        output.write("\n-------- crossover #%d --------\n"%rep)'''
        offspring = order_crossover(p1, p2, start, end)
        new_population.append(offspring)
        chrN += 1
    '''----end reproduction-----'''
    POPULATION = new_population

def evolution(machines, standard, CNCs, pool_size):
    genN = 0
    while genN <= LAST_GENERATION:
        next_generation(machines, standard, CNCs, pool_size, genN)
        genN += 1

def print_job_schedule(row, worksheet, job = None):
    if row == 0:
        worksheet.write(row, 0, "작업지시서 번호")
        worksheet.write(row, 1, "공정")
        worksheet.write(row, 2, "품번")
        worksheet.write(row, 3, "시작")
        worksheet.write(row, 4, "종료")
        return row + 1

    row_move = 0
    for i, comp in enumerate(job.getComponent()):
        start = comp.getStartDateTime()
        end = comp.getEndDateTime()
        worksheet.write(row + i, 0, job.getWorkno())
        worksheet.write(row + i, 1, "P%d"%(i+1))
        worksheet.write(row + i, 2, job.getGoodNum())
        worksheet.write(row + i, 3, start)
        worksheet.write(row + i, 4, end)
        row_move += 1
    return row + row_move

def linearNormalize(score):
    avg = sum(score) / len(score)
    minimum = min(score)
    scaled = []
    for s in score:
        new = avg * (s - minimum) / (avg - minimum)
        scaled.append(new)

    return scaled

def print_score_output():
    return
