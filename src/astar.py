# astar.py ==> solving the maze using breadth first search

import heapq
import pygame
import time
import csv
import os


# Manhattan Distance Heuristic
def heuristic(a, b):
    """
    Manhattan Distance Heuristic function.
    Calculates the distance between two points (a, b) assuming 4-directional movement.
    A* uses this to estimate cost to the goal, allowing smarter decision-making than BFS.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class StaticMaze:
    """
    Represents a static 2D maze and contains logic for solving it using the A* algorithm.
    """

    def __init__(self, maze):
        """
        Initializes the maze.
        :param maze: 2D list where 0 = open cell, 1 = wall
        """
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

    def a_star(self, start, goal):
        """
        A* pathfinding algorithm implementation.
        Finds the shortest path from start to goal using a priority queue with heuristic guidance.
        Compared to BFS, A* is more efficient as it avoids exploring unnecessary paths.

        :param start: Tuple (x, y) for start location
        :param goal: Tuple (x, y) for goal location
        :return: List of path coordinates from start to goal, or None if no path exists
        """
        # Priority queue to hold nodes to explore; elements = (f_score, g_score, node)
        open_set = []
        heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))

        came_from = {}  # Keeps track of the best parent for each node
        g_score = {start: 0}  # Cost from start to this node
        f_score = {start: heuristic(start, goal)}  # Estimated cost from start -> goal through this node

        closed_set = set()  # Tracks visited nodes

        while open_set:
            # Choose node with lowest f_score (priority queue handles this)
            _, current_cost, current_node = heapq.heappop(open_set)

            # Goal reached; reconstruct the path
            if current_node == goal:
                path = []
                while current_node in came_from:
                    path.append(current_node)
                    current_node = came_from[current_node]
                path.append(start)
                return path[::-1]  # Return reversed path: start -> goal

            closed_set.add(current_node)

            # Explore neighbors: up, down, left, right
            for neighbor in [
                (current_node[0] + 1, current_node[1]),
                (current_node[0] - 1, current_node[1]),
                (current_node[0], current_node[1] + 1),
                (current_node[0], current_node[1] - 1)
            ]:
                # Check boundaries
                if not (0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols):
                    continue
                # Skip walls
                if self.maze[neighbor[0]][neighbor[1]] == 1:
                    continue
                # Skip already visited nodes
                if neighbor in closed_set:
                    continue

                # Tentative cost from start to neighbor
                tentative_g_score = current_cost + 1  # Uniform cost for moving to a neighbor

                # If this path to neighbor is better than previous (or first time visiting)
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))

        # If goal is unreachable
        return None


# Function to log performance statistics to the console
def log_statistics(total_time, total_moves, backtrack_ops, avg_moves_per_sec):
    """
    Logs key metrics of the A* maze solving run.

    Args:
        total_time (float): Time taken to solve the maze.
        total_moves (int): Total number of steps taken to reach the goal.
        backtrack_ops (int): Number of backtrack operations during pathfinding.
        avg_moves_per_sec (float): Average number of moves made per second.
    """
    print("=" * 40)
    print("=== A* Maze Exploration Statistics ===")
    print(f"Total time taken: {total_time:.6f} seconds")
    print(f"Total moves made: {total_moves}")
    print(f"Number of backtrack operations: {backtrack_ops}")
    print(f"Average moves per second: {avg_moves_per_sec:.6f}")
    print("=" * 40)


# Function to append results to a CSV file for benchmarking purposes
def save_results_to_csv(algorithm, filename, total_time, total_moves):
    """
    Appends the algorithm performance results to a CSV file for analysis.

    Args:
        algorithm (str): Name of the algorithm used (e.g., "A*").
        filename (str): Path to the CSV file.
        total_time (float): Execution time in seconds.
        total_moves (int): Total steps in the solution path.
    """
    algorithm = "A*"  # Ensure algorithm is labeled consistently
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write header if file doesn't exist
        if not file_exists:
            writer.writerow(['Algorithm', 'Total Time (s)', 'Total Moves'])
        
        # Append run data
        writer.writerow([algorithm, f"{total_time:.6f}", total_moves])

# Function to render the maze and stats using Pygame
def visualize_maze_with_stats(maze, path, start, goal, total_time, total_moves, backtrack_ops, avg_moves_per_sec, cell_size=40):
    """
    Uses Pygame to visually display the maze, path, and relevant statistics.

    Args:
        maze (list of list of int): The maze grid (0 = open space, 1 = wall).
        path (list of tuple): The path from start to goal as (row, col) coordinates.
        start (tuple): Starting point coordinates.
        goal (tuple): Goal point coordinates.
        total_time (float): Time taken to compute the path.
        total_moves (int): Number of steps in the path.
        backtrack_ops (int): Number of backtracks performed (if applicable).
        avg_moves_per_sec (float): Moves per second performance metric.
        cell_size (int): Size of each maze cell in pixels.
    """
    pygame.init()

    # Define color scheme for visualization
    WALL_COLOR = (0, 0, 0)
    PATH_COLOR = (0, 255, 0)
    START_COLOR = (0, 0, 255)
    GOAL_COLOR = (255, 0, 0)
    FREE_COLOR = (255, 255, 255)

    rows = len(maze)
    cols = len(maze[0])
    screen_width = cols * cell_size
    screen_height = rows * cell_size + 100  # Extra space for stats

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Maze Explorer")

    font = pygame.font.SysFont("Arial", 18)
    stat_texts = [
        f"Total time taken: {total_time:.6f} seconds",
        f"Total moves made: {total_moves}",
        f"Number of backtrack operations: {backtrack_ops}",
        f"Average moves per second: {avg_moves_per_sec:.2f}"
    ]

    running = True
    clock = pygame.time.Clock()
    start_time = time.time()

    # Run loop for displaying visuals (stops after 3 seconds)
    while running:
        screen.fill(FREE_COLOR)

        # Render the maze grid
        for row in range(rows):
            for col in range(cols):
                if maze[row][col] == 1:
                    pygame.draw.rect(screen, WALL_COLOR, (col * cell_size, row * cell_size, cell_size, cell_size))

        # Render the A* path
        for node in path:
            pygame.draw.rect(screen, PATH_COLOR, (node[1] * cell_size, node[0] * cell_size, cell_size, cell_size))

        # Draw start and goal nodes
        pygame.draw.rect(screen, START_COLOR, (start[1] * cell_size, start[0] * cell_size, cell_size, cell_size))
        pygame.draw.rect(screen, GOAL_COLOR, (goal[1] * cell_size, goal[0] * cell_size, cell_size, cell_size))

        # Display performance statistics
        y_offset = rows * cell_size + 10
        for i, text in enumerate(stat_texts):
            stat_surface = font.render(text, True, (0, 0, 0))
            screen.blit(stat_surface, (10, y_offset + i * 30))

        pygame.display.update()

        # Exit after 3 seconds
        if time.time() - start_time > 3:
            running = False

        clock.tick(60)  # Cap frame rate for smoother display

    pygame.quit()

# Main execution point of the script
def main():
    """
    Main driver function that initializes the maze, runs A* pathfinding, 
    logs the results, visualizes them, and saves data for later analysis.
    """
    # Define a static maze using strings, where 1 = wall, 0 = open path
    maze = [
        "11111111111011111111111111111111111111111111111111111111111111",
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
        "10111110011111111111111111111111001011111111111001001111100101",
        "10010010000000010000000000000001000000001000000000001000000001",
        "10010010011110011111111011111001011011111111111001111111100101",
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
        "10000000000000000000000000001000000000000001001001001000000001",
        "11111111111110111111111111111111111111111111111111111111111111"
    ]
    
    # Convert the maze from string format to 2D integer list
    solver = StaticMaze([[int(c) for c in row] for row in maze])
    start = (1, 1)
    goal = (34, 60)

    start_time = time.time()
    path = solver.a_star(start, goal)
    end_time = time.time()

    algorithm = "A*"

    if path:
        total_time = end_time - start_time
        total_moves = len(path) - 1
        backtrack_ops = 0
        avg_moves_per_sec = total_moves / total_time if total_time > 0 else 0

        # Log and save results
        log_statistics(total_time, total_moves, backtrack_ops, avg_moves_per_sec)
        save_results_to_csv(algorithm, 'results.csv', total_time, total_moves)

        # Visualize maze and results
        visualize_maze_with_stats(maze, path, start, goal, total_time, total_moves, backtrack_ops, avg_moves_per_sec)
    else:
        print("No path found.")

# Run the main function
if __name__ == "__main__":
    main()