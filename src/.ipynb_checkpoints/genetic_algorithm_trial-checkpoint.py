import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from genetic_algorithms_functions import (
    calculate_fitness,
    select_in_tournament,
    order_crossover,
    mutate,
    generate_unique_population
)

# Load the distance matrix
distance_matrix = pd.read_csv('../data/city_distances.csv').to_numpy()

# Parameters
num_nodes = distance_matrix.shape[0]
population_size = 10000
num_tournaments = 4  # Number of tournaments to run
mutation_rate = 0.1
num_generations = 200
infeasible_penalty = 1e6  # Penalty for infeasible routes
stagnation_limit = 5

# Generate initial population: each individual is a route starting at node 0
np.random.seed(42)  # For reproducibility
population = generate_unique_population(population_size, num_nodes)

# Initialize variables for tracking stagnation
best_calculate_fitness = int(1e6)
stagnation_counter = 0


# Function to calculate fitness in parallel
def parallel_fitness(route):
    return calculate_fitness(route, distance_matrix)


# Main GA loop
with ProcessPoolExecutor() as executor:
    for generation in range(num_generations):
        # Evaluate fitness in parallel
        calculate_fitness_values = np.array(list(executor.map(parallel_fitness,
                                                              population)))

        # Check for stagnation
        current_best_calculate_fitness = np.min(calculate_fitness_values)
        if current_best_calculate_fitness < best_calculate_fitness:
            best_calculate_fitness = current_best_calculate_fitness
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        if stagnation_counter >= stagnation_limit:
            print(f"Regenerating population at generation {generation} "
                  "due to stagnation")
            best_individual = population[np.argmin(calculate_fitness_values)]
            population = generate_unique_population(population_size - 1,
                                                    num_nodes)
            population.append(best_individual)
            stagnation_counter = 0
            continue  # Skip the rest of the loop for this generation

        # Selection, crossover, and mutation
        selected = select_in_tournament(population, calculate_fitness_values)

        # Crossover in parallel
        offspring = []
        with ProcessPoolExecutor() as crossover_executor:
            offspring = list(crossover_executor.map(
                lambda parents: order_crossover(parents[0], parents[1]),
                zip(selected[::2], selected[1::2])
            ))

        # Mutation in parallel
        mutated_offspring = list(
            executor.map(lambda route: mutate(route, mutation_rate), offspring)
            )

        # Replacement: Replace the individuals that lost in the tournaments
        # with the new offspring
        sorted_indices = np.argsort(calculate_fitness_values)[::-1]
        num_offspring = len(mutated_offspring)
        for i, idx in enumerate(sorted_indices[:num_offspring]):
            population[idx] = mutated_offspring[i]

        # Ensure population uniqueness
        unique_population = set(tuple(ind) for ind in population)
        while len(unique_population) < population_size:
            individual = [0] + list(np.random.permutation(np.arange(1,
                                                                    num_nodes)
                                                          ))
            unique_population.add(tuple(individual))
        population = [list(individual) for individual in unique_population]

    # Print best calculate_fitness
    print(f"Generation {generation}: "
          f"Best calculate_fitness = {current_best_calculate_fitness}")

    # Update calculate_fitness_values for the final population
    calculate_fitness_values = np.array(list(executor.map(parallel_fitness,
                                                          population)))

    # Output the best solution
    best_idx = np.argmin(calculate_fitness_values)
    best_solution = population[best_idx]
    print("Best Solution:", best_solution)
    print("Total Distance:", calculate_fitness(best_solution, distance_matrix))
