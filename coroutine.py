from collections import deque
import typing as T
 
Coroutine = T.Generator[None, None, int]
 
class EventLoop:
    def __init__(self) -> None:
        self.tasks: T.Deque[Coroutine] = deque()
 
    def add_coroutine(self, task: Coroutine) -> None: #A
        self.tasks.append(task) #A
 
    def run_coroutine(self, task: Coroutine) -> None:
        try:
            task.send(None) #B
            self.add_coroutine(task)
        except StopIteration: #C
            print("Task completed")
 
    def run_forever(self) -> None: #D
        while self.tasks: #D
            print("Event loop cycle.") #D
            self.run_coroutine(self.tasks.popleft()) #D
 
def fibonacci(n: int) -> Coroutine:
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
        print(f"Fibonacci({i}): {a}")
        yield #E
    return a #F
 
if __name__ == "__main__":
    event_loop = EventLoop()
    event_loop.add_coroutine(fibonacci(5)) #G
    event_loop.run_forever()