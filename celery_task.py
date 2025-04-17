# celery_task.py
from celery_app import app
from src.explorer import Explorer
from src.maze import create_maze
import time

@app.task
def solve_maze(width: int, height: int, visualize: bool = False):
    try:
        maze = create_maze(width, height, maze_type="random")
        print(f"Created maze with dimensions {width}x{height}")

        explorer = Explorer(maze, visualize=visualize)
        time_taken, moves = explorer.solve()

        if not isinstance(moves, (list, tuple)):
            raise ValueError("Moves is not a list or tuple")

        print(f"Solved maze in {time_taken:.6f} seconds with {len(moves)} moves")
        return {
            "time_taken": time_taken,
            "moves": len(moves)
        }
    except Exception as e:
        print(f"ERROR in solve_maze task: {e}")
        return None
