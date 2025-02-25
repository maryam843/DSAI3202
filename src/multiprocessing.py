import multiprocessing
import time

def process_sum(start, end, result, index):
    result[index] = sum(range(start, end + 1))

def parallel_process_sum(n, num_processes):
    # Divide the range into equal parts
    part_size = n // num_processes
    processes = []
    result = multiprocessing.Array('i', num_processes)

    for i in range(num_processes):
        start = i * part_size + 1
        end = (i + 1) * part_size if i != num_processes - 1 else n
        process = multiprocessing.Process(target=process_sum, args=(start, end, result, i))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    return sum(result)

if __name__ == "__main__":
    n = 10**6  # Large number for summation
    num_processes = 4  # Adjust as needed

    # Measure the start time
    start_time = time.time()

    total_sum = parallel_process_sum(n, num_processes)

    # Measure the end time
    end_time = time.time()

    # Print the sum and execution time
    print(f"Sum: {total_sum}")
    print(f"Execution Time: {end_time - start_time} seconds")
