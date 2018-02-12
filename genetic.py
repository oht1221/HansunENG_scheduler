import scheduler
import time
import AccessDB
import random
POPULATION = 10
chromosomes = list()

def make_pool(job_pool):
    for i in range(POPULATION):
        chromosomes.append(initial_permutation(job_pool))

def initial_permutation(pool):
    per = list()
    while (len(pool) != len(per)):
        i = random.randrange(0, len(pool))
        newElement = pool[i]
        per.append(newElement)
    return per

def order_corssover(parent_1, parent_2, start, end):
    offspring = list()
    not_selected = parent_1
    for i in range(start, end+1):
        offspring[i] = parent_1[i]
        not_selected.remove(parent_1[i])
    i = end + 1
    while 1:
        if parent_2[i/len(parent_2)] in not_selected:
            offspring[i/len(parent_1)] = parent_2[i/len(parent_2)]
            not_selected.remove(parent_2[i/len(parent_2)])
        i = i + 1
        if not not_selected:
            break

    return offspring
def show_pool(machines):
    for c in chromosomes:
        interpret(machines, c)

def interpret(machines, chromosome):
    position = 0
    i = 0
    machines_numbers = list(machines.keys())
    direction = 1
    while position < len(chromosome):
        try :
            machines[machines_numbers[i]].append(chromosome[position])
        except IndexError as e:
            print(e)
            break
        position = position + 1
        i, direction = choose_next_machine(i, direction, len(machines) - 1)

    i = 0
    for m in machines.values():
        for j in m:
            i = (i + 1) % 5
            print(end='|  ')
            print(j.getWorkno(), end='  ')
            print(j.getGoodNum(), end=' (')
            for n in range(len(j.getSeries())):
                print(j.getComponent(n).ifDone(), end=' ')
            print(end=') ')
            print(j.getTime(), end='  |')
            if (i == 0): print(' ')
        print(' ')
        print('\n')


def choose_next_machine(machineIndex, direction, upper_limit):
    next_machine = machineIndex
    next_direction = machineIndex
    if direction == 1:
        next_machine = machineIndex + 1
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
        i = (i + 1) % 5
        print(end='|  ')
        print(j.getWorkno(), end='  ')
        print(j.getGoodNum(), end=' (')
        for n in range(len(j.getSeries())):
            print(j.getComponent(n).ifDone(), end=' ')
        print(end=') ')
        print(j.getTime(), end='  |')
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
