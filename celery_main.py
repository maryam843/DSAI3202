# celery_main.py => multiprocessing using celery + rabbitmq
from celery_task import solve_maze
import time

NUM_EXPLORERS = 4
width, height = 10, 10 

if __name__ == "__main__":
    print("=== MULTIPLE RUN - CELERY: Maze Exploration Summary ===\n")
    async_results = [
        solve_maze.delay(width, height, False)
        for _ in range(NUM_EXPLORERS)
    ]

    explorers = []
    for idx, res in enumerate(async_results):
        try:
            result = res.get(timeout=10) 
            if result:
                print(f"Explorer {idx + 1} result: {result}")
                explorers.append((result["time_taken"], result["moves"]))
            else:
                print(f"Explorer {idx + 1} did not return a valid result.")
        except Exception as e:
            print(f"Explorer {idx + 1} failed: {e}")

    if explorers:
        for idx, (time_taken, moves) in enumerate(explorers, 1):
            avg_speed = moves / time_taken if time_taken > 0 else 0
            print(f"\nExplorer {idx}:\n")
            print("=== Maze Exploration Statistics ===")
            print(f"Total time taken: {time_taken:.6f} seconds")
            print(f"Total moves made: {moves}")
            print("Number of backtrack operations: 0") 
            print(f"Average moves per second: {avg_speed:.1f}")
            print("==================================")

        # Find best explorer
        best = min(explorers, key=lambda x: x[0])
        print(f"\n\nBest Explorer: Explorer {explorers.index(best) + 1}")
        print(f"Best Explorer Time: {best[0]:.6f} seconds")
    else:
        print("No valid results to display.")
