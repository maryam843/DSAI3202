from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
hostname = MPI.Get_processor_name()

print(f"Process {rank} running on {hostname}")
