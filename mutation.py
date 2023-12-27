import math
import random

from length import tsp_length

#TODO change mutation based on parent length
# 1. Swap Mutation
def swap_mutation(route):
    mutated_route = route.copy()
    idx1, idx2 = random.sample(range(len(mutated_route)), 2)
    mutated_route[idx1], mutated_route[idx2] = mutated_route[idx2], mutated_route[idx1]
    return mutated_route

def multiple_swap_mutation(route, tour_length):
    for i in range(math.ceil(int(tour_length / 25))):
        mutated_route = route.copy()
        idx1, idx2 = random.sample(range(len(mutated_route)), 2)
        mutated_route[idx1], mutated_route[idx2] = mutated_route[idx2], mutated_route[idx1]
    return mutated_route

# 2. Insertion Mutation
def insertion_mutation(route):
    mutated_route = route.copy()
    idx1, idx2 = random.sample(range(len(mutated_route)), 2)
    city = mutated_route.pop(idx1)
    mutated_route.insert(idx2, city)
    return mutated_route

# 3. Inversion Mutation
def inversion_mutation(route):
    mutated_route = route.copy()
    start, end = sorted(random.sample(range(len(mutated_route)), 2))
    mutated_route[start:end+1] = reversed(mutated_route[start:end+1])
    return mutated_route

# 4. Scramble Mutation
def scramble_mutation(route):
    mutated_route = route.copy()
    start, end = sorted(random.sample(range(len(mutated_route)), 2))
    segment = mutated_route[start:end+1]
    random.shuffle(segment)
    mutated_route[start:end+1] = segment
    return mutated_route

# 5. Displacement Mutation
def displacement_mutation(route):
    mutated_route = route.copy()
    start, end = sorted(random.sample(range(len(mutated_route)), 2))
    segment = mutated_route[start:end+1]
    del mutated_route[start:end+1]
    insert_position = random.randint(0, len(mutated_route) - len(segment))
    for idx, city in enumerate(segment):
        mutated_route.insert(insert_position + idx, city)
    return mutated_route

def mutation_interface(route, distanceMatrix, mutation):
    length = float('inf')
    while(length == float('inf')):
        individual = mutation(route)
        length = tsp_length(distanceMatrix, individual)
    return individual