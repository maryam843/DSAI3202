import time
import multiprocessing
import concurrent.futures
from src.utils import log_timing


def square(num: int) -> int:
    """Returns the square of a given number."""
    return num * num


def sequential_squares(numbers: list) -> list:
    """Calculates squares sequentially."""
    start = time.perf_counter()
    result = [square(num) for num in numbers]
    end = time.perf_counter()
    log_timing("sequential_squares", start, end)
    return result


def multiprocessing_squares(numbers: list) -> list:
    """Calculates squares using multiprocessing."""
    num_workers = min(8, multiprocessing.cpu_count())
    with multiprocessing.Pool(processes=num_workers) as pool:
        start = time.perf_counter()
        result = pool.map(square, numbers)
        end = time.perf_counter()
    log_timing("multiprocessing_squares", start, end)
    return result


def pool_map(numbers: list) -> list:
    """Calculates squares using Pool.map()."""
    num_workers = min(8, multiprocessing.cpu_count())
    with multiprocessing.Pool(processes=num_workers) as pool:
        start = time.perf_counter()
        result = pool.map(square, numbers)
        end = time.perf_counter()
    log_timing("pool_map", start, end)
    return result


def pool_apply_async(numbers: list) -> list:
    """Calculates squares asynchronously using Pool.apply_async()."""
    num_workers = min(8, multiprocessing.cpu_count())
    with multiprocessing.Pool(processes=num_workers) as pool:
        start = time.perf_counter()
        results = [pool.apply_async(square, (num,)) for num in numbers]
        result = [res.get() for res in results]  # Collect results
        end = time.perf_counter()
    log_timing("pool_apply_async", start, end)
    return result


def concurrent_futures(numbers: list) -> list:
    """Calculates squares using concurrent.futures with optimized workers
    & chunking."""
    num_workers = min(8, multiprocessing.cpu_count())  # Adjusted workers
    chunksize = max(len(numbers) // (num_workers * 4), 100)
    with concurrent.futures.ProcessPoolExecutor(
         max_workers=num_workers) as executor:
        start = time.perf_counter()
        result = list(executor.map(square, numbers, chunksize=chunksize))
        end = time.perf_counter()
    log_timing("concurrent_futures", start, end)
    return result


if __name__ == "__main__":
    # Generate large test lists
    numbers_1M = list(range(10**6))  # 10⁶ numbers
    numbers_10M = list(range(10**7))  # 10⁷ numbers

    print("⚡ Running for 10⁶ numbers...")
    sequential_squares(numbers_1M)
    multiprocessing_squares(numbers_1M)
    pool_map(numbers_1M)
    pool_apply_async(numbers_1M)
    concurrent_futures(numbers_1M)

    print("\n⚡ Running for 10⁷ numbers...")
    sequential_squares(numbers_10M)
    multiprocessing_squares(numbers_10M)
    pool_map(numbers_10M)
    pool_apply_async(numbers_10M)
    concurrent_futures(numbers_10M)
