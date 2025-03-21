import os
import json
import time
import random
import matplotlib.pyplot as plt
import pandas as pd

# Outputs Folder Path
OUTPUT_PATH = "outputs"


def ensure_output_folder():
    """Ensure the outputs/ folder exists."""
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)


def save_output(filename, content):
    """Save output to the specified file."""
    ensure_output_folder()
    filepath = os.path.join(OUTPUT_PATH, filename)
    with open(filepath, 'a', encoding="utf-8") as f:
        f.write(content + '\n')


def log_to_file(filename, content):
    """Log parallel output to a file."""
    save_output(filename, content)


def log_timing(task_name, start_time, end_time):
    """Log execution time for each parallel approach."""
    duration = round(end_time - start_time, 4)
    save_output("timing_results.csv", f"{task_name},{duration}")


def save_json(filename, data):
    """Save data as JSON file."""
    ensure_output_folder()
    filepath = os.path.join(OUTPUT_PATH, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)


def square(num):
    """Return the square of a number."""
    return num * num


def simulate_work(duration=2):
    """Simulate random work with a sleep between 1 to `duration` seconds."""
    time.sleep(random.uniform(1, duration))


def plot_execution_time(csv_file="outputs/timing_results.csv"):
    """Plots the execution time for different parallel approaches."""
    ensure_output_folder()  # Ensure the folder exists before reading the file

    if not os.path.exists(csv_file):
        print(
            "❌ Timing results file not found!"
            "Run the parallel execution first.")
        return

    # Load timing data
    data = pd.read_csv(csv_file, names=['Approach', 'Time'])

    # Sort by execution time for better visualization
    data = data.sort_values("Time")

    # Increase figure size for clarity
    plt.figure(figsize=(12, 6))

    # Plot bar chart
    plt.bar(data['Approach'], data['Time'], color='skyblue')

    # Improve readability
    plt.xlabel("Parallel Approach")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Parallel Execution Timing")
    plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels

    plt.tight_layout()

    # Save the graph
    output_path = os.path.join(OUTPUT_PATH, "parallel_graph.png")
    plt.savefig(output_path)

    print(f"✅ Parallel graph saved in '{output_path}'")


# Run plotting after timing results are generated
if __name__ == "__main__":
    plot_execution_time()
