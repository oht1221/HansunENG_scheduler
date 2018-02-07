import scheduler
import time
import AccessDB
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

def cross_over(chromosome):

def mutation(chromosome):

def total_delayed_time(chromosome):

def total_delayed_jobs_count(chromosome):

def last_job_execution(chromosome):

def inappropriate_size_count(chromosome:

def inappropriate_type_count(chromosome):

def evaluate(chromosome):

def interpret(machines, chromosome):
    position = 1
    Machines = machines.values()
    machineNo = 0
    direction = 1
    while machineNo < len(Machines):
        try :
            Machines[machineNo].append(chromosome[position])
        except IndexError as e:
            print(e)
            break
        position = position + 1
        choose_next_machine(machineNo, direction, len(Machines))
def check_if_last(chromosome):
    if chromosome
def choose_next_machine(machineNo, direction, upper_limit):
    if direction == 1:
        machineNo = machineNo + 1
    else:
        machineNo = machineNo - 1
    if machineNo >= upper_limit:  # 맨 뒷자리 machine에 도달하면
        direction = 0  # 이동방향 전환
        machineNo = machineNo - 1  #
    elif machineNo < 0:  # 맨 앞자리 machine으로 돌아오면
        direction = 1
        machineNo = machineNo + 1

def splitPool(job_pool, normPool, hexPool):

    for i,assignment in enumerate(job_pool):
        if assignment.getType() == 0:
            normPool.append(assignment)

        elif assignment.getType() == 1:
            hexPool.append(assignment)

    return 0
