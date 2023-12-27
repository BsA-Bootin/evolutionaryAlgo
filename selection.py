import random
from length import tsp_length

def k_tournament_selection(population, k, tournament_size, distance_matrix):
    selected = []
    for i in range(k):
        tournament = random.sample(population, tournament_size)
        winner = min(tournament, key=lambda x: tsp_length(distance_matrix, x))
        selected.append(winner)
    return selected