import multiprocessing
import time
from src.square import (
    sequential_squares,
    multiprocessing_squares,
    pool_map,
    concurrent_futures
)
from src.connection_pool import ConnectionPool, access_database
from src.utils import log_to_file, log_timing, plot_execution_time, save_json


def run_square():
    """Runs all square calculation approaches and logs output."""
    test_sizes = [10**4, 10**5]  # Start small before scaling up

    for size in test_sizes:
        numbers = list(range(size))
        log_to_file("parallel_logs.txt", f"\n⚡ Running for {size} numbers...")

        functions = [
            ("sequential_squares", sequential_squares),
            ("multiprocessing_squares", multiprocessing_squares),
            ("pool_map", pool_map),
            ("concurrent_futures", concurrent_futures)
        ]

        for name, func in functions:
            start_time = time.perf_counter()
            func(numbers)
            end_time = time.perf_counter()
            log_timing(f"{name}_{size}", start_time, end_time)

    print("✅ Timing tests completed! Check 'timing_results.csv'.")


def run_connection_pool():
    """Simulates connection pool handling with logging."""
    pool = ConnectionPool(size=2)  # ✅ Limited to 2 connections
    processes = []

    for i in range(8):  # ✅ Spawn 8 processes
        p = multiprocessing.Process(target=access_database, args=(pool, i))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    # Save connection pool usage to JSON
    save_json("pool_usage.json", list(pool.usage_log))


if __name__ == "__main__":
    print("\n💻 Running Parallel Squares 🔥\n")
    run_square()  # Run parallel computations

    print("\n🔒 Running Connection Pool 🛑\n")
    run_connection_pool()

    plot_execution_time("outputs/timing_results.csv")
