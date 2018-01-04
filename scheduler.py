from cnc import *
from job import *
import xlrd
import random
import numpy as np
import AccessDB
from itertools import permutations
import time

def read_CNCs(input, CNCs):
    workbook = xlrd.open_workbook(input)

    worksheet = workbook.sheet_by_name("기계정보")

    n_cols = worksheet.ncols
    n_rows = worksheet.nrows

    for i in range(2,41): #1, 2, 6, 8, 10, 16, 22번 cnc
        row = worksheet.row_values(i)
        number = str(row[1])
        if str(row[2]) == "2JAW":   #2JAW 면 shape이 0, 3JAW면 shape이 1
            shape = 0
        elif str(row[2]) == "3JAW":
            shape = 1
        type = str(row[3])
        size = str(row[4])

        if (size.find('~') == -1):
            continue
        ground = size.split('~')[0]
        ground = float(ground[1:])

        try :
            ceiling = float(size.split('~')[1])
        except ValueError :
            ceiling = 100.0
        cnc = CNC(number, ground, ceiling, shape, type)
        CNCs.append(cnc)

def is_digit(str):
   try:
     tmp = float(str)
     return True
   except ValueError:
     return False

def make_job_pool(job_pool):
    cursor1 = AccessDB.AccessDB()
    cursor2 = AccessDB.AccessDB()
    work_start = str(input("work date from : "))
    work_end = str(input("work date until: "))
    deli_start = str(input("delivery date from: "))
    deli_end = str(input("delivery date until: "))
    cursor1.execute("""
        select  w.workno, w.workdate, w.DeliveryDate, w.GoodCd,i.GoodCd as raw_materialCd, w.OrderQty,
		case when i.Class3 = '061038' then 0 else 1 end as Gubun,
		REPLACE(REPLACE(i.Spec, 'HEX.', ''),'HEX','') as Spec

	    from TWorkreport_Han_Eng w
	    inner join TGood i on w.Raw_Materialcd = i.GoodCd
	    where w.workdate between """ + work_start + """ and """ + work_end + """
	    and w.DeliveryDate between """ + deli_start + """ and """ + deli_end + """
	    and w.PmsYn = 'N'
	    and w.ContractYn = '1'
	    and i.Class2 not in ('060002', '060006')
	    and i.Class3 in ('061038', '061039')
        """)
    row = cursor1.fetchone()
    while row:
        GoodCd = row[3]
        cycle_time = [0,0,0]
        try :
            spec = float((row[7].split('-'))[0]) #숫자(-문자) 형식 아닌 spec이 나오면 무시
        except ValueError:
            row = cursor1.fetchone()
            continue
        Qty = row[5]
        Gubun = int(row[6])
        search_cycle_time(cursor2, cycle_time, GoodCd, Gubun)
        due_date = row[1]
        print(due_date)
        due_date_seconds = time.mktime((int(due_date[0:4]), int(due_date[4:6]), int(due_date[6:8]), 12, 0, 0, 0, 0, 0)) # 정오 기준
        print(due_date_seconds)
        newJob = Job(GoodCd, time = cycle_time, type = Gubun, quantity = Qty, due = due_date_seconds, size = spec)
        job_pool.appendleft(newJob)
        row = cursor1.fetchone()

def search_cycle_time(cursor, cycle_time, GoodCd, Gubun):
    flag1 = 0
    flag2 = 0
    if Gubun == 1:
        flag3 = 1
    elif Gubun == 0: # Gubun = 0 이면 3차 가공까지
        flag3 = 0

    cursor.execute("""
                    select  max(c.workdate) as workdate, j.DeliveryDate, j.GoodCd, j.OrderQty,
    		        -- ISNULL(c.Prodqty,0) + ISNULL(c.Errqty,0) as Qty,
    		        case when j.Class3 = '061038' then 0 else 1 end as Gubun,
                    REPLACE(REPLACE(j.Spec, 'HEX.', ''),'HEX','')  as Spec,
    			    c.Processcd, c.Cycletime , c.starttime, c.Endtime

    		        from  TWorkReport_CNC c 
    		        inner join
    				(
    				select  w.workno, /*, max(c.workdate) as workdate*/ w.DeliveryDate, w.GoodCd, w.OrderQty, i.Class3, i.Spec
    				from TWorkreport_Han_Eng w
    				inner join TGood i on w.Raw_Materialcd = i.GoodCd
    				where w.workdate between '20171201' and '20171220'
    				and w.DeliveryDate between '20171220' and '20171231'  
    				and w.PmsYn = 'N'
    				and w.ContractYn = '1'
    				and i.Class2 not in ('060002', '060006')
    				and i.Class3 in ('061038', '061039')
    				) j 
    				 on c.Goodcd = j.GoodCd
    				 where j.Goodcd = """ + GoodCd + """
                    group by j.Goodcd, c.workdate, j.workno, j.DeliveryDate, j.OrderQty, c.Cycletime, c.Processcd,c.starttime, c.Endtime, j.Class3, Spec

                    order by c.workdate DESC
                    """
                    )
    row = cursor.fetchone()
    while(row):
        processcd = row[6].strip()
        if processcd == 'P1' and flag1 == 0:
            cycle_time[0] = float(row[7])
            flag1 = 1
        elif processcd == 'P2' and flag2 == 0:
            cycle_time[1] = float(row[7])
            flag2 = 1
        elif processcd == 'P3' and flag3 == 0:
            cycle_time[2] = float(row[7])
            flag3 = 1
        if flag1 == 1 and flag2 == 1 and flag3 == 1:
            break
        row = cursor.fetchone()

def schedule(CNCs, job_pool, machines):
    total_delayed_time = 0
    total_delayed_jobs_count = 0
    last_job_execution = 0
    unAssigned = []
    for cnc in CNCs:
        machines[cnc.getNumber()] = list()

    avg_time = sum(list(job.getTime() for job in job_pool)) / len(job_pool)

    normPool = list()
    hexPool = list()
    splitPool(job_pool, normPool, hexPool)
    #normPool.sort(key=lambda x: x.getDue())
    #hexPool.sort(key=lambda x: x.getDue())
    normPool = permutation(normPool)
    hexPool = permutation(hexPool)
    # normPool = permutations(normPool,len(normPool))
    # hexPool = permutations(hexPool,len(hexPool))
    normCNCs = list(filter(lambda x: x.getShape() == 0, CNCs))
    hexCNCs = list(filter(lambda x: x.getShape() == 1, CNCs))
    # sortedNormPool = sorted(normPool, key = lambda j : j.getDue())
    # sortedHexPool = sorted(hexPool, key = lambda j: j.getDue())


    for i, j in enumerate(normPool):

        selected_CNCs = []
        for c in normCNCs:
            if c.getGround() <= j.getSize() <= c.getCeiling():  # size 맞는 CNC는 모두 찾음
                selected_CNCs.append(c)

        timeLefts = [sum([j.getTime() for j in machines[c.getNumber()]]) for c in selected_CNCs]
        if len(timeLefts) <= 0: #조건에 맞는 CNC가 하나도 없으면
            unAssigned.append(j)
            continue
        minValue = min(timeLefts)
        minIndex = timeLefts.index(minValue)
        cnc = selected_CNCs[minIndex]
        #cnc.enQ(j, in_progress=in_progress)
        (machines[cnc.getNumber()]).append(j)
        j.assignedTo(cnc)
        #ready_pool.appendleft(j)
        #job_pool.remove(j)
        notice = "a new job(" + str(j.getNumber()) + ") asggined to CNC #(" + \
                 str(cnc.getNumber()) + ")!\n"

        time_left_of_cnc = sum([j.getTime() for j in machines[cnc.getNumber()]])
        if last_job_execution < time_left_of_cnc:
            last_job_execution = time_left_of_cnc

        diff = j.getDue() - (time_left_of_cnc + j.getTime() + int(time.time()))
        if diff < 0:
            notice += "(" + str((-1) * diff) + "more time units needed to meet duetime)\n"
            total_delayed_jobs_count += 1
            total_delayed_time += (-1) * diff
        j.setMsg(notice)

    for i, j in enumerate(hexPool):
        selected_CNCs = []
        for c in hexCNCs:
            if (c.getGround() <= j.getSize() <= c.getCeiling()):  # size 맞는 CNC는 모두 찾음
                selected_CNCs.append(c)

                timeLefts = [sum([j.getTime() for j in machines[c.getNumber()]]) for c in selected_CNCs]
        minValue = min(timeLefts)
        minIndex = timeLefts.index(minValue)
        cnc = selected_CNCs[minIndex]
        #cnc.enQ(j, in_progress=in_progress)
        (machines[cnc.getNumber()]).append(j)
        j.assignedTo(cnc)
        #ready_pool.appendleft(j)
        #job_pool.remove(j)
        notice = "a new job(" + str(j.getNumber()) + ") asggined to CNC #(" + \
                 str(cnc.getNumber()) + ")!\n"

        time_left_of_cnc = sum([j.getTime() for j in machines[cnc.getNumber()]])
        if last_job_execution < time_left_of_cnc:
            last_job_execution = time_left_of_cnc

        diff = j.getDue() - (time_left_of_cnc + j.getTime() +  int(time.time()))
        if diff < 0:
            notice += "(" + str((-1) * diff) + "more time units needed to meet duetime)\n"
            total_delayed_jobs_count += 1
            total_delayed_time += (-1) * diff
        j.setMsg(notice)

    msg = [total_delayed_time, total_delayed_jobs_count, last_job_execution, machines]
    return msg


def assign(CNCs, job_pool, ready_pool, in_progress):  #CNC에 job들을 분배하는 함수

    total_delayed_time = 0
    total_delayed_jobs_count = 0
    last_job_execution = 0
    avg_time = sum(list(job.getTime() for job in job_pool)) / len(job_pool)

    normPool = []
    hexPool = []
    splitPool(job_pool,normPool,hexPool)
    normPool.sort(key = lambda x : x.getDue())
    hexPool.sort(key=lambda x: x.getDue())
    #normPool = permutations(normPool,len(normPool))
    #hexPool = permutations(hexPool,len(hexPool))
    normCNCs = list(filter(lambda x : x.getShape() == 0, CNCs))
    hexCNCs = list(filter(lambda x : x.getShape() == 1, CNCs))
   # sortedNormPool = sorted(normPool, key = lambda j : j.getDue())
    #sortedHexPool = sorted(hexPool, key = lambda j: j.getDue())



    for i,j in enumerate(normPool):

        selected_CNCs = []

        for c in normCNCs:
            if (float(c.getGround()) <= float(j.getSize()) < float(c.getCeiling())):  # size 맞는 CNC는 모두 찾음
                selected_CNCs.append(c)

        timeLefts = [c.get_timeLeft() for c in selected_CNCs]
        minValue = min(timeLefts)
        minIndex = timeLefts.index(minValue)
        cnc = selected_CNCs[minIndex]
        cnc.enQ(j, in_progress = in_progress)
        j.assignedTo(cnc)
        ready_pool.appendleft(j)
        job_pool.remove(j)
        notice = "a new job(" + str(j.getNumber()) + ") asggined to CNC #(" + \
                 str(cnc.getNumber()) + ")!\n"

        if last_job_execution < cnc.get_timeLeft():
            last_job_execution = cnc.get_timeLeft()
        diff = cnc.on_time(j)
        if  diff < 0:
            notice += "(" + str((-1)*diff) + "more time units needed to meet duetime)\n"
            total_delayed_jobs_count += 1
            total_delayed_time += (-1)*diff
        j.setMsg(notice)


    for i,j in enumerate(hexPool):
        selected_CNCs = []
        for c in hexCNCs:
            if (float(c.getGround()) <= float(j.getSize()) < float(c.getCeiling())):  # size 맞는 CNC는 모두 찾음
                selected_CNCs.append(c)

        timeLefts = [c.get_timeLeft() for c in selected_CNCs]
        minValue = min(timeLefts)
        minIndex = timeLefts.index(minValue)
        cnc = selected_CNCs[minIndex]
        cnc.enQ(j, in_progress=in_progress)
        ready_pool.appendleft(j)
        job_pool.remove(j)
        notice = "a new job(" + str(j.getNumber()) + ") asggined to CNC #(" + \
                 str(cnc.getNumber()) + ")!\n"

        if last_job_execution < cnc.get_timeLeft():
            last_job_execution = cnc.get_timeLeft()
        diff = cnc.on_time(j)
        if diff < 0:
            notice += "(" + str((-1) * diff) + "more time units needed to meet duetime)\n"
            total_delayed_jobs_count += 1
            total_delayed_time += (-1) * diff
        j.setMsg(notice)

    msg = [total_delayed_time, total_delayed_jobs_count, last_job_execution]
    return msg

def update(CNCs, unitTime, ready_pool, in_progress):
    for c in CNCs:
        try:
            job = c.get_jobQ()[-1]
        except IndexError as e:
            #print(e)
            continue
        for i in range(len(job.getSeries())):
            component = job.getComponent(i)
            if not component.ifDone():  #3개의 콤포넌트 중 아직 안끝난 것이 나오면
                component.spendTime(unitTime) #주어진 unitTime만큼 뺌
                break
            if(i == len(job.getSeries()) - 1):  ##마지막 콤포넌트까지 모두 done이면
                if(job.ifAllDone()): #job의 함수를 통해 한번더 검사하고
                    c.deQ() #job을 jobQ에서 뺀다.
                    in_progress.appendleft((c.get_jobQ())[-1]) #inprogress에 넣고
                    ready_pool.remove((c.get_jobQ())[-1]) #reaypool에서는 뺀다

def splitPool(job_pool, normPool, hexPool):

    for i,assignment in enumerate(job_pool):
        if assignment.getType() == 0:
            normPool.append(assignment)

        elif assignment.getType() == 1:
            hexPool.append(assignment)

    return 0

def permutation(pool):
    per = list()
    while(len(pool) != 0):
        i = random.randrange(0, len(pool))
        newElement =  pool.pop(i)
        per.append(newElement)
    return per