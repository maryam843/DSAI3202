# bfs.py ==> solving the maze using breadth first search

from collections import deque
import pygame
import time
import csv
import os

class StaticMaze:
    """
    Represents a static maze and provides a method to solve it using BFS.
    """
    def __init__(self, maze):
        """
        Initialize the maze with given 2D list.

        Args:
            maze (List[List[int]]): 2D maze grid (0: free, 1: wall).
        """
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

    def bfs(self, start, goal):
        """
        Performs Breadth-First Search to find the shortest path from start to goal.

        Args:
            start (Tuple[int, int]): Starting cell coordinates (row, col).
            goal (Tuple[int, int]): Goal cell coordinates (row, col).

        Returns:
            List[Tuple[int, int]] or None: The path from start to goal, or None if unreachable.
        """
        queue = deque([start])               # Queue for BFS traversal
        came_from = {start: None}            # Tracks path history
        visited = set([start])               # Tracks visited nodes to avoid revisiting

        while queue:
            current = queue.popleft()

            if current == goal:
                # Reconstruct the path from goal to start using came_from
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]  # Return reversed path (start to goal)

            # Check all 4 possible directions (up, down, left, right)
            for neighbor in [
                (current[0] + 1, current[1]), (current[0] - 1, current[1]),
                (current[0], current[1] + 1), (current[0], current[1] - 1)
            ]:
                r, c = neighbor
                # Ensure neighbor is within bounds and walkable, and not already visited
                if (0 <= r < self.rows and 0 <= c < self.cols and
                    self.maze[r][c] == 0 and neighbor not in visited):
                    queue.append(neighbor)
                    came_from[neighbor] = current
                    visited.add(neighbor)

        return None  # No path found


def log_statistics(total_time, total_moves, backtrack_ops, avg_moves_per_sec):
    """
    Prints maze exploration statistics.

    Args:
        total_time (float): Total time taken in seconds.
        total_moves (int): Total number of moves in the path.
        backtrack_ops (int): Number of backtracking steps (moves - 1).
        avg_moves_per_sec (float): Average speed in moves per second.
    """
    print("=" * 40)
    print("=== BFS Maze Exploration Statistics ===")
    print(f"Total time taken: {total_time:.6f} seconds")
    print(f"Total moves made: {total_moves}")
    print(f"Number of backtrack operations: {backtrack_ops}")
    print(f"Average moves per second: {avg_moves_per_sec:.6f}")
    print("=" * 40)


def save_results_to_csv(algorithm, filename, total_time, total_moves):
    """
    Appends the result of a run to a CSV file.

    Args:
        algorithm (str): Name of the algorithm used.
        filename (str): Path to the output CSV file.
        total_time (float): Time taken by the algorithm.
        total_moves (int): Number of steps in the path.
    """
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Algorithm', 'Total Time (s)', 'Total Moves'])
        writer.writerow([algorithm, f"{total_time:.6f}", total_moves])


def visualize_maze_with_stats(maze, path, start, goal, total_time, total_moves, backtrack_ops, avg_moves_per_sec, cell_size=10):
    """
    Visualizes the maze and the computed path using pygame.

    Args:
        maze (List[List[int]]): 2D maze grid.
        path (List[Tuple[int, int]]): Computed path from BFS.
        start (Tuple[int, int]): Starting cell.
        goal (Tuple[int, int]): Goal cell.
        total_time (float): Time taken (unused in visualization but included for consistency).
        total_moves (int): Number of moves (unused in visualization).
        backtrack_ops (int): Number of backtracks (unused in visualization).
        avg_moves_per_sec (float): Moves per second (unused in visualization).
        cell_size (int): Size of each cell in the visualization.
    """
    pygame.init()

    # Color definitions
    WALL_COLOR = (0, 0, 0)
    PATH_COLOR = (0, 255, 0)
    START_COLOR = (0, 0, 255)
    GOAL_COLOR = (255, 0, 0)
    FREE_COLOR = (255, 255, 255)

    rows = len(maze)
    cols = len(maze[0])

    screen_width = cols * cell_size
    screen_height = rows * cell_size + 100
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("BFS Maze Explorer")

    running = True
    clock = pygame.time.Clock()
    start_time = time.time()

    while running:
        screen.fill(FREE_COLOR)

        # Draw the maze grid
        for row in range(rows):
            for col in range(cols):
                if maze[row][col] == 1:
                    pygame.draw.rect(screen, WALL_COLOR, (col * cell_size, row * cell_size, cell_size, cell_size))

        # Draw the path
        for node in path:
            pygame.draw.rect(screen, PATH_COLOR, (node[1] * cell_size, node[0] * cell_size, cell_size, cell_size))

        # Draw start and goal positions
        pygame.draw.rect(screen, START_COLOR, (start[1] * cell_size, start[0] * cell_size, cell_size, cell_size))
        pygame.draw.rect(screen, GOAL_COLOR, (goal[1] * cell_size, goal[0] * cell_size, cell_size, cell_size))

        # Offset for any text/stats display
        y_offset = rows * cell_size + 10

        pygame.display.update()

        if time.time() - start_time > 3:
            running = False

        clock.tick(60)

    pygame.quit()


# Sample usage and entry point
def main():
    """
    Entry point for the program. Loads the maze, runs BFS, and visualizes the result.
    """
    # Load maze from strings (convert to 2D list of ints)
    maze_str = [
        "11111111111111111111111111111111111111111111111111111111111111",
        "10000000010000000000000001011001000000000001001000000000000101",
        "10010011111111110011111001011011111111001001001001001111111101",
        "10010000000000000010001000000001011001001000000001000000000001",
        "11110010011111111110011110001011001011111111001001001111111111",
        "10000010000010000000000001011000000000000001001001000000000101",
        "10111111110010010010011111111011111111001001001111001111100101",
        "10010000010010010010000000001000001000001001001000001000000001",
        "10010010011110011110011111111011111011111111001111111111111101",
        "10010010010010010000001000001011001011000001000001001000000001",
        "11110011110010010011111111011111001011001111001001001111111101",
        "10000000010000010010000001011001000000001000001000000000100001",
        "11110011110010011110011111001011111011111111111001111111101111",
        "10000000000010000000000000000000000001000001000000000000100001",
        "10111111111111110011111011111111111011111001111001111111111101",
        "10010000000010000000001011000000001000000001000000001000000001",
        "10010011111110011111111001011011111011111001001111111111111101",
        "10000000000010000000001011001000001011001001000000000000000101",
        "11110011111111110010011111111001011111001001111001111111111111",
        "10000010000000000010000001011001011000000000000001000000000101",
        "10111110011111110010001011001011011111001001111001111000101101",
        "10010010000000010010001000001011000001001001001000000000101101",
        "11110011110011111111111111111001011111001111001111001111111101",
        "10000010010000010000001011000001000000000000000001000000000101",
        "11110010011111111110001011111111111111001001111111001111100101",
        "10000000000000000000000000000001000000001001001000000000100001",
        "10111111111110011111111011111111001011111001001001111111101111",
        "10011111111110011111110011111111001011111001001001111111001111",
        "10000010000010010000000000001000001011000000001001001000000001",
        "11110011110010010011111011111111111011111001111001001001111101",
        "10010000010010010010000000000001000000001001001000001000000101",
        "10111110010011111110001011111001011111111001001001111111111101",
        "10000010000000010000001000001000001011000001000001000000101101",
         "11110011110010010011111111011111001011001111001001001111111101",
        "10000000010000010010000001011001000000001000001000000000100001",
        "11110011110010011110011111001011111011111111111001111111101111",
        "10000000000010010000001000001000001000001000001000001000101101",
        "11111110011111110011111111011111111001001111001111111000101111",
        "10000010000010010000000001000000001011001000000000000000101101",
        "10010010010010010011111111111001011111111111111001111001111101",
        "10010000010000000010000000000001000000001001001000001000000001",
        "11111111111111110011111011111011111111111001001001001111111101",
        "10010000000000010010000001000001000000001000000001000000101101",
        "10010011111111110010001011111111001011001001001111111111100101",
        "10010010010000010010001011000001011001001001000001000000101101",
        "10010010010011111111111001011011111011111001001001001000101101",
        "11110011110010010011111111011111001011001111001001001111111101",
        "11111111111111111111111111111111111111111111111111111111111111"
    ]
    # Convert the maze from string format to 2D integer list
    maze = [[int(cell) for cell in row] for row in maze_str]

    start = (1, 1)
    goal = (25, 11)
    explorer = StaticMaze(maze)

    start_time = time.time()

    # Solve the maze using BFS
    path = explorer.bfs(start, goal)

    # Visualize path (passing dummy stats for now)
    visualize_maze_with_stats(maze, path, start, goal, 0, 0, 0, 0)

    end_time = time.time()

    if path:
        total_time = end_time - start_time
        total_moves = len(path)
        backtrack_ops = total_moves - 1
        avg_moves_per_sec = total_moves / total_time if total_time > 0 else 0

        log_statistics(total_time, total_moves, backtrack_ops, avg_moves_per_sec)
        save_results_to_csv("BFS", "results.csv", total_time, total_moves)
    else:
        print("No path found.")

# Run the main function
if __name__ == "__main__":
    main()