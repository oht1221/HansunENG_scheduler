
import scheduler
import random

solution = list()

def genetic_algorithm(job_pool):
    cities = job_pool
    permutation(cities)





def permutation(pool):
    per = list()
    while(len(pool) != 0):
        i = random.randrange(0, len(pool))
        newElement =  pool[i]
        per.append(newElement)
    return per