import time
import threading
import multiprocessing


def calculate_sum_multiprocessing(n, num_processes):
    def worker(start, end, queue):
        queue.put(sum(range(start, end + 1)))

    processes = []
    queue = multiprocessing.Queue()
    step = n // num_processes

    start_time = time.time()

    for i in range(num_processes):
        start = i * step + 1
        end = (i + 1) * step if i != num_processes - 1 else n
        process = multiprocessing.Process(target=worker, args=(start, end, queue))
        processes.append(process)
        process.start()

    total_sum = sum(queue.get() for _ in processes)

    for process in processes:
        process.join()

    end_time = time.time()
    execution_time = end_time - start_time
    return total_sum, execution_time
