import unittest
from backend.queues.submission_queue import SubmissionQueue

class TestSubmissionQueue(unittest.TestCase):
    def test_priority_ordering(self):
        sq = SubmissionQueue()
        sq.enqueue(submission_id=101, priority=10) # Practice
        sq.enqueue(submission_id=999, priority=1)  # Contest
        sq.enqueue(submission_id=202, priority=5)

        first = sq.dequeue()
        self.assertEqual(first[1], 999) # Priority 1 dequeued first

        second = sq.dequeue()
        self.assertEqual(second[1], 202)

    def test_empty_dequeue(self):
        sq = SubmissionQueue()
        self.assertIsNone(sq.dequeue())

    def test_size(self):
        sq = SubmissionQueue()
        sq.enqueue(1)
        sq.enqueue(2)
        self.assertEqual(sq.size(), 2)

if __name__ == "__main__":
    unittest.main()
