import random
import time
from queue import Queue
import threading

# Global dictionaries to hold the latest and average temperatures
latest_temperatures = {}
temperature_averages = {}

# RLock and Condition for synchronization
lock = threading.RLock()

def simulate_sensor(sensor_id, queue):
    while True:
        with lock:
            # Simulate temperature readings
            temperature = random.randint(15, 40)
            latest_temperatures[sensor_id] = temperature
            # Put the reading in the queue for processing
            queue.put((sensor_id, temperature))
        time.sleep(1)  # Simulate sensor reading every second

def process_temperatures(queue):
    while True:
        sensor_data = queue.get()
        sensor_id, temperature = sensor_data
        with lock:
            if sensor_id not in temperature_averages:
                temperature_averages[sensor_id] = []
            temperature_averages[sensor_id].append(temperature)
            
            # Calculate the average for the sensor
            avg_temp = sum(temperature_averages[sensor_id]) / len(temperature_averages[sensor_id])
            temperature_averages[sensor_id] = avg_temp
        time.sleep(5)  # Update the average every 5 seconds
