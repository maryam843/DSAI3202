import time
import os
from sensor import latest_temperatures, temperature_averages

def initialize_display():
    print("Current temperatures:")
    print("Latest Temperatures: ", end="")
    for i in range(3):  # Adjust based on the number of sensors
        print(f"Sensor {i}: --°C", end="  ")
    print("\n")
    print("Sensor Averages:")
    for i in range(3):  # Adjust based on the number of sensors
        print(f"Sensor {i} Average: --°C")
    print("\n")

def update_display():
    while True:
        # Clear the console (works in UNIX-like systems)
        os.system('clear')  # Use 'cls' for Windows
        
        print("Current temperatures:")
        print("Latest Temperatures: ", end="")
        for i in range(3):  # Adjust based on the number of sensors
            temperature = latest_temperatures.get(i, '--')
            print(f"Sensor {i}: {temperature}°C", end="  ")
        print("\n")

        print("Sensor Averages:")
        for i in range(3):  # Adjust based on the number of sensors
            average = temperature_averages.get(i, '--')
            print(f"Sensor {i} Average: {average}°C")
        print("\n")

        time.sleep(5)  # Refresh every 5 seconds
