import random
from length import tsp_length
import numpy as np

def tsp_2opt(tour, distance_matrix, closest_cities, amount_of_cities_checked):
    tour_length = len(tour)
    best_fitness = tsp_length(distance_matrix, tour)
    best_tour = tour[:]

    for _ in range(1, amount_of_cities_checked):
        city_number = random.randint(0, tour_length - 1)
        swap_city_list = closest_cities[city_number]
        city_index = tour.index(city_number)
        indexes_to_swap = (0,0)
        for swap_city in swap_city_list:
            swap_city_number = swap_city[0]
            swap_city_index = tour.index(swap_city_number)

            new_route = tour[:]
            new_route[city_index:swap_city_index] = list(reversed(new_route[city_index:swap_city_index]))
            fitness = tsp_length(distance_matrix, new_route)

            if fitness < best_fitness:
                best_fitness = fitness
                best_tour = new_route
    
    return best_tour


def tsp_2opt_optimized(tour, distance_matrix, closest_cities, amount_of_cities_checked):
    tour_length = len(tour)
    best_fitness = tsp_length(distance_matrix, tour)

    forward_cumulative, backward_cumulative = generate_cumulative_distances(tour, distance_matrix)

    for _ in range(1, amount_of_cities_checked):
        city_number = random.randint(0, tour_length - 1)
        swap_city_list = closest_cities[city_number]
        city_index = tour.index(city_number)
        indexes_to_swap = (0,0)
        for swap_city in swap_city_list:
            swap_city_number = swap_city[0]
            swap_city_index = tour.index(swap_city_number)
        
            if (city_index < swap_city_index):
                first = city_index
                second = swap_city_index
            else: 
                second = city_index
                first = swap_city_index


            fit_first_part = forward_cumulative[first - 1]
            fit_last_part = forward_cumulative[tour_length] - forward_cumulative[second + 1]
            fit_middle_part = backward_cumulative[first] - backward_cumulative[second]
            if (first == 0):
                continue
            else: 
                first_bridge = distance_matrix[tour[first - 1]][tour[second]]
            if (second + 1 == tour_length):
                continue
            else:
                second_bridge = distance_matrix[tour[first]][tour[second + 1]]
            fitness = fit_first_part + first_bridge + fit_middle_part + second_bridge + fit_last_part

            if fitness < best_fitness:
                best_fitness = fitness
                indexes_to_swap = (first, second)

    new_route = tour[:]
    first, second = indexes_to_swap
    new_route[first:second] = list(reversed(new_route[first:second]))
    
    return new_route

def closest_cities(distance_matrix, n):
    closest = {}
    num_cities = len(distance_matrix)
    
    for i in range(num_cities):
        distances = [(j, distance_matrix[i][j]) for j in range(num_cities) if i != j]
        distances.sort(key=lambda x: x[1])  # Sort distances
        
        closest[i] = distances[:n]  # Store the closest n cities for each city
    
    return closest

# using cumulatives

def generate_cumulative_distances(tour, dist_matrix):
    num_cities = len(tour)
    forward_cumulative = np.zeros(num_cities + 1)
    backward_cumulative = np.zeros(num_cities)

    # Calculate forward cumulative distances
    forward_cumulative[0] = 0
    for i in range(1, num_cities):
        forward_cumulative[i] = forward_cumulative[i - 1] + dist_matrix[tour[i - 1]][tour[i]]
    forward_cumulative[num_cities] = forward_cumulative[num_cities - 1] + dist_matrix[tour[num_cities - 1]][tour[0]]

    # Calculate backward cumulative distances
    backward_cumulative[num_cities - 1] = 0
    for i in range(num_cities - 2, -1, -1):
        backward_cumulative[i] = backward_cumulative[i + 1] + dist_matrix[tour[i]][tour[i + 1]]

    return forward_cumulative, backward_cumulative

def ts2_opt_cumulatives(tour, dist_matrix):
    num_cities = len(tour)
    best_fitness = tsp_length(dist_matrix, tour)
    best_combination = (0, 0)

    forward_cumulative, backward_cumulative = generate_cumulative_distances(tour, dist_matrix)

    for first in range(1, num_cities - 2):
        fit_first_part = forward_cumulative[first - 1]
        fit_middle_part = 0
        for second in range(first + 2, num_cities - 1):
            fit_last_part = backward_cumulative[second]
            fit_middle_part += forward_cumulative[second - 1] - forward_cumulative[first]
            first_bridge = dist_matrix[tour[first - 1]][tour[second - 1]]
            second_bridge = dist_matrix[tour[first]][tour[second]]
            fitness = fit_first_part + first_bridge + fit_middle_part + second_bridge + fit_last_part

            if fitness < best_fitness:
                best_combination = (first, second)
                best_fitness = fitness

    if best_combination != (0, 0):
        first, second = best_combination
        tour[first:second] = tour[first:second][::-1]

    return tour