# mpi_main.py => multiprocessing using MPI

from mpi4py import MPI
from src.explorer import Explorer
from src.maze import create_maze

print("\n=== MULTIPLE RUN - MPI: Maze Exploration Summary ===")

comm = MPI.COMM_WORLD
rank = comm.Get_rank() 
size = comm.Get_size()

maze = create_maze(width=30, height=30, maze_type='static')
explorer = Explorer(maze, visualize=False)

time_taken, moves = explorer.solve()

stats = {
    "time": time_taken,
    "moves": len(moves),
    "backtracks": explorer.backtrack_count
}
all_stats = comm.gather(stats, root=0)
if rank == 0:
    best_explorer = None
    best_time = float('inf')
    
    for i, stat in enumerate(all_stats):
        print(f"Explorer {i} | Time: {stat['time']:.6f}s | Moves: {stat['moves']} | Backtracks: {stat['backtracks']}")
        
        if stat['time'] < best_time:
            best_time = stat['time']
            best_explorer = i
        
    
    print("\nBest Explorer:", best_explorer)
    print("Best Time:", best_time)