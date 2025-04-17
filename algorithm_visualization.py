# algorithm_visualization.py => plot the performance of intial explorer, bfs, & A* algorithms; using the same static maze
# the results of these performances after running is stored in results.csv

import pandas as pd 
import matplotlib.pyplot as plt

# Load the CSV data
df = pd.read_csv("results.csv")

plt.figure(figsize=(12, 6))

# Line plot for Time Taken (in seconds)
plt.subplot(1, 2, 1)
plt.plot(df["Algorithm"], df["Time Taken"], marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
plt.title("Time Taken by Algorithm (Seconds)")
plt.ylabel("Time (seconds)")

# Add annotations for the exact time taken at each point
for i, txt in enumerate(df["Time Taken"]):
    plt.text(i, txt, f'{txt:.6f}', ha='center', va='bottom', fontsize=7)

plt.ylim(0, max(df["Time Taken"]) * 1.1)  # Adjust y-axis for visibility

# Bar plot for Total Moves
plt.subplot(1, 2, 2)
plt.bar(df["Algorithm"], df["Total Moves"], color=["skyblue", "salmon", "lightgreen"])
plt.title("Total Moves by Algorithm")
plt.ylabel("Moves")

for i, txt in enumerate(df["Total Moves"]):
    plt.text(i, txt, f'{txt}', ha='center', va='bottom', fontsize=7)
    
# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig("algorithm_performance.png")

# Show the plot
plt.show()
