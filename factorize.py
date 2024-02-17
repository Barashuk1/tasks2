from multiprocessing import Pool, cpu_count
from time import time


def calculate_factors(number):
    factors = [i for i in range(1, number + 1) if number % i == 0]
    return factors


def factorize_parallel(numbers):
    num_processes = cpu_count()
    pool = Pool(processes=num_processes)
    results = pool.map(calculate_factors, numbers)
    pool.close()
    pool.join()
    return results


def factorize(*numbers):
    results = []
    for number in numbers:
        factors = calculate_factors(number)
        results.append(factors)
    return results


if __name__ == "__main__":
    numbers = [128, 255, 99999, 10651060]

    start_time = time()
    a, b, c, d = factorize_parallel(numbers)
    end_time = time()
    print(f"Parallel Execution Time: {end_time - start_time} seconds")

    start_time = time()
    a, b, c, d = factorize(*numbers)
    end_time = time()
    print(f"Synchronous Execution Time: {end_time - start_time} seconds")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790,
                 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
