# src/square.py

import multiprocessing
import concurrent.futures
import time


def square(num):
    return num * num


def sequential_squares(numbers):
    return [square(num) for num in numbers]


def multiprocessing_squares(numbers):
    with multiprocessing.Pool(processes=len(numbers)) as pool:
        return pool.map(square, numbers)


def pool_map(numbers):
    with multiprocessing.Pool() as pool:
        return pool.map(square, numbers)


def pool_apply(numbers):
    with multiprocessing.Pool() as pool:
        return [pool.apply(square, args=(num,)) for num in numbers]


def concurrent_futures(numbers):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        return list(executor.map(square, numbers))
