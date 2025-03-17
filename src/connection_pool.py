# src/connection_pool.py

import multiprocessing
import time
import random


class ConnectionPool:
    def __init__(self, max_connections):
        self.semaphore = multiprocessing.Semaphore(max_connections)
        self.connections = ["Connection-" + str(i) for i in range(1, max_connections + 1)]

    def get_connection(self):
        self.semaphore.acquire()
        connection = self.connections.pop(0)
        return connection

    def release_connection(self, connection):
        self.connections.append(connection)
        self.semaphore.release()


def access_database(pool, process_id):
    connection = pool.get_connection()
    print(f"Process {process_id} acquired {connection}")
    time.sleep(random.uniform(1, 3))  # Simulate work
    print(f"Process {process_id} released {connection}")
    pool.release_connection(connection)
