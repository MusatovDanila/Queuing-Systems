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

def savetable(array,numberOfTable):
    table = Texttable()

    table.set_cols_align(["c"] * len(array[0]))
    table.set_cols_dtype(['t'] * len(array[0]))
    table.set_deco(Texttable.HEADER | Texttable.VLINES | Texttable.HLINES)
    table.add_rows(array)

    path = "C:/Users/Danila/Documents/Study/7 semestor/Queuing systems/3-hd lab/Report/table_" + str(numberOfTable) + ".tex"
    my_file = open(path, 'w+')
    my_file.write(latextable.draw_latex(table))
    my_file.close()
    return

def gen_wait_time(lambda_m):
    return round(np.random.exponential(1/lambda_m),5)

def gen_serv_time(myu):
    return round(np.random.exponential(1/myu),5)

class SMO:
    def __init__(self,m_flag, n ,m_delt_T = 0,m_delt_proc = 0,m_lambda = 0,m_myu = 0):
        self.event_counter  =  1 #счётчик событий
        self.SMO_table  =  [] #Таблица данных СМО (Таблица 1)
        self.queue  =  [] #очередь заявок по номерам в СМО
        self.SMO_counter_app = 1 #количество заявок в СМО
        self.m_Application = [] #список заявок (Таблица 1)
        self.SMO_condition = [0,1]
        self.SMO_counter_avr = self.SMO_counter_app #параметр для нахождения среднего числа заявок в СМО
        self.quantity_Unit = n
        self.flag = m_flag
        self.units = []
        self.remaining_time_unit = [] #массив времени обработки заявки
        for i in range(n):
                self.remaining_time_unit.append(-1)
                self.units.append(Unit(m_flag,m_delt_proc,m_myu))
        self.remaining_time = self.units[0].start_work(0) #оставшееся время обслуживания(в момент инициализации равно времени обслуживания)
        self.remaining_time_unit[0] = self.remaining_time
        self.remaining_index = 0
        if self.flag == 1:
            if m_delt_T == 0 or m_myu == 0:
                print("incorrect parameters entered")
                return 
            self.delt_T = m_delt_T #постоянное время ожидания заявки
            self.time_event_now = m_delt_T #время текущего события
            self.wait_app_time = m_delt_T #оставшееся время ожидания заявки
            self.m_Application.append(Appliccation(round(self.time_event_now,5),0,round(self.time_event_now,5),round(self.remaining_time,5),self.remaining_index))
            self.SMO_table.append([self.event_counter,round(self.time_event_now,5),1,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),1]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии
            return 
        elif self.flag == 2:
            if m_delt_proc == 0 or m_lambda == 0:
                print("incorrect parameters entered")
                return 
            self.lambda_m  =  m_lambda #параметр для генерации времени ожидания заявки по закону показательного распределения 
            self.wait_app_time  =  gen_wait_time(self.lambda_m) #оставшееся время ожидания заявки(в момент инициализации равно времени ожидания)
            self.time_event_now  =  gen_wait_time(self.lambda_m) #время текущего события
            self.m_Application.append(Appliccation(round(self.time_event_now,5),0,round(self.time_event_now,5),round(self.remaining_time,5),self.remaining_index))
            self.SMO_table.append([self.event_counter,round(self.time_event_now,5),1,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),1]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии
            return 
        elif self.flag == 3:
            if m_lambda == 0 or m_myu == 0:
                print("incorrect parameters entered")
                return 
            self.lambda_m = m_lambda #параметр для генерации времени ожидания заявки по закону показательного распределения 
            self.wait_app_time = gen_wait_time(self.lambda_m) #оставшееся время ожидания заявки(в момент инициализации равно времени ожидания)
            self.time_event_now = gen_wait_time(self.lambda_m) #время текущего события
            self.m_Application.append(Appliccation(round(self.time_event_now,5),0,round(self.time_event_now,5),round(self.remaining_time,5),self.remaining_index))
            self.SMO_table.append([self.event_counter,round(self.time_event_now,5),1,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),1]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии
            return 
        else: 
            print("m_flag - incorrect parameters entered")
            return 
        
    def min_rem_time(self):
        min_v = max(self.remaining_time_unit)
        index = -1
        for i in range(self.quantity_Unit):
            if min_v >= self.remaining_time_unit[i] and self.remaining_time_unit[i] >= 0 :
                    min_v = self.remaining_time_unit[i]
                    index = i
        if min_v < 0:
            return -1,-1
        return min_v, index
    
    def need_q(self):
        check_free = min(self.remaining_time_unit)
        if check_free > 0: #количество заявок в СМО больше чем количество приборов
            self.queue.append(len(self.m_Application))
            return 0 , -1
        else:
            index = next(x[0] for x in enumerate(self.remaining_time_unit) if x[1] < 0)
            self.remaining_time_unit[index] = self.units[index].start_work(len(self.m_Application))
            return 1, index 

    
    def gen_event(self):
        if self.remaining_time > self.wait_app_time:#заявка придёт раньше, чем предыдущая закончит обрабатываться
            self.time_event_now += self.wait_app_time 
            self.event_counter += 1
            for i in range (self.quantity_Unit):
                self.remaining_time_unit[i] -= self.wait_app_time
            if self.flag == 1:
                self.wait_app_time = self.delt_T
            else:
                self.wait_app_time = gen_wait_time(self.lambda_m)
            self.SMO_counter_app += 1
            flag_free,index_free = self.need_q()
            if (self.SMO_counter_app+1) > len(self.SMO_condition):
                self.SMO_condition.append(1)
            else:
                self.SMO_condition[self.SMO_counter_app] += 1
            self.SMO_counter_avr += self.SMO_counter_app #параметр для нахождения среднего числа заявок в СМО
            if(flag_free == 0):
                self.m_Application.append(Appliccation(round(self.time_event_now,5),len(self.queue),-1,-1))
            else:
                self.m_Application.append(Appliccation(round(self.time_event_now,5),0,round(self.time_event_now,5),round(self.remaining_time_unit[index_free],5),index_free))
            self.remaining_time, self.remaining_index = self.min_rem_time()
            self.SMO_table.append([self.event_counter,round(self.time_event_now,5),1,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),len(self.m_Application)]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии 
        else: 
            #СМО закончила обрабатывать заявку и либо берёт из очереди, либо стоит и ждёт
            if len(self.queue) > 0: #тот прибор, который освободился берёт из очереди виновница заявка ушедшая
                self.event_counter += 1
                self.time_event_now += self.remaining_time
                self.wait_app_time -= self.remaining_time
                for i in range (self.quantity_Unit):
                    self.remaining_time_unit[i] -= self.remaining_time
                self.SMO_counter_app -= 1
                self.SMO_condition[self.SMO_counter_app] += 1
                helper = (self.queue).pop(0)
                self.remaining_time_unit[self.remaining_index] = self.units[self.remaining_index].start_work(helper)
                self.SMO_counter_avr += self.SMO_counter_app #параметр для нахождения среднего числа заявок в СМО
                self.m_Application[helper].start_serv(round(self.time_event_now,5),round(self.remaining_time_unit[self.remaining_index],5),self.remaining_index)
                self.remaining_time, self.remaining_index = self.min_rem_time()
                self.SMO_table.append([self.event_counter,round(self.time_event_now,5),2,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),helper+1]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии 
            elif self.remaining_time != -1:
                self.event_counter += 1
                self.time_event_now += self.remaining_time
                self.wait_app_time -= self.remaining_time
                for i in range  (self.quantity_Unit):
                    self.remaining_time_unit[i] -= self.remaining_time
                self.remaining_time_unit[self.remaining_index]=-1
                self.SMO_counter_app -= 1
                active_app = self.units[self.remaining_index].last_app()+1
                self.SMO_condition[self.SMO_counter_app] += 1
                self.remaining_time, self.remaining_index = self.min_rem_time()
                self.SMO_table.append([self.event_counter,round(self.time_event_now,5),2,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),active_app]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии 
            else:
                self.time_event_now += self.wait_app_time 
                self.event_counter += 1
                self.SMO_counter_app += 1                    
                self.SMO_condition[self.SMO_counter_app] += 1
                self.SMO_counter_avr += self.SMO_counter_app #параметр для нахождения среднего числа заявок в СМО
                active_app = len(self.m_Application)+1
                self.remaining_time = self.units[0].start_work(active_app) #оставшееся время обслуживания(в момент инициализации равно времени обслуживания)
                self.remaining_time_unit[0] = self.remaining_time
                self.remaining_index = 0
                if self.flag == 1:
                    self.wait_app_time = self.delt_T
                else:
                    self.wait_app_time = gen_wait_time(self.lambda_m) 
                self.m_Application.append(Appliccation(round(self.time_event_now,5),0,round(self.time_event_now,5),round(self.remaining_time,5), self.remaining_index))
                self.SMO_table.append([self.event_counter,round(self.time_event_now,5),1,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),active_app]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событи
        return 1   
    
    def save_data(self):  
        Table_2 = []
        time_que_avr = 0
        time_SMO_avr = 0
        Table_3 = [] 
        Table_4 = []
        j = 0
        App_stop_in_work = {}
      
        for i in range(len(self.m_Application) ):
            if self.m_Application[i].time_end_serv <= round(self.time_event_now,5)  and self.m_Application[i].time_end_serv != -1:
                time_SMO_avr += round((self.m_Application[i].time_end_serv-self.m_Application[i].time_coming),5)
                j += 1
            elif self.m_Application[i].time_end_serv!=-1:
                App_stop_in_work[self.m_Application[i].number_unit] = self.m_Application[i].time_end_serv-self.time_event_now  # для учёта непроработавшего времени приборов
        #print(j)
        
        
        for i in range(self.quantity_Unit):
            if i in App_stop_in_work.keys():
                Table_3.append([i+1,self.units[i].app_counter,round(self.units[i].work_time-App_stop_in_work[i],5),round((self.time_event_now-self.units[i].work_time+App_stop_in_work[i])/self.time_event_now,5)])
            else:
                Table_3.append([i+1, self.units[i].app_counter, round(self.units[i].work_time,5), round((self.time_event_now-self.units[i].work_time)/self.time_event_now, 5)])
        
        if self.flag != 3:
            for i in range(len(self.SMO_condition)):
                Table_4.append([i,round(self.SMO_condition[i]/self.event_counter,5)])
        else: 
            nyu=self.lambda_m/(self.quantity_Unit*self.units[0].myu)
            p=self.lambda_m/self.units[0].myu
            r_0 = (p**self.quantity_Unit)/(np.math.factorial(self.quantity_Unit)*(1-nyu))
            for i in range(self.quantity_Unit):
                r_0 += (p**i)/np.math.factorial(i)
            r_0 = 1/r_0
            r_k=[r_0]
            for i in range(1, len(self.SMO_condition)):
                if self.quantity_Unit >= i:
                    r_k.append((p**i)*r_0/np.math.factorial(i))
                else:
                    r_k.append((nyu**(i-self.quantity_Unit))*r_k[self.quantity_Unit])
            for i in range(len(self.SMO_condition)):
                Table_4.append([i, round(r_k[i],5), round(self.SMO_condition[i]/self.event_counter,5), round(np.fabs((self.SMO_condition[i]/self.event_counter)-r_k[i]),5)])
            
                    
        
        for i in range(len(self.m_Application)):
            time_que_avr += round(self.m_Application[i].time_in_queue,5)
            Table_2.append([i+1,round(self.m_Application[i].time_coming,5),self.m_Application[i].number_in_queue,round(self.m_Application[i].time_in_queue,5), round(self.m_Application[i].time_start_serv,5),round(self.m_Application[i].time_serv,5), round(self.m_Application[i].time_end_serv,5)])
       
        print("СМО имеет вид")
        if self.flag == 1:
            savetable(self.SMO_table,1_1)
            savetable(Table_2,1_2)
            savetable(Table_3,1_3)
            savetable(Table_4,1_4)
            print("(D|M|1)")
        elif self.flag == 2:
            savetable(self.SMO_table,2_1)
            savetable(Table_2,2_2)
            savetable(Table_3,2_3)
            savetable(Table_4,2_4)
            print("(M|D|1)")
        else:
            savetable(self.SMO_table,3_1)
            savetable(Table_2,3_2)
            savetable(Table_3,3_3)
            savetable(Table_4,3_4)
            print("(M|M|1)")
            
        print("\nчисло  заявок:")
        print(len(self.m_Application))    
        print("\nчисло полностью обслуженных заявок:")
        print(j)           
        print("\nсреднее число заявок в системе:")
        print(round(self.SMO_counter_avr/self.event_counter,5))
        print("\nсреднее время пребывания заявок в очереди:")
        print(round(time_que_avr/j,5))
        print("\nсреднее время пребывания заявок в СМО на интервале:")
        print(round(time_SMO_avr/j,5))
        
        
            
class Appliccation:
    def __init__(self,m_time_coming,m_number_in_queue,m_time_start_serv, m_time_serv, m_number_unit=-1):
        self.time_coming = m_time_coming
        self.number_in_queue = m_number_in_queue
        self.number_unit = m_number_unit
        if m_number_in_queue == 0:
            self.time_in_queue = 0
        else:
            self.time_in_queue = -1
        self.time_start_serv = m_time_start_serv
        self.time_serv = m_time_serv
        if m_time_start_serv == -1:
            self.time_end_serv = -1
        else:
            self.time_end_serv = m_time_start_serv+m_time_serv
    def start_serv(self,m_time_start_serv, m_time_serv, m_number_unit):
        self.time_in_queue = m_time_start_serv-self.time_coming
        self.time_start_serv = m_time_start_serv
        self.time_serv = m_time_serv
        self.number_unit = m_number_unit
        self.time_end_serv = m_time_start_serv+m_time_serv
        
class Unit:
    def __init__(self, m_flag, m_delt_proc = 0, m_myu = 0):
        self.numbers_app = []
        self.work_time = 0
        self.app_counter = 0 #счётчик заявок поступивших в прибор
        self.flag = m_flag #Флаг - вид СМО: 1(D,M,1); 2(M,D,1); 3(M,M,1)
        if m_flag  ==  2:
            self.delt_proc = m_delt_proc
        else:
            self.myu = m_myu
    def start_work(self, number_app):
        self.numbers_app.append(number_app)
        self.app_counter += 1
        if self.flag  ==  2:
            self.work_time += self.delt_proc
            return(self.delt_proc)
        else:
            work_time = gen_serv_time(self.myu)
            self.work_time += work_time
            return(work_time)
        
    def last_app(self):
        return self.numbers_app[len(self.numbers_app)-1]
                
        
def SMO_start(number_of_SMO, number_of_events, quantity_units, m_delt_T=0, m_delt_proc=0, m_lambda=0, m_myu=0):
    my_SMO=SMO(number_of_SMO, quantity_units,m_delt_T, m_delt_proc, m_lambda, m_myu)
    while my_SMO.event_counter<number_of_events:
        my_SMO.gen_event()
    my_SMO.save_data()
    return 1

def main():
    delt_T=0.21
    delt_process=2.468
    lambda_m=1.082
    myu=0.405
    n=13
    SMO_start(1, 100, n, delt_T, delt_process, lambda_m, myu)
    SMO_start(2, 100, n, delt_T, delt_process, lambda_m, myu)
    SMO_start(3, 100, n, delt_T, delt_process, lambda_m, myu)
    return 1

main()
    