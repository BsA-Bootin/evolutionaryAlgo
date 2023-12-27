import random
from length import tsp_length
from selection import k_tournament_selection

# Cities Generator
def generate_number_list(n):
    return list(range(n))

# 1. Random Initialization
def random_initialization(num_individuals, n, distance_matrix):
    population = []

    for _ in range(num_individuals):
        while True:
            tour = []
            visited = set()
            current_city = random.randint(0, n - 1)  # Start from a random city
            tour.append(current_city)
            visited.add(current_city)
            broken = False

            while len(tour) < n:
                legal_cities = [city for city in range(n) if city not in visited and distance_matrix[current_city][city] != float('inf')]
                if not legal_cities:
                    broken = True
                    break  # No legal possibilities, break out of the inner loop
                else:
                    next_city = random.choice(legal_cities)
                    tour.append(next_city)
                    visited.add(next_city)
                    current_city = next_city

            # Check if a valid tour is generated
            if not broken and distance_matrix[tour[-1]][tour[0]] != float('inf'):
                population.append(tour)
                break  # Break out of the outer loop as a valid tour is generated

    return population

# 2. Nearest Neighbor Initialization
def nearest_neighbor_initialization(num_individuals, distance_matrix):
    def nearest_city(current_city, unvisited):
        return min(unvisited, key=lambda city: distance_matrix[current_city][city])

    population = []
    for _ in range(num_individuals):
        start_city = random.choice(range(len(distance_matrix)))
        unvisited = set(range(len(distance_matrix)))
        unvisited.remove(start_city)
        individual = [start_city]
        
        while unvisited:
            next_city = nearest_city(individual[-1], unvisited)
            individual.append(next_city)
            unvisited.remove(next_city)
            
        population.append(individual)
    
    return population

# If you're considering Cluster-Based Initialization, it would require a clustering algorithm (like K-means) 
# and then solving TSP for each cluster, potentially using a simpler method or heuristic.

# 3. Greedy Initialization
def greedy_initialization(num_individuals, distance_matrix):
    def nearest_city(current_city, unvisited):
        return min(unvisited, key=lambda city: distance_matrix[current_city][city])
    
    population = []
    for _ in range(num_individuals):
        start_city = random.choice(range(len(distance_matrix)))
        unvisited = set(range(len(distance_matrix)))
        unvisited.remove(start_city)
        individual = [start_city]
        
        while unvisited:
            next_city = nearest_city(individual[-1], unvisited)
            individual.append(next_city)
            unvisited.remove(next_city)
            
        population.append(individual)
    
    return population

def greedy_initialization_advanced(num_individuals, distance_matrix):
    greedy_initialization_list = greedy_initialization(num_individuals*10, distance_matrix)
    return k_tournament_selection(greedy_initialization_list, num_individuals, 10, distance_matrix)

# 4. insertion heuristic
def nearest_neighbor(matrix, start_node=0):
    num_points = len(matrix)
    visited = [False] * num_points
    tour = [start_node]
    visited[start_node] = True

    for _ in range(num_points - 1):
        min_dist = float('inf')
        nearest_city = None

        for city in range(num_points):
            if not visited[city] and matrix[tour[-1]][city] < min_dist:
                min_dist = matrix[tour[-1]][city]
                nearest_city = city

        if nearest_city is not None:
            tour.append(nearest_city)
            visited[nearest_city] = True

    return tour

def insertion_heuristic(num_individuals, matrix):
    tours = []

    for _ in range(num_individuals):
        tour_size = len(matrix)
        initial_tour = nearest_neighbor(matrix, random.randint(0, tour_size - 1))  # Use nearest neighbor as initial tour
        
        num_points = len(matrix)
        remaining_points = list(range(num_points))
        for city in initial_tour:
            remaining_points.remove(city)  # Remove visited cities from remaining

        for _ in range(num_points - 1):
            best_insertion = None
            best_cost = float('inf')

            for point in remaining_points:
                min_cost = float('inf')
                min_index = -1

                for i in range(len(initial_tour)):
                    current_cost = matrix[initial_tour[i]][point] + matrix[point][initial_tour[(i + 1) % len(initial_tour)]]
                    
                    if current_cost < min_cost:
                        min_cost = current_cost
                        min_index = i
                
                if min_cost < best_cost:
                    best_cost = min_cost
                    best_insertion = (min_index + 1, point)

            if best_insertion:
                index, new_point = best_insertion
                initial_tour.insert(index, new_point)
                remaining_points.remove(new_point)

        tours.append(initial_tour)

    return tours
