# Chapter 6/arcade_machine_multitasking.py
import typing as T
from threading import Thread, Timer, Event
 
from pacman import get_user_input, compute_game_world, render_next_screen
 
processor_free = Event()
processor_free.set()
TIME_SLICE = 0.5
 
 
class Task(Thread):
    def __init__(self, func: T.Callable[..., None]):
        super().__init__()
        self.func = func
 
    def run(self) -> None:
        while True:
            processor_free.wait()
            processor_free.clear()
            self.func()
 
 
class InterruptService(Timer):
    def __init__(self):
        super().__init__(TIME_SLICE, lambda: None)
 
    def run(self):
        while not self.finished.wait(self.interval):
            print("Tick!")
            processor_free.set()
 
 
def arcade_machine() -> None:
    get_user_input_task = Task(get_user_input)
    compute_game_world_task = Task(compute_game_world)
    render_next_screen_task = Task(render_next_screen)
 
    InterruptService().start()
    get_user_input_task.start()
    compute_game_world_task.start()
    render_next_screen_task.start()
 
 
if __name__ == "__main__":
    arcade_machine()