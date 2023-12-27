import random
from length import tsp_length

#useless piece of shit
def bigDistanceFlipProb(population, distance_matrix, big_flip_prob):
    new_population = []
    for tour in population:
        new_tour = tour
        if random.random() < big_flip_prob:
            new_tour = bigDistanceFlipper(tour, distance_matrix)
        new_population.append(new_tour)
    return new_population


def bigDistanceFlipper(tour, distance_matrix):
    new_route1 = tour[:]
    new_route2 = tour[:]
    distances = []

    for i in range(len(tour) - 1):
        city1 = tour[i]
        city2 = tour[i + 1]
        distance = distance_matrix[city1][city2]
        distances.append((city1, city2, distance))

    sorted_distances = sorted(distances, key=lambda x: x[2], reverse=True)
    city1 = sorted_distances[0][0]
    city3 = sorted_distances[1][0]
    city4 = sorted_distances[1][1]
    new_route1[city1:city3] = list(reversed(new_route1[city1:city3]))
    new_route2[city1:city4] = list(reversed(new_route2[city1:city4]))
    if (tsp_length(distance_matrix, new_route1) > tsp_length(distance_matrix, new_route2)):
        return new_route2
    return new_route1