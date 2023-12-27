import random
import Reporter
import numpy as np
from distance import kendall_tau_distance
from elimination import crowdings_algorithm
from length import tsp_length, tsp_fitness
from crossover import cycle_crossover, order_crossover, pmx
from localSearch import ts2_opt_cumulatives, tsp_2opt, tsp_2opt_optimized
from mutation import inversion_mutation, multiple_swap_mutation
from initialization import greedy_initialization_advanced, random_initialization, nearest_neighbor_initialization, greedy_initialization, insertion_heuristic
from offspring import generate_offspring
from selection import k_tournament_selection
from localSearch import closest_cities

# Modify the class name to match your student number.
class r0123456:

	def __init__(self):
		self.reporter = Reporter.Reporter(self.__class__.__name__)

	# The evolutionary algorithm's main loop
	def optimize(self, filename):
		# Read distance matrix from file.		
		file = open(filename)
		distance_matrix = np.loadtxt(file, delimiter=",")
		file.close()

		# parameters
		permutationSize = len(distance_matrix[0])
		populationSize = 100
		offspringSize = int(1.5*populationSize)
		iterations = 1000
		amount_of_closest_cities = 4
		amount_of_cities_checked = 30
		mutation_prob = 0.1

		# Your code here.
		yourConvergenceTestsHere = True
		while( yourConvergenceTestsHere ):
			meanObjective = 0.0
			bestObjective = 0.0
			bestSolution = np.array([1,2,3,4,5])

			# population initializations
			population = random_initialization(int(populationSize / 4 * 3), permutationSize, distance_matrix)
			# population += nearest_neighbor_initialization(int(populationSize / 4), distance_matrix)
			population += greedy_initialization_advanced(int(populationSize / 4 ), distance_matrix)
			# population += insertion_heuristic(int(populationSize / 4), distance_matrix)
			print("populations initialized")


			closest_cities_list = closest_cities(distance_matrix, amount_of_closest_cities)


			# Your code here.
			for i in range (iterations):
				print(f"iterations {i}")

				# selection
				selection = k_tournament_selection(population=population, k=offspringSize, tournament_size=5, distance_matrix=distance_matrix)

				# crossover + mutation (children)
				offspring = generate_offspring(population=selection, crossover=order_crossover, offspring_size=offspringSize, distance_matrix=distance_matrix)

				combined_population = selection + offspring
				
				sorted_population = sorted(combined_population, key=lambda x: tsp_fitness(x, distance_matrix))
				mutated_population = [sorted_population[0]]
				for tour in sorted_population[1:]:
					if random.random() < mutation_prob:
						tour = multiple_swap_mutation(tour, permutationSize)
					mutated_population.append(tour)

				# local search on population
				local_optimized_population = []
				for tour in mutated_population:
					local_optimized_population.append(tsp_2opt(tour, distance_matrix, closest_cities_list, amount_of_cities_checked))
				        
				# Apply mutation with a given probability

					
				# elimination
				population = crowdings_algorithm(local_optimized_population, populationSize, distance_matrix)

				if (len(population)) < 30:
					difference = 30 - len(population) + 20
					population += greedy_initialization(difference, distance_matrix)

				print("population size")
				print(len(population))
				print("mutation prob")
				print(mutation_prob)

				# sorted_population = sorted(combined_population, key=lambda x: tsp_fitness(x, distance_matrix))
				# population = sorted_population[:populationSize]


				# reporting
				permutationScores = []
				for permutation in population:
					permutationScores.append(tsp_length(distance_matrix, permutation))

				meanObjective = sum(permutationScores)/len(population)
				bestObjective = min(permutationScores)
				bestSolution = np.array(population[0])

				if meanObjective - bestObjective < 1000:
					mutation_prob += 0.01

				# Call the reporter with:
				#  - the mean objective function value of the population
				#  - the best objective function value of the population
				#  - a 1D numpy array in the cycle notation containing the best solution 
				#    with city numbering starting from 0
				timeLeft = self.reporter.report(meanObjective, bestObjective, bestSolution)
				if timeLeft < 0:
					break

			yourConvergenceTestsHere = False
		# Your code here.
		return 0
	
#program
solver = r0123456()
solver.optimize("matrices/tour200.csv")