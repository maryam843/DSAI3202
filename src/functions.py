import time
import threading
import multiprocessing

def calculate_sum_sequential(n):
    start_time = time.time()
    total_sum = sum(range(1, n + 1))
    end_time = time.time()
    execution_time = end_time - start_time
    return total_sum, execution_time

