import matplotlib.pyplot as plt
import numpy as np
import math
import plotly.graph_objects as go
import copy
import xlsxwriter
import pandas as pd
from texttable import Texttable
from tabulate import tabulate
import latextable

def gen_wait_time(lambda_m):
    return round(np.random.exponential(1/lambda_m),5)

def gen_serv_time(myu):
    return round(np.random.exponential(1/myu),5)

def savetable(array,numberOfTable):
    table = Texttable()

    table.set_cols_align(["c"] * len(array[0]))
    table.set_cols_dtype(['t'] * len(array[0]))
    table.set_deco(Texttable.HEADER | Texttable.VLINES | Texttable.HLINES)
    table.add_rows(array)

    path = "C:/Users/Danila/Documents/Study/7 semestor/Queuing systems/1-st laba/Report/table_" + str(numberOfTable) + ".tex"
    my_file = open(path, 'w+')
    my_file.write(latextable.draw_latex(table))
    my_file.close()


def queuing_system(flag,delt_T=0,delt_proc=0,lambda_m=0,myu=0):
    if flag==1:
        if delt_T==0 or myu==0 :
            return 0
        event_counter=1
        time_serv=gen_serv_time(myu)
        counter_app=1
        time_event=delt_T
        time_app_now=delt_T
        QS_condition_after=1
        type_event=1
        remaining_time=time_serv
        time_end_serv=time_app_now+time_serv
        expectation_time_app=delt_T
        Table_1=[[event_counter,round(time_event,5),type_event,QS_condition_after,round(remaining_time,5),round(expectation_time_app,5)]]
        Table_2=[[round(counter_app,5),round(time_app_now,5),round(time_serv,5),round(time_end_serv,5)]]

        if remaining_time<delt_T:
            type_event=3
            QS_condition_after=0
            expectation_time_app=delt_T-remaining_time
            remaining_time=-1
            time_event+=time_serv
        else:
            type_event=2
            remaining_time-=delt_T
            expectation_time_app=delt_T
            counter_app+=1
            time_app_now+=delt_T
            time_event+=delt_T

        while event_counter<100:
            if type_event==1:
                event_counter+=1
                Table_1.append([event_counter,round(time_event,5),type_event,QS_condition_after,round(remaining_time,5),round(expectation_time_app,5)])
                Table_2.append([round(counter_app,5),round(time_app_now,5),round(time_serv,5),round(time_end_serv,5)])
                if remaining_time<delt_T:
                    type_event=3
                    QS_condition_after=0
                    expectation_time_app=delt_T-remaining_time
                    time_event+=remaining_time
                    remaining_time=-1
                else:
                    type_event=2
                    remaining_time-=delt_T
                    expectation_time_app=delt_T
                    counter_app+=1
                    time_app_now+=delt_T
                    time_event+=delt_T
            elif type_event==2:
                event_counter+=1
                Table_1.append([event_counter,round(time_event,5),type_event,QS_condition_after,round(remaining_time,5),round(expectation_time_app,5)])
                Table_2.append([round(counter_app,5),round(time_app_now,5),0,round(time_app_now,5)])
                if remaining_time<delt_T:
                    type_event=3
                    QS_condition_after=0
                    expectation_time_app=delt_T-remaining_time
                    time_event+=remaining_time
                    remaining_time=-1
                else:
                    type_event=2
                    remaining_time-=delt_T
                    expectation_time_app=delt_T
                    counter_app+=1
                    time_app_now+=delt_T
                    time_event+=delt_T
            else:
                event_counter+=1
                Table_1.append([event_counter,round(time_event,5),type_event,QS_condition_after,round(remaining_time,5),round(expectation_time_app,5)])
                time_serv=gen_serv_time(myu)
                time_event+=expectation_time_app
                type_event=1
                QS_condition_after=1
                remaining_time=time_serv
                expectation_time_app=delt_T
                time_app_now+=delt_T
                time_end_serv=time_app_now+time_serv
                counter_app+=1
        savetable(Table_1,1_1)
        savetable(Table_2,1_2)

    elif flag==2:
        
        if delt_proc==0 or lambda_m==0 :
            return 0
        event_counter=1
        time_serv=delt_proc
        counter_app=1
        time_event=gen_wait_time(lambda_m)
        time_app_now=time_event
        QS_condition_after=1
        type_event=1
        remaining_time=time_serv
        time_end_serv=time_app_now+time_serv
        expectation_time_app=gen_wait_time(lambda_m)
        Table_1=[[event_counter,round(time_event,5),type_event,QS_condition_after,round(remaining_time,5),round(expectation_time_app,5)]]
        Table_2=[[round(counter_app,5),round(time_app_now,5),round(time_serv,5),round(time_end_serv,5)]]

        if remaining_time<expectation_time_app:
            type_event=3
            QS_condition_after=0
            expectation_time_app-=remaining_time
            remaining_time=-1
            time_event+=time_serv
        else:
            type_event=2
            remaining_time-=expectation_time_app
            time_event+=expectation_time_app
            time_app_now+=expectation_time_app
            expectation_time_app=gen_wait_time(lambda_m)
            counter_app+=1

        while event_counter<100:
            if type_event==1:
                event_counter+=1
                Table_1.append([event_counter,round(time_event,5),type_event,QS_condition_after,round(remaining_time,5),round(expectation_time_app,5)])
                Table_2.append([round(counter_app,5),round(time_app_now,5),round(time_serv,5),round(time_end_serv,5)])
                if remaining_time<expectation_time_app:
                    type_event=3
                    QS_condition_after=0
                    expectation_time_app-=remaining_time
                    time_event+=remaining_time
                    remaining_time=-1
                else:
                    type_event=2
                    remaining_time-=expectation_time_app
                    time_event+=expectation_time_app
                    time_app_now+=expectation_time_app
                    expectation_time_app=gen_wait_time(lambda_m)
                    counter_app+=1

            elif type_event==2:
                event_counter+=1
                Table_1.append([event_counter,round(time_event,5),type_event,QS_condition_after,round(remaining_time,5),round(expectation_time_app,5)])
                Table_2.append([round(counter_app,5),round(time_app_now,5),0,round(time_app_now,5)])
                if remaining_time<expectation_time_app:
                    type_event=3
                    QS_condition_after=0
                    expectation_time_app-=remaining_time
                    time_event+=remaining_time
    
                    remaining_time=-1
                else:
                    type_event=2
                    remaining_time-=expectation_time_app
                    time_event+=expectation_time_app
                    time_app_now+=expectation_time_app
                    expectation_time_app=gen_wait_time(lambda_m)
                    counter_app+=1

            else:
                event_counter+=1
                Table_1.append([event_counter,round(time_event,5),type_event,QS_condition_after,round(remaining_time,5),round(expectation_time_app,5)])
                time_serv=delt_proc
                time_event+=expectation_time_app
                type_event=1
                QS_condition_after=1
                remaining_time=time_serv
                time_app_now=time_event
                time_end_serv=time_app_now+time_serv
                expectation_time_app=gen_wait_time(lambda_m)
                counter_app+=1
        savetable(Table_1,2_1)
        savetable(Table_2,2_2)


    elif flag==3:
        if myu==0 or lambda_m==0 :
            return 0
        event_counter=1
        time_serv=gen_serv_time(myu)
        counter_app=1
        time_event=gen_wait_time(lambda_m)
        time_app_now=time_event
        QS_condition_after=1
        type_event=1
        remaining_time=time_serv
        time_end_serv=time_app_now+time_serv
        expectation_time_app=gen_wait_time(lambda_m)
        Table_1=[[event_counter,round(time_event,5),type_event,QS_condition_after,round(remaining_time,5),round(expectation_time_app,5)]]
        Table_2=[[round(counter_app,5),round(time_app_now,5),round(time_serv,5),round(time_end_serv,5)]]

        if remaining_time<expectation_time_app:
            type_event=3
            QS_condition_after=0
            expectation_time_app-=remaining_time
            remaining_time=-1
            time_event+=time_serv
        else:
            type_event=2
            remaining_time-=expectation_time_app
            time_event+=expectation_time_app
            time_app_now+=expectation_time_app
            expectation_time_app=gen_wait_time(lambda_m)
            counter_app+=1

        while event_counter<100:
            if type_event==1:
                event_counter+=1
                Table_1.append([event_counter,round(time_event,5),type_event,QS_condition_after,round(remaining_time,5),round(expectation_time_app,5)])
                Table_2.append([round(counter_app,5),round(time_app_now,5),round(time_serv,5),round(time_end_serv,5)])
                if remaining_time<expectation_time_app:
                    type_event=3
                    QS_condition_after=0
                    expectation_time_app-=remaining_time
                    time_event+=remaining_time
                    remaining_time=-1
                else:
                    type_event=2
                    remaining_time-=expectation_time_app
                    time_event+=expectation_time_app
                    time_app_now+=expectation_time_app
                    expectation_time_app=gen_wait_time(lambda_m)
                    counter_app+=1

            elif type_event==2:
                event_counter+=1
                Table_1.append([event_counter,round(time_event,5),type_event,QS_condition_after,round(remaining_time,5),round(expectation_time_app,5)])
                Table_2.append([round(counter_app,5),round(time_app_now,5),0,round(time_app_now,5)])
                if remaining_time<expectation_time_app:
                    type_event=3
                    QS_condition_after=0
                    expectation_time_app-=remaining_time
                    time_event+=remaining_time
    
                    remaining_time=-1
                else:
                    type_event=2
                    remaining_time-=expectation_time_app
                    time_event+=expectation_time_app
                    time_app_now+=expectation_time_app
                    expectation_time_app=gen_wait_time(lambda_m)
                    counter_app+=1

            else:
                event_counter+=1
                Table_1.append([event_counter,round(time_event,5),type_event,QS_condition_after,round(remaining_time,5),round(expectation_time_app,5)])
                time_serv=gen_serv_time(myu)
                time_event+=expectation_time_app
                type_event=1
                QS_condition_after=1
                remaining_time=time_serv
                time_app_now=time_event
                time_end_serv=time_app_now+time_serv
                expectation_time_app=gen_wait_time(lambda_m)
                counter_app+=1
        savetable(Table_1,3_1)
        savetable(Table_2,3_2)


                                      
            
    else:
        print("Your input flag don`t exist")
            
            
    return 1        

delt_process=0.703
delt_T=0.688
lambda_m=1.451
myu=1.403

queuing_system(1,delt_T,delt_process,lambda_m,myu)
queuing_system(2,delt_T,delt_process,lambda_m,myu)
queuing_system(3,delt_T,delt_process,lambda_m,myu)