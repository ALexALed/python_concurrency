import os
import time
import typing as T
from multiprocessing.pool import ThreadPool
 
def search_file(file_location: str, search_string: str) -> bool:
    with open(file_location, "r", encoding="utf8") as file:
        return search_string in file.read()
 
def search_files_concurrently(file_locations: T.List[str],
                              search_string: str) -> None:
    with ThreadPool() as pool:
        results = pool.starmap(search_file,
                               ((file_location, search_string) for
                                file_location in file_locations))
        for result, file_name in zip(results, file_locations):
            if result:
                print(f"Found string in file: `{file_name}`")
 
if __name__ == "__main__":
    file_locations = list(
        glob.glob(f"{os.path.abspath(os.getcwd())}/books/*.txt"))
    search_string = input("What word are you trying to find?: ")
 
    start_time = time.perf_counter()
    search_files_concurrently(file_locations, search_string)
    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}")