import random
import numpy as np

def tsp_length(distance_matrix, route):
    return sum(distance_matrix[route[i]][route[i+1]] for i in range(len(route)-1)) + distance_matrix[route[-1]][route[0]]


def tsp_fitness(route, distance_matrix):
    """Compute the total distance of the route."""
    return sum(distance_matrix[route[i]][route[i+1]] for i in range(len(route)-1)) + distance_matrix[route[-1]][route[0]]