import time
import scheduler
import classes



CNCs = []
item_numbers = ['00015604', '00015606', '00015608', '00015609', '00015610', '00057515', '00015629', '00032905', '00015875','00015991',
                '00016144', '00015914', '00016138', '00015921', '00016034', '00016145', '00016036', '00016146', '00016044', '00015887',
                '00016000', '00015935', '00016048', '00015845', '00015958', ] #품번
to_do_list = scheduler.deque()

scheduler.read_CNCs('./hansun2.xlsx', CNCs)
cycle_time_avgs = scheduler.calculate_cycle_time_avgs('./hansun2.xlsx', item_numbers)
to_do_list = scheduler.make_to_do_list('./hansun2.xlsx', item_numbers, cycle_time_avgs)
##while (1):
##    if(scheduler.newJobs()):
  ##      scheduler.assign(CNCs, to_do_list)
for j in to_do_list:
    print(j.getNumber())
    print(j.getTime())
    print(j.getSize())
    print('\n')

scheduler.assign(CNCs, to_do_list)
'''for 
c in CNCs:
c.print_info()'''
print(cycle_time_avgs ,'\n')
i = 0
while(1):

    if(i == 0):
        for c in CNCs:
            c.print_info()
            c.print_state()

        for j in to_do_list:
            print(j.getNumber())
            print(j.getTime())
            print(j.getSize())
            print('\n')
        print("----------------------------------------------------------------------------")
        time.sleep(1)



    scheduler.update(CNCs, 1)

    i = (i + 1) % 2000