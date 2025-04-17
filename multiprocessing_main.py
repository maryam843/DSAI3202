# multiprocess_main.py => multripocessing

import multiprocessing
from typing import List, Tuple
from src import explorer

def run_explorer(maze, visualize: bool = False):
    # Assuming Explorer is a class that performs the maze solving task
    explorer_instance = explorer.Explorer(maze, visualize)
    time_taken, moves = explorer_instance.solve()  # Run the maze solving
    return time_taken, moves, explorer_instance  # Return explorer instance for comparison

def parallel_exploration(maze, num_explorers: int):
    # Create a pool of explorers (processes)
    with multiprocessing.Pool(processes=num_explorers) as pool:
        results = pool.starmap(run_explorer, [(maze, False)] * num_explorers)
    print("\n=== MULTIPLE RUN - MULTIPROCESSING: Maze Exploration Summary ===")

    # Collect and compare results
    best_time, best_moves, best_explorer = min(results, key=lambda x: x[0])  # Get the best (min time)
    # Display statistics for all explorers
    print("\n=== Maze Exploration Summary ===")
    for idx, (time_taken, moves, explorer_instance) in enumerate(results, start=1):
        print(f"\nExplorer {idx}:")
        explorer_instance.print_statistics(time_taken)  # Assuming print_statistics is defined in Explorer

    # Display the best explorer with better precision for time
    best_explorer_index = results.index((best_time, best_moves, best_explorer)) + 1
    print(f"\nBest Explorer: Explorer {best_explorer_index}")
    print(f"Best Explorer Time: {best_time:.6f} seconds")  # Show 6 decimal places for better precision

    return best_explorer, best_time  # Return best explorer and its time

# Example Usage:
if __name__ == "__main__":
    from src.maze import Maze  # Assuming this is how you're loading the Maze class
    
    # Initialize your maze with width and height (e.g., 10x10 maze)
    maze = Maze(width=10, height=10)
    
    num_explorers = 4  # Number of explorers to run in parallel
    best_explorer, best_time = parallel_exploration(maze, num_explorers)

    print(f"\nBest Explorer Details: Time = {best_time:.6f} seconds")  # Better precision here as well
    best_explorer.print_statistics(best_time)
