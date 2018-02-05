    import scheduler
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

    def cross_over():

    def mutation():

    def total_delayed_time():

    def total_delayed_jobs_count():

    def last_job_execution():

    def evaluate():
