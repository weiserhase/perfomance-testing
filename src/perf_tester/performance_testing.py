import time
from collections import defaultdict
from collections.abc import Iterable
from typing import Any, Callable, Generic, TypeVar

from perf_tester.statistics import StatsCollection
from perf_tester.utils.progress_bar import ProgressBar

A = TypeVar('A')
T = TypeVar('T')
R = TypeVar('R')

class PerformanceTester(Generic[A]):
    """Compares the performance of multiple functions.
    All registered functions must be linked to a special function that
    transforms the general data to inputs the function can use.
    The statistics are stored in a StatsCollection and pretty printed.
    """

    def __init__(self, num_tests: int, gen_data: Callable[[], A]):
        self.num_tests = num_tests
        self.functions: list[tuple[str, Callable[[A], Any], Callable[[Any], Any]]] = []
        self.generate_data: Callable[[], A] = gen_data
        self.results: dict[str, list[float]] = defaultdict(list)
        self.stats_collection = StatsCollection()

    def add_function(self, name: str, func: Callable[[T], Any], data_func: Callable[[A], T]) -> None:
        """Add one function to test with its name and data preparation function."""
        if not name:
            name = func.__name__
        self.functions.append((name, data_func, func))

    def run_tests(self) -> None:
        prog_bar = ProgressBar(self.num_tests)
        for i in range(self.num_tests):
            prog_bar.update(i)
            data = self.generate_data()
            for name, data_func, func in self.functions:
                special_data = data_func(data)
                start_time = time.perf_counter()
                res = func(special_data)
                if isinstance(res, Iterable):
                    for _ in res:  # type: ignore
                        pass
                end_time = time.perf_counter()
                self.results[name].append(end_time - start_time)

    @staticmethod
    def run_test_mp(func: Callable[[T], R], data_func: Callable[[A], T], data_block: list[A]) -> list[float]:
        return []

    def compare_performance(self) -> None:
        """Runs the tests and prints the results."""
        self.run_tests()

        # Create Stats objects for each function and store them in the stats_collection.
        for name, res in self.results.items():
            self.stats_collection.add_stats(name, res)

        # Print all stats in the stats_collection.
        self.stats_collection.print_all_stats()
        
        
if __name__ == "__main__": 
    pft = PerformanceTester 