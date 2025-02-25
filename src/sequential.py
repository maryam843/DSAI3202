import time

def sequential_sum(n):
    return sum(range(1, n + 1))

if __name__ == "__main__":
    n = 10**6  # Large number for summation

    # Measure the start time
    start_time = time.time()
    
    total_sum = sequential_sum(n)
    
    # Measure the end time
    end_time = time.time()
    
    # Print the sum and execution time
    print(f"Sum: {total_sum}")
    print(f"Execution Time: {end_time - start_time} seconds")
