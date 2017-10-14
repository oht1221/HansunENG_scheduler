import classes
import xlrd
from collections import deque
import random
import numpy as np

def read_CNCs(input, CNCs):
    workbook = xlrd.open_workbook(input)

    worksheet = workbook.sheet_by_name("기계정보")

    n_cols = worksheet.ncols
    n_rows = worksheet.nrows

    for i in (2, 3, 7, 9, 10, 11,17, 23): #1, 2, 6, 8, 10, 16, 22번 cnc
        row = worksheet.row_values(i)
        number = str(row[1])
        if str(row[2]) == "2JAW":   #2JAW 면 shape이 0, 3JAW면 shape이 1
            shape = 0
        else :
            shape = 1
        type = str(row[3])
        size = str(row[4])

        if (size.find('~') == -1):
            continue
        ground = size.split('~')[0]
        ground = ground[1:]
        ceiling = size.split('~')[1]

        cnc = classes.CNC(number, ground, ceiling, shape, type)
        CNCs.append(cnc)

def calculate_cycle_time_avgs(input, item_numbers):
    workbook = xlrd.open_workbook(input)
    worksheet = workbook.sheet_by_name("품번별 싸이클 타임 정보")

    n_rows = worksheet.nrows

    cycle_time_sums = {}
    cycle_time_avgs = {}
    n = {}
    for j in item_numbers:
        cycle_time_sums[j] = [0,0,0]
        cycle_time_avgs[j] = [0,0,0]
        n[j] = [0,0,0]

    for i in range(1, n_rows):
        row = worksheet.row_values(i)
        for j in item_numbers:
            if str(row[0]) == j:

                if((row[9]) == 'P1    '):
                    (cycle_time_sums[j])[0] += row[12]
                    n[j][0] += 1

                elif((row[9]) == 'P2    '):
                    (cycle_time_sums[j])[1] += row[12]
                    n[j][1] += 1

                elif ((row[9]) == 'P3    '):
                    (cycle_time_sums[j])[2] += row[12]
                    (n[j])[2] += 1

                break

    for i in item_numbers:
        if ((n[i])[2] == 0):  #HEX BAR인 경우 2단계 공정까지밖에 없기 때문에 세번째 element 지움
            (cycle_time_sums[i]).pop(2)
            (cycle_time_avgs[i]).pop(2)
            (n[i]).pop(2)
        for j in range(len(n[i])):
            (cycle_time_avgs[i])[j] = (cycle_time_sums[i])[j] / (n[i])[j]


    return cycle_time_avgs

def make_to_do_list(input, item_numbers, cycle_time_avgs):

    to_do_list = deque()
    workbook = xlrd.open_workbook(input)
    worksheet1 = workbook.sheet_by_name("단조 사용 품번")
    worksheet2 = workbook.sheet_by_name("HEX BAR 사용 품번")
    n_rows1 = worksheet1.nrows
    n_rows2 = worksheet2.nrows


    for i in range(200):  #40개의 작업 만들어냄
        n = random.randrange(0, len(item_numbers)) # len(item_numbers)개의 일 종류
        quantity = random.randrange(50, 100)
        flag = 0
        for j in range(1, n_rows1):
            row = worksheet1.row_values(j)
            if str(row[4]) == item_numbers[n]:
                size = str(row[9])
                to_do_list.appendleft(classes.job(item_numbers[n], cycle_time_avgs[item_numbers[n]], 0, size, quantity))  # 단조 사용 품번은 type 0으로 설정
                flag = 1 #단조 사용품번에서 찾았으면  flag를 설정해서 다음 if문(HEX BAR 품번 찾는)을 무시하도록 함
                break

        if not flag: #단조 사용 품번에 없을 경우 HEX BAR 사용 품번으로 감
            for j in range(1, n_rows2):
                row = worksheet2.row_values(j)
                if str(row[4]) == item_numbers[n]:
                    size = str(row[9])
                    to_do_list.appendleft(classes.job(item_numbers[n], cycle_time_avgs[item_numbers[n]], 1, size, quantity))   # HEX BAR 사용 품번은 type 1로 설정
                    break
    return to_do_list


def assign(CNCs, to_do_list):  #CNC에 job들을 분배하는 함수
    for a in range(len(to_do_list)):
        assignment = to_do_list.pop()
        selected_CNCs = []
        for c in CNCs:
            if (float(c.getGround()) <= float(assignment.getSize()) < float(c.getCeiling())) \
                    and (c.getShape() == assignment.getType()):  #size 맞는 CNC는 모두 찾음
                selected_CNCs.append(c)


        if len(selected_CNCs) == 1: #cnc 1개만 size가 맞으면
            selected_CNCs[0].enQ(assignment)

        elif len(selected_CNCs) > 1: #복수개이면
            timeLefts = [c.get_timeLeft() for c in selected_CNCs]
            minValue = min(timeLefts)
            minIndex = timeLefts.index(minValue)
            #print("max index is : ", minIndex)
            cnc = selected_CNCs[minIndex]
            cnc.enQ(assignment)


def newJobs():
    return np.random.choice([0,1], 1, p = [0.9, 0.1])


def update(CNCs, unitTime):
    for c in CNCs:
        try:
            job = c.get_jobQ()[-1]
        except IndexError as e:
            print(e)
            continue
        for i in range(len(job.getSeries())):
            component = job.getComponent(i)
            if not component.ifDone():  #3개의 콤포넌트 중 아직 안끝난 것이 나오면
                component.spendTime(unitTime) #주어진 unitTime만큼 뺌
                break
            if(i == len(job.getSeries()) - 1):  ##마지막 콤포넌트까지 모두 done이면
                if(job.ifAllDone()): #job의 함수를 통해 한번더 검사하고
                    c.deQ() #job을 jobQ에서 뺀다.

