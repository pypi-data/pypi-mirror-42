import bisect
import time
from collections import deque


class Scheduler(object):
    """"A timer based on EventLoop class"""
    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.tasks = deque()
        self.running = False

    def add_task(self, deadline, callback):
        """Add task into queue. Tasks are orderly"""
        task = Task(deadline, callback)
        bisect.insort(self.tasks, task)
        self.running = True

    def cancel_task(self):
        """Cancel scheduler: TODO"""
        pass


class Task(object):

    __slots__ = ["deadline", "callback"]

    def __init__(self, deadline, callback):
        self.deadline = time.time() + deadline   # Unit for seconds
        self.callback = callback

    def __eq__(self, other):
        return self.deadline == other.deadline

    def __lt__(self, other):
        return self.deadline < other.deadline

    def __le__(self, other):
        return self.deadline <= other.deadline
