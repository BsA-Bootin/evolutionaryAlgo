import numpy as np

from initialization import nearest_neighbor_initialization
from length import tsp_length


def cost_change(distance_matrix, tour, i, j, k):
    """Calculate the change in cost if edges (i, i+1) and (j, k) are swapped."""
    N = len(tour)
    a, b, c, d = tour[i], tour[i + 1], tour[j], tour[k % N]
    return distance_matrix[a][b] + distance_matrix[c][d] - distance_matrix[a][c] - distance_matrix[b][d]

def lin_kernighan(distance_matrix, tour):
    N = len(tour)
    improved = True
    while improved:
        improved = False
        for i in range(N - 1):
            print(i)
            for j in range(i + 2, N):
                for k in range(N):
                    if k != i and k != (i + 1) % N and k != j:
                        delta = cost_change(distance_matrix, tour, i, j, k)
                        if delta < 0:
                            tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
                            improved = True
                            break
                if improved:
                    break
            if improved:
                break
    return tour

# Example usage
# Assuming you have a filled-in distance_matrix
# Initialize a tour (can be random or any initial tour)

file = open("matrices/tour200.csv")
distance_matrix = np.loadtxt(file, delimiter=",")

initial_tour = nearest_neighbor_initialization(1, distance_matrix)[0]

# Apply Lin-Kernighan algorithm to improve the tour
optimized_tour = lin_kernighan(distance_matrix, initial_tour)

print("Initial tour:", initial_tour)
print("Optimized tour:", optimized_tour)
print(tsp_length(distance_matrix, optimized_tour))