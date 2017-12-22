import time
import scheduler
import AccessDB
from collections import deque


CNCs = []
ITEM_NUMBERS = ['00015604', '00015606', '00015608', '00015609', '00015610', '00057515', '00015629', '00032905', '00015875','00015991',
                '00016144', '00015914', '00016138', '00015921', '00016034', '00016145', '00016036', '00016146', '00016044', '00015887',
                '00016000', '00015935', '00016048', '00015845', '00015958', ]
JOB_POOL = deque()
READY_POOL = deque()
IN_PROGRESS = deque()
CYCLE_TIME_AVGS = {}

AccessDB.AccessDB()

'''
scheduler.read_CNCs('./hansun2.xlsx', CNCs)
scheduler.calculate_cycle_time_avgs(CYCLE_TIME_AVGS, './hansun2.xlsx', ITEM_NUMBERS)
scheduler.make_job_pool(JOB_POOL, './hansun2.xlsx', ITEM_NUMBERS, CYCLE_TIME_AVGS, 150)

while(1):
    machines= {}
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
            print(j.getNumber(), end=' (')
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
        '''
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