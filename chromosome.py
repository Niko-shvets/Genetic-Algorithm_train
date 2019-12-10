import ga_params
import utils
from nodes import Customer as Node
from typing import List
import random
import numpy as np
import pandas as pd
#read file with trucks list
print('input trucks file: ')
tr=input()

veh=pd.read_csv('data/'+tr+'.csv')
print('trucks quantaty: ', len(veh))
veh=veh.astype(str)
#dictionary with trucks created
def vehicles_dic(data):
    vehicles=[]
    for i in range(1,len(data)+1):
        vehicles.append(i)
    dic={}
    for j in range(len(data)):
        #for k in vehicles:
        dic.update({vehicles[j]:(data.T)[j].tolist()})
    return dic
dic=vehicles_dic(veh)
for i in range(1,len(dic)+1):
    print('vehicle number: ',i, ',capacity: ', dic[i][0])
np.random.seed(42)
random.seed(42)
List_Node = List[Node]


class Chromosome:    
    route = []                  # type: list
    value = None                # type: float
#
    vehicles_count = None       # type: int
    vehicles_routes = None      # type: list
    route_rounds = None         # type: int
    total_travel_dist = None    # type: float
    total_elapsed_time = None   # type: float
    # deport is 0
    current_load_1 = None       # type: int
    current_load_2 = None       # type: int
    current_load_3 = None       # type: int
    current_load_4 = None       # type: int
    current_load_5 = None       # type: int
    current_load_6 = None       # type: int
    cap_dict = None             # type: dictionary
    elapsed_time = None         # type: float
    max_elapsed_time = None     # type: float
    distance_table = None       # type: list

    higher_value_fitter = False# для минимизации False, для максимизации True

    def __init__(self, route: iter):
        self.route = list(route)
        self.value = self.get_cost_score()

    def initial_port(self):
        self.vehicles_count = 1
        self.vehicles_routes = [[0]]
        self.route_rounds = 0
        self.total_travel_dist = 0
        self.total_elapsed_time = 0
        #assigment of capacity values for trucl compartment
        self.current_load_1 = int(dic[self.vehicles_count][0] if dic[self.vehicles_count][1]!=(0 or '0') else 0) 
        self.current_load_2 = int(dic[self.vehicles_count][0] if dic[self.vehicles_count][2]!=(0 or "0") else 0 )
        self.current_load_3 = int(dic[self.vehicles_count][0] if dic[self.vehicles_count][3]!=(0 or '0') else 0)
        self.current_load_4 = int(dic[self.vehicles_count][0] if dic[self.vehicles_count][4]!=(0 or '0')  else 0)
        self.current_load_5 = int(dic[self.vehicles_count][0] if dic[self.vehicles_count][5]!= (0 or '0') else 0)
        self.current_load_6 = int(dic[self.vehicles_count][0] if dic[self.vehicles_count][6]!=( 0 or '0') else 0) 
        self.cap_dict={1:self.current_load_1,2:self.current_load_2,3:self.current_load_3,4:self.current_load_4,5:self.current_load_5,6:self.current_load_6 }
        self.elapsed_time = 0
        self.max_elapsed_time = 0
# main static methods for distance, time calculation
    @staticmethod
    def get_distance(source: int, dest: int) -> float: 
        pass

    @staticmethod
    def get_node(index: int) -> Node:
        pass

    @staticmethod
    def get_travel_time(distance: float) -> float:
        return distance / ga_params.vehicle_speed_avg

    @staticmethod
    def get_travel_cost(distance: float) -> float:
        return distance * ga_params.vehicle_cost_per_dist
#method for time windows checking
    def check_time_and_go(self, source: int, dest: int, distance: float=None) -> bool:
        if distance is None:
            distance = self.get_distance(source, dest)
        dest_customer = self.get_node(dest)  # type: Node
        elapsed_new = self.get_travel_time(distance) + self.elapsed_time
        if elapsed_new <= dest_customer.due_time:
            return_time = self.get_travel_time(self.get_distance(dest, 0))
            deport_due_time = self.get_node(0).due_time
            if elapsed_new + dest_customer.service_time + return_time <= deport_due_time:
                self.move_vehicle(source, dest, distance=distance)
                return True
            else:
                return False
        else:
            return False


# check compartments capacity for each truck, must be more then 0 and
# check demand capacity i.e. (demand capacity - compartment capacity) > 0
# if at least for 1 compartment condition is True, then all method is True, else False
    def check_capacity(self, dest: int) -> bool:
        results=[]
        check_cap_92_1=0
        check_cap_92_2=0
        check_cap_95_1=0
        check_cap_95_2=0
        check_cap_98_1=0
        check_cap_98_2=0
        check_cap_DF_1=0
        check_cap_DF_2=0
        dest_customer = self.get_node(dest)# type: Node
        for i,j in zip(np.arange(1,len(self.cap_dict)+1),dic[self.vehicles_count][1:]):
            if j=='92':
                check_cap_92_1=self.cap_dict[i]-dest_customer.demand_92_1
                check_cap_92_2=self.cap_dict[i]-dest_customer.demand_92_2
            elif j=='95':
                check_cap_95_1=self.cap_dict[i]-dest_customer.demand_95_1
                check_cap_95_2=self.cap_dict[i]-dest_customer.demand_95_2
                
            elif j=='98':
                check_cap_98_1=self.cap_dict[i]-dest_customer.demand_98_1
                check_cap_98_2=self.cap_dict[i]-dest_customer.demand_98_2
                
            elif j=='DF':
                check_cap_DF_1=self.cap_dict[i]-dest_customer.demand_DF_1
                check_cap_DF_2=self.cap_dict[i]-dest_customer.demand_DF_2
            if ((self.cap_dict[i]!=0) and check_cap_92_1<=0) or ((self.cap_dict[i]!=0) and check_cap_92_2<=0) or \
            ((self.cap_dict[i]!=0) and check_cap_95_1<=0) or ((self.cap_dict[i]!=0) and check_cap_95_2<=0) or ((self.cap_dict[i]!=0) and check_cap_98_1<=0)\
            or ((self.cap_dict[i]!=0) and check_cap_98_2<=0) or ((self.cap_dict[i]!=0) and check_cap_DF_1<=0) or ((self.cap_dict[i]!=0) and check_cap_92_2<=0):
                results.append(True)
            else:
                results.append(False)
            #print('capacity: ',self.cap_dict)
        if any(results)==True:
            return True
        else:
            return False
#check demand for each AZS, if at least 1 demand>0, method is True
    def check_demand(self,dest:int) -> bool:
        dest_customer = self.get_node(dest)
        if dest_customer.demand_92_1!=0 or dest_customer.demand_92_2!=0 or dest_customer.demand_95_1!=0 or dest_customer.demand_95_2!=0 or dest_customer.demand_98_1!=0 or  dest_customer.demand_98_2!=0 or dest_customer.demand_DF_1!=0 or dest_customer.demand_DF_2!=0 :
            return True
        else:
            return False
    
    @staticmethod
    def get_vehicle_count_preference_cost(vehicles_count: int, deport_working_hours: int) -> float:
        # less_vehicles_preference * (vehicles_count) + less_deport_working_hours * (deport_working_hours)
        # vehicles_count_over_deport_hours_preference = less_vehicles_preference / less_deport_working_hours
        return ga_params.vehicles_count_over_deport_hours_preference * vehicles_count + deport_working_hours
# method for vehicle moving
# adding distance to total distance value and time penalties, adding routes.
# 
    def move_vehicle(self, source: int, dest: int, distance: float=None):
        dest_customer = self.get_node(dest)# add
        if distance is None:
            distance = self.get_distance(source, dest)
        self.total_travel_dist += distance
        self.elapsed_time += self.get_travel_time(distance)
        self.max_elapsed_time = max(self.elapsed_time, self.max_elapsed_time)
        self.vehicles_routes[-1].append(dest_customer.AZS_no) #add
        if dest == 0: # Depot
            self.route_rounds += 1 #new round
            # vehicle get loaded all compartment
            self.current_load_1 = int(dic[self.vehicles_count][0] if dic[self.vehicles_count][1]!=(0 or '0') else 0) 
            self.current_load_2 = int(dic[self.vehicles_count][0] if dic[self.vehicles_count][2]!=(0 or "0") else 0 )
            self.current_load_3 = int(dic[self.vehicles_count][0] if dic[self.vehicles_count][3]!=(0 or '0') else 0)
            self.current_load_4 = int(dic[self.vehicles_count][0] if dic[self.vehicles_count][4]!=(0 or '0')  else 0)
            self.current_load_5 = int(dic[self.vehicles_count][0] if dic[self.vehicles_count][5]!= (0 or '0') else 0)
            self.current_load_6 = int(dic[self.vehicles_count][0] if dic[self.vehicles_count][6]!=( 0 or '0') else 0 )
        else:
            dest_customer = self.get_node(dest)  # type: Node some AZS
            #check each demand, if AZS has 2 demand of 1 type fuel, then firstly will be loaded minimal demand
            # if truck loaded 1 compartment to AZS, then (compartment = 0), full drain condition  
            for i,j in zip(np.arange(1,len(self.cap_dict)+1),dic[self.vehicles_count][1:]):
                if j=='92':

                    if dest_customer.demand_92_1<dest_customer.demand_92_2 and dest_customer.demand_92_1>self.cap_dict[i]:
                        dest_customer.demand_92_1=dest_customer.demand_92_1-self.cap_dict[i]
                        self.cap_dict[i]=0
                    elif dest_customer.demand_92_1>dest_customer.demand_92_2 and dest_customer.demand_92_2>self.cap_dict[i]:
                        dest_customer.demand_92_2=dest_customer.demand_92_2-self.cap_dict[i]
                        self.cap_dict[i]=0
                    else:
                        if dest_customer.demand_92_1>self.cap_dict[i]:
                            dest_customer.demand_92_1=dest_customer.demand_92_1-self.cap_dict[i]
                            self.cap_dict[i]=0
                        if dest_customer.demand_92_2>self.cap_dict[i]:
                            dest_customer.demand_92_2=dest_customer.demand_92_2-self.cap_dict[i]
                            self.cap_dict[i]=0
                if j=='95':
                    if dest_customer.demand_95_1<dest_customer.demand_95_2 and dest_customer.demand_95_1>self.cap_dict[i]:
                        dest_customer.demand_95_1=dest_customer.demand_95_1-self.cap_dict[i]
                        self.cap_dict[i]=0
                    elif dest_customer.demand_95_1>dest_customer.demand_95_2 and dest_customer.demand_95_2>self.cap_dict[i]:
                        dest_customer.demand_95_2=dest_customer.demand_95_2-self.cap_dict[i]
                        self.cap_dict[i]=0
                    else:
                        if dest_customer.demand_95_1>self.cap_dict[i]:
                            dest_customer.demand_95_1=dest_customer.demand_95_1-self.cap_dict[i]
                            self.cap_dict[i]=0
                        if dest_customer.demand_95_2>self.cap_dict[i]:
                            dest_customer.demand_95_2=dest_customer.demand_95_2-self.cap_dict[i]
                            self.cap_dict[i]=0
                            
                if j=='98':
                    if dest_customer.demand_98_1<dest_customer.demand_98_2 and dest_customer.demand_98_1>self.cap_dict[i]:
                        dest_customer.demand_98_1=dest_customer.demand_98_1-self.cap_dict[i]
                        self.cap_dict[i]=0
                    elif dest_customer.demand_98_1>dest_customer.demand_98_2 and dest_customer.demand_98_2>self.cap_dict[i]:
                        dest_customer_demand_98_2=dest_customer.demand_98_2-self.cap_dict[i]
                        self.cap_dict[i]=0
                    else:
                        if dest_customer.demand_98_1>self.cap_dict[i]:
                            dest_customer.demand_98_1=dest_customer.demand_98_1-self.cap_dict[i]
                            self.cap_dict[i]=0
                        if dest_customer.demand_98_2>self.cap_dict[i]:
                            dest_customer.demand_98_2=dest_customer.demand_98_2-self.cap_dict[i]
                            self.cap_dict[i]=0
                            
                if j=='DF':
                    if dest_customer.demand_DF_1<dest_customer.demand_DF_2 and dest_customer.demand_DF_1>self.cap_dict[i]:
                        dest_customer.demand_DF_1=dest_customer.demand_DF_1-self.cap_dict[i]
                        self.cap_dict[i]=0
                    elif dest_customer.demand_DF_1>dest_customer.demand_DF_2 and dest_customer.demand_DF_2>self.cap_dict[i]:
                        dest_customer.demand_DF_2=dest_customer.demand_DF_2-self.cap_dict[i]
                        self.cap_dict[i]=0
                    else:
                        if dest_customer.demand_DF_1>self.cap_dict[i]:
                            dest_customer.demand_DF_1=dest_customer.demand_DF_1-self.cap_dict[i]
                            self.cap_dict[i]=0
                        if dest_customer.demand_DF_2>self.cap_dict[i]:
                            dest_customer.demand_DF_2=dest_customer.demand_DF_2-self.cap_dict[i]
                            self.cap_dict[i]=0

                
    def add_vehicle(self):
# if truck can not get in time to AZS, or all compartment = 0, new vehicle created
        if self.vehicles_count<len(veh):
        # if we have free additional truck, we add
            self.vehicles_count += 1
            self.vehicles_routes.append([0])
            self.elapsed_time = 0
            self.cap_dict[1]=self.current_load_1 #full compartments loading
            self.cap_dict[2]=self.current_load_2
            self.cap_dict[3]=self.current_load_3
            self.cap_dict[4]=self.current_load_4
            self.cap_dict[5]=self.current_load_5
            self.cap_dict[6]=self.current_load_6

        else:
            # if we have not free trucks, we take last one
            self.vehicles_count=self.vehicles_count
            self.elapsed_time = 0
            self.cap_dict[1]=self.current_load_1
            self.cap_dict[2]=self.current_load_2
            self.cap_dict[3]=self.current_load_3
            self.cap_dict[4]=self.current_load_4
            self.cap_dict[5]=self.current_load_5
            self.cap_dict[6]=self.current_load_6
        
# Fitness function
    def get_cost_score(self) -> float:
     
        self.initial_port()

        for source, dest in utils.pairwise([0] + self.route + [0]):
            # проверка на наличие потребности каждого вида топлива
            if dest!=0:
                if not self.check_demand(dest):
                    continue
            if self.check_capacity(dest):
                # автомобиль удовлетворяет условиям multi-compartment
                if not self.check_time_and_go(source, dest):
                    # автомобиль не успевает прибыть к новому потребителю, тогда + авто
                    # Текущий автомобиль возвращается в депо 
                    self.move_vehicle(source, 0)
                    # новый атомобиль стартует с депо
                    self.add_vehicle()
                    self.move_vehicle(0, dest)
            else:
                # автомобиль не проходит по ограничениям груза 
                # возвращается в депо
                self.move_vehicle(source, 0)
                # расчет дистанции из депо к азс
                distance = self.get_distance(0, dest)  # just for speeding up (caching)
                self.total_travel_dist +=distance
                if not self.check_time_and_go(0, dest, distance):
                    #этот автомобиль не успевает, тогда выезжает новый 
                    self.add_vehicle()
                    self.move_vehicle(0, dest, distance)

        total_travel_cost = Chromosome.get_travel_cost(self.total_travel_dist)
        total_vehicles_and_deport_working_hours_cost = self.get_vehicle_count_preference_cost(
            vehicles_count=self.vehicles_count,
            deport_working_hours=self.max_elapsed_time)
        return total_travel_cost + total_vehicles_and_deport_working_hours_cost


    def __iter__(self):
        for r in self.route:
            yield r

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __radd__(self, other):
        return self.value + other

    def __add__(self, other):
        return self.value + other

    def __sub__(self, other):
        return self.value - other

    def __float__(self):
        return float(self.value)

    def __str__(self):
        return str(self.route) + ", value= " + str(self.value) + ", vehicles_count= " + str(self.vehicles_count) \
               + ", total deport visits=" + str(self.route_rounds) \
               +  ", routes= " + str(self.vehicles_routes)

    def __repr__(self):
        return self.__str__()

    