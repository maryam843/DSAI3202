import multiprocessing
import time
import random
from src.utils import log_to_file


class ConnectionPool:
    """Manages a pool of database connections with thread-safe access."""

    def __init__(self, size: int):
        self.pool = multiprocessing.Queue()
        for i in range(size):
            self.pool.put(f"DB_Conn_{i}")
        self.usage_log = multiprocessing.Manager().list()

    def get_connection(self) -> str:
        """Acquires a connection from the pool."""
        if self.pool.empty():
            return None
        conn = self.pool.get()
        self.usage_log.append(f"Acquired {conn}")
        return conn

    def release_connection(self, conn: str) -> None:
        """Releases a connection back to the pool."""
        self.pool.put(conn)
        self.usage_log.append(f"Released {conn}")


def access_database(pool: ConnectionPool, process_id: int) -> None:
    """Simulates a process accessing the database."""
    conn = pool.get_connection()

    if conn:
        log_to_file("parallel_logs.txt",
                    f"Process {process_id}: Acquired {conn} ✅")
        time.sleep(random.uniform(1, 2))  # Simulate work
        pool.release_connection(conn)
        log_to_file("parallel_logs.txt",
                    f"Process {process_id}: Released {conn} ❌")
    else:
        log_to_file("parallel_logs.txt",
                    f"Process {process_id}: Waiting for connection... 🕒")
