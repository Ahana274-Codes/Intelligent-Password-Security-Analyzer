import threading
import queue
import time
import hashlib


class ConcurrentBreachChecker:
    """
    A high-performance security module that checks a list of passwords
    for compromises concurrently using multi-threaded execution.
    """

    def __init__(self, password_list, num_threads=4):
        self.task_queue = queue.Queue()
        self.num_threads = num_threads
        self.results = {}
        self.lock = threading.Lock()  # Synchronizes writes to shared results memory

        # Populate the shared queue with tasks
        for pwd in password_list:
            self.task_queue.put(pwd)

    def _worker(self):
        """Worker thread loop to consume passwords and evaluate hashes."""
        while not self.task_queue.empty():
            try:
                # Retrieve next task non-blockingly
                password = self.task_queue.get_nowait()
            except queue.Empty:
                break

            # Simulate a performance-intensive cryptographic hashing operation
            hashed_val = hashlib.sha256(password.encode()).hexdigest()

            # Check length/vulnerability parameters
            is_compromised = len(password) < 6 or "123" in password

            # Use explicit thread synchronization for memory protection
            with self.lock:
                self.results[password] = {
                    "sha256": hashed_val,
                    "compromised_flag": is_compromised,
                }

            self.task_queue.task_done()

    def run_system_audit(self):
        """Spawns system worker threads and tracks performance overhead."""
        print(
            f"[SYSTEM] Initializing {self.num_threads} worker threads for parallel security audit..."
        )
        threads = []
        start_time = time.time()

        # Spawn threads
        for i in range(self.num_threads):
            t = threading.Thread(target=self._worker, name=f"SecurityWorker-{i}")
            threads.append(t)
            t.start()

        # Join threads back to main system line execution
        for t in threads:
            t.join()

        execution_time = time.time() - start_time
        print(
            f"[SYSTEM] Audit complete. Processed {len(self.results)} keys in {execution_time:.4f} seconds."
        )
        return self.results


if __name__ == "__main__":
    # Simulate a production runtime environment checking 1,000 requests
    mock_passwords = [f"UserPassword_{i}!@" for i in range(1000)]

    checker = ConcurrentBreachChecker(mock_passwords, num_threads=4)
    audit_log = checker.run_system_audit()
