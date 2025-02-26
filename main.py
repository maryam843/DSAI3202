import threading
from queue import Queue
from sensor import simulate_sensor, process_temperatures
from display import initialize_display, update_display

def main():
    # Create a queue to pass sensor data between threads
    queue = Queue()

    # Start threads for sensor simulation
    num_sensors = 3  # Adjust the number of sensors as needed
    sensor_threads = []
    for i in range(num_sensors):
        thread = threading.Thread(target=simulate_sensor, args=(i, queue))
        thread.daemon = True
        sensor_threads.append(thread)
        thread.start()

    # Start the temperature processing thread
    processor_thread = threading.Thread(target=process_temperatures, args=(queue,))
    processor_thread.daemon = True
    processor_thread.start()

    # Start the display thread
    display_thread = threading.Thread(target=update_display)
    display_thread.daemon = True
    display_thread.start()

    # Initialize the display
    initialize_display()

    # Keep the main program running
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
