from distance import kendall_tau_distance
from length import tsp_fitness


def crowdings_algorithm(population, population_size, distance_matrix):
	tour_length = len(distance_matrix)

	find_inf_population = []
	for tour in population:
		find_inf_population.append((tour, tsp_fitness(tour, distance_matrix)))
	find_inf_population.sort(key=lambda x: x[1])
	sorted_population = [tour for (tour, fitness) in find_inf_population if fitness != float('inf')]
	eliminated_population = []
	for _ in range(0, population_size):
		tour = sorted_population[0]
		eliminated_population.append(tour)
		sorted_population.remove(tour)
		
		index = 0
		while index < 5 and len(sorted_population) > 4:
			extra_tour = sorted_population[index]
			if (kendall_tau_distance(tour, extra_tour) < tour_length*5):
				sorted_population.remove(extra_tour)
			else:
				index += 1
		
		if len(sorted_population) <= 4: 
			break
					
	return eliminated_population
