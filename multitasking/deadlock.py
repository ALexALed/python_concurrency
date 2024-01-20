import time
from threading import Thread, Lock


THREAD_DELAY = 0.1
dumplings = 20


class Philosopher(Thread):
    def __init__(
        self, name: str, left_chopstick: Lock, right_chopstick: Lock
    ):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick  # A
        self.right_chopstick = right_chopstick  # A

    def run(self) -> None:
        global dumplings

        while dumplings > 0:  # B
            self.left_chopstick.acquire()  # C
            print(
                f"{self.left_chopstick} grabbed by {self.name} "
                f"now needs {self.right_chopstick}"
            )
            self.right_chopstick.acquire()  # D
            print(f"{self.right_chopstick} grabbed by {self.name}")
            dumplings -= 1  # E
            print(f"{self.name} eats a dumpling. " f"Dumplings left: {dumplings}")
            self.right_chopstick.release()  # F
            print(f"{self.right_chopstick} released by {self.name}")
            self.left_chopstick.release()  # G
            print(f"{self.left_chopstick} released by {self.name}")
            print(f"{self.name} is thinking...")
            time.sleep(0.1)


if __name__ == "__main__":
    chopstick_a = Lock()
    chopstick_b = Lock()

    philosopher_1 = Philosopher("Philosopher #1", chopstick_a, chopstick_b)
    philosopher_2 = Philosopher("Philosopher #2", chopstick_b, chopstick_a)

    philosopher_1.start()
    philosopher_2.start()
