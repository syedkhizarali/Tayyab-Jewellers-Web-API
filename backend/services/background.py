from threading import Thread
from queue import Queue
import logging


class BackgroundTasks:
    def __init__(self):
        self.task_queue = Queue()
        self.worker_thread = Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def _worker(self):
        while True:
            try:
                task, args, kwargs = self.task_queue.get()
                task(*args, **kwargs)
                self.task_queue.task_done()
            except Exception as e:
                logging.error(f"Background task failed: {e}")

    def add_task(self, task, *args, **kwargs):
        self.task_queue.put((task, args, kwargs))


# Create a global instance
background = BackgroundTasks()