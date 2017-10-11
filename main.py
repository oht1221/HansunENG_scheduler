import time
import scheduler
import classes



CNCs = []
item_numbers = ['00015604', '00015606', '00015608', '00015609', '00015610', '00057515', '00015629', '00032905'] #품번
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
        time.sleep(1)

    for j in to_do_list:
        print(j.getNumber())
        print(j.getTime())
        print(j.getSize())
        print('\n')
    print("----------------------------------------------------------------------------")
    scheduler.update(CNCs, 1)

    i = (i + 1) % 500