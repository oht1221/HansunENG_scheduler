import time
import scheduler
from collections import deque


CNCs = []
ITEM_NUMBERS = ['00015604', '00015606', '00015608', '00015609', '00015610', '00057515', '00015629', '00032905', '00015875','00015991',
                '00016144', '00015914', '00016138', '00015921', '00016034', '00016145', '00016036', '00016146', '00016044', '00015887',
                '00016000', '00015935', '00016048', '00015845', '00015958', ] #품번
JOB_POOL = deque()
CYCLE_TIME_AVGS = {}

scheduler.read_CNCs('./hansun2.xlsx', CNCs)
scheduler.calculate_cycle_time_avgs(CYCLE_TIME_AVGS, './hansun2.xlsx', ITEM_NUMBERS)
scheduler.make_job_pool(JOB_POOL, './hansun2.xlsx', ITEM_NUMBERS, CYCLE_TIME_AVGS, 200)  #시작할 때 200개 생성

for j in JOB_POOL:
    print(j.getNumber())
    print(j.getTime())
    print(j.getSize())
    print('\n')

scheduler.assign(CNCs, JOB_POOL)
'''for 
c in CNCs:
c.print_info()'''
print(CYCLE_TIME_AVGS ,'\n')
i = 0
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



    scheduler.update(CNCs, unitTime = 1)
    if(scheduler.newJobs()):
        scheduler.make_job_pool(JOB_POOL, './hansun2.xlsx', ITEM_NUMBERS, CYCLE_TIME_AVGS, 1)
     #   number = TO_DO_LIST[0].getNumber()
        cnc = scheduler.assign(CNCs, JOB_POOL)
    #    if(cnc):
     #       print("a new job(%s) asggined to CNC #(%s)!\n----------------------------------------------------------------------------" % (
     #           number, cnc.getNumber()))
     #   elif(not cnc):
     #       print("a new job(%s) can not be asggined\n----------------------------------------------------------------------------" % number)

    i = (i + 1) % 1000


