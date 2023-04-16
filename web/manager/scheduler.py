from typing import List


class Scheduler:
    def __init__(self, queue: List[str]):
        self.queue = queue

    def next(self) -> str:
        raise NotImplementedError

    def null(self) -> bool:
        return len(self.queue) == 0
    
    def length(self) -> int:
        return len(self.queue)


class DefaultScheduler(Scheduler):
    def next(self) -> str:
        return self.queue.pop(0)
