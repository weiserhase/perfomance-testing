
import os
import random

from perf_tester.cperf_test import CPerformanceTester


def gen_data():
    """
    Returns a composite number as a string.
    For example, 997 * 991 = 988027.
    """
    return str(random.randint(100_000, 100_000_000))

def main():
    tester = CPerformanceTester(num_tests=100, gen_data=gen_data, dir = 
 os.path.dirname(os.path.realpath(__file__)))
    
    # Register the three prime factorization programs.
    # Adjust executable paths/extensions as needed for your platform.
    tester.add_program("Prime Factor Naive", "prime_naive.exe", lambda data: [data])
    tester.add_program("Prime Factor Optimized", "prime_optimized.exe", lambda data: [data])
    tester.add_program("Prime Factor Pollard", "prime_pollard.exe", lambda data: [data])
    
    tester.compare_performance()

if __name__ == "__main__":
    main()