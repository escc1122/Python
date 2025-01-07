import queue
from gracefully_shutdown.c_queue.base_queue import BaseQueue


class MemoryQueue(BaseQueue):
    def __init__(self):
        self._queue = queue.Queue()

    def put(self, item):
        self._queue.put(item)

    def get(self, block=True, timeout=None):
        return self._queue.get(block=block, timeout=timeout)

    def task_done(self):
        self._queue.task_done()

    def empty(self) -> bool:
        return self._queue.empty()
