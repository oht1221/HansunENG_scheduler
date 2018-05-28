import time
import scheduler
import genetic
import cnc
import AccessDB
from collections import deque
import greedy

if __name__ == "__main__":
    CNCs = []
    JOB_POOL = deque()
    READY_POOL = deque()
    IN_PROGRESS = deque()

    TOTAL_NUMBER_OF_THE_POOL = scheduler.make_job_pool(JOB_POOL)
    scheduler.read_CNCs('./hansun2.xlsx', CNCs)


    machines = {}
    for cnc in CNCs:
        machines[float(cnc.getNumber())] = list()
    standard = input("schedule starts on : ")
    standard = (lambda x: int(time.time()) if (x == 'now') else time.mktime(
        (int(x[0:4]), int(x[4:6]), int(x[6:8]), 12, 0, 0, 0, 0, 0)))(standard)
    standard = int(standard)
    greedy.sort_pool(JOB_POOL)
    greedy.start(JOB_POOL, machines,CNCs, standard)