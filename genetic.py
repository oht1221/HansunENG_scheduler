import scheduler
import time
import AccessDB
import random
POPULATION = 10
chromosomes = list()

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
    offspring = list()
    not_selected = list(range(0, len(p2))) #p1에서
    for j in p1:
        offspring.append(j)
    for i in range(start, end+1):
        selected = p2.index(p1[i])
        not_selected.remove(selected)#여기서 선택 안된 것은 p2에서 선택할 것들
    i = end + 1
    print(not_selected)
    while 1:
        if i%len(p2) in not_selected:
            offspring[i%len(offspring)] = p2[i%len(p2)]
            not_selected.remove(i%len(p2))
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
        print(" -------------------------------------------- chromosome %d end -------------------------------------------- " % (i + 1))
        print("")
        for v in machines.values():  #각 machine에 있는 작업들 제거(초기화)
            v.clear()


def interpret(machines, chromosome):
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


def mutation(chromosome):
    return
def total_delayed_time(chromosome, machines):
    return
def total_delayed_jobs_count(chromosome):
    return
def last_job_execution(chromosome):
    return
def inappropriate_size_count(chromosome):
    return
def inappropriate_type_count(chromosome):
    return
def evaluate(chromosome):
    return
