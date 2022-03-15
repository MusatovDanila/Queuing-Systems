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

def bmatrix(b):
    #b is ndarray of numpy
    """Returns a LaTeX bmatrix

    :a: numpy array
    :returns: LaTeX bmatrix as a string
    """
    a = np.asarray(b)
    if len(a.shape) > 2:
        raise ValueError('bmatrix can at most display two dimensions')
    temp_string = np.array2string(a, formatter={'float_kind':lambda x: "{:.5f}".format(x)})
    
    lines = temp_string.replace('[', '').replace(']', '').splitlines()
    rv = [r'$\begin{pmatrix}']
    rv += ['  ' + ' & '.join(l.split()) + r'\\' for l in lines]
    rv +=  [r'\end{pmatrix}$']
    return '\n'.join(rv)

def savetable(array,numberOfTable):
    table = Texttable()

    table.set_cols_align(["c"] * len(array[0]))
    table.set_cols_dtype(['t'] * len(array[0]))
    table.set_deco(Texttable.HEADER | Texttable.VLINES | Texttable.HLINES)
    table.add_rows(array)

    path = "C:/Users/Danila/Documents/Study/7 semestor/Queuing systems/2-nd lab/Report/table_" + str(numberOfTable) + ".tex"
    my_file = open(path, 'w+')
    my_file.write(latextable.draw_latex(table))
    my_file.close()

def gen_wait_time(lambda_m):
    return round(np.random.exponential(1/lambda_m),5)

def gen_serv_time(myu):
    return round(np.random.exponential(1/myu),5)

class SMO:
    def __init__(self,m_flag,m_delt_T=0,m_delt_proc=0,m_lambda=0,m_myu=0):
        self.active_app=1 #номер заявки обрабатываемой СМО(следующей на покидание СМО)
        self.event_counter=1 #счётчик событий
        self.flag=m_flag #Флаг - вид СМО: 1(D,M,1); 2(M,D,1); 3(M,M,1)
        self.SMO_table=[] #Таблица данных СМО
        self.queue=[] #очередь заявок по номерам в СМО
        self.SMO_counter_app=1 #количество заявок в СМО
        self.m_Application=[] #список заявок
        self.SMO_condition=[0,1]
        self.idle_time=0 #время простоя
        self.SMO_counter_avr=self.SMO_counter_app #параметр для нахождения среднего числа заявок в СМО
        if self.flag==1:
            if m_delt_T==0 or m_myu==0:
                print("incorrect parameters entered")
                return 
            self.delt_T=m_delt_T #постоянное время ожидания заявки
            self.myu_m=m_myu #параметр для генерации времени обслуживания заявки по закону показательного распределения 
            self.time_event_now=m_delt_T #время текущего события
            self.wait_app_time=m_delt_T #оставшееся время ожидания заявки
            self.remaining_time=round(gen_serv_time(self.myu_m),5) #оставшееся время обслуживания(в момент инициализации равно времени обслуживания)
            self.m_Application.append(Appliccation(round(self.time_event_now,5),0,round(self.time_event_now,5),round(self.remaining_time,5)))
            self.SMO_table.append([self.event_counter,round(self.time_event_now,5),1,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),self.active_app]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии
            return 
        elif self.flag==2:
            if m_delt_proc==0 or m_lambda==0:
                print("incorrect parameters entered")
                return 
            self.delt_proc=m_delt_proc #постоянное время обслуживания заявки
            self.lambda_m=m_lambda #параметр для генерации времени ожидания заявки по закону показательного распределения 
            self.wait_app_time=round(gen_wait_time(self.lambda_m),5) #оставшееся время ожидания заявки(в момент инициализации равно времени ожидания)
            self.time_event_now=self.wait_app_time #время текущего события
            self.remaining_time=m_delt_proc #оставшееся время обслуживания
            self.m_Application.append(Appliccation(round(self.time_event_now,5),0,round(self.time_event_now,5),round(self.remaining_time,5)))
            self.SMO_table.append([self.event_counter,round(self.time_event_now,5),1,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),self.active_app]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии
            return 
        elif self.flag==3:
            if m_lambda==0 or m_myu==0:
                print("incorrect parameters entered")
                return 
            self.lambda_m=m_lambda #параметр для генерации времени ожидания заявки по закону показательного распределения 
            self.myu_m=m_myu #параметр для генерации времени обслуживания заявки по закону показательного распределения 
            self.wait_app_time=round(gen_wait_time(self.lambda_m),5) #оставшееся время ожидания заявки(в момент инициализации равно времени ожидания)
            self.remaining_time=round(gen_serv_time(self.myu_m),5) #оставшееся время обслуживания(в момент инициализации равно времени обслуживания)
            self.time_event_now=self.wait_app_time #время текущего события
            self.m_Application.append(Appliccation(round(self.time_event_now,5),0,round(self.time_event_now,5),round(self.remaining_time,5)))
            self.SMO_table.append([self.event_counter,round(self.time_event_now,5),1,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),self.active_app]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии
            return 
        else: 
            print("m_flag - incorrect parameters entered")
            return 
        
    def gen_event(self):
        if self.flag==1:
            if self.remaining_time>self.wait_app_time:#заявка придёт раньше, чем предыдущая закончит обрабатываться
                self.time_event_now+=self.wait_app_time 
                self.event_counter+=1
                self.remaining_time-=self.wait_app_time
                self.wait_app_time=self.delt_T
                self.SMO_counter_app+=1
                if (self.SMO_counter_app+1)>len(self.SMO_condition):
                    self.SMO_condition.append(1)
                else:
                    self.SMO_condition[self.SMO_counter_app]+=1
                self.queue.append(len(self.m_Application)+1)
                self.SMO_counter_avr+=self.SMO_counter_app #параметр для нахождения среднего числа заявок в СМО
                self.m_Application.append(Appliccation(round(self.time_event_now,5),(len(self.queue)+1),-1,-1))
                self.SMO_table.append([self.event_counter,round(self.time_event_now,5),1,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),len(self.m_Application)]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии 
            else: 
                #СМО закончила обрабатывать заявку и либо берёт из очереди, либо стоит и ждёт
                if len(self.queue)>0:
                    self.event_counter+=1
                    self.time_event_now+=self.remaining_time
                    self.wait_app_time-=self.remaining_time
                    self.SMO_counter_app-=1
                    self.SMO_condition[self.SMO_counter_app]+=1
                    helper=(self.queue).pop(0)
                    self.SMO_counter_avr+=self.SMO_counter_app #параметр для нахождения среднего числа заявок в СМО
                    self.remaining_time=round(gen_serv_time(self.myu_m),5) #оставшееся время обслуживания(в момент начала обслуживания равно времени обслуживания)
                    self.m_Application[helper-1].start_serv(round(self.time_event_now,5),round(self.remaining_time,5))
                    self.SMO_table.append([self.event_counter,round(self.time_event_now,5),2,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),self.active_app]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии 
                    self.active_app=helper
                elif self.remaining_time!=-1:
                    self.event_counter+=1
                    self.time_event_now+=self.remaining_time
                    self.wait_app_time-=self.remaining_time
                    self.SMO_counter_app-=1
                    self.SMO_condition[self.SMO_counter_app]+=1
                    self.remaining_time=-1 #оставшееся время обслуживания(в момент начала обслуживания равно времени обслуживания)
                    self.SMO_table.append([self.event_counter,round(self.time_event_now,5),2,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),self.active_app]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии 
                else:
                    self.idle_time+=self.wait_app_time
                    self.time_event_now+=self.wait_app_time 
                    self.event_counter+=1
                    self.SMO_counter_app+=1                    
                    self.SMO_condition[self.SMO_counter_app]+=1
                    self.SMO_counter_avr+=self.SMO_counter_app #параметр для нахождения среднего числа заявок в СМО
                    self.remaining_time=round(gen_serv_time(self.myu_m),5) #оставшееся время обслуживания(в момент начала обслуживания равно времени обслуживания)
                    self.wait_app_time=self.delt_T
                    self.m_Application.append(Appliccation(round(self.time_event_now,5),0,round(self.time_event_now,5),round(self.remaining_time,5)))
                    self.active_app=len(self.m_Application)
                    self.SMO_table.append([self.event_counter,round(self.time_event_now,5),1,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),self.active_app]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии
                
        elif self.flag==2:
            if self.remaining_time>self.wait_app_time:#заявка придёт раньше, чем предыдущая закончит обрабатываться
                self.time_event_now+=self.wait_app_time 
                self.event_counter+=1
                self.remaining_time-=self.wait_app_time
                self.wait_app_time=round(gen_wait_time(self.lambda_m),5) #оставшееся время ожидания заявки(в момент инициализации равно времени ожидания)
                self.SMO_counter_app+=1
                if (self.SMO_counter_app+1)>len(self.SMO_condition):
                    self.SMO_condition.append(1)
                else:
                    self.SMO_condition[self.SMO_counter_app]+=1
                self.SMO_counter_avr+=self.SMO_counter_app #параметр для нахождения среднего числа заявок в СМО
                self.queue.append(len(self.m_Application)+1)
                self.m_Application.append(Appliccation(round(self.time_event_now,5),(len(self.queue)+1),-1,-1))
                self.SMO_table.append([self.event_counter,round(self.time_event_now,5),1,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),len(self.m_Application)]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии 
            else: 
                #СМО закончила обрабатывать заявку и либо берёт из очереди, либо стоит и ждёт
                if len(self.queue)>0:
                    self.event_counter+=1
                    self.time_event_now+=self.remaining_time
                    self.wait_app_time-=self.remaining_time
                    self.SMO_counter_app-=1
                    self.SMO_condition[self.SMO_counter_app]+=1
                    self.SMO_counter_avr+=self.SMO_counter_app #параметр для нахождения среднего числа заявок в СМО
                    helper=(self.queue).pop(0)
                    self.remaining_time=self.delt_proc #оставшееся время обслуживания(в момент начала обслуживания равно времени обслуживания)
                    self.m_Application[helper-1].start_serv(round(self.time_event_now,5),round(self.remaining_time,5))
                    self.SMO_table.append([self.event_counter,round(self.time_event_now,5),2,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),self.active_app]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии 
                    self.active_app=helper
                elif self.remaining_time!=-1:
                    self.event_counter+=1
                    self.time_event_now+=self.remaining_time
                    self.wait_app_time-=self.remaining_time
                    self.SMO_counter_app-=1
                    self.SMO_condition[self.SMO_counter_app]+=1
                    self.remaining_time=-1 #оставшееся время обслуживания(в момент начала обслуживания равно времени обслуживания)
                    self.SMO_table.append([self.event_counter,round(self.time_event_now,5),2,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),self.active_app]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии 
                else:
                    self.idle_time+=self.wait_app_time
                    self.time_event_now+=self.wait_app_time 
                    self.event_counter+=1
                    self.SMO_counter_app+=1
                    self.SMO_condition[self.SMO_counter_app]+=1
                    self.SMO_counter_avr+=self.SMO_counter_app #параметр для нахождения среднего числа заявок в СМО
                    self.remaining_time=self.delt_proc #оставшееся время обслуживания(в момент начала обслуживания равно времени обслуживания)
                    self.wait_app_time=round(gen_wait_time(self.lambda_m),5) 
                    self.m_Application.append(Appliccation(round(self.time_event_now,5),0,round(self.time_event_now,5),round(self.remaining_time,5)))
                    self.active_app=len(self.m_Application)
                    self.SMO_table.append([self.event_counter,round(self.time_event_now,5),1,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),self.active_app]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии
                
        
        else:
            if self.remaining_time>self.wait_app_time:#заявка придёт раньше, чем предыдущая закончит обрабатываться
                self.time_event_now+=self.wait_app_time 
                self.event_counter+=1
                self.remaining_time-=self.wait_app_time
                self.wait_app_time=round(gen_wait_time(self.lambda_m),5) #оставшееся время ожидания заявки(в момент инициализации равно времени ожидания)
                self.SMO_counter_app+=1
                if (self.SMO_counter_app+1)>len(self.SMO_condition):
                    self.SMO_condition.append(1)
                else:
                    self.SMO_condition[self.SMO_counter_app]+=1
                self.SMO_counter_avr+=self.SMO_counter_app #параметр для нахождения среднего числа заявок в СМО
                self.queue.append(len(self.m_Application)+1)
                self.m_Application.append(Appliccation(round(self.time_event_now,5),(len(self.queue)+1),-1,-1))
                self.SMO_table.append([self.event_counter,round(self.time_event_now,5),1,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),len(self.m_Application)]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии 
            else: 
                #СМО закончила обрабатывать заявку и либо берёт из очереди, либо стоит и ждёт
                if len(self.queue)>0:
                    self.event_counter+=1
                    self.time_event_now+=self.remaining_time
                    self.wait_app_time-=self.remaining_time
                    self.SMO_counter_app-=1
                    self.SMO_condition[self.SMO_counter_app]+=1
                    self.SMO_counter_avr+=self.SMO_counter_app #параметр для нахождения среднего числа заявок в СМО
                    helper=(self.queue).pop(0)
                    self.remaining_time=round(gen_serv_time(self.myu_m),5) #оставшееся время обслуживания(в момент начала обслуживания равно времени обслуживания)
                    self.m_Application[helper-1].start_serv(round(self.time_event_now,5),round(self.remaining_time,5))
                    self.SMO_table.append([self.event_counter,round(self.time_event_now,5),2,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),self.active_app]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии 
                    self.active_app=helper
                elif self.remaining_time!=-1:
                    self.event_counter+=1
                    self.time_event_now+=self.remaining_time
                    self.wait_app_time-=self.remaining_time
                    self.SMO_counter_app-=1
                    self.SMO_condition[self.SMO_counter_app]+=1
                    self.remaining_time=-1 #оставшееся время обслуживания(в момент начала обслуживания равно времени обслуживания)
                    self.SMO_table.append([self.event_counter,round(self.time_event_now,5),2,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),self.active_app]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии 
                else:
                    self.idle_time+=self.wait_app_time
                    self.time_event_now+=self.wait_app_time 
                    self.event_counter+=1
                    self.SMO_counter_app+=1
                    self.SMO_condition[self.SMO_counter_app]+=1
                    self.SMO_counter_avr+=self.SMO_counter_app #параметр для нахождения среднего числа заявок в СМО
                    self.remaining_time=round(gen_serv_time(self.myu_m),5) #оставшееся время обслуживания(в момент начала обслуживания равно времени обслуживания)
                    self.wait_app_time=round(gen_wait_time(self.lambda_m),5) 
                    self.m_Application.append(Appliccation(round(self.time_event_now,5),0,round(self.time_event_now,5),round(self.remaining_time,5)))
                    self.active_app=len(self.m_Application)
                    self.SMO_table.append([self.event_counter,round(self.time_event_now,5),1,self.SMO_counter_app,round(self.remaining_time,5),round(self.wait_app_time,5),self.active_app]) #номер события, время события, тип события, кол-во заявок в СМО, оставщесяя время обработки, оставшееся время ожидания заявки, номер заявки виновной в событии
                
            
        return 1   
            
    def save_data(self):  
        Table_2=[]
        time_que_avr=0
        time_SMO_avr=0
        Table_3=[]
        j=0
        while 1:
            if (j<len(self.m_Application) and self.m_Application[j].time_end_serv!=-1):
                time_SMO_avr+=round((self.m_Application[j].time_end_serv-self.m_Application[j].time_coming),5)
                j+=1
            else:
                break
            
        for i in range(len(self.SMO_condition)):
            Table_3.append([i,round(self.SMO_condition[i]/self.event_counter,5)])
        for i in range(len(self.m_Application)):
            time_que_avr+=round(self.m_Application[i].time_in_queue,5)
            Table_2.append([i+1,round(self.m_Application[i].time_coming,5),self.m_Application[i].number_in_queue,round(self.m_Application[i].time_in_queue,5), round(self.m_Application[i].time_start_serv,5),round(self.m_Application[i].time_serv,5), round(self.m_Application[i].time_end_serv,5)])
       
        print("СМО имеет вид")
        if self.flag==1:
            savetable(self.SMO_table,1_1)
            savetable(Table_2,1_2)
            savetable(Table_3,1_3)
            print("(D|M|1)")
        elif self.flag==2:
            savetable(self.SMO_table,2_1)
            savetable(Table_2,2_2)
            savetable(Table_3,2_3)
            print("(M|D|1)")
        else:
            savetable(self.SMO_table,3_1)
            savetable(Table_2,3_2)
            savetable(Table_3,3_3)
            print("(M|M|1)")
        
        if self.SMO_table[self.event_counter-1][4]!=-1:
            j-=1     
        if self.SMO_table[self.event_counter-1][2]!=2 :
            time_SMO_avr-=round((self.m_Application[j].time_end_serv-self.m_Application[j].time_coming),5)
        
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
        print("\nкоэффициент простоя прибора:")
        print(round(self.idle_time/self.time_event_now,5))
        
        
            
class Appliccation:
    def __init__(self,m_time_coming,m_number_in_queue,m_time_start_serv, m_time_serv):
        self.time_coming=m_time_coming
        self.number_in_queue=m_number_in_queue
        if m_number_in_queue==0:
            self.time_in_queue=0
        else:
            self.time_in_queue=-1
        self.time_start_serv=m_time_start_serv
        self.time_serv=m_time_serv
        if m_time_start_serv==-1:
            self.time_end_serv=-1
        else:
            self.time_end_serv=m_time_start_serv+m_time_serv
    def start_serv(self,m_time_start_serv, m_time_serv):
        self.time_in_queue=m_time_start_serv-self.time_coming
        self.time_start_serv=m_time_start_serv
        self.time_serv=m_time_serv
        self.time_end_serv=m_time_start_serv+m_time_serv

def SMO_start(number_of_SMO, number_of_events, m_delt_T=0, m_delt_proc=0, m_lambda=0, m_myu=0):
    my_SMO=SMO(number_of_SMO, m_delt_T, m_delt_proc, m_lambda, m_myu)
    while my_SMO.event_counter<number_of_events:
        my_SMO.gen_event()
    my_SMO.save_data()
    return 1

delt_T=0.829
delt_process=0.843
lambda_m=1.082
myu=1.208

SMO_start(1,100,delt_T,delt_process,lambda_m,myu)

SMO_start(2,100,delt_T,delt_process,lambda_m,myu)

SMO_start(3,100,delt_T,delt_process,lambda_m,myu)