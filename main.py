# main.py

import random
import time
from src.square import *
from src.connection_pool import *
import multiprocessing


def generate_random_numbers(n):
    return [random.randint(1, 100) for _ in range(n)]


if __name__ == "__main__":
    numbers = generate_random_numbers(10**6)

    # Square Program
    print("Running sequential loop...")
    start = time.time()
    sequential_squares(numbers)
    print(f"Sequential Time: {time.time() - start:.2f} sec\n")

    print("Running multiprocessing loop...")
    start = time.time()
    multiprocessing_squares(numbers)
    print(f"Multiprocessing Time: {time.time() - start:.2f} sec\n")

    print("Running pool map()...")
    start = time.time()
    pool_map(numbers)
    print(f"Pool Map Time: {time.time() - start:.2f} sec\n")

    print("Running concurrent.futures...")
    start = time.time()
    concurrent_futures(numbers)
    print(f"Concurrent Futures Time: {time.time() - start:.2f} sec\n")

    # Semaphore Connection Pool
    print("\n--- Connection Pool with Semaphore ---")
    pool = ConnectionPool(max_connections=3)
    processes = []
    for i in range(10):
        process = multiprocessing.Process(target=access_database, args=(pool, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
