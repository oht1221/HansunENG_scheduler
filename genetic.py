import scheduler
import random
POPULATION = 10
chromosomes = [POPULATION]
scheduler.make_job_pool()
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

def cross_over(chrmosome):

def mutation(chrmosome):

def total_delayed_time(chrmosome):

def total_delayed_jobs_count(chrmosome):

def last_job_execution(chrmosome):

def evaluate(chrmosome):

def interpret(chromosome):
    chromosome
def splitPool(job_pool, normPool, hexPool):

    for i,assignment in enumerate(job_pool):
        if assignment.getType() == 0:
            normPool.append(assignment)

        elif assignment.getType() == 1:
            hexPool.append(assignment)

    return 0
