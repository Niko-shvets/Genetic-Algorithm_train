import random 
import numpy as np
np.random.seed(42)
random.seed(42)
from crossovers import crossover_uox, crossover_cx, crossover_pmx
from selections import selection_tournament_deterministic
from mutations import mutation_inversion, mutation_scramble

print_benchmarks = True
draw_plot = False
export_spreadsheet = False

MAX_GEN = 600

vehicle_cost_per_dist = 100 # для системы штрафов
vehicle_speed_avg = 75
# vehicle_capacity_1 = 7
# vehicle_capacity_2=7
# vehicle_capacity_3=7
#maximum_vehicle_number=9
#print('capacity of 1st compartment ',vehicle_capacity_1)
#print('capacity of 2nd compartment ',vehicle_capacity_2)
#print('capacity of 3rd compartment ',vehicle_capacity_3)
vehicles_count_over_deport_hours_preference = 100

run_file = {
    'name': 'm',
    'header_map': {
        'CUST_NO':'AZS_no',
        'DEMAND_92_1': 'demand_92_1',
        'DEMAND_92_2': 'demand_92_2',
        'DEMAND_95_1': 'demand_95_1',
        'DEMAND_95_2': 'demand_95_2',
        'DEMAND_98_1': 'demand_98_1',
        'DEMAND_98_2': 'demand_98_2',
        'DEMAND_DF_1': 'demand_DF_1',
        'DEMAND_DF_2': 'demand_DF_2',
        'READY_TIME': 'ready_time',
        'DUE_DATE': 'due_time',
        'SERVICE_TIME': 'service_time',
    }
}

population = {
    'pop_size': 200,
    'crossover_method': staticmethod(crossover_cx),
    'mutation_method': staticmethod(mutation_scramble),
    'removing_method': staticmethod(selection_tournament_deterministic),
    'selection_method': staticmethod(selection_tournament_deterministic),
    'selection_pressure': 10,  # tournament size (k)
    'selection_repeat': True,
    'parent_selection_ratio':0.8,
    'mutation_ratio': 0.1,
    'elitism_count':3,
    
}
