"""Среднее задание №8: декоратор замера времени работы функции."""

import functools
import time


def timed(func):
    """Декоратор: измеряет время выполнения функции.

    Результат функции не меняется. Время последнего вызова (в секундах)
    сохраняется в атрибуте wrapper.last_time, а в консоль выводится
    строка вида 'slow_sum выполнена за 0.0123 с'.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            wrapper.last_time = time.perf_counter() - start
            print(f"{func.__name__} выполнена за {wrapper.last_time:.4f} с")

    wrapper.last_time = None
    return wrapper
