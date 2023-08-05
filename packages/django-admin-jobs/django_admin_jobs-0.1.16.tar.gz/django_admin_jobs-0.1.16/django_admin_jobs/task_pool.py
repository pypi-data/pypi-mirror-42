import traceback
import time
from multiprocessing.pool import ThreadPool
from multiprocessing import Lock


def _run_task(fn, args):
    self = args[0]
    args = args[1:]

    # apply using the enter/exit guards
    self.task_entered()
    fn(*args)
    self.task_exited()


class TaskPool:
    def __init__(self, workers):
        self._n_started = 0
        self.workers = workers if workers > 1 else 1
        self._guard_mutex = Lock()
        self.pool = ThreadPool(processes=self.workers)

    def is_full(self):
        return self._n_started == self.workers

    def task_entered(self):
        self._guard_mutex.acquire()
        self._n_started += 1
        self._guard_mutex.release()

    def task_exited(self):
        self._guard_mutex.acquire()
        self._n_started -= 1
        self._guard_mutex.release()

    def add_task(self, fn, args):
        # apply task
        self.pool.apply_async(_run_task, (fn, (self,) + args))
