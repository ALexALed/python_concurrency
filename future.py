from __future__ import annotations
 
import typing as T
from collections import deque
from random import randint
 
Result = T.Any
Burger = Result
Coroutine = T.Callable[[], 'Future']
 
class Future:
    def __init__(self) -> None:
        self.done = False
        self.coroutine = None
        self.result = None
 
    def set_coroutine(self, coroutine: Coroutine) -> None: #A
        self.coroutine = coroutine #A
 
    def set_result(self, result: Result) -> None: #B
        self.done = True #B
        self.result = result #B
 
    def __iter__(self) -> Future:
        return self
 
    def __next__(self) -> Result: #C
        if not self.done: #C
            raise StopIteration #C
        return self.result #C
 
class EventLoop:
    def __init__(self) -> None:
        self.tasks: T.Deque[Coroutine] = deque()
 
    def add_coroutine(self, coroutine: Coroutine) -> None:
        self.tasks.append(coroutine)
 
    def run_coroutine(self, task: T.Callable) -> None:
        future = task() #D
        future.set_coroutine(task) #D
        try: #D
            next(future) #D
            if not future.done: #D
                future.set_coroutine(task) #D
                self.add_coroutine(task) #D
        except StopIteration: #D
            return #D
 
    def run_forever(self) -> None:
        while self.tasks:
            self.run_coroutine(self.tasks.popleft())
 
def cook(on_done: T.Callable[[Burger], None]) -> None: #E
    burger: str = f"Burger #{randint(1, 10)}" #E
    print(f"{burger} is cooked!") #E
    on_done(burger) #E
 
 
def cashier(burger: Burger, on_done: T.Callable[[Burger], None]) -> None: #F
    print("Burger is ready for pick up!") #F
    on_done(burger) #F
 
def order_burger() -> Future:
    order = Future() #G
 
    def on_cook_done(burger: Burger) -> None:
        cashier(burger, on_cashier_done)
 
    def on_cashier_done(burger: Burger) -> None:
        print(f"{burger}? That's me! Mmmmmm!")
        order.set_result(burger)
 
    cook(on_cook_done) #H
    return order
 
if __name__ == "__main__":
    event_loop = EventLoop()
    event_loop.add_coroutine(order_burger)
    event_loop.run_forever()