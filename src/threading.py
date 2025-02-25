import threading
import time

def thread_sum(start, end, result, index):
    result[index] = sum(range(start, end + 1))

def parallel_thread_sum(n, num_threads):
    # Divide the range into equal parts
    part_size = n // num_threads
    threads = []
    result = [0] * num_threads

    for i in range(num_threads):
        start = i * part_size + 1
        end = (i + 1) * part_size if i != num_threads - 1 else n
        thread = threading.Thread(target=thread_sum, args=(start, end, result, i))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return sum(result)

if __name__ == "__main__":
    n = 10**6  # Large number for summation
    num_threads = 4  # Adjust as needed

    # Measure the start time
    start_time = time.time()

    total_sum = parallel_thread_sum(n, num_threads)

    # Measure the end time
    end_time = time.time()

    # Print the sum and execution time
    print(f"Sum: {total_sum}")
    print(f"Execution Time: {end_time - start_time} seconds")
