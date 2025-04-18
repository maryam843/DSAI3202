from mpi4py import MPI
import numpy as np

def square(n):
    """Computes the square of a number."""
    return n * n

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define the range of numbers
n = 10  # Change this as needed
numbers = np.arange(1, n + 1)

# Split workload among processes
chunk_size = len(numbers) // size
remainder = len(numbers) % size

if rank < remainder:
    start = rank * (chunk_size + 1)
    end = start + chunk_size + 1
else:
    start = rank * chunk_size + remainder
    end = start + chunk_size

local_numbers = numbers[start:end]
local_squares = [square(num) for num in local_numbers]

# Gather results at root process
all_squares = comm.gather(local_squares, root=0)

if rank == 0:
    # Flatten the list of lists
    result = [num for sublist in all_squares for num in sublist]
    print("Squared numbers:", result)
