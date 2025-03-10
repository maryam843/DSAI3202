from src.threads import calculate_sum_parallel
from src.processing import calculate_sum_multiprocessing
from src.functions import calculate_sum_sequential


def evaluate_performance(n, num_threads, num_processes):
    
    # Sequential Execution
    seq_sum, seq_time = calculate_sum_sequential(n)
    print(f"Sequential Sum: {seq_sum}")
    print(f"Sequential Execution Time: {seq_time:.4f} seconds")
    print("___________________")

    # Threaded Execution
    par_sum, par_time = calculate_sum_parallel(n, num_threads)
    print(f"Threaded Sum: {par_sum}")
    print(f"Threaded Execution Time: {par_time:.4f} seconds")
    print("___________________")

    # Process Execution
    pro_sum, pro_time = calculate_sum_multiprocessing(n, num_processes)
    print(f"Process Sum: {pro_sum}")
    print(f"Process Execution Time: {pro_time:.4f} seconds")
    print("___________________")

    # Check if sums match
    if seq_sum == par_sum == pro_sum:
        # Calculate Speedups
        speedup_thread = seq_time / par_time
        speedup_process = seq_time / pro_time

        # Efficiency
        efficiency_thread = speedup_thread / num_threads
        efficiency_process = speedup_process / num_processes

        # Amdahl's Law Speedup (Assuming 90% parallelizable)
        P = 0.9
        amdahl_speedup_thread = 1 / ((1 - P) + (P / num_threads))
        amdahl_speedup_process = 1 / ((1 - P) + (P / num_processes))

        # Gustafson's Law Speedup
        gustafson_speedup_thread = num_threads - (1 - P) * num_threads
        gustafson_speedup_process = num_processes - (1 - P) * num_processes

        print(f"Thread Speedup: {speedup_thread:.2f}")
        print(f"Process Speedup: {speedup_process:.2f}")

        print(f"Thread Efficiency: {efficiency_thread:.2f}")
        print(f"Process Efficiency: {efficiency_process:.2f}")

        print(f"Amdahl's Speedup (Thread): {amdahl_speedup_thread:.2f}")
        print(f"Amdahl's Speedup (Process): {amdahl_speedup_process:.2f}")

        print(f"Gustafson's Speedup (Thread): {gustafson_speedup_thread:.2f}")
        print(f"Gustafson's Speedup (Process): {gustafson_speedup_process:.2f}")
    else:
        print("Error: The sums do not match!")

if __name__ == "__main__":
    large_number = 10**6
    num_threads = 4
    num_processes = 4

    evaluate_performance(large_number, num_threads, num_processes)
