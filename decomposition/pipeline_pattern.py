import time
from queue import Queue
from threading import Thread
 
Washload = str
 
class Washer(Thread):
    def __init__(self, in_queue: Queue[Washload], out_queue: Queue[Washload]):
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue
 
    def run(self) -> None:
        while True:
            washload = self.in_queue.get()
            print(f"Washer: washing {washload}...")
            time.sleep(4)
            self.out_queue.put(f'{washload}')
            self.in_queue.task_done()
 
class Dryer(Thread):
    def __init__(self, in_queue: Queue[Washload], out_queue: Queue[Washload]):
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue
 
    def run(self) -> None:
        while True:
            washload = self.in_queue.get()
            print(f"Dryer: drying {washload}...")
            time.sleep(2)
            self.out_queue.put(f'{washload}')
            self.in_queue.task_done()
 
class Folder(Thread):
    def __init__(self, in_queue: Queue[Washload]):
        super().__init__()
        self.in_queue = in_queue
 
    def run(self) -> None:
        while True:
            washload = self.in_queue.get()
            print(f"Folder: folding {washload}...")
            time.sleep(1)
            print(f"Folder: {washload} done!")
            self.in_queue.task_done()
 
class Pipeline:
    def assemble_laundry_for_washing(self) -> Queue[Washload]:
        washload_count = 8
        washloads_in: Queue[Washload] = Queue(washload_count)
        for washload_num in range(washload_count):
            washloads_in.put(f'Washload #{washload_num}')
        return washloads_in
 
    def run_concurrently(self) -> None:
        to_be_washed = self.assemble_laundry_for_washing()
        to_be_dried: Queue[Washload] = Queue()
        to_be_folded: Queue[Washload] = Queue()
 
        Washer(to_be_washed, to_be_dried).start()
        Dryer(to_be_dried, to_be_folded).start()
        Folder(to_be_folded).start()
 
        to_be_washed.join()
        to_be_dried.join()
        to_be_folded.join()
        print("All done!")
 
if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run_concurrently()