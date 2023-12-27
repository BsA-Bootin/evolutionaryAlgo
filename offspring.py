import random
from length import tsp_length
from mutation import multiple_swap_mutation, mutation_interface


def generate_offspring(population, crossover, distance_matrix, offspring_size):
    offspring = []
    for _ in range(int(offspring_size/2)):
        length1 = float('inf')
        length2 = float('inf')
        while ((length1 == float('inf')) | (length2 == float('inf'))):
            parent1, parent2 = random.choices(population, k=2)  # Randomly select two parents
            child1, child2 = crossover(parent1, parent2)                 # Apply crossover
            length1 = tsp_length(distance_matrix, child1)
            length2 = tsp_length(distance_matrix, child2)
            
        offspring.append(child1)
        offspring.append(child2)
    return offspring