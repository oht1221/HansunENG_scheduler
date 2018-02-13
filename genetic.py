import scheduler
import time
import AccessDB
import copy
import random
POPULATION = 10
chromosomes = list()
LAST_JOB_EXECUTION = 0

def initialize_mating_pool(job_pool):
    for i in range(POPULATION):
        chromosomes.append(initial_permutation(job_pool))

def initial_permutation(pool):
    per = list()
    while (len(pool) != len(per)):
        i = random.randrange(0, len(pool))
        newElement = pool[i]
        if newElement in per:
            continue
        per.append(newElement)
    return per

def order_corssover(parent_1, parent_2, start, end):
    p1 = chromosomes[parent_1 - 1]
    p2 = chromosomes[parent_2 - 1]
    start = start - 1
    end = end - 1
    offspring = copy.copy(p1)
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
        pool = chromosomes
    for i, c in enumerate(pool):
        print(" -------------------------------------------- chromosome %d start -------------------------------------------- "%(i+1))
        interpret(machines, c)
        for k, v in machines.items():
            i = 0
            print(k)
            for j in v:
                print(end='|  ')
                print(j.getWorkno(), end='  ')
                print(j.getGoodNum(), end=' (')
                for n in range(len(j.getSeries())):
                    print(j.getComponent(n).ifDone(), end=' ')
                print(end=') ')
                print(j.getTime(), end='  |')
                i = (i + 1) % 3
                if (i == 0): print(' ')
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

    evaluate(machines, chromosome)

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

def show_chromosome(chromosome):
    i = 0
    for j in chromosome:

        print(end='|  ')
        print(j.getWorkno(), end='  ')
        print(j.getGoodNum(), end=' (')
        for n in range(len(j.getSeries())):
            print(j.getComponent(n).ifDone(), end=' ')
        print(end=') ')
        print(j.getTime(), end='  |')
        i = (i + 1) % 3
        if (i == 0): print(' ')
    print(' ')
    print('\n')

def show_chromosomes():
    for c in chromosomes:
        show_chromosome(c)
def next_generation(chromosomes):

    order_corssover(parent_1, parent_2, start, end)

def mutation(chromosome):
    return
def total_delayed_time(machines):
    return
def total_delayed_jobs_count(machines, standard):
    for m in machines:
        time_left_of_cnc = sum([j.getTime() for j in m])
        diff = j.getDue() - (time_left_of_cnc + j.getTime() + standard)
        print('----------')
        print(j.getDue())
        if diff < 0:
            notice += "(" + str((-1) * diff) + "more time units needed to meet duetime)\n"
            total_delayed_jobs_count += 1
            total_delayed_time += (-1) * diff
    return

def last_job_execution(machines):
    global LAST_JOB_EXECUTION
    for m in machines:
        time_left_of_cnc = sum([j.getTime() for j in m])
        if time_left_of_cnc > LAST_JOB_EXECUTION :
            LAST_JOB_EXECUTION = time_left_of_cnc
    return 0
def inappropriate_size_count(machines):

    return
def inappropriate_type_count(machines):
    return
def evaluate(machines):
    result1 = total_delayed_jobs_count(machines)
    result2 = total_delayed_jobs_count(machines)
    result3 = last_job_execution(machines)
    result4 = inappropriate_size_count(machines)
    result5 = inappropriate_type_count(machines)

    return [result1, result2, result3, result4, result5]
