import time
import scheduler
import genetic
import cnc
import AccessDB
from collections import deque


CNCs = []
JOB_POOL = deque()
READY_POOL = deque()
IN_PROGRESS = deque()

scheduler.make_job_pool(JOB_POOL)
scheduler.read_CNCs('./hansun2.xlsx', CNCs)


machines = {}
for cnc in CNCs:
    machines[float(cnc.getNumber())] = list()

genetic.initialize_mating_pool(JOB_POOL)
genetic.show_pool(machines)
offspring1 = genetic.order_corssover(1,2,5,18)
offspring2 = genetic.order_corssover(3,4,13,26)
genetic.show_pool(machines,[offspring1, offspring2])

"""
while(1):
    machines= {}
    for cnc in CNCs:
        machines[float(cnc.getNumber())] = list()
    scheduler.initial_assignment(CNCs, machines)
    msg = scheduler.schedule(CNCs, JOB_POOL, machines)
    client = ''

    print("total sum of delay time : %d\n" % (msg[0]))
    print("total number of delayed jobs : %d\n" % (msg[1]))
    print("last job execution time : %d\n" % (msg[2]))
    for key in machines.keys():
        print("CNC No. : %s\n"% key)
        i = 0
        m = machines[key]
        for j in m:
            i = (i + 1) % 5
            print(end='|  ')
            print(j.getWorkno(), end = '  ')
            print(j.getGoodNum(), end=' (')
            for n in range(len(j.getSeries())):
                print(j.getComponent(n).ifDone(), end=' ')
            print(end=') ')
            print(j.getTime(), end='  |')
            if (i == 0): print(' ')
        print(' ')
        print('\n')

    while(1):
        client = input("Do you want another schedule? (y/n) ")
        if client == 'y':
            break
        if client == 'n':
            break
        else:
            print('Wrong input!\n')
    if client == 'y':
        #JOB_POOL = READY_POOL + IN_PROGRESS
        continue
    if client == 'n':
        break

"""
'''i = 0
while(1):

    if(i == 0):
        for c in CNCs:
            c.print_info()
            c.print_state()

        for j in JOB_POOL:
            print(j.getNumber())
             print(j.getTime())
            print(j.getType())
            print(j.getSize())
            print('\n')
        print("----------------------------------------------------------------------------")
        time.sleep(0.5)



    scheduler.update(CNCs, unitTime = 1, ready_pool = READY_POOL, in_progress = IN_PROGRESS)
    if(scheduler.newJobs()):
        scheduler.make_job_pool(JOB_POOL, './hansun2.xlsx', ITEM_NUMBERS, CYCLE_TIME_AVGS, 1)
     #   number = TO_DO_LIST[0].getNumber()
        cnc = scheduler.assign(CNCs, JOB_POOL, READY_POOL, IN_PROGRESS)
    #    if(cnc):
     #       print("a new job(%s) asggined to CNC #(%s)!\n----------------------------------------------------------------------------" % (
     #           number, cnc.getNumber()))
     #   elif(not cnc):
     #       print("a new job(%s) can not be asggined\n----------------------------------------------------------------------------" % number)

    i = (i + 1) % 1000'''