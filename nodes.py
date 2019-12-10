import ga_params
from typing import List
from datetime import datetime
import math
import pickle
import pandas as pd
import csv_reader
dist=csv_reader.dist_table
#dist=pd.read_pickle('dist_from_mariana_gorka')


class Customer:
    AZS_no=None
    demand_92_1 = None      # type: int
    demand_92_2 = None      # type: int
    demand_95_1 = None      # type: int 
    demand_95_2 = None      # type: int 
    demand_98_1 = None      # type: int 
    demand_98_2 = None      # type: int 
    demand_DF_1 = None      # type: int 
    demand_DF_2 = None      # type: int 
    ready_time = None    # type: int
    due_time = None      # type: int
    service_time = None  # type: int

    def __init__(self,AZS_no:int,  demand_92_1: float,demand_92_2: float,demand_95_1: float, demand_95_2: float,demand_98_1: float,demand_98_2: float,demand_DF_1: float,demand_DF_2: float, ready_time: float, due_time: float,service_time: float, **kwargs):
        self.AZS_no=int(AZS_no)
        self.demand_92_1 = round(float(float(demand_92_1)),4)
        self.demand_92_2 = round(float(float(demand_92_2)),4)
        self.demand_95_1 = round(float(float(demand_95_1)),4)
        self.demand_95_2= round(float(float(demand_95_2)),4)
        self.demand_98_1= round(float(float(demand_98_1)),4)
        self.demand_98_2= round(float(float(demand_98_2)),4)
        self.demand_DF_1= round(float(float(demand_DF_1)),4)
        self.demand_DF_2= round(float(float(demand_DF_2)),4)
        self.ready_time = round(float(float(ready_time)),4)
        self.due_time = round(float(float(due_time)),4)
        self.service_time = round(float(float(service_time)),4)

    def __str__(self):
        return 'demand_92_1: ' + str(self.demand_92_1)  + '|demand_92_2: ' + str(self.demand_92_2) + '|demand_95_1: ' + str(self.demand_95_1) + '|demand_95_2: ' + str(self.demand_95_2) + '|demand_98_1: ' + str(self.demand_98_1) + '|demand_98_2: ' + str(self.demand_98_2) + '|demand_DF_1: ' + str(self.demand_DF_1) + ' |demand_DF_2: ' + str(self.demand_DF_2)+  \
                '| ready_time: ' + str(self.ready_time) + '| due _time: ' + str(self.due_time) + '| service_time: ' + str(self.service_time)

    def __repr__(self):
        return self.__str__()


List_Customer = List[Customer]


class Deport(Customer):
    def __init__(self,  due_time: int, **kwargs):
        super(Deport, self).__init__(AZS_no=0,demand_92_1=0,demand_92_2=0,demand_95_1=0, demand_95_2=0, demand_98_1=0, demand_98_2=0, demand_DF_1=0,demand_DF_2=0, ready_time=0, due_time=due_time,service_time=0)


# def get_distance_customers_pair(c1: Customer, c2: Customer) -> float:
#     return math.hypot(c2.x - c1.x, c2.y - c1.y)


class CustomerDistanceTable:
    distance_table = dist   # type: list

    def get_distance(self, source: int, dest: int) -> float:
        return self.distance_table[source][dest]
    
    def __init__(self, customer_list: List_Customer):
        cost_table_timer = datetime.now()
        self.distance_table = dist
    
#
    
        if ga_params.print_benchmarks:
            print('--- distance table pre-computation time: ' + str(datetime.now() - cost_table_timer))
    
    def __str__(self):
        table_str = "--- Travel Cost between Customers"
        for row in self.distance_table:
            table_str += str(row)
        table_str += "--- END | Travel Cost Between Customers"
        return table_str

    def __repr__(self):
        return self.__str__()
