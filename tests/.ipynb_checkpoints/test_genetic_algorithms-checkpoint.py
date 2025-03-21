import sys
import os
import numpy as np

# Add the src directory to sys.path so we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..', 'src')))


from genetic_algorithms_functions import (
    calculate_fitness, select_in_tournament,
    order_crossover, mutate, generate_unique_population
)


def test_fitness():
    """Test the calculate_fitness function."""
    distance_matrix = np.array([
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ])
    route = [0, 1, 3, 2, 0]
    fitness = calculate_fitness(route, distance_matrix)
    print(f"Route: {route}")
    print(f"Fitness: {fitness}")


def test_tournament_selection():
    """Test the tournament selection function."""
    population = [[0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]
    scores = np.array([-50, -40, -30])
    selected = select_in_tournament(population, scores, 2, 2)
    assert len(selected) == 2, "Tournament selection failed!"


def test_crossover():
    """Test the order crossover function."""
    p1 = [0, 1, 2, 3]
    p2 = [0, 3, 1, 2]
    child = order_crossover(p1, p2)
    assert set(child) == set(p1), "Crossover produced invalid offspring!"


def test_mutation():
    """Test the mutation function."""
    route = [0, 1, 2, 3]
    mutated = mutate(route.copy(), 1.0)  # 100% mutation rate
    assert route != mutated, "Mutation failed!"


def test_population():
    """Test unique population generation."""
    pop = generate_unique_population(5, 4)
    assert len(pop) == 5, "Population generation failed!"
    assert len(set(tuple(p) for p in pop)) == 5, "Population has duplicates!"


if __name__ == "__main__":
    test_fitness()
    test_tournament_selection()
    test_crossover()
    test_mutation()
    test_population()
    print("✅ All tests passed!")
