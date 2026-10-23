"""
Judge Submission Queue & Concurrency Management
"""
import queue
import threading

class SubmissionQueue:
    def __init__(self, max_concurrency: int = 4):
        self.q = queue.PriorityQueue()
        self.max_concurrency = max_concurrency
        self.active_workers = 0
        self._lock = threading.Lock()

    def enqueue(self, submission_id: int, priority: int = 10):
        # Lower priority number = higher execution priority (1 = contest, 10 = practice)
        self.q.put((priority, submission_id))

    def dequeue(self):
        try:
            return self.q.get_nowait()
        except queue.Empty:
            return None

    def size(self) -> int:
        return self.q.qsize()
