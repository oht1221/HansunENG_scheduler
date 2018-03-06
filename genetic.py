import scheduler
import time
import AccessDB
import numpy as np
import copy
import random

PROB = list()
POPULATION = list()
INTERPRETED_POPULATION = list()
POPULATION_NUMBER = 20
LAST_JOB_EXECUTION = 0
TOTAL_DELAYED_TIME = 0
TOTAL_DELAYED_JOBS_COUNT = 0
INAPPROPRIATE_SIZE_COUNT = 0
INAPPROPRIATE_TYPE_COUNT = 0
SCORE_AVG = 0

def initialize_mating_pool(job_pool):
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

def order_crossover(parent_1, parent_2, start, end):
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

def interpret(machines, chromosome):
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
    interpreted = copy.deepcopy(machines)
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

def inversion_mutation(chromosome):
    position = random.randrange(0, len(chromosome))
    left = chromosome[position - 1]
    chromosome[position - 1] = chromosome[position + 1]
    chromosome[position + 1] = left

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
    global TOTAL_DELAYED_JOBS_COUNT
    global TOTAL_DELAYED_TIME
    global LAST_JOB_EXECUTION
    TOTAL_DELAYED_JOBS_COUNT = 0
    TOTAL_DELAYED_TIME = 0
    LAST_JOB_EXECUTION = 0

    for m in machines.values():
        each_job_execution_time = standard
        #time_left_of_machine = sum([j.getTime() for j in m])
        time_left_of_machine = 0

        for j in m:
            each_job_execution_time += j.getTime()
            time_left_of_machine += j.getTime()
            diff = j.getDue() - each_job_execution_time
            if diff < 0:
                TOTAL_DELAYED_JOBS_COUNT += 1
                TOTAL_DELAYED_TIME += (-1) * diff
        if time_left_of_machine > LAST_JOB_EXECUTION :
            LAST_JOB_EXECUTION = time_left_of_machine
    return

def size_type_related_score(machines, CNCs):
    global INAPPROPRIATE_TYPE_COUNT
    global INAPPROPRIATE_SIZE_COUNT
    INAPPROPRIATE_TYPE_COUNT = 0
    INAPPROPRIATE_SIZE_COUNT = 0

    for k, m in machines.items(): # machines 번호(key)와 ,포인터 반환
        for c in CNCs:
            if c.getNumber() == k: # 해당 번호의 CNC 찾고
                for j in m: #job과 CNC의 type이 일치하는지 확인
                    if j.getType() !=  c.getShape():
                        INAPPROPRIATE_TYPE_COUNT += 1
                    if j.getSize() < c.getGround() or j.getSize() > c.getCeiling():
                        INAPPROPRIATE_SIZE_COUNT += 1
                break

    return

def evaluate(interpreted_chromosome, standard, CNCs):

    time_related_score(interpreted_chromosome, standard)
    size_type_related_score(interpreted_chromosome, CNCs)

    global INAPPROPRIATE_SIZE_COUNT
    global INAPPROPRIATE_TYPE_COUNT
    global LAST_JOB_EXECUTION
    global TOTAL_DELAYED_JOBS_COUNT
    global TOTAL_DELAYED_TIME
    TOTAL_DELAYED_TIME /= 10000
    LAST_JOB_EXECUTION /= 10000


    score = INAPPROPRIATE_SIZE_COUNT + INAPPROPRIATE_TYPE_COUNT + LAST_JOB_EXECUTION \
            + TOTAL_DELAYED_JOBS_COUNT + TOTAL_DELAYED_TIME

    return score

def next_generation(machines, standard, CNCs, TOTAL_NUMBER_OF_THE_POOL, repetition):
    fitness_total = 0
    rep = 0
    summ = 0
    global POPULATION
    global SCORE_AVG
    SCORE_AVG = 0
    new_population = []
    INTERPRETED_POPULATION.clear()
    PROB.clear()
    output = open("./results/generation_%d_result.txt"%repetition, "w")

    for i, chr in enumerate(POPULATION):
        output.write("------------------- chromosome %d -------------------\n" % (i + 1))
        show_chromosome(chr, output)
        output.write("------------------- chromosome %d -------------------\n\n"%(i+1))
        INTERPRETED_POPULATION.append(interpret(machines, chr))
    for i, ichr in enumerate(INTERPRETED_POPULATION):
        score = evaluate(ichr, standard, CNCs)
        output.write("score : %d\n" % (score))
        SCORE_AVG += score
        output.write("------------------- chromosome %d -------------------\n"%(i+1))
        output.write("inappropriate_size_count: %d\n" %(INAPPROPRIATE_SIZE_COUNT))
        output.write("inappropriate_type_count: %d\n" %(INAPPROPRIATE_TYPE_COUNT))
        output.write("last_job_execution: %d\n" %(LAST_JOB_EXECUTION))
        output.write("total_delayed_jobs_count: %d\n" %(TOTAL_DELAYED_JOBS_COUNT))
        output.write("total_delayed_time: %d\n" %(TOTAL_DELAYED_TIME))
        output.write("total_score: %d\n" %(score))
        output.write("------------------- chromosome %d -------------------\n"%(i+1))
        output.write("\n")
        fitness = 1/score
        fitness_total = fitness_total + fitness
        PROB.append(fitness)

    SCORE_AVG = SCORE_AVG / POPULATION_NUMBER
    output.write("score average of the generation : %d\n" %(SCORE_AVG))
    #print("fitness_total : %lf" %(fitness_total))

    for i, p in enumerate(PROB):
        if i != len(PROB) - 1:
            PROB[i] = PROB[i] / fitness_total
        else:
            PROB[i] = 1 - summ
        summ += PROB[i]

    for p in PROB:
        output.write(str(p) + " | ")
    output.write("\n\n")

    while POPULATION_NUMBER > rep:
        parents = np.random.choice(POPULATION_NUMBER, 2, replace=False, p=PROB)
        p1 = parents[0]
        p2 = parents[1]
        start = np.random.choice(int(TOTAL_NUMBER_OF_THE_POOL / 2), 1)
        start = start[0]
        output.write("-------- crossover #%d --------\n"%rep + str(start + 1))
        end = start + int(TOTAL_NUMBER_OF_THE_POOL / 2)
        output.write("\n" + str(end) + "\nparent 1 | parent 2 : %d | %d\n" %(p1+1, p2+1))
        output.write("\n-------- crossover #%d --------\n"%rep)
        offspring = order_crossover(p1, p2, start, end)
        new_population.append(offspring)
        rep += 1

    POPULATION = new_population
